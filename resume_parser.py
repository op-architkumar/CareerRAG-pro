import pdfplumber
import re


def extract_text_from_resume(file):

    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    # remove emails
    text = re.sub(r'\S+@\S+', ' ', text)

    # remove phone numbers
    text = re.sub(r'\b\d{10}\b', ' ', text)

    # remove urls
    text = re.sub(r'http\S+', ' ', text)

    return text