---
name: frappe-report-generator
description: Generate custom reports, query reports, and script reports for Frappe applications. Use when creating data analysis and reporting features.
---

# Frappe Report Generator Skill

Create custom reports for data analysis, dashboards, and business intelligence in Frappe.

## When to Use This Skill

Claude should invoke this skill when:
- User wants to create custom reports
- User needs data analysis or aggregation
- User asks about query reports or script reports
- User wants to build dashboards
- User needs help with report formatting or filters

## Capabilities

### 1. Report Types

**Query Report (SQL-based):**
- Fast performance for large datasets
- Direct SQL queries
- Complex joins and aggregations
- Limited formatting options

**Script Report (Python-based):**
- Full Python flexibility
- Complex business logic
- Dynamic columns and formatting
- Access to Frappe ORM

**Report Builder (No-code):**
- User-configurable
- No coding required
- Basic aggregations
- Simple use cases

### 2. Query Report Structure

**Basic Query Report JSON:**
```json
{
  "name": "Sales Analysis",
  "report_name": "Sales Analysis",
  "ref_doctype": "Sales Order",
  "report_type": "Query Report",
  "is_standard": "Yes",
  "module": "Selling",
  "disabled": 0,
  "query": "",
  "filters": [],
  "columns": []
}
```

**Python File (sales_analysis.py):**
```python
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "sales_order",
            "label": _("Sales Order"),
            "fieldtype": "Link",
            "options": "Sales Order",
            "width": 150
        },
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150
        },
        {
            "fieldname": "posting_date",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "grand_total",
            "label": _("Grand Total"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100
        }
    ]

def get_data(filters):
    conditions = get_conditions(filters)

    query = f"""
        SELECT
            so.name as sales_order,
            so.customer,
            so.posting_date,
            so.grand_total,
            so.status
        FROM
            `tabSales Order` so
        WHERE
            so.docstatus = 1
            {conditions}
        ORDER BY
            so.posting_date DESC
    """

    return frappe.db.sql(query, filters, as_dict=1)

def get_conditions(filters):
    conditions = []

    if filters.get("customer"):
        conditions.append("so.customer = %(customer)s")

    if filters.get("from_date"):
        conditions.append("so.posting_date >= %(from_date)s")

    if filters.get("to_date"):
        conditions.append("so.posting_date <= %(to_date)s")

    if filters.get("status"):
        conditions.append("so.status = %(status)s")

    return " AND " + " AND ".join(conditions) if conditions else ""
```

### 3. Script Report Structure

**Advanced Script Report:**
```python
import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    report_summary = get_report_summary(data)

    return columns, data, None, chart, report_summary

def get_columns():
    return [
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150
        },
        {
            "fieldname": "total_orders",
            "label": _("Total Orders"),
            "fieldtype": "Int",
            "width": 100
        },
        {
            "fieldname": "total_amount",
            "label": _("Total Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "avg_order_value",
            "label": _("Avg Order Value"),
            "fieldtype": "Currency",
            "width": 120
        }
    ]

def get_data(filters):
    # Get sales orders
    sales_orders = frappe.get_all(
        "Sales Order",
        filters={
            "docstatus": 1,
            "posting_date": ["between", [filters.get("from_date"), filters.get("to_date")]]
        },
        fields=["customer", "grand_total"]
    )

    # Aggregate by customer
    customer_data = {}
    for order in sales_orders:
        customer = order.customer
        if customer not in customer_data:
            customer_data[customer] = {
                "customer": customer,
                "total_orders": 0,
                "total_amount": 0
            }

        customer_data[customer]["total_orders"] += 1
        customer_data[customer]["total_amount"] += flt(order.grand_total)

    # Calculate averages
    data = []
    for customer, values in customer_data.items():
        data.append({
            "customer": customer,
            "total_orders": values["total_orders"],
            "total_amount": values["total_amount"],
            "avg_order_value": values["total_amount"] / values["total_orders"]
        })

    return sorted(data, key=lambda x: x["total_amount"], reverse=True)

def get_chart_data(data):
    """Generate chart for report"""
    if not data:
        return None

    labels = [d["customer"] for d in data[:10]]  # Top 10
    values = [d["total_amount"] for d in data[:10]]

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Total Sales",
                    "values": values
                }
            ]
        },
        "type": "bar",
        "colors": ["#7cd6fd"]
    }

def get_report_summary(data):
    """Generate summary cards"""
    if not data:
        return []

    total_customers = len(data)
    total_revenue = sum(d["total_amount"] for d in data)
    total_orders = sum(d["total_orders"] for d in data)
    avg_order_value = total_revenue / total_orders if total_orders else 0

    return [
        {
            "value": total_customers,
            "label": "Total Customers",
            "datatype": "Int"
        },
        {
            "value": total_revenue,
            "label": "Total Revenue",
            "datatype": "Currency"
        },
        {
            "value": total_orders,
            "label": "Total Orders",
            "datatype": "Int"
        },
        {
            "value": avg_order_value,
            "label": "Avg Order Value",
            "datatype": "Currency"
        }
    ]
```

### 4. Report Filters

