---
name: server-scripts
description: Frappe server-side Python patterns for controllers, document events, whitelisted APIs, background jobs, and database operations. Use when writing controller logic, creating APIs, handling document events, or processing data on the server.
---

# Frappe Server Scripts Reference

Complete reference for server-side Python development in Frappe Framework.

## When to Use This Skill

- Writing document controllers
- Creating whitelisted API endpoints
- Handling document lifecycle events
- Background job processing
- Database operations and queries
- Permission checks and validation
- Email and notification handling

## Controller Location

```
my_app/
└── my_module/
    └── doctype/
        └── my_doctype/
            └── my_doctype.py    # Python controller
```

## Document Controller

### Complete Controller Template

```python
# my_doctype.py
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, nowtime, flt, cint, getdate, add_days


class MyDocType(Document):
    # ===== NAMING =====

    def autoname(self):
        """Custom naming logic"""
        self.name = f"{self.prefix}-{frappe.generate_hash()[:8].upper()}"

    def before_naming(self):
        """Called before autoname"""
        pass

    # ===== VALIDATION =====

    def before_validate(self):
        """Called before validate"""
        self.set_defaults()

    def validate(self):
        """Main validation - called on insert and update"""
        self.validate_dates()
        self.validate_amounts()
        self.calculate_totals()
        self.set_status()

    def before_save(self):
        """Called after validate, before database write"""
        self.update_modified_info()

    # ===== INSERT =====

    def before_insert(self):
        """Called before new document is inserted"""
        self.set_initial_values()

    def after_insert(self):
        """Called after new document is inserted"""
        self.create_related_documents()
        self.send_notification()

    # ===== UPDATE =====

    def on_update(self):
        """Called after document is saved (insert or update)"""
        self.update_related_documents()
        self.clear_cache()

    def after_save(self):
        """Called after on_update, always runs"""
        pass

    def on_change(self):
        """Called when document changes in database"""
        pass

    # ===== SUBMISSION =====

    def before_submit(self):
        """Called before document is submitted"""
        self.validate_for_submit()

    def on_submit(self):
        """Called after document is submitted"""
        self.create_gl_entries()
        self.update_stock()

    def on_update_after_submit(self):
        """Called when submitted doc is updated (limited fields)"""
        pass

    # ===== CANCELLATION =====

    def before_cancel(self):
        """Called before document is cancelled"""
        self.validate_cancellation()

    def on_cancel(self):
        """Called after document is cancelled"""
        self.reverse_gl_entries()
        self.reverse_stock()

    # ===== DELETION =====

    def before_delete(self):
        """Called before document is deleted"""
        self.check_dependencies()

    def after_delete(self):
        """Called after document is deleted"""
        self.cleanup_related()

    def on_trash(self):
        """Called when document is trashed"""
        pass

    def after_restore(self):
        """Called after document is restored from trash"""
        pass

    # ===== CUSTOM METHODS =====

    def set_defaults(self):
        """Set default values"""
        if not self.posting_date:
            self.posting_date = nowdate()
        if not self.company:
            self.company = frappe.defaults.get_user_default("Company")

    def validate_dates(self):
        """Validate date fields"""
        if self.end_date and getdate(self.start_date) > getdate(self.end_date):
            frappe.throw(_("End Date cannot be before Start Date"))

        if getdate(self.posting_date) > getdate(nowdate()):
            frappe.throw(_("Posting Date cannot be in the future"))

    def validate_amounts(self):
        """Validate amount fields"""
        for item in self.items:
            if flt(item.qty) <= 0:
                frappe.throw(_("Row {0}: Quantity must be greater than 0").format(item.idx))
            if flt(item.rate) < 0:
                frappe.throw(_("Row {0}: Rate cannot be negative").format(item.idx))

    def calculate_totals(self):
        """Calculate document totals"""
        self.total = 0
        for item in self.items:
            item.amount = flt(item.qty) * flt(item.rate)
            self.total += item.amount

        self.tax_amount = flt(self.total) * flt(self.tax_rate) / 100
        self.grand_total = flt(self.total) + flt(self.tax_amount)

    def set_status(self):
        """Set document status based on state"""
        if self.docstatus == 0:
            self.status = "Draft"
        elif self.docstatus == 1:
            if self.is_completed():
                self.status = "Completed"
            else:
                self.status = "Submitted"
        elif self.docstatus == 2:
            self.status = "Cancelled"

    def is_completed(self):
        """Check if document is completed"""
        return all(item.delivered_qty >= item.qty for item in self.items)
```

