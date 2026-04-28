import os
from fastapi import FastAPI , UploadFile , File , HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.responses import JSONResponse
from core.qdrant_client import create_qdrant_db
from core.document_processor import process_document
from core.chunking import chunk_text
from core.generator import generate_response
from fastapi.middleware.cors import CORSMiddleware
import boto3
import uuid
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

s3 = boto3.client(
    service_name='s3',
    region_name = 'ap-south-1',
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
)


BUCKET_NAME = os.getenv("BUCKET_NAME")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    # file_path:str
    query:str

class ChatResponse(BaseModel):
    response:dict


# UPLOAD_DIR = "./uploads"
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}
# os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):


    if not file.filename:
        raise HTTPException(status_code=400 , detail="NO file Found")
    
    MAX_FILE_SIZE = 10 * 1024 * 1024 
    
    # In recent FastAPI versions, file.size is available directly
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"File too large. Maximum allowed size is 10MB. Your file is {file.size / (1024*1024):.2f}MB"
        )
    
    filename , ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400 , detail="Unsupported file type")
    

    try:
        file_id = str(uuid.uuid4())
        s3_key = f"{filename}_{file_id}{ext}"
        print("Uploading file to S3 ...")
        s3.upload_fileobj(file.file , BUCKET_NAME , s3_key)

        print('Downloading file from S3 ...')

        response = s3.get_object(Bucket=BUCKET_NAME , Key=s3_key)
        file_content = response['Body'].read()

        print('Extracting and Indexing Document to Vector Database ...')
        file_format = s3_key.split(".")[-1]

        text = process_document(file_content , file_format)

        chunks = chunk_text(text , s3_key)
        print('Storing Document in Vector Database ...')
        client = create_qdrant_db(chunks)

        print("Processing complete ✅")

        
        return {
            "message": "File Uploaded Successfully",
            "filename": s3_key
        }

    except Exception as e:
        raise HTTPException(status_code=500 , detail=f"File upload failed: {str(e)}")
    




@app.post("/chat")
async def query(req:ChatRequest):

    if not req.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    
    res = generate_response(req.query)

    response_content = {
        "question":res['question'],
        "answer":res['answer'],
        "source":res['source']
    }

    return JSONResponse(
        content=response_content,
        status_code=200
    )




# if __name__ =="__main__":

#     uvicorn.run(
#         "api.main:app", 
#         host="127.0.0.1", 
#         port=8000, 
#         reload=True
#     )




