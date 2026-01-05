#!/home/michael/PycharmProjects/Zurich-Linux-Pulldwn-ver3/.venv/bin/python3.10
import requests
import pandas as pd
import io

# alternate ECB api address is https://data-api.ecb.europa.eu/service/ this is the new site old one is repointed
# for a year after which it may switch off. Old one was: https://sdw-wsrest.ecb.europa.eu/service/
# Building blocks for the API URL
start = ''
end = ''

entrypoint = 'https://data-api.ecb.europa.eu/service/'  # Using protocol 'https'
resource = 'data'  # The resource for data queries is always 'data'
flowRef = 'EXR'  # Dataflow describing the data that needs to be returned, exchange rates in this case
key = 'D.GBP.EUR.SP00.A'  # Defining the dimension values, D -daily. the currency being measured, the other currency.SP00- type of exchange rates.A- teh series variation
# Define the parameters
parameters = {
    'startPeriod': '2025-01-01',  # Start date of the time series
    'endPeriod': '2025-04-14'  # End of the time series
}

# Construct the URL:
request_url = entrypoint + resource + '/' + flowRef + '/' + key

response = requests.get(request_url, params=parameters, headers={'Accept': 'text/csv'})

df = pd.read_csv(io.StringIO(response.text))

ts = df.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)

ts['TIME_PERIOD'] = pd.to_datetime(ts['TIME_PERIOD'])

ts_c = ts.rename(
    columns={'TIME_PERIOD': 'date', 'OBS_VALUE': 'rate'})  #to change 'TIME_PERIOD' to 'date', 'OBS_VALUE' to 'rate'
print(ts_c)

