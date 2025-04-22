import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def answer_question(question, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"""
Answer the question using only the context below. If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}
Answer:
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300,
    )

    return response["choices"][0]["message"]["content"].strip()
