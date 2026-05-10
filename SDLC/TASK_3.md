# Task 3: Concurrent Dashboard API Using FastAPI and asyncio

# Objective

The objective of this task was to develop a high-performance API dashboard capable of retrieving record counts from multiple database tables simultaneously using concurrency.

Instead of querying each table sequentially, asynchronous programming techniques using `asyncio.gather()` were implemented to execute all database count queries concurrently. This significantly improves API response speed and demonstrates scalable backend system design.

The task also emphasized:

- modular API design
- concurrency
- asynchronous programming
- logging
- scalability principles from the Twelve-Factor App methodology

---

# Project Goal

The API was designed to:

- Create individual count endpoints for each database table
- Create one aggregated dashboard endpoint
- Execute database queries concurrently
- Track all operations using logging

---

# Database Tables Used

The following database tables were included in the implementation:

| Table Name | Endpoint |
|---|---|
| customers | `/customers/count` |
| orders | `/orders/count` |
| products | `/products/count` |
| employees | `/employees/count` |
| offices | `/offices/count` |
| payments | `/payments/count` |
| orderdetails | `/orderdetails/count` |
| productlines | `/productlines/count` |

---

# Project Structure

The project continued using modular layered architecture.

```text
project/
│
├── app/
│   ├── crud.py
│   ├── router.py
│   ├── database.py
│   ├── logger.py
│   ├── main.py
│   └── schemas.py
│
├── requirements.txt
└── app.log
```

---

# Part 1: Creating Individual Count Endpoints

# Objective

Separate endpoints were created for each database table to return the total number of records.

This follows the principle of modularity:

- each endpoint performs only one responsibility
- endpoints remain reusable and maintainable
- users can request only the required data

---

# Step 1: Implementing CRUD Count Functions

Inside `crud.py`, separate functions were created for each table.

## Example Customer Count Function

```python
def get_customers_count(db):
    return db.query(Customer).count()
```

## Example Orders Count Function

```python
def get_orders_count(db):
    return db.query(Order).count()
```

---

# Similar Functions Were Created For

- products
- employees
- offices
- payments
- orderdetails
- productlines

Each function was responsible only for interacting with the database.

---

# Logging in CRUD Layer

Logging was implemented to track:

- query execution start
- query completion
- database failures

Example:

```python
logger.info("Fetching customer count")
```

---

# Step 2: Creating Individual API Endpoints

Separate FastAPI routes were created for each table count.

## Example Customer Endpoint

```python
@router.get("/customers/count")
def customers_count(db: Session = Depends(get_db)):
    return {"customers": crud.get_customers_count(db)}
```

## Example Orders Endpoint

```python
@router.get("/orders/count")
def orders_count(db: Session = Depends(get_db)):
    return {"orders": crud.get_orders_count(db)}
```

---

# Endpoint Functionality

Each endpoint:

- Receives HTTP request
- Calls corresponding CRUD function
- Retrieves count from database
- Returns JSON response

Example response:

```json
{
  "customers": 122
}
```

---

# Logging in Router Layer

The router layer logged:

- incoming API requests
- successful responses
- endpoint failures

Example:

```python
logger.info("GET /customers/count requested")
```

---

# Testing Individual Endpoints

The endpoints were tested using FastAPI Swagger UI.

Accessible at:

```text
http://127.0.0.1:8000/docs
```

---

## Placeholder for Screenshot

```text
[Insert Screenshot: GET /customers/count response]
```

---

## Placeholder for Screenshot

```text
[Insert Screenshot: GET /orders/count response]
```

---

# Part 2: Building the Aggregated Dashboard Endpoint

# Objective

A master endpoint named `/overall_counts` was created to retrieve counts from all database tables simultaneously.

---

# Problem with Sequential Execution

Sequential processing would execute queries one after another:

```text
customers → wait
orders → wait
products → wait
employees → wait
```

This increases response time unnecessarily.

---

# Concurrent Execution Approach

To improve performance, asynchronous concurrency was implemented using:

```python
asyncio.gather()
```

This allows all queries to run simultaneously.

---

# Step 3: Implementing Async Count Functions

Async-compatible functions were created.

## Example Async Function

```python
async def get_customers_count_async(db):
    return crud.get_customers_count(db)
```

