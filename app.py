import streamlit as st
from dotenv import load_dotenv

from services.pdf_service import extract_text_from_pdf
from services.chunk_service import chunk_text
from services.embedding_service import get_embeddings
from services.vectorstore_service import create_vectorstore, get_retriever
from services.rag_service import ask_question

load_dotenv()

st.set_page_config(page_title="Legal AI Assistant", layout="wide")

st.title("⚖️ Legal Document AI Assistant (RAG)")

# session state
if "retriever" not in st.session_state:
    st.session_state.retriever = None


# Sidebar
st.sidebar.header("Upload & Controls")

uploaded_file = st.sidebar.file_uploader("Upload Legal PDF", type=["pdf"])

process_btn = st.sidebar.button("Process Document")


# PROCESS DOCUMENT
if process_btn and uploaded_file:

    try:
        with st.spinner("Extracting text..."):
            text = extract_text_from_pdf(uploaded_file)

        st.success("Text extracted successfully!")

        st.text_area("📄 Extracted Text Preview", text[:3000], height=200)

        with st.spinner("Chunking text..."):
            chunks = chunk_text(text)

        with st.spinner("Creating embeddings & vector store..."):
            embeddings = get_embeddings()
            vectorstore = create_vectorstore(chunks, embeddings)

            st.session_state.retriever = get_retriever(vectorstore)

        st.success("Document ready for Q&A!")

    except Exception as e:
        st.error(str(e))


# QUESTION SECTION
st.subheader("💬 Ask Questions")

query = st.text_input("Enter your question about the document")

if st.button("Ask"):

    if st.session_state.retriever is None:
        st.warning("Please upload and process a document first.")
    else:
        with st.spinner("Thinking..."):
            answer = ask_question(st.session_state.retriever, query)

        st.write("### Answer")
        st.write(answer)


# SUMMARY FEATURE
st.subheader("🧾 Document Summary")

if st.button("Generate Summary"):

    if st.session_state.retriever is None:
        st.warning("Upload document first")
    else:
        with st.spinner("Generating summary..."):
            summary = ask_question(
                st.session_state.retriever,
                "Summarize this legal document with key clauses, obligations, and risks"
            )

        st.write(summary)