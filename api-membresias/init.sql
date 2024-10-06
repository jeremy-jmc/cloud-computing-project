CREATE TABLE IF NOT EXISTS membresia_cliente (
    cliente_id SERIAL PRIMARY KEY,
    dni VARCHAR(20),
    promo_id INTEGER,
    fecha_inicio DATE,
    fecha_fin DATE,
    estado VARCHAR(20)
);
-- DELETE FROM membresia_cliente;
INSERT INTO membresia_cliente (dni, promo_id, fecha_inicio, fecha_fin, estado)
VALUES ('77777777', 1, '2024-07-01', '2024-11-30', 'ACTIVO');

CREATE TABLE IF NOT EXISTS membresia_historial (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50),
    fecha_inicio DATE,
    fecha_fin DATE,
    estado VARCHAR(20),
    cliente_id INTEGER REFERENCES membresia_cliente(cliente_id),
    promo_id INTEGER
);

CREATE TABLE IF NOT EXISTS membresia_pagos (
    pago_id SERIAL PRIMARY KEY,
    promo_id INTEGER,
    cliente_id INTEGER REFERENCES membresia_cliente(cliente_id),
    fecha_pago DATE,
    monto DECIMAL(10,2),
    metodo_pago VARCHAR(20)
);