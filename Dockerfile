FROM python:3.8.12-buster

RUN pip install -U pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy only the directories that exist
COPY facial_expression /facial_expression
COPY API /API
COPY gen_ai /gen_ai

# Copy individual files
COPY setup.py /setup.py
COPY app.py /app.py
COPY README.md /README.md

CMD uvicorn API.api:app --host 0.0.0.0 --port $PORT
