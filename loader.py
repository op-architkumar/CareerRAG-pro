import os
from pypdf import PdfReader

def load_documents_from_folder(folder_path):
    all_text = ""

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Handle PDF files
        if filename.endswith(".pdf"):
            reader = PdfReader(file_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"

        # Handle TXT files
        elif filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                all_text += f.read() + "\n"

    return all_text