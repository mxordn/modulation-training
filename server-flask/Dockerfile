FROM python:3.9-bookworm

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y inkscape

COPY . .

CMD [ "python3", "run.py" ]
