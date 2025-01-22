from flask import Flask, request, jsonify
from bert_score import score
from pymongo import MongoClient
import pdfplumber
import os

app = Flask(__name__)

# Mongodb set up
client = MongoClient("mongodb://localhost:27017")
db = client["pdf_database"]
collection = db["pdfs"]

def extract_text_from_pdf(pdf_file):
    try: 
        with pdfplumber.open(pdf_file) as pdf:
            return "\\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    except Exception as err:
        print(f"Error reading pdf {pdf_file}: {err}")
        return 
    
def save_pdf_to_db(pdf):
    try:
        with open(pdf, "rb") as pdf_file:
            pdf_data = pdf_file.read()
            pdf_name = os.path.basename(pdf)

            #save to mongo
            collection.insert_one({
                "filename": pdf_name,
                "file_data": pdf_data
            })
            print(f"pdf {pdf_name} saved to mongo.")
    except Exception as err:
        print(f"Error reading pdf {pdf}: {err}")
        return


@app.route("/compare", methods=["POST"])

def compare_pdfs():
    ref_file = request.files['reference']
    candi_file = request.files['candidate']
    
    


if __name__ == "__main__":
    print("testi")

