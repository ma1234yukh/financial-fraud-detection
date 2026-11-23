import csv, os, random
from datetime import datetime, timedelta, timezone

random.seed(42)
os.makedirs("data", exist_ok=True)

countries = ["IN", "IN", "IN", "US", "GB", "SG"]
rows = []
start = datetime.now(timezone.utc) - timedelta(days=30)

for customer_id in range(1, 151):
    home_country = random.choice(["IN", "IN", "IN", "US", "GB"])
    count = random.randint(12, 45)
    base_time = start + timedelta(days=random.randint(0, 10))
    for _ in range(count):
        ts = base_time + timedelta(minutes=random.randint(0, 30 * 24 * 60))
        country = home_country if random.random() < 0.92 else random.choice(countries)
        amount = round(random.lognormvariate(7.4, 1.0), 2)
        # Inject a few synthetic high-risk patterns for demonstration.
        if customer_id % 23 == 0 and random.random() < 0.22:
            amount = round(random.uniform(100000, 250000), 2)
        if customer_id % 19 == 0 and random.random() < 0.30:
            ts = base_time + timedelta(days=12, minutes=random.randint(0, 7))
        rows.append([
            f"TX{len(rows)+1:07d}", customer_id, ts.isoformat(),
            amount, random.choice(["CARD", "UPI", "BANK_TRANSFER", "WALLET"]),
            country, random.choice(["SUCCESS", "SUCCESS", "SUCCESS", "DECLINED"]),
            f"MER{random.randint(1, 80):03d}"
        ])

rows.sort(key=lambda r: r[2])
with open("data/transactions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["transaction_id", "customer_id", "transaction_time", "amount",
                     "channel", "country_code", "status", "merchant_id"])
    writer.writerows(rows)

print(f"Created data/transactions.csv with {len(rows)} synthetic transactions.")
