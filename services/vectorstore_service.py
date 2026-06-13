from langchain_community.vectorstores import FAISS

def create_vectorstore(text_chunks, embeddings):
    return FAISS.from_texts(text_chunks, embeddings)


def get_retriever(vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k": 4})