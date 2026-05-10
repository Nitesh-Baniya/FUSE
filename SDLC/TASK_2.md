# Part 2: Building the Customer API Using FastAPI

## Objective

The objective of this task was to build a RESTful Customer API using FastAPI that connects to the PostgreSQL database created in Task 1. The API acts as a bridge between users and the database, allowing users to retrieve, create, update, and manage customer information safely and efficiently.

To maintain clean and scalable code organization, a Layered Architecture approach was followed. This architecture separates the application into multiple layers, where each layer is responsible for only one specific task.

The API was built using:

- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Pydantic
- Python Logging
- Dockerized PostgreSQL database

---

# Project Structure

The project was organized into multiple layers and folders to ensure modularity and maintainability.

```text
project/
│
├── app/
│   ├── database.py
│   ├── schemas.py
│   ├── crud.py
│   ├── router.py
│   ├── models.py
│   ├── logger.py
│   └── main.py
│
├── .env
├── requirements.txt
└── app.log
```

---

# Layered Architecture Overview

The application follows a 4-layer architecture:

| Layer | Responsibility |
|---|---|
| database.py | Handles database connection |
| schemas.py | Defines data validation models |
| crud.py | Handles database operations |
| router.py | Handles API requests and responses |

This separation improves:

- readability
- maintainability
- debugging
- scalability

---

# Step 1: Setting Up Dependencies

A virtual environment was created to isolate project dependencies.

## Creating Virtual Environment

```bash
python -m venv venv
```

## Activating Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

# Installing Required Libraries

The following dependencies were installed:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

---

# Creating requirements.txt

Installed libraries were saved using:

```bash
pip freeze > requirements.txt
```

This ensures that the same library versions can be reused across different systems.

---

# Step 2: Creating Logger Configuration

A centralized logging configuration file named `logger.py` was created.

The logging system records:

- API requests
- database operations
- validation errors
- exceptions
- warnings

## Purpose of Logging

Logging helps:

- monitor application behavior
- debug errors
- track requests
- monitor database activity

---

## Example Logging Configuration

```python
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
```

---

# Step 3: Database Connection Layer (`database.py`)

The `database.py` file was responsible for creating the connection between FastAPI and PostgreSQL.

## Responsibilities

- Establish database connection
- Create SQLAlchemy engine
- Manage database sessions
- Load environment variables securely

---

# Loading Environment Variables

Database credentials were loaded from the `.env` file instead of being hardcoded.

Example `.env`:

```env
POSTGRES_USER=fuseadmin
POSTGRES_PASSWORD=fusepassword
POSTGRES_DB=fusedb
POSTGRES_PORT=5432
```

---

# Example Database Connection

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
```

---

# Logging in `database.py`

Logging was added to:

- track successful connections
- detect connection failures
- monitor session creation and closure

---

# Step 4: Defining Database Models (`models.py`)

SQLAlchemy ORM models were created to represent database tables as Python classes.

## Purpose of ORM

ORM (Object Relational Mapping) allows interaction with the database using Python objects instead of writing raw SQL queries.

Example:

- Database table → Python class
- Table row → Python object

---

# Example Customer Model

```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    customerNumber = Column(Integer, primary_key=True)
    customerName = Column(String)
    phone = Column(String)
    city = Column(String)
    country = Column(String)
```

---

# Step 5: Creating Validation Schemas (`schemas.py`)

Pydantic schemas were created to validate incoming and outgoing API data.

---

# Schema Types Implemented

| Schema | Purpose |
|---|---|
| CustomerCreate | Create new customer |
| CustomerOut | Return customer data |
| CustomerUpdate | Update existing customer |

---

# Example CustomerCreate Schema

```python
from pydantic import BaseModel
from typing import Optional

class CustomerCreate(BaseModel):
    customerName: str
    phone: str
    city: str
    country: str
```

---

# Example CustomerUpdate Schema

```python
class CustomerUpdate(BaseModel):
    customerName: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
