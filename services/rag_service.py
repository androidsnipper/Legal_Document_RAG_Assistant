import os
from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.2
    )


def ask_question(retriever, question):
    docs = retriever.invoke(question)

    context = "\n\n".join([d.page_content for d in docs])

    llm = get_llm()

    prompt = f"""
You are a legal assistant.

Use ONLY the context below to answer.

Context:
{context}

Question:
{question}

Answer clearly and concisely.
"""

    response = llm.invoke(prompt)
    return response.content