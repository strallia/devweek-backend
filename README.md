# DevWeek Backend

## Prerequisites

Make sure you have the following installed:

- Python (3.9.6 or later)
- pip (Python package manager)

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

1. Create .env file in root directory:

    Replace variables with < > with your info

    ```
    FLASK_APP=app.py
    FlASK_ENV=development
    SECRET_KEY=your_secret_key_here
    SQLALCHEMY_DATABASE_URI=postgresql://<USERNAME>:<PASSWORD>@localhost:5432/<DB_NAME>
    ```

1. Run the Flask application:

    ```bash
    python app.py
    ```

    Access the app at http://127.0.0.1:5000

