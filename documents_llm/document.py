import io
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from streamlit.runtime.uploaded_file_manager import UploadedFile

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_core.documents.base import Document


def load_pdf(
    file_path: Path | str, start_page: int = 1, end_page: int = -1
) -> list[Document]:
    """
    Loads a PDF file and returns a list of Document objects.
    Accepts 1-based page numbers and handles a special value of -1 for end_page.
    """
    print(f"Loading PDF: {file_path}, start_page: {start_page}, end_page: {end_page}")
    loader = PyPDFLoader(str(file_path))
    docs = loader.load()

    # --- LOGIC UPDATED FOR 1-BASED INDEXING ---
    # Convert 1-based start page to 0-based index
    start_index = start_page - 1

    if start_index < 0:
        raise ValueError("Start page must be 1 or greater.")

    if end_page == -1:
        # Slice from the start index to the end of the document
        return docs[start_index:]
    else:
        # Slice from the start index up to the end page.
        # The end page is inclusive for the user, so it becomes the exclusive end of the slice.
        return docs[start_index:end_page]


def load_text(file_path: Path | str) -> list[Document]:
    loader = TextLoader(str(file_path))
    return loader.load()


def extract_pages_as_pdf(
    uploaded_file: UploadedFile, start_page: int, end_page: int
) -> bytes:
    """
    Extracts a range of pages from an uploaded PDF and returns it as a new PDF in bytes.
    Accepts 1-based page numbers from the user and converts them to 0-based indices.
    """
    uploaded_file.seek(0)
    
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()

    num_pages = len(reader.pages)

    # Convert 1-based user input to 0-based list indices
    start_page_idx = start_page - 1
    end_page_idx = end_page - 1
    
    if not (0 <= start_page_idx < num_pages):
        raise ValueError(f"Start page '{start_page}' is out of valid range (1-{num_pages}).")
    if not (0 <= end_page_idx < num_pages):
         raise ValueError(f"End page '{end_page}' is out of valid range (1-{num_pages}).")
    if start_page_idx > end_page_idx:
        raise ValueError("Start page cannot be after the end page.")

    for i in range(start_page_idx, end_page_idx + 1):
        writer.add_page(reader.pages[i])

    pdf_buffer = io.BytesIO()
    writer.write(pdf_buffer)
    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()