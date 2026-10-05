import pandas as pd


# ---------------------------------------------------------
# INVENTORY EXCEPTION
# ---------------------------------------------------------

def check_inventory_exception(row):
    """
    Identify orders where requested quantity exceeds
    available inventory.

    Severity:
    High = severe inventory shortage
    Medium = moderate inventory shortage
    Low = minor inventory shortage
    """

    quantity = row["quantity"]
    inventory = row["available_inventory"]

    if inventory < quantity:

        shortage = quantity - inventory

        shortage_percentage = shortage / quantity

        if shortage_percentage >= 0.50:
            severity = "High"

        elif shortage_percentage >= 0.20:
            severity = "Medium"

        else:
            severity = "Low"

        return {
            "exception_type": "Inventory Shortage",
            "severity": severity,
            "problem": (
                f"Order requires {quantity} units, "
                f"but only {inventory} are available."
            ),
            "impact": (
                f"{shortage} units are unavailable "
                "for fulfillment."
            ),
            "recommended_action": (
                "Check alternate warehouse inventory, "
                "review replenishment options, or "
                "split the shipment."
            ),
        }

    return None


# ---------------------------------------------------------
# DELIVERY EXCEPTION
# ---------------------------------------------------------

def check_delivery_exception(row):
    """
    Identify orders where estimated delivery is later
    than the requested delivery date.

    Severity:
    High = 5 or more days late
    Medium = 3 to 4 days late
    Low = 1 to 2 days late
    """

    requested = pd.to_datetime(
        row["requested_delivery"]
    )

    estimated = pd.to_datetime(
        row["estimated_delivery"]
    )

    if estimated > requested:

        delay_days = (
            estimated - requested
        ).days

        if delay_days >= 5:
            severity = "High"

        elif delay_days >= 3:
            severity = "Medium"

        else:
            severity = "Low"

        return {
            "exception_type": "Delivery Risk",
            "severity": severity,
            "problem": (
                f"Estimated delivery is "
                f"{delay_days} days later than "
                "the requested delivery date."
            ),
            "impact": (
                f"Customer delivery may be delayed "
                f"by {delay_days} days."
            ),
            "recommended_action": (
                "Review supplier lead time, check "
                "alternate fulfillment options, or "
                "update the delivery commitment."
            ),
        }

    return None


# ---------------------------------------------------------
# SUPPLIER EXCEPTION
# ---------------------------------------------------------

def check_supplier_exception(row):
    """
    Identify orders associated with suppliers
    that have lower on-time delivery performance.

    Severity:
    High = below 80%
    Medium = 80% to below 85%
    Low = 85% to below 90%
    """

    on_time_rate = row[
        "supplier_on_time_rate"
    ]

    if on_time_rate < 0.90:

        if on_time_rate < 0.80:
            severity = "High"

        elif on_time_rate < 0.85:
            severity = "Medium"

        else:
            severity = "Low"

        return {
            "exception_type": "Supplier Performance",
            "severity": severity,
            "problem": (
                "Supplier on-time delivery rate is "
                f"{on_time_rate:.0%}."
            ),
            "impact": (
                "Lower supplier reliability may "
                "increase the risk of order delays."
            ),
            "recommended_action": (
                "Review supplier performance, confirm "
                "the order commitment, and evaluate "
                "an alternate supplier if needed."
            ),
        }

    return None


# ---------------------------------------------------------
# DATA QUALITY EXCEPTION
# ---------------------------------------------------------

def check_data_quality_exception(row):
    """
    Identify orders with missing required ERP information.

    Data quality issues are classified as Medium because
    incomplete information can prevent an order from
    being processed correctly.
    """

    required_fields = [
        "customer",
        "product",
        "supplier",
        "payment_terms",
    ]

    missing_fields = []

    for field in required_fields:

        if (
            pd.isna(row[field])
            or row[field] == ""
        ):
            missing_fields.append(field)

    if missing_fields:

        return {
            "exception_type": "Data Quality",
            "severity": "Medium",
            "problem": (
                "Required ERP information is missing: "
                + ", ".join(missing_fields)
            ),
            "impact": (
                "Incomplete information may prevent "
                "the order from being processed correctly."
            ),
            "recommended_action": (
                "Complete the missing order information "
                "before processing the order."
            ),
        }

    return None


# ---------------------------------------------------------
# DETECT ALL EXCEPTIONS
# ---------------------------------------------------------

def detect_exceptions(row):
    """
    Run all exception checks against an order.
    """

    checks = [
        check_inventory_exception,
        check_delivery_exception,
        check_supplier_exception,
        check_data_quality_exception,
    ]

    exceptions = []

    for check in checks:

        result = check(row)

        if result:
            exceptions.append(result)

    return exceptions


# ---------------------------------------------------------
# ANALYZE ORDERS
# ---------------------------------------------------------

def analyze_orders(df):
    """
    Analyze all orders and return a DataFrame
    containing detected exceptions.
    """

    results = []

    for _, row in df.iterrows():

        detected_exceptions = detect_exceptions(
            row
        )

        for exception in detected_exceptions:

            results.append(
                {
                    "order_id": row["order_id"],
                    "customer": row["customer"],
                    "product": row["product"],
                    "supplier": row["supplier"],
                    "region": row["region"],
                    "quantity": row["quantity"],
                    "available_inventory": row[
                        "available_inventory"
                    ],
                    "order_value": row[
                        "order_value"
                    ],
                    "supplier_rating": row[
                        "supplier_rating"
                    ],
                    "supplier_on_time_rate": row[
                        "supplier_on_time_rate"
                    ],
                    **exception,
                }
            )

    return pd.DataFrame(results)