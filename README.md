# Knowledge Quiz

This small project is built around a simple, modular architecture to make iterating on quiz generation and evaluation fast and safe. The primary text-generation work is performed by a local Ollama server running the `llama3.2:3b` model; this was chosen after briefly testing an OpenAI-hosted model because Ollama lets development happen entirely offline and without API keys, which simplifies iteration and debugging. The system expects the LLM output to be formatted as JSON so downstream code can parse it deterministically — the `quiz.py` module requests and validates JSON responses to keep parsing simple and robust.

## Installation

### Install Ollama

Visit [https://ollama.ai](https://ollama.ai) and download Ollama for your operating system:

**macOS:**
```bash
# Download and install from https://ollama.ai
# Or use Homebrew:
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download the installer from [https://ollama.ai](https://ollama.ai)

### Pull the Required Model

Download the Llama 3.2 3B model:
```bash
ollama pull llama3.2:3b
```

## Running the Application

### Start Ollama Server

In a terminal window, start the Ollama server:
```bash
ollama serve
```

Keep this terminal open - the server needs to be running for the quiz generator to work.

### Run the Quiz Generator

In another terminal window:
```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the quiz generator
python main.py
```

Code is split into small, focused modules to keep responsibilities clear: `llm.py` encapsulates all interactions with the language model (prompt construction, HTTP calls to the local Ollama endpoint, and basic response validation), `quiz.py` contains the quiz-manipulation logic (question/choice handling, scoring, and presentation), and `main.py` performs top-level orchestration and CLI handling. This separation makes it straightforward to replace or mock any single piece (for example, swapping the model client or unit-testing quiz scoring) and keeps the repository easy to navigate on GitHub.

## Highlights

- Uses a local Ollama server with the `llama3.2:3b` model for quick, offline iteration.
- Responses are requested and validated as JSON for predictable, easy parsing.
- Clear file separation: `llm.py` for LLM logic, `quiz.py` for quiz operations, and `main.py` for top-level control and CLI.

## Planned RAG expansion

I'd like to expand the project to include a Wikipedia-based Retrieval-Augmented Generation (RAG) pipeline to improve answer accuracy and provide citations. The high-level plan:

- Ingestion: crawl or download a snapshot of relevant Wikipedia articles (either via the MediaWiki API or pre-built dumps). Split articles into smaller chunks (e.g., 500–1,000 tokens) with overlap for context continuity.
- Vector store: embed the chunks with an embedding model (local or remote) and store them in a fast similarity index (FAISS, Milvus, or Weaviate). Keep this logic in a new module, e.g., `store.py` or `retriever.py`.
- Retrieval: extend `llm.py` to accept an optional `context` parameter or add a `retriever` helper that returns the top-k passages for a prompt. When generating quizzes or explanations, the main flow would call the retriever first, then build a prompt that includes the retrieved passages as grounding material.
- Prompting & citation: update prompt templates so the model must ground answers in the provided passages and return citation snippets (e.g., article title + sentence offset). Parse the structured response (still JSON) to include citations alongside each question's explanation.

This design keeps the existing modular separation: `llm.py` remains responsible for calling the model, `quiz.py` can be extended to accept and render citations, and a new `retriever.py`/`store.py` handles the indexing and search lifecycle. The RAG layer could be toggled via a CLI flag in `main.py` so experiments can run with or without external context.