#!/usr/bin/env python3

import csv
from datetime import datetime, timedelta, timezone
import os

# Get current date and format it as a string in the desired format
today = datetime.now()
date_str = today.strftime('%Y-%m-%d')

tomorrow = today + timedelta(days=1)
tomorrow_str = tomorrow.strftime('%Y-%m-%d')

# Open the file with the current date in the filename
try:
    with open(f"tibberpricing/{date_str}.csv", 'r') as csv_file:
        # Use the csv module to read the file and store the contents in the 'prices' list
        csv_reader = csv.reader(csv_file)
        prices = list(csv_reader)
except FileNotFoundError:
    print('stuk')
    pass

# And if tomorrow exists, also get that
try:
    with open(f"tibberpricing/{tomorrow_str}.csv", 'r') as csv_file:
        # Use the csv module to read the file and store the contents in the 'prices' list
        csv_reader = csv.reader(csv_file)
        prices += list(csv_reader)
except FileNotFoundError:
    print('stuk')
    pass

# Convert the strings to properly useable content. Column 0 is date/time, 1 is the price. 
for row in prices:
    row[0] = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S%z')
    row[1] = int(row[1])


#Dishwasherconsumption, create a table of consumption per minute.
dishwasherprofile = [[15, 0.700], [75, 0.07]] # minutes, KWh
dishwasherperminute =[]
for i in range(0, len(dishwasherprofile)):
    for j in range(0, dishwasherprofile[i][0]):
        dishwasherperminute.append(dishwasherprofile[i][1]/dishwasherprofile[i][0]) #calculate KWh per minute for the profile

def find_rate(timestamp):
    timestamp = timestamp.replace(minute=0, second=0, microsecond=0)
    for i, row in enumerate(prices):
        if (row[0] == timestamp):
            return row[1]
    return -1

def find_cost(timestamp):
    totalconsumption = 0
    for i in range(0, len(dishwasherperminute)):
        rate = find_rate(timestamp+timedelta(minutes=i))/10000
        totalconsumption = totalconsumption + dishwasherperminute[i] * rate
    return totalconsumption

starttime = datetime.now()
tz = timezone(timedelta(hours=1))
starttime = starttime.replace(tzinfo=tz, second=0)

def print_cost(timestamp):
    print("Runtime:", timestamp.strftime('%H:%M'),"-", (timestamp+timedelta(minutes=len(dishwasherperminute))).strftime('%H:%M'),", cost: EUR","{:.2f}".format(find_cost(timestamp)))
    return
    
starttime = datetime.now()
tz = timezone(timedelta(hours=1))
starttime = starttime.replace(tzinfo=tz, second=0)


timestamp = starttime
while (timestamp + timedelta(minutes=len(dishwasherperminute))) <= prices[-1][0]:
    print_cost(timestamp)
    timestamp = timestamp + timedelta(minutes=60)

## while value <= 13:



