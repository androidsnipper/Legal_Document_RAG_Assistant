import os
from langchain_openai import ChatOpenAI

def summarize_text(chunks):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.3
    )

    text = "\n".join(chunks[:6])

    prompt = f"""
Summarize this legal document.

Focus on:
- Key obligations
- Payment terms
- Termination clauses
- Risks

TEXT:
{text}
"""

    return llm.invoke(prompt).content