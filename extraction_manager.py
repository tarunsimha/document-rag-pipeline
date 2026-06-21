import extractors.pdf_extractor as pdf_e
import extractors.docx_extractor as docx_e
import extractors.pptx_extractor as pptx_e
import extractors.xlsx_extractor as xlsx_e

def extract_text(path, extension):
    if extension == 'pdf':
        return pdf_e.extract_text(path)
    elif extension == 'docx':
        return docx_e.extract_text(path)
    elif extension == 'pptx':
        return pptx_e.extract_text(path)
    elif extension == 'xlsx':
        return xlsx_e.extract_text(path)
    else:
        with open(path, encoding="utf-8", errors="ignore") as file:
            return file.read()