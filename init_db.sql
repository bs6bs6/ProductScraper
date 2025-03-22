CREATE TABLE IF NOT EXISTS product (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    rating DECIMAL(3, 2),
    url VARCHAR(255) NOT NULL,
    brand VARCHAR(255),
    img VARCHAR(255),
    scrape_timestamp DATETIME NOT NULL
);