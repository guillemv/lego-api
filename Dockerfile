FROM python:3.9

WORKDIR /app

COPY ./requirements.txt .
COPY ./code/ .    # ← Copia solo el contenido del directorio code/ al WORKDIR

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]