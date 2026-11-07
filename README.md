# Integrated Business Management System — INFOSOLUTIONS ANGOLA

A **Python** console application for managing the customers, employees, products and sales of a fictional IT equipment company, **INFOSOLUTIONS ANGOLA, LDA.**. It was built as an entry for the *Final Challenge – Internal Programming Contest 2025/2026*.

The project follows the **MVC (Model – View – Controller)** pattern and stores its data in an **SQLite** database, using only the Python standard library.

---

## Features

| Module | What it does |
|--------|--------------|
| **Customers** | Add, list, search (by name or tax ID), update and delete |
| **Employees** | Add, list, delete, calculate the total payroll and find the highest-paid employee(s) |
| **Products** | Add, list, update stock and delete |
| **Sales** | Register sales with a stock check, automatic total calculation and automatic stock deduction |
| **Reports** | Customers, completed sales, best-selling product, top-spending customer, total sales, highest salary and total payroll |

### Business rules and validation

- **Customers:** name is required; email is validated with a regular expression; Angolan phone numbers are validated (mobile `9XXXXXXXX` or landline `22XXXXXXX`, with the `+244` / `00244` prefix accepted and stripped); the tax ID (NIF) is validated and **unique**.
- **Employees:** name and position are required; base salary and bonus cannot be negative; total salary = `base_salary + bonus`. If several employees tie for the highest total salary, all of them are shown.
- **Products:** name is required; price and stock cannot be negative.
- **Sales:** a sale is only registered if there is enough stock (otherwise an `InsufficientStockError` is raised); the total is `quantity × price`, and the stock is updated in the same operation.
- **Referential integrity:** foreign keys are enforced (`PRAGMA foreign_keys = ON`). Customers and products that already have sales cannot be deleted.
- **Robustness:** input errors (`ValueError`), database errors (`sqlite3.Error`, `IntegrityError`) and invalid menu options are all handled. The main menu loop also has a safety net, so the program never crashes abruptly.

---

## Project structure

```
infosolutions-system/
├── index.py                       # Entry point
├── model/                         # Data layer and business rules
│   ├── database_model.py          #   SQLite connection and table creation
│   ├── customer_model.py          #   CustomerModel
│   ├── employee_model.py          #   EmployeeModel
│   ├── product_model.py           #   ProductModel
│   └── sale_model.py              #   SaleModel, InsufficientStockError
├── view/                          # Presentation layer (menus, input/print)
│   ├── menu_view.py               #   MenuView
│   ├── customer_view.py           #   CustomerView
│   ├── employee_view.py           #   EmployeeView
│   ├── product_view.py            #   ProductView
│   ├── sale_view.py               #   SaleView
│   └── report_view.py             #   ReportView
├── controller/                    # Control layer (connects View and Model)
│   ├── app_controller.py          #   Main menu
│   ├── customer_controller.py
│   ├── employee_controller.py
│   ├── product_controller.py
│   ├── sale_controller.py
│   └── report_controller.py
└── database/                      # Created automatically; holds the .db file
```

> All file, class, method and database names are in English. Each model class has a unique name (`CustomerModel`, `EmployeeModel`, `ProductModel`, `SaleModel`) so it can never be confused with its view or controller.

### How the layers interact

```
 User ⇄ View ⇄ Controller ⇄ Model ⇄ SQLite
```

- **View** only displays menus and reads keyboard input; it knows nothing about the database. Numeric prompts such as IDs and stock quantities re-ask on invalid input instead of crashing.
- **Controller** takes the data from the View, calls the Model, handles exceptions and sends messages back to the View.
- **Model** validates data, runs the SQL and implements the business rules.

---

## Database

The file `database/infosolutions.db` is **created automatically** the first time the program runs.

| Table | Columns |
|-------|---------|
| `customers` | `id`, `name`, `phone`, `email`, `tax_id` (unique) |
| `employees` | `id`, `name`, `position`, `base_salary`, `bonus` |
| `products` | `id`, `name`, `price`, `quantity` |
| `sales` | `id`, `customer_id` → `customers`, `product_id` → `products`, `quantity`, `total`, `sale_date` |

Relationships: **1 customer → N sales** and **1 product → N sales**.

> **Upgrading from an older version:** earlier versions used Portuguese table and column names (`clientes`, `nome`, ...). `CREATE TABLE IF NOT EXISTS` does not rename existing tables, so delete the old `database/infosolutions.db` file once and let the program recreate it.

---

## Getting started

**Requirements:** Python 3.8 or higher. No external dependencies.

```bash
git clone https://github.com/franciscoyg3/infosolutions-system.git
cd infosolutions-system
python index.py        # on Linux/macOS: python3 index.py
```

### Suggested first run

1. **Product Management** → add a few products with price and stock.
2. **Customer Management** → register at least one customer.
3. **Sales** → enter the customer ID, product ID and quantity.
4. **Reports** → check the totals and rankings.

### Main menu

The interface is in English:

```
---------------MAIN MENU---------------
0 - Exit System
1 - Customer Management
2 - Employee Management
3 - Product Management
4 - Sales Registration
5 - Reports
```

---

## Git workflow

Development uses a simple branch flow: short-lived work branches (`feature`, `bugfix`, `refactor`) are merged into `main`, and `dev` is kept in sync with `main`.

---

## Status against the brief

**Mandatory requirements:** OOP with `CustomerModel`, `ProductModel`, `EmployeeModel` and `SaleModel` classes; SQLite with full CRUD; exception handling; clear Model/View/Controller separation; main and reports menus. ✅

**Bonus items:**

- [x] Email validation
- [x] 1 customer → many sales relationship
- [ ] Authentication (administrator login)
- [ ] Sortable reports
- [ ] More polished interface

---

## Possible improvements

- Administrator login with hashed passwords.
- Editing employee records; sales with multiple line items per invoice.
- Sortable reports and CSV export.
- Automated tests (`unittest` / `pytest`).
- Add the same re-prompt behaviour to the remaining `int()` / `float()` inputs (employee salary and bonus, product price and quantity, sale data), so a typo does not return the user to the menu.

---

## Project Author

**Claudio Francisco** — academic / contest project, Luanda, Angola.