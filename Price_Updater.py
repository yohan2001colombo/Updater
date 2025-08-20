#!/usr/bin/env python
# coding: utf-8

# In[30]:


# import requests
# import json

# # API endpoint
# url = "https://api.dambulladec.com/api/prices/by-date/2025-08-14"

# # Make the GET request
# response = requests.get(url)

# # Check if request was successful
# if response.status_code == 200:
#     data = response.json()
    
#     # Format output without the image
#     output = []
#     for item in data:
#         formatted_item = {
#             "id": item.get("id"),
#             "date": item.get("date"),
#             "min_price": item.get("min_price"),
#             "max_price": item.get("max_price"),
#             "product": {
#                 "id": item["product"].get("id"),
#                 "name": item["product"].get("name"),
#                 "type": item["product"].get("type")
#             }
#         }
#         output.append(formatted_item)
    
#     # Print nicely formatted JSON
#     print(json.dumps(output, indent=2))
# else:
#     print(f"Error fetching data: {response.status_code}")


# In[32]:


import requests
import pandas as pd
from datetime import datetime, timedelta

# Date range
start_date = datetime.today() - timedelta(days=1)
end_date = datetime.today()  # inclusive

# CSV file
csv_file = "dambulla_daily.csv"

# Load existing CSV or create empty
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        "Date", "Beans", "Carrot", "Cabbage", "Tomatoes",
        "Brinjal", "Pumpkin", "Snake gourd", "Lime",
        "Red Onions (local)", "Red Onions (imp)",
        "Potatoes (local)", "Potatoes (imp)"
    ])

# Loop over dates
current_date = start_date
while current_date <= end_date:
    date_str = current_date.date().isoformat()
    url = f"https://api.dambulladec.com/api/prices/by-date/{date_str}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # Create dictionary to hold mean prices for this day
        daily_prices = {"Date": date_str}
        
        # Group prices by product name and calculate mean
        prices_by_product = {}
        for item in data:
            product_name = item["product"].get("name")
            price = (item.get("min_price")+item.get("min_price"))/2 # or use (min+max)/2 if you want
            if product_name:
                prices_by_product.setdefault(product_name, []).append(price)
        
        for product, prices in prices_by_product.items():
            if product in df.columns:
                daily_prices[product] = sum(prices)/len(prices)  # mean price

        # Check if date exists in CSV
        if date_str in df["Date"].values:
            row_index = df.index[df["Date"] == date_str][0]
            for product, price in daily_prices.items():
                df.at[row_index, product] = price
        else:
            df = df.append(daily_prices, ignore_index=True)
        
        print(f"Data for {date_str} processed.")
    else:
        print(f"Error fetching data for {date_str}: {response.status_code}")

    current_date += timedelta(days=1)

# Save CSV
df.to_csv(csv_file, index=False)
print(f"All data saved/updated in {csv_file}.")


# In[ ]:




