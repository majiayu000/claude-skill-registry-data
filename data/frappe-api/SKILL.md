---
name: frappe-api
description: Frappe Python and JavaScript API reference including document operations, database queries, utilities, and REST API patterns. Use when working with frappe.get_doc, frappe.db, frappe.call, or any Frappe API methods.
---

# Frappe API Reference

Complete reference for Frappe's Python and JavaScript APIs for document operations, database queries, utilities, and server communication.

## When to Use This Skill

- Working with Document API (get_doc, new_doc, save)
- Database operations (frappe.db.*)
- Making API calls from client to server
- Using Frappe utilities (date, number formatting)
- Creating whitelisted API endpoints
- Working with REST API

## Python API

### Document Operations

#### Get Document
```python
# Get existing document
doc = frappe.get_doc("Customer", "CUST-001")

# Get document with filters
doc = frappe.get_doc("Customer", {"customer_name": "John"})

# Get last document
doc = frappe.get_last_doc("Customer", filters={"status": "Active"})

# Get cached document (read-only, faster)
doc = frappe.get_cached_doc("Customer", "CUST-001")

# Check if document exists
if frappe.db.exists("Customer", "CUST-001"):
    doc = frappe.get_doc("Customer", "CUST-001")
```

#### Create Document
```python
# Create new document
doc = frappe.new_doc("Customer")
doc.customer_name = "New Customer"
doc.customer_type = "Company"
doc.insert()

# Create with dict
doc = frappe.get_doc({
    "doctype": "Customer",
    "customer_name": "New Customer",
    "customer_type": "Company"
})
doc.insert()

# Create and insert in one step
doc = frappe.get_doc({
    "doctype": "Customer",
    "customer_name": "New Customer"
}).insert()

# Insert ignoring permissions
doc.insert(ignore_permissions=True)

# Insert ignoring mandatory fields
doc.insert(ignore_mandatory=True)
```

#### Update Document
```python
# Update and save
doc = frappe.get_doc("Customer", "CUST-001")
doc.customer_name = "Updated Name"
doc.save()

# Save ignoring permissions
doc.save(ignore_permissions=True)

# Update single value
frappe.db.set_value("Customer", "CUST-001", "customer_name", "New Name")

# Update multiple values
frappe.db.set_value("Customer", "CUST-001", {
    "customer_name": "New Name",
    "status": "Active"
})

# Bulk update
frappe.db.set_value("Customer", {"status": "Inactive"}, "status", "Active")
```

#### Delete Document
```python
# Delete document
frappe.delete_doc("Customer", "CUST-001")

# Delete ignoring permissions
frappe.delete_doc("Customer", "CUST-001", ignore_permissions=True)

# Delete with linked documents
frappe.delete_doc("Customer", "CUST-001", force=True)

# Delete from controller
doc.delete()
```

### Database API (frappe.db)

#### Select Queries
```python
# Get single value
value = frappe.db.get_value("Customer", "CUST-001", "customer_name")

# Get multiple fields
values = frappe.db.get_value("Customer", "CUST-001",
    ["customer_name", "status"], as_dict=True)

# Get with filters
value = frappe.db.get_value("Customer",
    {"customer_type": "Company"}, "customer_name")

# Get list of values
names = frappe.db.get_all("Customer",
    filters={"status": "Active"},
    fields=["name", "customer_name"],
    order_by="creation desc",
    limit=10
)

# Get list with pluck (single field as list)
names = frappe.db.get_all("Customer",
    filters={"status": "Active"},
    pluck="name"
)

# Complex filters
docs = frappe.db.get_all("Sales Invoice",
    filters={
        "status": ["in", ["Paid", "Unpaid"]],
        "grand_total": [">", 1000],
        "posting_date": ["between", ["2024-01-01", "2024-12-31"]],
        "customer": ["like", "%Corp%"]
    },
    fields=["name", "customer", "grand_total"]
)

# Filter operators
# =, !=, <, >, <=, >=
# in, not in
# like, not like
# between
# is, is not (for None)
# descendants of, ancestors of (for tree doctypes)

# Get count
count = frappe.db.count("Customer", {"status": "Active"})

# Check existence
exists = frappe.db.exists("Customer", "CUST-001")
exists = frappe.db.exists("Customer", {"customer_name": "John"})
```

