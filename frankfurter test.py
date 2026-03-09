import requests

import requests
import pandas as pd

url = "https://api.frankfurter.dev/v1/2026-01-01..2026-02-28"
params = {
    "symbols": "GBP"
}

response = requests.get(url, params=params)
data = response.json()
print(data)

""" Now we have a variable called data with Json data inside and we will want to change that into a pandas data frame "
 format so we can work more easily with it. The Json format contains a series of dictionary's that pandas can extract 
 using the data frame from dict option. Inside data there is a Rates dictionary and there is a sub dictionary 
 with key/value pairs with currency and currency rate which we can extract and use in our Data frame"""

df = pd.DataFrame.from_dict(data["rates"], orient="index").reset_index()
df.columns = ["date", "GBP"]

df["date"] = pd.to_datetime(df["date"])

print(df)
