"""Case Study 3: Retail Inventory Optimization Tracker
Focus: Business Logic Automation & Local Persistence
Core Tech: Python Standard Library, json / csv Engine, Datetime Utilities
Business Scenario:
An online retailer frequently faces structural stockouts on high-demand inventory. Your goal is to write a script
that systematically calculates safety stock levels, logs emergency supply chain warnings, and saves the system
state to prevent critical loss of visibility.
Student Deliverables:
1. State Serialization: Read and decode the initial inventory records dynamically from a localized
inventory.json source template.
2. Algorithmic Threshold Checking: Compute a dynamic minimum safety value: 1.5 * Daily Lead Time
Demand. Flag items whose active counts drop below this value.
3. Log Generation: Create a text-based report named reorder_report_YYYY-MM-DD.txt capturing all critical
items requiring fulfillment.
4. Batch Mutations: Write execution procedures to apply inbound bulk replenishment additions and adjust item
pricing systematically"""

import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
# data set creating
df={
    "product_id":[1,2,3,4,5],
    "product_Name":["cellphone","chip","memory","screens","monitors"],
    "stock":[3,4,0,6,7],
    "user_request":[2,7,8,6,2],
    "price":[400,600,700,230,70]
}
stocks = pd.DataFrame(df)

# data analysis and cleaning
stocks.info()
print(stocks.to_string())

stocks["saftey_stock_levels"] = 1.5 * stocks["user_request"]
stocks["below_saftey_stock_levels"] = (stocks["stock"] < stocks["saftey_stock_levels"])

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

stocks["reorder"] = np.where(stocks["below_saftey_stock_levels"], current_time, None)

reorder_filter = stocks["reorder"].notna()
reordered_items_df = stocks[reorder_filter]
reordered_items_df.to_csv("reorder.txt",index=False)

# creating the reorder.txt
with open("reorder.txt","r") as f:
    print(f.read())

cond_multiplier = (stocks["user_request"] >= stocks["stock"]) | (stocks["stock"] <= 0)
cond_subtraction = (stocks["user_request"] < stocks["stock"]) | (stocks["stock"] > 0)

choices = [
    stocks["price"] * stocks["user_request"],
    stocks["price"] - stocks["user_request"]
]

stocks["price"] = np.select([cond_multiplier, cond_subtraction], choices, default=stocks["price"])

stocks["requested_stocks"] = (stocks["user_request"] - stocks["stock"]).where(
    stocks["user_request"] != stocks["stock"],
    stocks["user_request"]
)
print(stocks.to_string())

# graphs
plt.bar(stocks["product_Name"], stocks["stock"], label="Stock")
plt.bar(stocks["product_Name"], stocks["user_request"],
        alpha=0.5, label="User Request")

plt.title("Stock vs User Request")
plt.xlabel("Products")
plt.ylabel("Quantity")
plt.legend()
plt.xticks(rotation=30)
plt.show()

plt.bar(stocks["product_Name"], stocks["price"], color="orange")

plt.title("Product Price Comparison")
plt.xlabel("Products")
plt.ylabel("Price")
plt.xticks(rotation=30)
plt.show()

shortage = (stocks["user_request"] - stocks["stock"]).clip(lower=0)

plt.bar(stocks["product_Name"], shortage, color="red")

plt.title("Product Stock Shortage")
plt.xlabel("Products")
plt.ylabel("Missing Units")
plt.xticks(rotation=30)
plt.show()

safety_stock = 1.5 * stocks["user_request"]

plt.plot(stocks["product_Name"], stocks["stock"],
         marker="o", label="Current Stock")

plt.plot(stocks["product_Name"], safety_stock,
         marker="o", label="Safety Stock")

plt.title("Current Stock vs Safety Stock")
plt.xlabel("Products")
plt.ylabel("Quantity")
plt.legend()
plt.xticks(rotation=30)
plt.show()