#### Raw SQL
```python
# Execute SQL query
result = frappe.db.sql("""
    SELECT name, customer_name, grand_total
    FROM `tabSales Invoice`
    WHERE status = %s AND grand_total > %s
    ORDER BY creation DESC
    LIMIT 10
""", ("Paid", 1000), as_dict=True)

# Single value
total = frappe.db.sql("""
    SELECT SUM(grand_total) FROM `tabSales Invoice`
    WHERE status = 'Paid'
""")[0][0]

# With named parameters
result = frappe.db.sql("""
    SELECT * FROM `tabCustomer`
    WHERE name = %(name)s
""", {"name": "CUST-001"}, as_dict=True)
```

#### Insert/Update
```python
# Insert raw
frappe.db.sql("""
    INSERT INTO `tabCustomer` (name, customer_name)
    VALUES (%s, %s)
""", ("CUST-002", "New Customer"))

# Commit transaction
frappe.db.commit()

# Rollback
frappe.db.rollback()
```

### Whitelisted API

```python
# Create API endpoint
@frappe.whitelist()
def get_customer_details(customer):
    """Get customer details

    Args:
        customer: Customer ID

    Returns:
        dict: Customer details
    """
    doc = frappe.get_doc("Customer", customer)
    return {
        "name": doc.name,
        "customer_name": doc.customer_name,
        "outstanding_amount": get_outstanding(customer)
    }

# Allow guest access (no login required)
@frappe.whitelist(allow_guest=True)
def public_api():
    return {"status": "ok"}

# With specific methods
@frappe.whitelist(methods=["POST"])
def create_record(data):
    doc = frappe.get_doc(data)
    doc.insert()
    return doc.name
```

### Utilities

#### Date/Time
```python
from frappe.utils import (
    now, nowdate, nowtime, now_datetime,
    today, getdate, get_datetime,
    add_days, add_months, add_years,
    date_diff, time_diff, time_diff_in_seconds,
    get_first_day, get_last_day,
    formatdate, format_datetime
)

# Current date/time
current = nowdate()  # "2024-01-15"
current_dt = now_datetime()  # datetime object
timestamp = now()  # "2024-01-15 10:30:00"

# Date arithmetic
next_week = add_days(nowdate(), 7)
next_month = add_months(nowdate(), 1)
last_year = add_years(nowdate(), -1)

# Date difference
days = date_diff(end_date, start_date)
seconds = time_diff_in_seconds(end_time, start_time)

# First/last day of month
first = get_first_day(nowdate())
last = get_last_day(nowdate())

# Parse dates
date_obj = getdate("2024-01-15")
dt_obj = get_datetime("2024-01-15 10:30:00")

# Format dates
formatted = formatdate("2024-01-15", "dd-MM-yyyy")
```

#### Numbers
```python
from frappe.utils import (
    flt, cint, cstr,
    fmt_money, rounded,
    money_in_words
)

# Type conversion with defaults
num = flt(value)  # float, None -> 0.0
num = flt(value, 2)  # with precision
integer = cint(value)  # int, None -> 0
string = cstr(value)  # string, None -> ""

# Formatting
formatted = fmt_money(1234.56, currency="USD")  # "$1,234.56"
rounded_val = rounded(1234.567, 2)  # 1234.57
words = money_in_words(1234.56, "USD")  # "One Thousand..."
```

#### Strings
```python
from frappe.utils import (
    strip_html, strip_html_tags,
    escape_html, sanitize_html,
    scrub, unscrub
)

# HTML handling
plain = strip_html("<p>Hello</p>")  # "Hello"
safe = escape_html("<script>bad</script>")

# Field name conversion
field = scrub("My Field Name")  # "my_field_name"
label = unscrub("my_field_name")  # "My Field Name"
```

### Messaging & Notifications

```python
# Show message (appears as toast)
frappe.msgprint("Document saved successfully")

# With indicator
frappe.msgprint("Error occurred", indicator="red", title="Error")

# Throw error (stops execution)
frappe.throw("Invalid data provided")

# With exception type
from frappe.exceptions import ValidationError
frappe.throw("Validation failed", exc=ValidationError)

# Send email
frappe.sendmail(
    recipients=["user@example.com"],
    subject="Hello",
    message="Email body",
    template="email_template",
    args={"name": "John"}
)

# Create system notification
frappe.publish_realtime(
    "msgprint",
    {"message": "Task completed"},
    user="user@example.com"
)
```

