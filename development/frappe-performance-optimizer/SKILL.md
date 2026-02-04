---
name: frappe-performance-optimizer
description: Generate optimized queries, caching, and indexes for Frappe performance. Use when optimizing slow queries, implementing caching, or improving performance.
---

# Frappe Performance Optimizer

Generate performance-optimized code including efficient queries, caching strategies, and database indexes for Frappe applications.

## When to Use This Skill

Claude should invoke this skill when:
- User reports slow queries or performance issues
- User wants to add caching
- User needs database indexing
- User mentions performance, optimization, or slow queries
- User wants to eliminate N+1 queries

## Capabilities

### 1. Query Optimization

**Optimized Report Query:**
```python
# Efficient query with proper indexing
def get_sales_summary(from_date, to_date):
    return frappe.db.sql("""
        SELECT
            si.customer,
            c.customer_name,
            c.customer_group,
            COUNT(si.name) as invoice_count,
            SUM(si.grand_total) as total_amount
        FROM `tabSales Invoice` si
        INNER JOIN `tabCustomer` c ON c.name = si.customer
        WHERE si.posting_date BETWEEN %s AND %s
            AND si.docstatus = 1
        GROUP BY si.customer
        ORDER BY total_amount DESC
        LIMIT 100
    """, (from_date, to_date), as_dict=True)

# Add index for performance
frappe.db.add_index('Sales Invoice', ['customer', 'posting_date', 'docstatus'])
```

### 2. Caching Implementation

**Cache Expensive Calculations:**
```python
def get_item_price(item_code, price_list, customer=None):
    """Get price with caching"""
    cache_key = f"price:{item_code}:{price_list}:{customer or 'default'}"

    # Try cache
    cached_price = frappe.cache().get_value(cache_key)
    if cached_price is not None:
        return cached_price

    # Calculate price (expensive)
    price = frappe.db.get_value('Item Price',
        filters={'item_code': item_code, 'price_list': price_list},
        fieldname='price_list_rate'
    )

    # Cache for 1 hour
    if price:
        frappe.cache().set_value(cache_key, price, expires_in_sec=3600)

    return price
```

### 3. Batch Operations

**Bulk Update Pattern:**
```python
def bulk_update_items(updates):
    """Update multiple items efficiently"""
    # updates = [{'item_code': 'ITEM-001', 'is_active': 1}, ...]

    # Build single query
    item_codes = [u['item_code'] for u in updates]

    frappe.db.sql("""
        UPDATE `tabItem`
        SET is_active = 1,
            modified = NOW(),
            modified_by = %s
        WHERE name IN %s
    """, (frappe.session.user, tuple(item_codes)))

    frappe.db.commit()
```

## References

**Performance Examples:**
- Stock Ledger: https://github.com/frappe/erpnext/blob/develop/erpnext/stock/stock_ledger.py
- Get Item Details: https://github.com/frappe/erpnext/blob/develop/erpnext/stock/get_item_details.py
