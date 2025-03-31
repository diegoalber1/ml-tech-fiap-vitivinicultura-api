CREATE DATABASE vitivinicultura_db;



CREATE TABLE producao (
    id SERIAL PRIMARY KEY, -- Identificador único para cada registro
    ano INT NOT NULL,
    produto VARCHAR(255) NOT NULL, -- Nome do produto
    quantidade_litros BIGINT, -- Quantidade em litros (NULL para valores "-")
    data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Data de inserção do registro
);

CREATE TABLE comercializacao (
    id SERIAL PRIMARY KEY, -- Identificador único para cada registro
    ano INT NOT NULL,
    produto VARCHAR(255) NOT NULL, -- Nome do produto
    quantidade_litros BIGINT, -- Quantidade em litros (NULL para valores "-")
    data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Data de inserção do registro
);

CREATE TABLE exportacao (
    id SERIAL PRIMARY KEY, -- Identificador único para cada registro
    ano INT NOT NULL,
    pais VARCHAR(255) NOT NULL, -- Nome do país
    quantidade_litros BIGINT, -- Quantidade em quilogramas (NULL para valores "-")
    valor_usd DECIMAL(15, 2), -- Valor em dólares (NULL para valores "-")
    data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Data de inserção do registro
);

CREATE TABLE importacao (
    id SERIAL PRIMARY KEY, -- Identificador único para cada registro
    pais VARCHAR(255) NOT NULL, -- Nome do país
    quantidade_litros BIGINT, -- Quantidade em quilogramas (NULL para valores "-")
    valor_usd DECIMAL(15, 2), -- Valor em dólares (NULL para valores "-")
    data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Data de inserção do registro
);