### Background Jobs

```python
# Enqueue background job
frappe.enqueue(
    "myapp.tasks.heavy_task",
    queue="long",
    timeout=600,
    job_name="Heavy Task",
    customer="CUST-001"
)

# In tasks.py
def heavy_task(customer):
    # Long running task
    process_customer(customer)

# Enqueue with callback
frappe.enqueue(
    method=process_data,
    queue="default",
    on_success=on_complete,
    on_failure=on_error
)

# Scheduled jobs (in hooks.py)
scheduler_events = {
    "daily": [
        "myapp.tasks.daily_task"
    ],
    "hourly": [
        "myapp.tasks.hourly_task"
    ],
    "cron": {
        "0 0 * * *": [  # Midnight
            "myapp.tasks.midnight_task"
        ]
    }
}
```

### Session & User

```python
# Current user
user = frappe.session.user

# Check if logged in
if frappe.session.user != "Guest":
    pass

# Check permissions
if frappe.has_permission("Customer", "write"):
    pass

# Get user info
user_doc = frappe.get_doc("User", frappe.session.user)
full_name = frappe.utils.get_fullname(frappe.session.user)

# Check roles
if "System Manager" in frappe.get_roles():
    pass

# Run as different user
frappe.set_user("Administrator")
# ... do operations
frappe.set_user(original_user)
```

## JavaScript API

### Document Operations

```javascript
// Get document
frappe.call({
    method: 'frappe.client.get',
    args: {
        doctype: 'Customer',
        name: 'CUST-001'
    },
    callback: function(r) {
        console.log(r.message);
    }
});

// Create document
frappe.call({
    method: 'frappe.client.insert',
    args: {
        doc: {
            doctype: 'Customer',
            customer_name: 'New Customer'
        }
    },
    callback: function(r) {
        console.log('Created:', r.message.name);
    }
});

// Save document
frappe.call({
    method: 'frappe.client.save',
    args: {
        doc: cur_frm.doc
    }
});

// Delete document
frappe.call({
    method: 'frappe.client.delete',
    args: {
        doctype: 'Customer',
        name: 'CUST-001'
    }
});
```

### frappe.call (API Calls)

```javascript
// Call whitelisted method
frappe.call({
    method: 'myapp.api.get_customer_details',
    args: {
        customer: 'CUST-001'
    },
    freeze: true,
    freeze_message: 'Loading...',
    callback: function(r) {
        if (r.message) {
            console.log(r.message);
        }
    },
    error: function(r) {
        frappe.msgprint('Error occurred');
    }
});

// Async/await pattern
async function getCustomer(name) {
    const response = await frappe.call({
        method: 'myapp.api.get_customer',
        args: { name }
    });
    return response.message;
}

// Call with promise
frappe.call({
    method: 'myapp.api.process',
    args: { data: 'test' }
}).then(r => {
    console.log(r.message);
});
```

### Form API (cur_frm)

```javascript
frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        // Add custom button
        frm.add_custom_button('Process', function() {
            // Button action
        }, 'Actions');

        // Set field properties
        frm.set_df_property('field_name', 'read_only', 1);
        frm.set_df_property('field_name', 'hidden', 1);
        frm.set_df_property('field_name', 'reqd', 1);

        // Set query for link field
        frm.set_query('customer', function() {
            return {
                filters: {
                    status: 'Active'
                }
            };
        });

        // Toggle fields
        frm.toggle_display('field_name', frm.doc.show_field);
        frm.toggle_reqd('field_name', frm.doc.is_required);
    },

    customer: function(frm) {
        // Field change handler
        if (frm.doc.customer) {
            frappe.call({
                method: 'myapp.api.get_customer_details',
                args: { customer: frm.doc.customer },
                callback: function(r) {
                    frm.set_value('customer_name', r.message.name);
                }
            });
        }
    },

    validate: function(frm) {
        // Validate before save
        if (!frm.doc.customer) {
            frappe.throw('Customer is required');
            return false;
        }
    },

    before_save: function(frm) {
        // Before save actions
        frm.doc.modified_by_script = 1;
    },

    after_save: function(frm) {
        // After save actions
        frappe.show_alert('Document saved!');
    }
});

// Child table events
frappe.ui.form.on('Sales Invoice Item', {
    qty: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.amount = row.qty * row.rate;
        frm.refresh_field('items');
    },

    items_add: function(frm, cdt, cdn) {
        // New row added
        let row = locals[cdt][cdn];
        row.warehouse = frm.doc.default_warehouse;
    },

    items_remove: function(frm) {
        // Row removed - recalculate totals
        calculate_totals(frm);
    }
});
```

