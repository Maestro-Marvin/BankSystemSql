from datetime import date
from faker import Faker
from faker.providers import date_time
import psycopg2
import random

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    database="project",
    user="postgres",
    password="12345"
)

cur = conn.cursor()

def generate_address_data():
    city_nm = fake.city()
    street_nm = fake.street_name()
    house_no = fake.random_int(min=1, max=200)
    return (city_nm, street_nm, house_no)

jobs = ["Financial Analyst", "Auditor", "Financial advisor", "Accountant", "Trader",
        "Credit Analyst", "Investment banking", "Bank Clerk", "Banking Associate", "Banker",
        "Asset Manager", "Loan Officer", "Branch Manager", "Investment", "Broker"]

def generate_position_data(I):
    position_nm = jobs[I - 1]
    salary = fake.random_int(min=80000, max=300000)
    valid_from_dt = fake.date_between(start_date="-5y", end_date="today")
    valid_to_dt = fake.date_between(start_date=valid_from_dt, end_date="+5y")
    return (position_nm, salary, valid_from_dt, valid_to_dt)

def generate_person_data(I):
    first_nm = fake.first_name()
    last_nm = fake.last_name()
    birth_dt = fake.date_between(start_date=date(1940, 1, 1), end_date=date(2000, 12, 31))
    email = fake.email()
    address_id = I
    phone_no = fake.phone_number()
    return (first_nm, last_nm, birth_dt, email, address_id, phone_no)

customer_types = ["Individual customer", "Business customer", "Government", "Trust customer", "Investment Fund"]

def generate_customer_data(I):
    customer_id = I
    customer_type = random.choice(customer_types)
    return (customer_id, customer_type)

banks = ["Sberbank", "VTB Bank", "Gazprombank", "Alfa-Bank", "Tinkoff"]

def generate_branch_data():
    branch_nm = random.choice(banks)
    address_id = num_person + I
    phone_no = fake.phone_number()
    return (branch_nm, address_id, phone_no)

account_types = ["Investment Account", "Savings Account", "Current Account", "Time Deposit", "Credit Account",
                 "Business Account", "Retirement Account", "Trust Account"]

def generate_account_data():
    account_type = random.choice(account_types)
    customer_id = fake.random_int(min=1, max=num_customer)
    branch_id = fake.random_int(min=1, max=num_branch)
    balance = fake.random_int(min=-1000000, max=1000000)
    valid_from_dt = fake.date_between(start_date="-5y", end_date="-2y")
    valid_to_dt = fake.date_between(start_date="+2y", end_date="+5y")
    return (account_type, customer_id, branch_id, balance, valid_from_dt, valid_to_dt)

def generate_employee_data(I):
    employee_id = num_customer + I
    branch_id = fake.random_int(min=1, max=num_branch)
    position_id = fake.random_int(min=1, max=num_position)
    valid_from_dt = fake.date_between(start_date="-5y", end_date="today")
    valid_to_dt = fake.date_between(start_date=valid_from_dt, end_date="+5y")
    return (employee_id, branch_id, position_id, valid_from_dt, valid_to_dt)

def generate_transaction_data():
    account_id = fake.random_int(min=1, max=num_account)
    employee_id = fake.random_int(min=1, max=num_employee) + num_customer
    amount = fake.random_int(min=-100000, max=100000)
    transaction_dttm = fake.date_time_between(start_date="-3y", end_date="now")
    return (account_id, employee_id, amount, transaction_dttm)

num_address = 50
for I in range(1, num_address + 1):
    address_data = generate_address_data()
    cur.execute("""
        INSERT INTO BankSystem.Address (city_nm, street_nm, house_no)
        VALUES (%s, %s, %s)
        """, tuple(address_data))

num_position = len(jobs)
for I in range(1, num_position + 1):
    position_data = generate_position_data(I)
    cur.execute("""
        INSERT INTO BankSystem.Position (position_nm, salary, valid_from_dt, valid_to_dt)
        VALUES (%s, %s, %s, %s)
        """, tuple(position_data))

num_person = 30
for I in range(1, num_person + 1):
    person_data = generate_person_data(I)
    cur.execute("""
        INSERT INTO BankSystem.Person (first_nm, last_nm, birth_dt, email, address_id, phone_no)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, tuple(person_data))

num_customer = 20
for I in range(1, num_customer + 1):
    customer_data = generate_customer_data(I)
    cur.execute("""
        INSERT INTO BankSystem.Customer (customer_id, customer_type)
        VALUES (%s, %s)
        """, tuple(customer_data))
    
num_branch = 20
for I in range(1, num_branch + 1):
    branch_data = generate_branch_data()
    cur.execute("""
        INSERT INTO BankSystem.Branch (branch_nm, address_id, phone_no)
        VALUES (%s, %s, %s)
        """, tuple(branch_data))

num_account = 50
for I in range(1, num_account + 1):
    account_data = generate_account_data()
    cur.execute("""
        INSERT INTO BankSystem.Account (account_type, customer_id, branch_id, balance, valid_from_dt, valid_to_dt)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, tuple(account_data))

num_employee = 10
for I in range(1, num_employee + 1):
    employee_data = generate_employee_data(I)
    cur.execute("""
        INSERT INTO BankSystem.Employee (employee_id, branch_id, position_id, valid_from_dt, valid_to_dt)
        VALUES (%s, %s, %s, %s, %s)
        """, tuple(employee_data))
    
num_transaction = 50
for I in range(1, num_transaction + 1):
    transaction_data = generate_transaction_data()
    cur.execute("""
        INSERT INTO BankSystem.Transaction (account_id, employee_id, amount, transaction_dttm)
        VALUES (%s, %s, %s, %s)
        """, tuple(transaction_data))


conn.commit()
cur.close()
conn.close()