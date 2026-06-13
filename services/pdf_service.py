from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)

        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content

        if not text.strip():
            raise ValueError("No extractable text found. File may be scanned.")

        return text

    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")