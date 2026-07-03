from data_loader import load_assessments
from embedding import model, index, assessments



if __name__ == "__main__":
    assessments = load_assessments()
    print(f"Total assessments loaded: {len(assessments)}")
    print(assessments[0]["name"])

def search_assessments(query, top_k=10):
    """
    Search for the most relevant assessments.
    """

    # Convert the user's query into an embedding
    query_embedding = model.encode([query]).astype("float32")

    # Search FAISS
    distances, indices = index.search(query_embedding, top_k)

    results = []

    # Collect matching assessments
    for idx in indices[0]:
        results.append(assessments[idx])

    return results