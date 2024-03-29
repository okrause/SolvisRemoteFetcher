# SolvisRemoteFetcher

## What?
Code to read sensor data from an Solvis Remote

This tool reads data via HTTP from a Solvis Remote (http://www.solvis.de/privatkunden/fernbedienung-solvisremote.html), parses it and puts it into a Python dict.

The results can be:
* printed to stdout
* send to an InfluxDB

## How?
Adjust the variables in .environment file to fit your environment.

Run the tool either directly via command line:
```
export $(cat .environment | xargs)
python3 SolvisRemoteFetcher/SolvisRemoteFetcher.py
```

or use
```
docker-compose build
docker-compose up
```

Make sure you run at least version "1714SP4120-2 10 12" of the WebApp on the Solvis Remote.

## Testing
Some basic unit tests are enabled. Use pytest.

Enjoy