```

---

# Purpose of Validation

Validation prevents invalid data from entering the database.

Examples:

- String instead of integer
- Invalid email format
- Missing required fields

---

# Logging Validation Errors

Validation errors were logged to help identify incorrect user inputs.

---

# Step 6: CRUD Operations Layer (`crud.py`)

The `crud.py` file contained all database operations.

CRUD stands for:

- Create
- Read
- Update
- Delete

This layer communicates only with the database.

---

# Example CRUD Functions

## Create Customer

```python
def create_customer(db, customer):
    pass
```

## Read Customer

```python
def get_customer(db, customer_id):
    pass
```

## Update Customer

```python
def update_customer(db, customer_id, customer):
    pass
```

## Delete Customer

```python
def delete_customer(db, customer_id):
    pass
```

---

# Pagination Support

Pagination was implemented using:

- `skip`
- `limit`

Example:

```http
GET /customers?skip=0&limit=10
```

This prevents loading thousands of records at once.

---

# Error Handling

If a customer ID does not exist:

- API returns `404 Not Found`
- Application does not crash

Example:

```python
raise HTTPException(status_code=404, detail="Customer not found")
```

---

# Related Data Handling

Customer-related data such as:

- orders
- payments

were included in API responses.

If no related records exist:

- empty list `[]` is returned

This ensures API stability.

---

# Logging in `crud.py`

Logging was used to track:

- database reads
- inserts
- updates
- deletes
- missing records

Example log messages:

- “Fetching customer ID 101”
- “Customer not found: ID 999”

---

# Step 7: Router Layer (`router.py`)

The router layer handled incoming HTTP requests.

Responsibilities:

- receive requests
- call CRUD functions
- return responses

---

# Example Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/customers` | GET | List customers |
| `/customers/{id}` | GET | Retrieve customer |
| `/customers` | POST | Create customer |
| `/customers/{id}` | PUT | Update customer |
| `/customers/{id}` | DELETE | Delete customer |

---

# Example Route

```python
@router.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    pass
```

---

# Logging in `router.py`

The router layer logged:

- incoming requests
- outgoing responses
- API errors
- endpoint activity

Example:

- “GET request received for customer ID 101”

---

# Step 8: Running the FastAPI Application

The API server was started using:

```bash
uvicorn app.main:app --reload
```

---

# Automatic API Documentation

FastAPI automatically generated Swagger documentation.

Accessible at:

```text
http://localhost:8000/docs
```

This interface allows testing API endpoints directly from the browser.

---

## Placeholder for Screenshot

```text
[Insert Screenshot: Swagger UI documentation page]
```

---

# Testing API Endpoints

The following API functionalities were tested:

- retrieving customers
- fetching individual customer data
- pagination
- creating customers
- updating customers
- deleting customers
- error handling

---

## Placeholder for Screenshot

```text
[Insert Screenshot: GET /customers response]
```

---

## Placeholder for Screenshot

```text
[Insert Screenshot: GET /customers/{id} response]
```

---

## Placeholder for Screenshot

```text
[Insert Screenshot: 404 Not Found response]
```

---

# Reflection

## Factor II: Dependencies

Dependencies were managed using:

- virtual environments
- requirements.txt

This guarantees consistent library versions across systems and prevents compatibility issues.

---

## Factor IV: Backing Services

SQLAlchemy ORM separated application logic from the database engine.

This means PostgreSQL could later be replaced with:

- MySQL
- SQLite
- MariaDB

without rewriting the core business logic.

---

## Factor III: Config Management

Sensitive configuration values were stored in `.env` files.

Benefits:

- improved security
- environment flexibility
- easier deployment

Different environments can use different credentials without changing the application code.

---

# Conclusion

In this task, a modular Customer API was successfully developed using FastAPI and PostgreSQL. The project implemented layered architecture principles to separate responsibilities across multiple modules, improving maintainability and scalability.

The API supports:

- CRUD operations
- pagination
- validation
- error handling
- logging
- related data retrieval

Additionally, centralized logging and environment-based configuration improved monitoring, debugging, and security practices.