---

# Step 4: Creating the Aggregated Endpoint

The `/overall_counts` endpoint used `asyncio.gather()` to execute all queries concurrently.

## Example Concurrent Endpoint

```python
@router.get("/overall_counts")
async def overall_counts(db: Session = Depends(get_db)):

    results = await asyncio.gather(
        asyncio.to_thread(crud.get_customers_count, db),
        asyncio.to_thread(crud.get_orders_count, db),
        asyncio.to_thread(crud.get_products_count, db),
        asyncio.to_thread(crud.get_employees_count, db),
        asyncio.to_thread(crud.get_offices_count, db),
        asyncio.to_thread(crud.get_payments_count, db),
        asyncio.to_thread(crud.get_orderdetails_count, db),
        asyncio.to_thread(crud.get_productlines_count, db)
    )

    return {
        "customers": results[0],
        "orders": results[1],
        "products": results[2],
        "employees": results[3],
        "offices": results[4],
        "payments": results[5],
        "orderdetails": results[6],
        "productlines": results[7]
    }
```

---

# Explanation of `asyncio.gather()`

`asyncio.gather()` starts all tasks simultaneously and waits until all tasks complete.

Instead of waiting for one database query to finish before starting the next, all database operations run concurrently.

This significantly improves performance and scalability.

---

# Example JSON Response

```json
{
  "customers": 122,
  "orders": 326,
  "products": 110,
  "employees": 23,
  "offices": 7,
  "payments": 273,
  "orderdetails": 2996,
  "productlines": 7
}
```

---

# Logging Concurrent Operations

Additional logging was implemented for concurrency tracking.

The system logged:

- when all async tasks started
- when `asyncio.gather()` completed
- total endpoint execution time

Example:

```python
logger.info("Starting concurrent database queries")
logger.info("All concurrent queries completed")
```

---

# Measuring Performance

Execution time tracking was added for monitoring API performance.

Example:

```python
start_time = time.time()
execution_time = time.time() - start_time
```

This helps monitor scalability and optimization opportunities.

---

# Handling Empty Tables

The API was designed to handle empty tables gracefully.

If a table contains no data:

- the API returns `0`
- the application does not crash

Example:

```json
{
  "customers": 0
}
```

---

# Testing the Aggregated Endpoint

The `/overall_counts` endpoint was tested using Swagger UI.

---

## Placeholder for Screenshot

```text
[Insert Screenshot: GET /overall_counts response]
```

---

# Logging Output Verification

The generated `app.log` file recorded:

- API requests
- database queries
- async execution events
- errors
- performance metrics

---

## Placeholder for Screenshot

```text
[Insert Screenshot: app.log showing concurrency logs]
```

---

# Conceptual Understanding: Factor VIII – Concurrency

This task demonstrated the Twelve-Factor App principle of concurrency.

---

# Sequential Processing

Sequential execution:

- processes one task at a time
- wastes waiting time
- reduces scalability

Example analogy:

- one cashier serving a long queue

---

# Concurrent Processing

Concurrent execution:

- runs multiple tasks simultaneously
- improves throughput
- increases scalability

Example analogy:

- multiple cashiers serving customers at the same time

---

# Benefits of Using Async in FastAPI

Using `async` and `await` allows the FastAPI server to:

- continue handling other requests
- avoid blocking during database operations
- improve responsiveness under load

---

# Success Checklist

## Modularity

- Separate CRUD functions created
- Independent endpoints implemented

## Concurrency

- `asyncio.gather()` used
- No sequential execution

## Logging

- Request logging implemented
- Database operations logged
- Async execution tracked

## Robustness

- Empty tables handled safely
- Errors logged properly

---

# Conclusion

In this task, a concurrent dashboard API was successfully developed using FastAPI, SQLAlchemy, and Python asyncio. Separate modular endpoints were implemented for each database table, followed by an aggregated dashboard endpoint capable of executing all database queries concurrently.

The use of `asyncio.gather()` significantly improved performance by avoiding sequential delays. Centralized logging improved observability and debugging, while modular architecture ensured maintainability and scalability.

This task demonstrated practical backend engineering concepts including concurrency, asynchronous programming, modular API design, logging, and scalable system architecture.