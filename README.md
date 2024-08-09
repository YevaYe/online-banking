# Online Banking Platform

This project is a Django-based online banking platform that allows users to manage their accounts, perform transactions, and monitor their balances.

## Features

- **User Management**: Users can register, log in, and manage their accounts.
- **Account Management**: Users can create, view, and delete their bank accounts.
- **Transactions**: Users can perform money transfers between accounts, with real-time balance updates.
- **Search & Filter**: Transactions can be filtered and searched by date.
- **Error Handling**: Validation and error messages are provided for various operations, ensuring smooth user experience.
- **Atomic Transactions**: The platform ensures that all financial transactions are atomic, meaning either the entire transaction is processed or none of it is, preventing partial updates.

## You can use admin user
* Usermane: admin.user
* Password: 1qazcde3

## Installation

### Prerequisites

- Python 3.8+
- Django 4.x
- Virtual Environment

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/online_banking.git
   cd online_banking
   ```
   
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```
   python manage.py migrate
   ```
   
5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```
   python manage.py runserver
   ```

7. **Access the application:**
Open your browser and navigate to http://127.0.0.1:8000/

# Implementations
## User Model
The User model extends Django's AbstractUser and includes additional fields such as birthday, country, and user_type. The user type can either be regular or entrepreneur, which affects the functionality available to the user, such as account categories.

# Account Management
### Account Model
* The account number is automatically generated and is unique.
* The balance starts at zero.
* For regular users, the account category is automatically set to "Transfer", while entrepreneurs can choose a category.

### Account Form
* The account number is generated and displayed but cannot be edited.
* Only entrepreneurs can select an account category; otherwise, it's automatically set.

### Account Creation & Deletion
* Users can create accounts via the AccountCreateView.
* Accounts can be deleted via the AccountDeleteView, with confirmation.

## Transactions
### Money Transfer
* Users can transfer money between accounts using the **MoneyTransferView**.
* Validation ensures that the recipient account exists and that the sender has sufficient funds.
* Transactions are atomic, ensuring that all operations complete successfully or none at all.

### Transaction Filtering
* Users can filter transactions by date.
* The transaction list view displays only the transactions related to the logged-in user's accounts.

## Templates
The project features custom templates for the following:

* **Base Template (base.html)**: Includes the general structure and styles for the entire project, with a modern, responsive design.
* Sidebar: Contains navigation links with icons for home, balance, transactions, and money transfer.
* Forms: Enhanced with crispy-forms to provide a clean, user-friendly UI.
* Account Management: Templates for account creation and deletion, including confirmation prompts.
* Transaction List: Displays all relevant transactions for the user, with filtering options.

## Styling
* Integrated FontAwesome for iconography.
* Responsive design inspired by the Soft UI Dashboard.
* Custom styles include gradient buttons, a modern sidebar, and a professional overall look.

Error Handling
* Form Validation: Forms are validated for correct input, ensuring that account numbers are valid and amounts are positive.
* Atomic Transactions: Ensures that all operations in a transaction either complete successfully or are entirely rolled back in case of an error.

### Thank you! 
