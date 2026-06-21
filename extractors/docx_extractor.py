import docx

def extract_text(path):
    doc = docx.Document(path)
    full_text = [para.text for para in doc.paragraphs]
    return '\n'.join(full_text)