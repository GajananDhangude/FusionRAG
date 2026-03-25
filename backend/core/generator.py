import os
from groq import Groq
from core.reranker import rrf_fusion
from dotenv import load_dotenv

load_dotenv()


client = Groq()

def generate_response(file_path , query:str):

    rrf_res = rrf_fusion(file_path , query)

    context = " ".join([res['document'][0] for res in rrf_res])

    system_prompt = "You are a helpful assistant. Answer the user's question using ONLY the provided context. If the answer isn't present in context, say you don't know."


    user_prompt = f"""
    Context: {context}
    \n Question:{query}
    \n Answer:
"""
    
    res = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_completion_tokens=524
    )

    # for chunk in stream:
    #     print(chunk.choices[0].delta.content , end="")
    res = res.choices[0].message.content

    return {
        "answer":res,
        "context":rrf_res
    }

# if __name__ =="__main__":

#     file_path = "./uploads/attention-is-all-you-need-Paper.pdf"

#     query = input("Enter your query:")

#     res = generate_response(file_path , query)
#     print(res)