import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

project_root = Path(__file__).resolve().parents[2]
output_file = project_root / "data" / "raw" / "sales_data.csv"

output_file.parent.mkdir(parents=True, exist_ok=True)

regions = {
    "North": ["India", "Nepal"],
    "South": ["India", "Sri Lanka"],
    "East": ["India", "Bangladesh"],
    "West": ["India", "UAE"]
}

products = {
    "Laptop": ("Electronics", 800),
    "Phone": ("Electronics", 500),
    "Tablet": ("Electronics", 350),
    "Printer": ("Office", 250),
    "Monitor": ("Office", 300),
    "Chair": ("Furniture", 180),
    "Desk": ("Furniture", 400),
    "Headphones": ("Accessories", 100)
}

segments = ["Consumer", "Corporate", "Small Business"]

start_date = date(2024, 1, 1)
end_date = date(2024, 12, 31)

rows = []

current_date = start_date
order_id = 1

while current_date <= end_date:

    daily_orders = random.randint(25, 45)

    for _ in range(daily_orders):

        region = random.choice(list(regions.keys()))
        country = random.choice(regions[region])

        product = random.choice(list(products.keys()))
        category, base_price = products[product]

        segment = random.choice(segments)

        quantity = random.randint(1, 8)

        unit_price = base_price * random.uniform(0.90, 1.10)

        discount = random.uniform(0.00, 0.15)

        # Deliberate Q3 decline
        if current_date.month in [7, 8, 9]:

            # Region West is affected more strongly
            if region == "West":
                quantity = max(1, int(quantity * 0.65))
                discount += 0.03

            # Laptop and Phone sales decline in Q3
            if product in ["Laptop", "Phone"]:
                quantity = max(1, int(quantity * 0.70))

        revenue = quantity * unit_price * (1 - discount)

        cost = revenue * random.uniform(0.55, 0.75)

        profit = revenue - cost

        rows.append([
            order_id,
            current_date.isoformat(),
            region,
            country,
            product,
            category,
            segment,
            round(quantity, 2),
            round(unit_price, 2),
            round(discount, 4),
            round(revenue, 2),
            round(cost, 2),
            round(profit, 2)
        ])

        order_id += 1

    current_date += timedelta(days=1)


columns = [
    "order_id",
    "order_date",
    "region",
    "country",
    "product",
    "category",
    "customer_segment",
    "quantity",
    "unit_price",
    "discount",
    "revenue",
    "cost",
    "profit"
]

with open(output_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow(columns)
    writer.writerows(rows)

print("Dataset created successfully.")
print("File:", output_file)
print("Number of rows:", len(rows))
print("Number of columns:", len(columns))