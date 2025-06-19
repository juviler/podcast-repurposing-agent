import os
import docx
import PyPDF2
import re

def read_txt(file_path):
    """
    Reads plain text from a .txt file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf(file_path):
    """
    Extracts text from a PDF file using PyPDF2.
    Cleans up excessive whitespace and newlines.
    """
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    # Clean up formatting: remove excess whitespace and newlines
    cleaned = re.sub(r'\s*\n\s*', ' ', text)          # Replace line breaks with spaces
    cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip() # Collapse multiple spaces
    return cleaned

def read_docx(file_path):
    """
    Extracts and joins text from all paragraphs in a .docx file.
    """
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_file(file_path):
    """
    Determines the file extension and routes to the appropriate text extractor.
    Supports .txt, .pdf, and .docx.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return read_txt(file_path)
    elif ext == '.pdf':
        return read_pdf(file_path)
    elif ext == '.docx':
        return read_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")