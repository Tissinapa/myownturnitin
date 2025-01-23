from flask import Flask, request, jsonify
from bert_score import score
from pymongo import MongoClient
import pdfplumber
import os

app = Flask(__name__)

# Mongodb set up
client = MongoClient("mongodb://localhost:27017")
db = client["pdf_database"]
collection = db["peedeefs"]

def extract_text_from_pdf(pdf_file):
    try: 
        # Take text from pdf_file
        with pdfplumber.open(pdf_file) as pdf:
            return "\\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    except Exception as err:
        print(f"Error reading PDF: {err}")
        return 
    
def save_pdf_to_db(pdf):
    try:
        extracted_pdf_text = extract_text_from_pdf(pdf)
        if extracted_pdf_text:
            pdf_name = os.path.basename(pdf)
            #save to mongo
            collection.insert_one({
                "filename": pdf_name,
                "file_data": extracted_pdf_text
            })
            print(f"pdf {pdf_name} saved to mongo.")
            #compare_pdfs(extracted_pdf_text)
        else: 
            print(f"Failed to extract text from {pdf}")
    except Exception as err:
        print(f"Error reading pdf {pdf}: {err}")
        return



@app.route("/compare", methods=["POST"])

def compare_pdfs(extracted_pdf_text):
    ref_file = request.files['reference']
    candi_file = request.files['candidate']
    
    


if __name__ == "__main__":
    print("testi")
    pdf_file= "test_pdf.pdf"
    save_pdf_to_db(pdf_file)
    
    

