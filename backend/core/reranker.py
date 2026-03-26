from core.bm25 import bm25_search
from core.retriever import semantic_retriever



def rrf_fusion(query:str):

    rrf_score = {}

    semantic_result = semantic_retriever(query)

    for rank , item in enumerate(semantic_result , 1):
        doc_text = item.payload['text']
        source = item.payload['source']

        rrf_score[doc_text] = rrf_score.get(doc_text , 0) + 1/(60 + rank)

    # BM25 Keyword Search
    file_path = f"./uploads/{source}"
    bm25_result = bm25_search(file_path , query)

    for item in bm25_result:
        doc_text = item['document'][0]

        rank = item['rank']

        score = 1 / (60 + rank)

        rrf_score[doc_text] = rrf_score.get(doc_text , 0) + score

    
    sorted_docs = sorted(rrf_score.items() , key=lambda x: x[1] , reverse=True)

    final_result = []

    for i , (text , score) in enumerate(sorted_docs , 1):
        final_result.append({
            "rank":i,
            "rrf_score":score,
            "document":[text]
        })

    return {
        "result":final_result,
        "source":source
    }


if __name__ == "__main__":

#     file_path = "./uploads/attention-is-all-you-need-Paper.pdf"

    query = "What is multi Head attension?"

    result = rrf_fusion( query)

    print(result)