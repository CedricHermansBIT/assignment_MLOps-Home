FROM python:3.10
WORKDIR /code
COPY ./api/requirements.dev.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./api/app /code/app
COPY ./api/best_model /code/best_model
WORKDIR /code/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
