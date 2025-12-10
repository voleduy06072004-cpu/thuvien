-- Optional: run this if you need to create tables. Skip if tables already exist.
CREATE DATABASE IF NOT EXISTS libraryx;
USE libraryx;
CREATE TABLE IF NOT EXISTS accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin','user') DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    full_name VARCHAR(100) NOT NULL,
    age INT,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    gender ENUM('Nam','Nu','Khac'),
    address VARCHAR(255),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    book_code VARCHAR(20) UNIQUE NOT NULL,
    book_name VARCHAR(150) NOT NULL,
    book_type ENUM('Sách giáo khoa','Sách tham khảo') NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    publisher VARCHAR(100),
    import_date DATE,
    condition_status ENUM('Mới','Cũ'),
    tax DECIMAL(10,2) DEFAULT 0,
    image VARCHAR(255),
    description TEXT
);
CREATE TABLE IF NOT EXISTS invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    invoice_code VARCHAR(20) UNIQUE NOT NULL,
    invoice_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(12,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS invoice_details (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT,
    book_id INT,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS borrow_books (
    borrow_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    book_id INT,
    quantity INT NOT NULL,
    borrow_date DATE,
    return_date DATE,
    fee DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE SET NULL
);
