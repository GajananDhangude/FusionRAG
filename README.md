# 🔍 Hybrid RAG — Document Q&A System

A production-grade Retrieval-Augmented Generation system built from scratch — no LangChain. Combines dense, sparse, and late interaction retrieval with a React frontend and Qdrant vector database.

---

## Overview

Most RAG systems rely on a single retrieval method. This system uses a **three-stage hybrid pipeline** — BM25 sparse search handles keyword matching, BGE dense embeddings handle semantic similarity, and ColBERT late interaction reranks the final candidates using token-level MaxSim scoring.

The entire stack is evaluated using RAGAS with 20 benchmark questions derived from the "Attention Is All You Need" paper.

---

## RAGAS Evaluation Results

| Metric | Score |
|---|---|
| Faithfulness | **0.979** |
| Answer Relevancy | **0.863** |
| Context Recall | **0.778** |
| Context Precision | **0.742** |

> Evaluated on 20 held-out questions from the "Attention Is All You Need" paper.

---

## How It Works

```
User Query
    │
    ├── BM25 sparse search (Qdrant/bm25 via fastembed)     → top 20 candidates
    ├── Dense semantic search (BAAI/bge-small-en-v1.5)     → top 20 candidates
    │
    └── ColBERT late interaction reranking (colbertv2.0)
            └── MAX_SIM token-level scoring
                    └── Top 3–5 chunks → LLM → Answer
```

**Why three stages?**
- BM25 catches exact keyword matches that dense retrieval misses
- Dense retrieval catches semantic similarity that BM25 misses  
- ColBERT reranks using fine-grained token-level interaction — more precise than either alone

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Frontend | React |
| Vector DB | Qdrant |
| Dense Embeddings | `BAAI/bge-small-en-v1.5` via fastembed |
| Sparse Embeddings | `Qdrant/bm25` via fastembed |
| Reranker | `colbertv2.0` — late interaction, MAX_SIM |
| LLM | Groq / OpenAI |
| Evaluation | RAGAS |
| Containerization | Docker Compose |

---

## API Endpoints

### `POST /ingest`
Upload and index a document. Supported formats: `.pdf`, `.txt`, `.docx`.

```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@attention-paper.pdf"
```

```json
{
  "message": "File uploaded and indexed. Ready to chat.",
  "path": "./uploads/attention-paper.pdf"
}
```

### `POST /chat`
Query the indexed document.

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What BLEU score did the Transformer achieve?"}'
```

```json
{
  "question": "What BLEU score did the Transformer achieve?",
  "answer": "The Transformer big model achieved 28.4 BLEU on WMT 2014 English-to-German.",
  "source": "attention-paper.pdf"
}
```

### `GET /`
Health check — returns server status and currently active document.

---

## Quickstart

**Prerequisites:** Docker and Docker Compose installed.

```bash
# 1. Clone the repo
git clone https://github.com/your-username/hybrid-rag.git
cd hybrid-rag

# 2. Add your API key
echo "GROQ_API_KEY=your_key_here" > .env

# 3. Start the full stack
docker compose up --build
```

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Qdrant Dashboard: `http://localhost:6333/dashboard`

---

## Running Evaluation

```bash
# Install eval dependencies
pip install ragas datasets

# Run RAGAS evaluation
python evaluate.py
```

Expected output:
```
faithfulness         0.979167
answer_relevancy     0.863067
context_precision    0.741667
context_recall       0.777500
```

---

## Key Engineering Decisions

**Why no LangChain?**  
Built all retrieval, chunking, and generation logic from scratch to have full control over each stage and avoid abstraction overhead that makes debugging harder.

**Why ColBERT over cross-encoder reranking?**  
ColBERT pre-computes document token embeddings at index time, making reranking significantly faster at query time compared to cross-encoders that require full query-document pairs on every request.

**Why `Qdrant/bm25` over `Modifier.IDF`?**  
`Modifier.IDF` applies only IDF weighting internally — missing TF, k1, b, and document length normalization. `Qdrant/bm25` via fastembed computes the full BM25 formula before indexing, giving significantly better sparse retrieval quality.

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key for LLM generation |
| `QDRANT_URL` | Qdrant instance URL (default: `http://localhost:6333`) |
| `UPLOAD_DIR` | Directory for uploaded files (default: `./uploads`) |

---

## License

Apache License