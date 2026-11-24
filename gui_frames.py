""" This is a Tkinter project for currency rates checking.
It uses a Tkinter format interface using frames to separate each area for date picking, showing values and graphing.
We are using tkinter grid manager protocols in this version to arrange all the various objects inside separate frames
and this allows for much  easier placing and separation of our widgets that we need.
The button functions call functions for running an API which pulls down data from Frankfurter API source.
It is also able to use tree view to display the values returned as well as a Matplotlib graph view.
It can handle both sterling to Euro and Euro to Sterling. This version includes a small currency
value calculator based on the currency amount entered and using one of the daily values.
Finally, a code change on line 16 was introduced to make Matplotlib
use TkAgg instead of randomly selecting another backend such as QTAgg. QTAgg has some incompatible components such as
pyside2 and shiboken2 which are incompatible with the latest NumPy 2.4.4 version loaded in this project's packages"""

from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
import requests
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.dates as mdates

# now to put in a few pre-set variables for pyplot and global start values
#-------------------------------------Globals/Variables-------------------------------------------------------------

start_date = None
end_date = None
fig, ax = plt.subplots() # now declare the plot variable
# We will later construct the Tkinter window which includes a plot window
# There are two primary interfaces for plotting with Matplotlib the first  is  the pyplot approach using "Matplotlib"
# internal pyplot module. The second is the object-oriented style, you explicitly create Figure and Axes objects and
# then call methods on the resulting objects.
# As soon as you see the following line, you know you’re dealing with the object-oriented style:
# # fig, ax = plt.subplots().
# This gives you the most control over customising your plots and keeping track of multiple plots.
# This is the option seen in the next few code lines.

# -----------------------------------Create a GUI app ----------------------------------------------------

# The code used here caused PyCharm warning about unrecognised attributes. This is because I initially started with
# intention of using a pandas Dataframe but PyCharm was unhappy when I named variables app.df and app.data.
# So we wrap the Tk gui code inside a clean, object-oriented subclass and name the non-standard attributes there.

# 1. Define a custom subclass inheriting from Tk
class FileApp(Tk):

    def __init__(self):
        super().__init__()

        self.title(" STG to Euro /Euro to STG by MMcN Ver 1.0.0.0 ") # Change the default "Tk" title to something else

        # 2. Pre-declare our DataFrame and Data attributes here
        self.df: pd.DataFrame | None = None
        self.data: dict | None = None
        self.graph_title: str = ""

# 2. Now we can initialise our app in the normal way using the new class.
app = FileApp()
app.geometry("850x700")
# This ensures the window can grow to fill the space in the frame even  if it is stretched later.
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)
# This ensures the window can grow, but never shrink smaller than your base frame.
app.minsize(500, 700)

app.df = pd.DataFrame({"Col1": [1, 2]}) # placeholder variable for use in future pandas data frame
app.data = {"key": "value"} # placeholder variable for use in a treeview dictionary later.
# Now PyCharm knows these 2 exist inside a placeholder dictionary called app.data and will not flag errors in the code
# to follow. I started out with the aim of using a pandas data frame approach but later realised I could also use a
# simple dictionary format for use in treeview later.
# I have included app.df in the variable set up as I later changed the key function further along
# so it can work for either format.


# ----------------------------------Functions------------------------------------------------------------

# now set up the functions we will use in this module


def update_label1(_event):
    global start_date
    label1.config(text="Selected date:" + cal1.get_date())
    start_date = cal1.get_date()
    print(start_date)


def update_label2(_event):
    global end_date
    label2.config(text="Selected date:" + cal2.get_date())
    end_date = cal2.get_date()
    print(end_date)


# next function query's frankfurter API for Euro to GBP rates and returns a JSON file which is converted to both a
# list dictionary and a Pandas data frame by the following wrapper function "load_euro_data"

def euro_gbp():
    url = "https://api.frankfurter.dev/v2/rates?"
    params = {"from": {start_date}, "to": {end_date}, "base": "EUR", "quotes": "GBP"}
    response = requests.get(url, params=params)
    data = response.json()
    print(data)  # just a debug to be removed later
    return data


# this gave us a variable called "data" with the downloaded json contents as requested inside

# now I need a wrapper function to call the euro_gbp function in button 2 and store the resulting data frame created
# from that function. Later on in this code, we allocate this wrapper function to the button2 command.
# we also clear the calculator window ready for a calculation with the new rates obtained.
def load_euro_data():
    app.data = euro_gbp()  # list dictionaries
    app.df = pd.DataFrame(app.data)  #optional DataFrame

    app.graph_title = "Euro to GBP Exchange Rates"
    amount_label.config(text="Amount in EUR:")
    result_label.config(text="Result in GBP:")
    clear_calculator()
    populate_treeview()


