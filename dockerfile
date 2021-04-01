FROM python:3.7-alpine

COPY . /throwaway
RUN cp /throwaway/config.json . || echo 'config.json does not exist'
RUN rm -rf /throwaway
COPY src/config.py /src/
COPY src/main.py /src/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /src
CMD ["python3", "main.py"]
