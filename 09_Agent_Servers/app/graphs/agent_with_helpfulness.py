from __future__ import annotations
from typing import TypedDict

from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langgraph.graph import START, StateGraph, END, MessagesState

from app.models import get_chat_model
from app.tools import get_tool_belt
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain_core.runnables import RunnableConfig

SYSTEM_PROMPT = (
    "You are a helpful assistant specialized in feline (cat) health. "
    "Use the retrieve_information tool for cat-health questions, web search for "
    "current information, and Arxiv for research papers. Cite tool results when "
    "they inform your answer."
)

assistant = create_agent(
    model=get_chat_model(),
    tools=get_tool_belt(),
    system_prompt=SYSTEM_PROMPT,
)

class AssistantState(MessagesState):
    answer: str
    help_check_count: int
    helpful_flag: bool

class HelpfulnessResponse(TypedDict):
    is_helpful: bool


llm = get_chat_model()


def ask_assistant(state: AssistantState, config: RunnableConfig):

    count = 0 if not "help_check_count" in state.keys() else state["help_check_count"]
    result = assistant.invoke(state, config={"tags": ["nostream"]})
    return {"answer": result["messages"][-1].content, "help_check_count": count}

def confirm_helpfulness(state: AssistantState, config: RunnableConfig):
    helpful_bool = llm.with_config(tags=["langsmith:nostream"]).with_structured_output(HelpfulnessResponse).invoke(f"Was this response helpful? Question: {state["messages"][0].content}, Answer: {state['answer']}", config={"tags": ["nostream"]})
    
    #UNCOMMENT TO TEST HELP CHECK LIMIT
    #helpful_bool = {"is_helpful": False}
    
    help_check_count = state["help_check_count"]
    if helpful_bool["is_helpful"]:
        return {"helpful_flag": helpful_bool, "help_check_count": state["help_check_count"]+1, "messages": [AIMessage(content=state["answer"])]}
    elif not helpful_bool["is_helpful"] and help_check_count < 2:
        return {"helpful_flag": helpful_bool, "help_check_count": state["help_check_count"]+1}
    else:
        return {"helpful_flag": helpful_bool, "help_check_count": state["help_check_count"]+1, "messages":  [AIMessage(content="I'm sorry, I can't help with that.")]}
    
def route_after_judge(state: AssistantState, config: RunnableConfig):
    help_check_count = state["help_check_count"]
    is_helpful = state["helpful_flag"]["is_helpful"]
    if not is_helpful and help_check_count < 3:
        return "assistant"
    return "end"

builder = StateGraph(AssistantState)
builder.add_node("assistant", ask_assistant)
builder.add_node("judge", confirm_helpfulness)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", "judge")
builder.add_conditional_edges("judge", route_after_judge, {"assistant": "assistant","end": END})
graph = builder.compile()


# Build an `agent_with_helpfulness` graph that adds a post-response helpfulness check: 
# after the agent answers, a judge model decides whether the response is helpful, and 
# if not, the graph loops back for another attempt (with a safe loop limit). 
# Register it in `langgraph.json`, deploy it, then compare LangSmith traces for 
# queries that pass vs. fail the helpfulness check. Does the retry loop behave differently in Studio vs. production?