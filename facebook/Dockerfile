FROM python:3.10
WORKDIR /app/
COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN pip3 install pipenv
RUN pipenv install
COPY . /app/