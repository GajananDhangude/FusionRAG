from transformers import AutoModel , AutoTokenizer
from core.chunking import chunk_text
import torch
from qdrant_client import QdrantClient , models
from qdrant_client.models import Distance, VectorParams , PointStruct


model_name = "BAAI/bge-small-en-v1.5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
client = QdrantClient(url="http://localhost:6333")


if not client.collection_exists(collection_name="RAG_Collection"):
    client.create_collection(
        collection_name="RAG_Collection",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )


def create_qdrant_db(file_path:str):
    """To create a vector database, we need to obtain embeddings for each chunk’s text and map these embeddings to their corresponding chunk IDs and document IDs"""
    
    print("Chunking Document...")
    chunks = chunk_text(file_path)

    for chunk in chunks:
        text = chunk['text']
        source = chunk['source']
        chunk_id = chunk['chunk_id']

        existing_points = client.retrieve(
            collection_name="RAG_Collection",
            ids=[chunk_id]
        )

        if not existing_points:
            inputs = tokenizer(text , return_tensors ="pt" , padding = True , truncation = True)

            with torch.no_grad():
                embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze().tolist()

            client.upsert(
                collection_name = "RAG_Collection",
                wait = True,
                points=[PointStruct(id=chunk_id , vector=embeddings , payload={"text":text , "source":source})]
            )
            print(f"Uploaing data ....")
        
        else:
            print("Data already exists. Skipping... ")

    return client




# if __name__ =="__main__":

#     file_path = "./uploads/attention-is-all-you-need-Paper.pdf"
#     create_qdrant_db(file_path)


        

        
    
    


