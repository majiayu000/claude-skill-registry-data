---
name: frappe-api-handler
description: Create custom API endpoints and whitelisted methods for Frappe applications. Use when building REST APIs or custom endpoints.
---

# Frappe API Handler Skill

Create secure, efficient custom API endpoints for Frappe applications.

## When to Use This Skill

Claude should invoke this skill when:
- User wants to create custom API endpoints
- User needs to whitelist Python methods for API access
- User asks about REST API implementation
- User wants to integrate external systems with Frappe
- User needs help with API authentication or permissions

## Capabilities

### 1. Whitelisted Methods

Create Python methods accessible via API:

```python
import frappe
from frappe import _

@frappe.whitelist()
def get_customer_details(customer_name):
    """Get customer details with validation"""
    # Permission check
    if not frappe.has_permission("Customer", "read"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    customer = frappe.get_doc("Customer", customer_name)

    return {
        "name": customer.name,
        "customer_name": customer.customer_name,
        "email": customer.email_id,
        "phone": customer.mobile_no,
        "outstanding_amount": customer.get_outstanding()
    }
```

### 2. API Method Patterns

**Public Methods (No Authentication):**
```python
@frappe.whitelist(allow_guest=True)
def public_api_method():
    """Accessible without login"""
    return {"message": "Public data"}
```

**Authenticated Methods:**
```python
@frappe.whitelist()
def authenticated_method():
    """Requires valid session or API key"""
    user = frappe.session.user
    return {"user": user}
```

**Permission-based Methods:**
```python
@frappe.whitelist()
def delete_customer(customer_name):
    """Check permissions before action"""
    if not frappe.has_permission("Customer", "delete"):
        frappe.throw(_("Not permitted"))

    frappe.delete_doc("Customer", customer_name)
    return {"message": "Customer deleted"}
```

### 3. REST API Endpoints

**GET Request Handler:**
```python
@frappe.whitelist()
def get_items(filters=None, fields=None, limit=20):
    """Get list of items with filters"""
    filters = frappe.parse_json(filters) if isinstance(filters, str) else filters or {}
    fields = frappe.parse_json(fields) if isinstance(fields, str) else fields or ["*"]

    items = frappe.get_all(
        "Item",
        filters=filters,
        fields=fields,
        limit=limit,
        order_by="creation desc"
    )

    return {"items": items}
```

**POST Request Handler:**
```python
@frappe.whitelist()
def create_sales_order(customer, items, delivery_date=None):
    """Create sales order from API"""
    items = frappe.parse_json(items) if isinstance(items, str) else items

    doc = frappe.get_doc({
        "doctype": "Sales Order",
        "customer": customer,
        "delivery_date": delivery_date or frappe.utils.today(),
        "items": items
    })

    doc.insert()
    doc.submit()

    return {"name": doc.name, "grand_total": doc.grand_total}
```

**PUT/UPDATE Handler:**
```python
@frappe.whitelist()
def update_customer(customer_name, data):
    """Update customer details"""
    data = frappe.parse_json(data) if isinstance(data, str) else data

    doc = frappe.get_doc("Customer", customer_name)
    doc.update(data)
    doc.save()

    return {"name": doc.name, "message": "Updated successfully"}
```

**DELETE Handler:**
```python
@frappe.whitelist()
def delete_document(doctype, name):
    """Delete a document"""
    if not frappe.has_permission(doctype, "delete"):
        frappe.throw(_("Not permitted"))

    frappe.delete_doc(doctype, name)
    return {"message": f"{doctype} {name} deleted"}
```

### 4. Error Handling

```python
@frappe.whitelist()
def safe_api_method(param):
    """API method with proper error handling"""
    try:
        # Validate input
        if not param:
            frappe.throw(_("Parameter is required"))

        # Process request
        result = process_data(param)

        return {"success": True, "data": result}

    except frappe.ValidationError as e:
        frappe.log_error(frappe.get_traceback(), "API Validation Error")
        return {"success": False, "message": str(e)}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error")
        return {"success": False, "message": "Internal server error"}
```

### 5. Input Validation

```python
@frappe.whitelist()
def validated_method(email, phone, amount):
    """Validate all inputs"""
    # Email validation
    if not frappe.utils.validate_email_address(email):
        frappe.throw(_("Invalid email address"))

    # Phone validation
    if not phone or len(phone) < 10:
        frappe.throw(_("Invalid phone number"))

    # Amount validation
    amount = frappe.utils.flt(amount)
    if amount <= 0:
        frappe.throw(_("Amount must be greater than zero"))

    return {"valid": True}
```

### 6. Pagination

