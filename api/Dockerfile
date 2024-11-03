FROM python:3.7

WORKDIR /api

COPY requirements.txt /api/

RUN pip install -q -r requirements.txt

RUN apt-get update && apt-get install -y awscli

EXPOSE 5000

COPY . /api

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
