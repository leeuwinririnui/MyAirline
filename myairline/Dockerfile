FROM python:3.7.1

WORKDIR /code

RUN pip install Django requests

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
