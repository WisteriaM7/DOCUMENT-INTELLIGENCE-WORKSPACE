import streamlit as st
from extractor import extract_text
from agents import run_agent
from storage import save_analysis, load_all_analyses, clear_all_analyses

st.set_page_config(page_title="Document Intelligence Workspace", page_icon="📄", layout="wide")

AGENT_META = {
    "Summary":  ("🧠", "Summary Agent"),
    "RedFlag":  ("🚨", "Red Flag Detector"),
    "Decision": ("✅", "Decision Extractor"),
}


def display_results(results: dict):
    for agent_key, output in results.items():
        emoji, label = AGENT_META.get(agent_key, ("🤖", agent_key))
        st.markdown(f"### {emoji} {label}")
        st.markdown(output)
        st.divider()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    model = st.text_input("Ollama Model", value="llama3")

    st.divider()
    st.subheader("🗂 Select Agents")
    use_summary  = st.checkbox("🧠 Summary Agent",      value=True)
    use_redflag  = st.checkbox("🚨 Red Flag Detector",  value=True)
    use_decision = st.checkbox("✅ Decision Extractor", value=True)

    st.divider()
    if st.button("🗑️ Clear All Analyses", use_container_width=True):
        clear_all_analyses()
        st.success("Cleared.")
        st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📄 Document Intelligence Workspace")
st.caption("Upload a document and let AI agents collaboratively analyze it.")

# ── File Upload ───────────────────────────────────────────────────────────────
st.subheader("📤 Upload Document")
uploaded_file = st.file_uploader(
    "Supported formats: PDF, DOCX, TXT",
    type=["pdf", "docx", "txt"],
)

if uploaded_file:
    st.success(f"Uploaded: **{uploaded_file.name}**")

    with st.spinner("Extracting text from document..."):
        text = extract_text(uploaded_file)

    if not text.strip():
        st.error("Could not extract text from this file. Try another document.")
    else:
        word_count = len(text.split())
        char_count = len(text)
        col1, col2 = st.columns(2)
        col1.metric("Words", f"{word_count:,}")
        col2.metric("Characters", f"{char_count:,}")

        with st.expander("📃 View Extracted Text", expanded=False):
            preview = text[:5000] + ("\n\n... [truncated for preview]" if len(text) > 5000 else "")
            st.text_area("Raw Text", preview, height=300, label_visibility="collapsed")

        selected_agents = []
        if use_summary:  selected_agents.append("Summary")
        if use_redflag:  selected_agents.append("RedFlag")
        if use_decision: selected_agents.append("Decision")

        if not selected_agents:
            st.warning("Please enable at least one agent in the sidebar.")
        elif st.button("🚀 Run Analysis", use_container_width=True, type="primary"):
            results = {}
            progress_bar = st.progress(0, text="Starting agents...")

            for i, agent_name in enumerate(selected_agents):
                emoji, label = AGENT_META[agent_name]
                progress_bar.progress(
                    i / len(selected_agents),
                    text=f"Running {emoji} {label}..."
                )
                output = run_agent(text, agent_name, model)
                results[agent_name] = output

            progress_bar.progress(1.0, text="All agents done!")

            save_analysis(
                filename=uploaded_file.name,
                word_count=word_count,
                agents=selected_agents,
                results=results,
            )

            st.divider()
            st.subheader("🤝 Collaborative Document Insights")
            display_results(results)

# ── Past Analyses ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("📚 Past Analyses")

analyses = load_all_analyses()
if not analyses:
    st.info("No past analyses yet. Upload a document above to get started.")
else:
    for record in reversed(analyses):
        label = (
            f"📄 {record['filename']}  |  "
            f"{record['timestamp']}  |  "
            f"{record['word_count']:,} words"
        )
        with st.expander(label, expanded=False):
            display_results(record["results"])
