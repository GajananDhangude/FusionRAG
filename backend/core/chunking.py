from document_processor import process_document
import os
import uuid

def chunk_text(file_path:str , chunk_size:int = 800 ):
    """split text/docs into into fix sized chunks"""

    content = process_document(file_path)

    sentences = content.replace("\n" , " ").split('. ')
    file_name = os.path.basename(file_path)

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
        chunk_id = str(uuid.uuid4())

        all_chunks.append({
            "text":chunk,
            "source":file_name,
            "chunk_id":chunk_id
        })

    return all_chunks