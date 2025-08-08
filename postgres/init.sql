CREATE TABLE IF NOT EXISTS pedidos ( 
    id SERIAL PRIMARY KEY,
    restaurant VARCHAR NOT NULL,
    customer VARCHAR NOT NULL,
    order_value DOUBLE PRECISION,
    payment_method VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    order_date VARCHAR NOT NULL
);
