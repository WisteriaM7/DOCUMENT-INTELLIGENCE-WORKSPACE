import io
from pathlib import Path


def extract_text(uploaded_file) -> str:
    """
    Extracts plain text from an uploaded Streamlit file object.
    Supports: PDF, DOCX, TXT
    """
    name = uploaded_file.name.lower()

    if name.endswith(".txt"):
        return _extract_txt(uploaded_file)
    elif name.endswith(".pdf"):
        return _extract_pdf(uploaded_file)
    elif name.endswith(".docx"):
        return _extract_docx(uploaded_file)
    else:
        return ""


def _extract_txt(uploaded_file) -> str:
    try:
        return uploaded_file.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"[Error reading TXT: {e}]"


def _extract_pdf(uploaded_file) -> str:
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n\n".join(text_parts)
    except ImportError:
        return "[Error: pdfplumber not installed. Run: pip install pdfplumber]"
    except Exception as e:
        return f"[Error reading PDF: {e}]"


def _extract_docx(uploaded_file) -> str:
    try:
        from docx import Document
        doc = Document(io.BytesIO(uploaded_file.read()))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)
    except ImportError:
        return "[Error: python-docx not installed. Run: pip install python-docx]"
    except Exception as e:
        return f"[Error reading DOCX: {e}]"
