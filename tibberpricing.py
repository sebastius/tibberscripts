#!/usr/bin/env python3

import tibber
import datetime
import csv
import os

if not os.path.exists("tibberpricing"):
    os.makedirs("tibberpricing")

def convert_to_datetime(date_string):
  # Parse the date string using the strptime function
  date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')
  return date

# import your Tibber token. Keep it secret!
try:
    with open(f'../tibber.key', 'r') as f:
        print("Using your personal Tibber token")
        account = tibber.Account(f.read().strip())
except FileNotFoundError:
    print("Using Tibber demo token")
    account = tibber.Account(tibber.DEMO_TOKEN)
    pass

home = account.homes[0]

todayprices = home.current_subscription.price_info.today
tomorrowprices = home.current_subscription.price_info.tomorrow

prices = [0]*len(todayprices)

for i in range(0, len(todayprices)):
    date_string = todayprices[i].starts_at
    date = convert_to_datetime(date_string)
    prices[i] = [date,int(todayprices[i].total * 10000)] # Tibber 

date = prices[0][0]
date_str = date.strftime("%Y-%m-%d")
filename = f"tibberpricing/{date_str}.csv"
print(filename)
if os.path.exists(filename):
    os.remove(filename)

if (len(tomorrowprices)>0):
    date = date + datetime.timedelta(days=1)
    date_str = date.strftime("%Y-%m-%d")
    filename = f"tibberpricing/{date_str}.csv"
    print(filename)
    if os.path.exists(filename):
        os.remove(filename)

    print("adding tomorrows prices")
    for i in range(0, len(tomorrowprices)):
        date_string = tomorrowprices[i].starts_at
        date = convert_to_datetime(date_string)
        prices.append([date,int(tomorrowprices[i].total * 10000)])
else:
    print("no tomorrow pricing available yet, check back after 13:00")

print()

# Create a new file for each date and write the data to it
for price in prices:
    date = price[0]
    data = price[1]

    # Construct the filename based on the date
    date_str = date.strftime("%Y-%m-%d")
    filename = f"tibberpricing/{date_str}.csv"

    # Open the file in write mode and create a CSV writer object
    with open(filename, "a") as f:
        writer = csv.writer(f)
        # Write the data to the file
        writer.writerow([date, data])