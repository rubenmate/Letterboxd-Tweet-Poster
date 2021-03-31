FROM python:3.7-alpine

COPY foo config.json /
COPY src/config.py /src/
COPY src/main.py /src/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /src
CMD ["python3", "main.py"]