## Whitelisted APIs

### Basic API

```python
@frappe.whitelist()
def get_customer_details(customer):
    """Get customer details

    Args:
        customer (str): Customer ID

    Returns:
        dict: Customer details with outstanding amount
    """
    if not customer:
        frappe.throw(_("Customer is required"))

    doc = frappe.get_doc("Customer", customer)

    return {
        "customer_name": doc.customer_name,
        "customer_type": doc.customer_type,
        "territory": doc.territory,
        "credit_limit": flt(doc.credit_limit),
        "outstanding": get_customer_outstanding(customer)
    }


@frappe.whitelist()
def create_invoice(customer, items):
    """Create sales invoice from data

    Args:
        customer (str): Customer ID
        items (str): JSON string of items

    Returns:
        str: Invoice name
    """
    items = frappe.parse_json(items)

    doc = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": customer,
        "items": [{
            "item_code": item.get("item_code"),
            "qty": flt(item.get("qty")),
            "rate": flt(item.get("rate"))
        } for item in items]
    })

    doc.insert()
    doc.submit()

    return doc.name
```

### Guest API

```python
@frappe.whitelist(allow_guest=True)
def get_public_data():
    """Public API - no login required"""
    return {
        "status": "ok",
        "message": "This is public data"
    }
```

### Method-Restricted API

```python
@frappe.whitelist(methods=["POST"])
def create_record(data):
    """Only accepts POST requests"""
    data = frappe.parse_json(data)
    doc = frappe.get_doc(data)
    doc.insert()
    return {"name": doc.name}


@frappe.whitelist(methods=["GET", "POST"])
def flexible_endpoint(**kwargs):
    """Accepts GET and POST"""
    return kwargs
```

### Permission-Checked API

```python
@frappe.whitelist()
def sensitive_operation(doctype, name):
    """API with permission check"""
    # Check permission
    if not frappe.has_permission(doctype, "write", name):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    # Proceed with operation
    doc = frappe.get_doc(doctype, name)
    # ... do something

    return {"status": "success"}
```

## Database Operations

### Reading Data

```python
# Get single document
doc = frappe.get_doc("Customer", "CUST-001")

# Get with filters
doc = frappe.get_doc("Customer", {"customer_name": "John Corp"})

# Get single value
name = frappe.db.get_value("Customer", "CUST-001", "customer_name")

# Get multiple values
values = frappe.db.get_value("Customer", "CUST-001",
    ["customer_name", "territory"], as_dict=True)

# Get list
customers = frappe.db.get_all("Customer",
    filters={"status": "Active"},
    fields=["name", "customer_name", "territory"],
    order_by="customer_name asc",
    limit=10
)

# Complex filters
invoices = frappe.db.get_all("Sales Invoice",
    filters={
        "status": ["in", ["Paid", "Unpaid"]],
        "grand_total": [">", 1000],
        "posting_date": [">=", "2024-01-01"],
        "customer": ["like", "%Corp%"]
    },
    fields=["name", "customer", "grand_total"]
)

# Pluck single field
names = frappe.db.get_all("Customer",
    filters={"status": "Active"},
    pluck="name"
)

# Count
count = frappe.db.count("Customer", {"status": "Active"})

# Exists check
exists = frappe.db.exists("Customer", "CUST-001")
```

### Raw SQL

```python
# Simple query
result = frappe.db.sql("""
    SELECT name, customer_name, grand_total
    FROM `tabSales Invoice`
    WHERE status = %s AND grand_total > %s
    ORDER BY creation DESC
    LIMIT 10
""", ("Paid", 1000), as_dict=True)

# Named parameters
result = frappe.db.sql("""
    SELECT * FROM `tabCustomer`
    WHERE territory = %(territory)s
    AND status = %(status)s
""", {"territory": "West", "status": "Active"}, as_dict=True)

# Aggregation
total = frappe.db.sql("""
    SELECT SUM(grand_total) as total
    FROM `tabSales Invoice`
    WHERE status = 'Paid'
""")[0][0] or 0
```

### Writing Data

```python
# Create document
doc = frappe.get_doc({
    "doctype": "Customer",
    "customer_name": "New Customer",
    "customer_type": "Company"
})
doc.insert()

# Update document
doc = frappe.get_doc("Customer", "CUST-001")
doc.customer_name = "Updated Name"
doc.save()

# Quick update (bypasses controller)
frappe.db.set_value("Customer", "CUST-001", "status", "Inactive")

# Update multiple fields
frappe.db.set_value("Customer", "CUST-001", {
    "status": "Inactive",
    "disabled": 1
})

# Delete
frappe.delete_doc("Customer", "CUST-001")

# Commit transaction
frappe.db.commit()

# Rollback
frappe.db.rollback()
```