**Filter Definition (JSON):**
```json
{
  "filters": [
    {
      "fieldname": "customer",
      "label": "Customer",
      "fieldtype": "Link",
      "options": "Customer"
    },
    {
      "fieldname": "from_date",
      "label": "From Date",
      "fieldtype": "Date",
      "default": "frappe.datetime.month_start()",
      "reqd": 1
    },
    {
      "fieldname": "to_date",
      "label": "To Date",
      "fieldtype": "Date",
      "default": "frappe.datetime.month_end()",
      "reqd": 1
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "options": "\nDraft\nSubmitted\nCancelled",
      "default": "Submitted"
    }
  ]
}
```

### 5. Advanced Query Patterns

**Complex Joins:**
```python
def get_data(filters):
    query = """
        SELECT
            so.name as sales_order,
            so.customer,
            c.customer_group,
            c.territory,
            so.posting_date,
            SUM(soi.amount) as total_amount,
            COUNT(soi.name) as total_items
        FROM
            `tabSales Order` so
        INNER JOIN
            `tabCustomer` c ON so.customer = c.name
        INNER JOIN
            `tabSales Order Item` soi ON soi.parent = so.name
        WHERE
            so.docstatus = 1
            AND so.posting_date BETWEEN %(from_date)s AND %(to_date)s
        GROUP BY
            so.name
        ORDER BY
            total_amount DESC
    """

    return frappe.db.sql(query, filters, as_dict=1)
```

**Aggregations:**
```python
def get_summary_data(filters):
    query = """
        SELECT
            MONTH(posting_date) as month,
            YEAR(posting_date) as year,
            COUNT(name) as order_count,
            SUM(grand_total) as total_sales,
            AVG(grand_total) as avg_order_value,
            MIN(grand_total) as min_order,
            MAX(grand_total) as max_order
        FROM
            `tabSales Order`
        WHERE
            docstatus = 1
            AND posting_date BETWEEN %(from_date)s AND %(to_date)s
        GROUP BY
            YEAR(posting_date), MONTH(posting_date)
        ORDER BY
            year DESC, month DESC
    """

    return frappe.db.sql(query, filters, as_dict=1)
```

### 6. Dynamic Columns

```python
def get_columns():
    """Generate columns dynamically based on data"""
    base_columns = [
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150
        }
    ]

    # Add month columns dynamically
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for month in months:
        base_columns.append({
            "fieldname": month.lower(),
            "label": _(month),
            "fieldtype": "Currency",
            "width": 100
        })

    base_columns.append({
        "fieldname": "total",
        "label": _("Total"),
        "fieldtype": "Currency",
        "width": 120
    })

    return base_columns
```

### 7. Report Formatting

**Conditional Formatting:**
```python
def get_data(filters):
    data = # ... get data

    for row in data:
        # Add indicator
        if row.grand_total > 100000:
            row["indicator"] = "green"
        elif row.grand_total > 50000:
            row["indicator"] = "orange"
        else:
            row["indicator"] = "red"

    return data
```

### 8. Export Features

Reports automatically support:
- Excel export
- PDF export
- CSV export
- Print view

### 9. Performance Optimization

**Use Indexes:**
```python
# Ensure proper indexes exist
# ALTER TABLE `tabSales Order` ADD INDEX idx_posting_date (posting_date);
# ALTER TABLE `tabSales Order` ADD INDEX idx_customer (customer);
```

**Limit Results:**
```python
def get_data(filters):
    # Add LIMIT for large datasets
    query = f"""
        SELECT ...
        FROM ...
        WHERE ...
        LIMIT 1000
    """
    return frappe.db.sql(query, filters, as_dict=1)
```

**Use Query Caching:**
```python
def get_data(filters):
    cache_key = f"sales_report_{filters.get('from_date')}_{filters.get('to_date')}"

    data = frappe.cache().get_value(cache_key)
    if data:
        return data

    data = frappe.db.sql(query, filters, as_dict=1)
    frappe.cache().set_value(cache_key, data, expires_in_sec=300)

    return data
```

### 10. Report Permissions

**Permission Query:**
```python
def get_data(filters):
    # Only show data user has permission to see
    if not frappe.has_permission("Sales Order", "read"):
        frappe.throw(_("Not permitted"))

    # Filter by user permissions
    user_customers = frappe.get_list(
        "Customer",
        filters={"name": ["in", frappe.get_roles()]},
        pluck="name"
    )

    if user_customers:
        filters["customer"] = ["in", user_customers]
```

## File Structure

Reports should be organized as:
```
apps/<app_name>/<module>/report/<report_name>/
├── __init__.py
├── <report_name>.json
├── <report_name>.py
└── <report_name>.js (optional, for client-side customization)
```

## Best Practices

1. **Optimize queries** - Use proper indexes and LIMIT
2. **Filter early** - Apply filters in WHERE clause, not in Python
3. **Use parameterized queries** - Prevent SQL injection
4. **Cache when possible** - Cache expensive calculations
5. **Validate filters** - Always validate user inputs
6. **Handle permissions** - Check user permissions
7. **Provide defaults** - Set sensible default filters
8. **Document reports** - Add helpful descriptions
9. **Test with large data** - Ensure performance at scale
10. **Use chart/summary wisely** - Enhance user experience

## Testing Reports

Access reports at:
```
http://localhost:8000/app/query-report/Sales%20Analysis
```

Remember: This skill is model-invoked. Claude will use it autonomously when detecting report development tasks.
