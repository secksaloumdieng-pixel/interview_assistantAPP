import fitz
import re


def extract_cv_text(uploaded_file):
    """
    Extract raw text from an uploaded PDF CV and return a cleaned string.
    """
    if uploaded_file is None:
        return ""

    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    pages_text = []
    for page in doc:
        text = page.get_text("text")
        if text:
            pages_text.append(text)

    raw_text = "\n".join(pages_text)

    cleaned_text = re.sub(r"\s+", " ", raw_text).strip()

    return cleaned_text