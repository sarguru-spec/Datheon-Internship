# 🚀 Datheon Generative AI Internship Portfolio

Welcome to my Generative AI & LangChain Internship project repository! This repository contains a series of production-ready AI applications built from scratch, demonstrating expertise in LLM integration, RAG pipelines, and autonomous agentic workflows.

---

## 🌟 Project Overview

This project is divided into modular, scalable tasks that solve real-world AI engineering challenges:

### ✅ Task 1: Secure LLM JSON Extractor
- Extracts structured data from raw text or PDF documents.
- Uses **Pydantic** for strict, reliable JSON schema validation.
- Implements enterprise-grade security with `.env` variable management and `.gitignore` best practices.
- *Files:* `task1.py`, `task1_pdf.py`

### ✅ Task 2: RAG Document Q&A Pipeline
- A Retrieval-Augmented Generation (RAG) system that allows users to "chat" with PDF documents.
- Chunks documents, generates vector embeddings, and stores them in a local **ChromaDB** vector database.
- Prevents LLM hallucinations by grounding answers strictly in the retrieved document context.
- *Files:* `task2_rag.py`

### ✅ Task 3: Multi-Tool Autonomous AI Agent
- A ReAct (Reasoning + Acting) framework agent capable of multi-step problem solving.
- Equipped with custom tools:
  - 🔍 **Web Search** (via DuckDuckGo)
  - 🧮 **Python Calculator** (for complex math/code execution)
  - 📂 **Local File Reader** (to parse local text files dynamically)
- Prints the full reasoning chain (Thought → Action → Observation → Final Answer) in the console.
- *Files:* `agent_core.py`, `main.py`

### 🎨 Task 4: Interactive Streamlit UI (In Progress)
- A beautiful, real-time web interface to interact with the Autonomous Agent.
- Features live reasoning steps, typing effects, and conversation memory.
- *Files:* `app.py`

---

## 🛠️ Tech Stack

- **Language:** Python 3.12
- **LLM Provider:** Google Gemini API (`gemini-3.8-flash`)
- **Orchestration:** LangChain & LangChain Experimental
- **Vector Database:** ChromaDB
- **Validation:** Pydantic
- **Web UI:** Streamlit
- **Tools:** DuckDuckGo Search, PyPDF

---

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sarguru-spec/Datheon-Internship.git
   cd Datheon-Internship
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv

   # macOS / Linux
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key.** Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_api_key_here
   # Optional: override the default model if it is ever retired
   # GEMINI_MODEL=gemini-3.8-flash
   ```
   Get a free key from [Google AI Studio](https://aistudio.google.com/). The `.env` file is listed in `.gitignore`, so your key is never committed.

---

## ▶️ Running the Projects

| Task | Command |
|------|---------|
| Task 1 – JSON extractor (text) | `python task1.py` |
| Task 1 – JSON extractor (PDF) | `python task1_pdf.py` |
| Task 2 – RAG Q&A over a PDF | `python task2_rag.py` |
| Task 3 – Multi-tool agent (console) | `python main.py` |
| Task 4 – Streamlit chatbot | `streamlit run app.py` |

### Try the agent (Task 3)

Place a text file such as `sample_resume.txt` in the project root, then ask compound questions that force the agent to chain tools:

```text
❓ You: Read sample_resume.txt, count how many skills are listed, then search the web for the most in-demand AI skill this year.
❓ You: What is (4829 * 17) + sqrt(2025)? Use Python to be sure.
❓ You: Who is the current CEO of Google, and what is his age multiplied by 3?
```

Type `exit` to quit.

---

## 📁 Project Structure

```text
Datheon-Internship/
├── task1.py            # Pydantic JSON extractor (text)
├── task1_pdf.py        # Pydantic JSON extractor (PDF)
├── task2_rag.py        # RAG pipeline with ChromaDB
├── agent_core.py       # Tools, ReAct prompt and agent builder (Task 3)
├── main.py             # Console agent (Task 3)
├── app.py              # Streamlit UI (Task 4)
├── requirements.txt
├── .env                # Your secrets (not committed)
└── .gitignore
```

---

## 🔒 Security Notes

- API keys are loaded from `.env` and never hard-coded.
- `.env`, local vector stores (e.g. `chroma_db/`) and virtual environments are git-ignored.
- The Python calculator tool executes code on the host machine. Run the agent locally and do not expose it publicly without sandboxing.

---

## 🗺️ Roadmap

- [x] Task 1: Secure LLM JSON Extractor
- [x] Task 2: RAG Document Q&A Pipeline
- [x] Task 3: Multi-Tool Autonomous AI Agent
- [x] Task 4: Streamlit UI with streaming output and conversation memory

---

## 👤 Author

**Sarguru M**
- GitHub: [@sarguru-spec](https://github.com/sarguru-spec)
- LinkedIn: [linkedin.com/in/sargurum](https://linkedin.com/in/sargurum)