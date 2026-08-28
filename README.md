This project started out taking ECB rates from an ECB API (using a simple tkinter interface 
 with some date picker code (for the to and from date picking) and put them into a data frame 
before presenting the values in a tkinter graph view.
It worked but only worked for a currency(any) to Euro conversion. ECB API will not work for Euro 
to currency(any)
So,to do this I needed to use another API, I found an alternative using frankfurter.dev API. 
They have a range of API's that  cover my requirements, so I progressed that  aspect.
Then I developed the tkinter GUI some more and incorporated a tree view then a graph window and
improved the buttons. The latest iteration is the GUI Frames .py. This arranges the Tkinter  
gui much  more methodically with separate frames for each  part of the whole.
Future progress should include a currency  conversion tool allowing user to input an amount and 
also  pick one of the day rates to see what  it evaluates to in either Sterling or Euro.

