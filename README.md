# stockData
A python script to get stock data from alpha-vantage API, which plots the data in Candlesticks graphs and updates every one hour automatically. Also adds new data to a CSV continuously.

# Screenshots
![Example Screenshot 1](https://github.com/pssolanki111/stockData/blob/main/screenshots/22.PNG)

# Features
The program allows you to customize your results with 4 available options. These are:
    - Your API key (default will be used if left blank)
    - symbols' file - a text file containing symbol names. One name per line. All the symbol names will have their own graph plotted.
    - Interval - A dropdown with possible options 1min, 5min, 15min, 30min & 60min. Indicates duration between two consecutive data points in graph. Default being 30min.
    - Output Size - a dropdown with possible options compact & full. Compact will get most recent 100 data points whereas full will return all the data available data points. compact is default and recpmmended.

===================================================================================================

** Each symbol will have its own candlestick graph in its own sparate window.

** Each graph has two parts. Top one will be standard candlestick graph denoting OCHL (Open-Close-High-Low) vs Timestamp whereas the bottom one will be standard bar graph denoting total Volume vs Timestamp.

** The Graph once plotted will get updated every hour automatically.

** The information will also be written to a CSV file. Duplicate data will be left out. Each symnol will have its own separate CSV file. All the CSVs will be saved in the same folder where the script is stored.

** The program uses multiprocessing to make the most of resources available and hence resulting in good performance. 

===================================================================================================
# Dependencies

The script requires only the following third party packages/modules which are not included in official python distribution:
       - pandas
       - finplot
       
All other modules/pavkages used are part of standard python distribution and need not be installed separately.

![Example screenshot 2](https://github.com/pssolanki111/stockData/blob/main/screenshots/11.PNG)
