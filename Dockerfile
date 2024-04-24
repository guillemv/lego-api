FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./code /code/code
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
CMD ["uvicorn", "code.main:app", "--host", "0.0.0.0", "--port", "80"]