import numpy as np
import pandas as pd
from pathlib import Path


def generate_erp_orders(num_orders=1000, seed=42):
    rng = np.random.default_rng(seed)

    products = [
        "Industrial Safety Gloves",
        "Steel Storage Shelving",
        "Shipping Cartons",
        "Barcode Label Rolls",
        "Pallet Wrap",
        "Warehouse Scanners",
        "Thermal Printers",
        "Packaging Tape",
        "Office Workstations",
        "Ergonomic Office Chairs",
        "USB Docking Stations",
        "Laser Printers",
    ]

    customers = [
        "Atlantic Distribution",
        "SunCoast Retail",
        "Metro Office Supply",
        "Gulf Coast Logistics",
        "Southeast Wholesale",
        "Palm Business Solutions",
        "Evergreen Distribution",
        "Coastal Manufacturing",
    ]

    suppliers = [
        "NorthStar Industrial Supply",
        "BlueLine Distribution",
        "PrimeSource Materials",
        "Southeast Supply Co.",
        "Metro Logistics Supply",
        "Atlantic Warehouse Solutions",
    ]

    regions = [
        "Florida",
        "Georgia",
        "Texas",
        "North Carolina",
        "Virginia",
    ]

    rows = []

    for i in range(num_orders):
        product = rng.choice(products)
        customer = rng.choice(customers)
        supplier = rng.choice(suppliers)
        region = rng.choice(regions)

        quantity = int(rng.integers(10, 500))
        inventory = int(rng.integers(20, 600))

        unit_price = round(float(rng.uniform(25, 500)), 2)

        lead_time_days = int(rng.integers(3, 21))

        supplier_rating = round(
            float(rng.uniform(3.0, 5.0)), 1
        )

        supplier_on_time_rate = round(
            float(rng.uniform(0.75, 0.99)), 2
        )

        order_date = pd.Timestamp("2026-09-01") + pd.Timedelta(
            days=int(rng.integers(0, 30))
        )

        requested_delivery = order_date + pd.Timedelta(
            days=int(rng.integers(3, 15))
        )

        estimated_delivery = requested_delivery + pd.Timedelta(
            days=int(rng.integers(-2, 8))
        )

        payment_terms = rng.choice(
            ["Net 30", "Net 45", "Net 60", None],
            p=[0.35, 0.35, 0.20, 0.10],
        )

        rows.append(
            {
                "order_id": 10000 + i,
                "customer": customer,
                "product": product,
                "supplier": supplier,
                "region": region,
                "quantity": quantity,
                "available_inventory": inventory,
                "unit_price": unit_price,
                "lead_time_days": lead_time_days,
                "supplier_rating": supplier_rating,
                "supplier_on_time_rate": supplier_on_time_rate,
                "order_date": order_date.date(),
                "requested_delivery": requested_delivery.date(),
                "estimated_delivery": estimated_delivery.date(),
                "payment_terms": payment_terms,
            }
        )

    df = pd.DataFrame(rows)

    df["order_value"] = (
        df["quantity"] * df["unit_price"]
    ).round(2)

    output_path = Path("data/erp_orders.csv")
    output_path.parent.mkdir(exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} ERP orders.")
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    generate_erp_orders()