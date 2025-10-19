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

## Context injection strategy

This project usese context-injection using Wikipedia as a grounding source. The project uses Python's `wikipedia` package to retrieve several sentences on the topic as context, which is injected into the prompt.