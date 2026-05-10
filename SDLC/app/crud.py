from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Customer, Product, ProductLine, Office, Employee, Order, OrderDetail, Payment
from app.schemas import CustomerCreate, CustomerUpdate
from app.logger import logger
from typing import List, Optional

def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    """Retrieve a single customer by ID"""
    logger.info(f"Fetching customer ID {customer_id}")
    customer = db.query(Customer).filter(Customer.customerNumber == customer_id).first()
    if not customer:
        logger.warning(f"Customer not found: ID {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    logger.info(f"Successfully retrieved customer ID {customer_id}")
    return customer

def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
    """Retrieve multiple customers with pagination"""
    logger.info(f"Fetching customers with skip={skip}, limit={limit}")
    customers = db.query(Customer).offset(skip).limit(limit).all()
    logger.info(f"Retrieved {len(customers)} customers")
    return customers

def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    """Create a new customer"""
    logger.info(f"Creating new customer: {customer.customerName}")
    
    # Get the next customer number
    max_customer = db.query(Customer).order_by(Customer.customerNumber.desc()).first()
    next_customer_number = (max_customer.customerNumber + 1) if max_customer else 1
    
    db_customer = Customer(
        customerNumber=next_customer_number,
        customerName=customer.customerName,
        contactLastName=customer.contactLastName,
        contactFirstName=customer.contactFirstName,
        phone=customer.phone,
        addressLine1=customer.addressLine1,
        addressLine2=customer.addressLine2,
        city=customer.city,
        state=customer.state,
        postalCode=customer.postalCode,
        country=customer.country,
        salesRepEmployeeNumber=customer.salesRepEmployeeNumber,
        creditLimit=customer.creditLimit
    )
    
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    
    logger.info(f"Successfully created customer with ID {db_customer.customerNumber}")
    return db_customer

def update_customer(db: Session, customer_id: int, customer: CustomerUpdate) -> Customer:
    """Update an existing customer"""
    logger.info(f"Updating customer ID {customer_id}")
    
    db_customer = db.query(Customer).filter(Customer.customerNumber == customer_id).first()
    if not db_customer:
        logger.warning(f"Customer not found for update: ID {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    
    update_data = customer.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)
    
    db.commit()
    db.refresh(db_customer)
    
    logger.info(f"Successfully updated customer ID {customer_id}")
    return db_customer

def delete_customer(db: Session, customer_id: int) -> Customer:
    """Delete a customer"""
    logger.info(f"Deleting customer ID {customer_id}")
    
    db_customer = db.query(Customer).filter(Customer.customerNumber == customer_id).first()
    if not db_customer:
        logger.warning(f"Customer not found for deletion: ID {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(db_customer)
    db.commit()
    
    logger.info(f"Successfully deleted customer ID {customer_id}")
    return db_customer

# Count functions for dashboard API
def get_customers_count(db: Session) -> int:
    """Get total number of customers"""
    logger.info("Fetching customer count")
    count = db.query(Customer).count()
    logger.info(f"Customer count: {count}")
    return count

def get_orders_count(db: Session) -> int:
    """Get total number of orders"""
    logger.info("Fetching orders count")
    count = db.query(Order).count()
    logger.info(f"Orders count: {count}")
    return count

def get_products_count(db: Session) -> int:
    """Get total number of products"""
    logger.info("Fetching products count")
    count = db.query(Product).count()
    logger.info(f"Products count: {count}")
    return count

def get_employees_count(db: Session) -> int:
    """Get total number of employees"""
    logger.info("Fetching employees count")
    count = db.query(Employee).count()
    logger.info(f"Employees count: {count}")
    return count

def get_offices_count(db: Session) -> int:
    """Get total number of offices"""
    logger.info("Fetching offices count")
    count = db.query(Office).count()
    logger.info(f"Offices count: {count}")
    return count

def get_payments_count(db: Session) -> int:
    """Get total number of payments"""
    logger.info("Fetching payments count")
    count = db.query(Payment).count()
    logger.info(f"Payments count: {count}")
    return count

def get_orderdetails_count(db: Session) -> int:
    """Get total number of order details"""
    logger.info("Fetching order details count")
    count = db.query(OrderDetail).count()
    logger.info(f"Order details count: {count}")
    return count

def get_productlines_count(db: Session) -> int:
    """Get total number of product lines"""
    logger.info("Fetching product lines count")
    count = db.query(ProductLine).count()
    logger.info(f"Product lines count: {count}")
    return count