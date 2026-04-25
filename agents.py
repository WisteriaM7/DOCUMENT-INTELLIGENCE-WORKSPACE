from ollama_client import call_ollama

# ── Prompt templates ──────────────────────────────────────────────────────────

PROMPTS = {
    "Summary": """You are a Summary Agent. Your job is to read a document and produce a clear, structured summary.

Document Text:
{text}

Provide:
1. **One-paragraph overview** (3–5 sentences)
2. **Key topics covered** (bullet list)
3. **Main arguments or narratives** (bullet list)
4. **Document type and tone** (e.g., legal contract, news article, academic paper, business report)

Be concise and accurate. Do not add information not present in the document.""",

    "RedFlag": """You are a Red Flag Detector Agent. Your job is to read a document and identify anything that could be risky, problematic, concerning, or worth scrutiny.

Document Text:
{text}

Identify and list:
1. **Legal or compliance risks** (ambiguous clauses, missing protections, liability issues)
2. **Financial risks** (unusual payment terms, penalties, hidden costs)
3. **Logical inconsistencies or contradictions** in the document
4. **Vague or undefined terms** that could cause disputes
5. **Missing information** that should normally be present
6. **Unusual or one-sided clauses** that favor one party heavily

For each red flag, explain briefly WHY it is a concern.
If no red flags are found in a category, say "None detected."
Be specific and cite the relevant section or phrase when possible.""",

    "Decision": """You are a Decision Extractor Agent. Your job is to identify all decisions, commitments, action items, and deadlines in a document.

Document Text:
{text}

Extract and organize:
1. **Key decisions made** (what was decided, by whom if mentioned)
2. **Commitments and obligations** (who must do what)
3. **Action items** (concrete tasks or next steps)
4. **Deadlines and dates** (specific dates, timeframes, or milestones)
5. **Conditions and dependencies** (if X then Y, subject to approval, etc.)
6. **Signatories or responsible parties** (names, roles, or entities)

Present each item clearly. If information is not present, say "Not specified."
Focus only on what is explicitly stated in the document.""",
}

# ── Chunking for large documents ──────────────────────────────────────────────

MAX_CHARS = 8000  # safe context limit for most local models


def chunk_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Split text into chunks that fit within model context."""
    if len(text) <= max_chars:
        return [text]

    chunks = []
    while len(text) > max_chars:
        split_at = text.rfind("\n", 0, max_chars)
        if split_at == -1:
            split_at = max_chars
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip()
    if text:
        chunks.append(text)
    return chunks


def run_agent(text: str, agent_name: str, model: str = "llama3") -> str:
    """
    Run a single named agent on the document text.
    For large documents, chunks are processed and results merged.
    """
    if agent_name not in PROMPTS:
        return f"Unknown agent: {agent_name}"

    prompt_template = PROMPTS[agent_name]
    chunks = chunk_text(text)

    if len(chunks) == 1:
        prompt = prompt_template.format(text=chunks[0])
        return call_ollama(prompt, model)

    # Multi-chunk: run agent on each chunk, then synthesize
    partial_results = []
    for i, chunk in enumerate(chunks):
        chunk_prompt = prompt_template.format(text=chunk)
        result = call_ollama(chunk_prompt, model)
        partial_results.append(f"[Chunk {i+1}/{len(chunks)}]\n{result}")

    # Synthesis prompt
    combined = "\n\n".join(partial_results)
    synthesis_prompt = (
        f"You are a {agent_name} Agent. Below are partial analyses of a large document "
        f"split into {len(chunks)} chunks. Synthesize them into a single coherent final output "
        f"without repeating yourself.\n\nPartial Analyses:\n{combined}"
    )
    return call_ollama(synthesis_prompt, model)
