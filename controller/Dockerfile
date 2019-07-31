FROM python:3

RUN apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /controller

ENV FLASK_APP controller.py
ENV FLASK_RUN_HOST 0.0.0.0

COPY . .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY run.sh ./
COPY controller.py ./
COPY controller ./

RUN chmod +x ./run.sh

CMD ["./run.sh"]