# now create the function for GBP to Euro using the frankfurter API again which returns a JSON file which is converted
# to both a list dictionary and a Pandas data frame by the following wrapper function "load_gbp_data"
def gbp_euro():
    url = "https://api.frankfurter.dev/v2/rates?"
    params = {"from": {start_date}, "to": {end_date}, "base": "GBP", "quotes": "EUR"}
    response = requests.get(url, params=params)
    data = response.json()
    print(data)  # just a debug to be removed later
    return data


# this gave us a variable called "data" with the downloaded json contents as requested inside

# next a wrapper function to call the gbp_euro function in from button 1 and store the resulting data frame created.
# we also clear the calculator window ready for a calculation with the new rates obtained.
def load_gbp_data():
    app.data = gbp_euro()  # list dictionaries
    app.df = pd.DataFrame(app.data)  # optional DataFrame

    app.graph_title = "GBP to Euro Exchange Rates"
    amount_label.config(text="Amount in GBP:")
    result_label.config(text="Result in EUR:")
    clear_calculator()
    populate_treeview()


# This next function is to generate the main populated view of the data dictionary data into a Treeview.
# The Treeview is Initialised as a placeholder object further on in this code when the frame, holding the Treeview
# (which is empty) is created. This is triggered by wrapper function (above) which in turn is triggered by one of
# the "get rates" buttons. Please also note that I have added a line to pass the tree view to the graph window

def populate_treeview():
    if not app.data:
        return

    # Remove old rows
    tree.delete(*tree.get_children())

    # Configure columns
    tree["columns"] = ("date", "rate")

    tree.heading("date", text="Date")
    tree.heading("rate", text="GBP")

    # insert data
    for row in reversed (app.data): # sort the data rows by latest first (reverse to how they are in the actual app.data
        tree.insert(
            "",
            "end",
            values=(row["date"], row["rate"])
        )

    # Now plot what was just inserted
    plot_from_treeview()


# this alternate populate function version is based on a pandas data frame format of the api data.
# For now, we go with the list dictionary version above but the Panadas data frame might be useful for analysis in
# the future so is included here.

def populate_treeview_panda_df():
    if app.df is None:
        return

    # Remove old rows
    tree.delete(*tree.get_children())

    # Configure columns
    tree["columns"] = list(app.df.columns)

    # Create headings
    for col in app.df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Insert rows
    for index, row in app.df.iterrows():
        tree.insert("", "end", values=[row["date"].strftime("%Y-%m-%d"), row["GBP"]])


def plot_from_treeview():  # this function populates the treeview data onto the graph

    dates = []
    rates = []

    # read every row currently in the tree
    for row in tree.get_children():
        row_data = tree.item(row)["values"]

        # column 0 = Date
        dates.append(
            datetime.strptime(row_data[0], "%Y-%m-%d")
        )
        # column 1 = Rate
        rates.append(
            float(row_data[1])
        )

    # clear previous graph
    ax.clear()

    # Draw line
    ax.plot(
        dates,
        rates,
        marker='o'
    )

    # Format the x-axis as dates
    ax.xaxis.set_major_locator(mdates.DayLocator())
    # ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d")) # year,month date option
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))  # month (by name) and date option

    ax.set_title(app.graph_title) # changes graph title to reflect currency conversion requested on graph
    ax.set_xlabel("Date")
    ax.set_ylabel("Rate")

    fig.autofmt_xdate()
    # Refresh display
    canvas.draw()

# Calculator functions for exchange rate display

def get_selected_rate(): # pick rate to use from tree view

    selected_item = tree.selection()

    if not selected_item:
        return None

    row_data = tree.item(selected_item[0])["values"]

    rate = float(row_data[1])

    return rate

def display_result(message):
    result_entry.config(state="normal")
    result_entry.delete(0, END)
    result_entry.insert(0, message)
    result_entry.config(state="readonly")

def clear_calculator():
    amount_entry.delete(0, END)
    display_result("")

def calculate_amount(): # calculation to take chosen rate from tree view and display result

    rate = get_selected_rate()

    if rate is None:
        display_result("Please select a rate first")
        return

    amount = amount_entry.get()

    try:
        amount = float(amount)
    except ValueError:
        display_result("Enter a valid amount")
        return

    converted = amount * rate

    result_entry.config(state="normal")
    result_entry.delete(0, END)
    result_entry.insert(0, f"{converted:.2f}")
    result_entry.config(state="readonly")

#-------------------------------------------------------- GUI----------------------------------------------------------
# now we create the calendar widgets and also the process for picking start and end dates and set up the minimum
# start dates visible in the calendar picker view before we select actual dates for the search.
# We keep all the calendars and query buttons in a side frame isolated from the plot window in another frame.


# 1. THE SIDEBAR Frame(Column 0)
sidebar_frame = Frame(app)
sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="ns")  # "ns" makes it full height

