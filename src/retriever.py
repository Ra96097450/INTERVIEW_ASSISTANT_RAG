import chromadb

from sentence_transformers import SentenceTransformer


# Load the same embedding model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")


# Connect to existing ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="interviewiq"
)


def search(query, top_k=3):

    # Convert user query into an embedding
    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    query = "How does gradient descent update model weights?"

    results = search(query)

    print("\nUSER QUERY:")
    print(query)

    print("\nRETRIEVED CHUNKS:\n")

    for i, document in enumerate(results["documents"][0]):

        print(f"--- Result {i + 1} ---")
        print(document)

        print("\nSource:")
        print(results["metadatas"][0][i])

        print("\nDistance:")
        print(results["distances"][0][i])

        print()