from core.document_processor import process_document
import os
import hashlib
import uuid


def get_chunk_hashid(text:str) -> str:
    hash_hex = hashlib.md5(text.encode('utf-8')).hexdigest()
    return str(uuid.UUID(hash_hex))

def chunk_text(text:str , s3_key:str , chunk_size:int = 1000):
    """split text/docs into into fix sized chunks"""

    # content = process_document(file_path)

    sentences = text.replace("\n" , " ").split('. ')
    # file_name = os.path.basename(file_path)

    all_chunks = []
    chunks = []
    current_chunks =[]
    current_size = 0

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        if not sentence.endswith('.'):
            sentence += '.'

        sentence_size = len(sentence)

        if current_size + sentence_size > chunk_size and current_chunks:
            chunks.append(' '.join(current_chunks))
            current_chunks = [sentence]
            current_size = sentence_size
        
        else:
            current_chunks.append(sentence)
            current_size +=sentence_size

    if current_chunks:
        chunks.append(' '.join(current_chunks))

    for i , chunk in enumerate(chunks):
        chunk_id = get_chunk_hashid(chunk)

        all_chunks.append({
            "text":chunk,
            "source":s3_key,
            "chunk_id":chunk_id
        })

    return all_chunks


# if __name__ =="__main__":

#     file_path = "./uploads/attention-is-all-you-need-Paper.pdf"

#     chunks = chunk_text(file_path)
#     print(len(chunks))

#     print(chunks)
