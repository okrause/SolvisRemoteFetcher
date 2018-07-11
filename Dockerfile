FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY SolvisRemoteFetcher/SolvisRemoteFetcher.py .

CMD [ "python3", "-u", "./SolvisRemoteFetcher.py"]