## Background Jobs

### Enqueue Jobs

```python
# Basic enqueue
frappe.enqueue(
    "my_app.tasks.process_data",
    queue="default",
    customer="CUST-001"
)

# With options
frappe.enqueue(
    method="my_app.tasks.heavy_task",
    queue="long",        # short, default, long
    timeout=1800,        # 30 minutes
    is_async=True,
    job_name="Heavy Task",
    now=False,           # True to run immediately
    enqueue_after_commit=True,
    # Task arguments
    document_name="DOC-001",
    data={"key": "value"}
)
```

### Task Function

```python
# my_app/tasks.py
import frappe

def process_data(customer):
    """Background task"""
    frappe.init(site=frappe.local.site)
    frappe.connect()

    try:
        # Process logic
        doc = frappe.get_doc("Customer", customer)
        doc.last_processed = frappe.utils.now()
        doc.save()
        frappe.db.commit()
    except Exception:
        frappe.log_error(title="Process Data Failed")
        raise
    finally:
        frappe.destroy()
```

### Scheduled Jobs (hooks.py)

```python
scheduler_events = {
    "all": [
        "my_app.tasks.every_minute"
    ],
    "daily": [
        "my_app.tasks.daily_report"
    ],
    "hourly": [
        "my_app.tasks.hourly_sync"
    ],
    "cron": {
        "0 9 * * 1": [
            "my_app.tasks.monday_morning"
        ],
        "*/15 * * * *": [
            "my_app.tasks.every_15_min"
        ]
    }
}
```

## Error Handling

```python
from frappe import _
from frappe.exceptions import ValidationError, PermissionError

def my_function():
    # Throw with message
    frappe.throw(_("Invalid data"))

    # Throw with title
    frappe.throw(_("Cannot proceed"), title=_("Error"))

    # Throw with exception type
    frappe.throw(_("Permission denied"), exc=PermissionError)

    # Message without stopping
    frappe.msgprint(_("Warning: Check your data"))

    # Log error
    frappe.log_error(
        title="My Error",
        message=frappe.get_traceback()
    )

    # Try-except
    try:
        risky_operation()
    except Exception:
        frappe.log_error("Operation failed")
        frappe.throw(_("Something went wrong"))
```

## Utilities

```python
from frappe.utils import (
    nowdate, nowtime, now_datetime, today,
    getdate, get_datetime,
    add_days, add_months, add_years,
    date_diff, time_diff_in_seconds,
    flt, cint, cstr,
    fmt_money, rounded,
    strip_html, escape_html
)

# Date operations
today = nowdate()  # "2024-01-15"
week_later = add_days(nowdate(), 7)
month_end = frappe.utils.get_last_day(nowdate())

# Number operations
amount = flt(value, 2)  # Float with precision
count = cint(value)     # Integer

# Formatting
money = fmt_money(1234.56, currency="USD")

# Current user
user = frappe.session.user
roles = frappe.get_roles()
```

## Email & Notifications

```python
# Send email
frappe.sendmail(
    recipients=["user@example.com"],
    subject="Subject",
    message="Email body",
    reference_doctype="Sales Invoice",
    reference_name="SINV-00001"
)

# With template
frappe.sendmail(
    recipients=["user@example.com"],
    subject="Order Confirmation",
    template="order_confirmation",
    args={
        "customer_name": "John",
        "order_id": "ORD-001"
    }
)

# Real-time notification
frappe.publish_realtime(
    "msgprint",
    {"message": "Task completed"},
    user="user@example.com"
)
```

## Document Events via Hooks

```python
# hooks.py
doc_events = {
    "Sales Invoice": {
        "validate": "my_app.overrides.validate_invoice",
        "on_submit": "my_app.overrides.on_submit_invoice",
        "on_cancel": "my_app.overrides.on_cancel_invoice"
    },
    "*": {
        "on_update": "my_app.overrides.log_all_changes"
    }
}
```

```python
# my_app/overrides.py
import frappe

def validate_invoice(doc, method):
    """Called during Sales Invoice validation"""
    if doc.grand_total > 100000:
        if not doc.manager_approval:
            frappe.throw(_("Manager approval required for orders above 100,000"))

def on_submit_invoice(doc, method):
    """Called when Sales Invoice is submitted"""
    create_delivery_note(doc)
    notify_warehouse(doc)
```
