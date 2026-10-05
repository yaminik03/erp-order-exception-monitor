-- Total orders
SELECT
    COUNT(*) AS total_orders
FROM orders;


-- Total order value
SELECT
    ROUND(SUM(order_value), 2) AS total_order_value
FROM orders;


-- Orders with inventory shortages
SELECT
    COUNT(*) AS inventory_shortages
FROM orders
WHERE available_inventory < quantity;


-- Orders with delivery risk
SELECT
    COUNT(*) AS delivery_risks
FROM orders
WHERE estimated_delivery > requested_delivery;


-- Supplier performance
SELECT
    supplier,
    COUNT(*) AS total_orders,
    ROUND(AVG(supplier_on_time_rate) * 100, 1) AS avg_on_time_rate,
    ROUND(AVG(supplier_rating), 2) AS avg_rating
FROM orders
GROUP BY supplier
ORDER BY avg_on_time_rate ASC;


-- Highest-value orders
SELECT
    order_id,
    customer,
    product,
    order_value
FROM orders
ORDER BY order_value DESC
LIMIT 10;