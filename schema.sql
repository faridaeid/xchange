CREATE TABLE IF NOT EXISTS user (
  user_id       INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  first_name    VARCHAR(30)        NULL,
  last_name     VARCHAR(30)        NULL,
  username      VARCHAR(100)        NOT NULL UNIQUE,
  password      VARCHAR(100)        NOT NULL,
  email_address VARCHAR(254)       NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS store (
  store_id    INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  store_name  VARCHAR(40)        NOT NULL,
  create_date DATE               NOT NULL,
  owner_id    INT                NOT NULL,
  FOREIGN KEY (owner_id) REFERENCES user (user_id)
);


CREATE TABLE IF NOT EXISTS category (
  cat_id    INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  cat_name  VARCHAR(30)        NOT NULL,
  cat_descr VARCHAR(100)       NOT NULL
);

CREATE TABLE IF NOT EXISTS store_categories (
  category_id INT NOT NULL,
  store_id    INT NOT NULL,
  PRIMARY KEY (category_id, store_id),
  FOREIGN KEY (category_id) REFERENCES category (cat_id),
  FOREIGN KEY (store_id) REFERENCES store (store_id)
);

CREATE TABLE IF NOT EXISTS product (
  product_id      INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  product_name    VARCHAR(30)        NOT NULL,
  product_specs   VARCHAR(200)       NOT NULL,
  product_price   NUMERIC(20, 3)     NOT NULL,
  number_in_stock INT UNSIGNED       NOT NULL,
  category_id     INT                NOT NULL,
  FOREIGN KEY (category_id) REFERENCES category (cat_id)
);


CREATE TABLE IF NOT EXISTS cart (
  cart_id  INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  owner_id INT                NOT NULL,
  FOREIGN KEY (owner_id) REFERENCES user (user_id)
);

CREATE TABLE IF NOT EXISTS cart_products (
  cart_id    INT              NOT NULL,
  product_id INT              NOT NULL,
  quantity   INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY (cart_id, product_id),
  FOREIGN KEY (cart_id) REFERENCES cart (cart_id),
  FOREIGN KEY (product_id) REFERENCES product (product_id)
);

CREATE TABLE transaction (
  buyer_id INT NOT NULL,
  seller_id    INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT UNSIGNED NOT NULL,
  transaction_date DATE NOT NULL,
  PRIMARY KEY (buyer_id, seller_id, product_id, transaction_date),
  FOREIGN KEY (buyer_id) REFERENCES user (user_id),
  FOREIGN KEY (seller_id) REFERENCES user (user_id),
  FOREIGN KEY (product_id) REFERENCES product(product_id)
);

ALTER TABLE cart_products ADD COLUMN is_checkedout BOOL NOT NULL DEFAULT false;

ALTER TABLE user MODIFY COLUMN password VARCHAR(100);
ALTER TABLE user MODIFY COLUMN username VARCHAR(100);