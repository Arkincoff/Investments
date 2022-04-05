FROM python:3.10.2
RUN mkdir /app
ADD . /app
WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "Investments.py"]
