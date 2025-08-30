-- Schemas analíticos
CREATE SCHEMA IF NOT EXISTS stg;
CREATE SCHEMA IF NOT EXISTS mart;

-- Tabelas RAW simulando ingestão inicial
CREATE TABLE IF NOT EXISTS raw_orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_value NUMERIC,
    payment_type TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS raw_customers (
    customer_id INT,
    customer_name TEXT,
    email TEXT,
    registration_date DATE,
    city TEXT,
    state TEXT
);