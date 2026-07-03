import faiss
from sentence_transformers import SentenceTransformer
from data_loader import load_assessments

# Load the embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings():
    """
    Create embeddings for all assessments and build the FAISS index.
    """

    assessments = load_assessments()

    texts = []

    for assessment in assessments:
        text = f"""
        {assessment.get('name', '')}
        {' '.join(assessment.get('keys', []))}
        {' '.join(assessment.get('job_levels', []))}
        {assessment.get('description', '')}
        """

        texts.append(text)

    embeddings = model.encode(texts, show_progress_bar=True)

    # Convert to float32 (required by FAISS)
    embeddings = embeddings.astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return assessments, index


# Create these only once when the application starts
assessments, index = create_embeddings()


if __name__ == "__main__":
    print(f"Assessments: {len(assessments)}")
    print(f"FAISS Index Size: {index.ntotal}")