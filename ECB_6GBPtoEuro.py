""" this is a complete GPB to Euro exchange Script with a Tkinter interface to pick to and from dates 
and an API which pulls down data in the csv format from ECB which is converted to a Pandas 
DF format for use in a Mathplot lib Function to plot the data."""
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
import requests
import pandas as pd
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.backends.backend_tkagg import (
     FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np


# First  we create two  empty variables to hold the start and end dates required for the ECB parameters argument
start_date = None
end_date = None


# the next two functions store the date selected event in each calendar into a variable called start date and end date
# for use later in the ECB function. Note the calendar dates appear to be in date time format and do not need
# further formatting to be recognised by the ECB API function later on.

def update_label1(event):
    global start_date
    label1.config(text = "Selected date:" + cal1.get_date())
    start_date = cal1.get_date()
    print(start_date)


def update_label2(event):
    global end_date
    label2.config(text = "Selected date:" + cal2.get_date())
    end_date = cal2.get_date()
    print(end_date)


# Now we construct the Tkinter window
root = tk.Tk()
root.title("ECB STG to Euro")
root.geometry('950x600')
fig, ax = plt.subplots()

# Create Canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)


# Start date calendar
tk.Label(root, text="Select Report Start Date").pack()
cal1 = Calendar(root, mindate= datetime(2020,1,1), selectmode='day', date_pattern='yyyy-mm-dd',
                showweeknumbers= False,
                background = "blue")
cal1.pack(pady=5, padx=10)
cal1.bind("<<CalendarSelected>>", update_label1)
label1 = tk.Label(root, text = "") # we create a label space to display the selected date but leave it empty for now
label1.pack(pady=10)


# End date calendar
tk.Label(root, text="Select Report End Date").pack(pady=5)
cal2 = Calendar(root, mindate= datetime(2020,1,1), selectmode='day', date_pattern='yyyy-mm-dd',
                showweeknumbers= False,
                background = "blue")
cal2.pack(pady=5, padx=10)
cal2.bind("<<CalendarSelected>>", update_label2)
label2 = tk.Label(root, text = "") # we create a label space to display the selected date but leave it empty for now
label2.pack(pady=10)

# Now the main ECB API fetch function retrieves the data in a CSV format and is  converted in to  a data frame

def ecb():
    d1 = start_date
    d5 = end_date
    entrypoint = 'https://data-api.ecb.europa.eu/service/'  # Using protocol 'https'.this is new API old one dead
    resource = 'data'  # The resource for data queries is always 'data'
    flow_ref = 'EXR'  # Dataflow describing the data that needs to be returned, exchange rates in this case
    key = 'D.GBP.EUR.SP00.A'  # Defining the dimension values, D -daily. the currency being measured, the other
    # currency.SP00- type of exchange rates.A- teh series variation
    # Define the parameters
    parameters = {
    'startPeriod': d1,  # Start date of the time series (d1 is just a variable value input from calendar1)
    'endPeriod': d5  # End of the time series (d5 is just a variable value input from calendar2)
    }

    # Construct the URL path:
    request_url = entrypoint + resource + '/' + flow_ref + '/' + key

    response = requests.get(request_url, params=parameters, headers={'Accept': 'text/csv'})

    df = pd.read_csv(io.StringIO(response.text))


    ts = df.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)

    ts['TIME_PERIOD'] = pd.to_datetime(ts['TIME_PERIOD'])

    ts_c = ts.rename(
    columns={'TIME_PERIOD': 'date', 'OBS_VALUE': 'rate'})  # to change 'TIME_PERIOD' to 'date', 'OBS_VALUE' to 'rate'
    print(ts_c)
    # ax.plot(ts_c,['rate'])
    ts_c.plot(ax=ax, x='date', y='rate')
    canvas.draw()
btn3 = tk.Button(root, text="Get ECB Rates", command=ecb)
btn3.pack(pady=45)
root.mainloop()
