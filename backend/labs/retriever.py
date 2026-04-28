from transformers import AutoModel , AutoTokenizer
from qdrant_client import QdrantClient
import torch
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

model_name = "BAAI/bge-small-en-v1.5"

client = QdrantClient(url="http://localhost:6333")


def semantic_retriever(prompt:str):

    instruction_prompt = f"Represent this sentence for searching relevant passages:{prompt}"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    query_inputs = tokenizer(instruction_prompt , return_tensors ="pt" , padding = True , truncation = True)
    with torch.no_grad():
        embeddings = model(**query_inputs).last_hidden_state.mean(dim=1).squeeze().tolist()

    search_result = client.query_points(
        collection_name="FusionRAG",
        query=embeddings,
        with_payload=True,
        limit=2
    ).points

    return search_result


# if __name__ == "__main__":

#         prompt = input("Enter a query:")

#         result = semantic_retriever(prompt)

#         # for point in result:
#         #      print(point.payload['text'])
#         print(result)

#         for res in result:
#              doc_text = res.payload['text']
#              source = res.payload['source']
#              print(doc_text)
#              print(source)