# Now add all the widgets INSIDE the sidebar_frame-----------------------------------------------------------------
# Notice they all start at row 0, 1, 2... INSIDE this frame

# Start date calendar buildup  process
Label(sidebar_frame, text="Select Report Start Date").grid(row=0, column=0, pady=5)

cal1 = Calendar(sidebar_frame, mindate=datetime(2020, 1, 1), selectmode='day', date_pattern='yyyy-mm-dd',
                showweeknumbers=False,
                background="blue")
cal1.grid(row=1)

cal1.bind("<<CalendarSelected>>", update_label1)
label1 = Label(sidebar_frame, text="")  # we create a label space to show the selected date but leave it empty for now
label1.grid(pady=10, row=2, column=0)

# End date calendar
Label(sidebar_frame, text="Select Report End Date").grid(row=3, column=0, pady=5)
cal2 = Calendar(sidebar_frame, mindate=datetime(2020, 1, 1), selectmode='day', date_pattern='yyyy-mm-dd',
                showweeknumbers=False,
                background="blue")
cal2.grid(row=4, column=0, sticky="n")
cal2.bind("<<CalendarSelected>>", update_label2)
label2 = Label(sidebar_frame, text="")  # we create a label space to show the selected date but leave it empty for now
label2.grid(pady=5, row=5)

ttk.Label(
    sidebar_frame,
    text="CURRENCY CALCULATOR"
).grid(row=10, column=0, pady=(5, 5))

amount_label = ttk.Label(
    sidebar_frame,
    text="Amount to convert:"
)
amount_label.grid(row=11, column=0, pady=5)

amount_entry = ttk.Entry(
    sidebar_frame,
    width=15
)

amount_entry.grid(row=12, column=0, pady=5)

result_label = ttk.Label(
    sidebar_frame,
    text="Converted amount:"
)
result_label.grid(row=15, column=0, pady=(10, 5))

result_entry = ttk.Entry(
    sidebar_frame,
    width=20,
    state="readonly"
)

result_entry.grid(row=16, column=0, pady=5)

explanation_frame = Frame(app, height=60)
explanation_frame.grid(row=2, column=1, rowspan=1, sticky="ew")  # "ns" makes it full height
Label(explanation_frame, text="To calculate conversion pick an exchange rate from tree view above first").grid(
    row=0, column=0, padx=50, pady=5)

# ---------------------------------------------------Buttons------------------------------------------------------

# create the two buttons required under the calendars in column 0 of the sidebar frame

btn1 = ttk.Button(sidebar_frame, text="Get GBR to Euro Rates", command=load_gbp_data)  # we create a button to trigger
# the rates request using the load_gbp_data wrapper function which calls the main gbp_euro function and returns values
btn2 = ttk.Button(sidebar_frame, text="Get Euro to GBR Rates", command=load_euro_data)  # we create a button to trigger
# the rates request using the load_euro_data wrapper function which calls the main euro_gbh function and returns values.
btn3 = ttk.Button(sidebar_frame, text="Calculate", command=calculate_amount)

btn1.grid(row=6, column=0, rowspan=2, pady=5)
btn2.grid(row=8, column=0, rowspan=2, pady=5)
btn3.grid(row=13, column=0, rowspan=2, pady=5)

# 2. THE GRAPH Frame(Column 1)
# Now lets move on to create the graph display which will be in a separate frame row 0 but column 1

# 1. Create the canvas container frame. Note each frame lives inside the master tkinter window "app"
# we ensure that the graph frame will take up the space to its extent with the "weight" option
graph_frame = Frame(app, width=500, height=700)
graph_frame.grid_columnconfigure(0, weight=1)
graph_frame.grid_rowconfigure(0, weight=1)
graph_frame.grid(row=0, column=1, sticky="nsew")

# 2. Prevent the frame from shrinking to the graph's size
graph_frame.grid_propagate(False)

# 3. Place the canvas inside the frame
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

# 3. THE DATA VIEW Frame(Column 0)
# Create the Data Frame
data_frame = Frame(app, height=200)  # Give it a starting height
data_frame.grid(row=1, column=1, sticky="nsew")

# Make sure the main window knows Row 1 (data) and Row 0 (graph) share the height
app.rowconfigure(0, weight=3)  # Graph gets more space
app.rowconfigure(1, weight=1)  # Data gets less space

# now to create an empty Treeview for use later in the code by a function calling a populated tree view
tree = ttk.Treeview(data_frame, show='headings')
tree.pack(fill="both", expand=True)

#------------------------------------------ closer section ----------------------------------------------------

# Complete the loop code line for displaying app but also include some code to make sure Matplotlib closes
def on_closing():
    plt.close('all')  # Kills all open Matplotlib figures
    app.quit()  # Stops the Tkinter mainloop
    app.destroy()  # Closes the window


app.protocol("WM_DELETE_WINDOW", on_closing)

app.mainloop()
