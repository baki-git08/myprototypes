# Grocery List App (v1.1.0)
This is the first official launch of the simple prototype Grocery List app (v1.0.0) built in python and FastAPI. 
It allows users to input a grocery item, together with their price and mark it as bought. 

## Features
- List all grocery items stored in the database
- Add a new grocery item to the database

## Description
This simple app is built using FastAPI and it uses a MySQL database. 
The is not frontend built yet into this project. It is intended to allow beginners to learn how to build API 
endpoints that can connect to a database. 
In this version of the app, the only endpoint that is available is:
- GET /itemList (returns a list of all items stored in the database)
- POST /putitems (adds a new item to the database)

## Getting Started
### Prerequisites
- Python 3.x installed
- pip installed
- MySQL database running locally on port 3306
- Virtual environment (recommended)
- `.env` file in the root directory with the following:
DB_URL="mysql+pymysql://<username>:<password>@localhost:3306/<database_name>"

### Installation
Ensure that your virtual environment is activated. 
Run the *requirements.txt* file to install all dependencies:
> pip install -r requirements.txt

### Usage
Start FastAPI development server:

Run the app using:
> uvicorn main:app --reload

### Project Structure
- backend/
    - connect.py
    - database.py
    - main.py
    - routes.py
    - run.py
    - servicese.py
- requirements.txt
- README.md
- .gitignore

### Architecture 
This sections explains the architecture of the project.
- connect.py - contains the database connection logic.
- database.py - contains the SQLModel classes that define the database schema.
- main.py - initializes the FastAPI app
- routes.py – contains the API endpoints, calls the business logic from the service layer
- service.py – contains the business logic
- run.py - starts the FastAPI development server

## 🔧 Troubleshooting the App
If you encounter issues while running the application, check the following key components:

### Database Connection (connect.py)
Depends on the DB_URL variable in the .env file.
Validates the database URL before attempting a connection.
Creates a session engine and establishes a connection to the database
Tip: Ensure your .env file has a correct DB_URL and the database server is running. 

### Database Schema (database.py)
Contains SQLModel classes that define your database schema.
Acts as the blueprint for creating tables and managing data structure. 

### Application (main.py)
Initializes the FastAPI app.
Registers all routes and API endpoints.
Connects the router and service layers for proper request handling.

### ⚠️ Additional Tips
Verify that environment variables are loaded correctly.
Apply database migrations before running the app if necessary.
Check logs for connection errors or dependency issue


