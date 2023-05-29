FROM python:3.10.6

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /temp/requirements.txt
COPY service /service
WORKDIR /service
EXPOSE 8000

# upgrade pip
RUN pip install --upgrade pip

RUN pip3 install -r /temp/requirements.txt


RUN adduser --disabled-password service-user

USER service-user