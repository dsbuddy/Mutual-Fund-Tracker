# Mutual-Fund-Tracker
An automated application that inputs a list of mutual fund tickers with custom comments and outputs an excel spreadsheet of the mutual funds along with performance and additional features

## Deployment

To set up Fund Tracker:
  > Open input.csv with Excel (or your favorite CSV editor)
  > Enter ticker names of mutual funds in the first column
  > Enter comments in the second column

Example of input.csv
  > Fund Ticker, Fund Cusip ID

To run Fund Tracker:
  > Double click the RUNMUTFUND shortcut
  > A dialog should pop up displaying the program's process
  > Once the pop up goes away, open output.csv with Excel (or your favorite CSV editor) to view the results
  
Example of Output.csv
  > Ticker, Cusip, Category, Stars, NET, YTD, 1yr, 3yr, 5yr, 10yr, 10YrG


### Prerequisites


Don't have Python?
  > Open 'https://www.python.org/downloads/release/python-372/' in your favorite web browser
  > Download the package that fits your computer's needs (Windows/Mac/Linux)

Don't have the Request module?
  > Make sure you have Python (if not follow the steps above)
  > Open Powershell (or Terminal if on Mac)
  > Type 'python -m pip install request'

RUNMUTFUND Shortcut not working on Windows?
  > Right click total.py
  > Click 'Create Shortcut of "total.py"'
  > In the Make Target field, enter 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -command "python total.py"'
  > Run MUTFUND shortcut
