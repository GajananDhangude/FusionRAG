from transformers import AutoModel , AutoTokenizer
from chunking import chunk_text
import torch
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams , PointStruct

model_name = "BAAI/bge-small-en-v1.5"

client = QdrantClient(url="http://localhost:6333")

if not client.collection_exists(collection_name="test_collection"):
    client.create_collection(
        collection_name="test_collection",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )




def create_qdrant_db(file_path:str):
    """To create a vector database, we need to obtain embeddings for each chunk’s text and map these embeddings to their corresponding chunk IDs and document IDs"""

    print("Chunking Document...")
    chunks = chunk_text(file_path)
    print(f"Chunking is done {len(chunks)} chunks")

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = AutoModel.from_pretrained(model_name)

    for chunk in chunks:
        text = chunk['text']
        source = chunk['source']
        chunk_id = chunk['chunk_id']

        inputs = tokenizer(text , return_tensors ="pt" , padding = True , truncation = True)

        with torch.no_grad():
            embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze().tolist()
        
        client.upsert(
            collection_name = "test_collection",
            wait = True,
            points=[PointStruct(id=chunk_id , vector=embeddings , payload={"text":text})]
        )

    client.close()
    

# if __name__ =="__main__":

#     file_path = "./uploads/attention-is-all-you-need-Paper.pdf"
#     create_qdrant_db(file_path)


        

        
    
    


