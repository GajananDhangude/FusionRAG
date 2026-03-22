import pymupdf
import docx


def process_document(file_path:str):
    """Process unstructured documents"""

    if file_path.endswith(".pdf"):
        return read_pdf_file(file_path)
    elif file_path.endswith(".txt"):
        return read_text_file(file_path)
    elif file_path.endswith(".docx"):
        return read_docx_file(file_path)
    
    else:
        raise ValueError(f"Unsupported file format:{file_path.endswith}")
    

def read_pdf_file(file_path:str):
    """Read PDF file"""

    doc = pymupdf.open(file_path)

    docs = ""
    for page in doc:
        text = page.get_text()
        docs += text + "\n"
    doc.close()

    return docs

def read_text_file(file_path:str):
    """Read text file from file path"""

    with open(file_path , "r" , encoding="utf-8") as f:
        content = f.read()

    return "\n".join([content])

def read_docx_file(file_path:str):
    """Read docx file path"""

    doc = docx.Document(file_path)

    for paragraph in doc.paragraphs:
        text = paragraph.text

    return "\n".join([text])
                          
