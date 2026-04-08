from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
index = None


def add_documents(text_chunks):
    global documents, index

    embeddings = model.encode(text_chunks)

    documents = text_chunks

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))


def search(query, k=5):
    global documents, index

    if index is None:
        return []

    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)

    return [documents[i] for i in indices[0]]
