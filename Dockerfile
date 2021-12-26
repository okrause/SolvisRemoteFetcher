FROM python:3-alpine

RUN addgroup --gid 10001 --system nonroot \
 && adduser  --uid 10000 --system --ingroup nonroot --home /home/nonroot nonroot

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY SolvisRemoteFetcher/SolvisRemoteFetcher.py .

USER nonroot

CMD [ "python3", "-u", "./SolvisRemoteFetcher.py"]