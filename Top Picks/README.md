# MutualFundTracker Top Picks
An automated application that outputs an excel spreadsheet of Fidelity's top mutual funds picks along with performance and additional features

## Deployment

To run Top Picks:
  > Double click the 'Get Top Picks' shortcut
  > A dialog should pop up displaying the program's process
  > Once the pop up goes away, open topPicks.csv with Excel (or your favorite CSV editor) to view the results
  
Example of topPicks.csv
  > Ticker, Name, Category, Stars, NET, YTD, 1yr, 3yr, 5yr, 10yr



### Prerequisites

Don't have Python?
  > Open 'https://www.python.org/downloads/release/python-372/' in your favorite web browser
  > Download the package that fits your computer's needs (Windows/Mac/Linux)

Don't have the Request module?
  > Make sure you have Python (if not follow the steps above)
  > Open Powershell (or Terminal if on Mac)
  > Type 'python -m pip install request'

Get Top Picks Shortcut not working on Windows?
  > Change into Top Picks directory
  > Right click picks.py
  > Click 'Create Shortcut of "picks.py"'
  > In the Make Target field, enter 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -command "python picks.py"'
  > Run Get Top Picks shortcut
