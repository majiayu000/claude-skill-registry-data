---
name: frappe-documentation-generator
description: Generate API documentation, user guides, and technical documentation for Frappe apps. Use when documenting APIs, creating user guides, or generating OpenAPI specs.
---

# Frappe Documentation Generator

Generate comprehensive documentation for Frappe applications including API documentation, user guides, and OpenAPI specifications.

## When to Use This Skill

Claude should invoke this skill when:
- User wants to document APIs
- User needs user documentation
- User mentions documentation, API docs, or guides
- User wants OpenAPI/Swagger specs
- User needs to document DocTypes or workflows

## Capabilities

### 1. API Documentation

**Whitelisted Method Documentation:**
```python
@frappe.whitelist()
def get_customer_details(customer):
    """
    Get detailed customer information

    Args:
        customer (str): Customer ID or name

    Returns:
        dict: Customer details including:
            - name: Customer ID
            - customer_name: Full name
            - email_id: Email address
            - mobile_no: Phone number
            - credit_limit: Credit limit amount
            - outstanding_amount: Current outstanding

    Raises:
        frappe.PermissionError: If user lacks read permission
        frappe.DoesNotExistError: If customer not found

    Example:
        >>> get_customer_details("CUST-001")
        {
            "name": "CUST-001",
            "customer_name": "John Doe",
            "email_id": "john@example.com",
            ...
        }

    Endpoint:
        POST /api/method/my_app.api.get_customer_details
        {
            "customer": "CUST-001"
        }
    """
    if not frappe.has_permission('Customer', 'read'):
        frappe.throw(_('Not permitted'), frappe.PermissionError)

    customer_doc = frappe.get_doc('Customer', customer)

    return {
        'name': customer_doc.name,
        'customer_name': customer_doc.customer_name,
        'email_id': customer_doc.email_id,
        'mobile_no': customer_doc.mobile_no,
        'credit_limit': customer_doc.credit_limit,
        'outstanding_amount': customer_doc.get_outstanding()
    }
```

### 2. OpenAPI Specification

**Generate OpenAPI/Swagger:**
```yaml
openapi: 3.0.0
info:
  title: My Frappe App API
  version: 1.0.0
  description: API documentation for My Frappe App

servers:
  - url: https://example.com/api
    description: Production server

paths:
  /method/my_app.api.get_customer_details:
    post:
      summary: Get customer details
      description: Retrieve detailed information for a customer
      tags:
        - Customers
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                customer:
                  type: string
                  description: Customer ID
              required:
                - customer
      responses:
        '200':
          description: Customer details
          content:
            application/json:
              schema:
                type: object
                properties:
                  name:
                    type: string
                  customer_name:
                    type: string
                  email_id:
                    type: string
        '403':
          description: Permission denied
        '404':
          description: Customer not found
```

### 3. User Guide Generation

**DocType User Guide:**
```markdown
# Customer Management Guide

## Overview
The Customer DocType stores information about your customers including contact details, credit limits, and transaction history.

## Creating a Customer

1. Go to **Selling > Customer**
2. Click **New Customer**
3. Fill in required fields:
   - Customer Name: Full name of the customer
   - Customer Group: Classification (Individual/Company)
   - Territory: Geographic location
4. Optional fields:
   - Email, Phone, Address
   - Credit Limit and Payment Terms
5. Click **Save**

## Key Features

### Credit Management
- Set credit limits to control customer purchases
- Monitor outstanding amounts
- Get alerts on credit limit breach

### Transaction History
View all customer transactions:
- Sales Invoices
- Payment Entries
- Delivery Notes

## Workflows

### Standard Flow
1. Create Customer
2. Create Sales Order
3. Create Sales Invoice
4. Receive Payment
5. Deliver Goods

## Tips
- Use customer groups for bulk operations
- Set default price lists per customer
- Configure payment terms for auto-fill
```

## References

**Frappe Documentation Patterns:**
- Frappe Docs: https://github.com/frappe/frappe/tree/develop/frappe/docs
- ERPNext Docs: https://github.com/frappe/erpnext/tree/develop/erpnext/docs
