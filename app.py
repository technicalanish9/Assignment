import streamlit as st
from scraper import scrape_and_clean
from vector_store import embed_texts, search_similar_chunks, load_faiss_index, save_faiss_index
from llm_qa import answer_question
import os

st.set_page_config(page_title="Web Q&A Tool", layout="centered")
st.title("🔍 Web Content Q&A Tool")

if "documents" not in st.session_state:
    st.session_state.documents = []
    st.session_state.index = None
    st.session_state.text_chunks = []

url_input = st.text_area("Enter URLs (one per line):")

if st.button("Ingest"):
    urls = [url.strip() for url in url_input.splitlines() if url.strip()]
    all_texts = []
    for url in urls:
        with st.spinner(f"Scraping {url}..."):
            text = scrape_and_clean(url)
            all_texts.append(text)

    with st.spinner("Embedding and indexing..."):
        st.session_state.text_chunks = [chunk for text in all_texts for chunk in text]
        index = embed_texts(st.session_state.text_chunks)
        st.session_state.index = index
        save_faiss_index(index, "index.faiss")

    st.success("Content ingested successfully!")

question = st.text_input("Ask a question:")

if st.button("Get Answer"):
    if st.session_state.index is None:
        st.session_state.index = load_faiss_index("index.faiss")

    with st.spinner("Searching and generating answer..."):
        context_chunks = search_similar_chunks(question, st.session_state.index, st.session_state.text_chunks)
        answer = answer_question(question, context_chunks)
        st.markdown("### 💬 Answer")
        st.write(answer)

        with st.expander("🔍 Retrieved Context"):
            for i, chunk in enumerate(context_chunks):
                st.markdown(f"**Snippet {i+1}:**")
                st.code(chunk, language="text")
