import os
import time

import streamlit as st
from dotenv import load_dotenv

from documents_llm.st_helpers import run_query
from documents_llm.document import extract_pages_as_pdf

# Load environment variables
load_dotenv()

# Load model parameters from environment
MODEL_NAME = os.getenv("MODEL_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = os.getenv("OPENAI_URL")


st.title("🔮 Offline Oracle")
st.write(
    "Discover the essence of your documents — privately, and completely offline. "
    "This tool transforms PDFs and text files into clear, concise insights, helping you understand more with less effort — all while keeping your data safe on your device"
)

with st.sidebar:
    st.header("Model")
    model_name = st.text_input("Model name", value=MODEL_NAME)
    temperature = st.slider("Temperature", value=0.1, min_value=0.0, max_value=1.0)

    st.header("Document")
    st.subheader("Upload a PDF file")
    file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if file:
        st.write("File uploaded successfully!")

        # --- SECTION FOR ANALYSIS PAGE RANGE (UPDATED) ---
        st.subheader("Page range (for analysis)")
        st.write(
            "Select page range. Pages are numbered starting at 1. For end page, use -1 to go to the end of the document."
        ) # <-- UPDATED HELP TEXT
        col1, col2 = st.columns(2)
        with col1:
            start_page = st.number_input("Start page:", value=1, min_value=1) # <-- CHANGED value and min_value
        with col2:
            end_page = st.number_input("End page:", value=-1, min_value=-1) # <-- CHANGED min_value

        # --- QUERY TYPE SECTION ---
        st.subheader("Query type")
        query_type = st.radio("Select the query type", ["Summarize", "Query"])

        # --- EXTRACT PAGES SECTION ---
        st.subheader("Extract Pages")
        st.write(
            "Select a page range to create a new, smaller PDF. "
            "Pages are numbered starting at 1 (like a real book)."
        )
        
        extract_col1, extract_col2 = st.columns(2)
        with extract_col1:
            extract_start_page = st.number_input("Extract from page:", value=1, min_value=1)
        with extract_col2:
            extract_end_page = st.number_input("Extract to page:", value=1, min_value=1)
        
        if st.button("Generate Extracted PDF"):
            try:
                extracted_pdf_bytes = extract_pages_as_pdf(
                    file, extract_start_page, extract_end_page
                )
                st.session_state.pdf_to_download = extracted_pdf_bytes
                st.session_state.download_filename = f"extracted_{extract_start_page}-{extract_end_page}_{file.name}"
                st.success("PDF ready for download below!")
            except Exception as e:
                st.error(f"Error during extraction: {e}")

        if 'pdf_to_download' in st.session_state and st.session_state.pdf_to_download:
            st.download_button(
                label="Download Extracted PDF",
                data=st.session_state.pdf_to_download,
                file_name=st.session_state.download_filename,
                mime="application/pdf"
            )

# This part needs to be outside the `if file:` block in case no file is uploaded yet
if 'query_type' not in locals():
    with st.sidebar:
        st.subheader("Query type")
        query_type = st.radio("Select the query type", ["Summarize", "Query"])


if query_type == "Query":
    user_query = st.text_area(
        "User query", value="What is the data used in this analysis?"
    )

if st.button("Run Analysis"):
    result = None
    start = time.time()
    if file is None:
        st.error("Please upload a file.")
    else:
        with st.status("Running...", expanded=True) as status:
            try:
                result = run_query(
                    uploaded_file=file,
                    summarize=query_type == "Summarize",
                    user_query=user_query if query_type == "Query" else "",
                    start_page=start_page,
                    end_page=end_page,
                    model_name=model_name,
                    openai_api_key=OPENAI_API_KEY,
                    openai_url=OPENAI_URL,
                    temperature=temperature,
                )
                status.update(label="Done!", state="complete", expanded=False)

            except Exception as e:
                status.update(label="Error", state="error", expanded=False)
                st.error(f"An error occurred: {e}")
                result = ""

    if result:
        with st.container(border=True):
            st.header("Result")
            st.markdown(result)
            st.info(f"Time taken: {time.time() - start:.2f} seconds", icon="⏱️")