### Dialogs

```javascript
// Simple prompt
frappe.prompt(
    {fieldname: 'name', fieldtype: 'Data', label: 'Name', reqd: 1},
    function(values) {
        console.log(values.name);
    },
    'Enter Name'
);

// Multiple fields
frappe.prompt([
    {fieldname: 'name', fieldtype: 'Data', label: 'Name', reqd: 1},
    {fieldname: 'email', fieldtype: 'Data', label: 'Email', options: 'Email'},
    {fieldname: 'date', fieldtype: 'Date', label: 'Date', default: frappe.datetime.nowdate()}
], function(values) {
    console.log(values);
}, 'Enter Details', 'Submit');

// Custom dialog
let dialog = new frappe.ui.Dialog({
    title: 'My Dialog',
    fields: [
        {fieldname: 'customer', fieldtype: 'Link', options: 'Customer', label: 'Customer'},
        {fieldname: 'amount', fieldtype: 'Currency', label: 'Amount'}
    ],
    primary_action_label: 'Submit',
    primary_action: function(values) {
        console.log(values);
        dialog.hide();
    }
});
dialog.show();

// Confirmation
frappe.confirm(
    'Are you sure you want to proceed?',
    function() {
        // Yes
        process_action();
    },
    function() {
        // No
    }
);
```

### Utilities

```javascript
// Messages
frappe.msgprint('Hello World');
frappe.msgprint({
    title: 'Success',
    message: 'Operation completed',
    indicator: 'green'
});

frappe.throw('Error message');  // Stops execution

frappe.show_alert('Quick notification', 5);  // 5 seconds

// Date/time
frappe.datetime.nowdate();  // "2024-01-15"
frappe.datetime.now_datetime();  // "2024-01-15 10:30:00"
frappe.datetime.add_days('2024-01-15', 7);
frappe.datetime.str_to_obj('2024-01-15');

// Format
frappe.format(1234.56, {fieldtype: 'Currency'});
frappe.format('2024-01-15', {fieldtype: 'Date'});

// Routing
frappe.set_route('Form', 'Customer', 'CUST-001');
frappe.set_route('List', 'Customer');
frappe.set_route('query-report', 'Sales Report');

// Current route
let route = frappe.get_route();
```

## REST API

### Authentication

```bash
# Token-based
curl -X GET "https://site.com/api/resource/Customer" \
  -H "Authorization: token api_key:api_secret"

# Session-based (login first)
curl -X POST "https://site.com/api/method/login" \
  -d "usr=user&pwd=password"
```

### CRUD Operations

```bash
# List
GET /api/resource/Customer?filters=[["status","=","Active"]]&fields=["name","customer_name"]&limit_page_length=10

# Get single
GET /api/resource/Customer/CUST-001

# Create
POST /api/resource/Customer
Content-Type: application/json
{"customer_name": "New Customer", "customer_type": "Company"}

# Update
PUT /api/resource/Customer/CUST-001
Content-Type: application/json
{"customer_name": "Updated Name"}

# Delete
DELETE /api/resource/Customer/CUST-001
```

### Call Methods

```bash
# Call whitelisted method
POST /api/method/myapp.api.get_customer_details
Content-Type: application/json
{"customer": "CUST-001"}
```

### JavaScript Fetch

```javascript
// Using fetch API
async function getCustomers() {
    const response = await fetch('/api/resource/Customer?limit_page_length=10', {
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    return data.data;
}

// POST request
async function createCustomer(customerData) {
    const response = await fetch('/api/resource/Customer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(customerData)
    });
    return response.json();
}
```
