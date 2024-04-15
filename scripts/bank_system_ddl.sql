-- schema
CREATE SCHEMA IF NOT EXISTS BankSystem;

-- tables
-- Table: Account
CREATE TABLE IF NOT EXISTS BankSystem.Account (
    account_id SERIAL PRIMARY KEY,
    account_type varchar(100)  NOT NULL,
    customer_id int  NOT NULL,
    branch_id int  NOT NULL,
    balance int  NOT NULL,
    valid_from_dt date  NOT NULL,
    valid_to_dt date  NOT NULL
);

-- Table: Address
CREATE TABLE IF NOT EXISTS BankSystem.Address (
    address_id SERIAL PRIMARY KEY,
    city_nm varchar(100)  NOT NULL,
    street_nm varchar(100)  NOT NULL,
    house_no int  NOT NULL
);

-- Table: Branch
CREATE TABLE IF NOT EXISTS BankSystem.Branch (
    branch_id SERIAL PRIMARY KEY,
    branch_nm varchar(100)  NOT NULL,
    address_id int  NOT NULL,
    phone_no varchar(50)  NOT NULL
);

-- Table: Customer
CREATE TABLE IF NOT EXISTS BankSystem.Customer (
    customer_id int  PRIMARY KEY,
    customer_type varchar(100)  NOT NULL
);

-- Table: Employee
CREATE TABLE IF NOT EXISTS BankSystem.Employee (
    employee_id int  PRIMARY KEY,
    branch_id int  NOT NULL,
    position_id int  NOT NULL,
    valid_from_dt date  NOT NULL,
    valid_to_dt date  NOT NULL
);

-- Table: Person
CREATE TABLE IF NOT EXISTS BankSystem.Person (
    person_id SERIAL PRIMARY KEY,
    first_nm varchar(100)  NOT NULL,
    last_nm varchar(100)  NOT NULL,
    birth_dt date  NOT NULL,
    email varchar(100)  NOT NULL,
    address_id int  NOT NULL,
    phone_no varchar(50)  NOT NULL
);

-- Table: Position
CREATE TABLE IF NOT EXISTS BankSystem.Position (
    position_id SERIAL PRIMARY KEY,
    position_nm varchar(100)  NOT NULL,
    salary int  NOT NULL,
    valid_from_dt date  NOT NULL,
    valid_to_dt date  NOT NULL
);

-- Table: Transaction
CREATE TABLE IF NOT EXISTS BankSystem.Transaction (
    transaction_id SERIAL PRIMARY KEY,
    account_id int  NOT NULL,
    employee_id int  NOT NULL,
    amount int  NOT NULL,
    transaction_dttm timestamp  NOT NULL
);

-- foreign keys
-- Reference: Customer_Person (table: Customer)
ALTER TABLE BankSystem.Customer ADD CONSTRAINT Customer_Person
    FOREIGN KEY (customer_id)
    REFERENCES BankSystem.Person (person_id)  
;

-- Reference: Employee_Branch (table: Employee)
ALTER TABLE BankSystem.Employee ADD CONSTRAINT Employee_Branch
    FOREIGN KEY (branch_id)
    REFERENCES BankSystem.Branch (branch_id)  
;

-- Reference: Employee_Person (table: Employee)
ALTER TABLE BankSystem.Employee ADD CONSTRAINT Employee_Person
    FOREIGN KEY (employee_id)
    REFERENCES BankSystem.Person (person_id)  
;

-- Reference: Employee_Transaction (table: Transaction)
ALTER TABLE BankSystem.Transaction ADD CONSTRAINT Employee_Transaction
    FOREIGN KEY (employee_id)
    REFERENCES BankSystem.Employee (employee_id)  
;

-- Reference: Account_Branch (table: Account)
ALTER TABLE BankSystem.Account ADD CONSTRAINT Account_Branch
    FOREIGN KEY (branch_id)
    REFERENCES BankSystem.Branch (branch_id)  
;

-- Reference: Account_Customer (table: Account)
ALTER TABLE BankSystem.Account ADD CONSTRAINT Account_Customer
    FOREIGN KEY (customer_id)
    REFERENCES BankSystem.Customer (customer_id)  
;

-- Reference: Address_Branch (table: Branch)
ALTER TABLE BankSystem.Branch ADD CONSTRAINT Address_Branch
    FOREIGN KEY (address_id)
    REFERENCES BankSystem.Address (address_id)  
;

-- Reference: Person_Address (table: Person)
ALTER TABLE BankSystem.Person ADD CONSTRAINT Person_Address
    FOREIGN KEY (address_id)
    REFERENCES BankSystem.Address (address_id)  
;

-- Reference: Position_Employee (table: Employee)
ALTER TABLE BankSystem.Employee ADD CONSTRAINT Position_Employee
    FOREIGN KEY (position_id)
    REFERENCES BankSystem.Position (position_id)  
;

-- Reference: Transaction_Account (table: Transaction)
ALTER TABLE BankSystem.Transaction ADD CONSTRAINT Transaction_Account
    FOREIGN KEY (account_id)
    REFERENCES BankSystem.Account (account_id)  
;