-- Суммарный балланс всех валидных счетов, которыми владеют клиенты типа 'Business customer'

SELECT SUM(a.balance)
FROM BankSystem.account AS a
JOIN BankSystem.customer AS c ON c.customer_id = a.customer_id
WHERE c.customer_type = 'Business customer' AND NOW() BETWEEN a.valid_from_dt AND a.valid_to_dt;

-- Названия банков, в которых была позиция 'Credit Analyst'

SELECT b.branch_nm
FROM BankSystem.position AS p
JOIN BankSystem.employee AS e ON p.position_id = e.position_id
JOIN BankSystem.branch AS b ON e.branch_id = b.branch_id
WHERE p.position_nm = 'Credit Analyst';

-- Найти имя работника, который провёл больше всего транзакций в 2023 году

WITH
    employee_2023 AS (
        SELECT p.first_nm || ' ' || p.last_nm as name, COUNT(*) as frequency
        FROM BankSystem.person AS p
        JOIN BankSystem.employee AS e ON p.person_id = e.employee_id
        JOIN BankSystem.transaction AS t ON t.employee_id = e.employee_id
        WHERE EXTRACT(YEAR from t.transaction_dttm) = 2023 
        GROUP BY p.first_nm, p.last_nm
    )
    
SELECT name
FROM employee_2023
WHERE frequency = (SELECT MAX(frequency) FROM employee_2023);

-- Вывести список счетов, по которым есть хотя бы 3 транзакции

SELECT a.account_id
FROM BankSystem.account AS a
JOIN BankSystem.transaction AS t ON a.account_id = t.account_id
GROUP BY a.account_id
HAVING COUNT(t.transaction_id) > 2;

-- Найти самые востребованные позиции в банке и их зарплату (упорядочить по популярности и зарплате)

SELECT p.position_nm, COUNT(*) as frequency, p.salary
FROM BankSystem.position AS p
JOIN BankSystem.employee AS e ON p.position_id = e.position_id
JOIN BankSystem.branch AS b ON e.branch_id = b.branch_id
GROUP BY (p.position_nm, p.salary)
ORDER BY frequency DESC, salary DESC;

-- Построить таблицу где для каждого клиента будет счёт с самой поздней датой закрытия

WITH
    person_account AS (
        SELECT *
        FROM BankSystem.person AS p
        JOIN BankSystem.customer AS c on p.person_id = c.customer_id
        JOIN BankSystem.account AS a ON c.customer_id = a.customer_id
    )
SELECT first_nm || ' ' || last_nm as name, valid_from_dt, valid_to_dt
FROM person_account
WHERE (person_id, valid_to_dt) IN (SELECT person_id, MAX(valid_to_dt) FROM person_account
                                   GROUP BY person_id);

-- Отдел в котором работает более 1 сотрудника

SELECT b.branch_id, COUNT(e.employee_id) as employee_num
FROM BankSystem.branch AS b
JOIN BankSystem.employee AS e ON b.branch_id = e.branch_id
GROUP BY b.branch_id
HAVING COUNT(e.employee_id) > 1;

-- Упорядочить счета по их суммарному обороту за 2023 год

WITH
    account_turnover AS (
        SELECT a.account_id, SUM(ABS(t.amount)) as turnover
        FROM BankSystem.account AS a
        JOIN BankSystem.transaction AS t ON a.account_id = t.account_id
        WHERE EXTRACT(YEAR from t.transaction_dttm) = 2023 
        GROUP BY a.account_id
    )
SELECT *
FROM account_turnover
ORDER BY turnover DESC;

-- Упорядочить клиентов по частоте совершаемых ими транзаций

SELECT p.first_nm || ' ' || p.last_nm as name, COUNT(*) as frequency
FROM BankSystem.person AS p
JOIN BankSystem.customer AS c ON p.person_id = c.customer_id
JOIN BankSystem.account AS a ON c.customer_id = a.customer_id
JOIN BankSystem.transaction AS t on t.account_id = a.account_id
GROUP BY c.customer_id, p.first_nm, p.last_nm
ORDER BY frequency DESC;

-- Количество отделений адресс которых это дом с номером от 30 до 50

SELECT COUNT(*)
FROM BankSystem.branch AS b
JOIN BankSystem.address AS a ON b.address_id = a.address_id
WHERE house_no BETWEEN 30 AND 50;