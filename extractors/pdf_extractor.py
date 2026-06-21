from pypdf import PdfReader

def extract_text(path):
    reader = PdfReader(path)
    full_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)

    return '\n'.join(full_text)