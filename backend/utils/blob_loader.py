import os
from azure.storage.blob import BlobServiceClient
import fitz  # PyMuPDF

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "claim-docs"

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def list_pdfs():
    return [b.name for b in container_client.list_blobs()]

def download_pdf(blob_name):
    blob = container_client.get_blob_client(blob_name)
    return blob.download_blob().readall()

def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def load_all_docs():
    docs = []
    for pdf_name in list_pdfs():
        pdf_bytes = download_pdf(pdf_name)
        text = extract_text_from_pdf(pdf_bytes)

        docs.append({
            "source": pdf_name,
            "text": text
        })

    return docs