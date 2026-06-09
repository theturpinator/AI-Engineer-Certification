<p align = "center" draggable="false" ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719"
     width="200px"
     height="auto"/>
</p>

<h1 align="center" id="heading">Session 1: Dense Vector Retrieval</h1>

### [Quicklinks]()

| 📰 Module Sheet                                                                 | ⏺️ Recording | 🖼️ Slides | 👨‍💻 Repo       | 📝 Homework | 📁 Feedback |
| :------------------------------------------------------------------------------- | :----------- | :-------- | :------------ | :---------- | :---------- |
| [Dense Vector Retrieval](../00_Docs/Modules/01_Dense_Vector_Retrieval/README.md) |[Recording!](https://us02web.zoom.us/rec/share/sHWvo0Nd1aI0SEhKecOLEX9kFGVJJAdYfsKiuTmm8t85W48Z2lnjpnzTy8jAd8R5.PwuqibGwAZhvDd8c) <br> passcode: `C62n^@Q!`| [Session 1 Slides](https://canva.link/htfqf8i39yejyhn) | You are here! | [Session 1 Assignment](https://forms.gle/Z9qskfVaAvPjn6gz8) | [Feedback 6/2](https://forms.gle/21a2uoL9DVZPwgJP6) |


## 🏗️ How AIM Does Assignments

> 📅 **Assignments will always be released to students as live class begins.** We will never release assignments early.

Each assignment will have a few of the following categories of exercises:

- ❓ **Questions** - these will be questions that you will be expected to gather the answer to. These can appear as general questions, or questions meant to spark a discussion in your breakout rooms.

- 🏗️ **Activities** - these will be work or coding activities meant to reinforce specific concepts or theory components.

- 🚧 **Advanced Builds (optional)** - Take on a challenge. These builds require you to create something with minimal guidance outside of the documentation.

## Main Assignment

In this assignment, you will build a vector RAG application using LangChain v1, OpenAI embeddings, and Qdrant.

The main notebook is:

```text
01_Cat_Health_Vector_RAG_LangChain_Qdrant.ipynb
```

The notebook uses the bundled cat health guideline PDF in `data/cat_health_guidelines.pdf`.

### Setup

From this folder, install the environment with uv:

```bash
uv sync
```

Then open the notebook in Cursor or VS Code and select the Python/Jupyter environment created by uv.

You will also need an OpenAI API key available when running the notebook.

---

## 🏗️ Activity #1: Embedding Similarity

Run the embedding similarity primer in the notebook.

You will compare embeddings for terms like:

- `king`
- `queen`
- `banana`
- `cat`
- `veterinarian`
- `cat health guidelines`

#### ❓Question #1

Why is cosine similarity useful for dense vector retrieval?

##### ✅ Answer:

Cosine similary is useful because, as opposed to keyword search, we do not require an exact match. This means we can find out if 2 items are similar to one another, but not identical. We can identify peices of information that are "close" to the user query to identify data that may be contextually relevant and helpful in answering their query.

---

## 🏗️ Activity #2: Build the Vector RAG Pipeline

Run the notebook sections that:

1. Load the PDF into LangChain `Document` objects
2. Split the document into chunks
3. Embed the chunks
4. Store the chunk embeddings in in-memory Qdrant
5. Retrieve relevant chunks with similarity scores
6. Generate an answer grounded in retrieved context

#### ❓Question #2

Why is metadata important for a RAG application?

##### ✅ Answer:
Auditability - this will allow us to identify the document source of the chunk to cite our sources

Freshness - if maintaining a timestamp of when the document was loaded, we can know which documents are more recent.

Filtering - if we tag metadata surrounding the document, we can narrow the search to those documents of a specific category, for example (e.g. if have an "animal" metadata attribute, we can filter for "cat" specifically)

#### ❓Question #3

What tradeoff do we make when choosing chunk size and chunk overlap?

##### ✅ Answer:
Too small of a chunk would result in not enough context to capture any significant meaning or failure to establish an over-arching concept for a text chunk. Too large of a chunk would mean there are too many concepts discussed in a single vector, losing the ability to precisely capture what is relevant to the user query. 

Too little overlap between chunks could lead to splitting one single talking point in a document into multiple chunks - with overlap we reduce the risk of missing pertinent context in each chunk. However, the tradeoff is more redundancy between chunks. A large amount of overlap could make for less useful results (e.g., a high number of relevant chunks for any given query) and wasted space in the database, since we'll need more vectors to represent the entire document.

#### ❓Question #4

What does a similarity score help you understand, and what does it not prove by itself?

##### ✅ Answer:
The similarity score shows the cosine similarity between the embedding vector retrieved from Qdrant and the retrieval query. This is essentially the semantic simlarity between the two. However, this does not tell us how relevant the document is to the query, or how useful the provided information is. For example, if the vector DB contained the identical literal string of the user's prompt, I would expect a similarity score of 1, but this doesn't provide any useful additional context to answer the query.

---

## 🏗️ Activity #3: Vibe Check Retrieval Quality

Run the notebook's vibe check queries and inspect both:

- The retrieved context
- The generated answer

#### ❓Question #5

For the vibe check queries, did the retrieved context seem relevant before generation? Why or why not?

##### ✅ Answer:
It did feel relevant. For the preventative care question, all of the feedback was directly related to the query. Likewise for the questions regarding symptoms warranting veterinarian care and feeding directions. However, I think the answer for feeding instructions was a little too verbose and had information for obese cats, which may not be needed since the user mentioned the cat was healthy. For the question about filing taxes, the model responded that it could not help with that, as expected.
---

## 🏗️ Activity #4: Tune Retrieval

Improve retrieval quality by changing one or more of:

- Chunk size
- Chunk overlap
- Retrieval `k`
- Query wording

Document what changed and whether retrieval improved.

##### Settings Changed:

- Setting changed: chunk_size
- Before: 1000
- After: 2000

##### Results:

- Did retrieval improve? Why or why not? Yes, retrieval improved. The similarity scores for the top 4 chunks increased improved slightly. Also, while subjective, the quality of the responses seemed to improve - they are more coherent an have complete ideas instead of more fragmented suggestions.
---

## Optional Deep Dive: RAG From Scratch

If you want to look underneath the library abstractions, run the optional reference notebook:

```text
02_Cat_Health_Vector_RAG_From_Scratch.ipynb
```

It builds the same retrieval pipeline again with only:

- `pypdf` for extracting text from the PDF
- Python standard-library HTTP requests for calling OpenAI
- Handcrafted document, chunking, embedding, similarity-search, vector-store, and generation primitives

This notebook is a reference walkthrough, not an additional assignment. Its purpose is to make the responsibilities hidden by LangChain, Qdrant, and provider SDKs visible.

---

## Submitting Your Homework

### Main Assignment

Follow these steps to prepare and submit your homework:

1. Pull the latest updates from upstream into the main branch of your AIE9 repo:

```bash
git checkout main
git pull upstream main
git push origin main
```

2. Start Cursor from the `01_Dense_Vector_Retrieval` folder.
3. Complete the notebook.
4. Answer the questions in this `README.md`.
5. Add, commit, and push your modified work to your origin repository.

When submitting your homework, provide the GitHub URL to your AIE9 repo.
