import os

from groq import Groq

from .retriever import search


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_prompt(query, retrieved_chunks):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an AI Engineer interview assistant.

Answer the user's question using ONLY the context provided below.

If the answer cannot be found in the context, say:
"I don't have enough information in the knowledge base."

Context:
----------------
{context}
----------------

Question:
{query}

Answer:
"""

    return prompt


def generate_answer(query):

    results = search(query, top_k=3)

    retrieved_chunks = results["documents"][0]

    prompt = build_prompt(
        query,
        retrieved_chunks
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    return answer, results


if __name__ == "__main__":

    query =  "What is the architecture of a Kubernetes cluster?"

    answer, results = generate_answer(query)

    print("\nQUESTION:")
    print(query)

    print("\nANSWER:")
    print(answer)

    print("\nSOURCES:")

    for metadata in results["metadatas"][0]:
        print("-", metadata["source"])