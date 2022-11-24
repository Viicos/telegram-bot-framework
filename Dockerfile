# syntax=docker/dockerfile:1.4
FROM python:3.10-slim-buster

EXPOSE 443

RUN apt-get update && apt-get -y upgrade

WORKDIR /app

COPY ./requirements /app/requirements
RUN pip install -U pip setuptools \
    && pip install -r requirements/requirements.txt

RUN useradd -M user
RUN chown -R user /app
USER user

COPY . /app/

ENTRYPOINT ["python3"]
CMD ["src/main.py"]
