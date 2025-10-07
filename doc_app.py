import os
import time

import streamlit as st
from dotenv import load_dotenv

from documents_llm.st_helpers import run_query

# Load environment variables
load_dotenv()

# Load model parameters
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

    st.subheader("Page range")

    st.write(
        "Select page range. Pages are numbered starting at 0. For end page, you can also use negative numbers to count from the end, e.g., -1 is the last page, -2 is the second to last page, etc."
    )
    col1, col2 = st.columns(2)
    with col1:
        start_page = st.number_input("Start page:", value=0, min_value=0)
    with col2:
        end_page = st.number_input("End page:", value=-1)

    st.subheader("Query type")

    query_type = st.radio("Select the query type", ["Summarize", "Query"])


if query_type == "Query":
    user_query = st.text_area(
        "User query", value="What is the data used in this analysis?"
    )


if st.button("Run"):
    if file is None:
        st.error("Please upload a file.")
    else:
        # --- UI-ONLY DEMO ---
        # Display a placeholder message instead of running the AI query.
        st.info("Button clicked! The backend AI logic is not connected in this version.")
        
        result = (
            "This is a placeholder response for the summary. "
            "In the full version, the AI's summary of the document would appear here."
        )

        # We still display the result container to show where the output will go.
        if result:
            with st.container(border=True):
                st.header("Result")
                st.markdown(result)
                st.info("Time taken: 0.01 seconds (placeholder)", icon="⏱️")
