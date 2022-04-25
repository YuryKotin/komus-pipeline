CREATE TABLE categories (
    category    VARCHAR(100) UNIQUE NOT NULL,
    category_id INT          PRIMARY KEY
);

CREATE TABLE subcategories (
    subcategory    VARCHAR(256) NOT NULL,
    subcategory_id INT          PRIMARY KEY,
    category_id    INT          NOT NULL,
    cat__subcat    TEXT         NOT NULL UNIQUE,
    CONSTRAINT cat_id FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE dates (
	date_id INT  PRIMARY KEY,
	"date"  DATE NOT NULL,
    day     INT  NOT NULL,
    month   INT  NOT NULL,
    year    INT  NOT NULL
);

CREATE TABLE products (
	article           INT PRIMARY KEY,
	first_subcategory INT NOT NULL,
    first_seen        INT NOT NULL,
    last_seen         INT NOT NULL,
    CONSTRAINT frst_subcat FOREIGN KEY (first_subcategory) REFERENCES subcategories(subcategory_id),
    CONSTRAINT frst_sn     FOREIGN KEY (first_seen)        REFERENCES dates(date_id),
    CONSTRAINT lst_sn      FOREIGN KEY (last_seen)         REFERENCES dates(date_id)
);

CREATE TABLE prices (
	date_id        INT     NOT NULL,
	article        INT     NOT NULL,
	price          NUMERIC NOT NULL,
	discount       NUMERIC,
    subcategory_id INT     NOT NULL,
    CONSTRAINT art    FOREIGN KEY (article)        REFERENCES products(article),
    CONSTRAINT dt     FOREIGN KEY (date_id)        REFERENCES dates(date_id),
    CONSTRAINT subcat FOREIGN KEY (subcategory_id) REFERENCES subcategories(subcategory_id)
);

CREATE TABLE descriptions (
	article     INT  NOT NULL UNIQUE,
	title       TEXT NOT NULL,
	description TEXT,
	url         TEXT NOT NULL,
    CONSTRAINT art FOREIGN KEY (article) REFERENCES products(article)
);
