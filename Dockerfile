#Dockerfile, Image and Container

FROM python:3.11

ADD myOwnTurnItIn.py .

RUN pip install flask bert_score pymongo pdfplumber 

CMD ["python", "./myOwnTurnItIn.py"]



