from flask import Flask, request, jsonify
from bert_score import score
from pymongo import MongoClient
import pdfplumber
import os

#app = Flask(__name__)

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
            
        else: 
            print(f"Failed to extract text from {pdf}")
    except Exception as err:
        print(f"Error reading pdf {pdf}: {err}")
        return



#@app.route("/compare", methods=["POST"])

def compare_pdfs_bertscore(ref_text, candi_text):
    #ref_file = request.files['reference']
    #candi_file = request.files['candidate']
    
    try:
        P, R, F1 = score([candi_text], [ref_text], lang = "en", verbose=True)
        
        return {
            "Precision": P.mean().item(),
            "Recall": R.mean().item(),
            "F1": F1.mean().item()
        }
        
    except Exception as err:
        print(err)
        return

    
def main():
    
    print("testi")
    pdf_file= "test_pdf.pdf"
    pdf_file_candi = "test_pdf_takaperin.pdf"
    save_pdf_to_db(pdf_file)
    ref_text = extract_text_from_pdf(pdf_file)
    candi_text = extract_text_from_pdf(pdf_file_candi)
    results = compare_pdfs_bertscore(ref_text, candi_text)
    
    if results:
        print("\nBERTScore Results:")
        print(f"Precision: {results['Precision']:.4f}")
        print(f"Recall: {results['Recall']:.4f}")
        print(f"F1 Score: {results['F1']:.4f}")
    else:
        print("Failed to compute BERTScore.")

if __name__ == "__main__":
    main()
    
    

