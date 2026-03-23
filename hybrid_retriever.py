from rank_bm25 import BM25Okapi
import numpy as np


def build_bm25_index(chunks):

    tokenized_chunks = [chunk.split() for chunk in chunks]

    bm25 = BM25Okapi(tokenized_chunks)

    return bm25


def hybrid_search(query, chunks, faiss_results, bm25):

    tokenized_query = query.split()

    bm25_scores = bm25.get_scores(tokenized_query)

    ranked_indices = np.argsort(bm25_scores)[::-1][:5]

    bm25_results = [chunks[i] for i in ranked_indices]

    combined_results = list(set(faiss_results + bm25_results))

    return combined_results[:5]