FROM python:3.11

WORKDIR /app

COPY requirememts.txt requirememts.txt

RUN pip install -r requirememts.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]