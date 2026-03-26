from core.chunking import chunk_text
from fastembed import TextEmbedding , SparseTextEmbedding , LateInteractionTextEmbedding
from qdrant_client import QdrantClient , models
# from qdrant_client.models import Distance , VectorParams
from qdrant_client.models import PointStruct


model_name = "BAAI/bge-small-en-v1.5"
Dense_embedding_model = TextEmbedding(model_name=model_name)

sparse_embedding_model = SparseTextEmbedding("Qdrant/bm25")
late_embedding_model = LateInteractionTextEmbedding("colbert-ir/colbertv2.0")


client = QdrantClient(url="http://localhost:6333")
collection_name="FusionRAG"

if not client.collection_exists(collection_name=collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config={
            "dense-bge":models.VectorParams(
                size=384,
                distance=models.Distance.COSINE,
            ),
            "colbertv2.0": models.VectorParams(
                size=128,
                distance=models.Distance.COSINE,
                multivector_config=models.MultiVectorConfig(
                comparator=models.MultiVectorComparator.MAX_SIM,
                ),
            )
        },
        sparse_vectors_config={
            "sparse-bm25":models.SparseVectorParams()
        }
    )

    print(f"Collection '{collection_name}' created successfully.")
else:
    print(f"Collection '{collection_name}' already exists.")


def create_qdrant_db(file_path:str):
    """To create a vector database, we need to obtain embeddings for each chunk’s text and map these embeddings to their corresponding chunk IDs and document IDs"""
    
    print("Chunking Document...")
    chunks = chunk_text(file_path)

    texts = [chunk['text'] for chunk in chunks]
    chunk_ids = [chunk['chunk_id'] for chunk in chunks]
    
    existing_points = client.retrieve(
        collection_name=collection_name,
        ids=chunk_ids
    )

    existing_hashes = {p.id for p in existing_points}

    new_chunks = [c for c in chunks if c['chunk_id'] not in existing_hashes]

    if not new_chunks:
        print("All chunks already exist in Qdrant. Skipping...")
        return client
    
    dense_embeddings = list(Dense_embedding_model.passage_embed(texts))

    sparse_vectors = list(sparse_embedding_model.passage_embed(texts))

    late_embeddings = list(late_embedding_model.passage_embed(texts))

    print("Uploading Documents to Vector Database ..")
    points = []
    for i , chunk in enumerate(chunks):
        chunk_id = chunk['chunk_id']
        point = PointStruct(
            id=chunk_id,
            vector={
                "dense-bge":dense_embeddings[i].tolist(),
                "sparse-bm25":models.SparseVector(**sparse_vectors[i].as_object()),
                "colbertv2.0":late_embeddings[i].tolist()
            },
            payload={
                "text":chunk['text'],
                "source":chunk['source']
            }
        )
        points.append(point)

    client.upsert(
        collection_name=collection_name,
        wait=True,
        points=points
    )
    print(f"Uploaing Complete..")
        
    # else:
    #     print("Data already exists. Skipping... ")

    return client




if __name__ =="__main__":

    file_path = "./uploads/IJRPR46086.pdf"
    create_qdrant_db(file_path)


        

        
    
    


