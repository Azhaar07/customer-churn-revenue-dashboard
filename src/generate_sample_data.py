from faker import Faker
import pandas as pd
import random

fake = Faker()

NUM_CUSTOMERS = 1000

regions = ["North", "South", "East", "West"]
plans = ["Basic", "Standard", "Premium"]

customers = []

for _ in range(NUM_CUSTOMERS):
    customers.append({
        "full_name": fake.name(),
        "region": random.choice(regions),
        "signup_date": fake.date_between(start_date="-2y", end_date="today"),
        "subscription_type": random.choice(plans),
        "status": random.choice(["Active", "Inactive"])
    })

df = pd.DataFrame(customers)

df.to_csv("data/sample/customers.csv", index=False)

print("customers.csv created successfully!")