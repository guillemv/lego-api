FROM python:3.9
WORKDIR /
COPY ./requirements.txt /requirements.txt
COPY ./code /code
RUN pip install -r /requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]