```python
@frappe.whitelist()
def paginated_list(doctype, page=1, page_size=20, filters=None):
    """Get paginated results"""
    filters = frappe.parse_json(filters) if isinstance(filters, str) else filters or {}

    page = frappe.utils.cint(page)
    page_size = frappe.utils.cint(page_size)

    # Get total count
    total = frappe.db.count(doctype, filters=filters)

    # Get data
    data = frappe.get_all(
        doctype,
        filters=filters,
        fields=["*"],
        start=(page - 1) * page_size,
        page_length=page_size,
        order_by="creation desc"
    )

    return {
        "data": data,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }
```

### 7. File Upload Handling

```python
@frappe.whitelist()
def upload_file():
    """Handle file upload"""
    from frappe.utils.file_manager import save_file

    if not frappe.request.files:
        frappe.throw(_("No file uploaded"))

    file = frappe.request.files['file']

    # Save file
    file_doc = save_file(
        fname=file.filename,
        content=file.stream.read(),
        dt="Customer",  # DocType
        dn="CUST-001",  # Document name
        is_private=1
    )

    return {
        "file_url": file_doc.file_url,
        "file_name": file_doc.file_name
    }
```

### 8. Bulk Operations

```python
@frappe.whitelist()
def bulk_create(doctype, records):
    """Create multiple documents"""
    records = frappe.parse_json(records) if isinstance(records, str) else records

    created = []
    errors = []

    for record in records:
        try:
            doc = frappe.get_doc(record)
            doc.insert()
            created.append(doc.name)
        except Exception as e:
            errors.append({
                "record": record,
                "error": str(e)
            })

    return {
        "created": created,
        "errors": errors,
        "success_count": len(created),
        "error_count": len(errors)
    }
```

### 9. API Response Formats

**Success Response:**
```python
return {
    "success": True,
    "data": result,
    "message": "Operation completed successfully"
}
```

**Error Response:**
```python
return {
    "success": False,
    "message": "Error message",
    "errors": validation_errors
}
```

**List Response:**
```python
return {
    "success": True,
    "data": items,
    "total": total_count,
    "page": current_page
}
```

### 10. Authentication Patterns

**API Key/Secret:**
```python
@frappe.whitelist(allow_guest=True)
def api_key_method():
    """Authenticate using API key"""
    api_key = frappe.get_request_header("Authorization")

    if not api_key:
        frappe.throw(_("API key required"))

    # Validate API key
    user = frappe.db.get_value("User", {"api_key": api_key}, "name")
    if not user:
        frappe.throw(_("Invalid API key"))

    frappe.set_user(user)

    # Process request
    return {"authenticated": True}
```

**Token-based:**
```python
@frappe.whitelist(allow_guest=True)
def token_auth():
    """JWT or custom token authentication"""
    token = frappe.get_request_header("Authorization", "").replace("Bearer ", "")

    if not token:
        frappe.throw(_("Token required"))

    # Validate token
    user_data = validate_token(token)
    frappe.set_user(user_data["email"])

    return {"authenticated": True}
```

## API Endpoint URLs

Methods are accessible at:
```
/api/method/{app_name}.{module}.{file}.{method_name}
```

Example:
```
POST /api/method/my_app.api.customer.get_customer_details
Content-Type: application/json

{
  "customer_name": "CUST-001"
}
```

## Best Practices

1. **Always validate inputs** - Never trust user data
2. **Check permissions** - Use `frappe.has_permission()`
3. **Handle errors gracefully** - Return user-friendly messages
4. **Log errors** - Use `frappe.log_error()` for debugging
5. **Use transactions** - Wrap multiple operations in `frappe.db.commit()`
6. **Rate limiting** - Consider implementing for public APIs
7. **Version your APIs** - Include version in URL or headers
8. **Document your APIs** - Provide clear documentation
9. **Use HTTP status codes** - Return appropriate codes
10. **Sanitize output** - Don't expose sensitive data

## File Location

API methods should be placed in:
```
apps/<app_name>/api.py
```
or
```
apps/<app_name>/<module>/api.py
```

## Testing APIs

Use curl or Postman:
```bash
# With session
curl -X POST \
  http://localhost:8000/api/method/my_app.api.get_items \
  -H "Content-Type: application/json" \
  -d '{"filters": {"item_group": "Products"}}'

# With API key
curl -X POST \
  http://localhost:8000/api/method/my_app.api.get_items \
  -H "Authorization: token xxx:yyy" \
  -d '{"filters": {"item_group": "Products"}}'
```

Remember: This skill is model-invoked. Claude will use it autonomously when detecting API development tasks.
