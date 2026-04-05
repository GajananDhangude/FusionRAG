from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.document_processor import process_document
import hashlib
import uuid
import os


text_spitter = RecursiveCharacterTextSplitter(
    chunk_size = 800,
    chunk_overlap = 10,
    separators=["\n\n", "\n", ". ", " "]
)


def get_chunk_hashid(text:str) -> str:
    hash_hex = hashlib.md5(text.encode('utf-8')).hexdigest()
    return str(uuid.UUID(hash_hex))


def chunktext(file_path:str):
    all_chunks = []
    content = process_document(file_path)

    filename = os.path.basename(file_path)

    chunks = text_spitter.split_text(content)

    for i , chunk in enumerate(chunks):
        chunk_id = get_chunk_hashid(chunk)

        all_chunks.append({
            "chunk_id":chunk_id,
            "text":chunk,
            "source":filename
        })

    return all_chunks



if __name__ =="__main__":

    file_path = "./uploads/attention-is-all-you-need-Paper.pdf"

    chunk = chunktext(file_path)
    print(chunk)
    print(len(chunk))