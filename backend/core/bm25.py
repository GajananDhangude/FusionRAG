from typing import List , Dict , Tuple
import numpy as np
from rank_bm25 import BM25Okapi
import string
from chunking import chunk_text


def bm25_search(file_path:str , query:str):

    original_corpus = []
    tokenized_corpus = []

    chunks = chunk_text(file_path)

    for chunk in chunks:
        text = chunk['text']
        original_corpus.append([text])

        # tokenization
        token_text = chunk['text'].lower().translate(str.maketrans('' , '' , string.punctuation))
        doc_tokens = token_text.strip().split()

        tokenized_corpus.append(doc_tokens)

    bm25 = BM25Okapi(tokenized_corpus)

    clean_query = query.lower().translate(str.maketrans('' , '' , string.punctuation))
    tokenized_query = clean_query.strip().split()

    doc_score = bm25.get_scores(tokenized_query)


    ranked_indices = sorted(
        range(len(doc_score)),
        key = lambda i:doc_score[i],
        reverse=True
    )[:3]

    bm25_results = []

    for rank , idx in enumerate(ranked_indices):
        if doc_score[idx] > 0:
            bm25_results.append({
                "rank":rank + 1,
                "scores":float(doc_score[idx]),
                "document":original_corpus[idx]
            })

    return bm25_results


if __name__ =="__main__":

    file_path = "./uploads/attention-is-all-you-need-Paper.pdf"

    query = input("Enter Your query:")

    result = bm25_search(file_path , query)

    print(result)
    