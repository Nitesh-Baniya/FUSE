from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import asyncio
import time
from app.database import SessionLocal
from app.crud import (
    get_customer, get_customers, create_customer, update_customer, delete_customer,
    get_customers_count, get_orders_count, get_products_count, get_employees_count,
    get_offices_count, get_payments_count, get_orderdetails_count, get_productlines_count
)
from app.schemas import CustomerCreate, CustomerUpdate, CustomerOut
from app.logger import logger

router = APIRouter()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/customers", response_model=List[CustomerOut])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve multiple customers with pagination"""
    logger.info(f"GET request received for /customers with skip={skip}, limit={limit}")
    customers = get_customers(db, skip=skip, limit=limit)
    logger.info(f"Returning {len(customers)} customers")
    return customers

@router.get("/customers/count")
def customers_count(db: Session = Depends(get_db)):
    """Get total number of customers"""
    logger.info("GET request received for /customers/count")
    count = get_customers_count(db)
    logger.info(f"Returning customers count: {count}")
    return {"customers": count}

@router.get("/customers/{customer_id}", response_model=CustomerOut)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    """Retrieve a single customer by ID"""
    logger.info(f"GET request received for /customers/{customer_id}")
    customer = get_customer(db, customer_id=customer_id)
    logger.info(f"Returning customer ID {customer_id}")
    return customer

@router.post("/customers", response_model=CustomerOut)
def create_new_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    logger.info(f"POST request received for /customers with data: {customer.customerName}")
    new_customer = create_customer(db=db, customer=customer)
    logger.info(f"Created new customer with ID {new_customer.customerNumber}")
    return new_customer

@router.put("/customers/{customer_id}", response_model=CustomerOut)
def update_existing_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    """Update an existing customer"""
    logger.info(f"PUT request received for /customers/{customer_id}")
    updated_customer = update_customer(db=db, customer_id=customer_id, customer=customer)
    logger.info(f"Updated customer ID {customer_id}")
    return updated_customer

@router.delete("/customers/{customer_id}", response_model=CustomerOut)
def delete_existing_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete a customer"""
    logger.info(f"DELETE request received for /customers/{customer_id}")
    deleted_customer = delete_customer(db=db, customer_id=customer_id)
    logger.info(f"Deleted customer ID {customer_id}")
    return deleted_customer

# Individual count endpoints for dashboard API

@router.get("/orders/count")
def orders_count(db: Session = Depends(get_db)):
    """Get total number of orders"""
    logger.info("GET request received for /orders/count")
    count = get_orders_count(db)
    logger.info(f"Returning orders count: {count}")
    return {"orders": count}

@router.get("/products/count")
def products_count(db: Session = Depends(get_db)):
    """Get total number of products"""
    logger.info("GET request received for /products/count")
    count = get_products_count(db)
    logger.info(f"Returning products count: {count}")
    return {"products": count}

@router.get("/employees/count")
def employees_count(db: Session = Depends(get_db)):
    """Get total number of employees"""
    logger.info("GET request received for /employees/count")
    count = get_employees_count(db)
    logger.info(f"Returning employees count: {count}")
    return {"employees": count}

@router.get("/offices/count")
def offices_count(db: Session = Depends(get_db)):
    """Get total number of offices"""
    logger.info("GET request received for /offices/count")
    count = get_offices_count(db)
    logger.info(f"Returning offices count: {count}")
    return {"offices": count}

@router.get("/payments/count")
def payments_count(db: Session = Depends(get_db)):
    """Get total number of payments"""
    logger.info("GET request received for /payments/count")
    count = get_payments_count(db)
    logger.info(f"Returning payments count: {count}")
    return {"payments": count}

@router.get("/orderdetails/count")
def orderdetails_count(db: Session = Depends(get_db)):
    """Get total number of order details"""
    logger.info("GET request received for /orderdetails/count")
    count = get_orderdetails_count(db)
    logger.info(f"Returning orderdetails count: {count}")
    return {"orderdetails": count}

@router.get("/productlines/count")
def productlines_count(db: Session = Depends(get_db)):
    """Get total number of product lines"""
    logger.info("GET request received for /productlines/count")
    count = get_productlines_count(db)
    logger.info(f"Returning productlines count: {count}")
    return {"productlines": count}

# Aggregated dashboard endpoint with concurrent execution
@router.get("/overall_counts")
async def overall_counts(db: Session = Depends(get_db)):
    """Get counts from all database tables concurrently"""
    logger.info("GET request received for /overall_counts")
    start_time = time.time()
    
    logger.info("Starting concurrent database queries")
    
    # Execute all count queries concurrently using asyncio.gather
    results = await asyncio.gather(
        asyncio.to_thread(get_customers_count, db),
        asyncio.to_thread(get_orders_count, db),
        asyncio.to_thread(get_products_count, db),
        asyncio.to_thread(get_employees_count, db),
        asyncio.to_thread(get_offices_count, db),
        asyncio.to_thread(get_payments_count, db),
        asyncio.to_thread(get_orderdetails_count, db),
        asyncio.to_thread(get_productlines_count, db)
    )
    
    execution_time = time.time() - start_time
    logger.info(f"All concurrent queries completed in {execution_time:.4f} seconds")
    
    response = {
        "customers": results[0],
        "orders": results[1],
        "products": results[2],
        "employees": results[3],
        "offices": results[4],
        "payments": results[5],
        "orderdetails": results[6],
        "productlines": results[7],
        "execution_time_seconds": round(execution_time, 4)
    }
    
    logger.info(f"Returning overall counts: {response}")
    return response