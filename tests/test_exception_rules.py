import pandas as pd

from src.exception_rules import (
    check_inventory_exception,
    check_delivery_exception,
    check_supplier_exception,
    check_data_quality_exception,
)


def test_inventory_shortage():
    row = pd.Series(
        {
            "quantity": 500,
            "available_inventory": 120,
        }
    )

    result = check_inventory_exception(row)

    assert result is not None
    assert result["exception_type"] == "Inventory Shortage"
    assert result["severity"] == "High"


def test_no_inventory_shortage():
    row = pd.Series(
        {
            "quantity": 100,
            "available_inventory": 200,
        }
    )

    result = check_inventory_exception(row)

    assert result is None


def test_delivery_exception():
    row = pd.Series(
        {
            "requested_delivery": "2026-09-10",
            "estimated_delivery": "2026-09-17",
        }
    )

    result = check_delivery_exception(row)

    assert result is not None
    assert result["exception_type"] == "Delivery Risk"
    assert result["severity"] == "High"


def test_no_delivery_exception():
    row = pd.Series(
        {
            "requested_delivery": "2026-09-17",
            "estimated_delivery": "2026-09-15",
        }
    )

    result = check_delivery_exception(row)

    assert result is None


def test_supplier_exception():
    row = pd.Series(
        {
            "supplier_on_time_rate": 0.78,
        }
    )

    result = check_supplier_exception(row)

    assert result is not None
    assert result["exception_type"] == "Supplier Performance"
    assert result["severity"] == "High"


def test_reliable_supplier():
    row = pd.Series(
        {
            "supplier_on_time_rate": 0.95,
        }
    )

    result = check_supplier_exception(row)

    assert result is None


def test_missing_payment_terms():
    row = pd.Series(
        {
            "customer": "Atlantic Distribution",
            "product": "Shipping Cartons",
            "supplier": "NorthStar Industrial Supply",
            "payment_terms": None,
        }
    )

    result = check_data_quality_exception(row)

    assert result is not None
    assert result["exception_type"] == "Data Quality"
    assert result["severity"] == "Medium"


def test_complete_order():
    row = pd.Series(
        {
            "customer": "Atlantic Distribution",
            "product": "Shipping Cartons",
            "supplier": "NorthStar Industrial Supply",
            "payment_terms": "Net 30",
        }
    )

    result = check_data_quality_exception(row)

    assert result is None