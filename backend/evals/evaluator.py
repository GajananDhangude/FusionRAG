import json
import os
import pandas as pd
from ragas import evaluate
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig
from langchain_google_genai import GoogleGenerativeAIEmbeddings , ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from datasets import Dataset
from dotenv import load_dotenv
from core.generator import generate_response

load_dotenv()



llm = LangchainLLMWrapper(
    ChatGroq(
        model="moonshotai/kimi-k2-instruct",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )
)

embeddings = LangchainEmbeddingsWrapper(
    GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
)

run_config = RunConfig(
    max_workers=3,
    max_wait=60,
    timeout=60,
)



with open("evals/test_dataset.json", "r") as f:
    data = json.load(f)

def eval_rag(data: list[dict]):
    rag_result = []

    for i, item in enumerate(data):
        question = item["question"]
        ground_truth = item["ground_truth"]

        print(f"[{i+1}/{len(data)}] {question[:60]}...")

        try:
            print("generating response ...")
            result = generate_response(question)
            
            extracted_chunks = result['context']

            rag_result.append({
                "user_input": question,
                "response": result["answer"],
                "retrieved_contexts": extracted_chunks,
                "reference": ground_truth
            })

        except Exception as e:
            print(f" Skipping question {i+1}: {e}")
            continue

    ragas_dataset = Dataset.from_pandas(pd.DataFrame(rag_result))

    metrics = [
        Faithfulness(llm=llm),
        AnswerRelevancy(llm=llm, embeddings=embeddings),
        ContextPrecision(llm=llm),
        ContextRecall(llm=llm),
    ]

    score = evaluate(
        ragas_dataset,
        metrics=metrics,
        run_config=run_config
    )

    df = score.to_pandas()
    df.to_csv("evals/results/score.csv", index=False)

    return df


if __name__ == "__main__":

    df = eval_rag(data)


    print("\n--- Average Scores ---")
    print(df.mean(numeric_only=True))