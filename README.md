# Integrated Business Management System — INFOSOLUTIONS ANGOLA

A **Python** console application for managing the customers, employees, products and sales of a fictional IT equipment company, **INFOSOLUTIONS ANGOLA, LDA.**. It was built as an entry for the *Final Challenge – Internal Programming Contest 2025/2026*.

The project follows the **MVC (Model – View – Controller)** pattern and stores its data in an **SQLite** database, using only the Python standard library.

---

## Features

| Module | What it does |
|--------|--------------|
| **Customers** | Add, list, search (by name or tax ID), update and delete |
| **Employees** | Add, list, delete, calculate the total payroll and find the highest-paid employee |
| **Products** | Add, list, update stock and delete |
| **Sales** | Register sales with a stock check, automatic total calculation and automatic stock deduction |
| **Reports** | Customers, completed sales, best-selling product, top-spending customer, total sales, highest salary and total payroll |

### Business rules and validation

- **Customers:** name is required; email is validated with a regular expression; Angolan phone numbers are validated (mobile `9XXXXXXXX` or landline `22XXXXXXX`, with the `+244` / `00244` prefix accepted and stripped); the NIF (tax ID) is validated and **unique**.
- **Employees:** base salary and bonus cannot be negative; total salary = `salario_base + bonus`.
- **Products:** price and stock cannot be negative.
- **Sales:** a sale is only registered if there is enough stock (otherwise a `StockInsuficienteError` is raised); the total is `quantity × price`, and the stock is updated in the same operation.
- **Referential integrity:** foreign keys are enforced (`PRAGMA foreign_keys = on`). Customers and products that already have sales cannot be deleted.
- **Robustness:** input errors (`ValueError`), database errors (`sqlite3.Error`, `IntegrityError`) and invalid menu options are all handled. The main menu loop also has a safety net, so the program never crashes abruptly.

---