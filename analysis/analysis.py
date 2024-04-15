import psycopg2 as pg
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style='whitegrid', font_scale=1.3, palette='Set2')

def get_dataset(table_name : str, columns : list[str]) -> pd.DataFrame :
    df = pd.DataFrame(columns=columns)
    cursor.execute(f"SELECT {', '.join(columns)} FROM BankSystem.{table_name}")
    rows = cursor.fetchall()
    for row in rows:
        df = pd.concat(
            [df, pd.DataFrame.from_dict(dict(zip(columns, list(map(lambda x: [x], row)))))],
            ignore_index=True
        )
    return df

if __name__ == '__main__':
    conn = pg.connect(
        host="localhost",
        database="project",
        user="postgres",
        password="12345"
    )

    cursor = conn.cursor()
    transaction = get_dataset("transaction", 
                              ["transaction_id", "account_id", "employee_id", "amount", "transaction_dttm"])
    person = get_dataset("person", ["person_id", "first_nm", "last_nm", "birth_dt", "email", "address_id", "phone_no"])
    customer = get_dataset("customer", ["customer_id", "customer_type"])
    account = get_dataset("account",
                           ["account_id", "account_type", "customer_id", "branch_id", "balance", "valid_from_dt", "valid_to_dt"])
    position = get_dataset("position", ["position_id", "position_nm", "salary", "valid_from_dt", "valid_to_dt"])
    employee = get_dataset("employee", ["employee_id", "branch_id", "position_id", "valid_from_dt", "valid_to_dt"])
    branch = get_dataset("branch", ["branch_id", "branch_nm", "address_id", "phone_no"])

    # Найдём распределение транзакций по годам
    plt.figure(figsize=(8, 6))
    transaction["year"] = transaction["transaction_dttm"].dt.year
    sns.histplot(transaction["year"])
    plt.title("Распределение транзакций по годам")

    # Средний оборот транзакций в каждом году
    transaction["turnover"] = abs(transaction["amount"])
    plt.plot(transaction.groupby("year")["turnover"].mean())
    plt.ylabel("mean turnover")
    plt.title("Средняя сумма транзакции в каждом году")

    # Упорядочить клиентов банка по суммарному обороту
    person_transaction = transaction.merge(account, on="account_id", how="inner")
    person_transaction = person_transaction.merge(customer, on="customer_id", how="inner")
    person_transaction = person_transaction.merge(person, left_on="customer_id", right_on="person_id", how="inner")
    person_transaction["name"] = person_transaction["first_nm"] + " " + person_transaction["last_nm"]
    person_turnover = person_transaction.groupby(["name"])["turnover"].sum()
    person_turnover = person_turnover.sort_values(ascending=False)

    plt.figure(figsize=(18, 8))
    plt.barh(person_turnover.index, person_turnover, color='skyblue')
    plt.xlabel('turnover')
    plt.ylabel('name')
    plt.title('customer`s overall turnover')
    plt.gca().invert_yaxis()

    # Построим heat-map позиция-отдел по зарплате

    position_branch = position.merge(employee, on="position_id", how="inner")
    position_branch = position_branch.merge(branch, on="branch_id", how="inner")
    position_branch["salary"] = position_branch["salary"].astype("int64")
    sns.heatmap(position_branch.pivot_table(index="position_nm", columns="branch_nm", values="salary"),
                 vmin=80000, vmax=300000)
    plt.xlabel("branch name")
    plt.ylabel("position name")
    plt.title("salary")

    # Найдём распределение счетов, обслуживающихся в отеделниях банка
    plt.figure(figsize=(12, 8))
    account_branch = account.merge(branch, on="branch_id", how="inner")
    sns.histplot(account_branch["branch_nm"])
    plt.title("Распределение счетов по банкам")
    plt.xlabel("branch name")

    plt.show()



    


    
