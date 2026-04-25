# 📄 Document Intelligence Workspace

A Streamlit app that lets you upload documents (PDF, DOCX, TXT) and runs three AI agents collaboratively to extract insights using a local LLM via Ollama.

## Agents

| Agent | What it does |
|---|---|
| 🧠 **Summary Agent** | Overview, key topics, document type & tone |
| 🚨 **Red Flag Detector** | Legal risks, vague terms, inconsistencies, missing info |
| ✅ **Decision Extractor** | Decisions, obligations, action items, deadlines |

---

## Project Structure

```
doc_intelligence/
├── app.py            # Streamlit UI
├── extractor.py      # PDF / DOCX / TXT text extraction
├── agents.py         # Agent prompts + chunking logic
├── ollama_client.py  # Ollama HTTP client
├── storage.py        # Save/load analyses as JSON
├── requirements.txt
└── analyses/         # Auto-created, stores JSON results
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Install and run Ollama

```bash
# Install from https://ollama.com
ollama pull llama3      # or mistral, phi3, gemma, etc.
ollama serve
```

> Change the model in the sidebar or edit `DEFAULT_MODEL` in `ollama_client.py`.

### 3. Run the app

```bash
streamlit run app.py
```

---

## How to Use

1. Upload a **PDF**, **DOCX**, or **TXT** file
2. Select which agents to run in the sidebar
3. Click **🚀 Run Analysis**
4. View the collaborative insights from all agents
5. All analyses are saved and visible in **Past Analyses**

---

## Large Document Handling

For documents exceeding ~8,000 characters, the app automatically:
- Splits the document into chunks
- Runs each agent on every chunk
- Synthesizes the partial results into a final unified output

---

## Notes

- No external API keys required — runs fully locally via Ollama
- Analyses are stored as JSON files in the `analyses/` folder
- Supports any Ollama-compatible model (llama3, mistral, phi3, gemma2, etc.)
