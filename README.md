# 📦 Store Management App

**Course Project: Database Systems**  
**Title:** Development of a Store Management Automation Prototype  
**University:** Peter the Great St. Petersburg Polytechnic University  
**Student:** V.I. Gamin  
**Supervisor:** N.O. Stepina  
**Date:** December 2024

---

## 📌 Project Description

This is a store management automation application for tracking products, expenses, sales, and profit. The user interface is developed using Python's `tkinter`. PostgreSQL is used as the database management system. The system includes role-based access control (admin/user), reporting, triggers, and stored procedures.

---

## 🔧 Technologies Used

- Python 
- PostgreSQL
- Tkinter (GUI)
- psycopg2 (PostgreSQL adapter)
- JSON (configuration)
- SQL (triggers, procedures)

---

## 💡 Main Features

- 🔐 User authentication with role-based access
- 📦 Product management
- 💸 Expense tracking
- 🧾 Sales and expense logging
- 📊 Report generation:
  - Monthly profit report
  - Top 5 most profitable products
- 🔁 Triggers and stored procedures for data integrity

---

## 🧪 User Roles

| Role    | Access Level                                           |
|---------|--------------------------------------------------------|
| `admin` | Full access: add, edit, delete                         |
| `user`  | View-only access                                       |

---

## 🗃 Database Structure

![Image](https://github.com/user-attachments/assets/4bfced4b-578b-4904-97ce-934b0672fbbf)

---

## ▶️ How to Run

1. Install dependencies:
   ```bash
   pip install psycopg2
   ```

2. Configure your `db_config.json`:
   ```json
   {
     "host": "localhost",
     "port": 5432,
     "database": "store_db",
     "user": "postgres",
     "password": "1234"
   }
   ```

3. Create your PostgreSQL database and execute the schema with triggers and stored procedures.

4. Run the app from the project root:
   ```bash
   python -m main
   ```

---

## 📄 Full Documentation

For detailed documentation and analysis of the project, see the [Course Report (PDF)](cource_BD.pdf)

---

## 🖼 Interface Preview

Below is a visual walkthrough of the application's main interface and functionality.

### 🔐 Login Window (Admin/User Access)

![image](https://github.com/user-attachments/assets/26932822-9f9f-4a7e-a88e-0c16bc932322)

- Users enter their credentials to log in.
- Role-based access is applied: `admin` has full access, `user` has read-only rights.

---




---

### 🧭 Main Menu Navigation

![image](https://github.com/user-attachments/assets/44f69a22-6d96-4195-b62d-1606481cf176)

- Menu provides access to:
  - Products
  - Expense Categories
  - Logs
  - Reports

---


### ✅ Added Product Example

![image](https://github.com/user-attachments/assets/ce4fcc55-2cde-464c-b280-8e4d13e6e7d1)

- New product (`test`) added successfully.

---

### ✅ Added Expense Example

![image](https://github.com/user-attachments/assets/a117250b-2d3e-4037-9069-47fbb8958fb4)

- New category `Test` has been added.

---
## 📊 Functional Previews (Expenses, Reports)

Below is a continuation of the interface overview, focused on logging expenses and generating reports.

---

### 📘 Expense Log Journal

![image](https://github.com/user-attachments/assets/235f7fee-de84-4eb9-b263-22b66b0c4928)

- Shows a list of expenses with amounts, categories, and dates.
- Admin can add or edit expense entries.

---

### ✏️ Sales Editing Form

![image](https://github.com/user-attachments/assets/8ade4c54-730c-40ef-9434-46fed3767602)

- Allows editing sales transactions including product ID, quantity, price, and date.

---

### 💰 Monthly Profit Report

![image](https://github.com/user-attachments/assets/d8f42e76-e3ee-4be8-b17f-507bb3fcbcd5)

- Displays the total profit for a selected month.
- Automatically calculates based on recorded sales and expenses.

---

### 🏆 Top 5 Most Profitable Products

![image](https://github.com/user-attachments/assets/1c6c6f51-4fc2-4d68-9a73-1696f5317a50)

- Generates a list of the 5 most profitable products within a given date range.
- Output is shown in a text format.

---



