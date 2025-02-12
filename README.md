# DevWeek Backend

## Prerequisites

Make sure you have the following installed:

- Python (3.9.6 or later)
- pip (Python package manager)
- psql CLI

## Getting Started

1. Clone the repository:

    ```bash
    git clone git@github.com:strallia/devweek-backend.git
    cd devweek-backend
    ```

1. (Optional) Create and activate a virtual environment:

    Mac/Linux:

    ```bash 
    python -m venv venv
    source venv/bin/activate
    ```

    Windows (Command Prompt):

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Setting Up and Seeding the Database

1. Activate psql CLI
1. Create a new database
    ```bash
    CREATE DATABASE devweek;
    ```
1. Create .env file in root directory with flask variables and database URI

    Replace variables with < > with your info.

    ```
    FLASK_APP=app.py
    FlASK_ENV=development
    SECRET_KEY=your_secret_key_here
    SQLALCHEMY_DATABASE_URI=postgresql://<USERNAME>:<PASSWORD>@localhost:5432/devweek
    ```
1. In separate terminal, run these commands one by one to create the tables and seed the database
    ```bash
    python create_db_tables.py
    python seed_db.py
    ```

1. Run the Flask application:

    ```bash
    python app.py
    ```

    Access the app at http://127.0.0.1:5000

