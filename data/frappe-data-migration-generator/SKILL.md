---
name: frappe-data-migration-generator
description: Generate data migration scripts for Frappe. Use when migrating data from legacy systems, transforming data structures, or importing large datasets.
---

# Frappe Data Migration Generator

Generate robust data migration scripts with validation, error handling, and progress tracking for importing data into Frappe.

## When to Use This Skill

Claude should invoke this skill when:
- User wants to migrate data from legacy systems
- User needs to import large CSV/Excel files
- User mentions data migration, ETL, or data import
- User wants to transform data structures
- User needs bulk data operations

## Capabilities

### 1. CSV Import Script

**Production-Ready CSV Importer:**
```python
import csv
import frappe
from frappe.utils import flt, cint, getdate

def import_customers_from_csv(file_path):
    """Import customers with validation and error handling"""
    success = []
    errors = []

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader, start=2):
            try:
                # Validate required fields
                if not row.get('Customer Name'):
                    raise ValueError('Customer name required')

                # Transform data
                customer = {
                    'doctype': 'Customer',
                    'customer_name': row['Customer Name'].strip(),
                    'customer_group': row.get('Customer Group', 'Commercial'),
                    'territory': row.get('Territory', 'All Territories'),
                    'email_id': row.get('Email', '').strip(),
                    'mobile_no': row.get('Phone', '').strip(),
                    'credit_limit': flt(row.get('Credit Limit', 0))
                }

                # Check duplicate
                exists = frappe.db.exists('Customer',
                    {'customer_name': customer['customer_name']})

                if exists:
                    # Update
                    doc = frappe.get_doc('Customer', exists)
                    doc.update(customer)
                    doc.save()
                else:
                    # Insert
                    doc = frappe.get_doc(customer)
                    doc.insert()

                success.append(row['Customer Name'])

                # Commit every 100
                if len(success) % 100 == 0:
                    frappe.db.commit()
                    print(f"Processed {len(success)} records")

            except Exception as e:
                errors.append({'row': idx, 'data': row, 'error': str(e)})

    frappe.db.commit()
    return {'success': success, 'errors': errors}
```

## References

**Frappe Data Import:**
- Data Import: https://github.com/frappe/frappe/blob/develop/frappe/core/doctype/data_import/data_import.py
- CSV Utils: https://github.com/frappe/frappe/blob/develop/frappe/utils/csvutils.py
