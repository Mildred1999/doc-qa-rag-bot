# Document Q&A RAG Bot

A retrieval-augmented generation (RAG) system that answers natural language questions over a real software documentation corpus, with every answer grounded in and citing the exact source chunks it was generated from.

<!-- ## Why this project exists

Most RAG tutorials wrap everything in a framework like LangChain, which hides the actual mechanics of how retrieval-augmented generation works. This project is built from scratch in plain Python to demonstrate real understanding of each stage of the pipeline: document ingestion, chunking strategy, embedding generation, vector search, and grounded generation with source attribution. -->

## How it works

1. **Ingestion** — documentation files are recursively loaded from two open-source projects, each using a different markup format.
2. **Chunking** — files are split by header structure first (so related content stays together), with a fixed-size fallback and overlap for sections that are too long to embed as a single chunk.
3. **Embedding** — each chunk is converted into a vector representation using a local sentence-transformer model.
4. **Indexing** — chunks, their embeddings, and metadata (source file, section, chunk index) are stored in a persistent vector database.
5. **Retrieval** — a user's question is embedded the same way, and the most semantically similar chunks are retrieved via vector search.
6. **Generation** — the retrieved chunks are passed to an LLM with instructions to answer only from that context and cite which chunks it used.
7. **Interface** — a simple web UI lets a user ask a question and see the answer alongside its cited sources and the raw retrieved context.

## Corpus

Documentation from two open-source Python HTTP libraries, chosen for their real-world messiness and structural differences:

- [Requests](https://github.com/psf/requests) — `.rst` (reStructuredText) files, header style detected via text-plus-underline pattern matching
- [httpx](https://github.com/encode/httpx) — `.md` (Markdown) files, header style detected via `#` syntax

Using two different markup formats in one corpus means the ingestion pipeline has to normalize header detection across both, rather than assuming a single consistent format — a more realistic version of the problem than most single-source tutorials.

## Tech stack

| Component | Choice | Why |
|---|---|---|
| LLM | [Groq API](https://console.groq.com) | Free tier, very fast inference, OpenAI-compatible request format (transfers directly to future agent/tool-calling work) |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) | Small and fast enough to run locally on CPU, no API cost |
| Vector store | ChromaDB | Runs locally, no external service or cost, simple Python API |
| Orchestration | Plain Python (no LangChain) | Forces direct understanding of chunking, retrieval, and prompt construction rather than relying on framework abstractions |
| Interface | Streamlit | Lightweight way to expose the pipeline as a usable, shareable demo |

## Setup

```bash
git clone <this-repo-url>
cd doc-qa-rag-bot
conda create --name ragbot python=3.11
conda activate ragbot
pip install -r requirements.txt
```

Create a `.env` file in the project root with your own free Groq API key:
```
GROQ_API_KEY=your_key_here
```

Usage instructions (running ingestion, launching the app) will be added once the pipeline is complete end-to-end.

## License

MIT