import faiss
import numpy as np
import os


# ---------------- Build FAISS Index ----------------

def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index


# ---------------- Search Function ----------------

def search(index, query_embedding, chunks, top_k=3):
    D, I = index.search(np.array([query_embedding]), top_k)

    results = [chunks[i] for i in I[0]]
    scores = D[0]

    return results, scores


# ---------------- Save FAISS Index ----------------

def save_index(index, path="cache/faiss_index.bin"):

    if not os.path.exists("cache"):
        os.makedirs("cache")

    faiss.write_index(index, path)


# ---------------- Load FAISS Index ----------------

def load_index(path="cache/faiss_index.bin"):

    if os.path.exists(path):
        return faiss.read_index(path)

    return None