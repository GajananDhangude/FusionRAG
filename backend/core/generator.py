import os
from groq import Groq
from core.hybrid_search import hybrid_search
from dotenv import load_dotenv

load_dotenv()


client = Groq()

def generate_response(query:str):

    # rrf_res = rrf_fusion(query)

    search_result = hybrid_search(query)

    context = " ".join([res['text'] for res in search_result])
    source = [res['source'] for res in search_result]
    system_prompt = "You are a Knowledge Base assistant. Keep Answer Concise."



    user_prompt = f"""
    QUESTION:
    {query}

CONTEXT:
{context}

Using the CONTEXT provided, answer the QUESTION. Keep your answer grounded in the facts of the CONTEXT. If the CONTEXT doesn't contain the answer to the QUESTION, say you don't know.
"""
    
    res = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        max_completion_tokens=524
    )

    # for chunk in stream:
    #     print(chunk.choices[0].delta.content , end="")
    res = res.choices[0].message.content

    return {
        "question":query,
        "answer":res,
        "context":[res['text'] for res in search_result],
        "source":source[0]
    }

# if __name__ =="__main__":


#     query = input("Enter your query:")

#     res = generate_response(query)
#     print(res)