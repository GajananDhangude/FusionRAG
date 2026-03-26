import os
from fastapi import FastAPI , UploadFile , File , HTTPException
from pydantic import BaseModel
import uvicorn
import shutil
from core.qdrant_client import create_qdrant_db
from core.generator import generate_response


app = FastAPI()



class ChatRequest(BaseModel):
    # file_path:str
    query:str

class ChatResponse(BaseModel):
    response:dict


UPLOAD_DIR = "./uploads"
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/ingest")
async def ingest_file(file:UploadFile = File(...)):


    if not file.filename:
        raise HTTPException(status_code=400 , detail="NO file Found")
    
    _ , ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400 , detail="Unsupported file type")
    
    save_path = os.path.join(UPLOAD_DIR , f"{file.filename}")

    if os.path.exists(save_path):
        print("File Exists. Skipping upload and indexed...")

        return {"message":"File Already exists. No Action Taken"}
    
    try:
        print("saving file ...")
        with open(save_path , "wb") as f:
            shutil.copyfileobj(file.file , f)

        print("--------Indexing Document to Vector Database------------")
        client = create_qdrant_db(save_path)


        return {"message": "Document Uploaded and Indexed Successfully" , "path":save_path}
    
    except Exception as e:
        if os.path.exists(save_path):
            os.remove(save_path)
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")



@app.post("/chat" , response_model=ChatResponse)
async def query(req:ChatRequest):

    if not req.query:
        return {"message":"Please Provide Some query"}
    
    
    res = generate_response(req.query)

    return ChatResponse(response=res)




if __name__ =="__main__":

    uvicorn.run(
        "api.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )




