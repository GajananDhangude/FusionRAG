import docx
import fitz
import io


def process_document(file_bytes:bytes , file_format:str):
    """Process unstructured documents"""

    if file_format == "pdf":
        return read_pdf_file(file_bytes)
    elif file_format == "txt":
        return read_text_file(file_bytes)
    elif file_format == "docx":
        return read_docx_file(file_bytes)

    else:
        raise ValueError(f"Unsupported file format:{file_format}")
    

def read_pdf_file(file_bytes:bytes):
    """Read PDF file"""

    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def read_text_file(file_bytes:bytes):
    """Read text file from file bytes"""

    content = file_bytes.decode("utf-8")
    return content

def read_docx_file(file_bytes:bytes):
    """Read docx file from file bytes"""

    doc = docx.Document(io.BytesIO(file_bytes))

    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]

    return "\n".join(paragraphs)
                          
