from pypdf import PdfReader

def read_pdf(uploaded_file):
    text = ""

    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text[:12000]