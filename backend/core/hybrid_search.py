from qdrant_client import QdrantClient , models
from fastembed import TextEmbedding , SparseTextEmbedding , LateInteractionTextEmbedding


client = QdrantClient(url="http://localhost:6333")
collection_name="FusionRAG"

model_name = "BAAI/bge-small-en-v1.5"
Dense_embedding_model = TextEmbedding(model_name=model_name)

sparse_embedding_model = SparseTextEmbedding("Qdrant/bm25")
late_embedding_model = LateInteractionTextEmbedding("colbert-ir/colbertv2.0")

def hybrid_search(query:str , limit:int = 3):

    dense_query = next(Dense_embedding_model.query_embed(query)).tolist()
    sparse_query = next(sparse_embedding_model.query_embed(query))
    late_vectors = next(late_embedding_model.query_embed(query)).tolist()


    response = client.query_points(
        collection_name=collection_name,
        prefetch=[                                    # ← add this
            models.Prefetch(
                query=dense_query,
                using="dense-bge",
                limit=20,
            ),
            models.Prefetch(
                query=models.SparseVector(**sparse_query.as_object()),
                using="sparse-bm25",
                limit=20,
            ),
        ],
        query=late_vectors,                          # ColBERT reranks the prefetch candidates
        using="colbertv2.0",
        with_payload=True,
        limit=limit
    )

    # # 4. Extract results
    search_results = []
    for point in response.points:
        search_results.append({
            "text": point.payload["text"],
            "source": point.payload["source"], # THE CORRECT PATH
            "score": point.score # This is now an RRF score
        })
    
    return search_results


# if __name__ == "__main__":
#     query = "What performance metrics are used to evaluate the models?"
#     results = hybrid_search(query)
#     # print(results)
    
#     for res in results:
#         print(f"\nSource: {res['source']}")
#         print(f"Content: {res['text']}...")
#         print(f"Score:{res['score']}")
