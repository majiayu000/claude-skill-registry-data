---
name: splynx-api
description: |
  Splynx REST API client for validated operations on ISP management data.
  Use when creating, updating, or deleting customers, services, tariffs, invoices, documents, or tickets in Splynx.
  Validates data before writing. Reference: src/apis/splynx_client.py
---

# Splynx REST API

REST API client for Splynx ISP management platform.

## Authentication

```python
import base64

# HTTP Basic Auth
credentials = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()
headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
```

**Environment variables:**
- `SPLYNX_URL` - Base URL (e.g., `http://localhost` or `https://splynx.example.com`)
- `SPLYNX_API_KEY` - API key
- `SPLYNX_PASSWORD` - API secret/password

**Base endpoint:** `{SPLYNX_URL}/api/2.0/`

## Using the Client

```python
from src.apis.splynx_client import SplynxAPIClient, SplynxConfig
from src.config.settings import config

splynx_config = SplynxConfig(
    base_url=config.splynx_url,
    api_key=config.splynx_api_key,
    api_secret=config.splynx_password
)
client = SplynxAPIClient(splynx_config)

# Test connection
result = client.test_connection()
if result['success']:
    print("Connected!")
```

## Request Methods

```python
# GET - Retrieve data
result = client.get('admin/tariffs/internet', params={'limit': 100})

# POST - Create new record
result = client.post('admin/tariffs/internet', data={'title': 'Basic Plan', 'price': 49.99})

# PUT - Update existing record
result = client.put('admin/customers/customer/123', data={'name': 'Updated Name'})

# DELETE - Remove record
result = client.delete('admin/tariffs/internet/456')

# OPTIONS - Get schema/metadata
result = client.options('admin/tariffs/internet')

# POST Multipart - File upload
result = client.post_multipart('admin/customers/customer-documents/123--upload',
    files={'file': ('doc.pdf', content, 'application/pdf')})
```

## Response Format

All methods return:
```python
{
    'success': True,           # or False
    'status_code': 200,        # HTTP status code
    'data': {...},             # On success
    'error': {...}             # On failure
}
```

## Working Endpoints

### Tariffs (Full CRUD)
```python
# Internet tariffs
client.get('admin/tariffs/internet')
client.post('admin/tariffs/internet', {'title': 'Plan', 'price': 50})
client.put('admin/tariffs/internet/1', {'price': 55})
client.delete('admin/tariffs/internet/1')

# Voice tariffs
client.get('admin/tariffs/voice')
client.post('admin/tariffs/voice', {...})

# Bundle tariffs
client.get('admin/tariffs/bundle')
client.post('admin/tariffs/bundle', {...})

# One-time tariffs
client.get('admin/tariffs/one-time')
client.post('admin/tariffs/one-time', {...})

# Recurring tariffs
client.get('admin/tariffs/recurring')
```

### Networking
```python
# Routers
client.get('admin/networking/routers')
client.get('admin/networking/routers/1')
client.put('admin/networking/routers/1', {'title': 'Main Router'})
```

### Documents
```python
# Create document record
result = client.post('admin/customers/customer-documents', {
    'customer_id': 123,
    'type': 'uploaded',
    'title': 'Contract',
    'description': 'Service agreement'
})
doc_id = result['data']['id']

# Upload file content
client.post_multipart(f'admin/customers/customer-documents/{doc_id}--upload',
    files={'file': ('contract.pdf', pdf_bytes, 'application/pdf')})
```

### Administration
```python
# API check
client.get('admin/api/check')

# Administrators
client.get('admin/administration/administrators')
client.post('admin/administration/administrators', {...})

# Custom fields
client.get('admin/config/additional-fields/customers')
client.post('admin/config/additional-fields/customers', {...})
```

## Restricted Endpoints (May Return 403)

These require additional API permissions:

```python
# Customers - often restricted
client.get('admin/customers/customer')
client.post('admin/customers/customer', {...})

# Finance - often restricted
client.get('admin/finance/invoices')
client.get('admin/finance/payments')
client.get('admin/finance/transactions')

# Tickets - often restricted
client.get('admin/support/tickets')
```

**Workaround:** Use direct MySQL for restricted operations (faster anyway).

## Pagination

```python
# First page
result = client.get('admin/tariffs/internet', params={'limit': 100, 'offset': 0})

# Next page
result = client.get('admin/tariffs/internet', params={'limit': 100, 'offset': 100})

# Fetch all
all_items = []
offset = 0
while True:
    result = client.get('admin/tariffs/internet', params={'limit': 100, 'offset': offset})
    if not result['success'] or not result['data']:
        break
    all_items.extend(result['data'])
    if len(result['data']) < 100:
        break
    offset += 100
```

## File Upload Pattern

```python
from src.apis.splynx_client import SplynxAPIClient

def upload_document(client, customer_id, filename, content, mime_type):
    # Step 1: Create document record
    doc_result = client.post('admin/customers/customer-documents', {
        'customer_id': customer_id,
        'type': 'uploaded',
        'title': filename,
        'visible_by_customer': '0'
    })

    if not doc_result['success']:
        return None

    doc_id = doc_result['data']['id']

    # Step 2: Upload file content
    upload_result = client.post_multipart(
        f'admin/customers/customer-documents/{doc_id}--upload',
        files={'file': (filename, content, mime_type)}
    )

    if not upload_result['success']:
        # Rollback on failure
        client.delete(f'admin/customers/customer-documents/{doc_id}')
        return None

    return doc_id
```

## Error Handling

```python
result = client.post('admin/tariffs/internet', tariff_data)

if result['success']:
    tariff_id = result['data']['id']
    print(f"Created tariff {tariff_id}")
else:
    error = result.get('error', {})
    status = result.get('status_code')

    if status == 403:
        print("Permission denied - check API permissions")
    elif status == 404:
        print("Endpoint not found")
    elif status == 422:
        print(f"Validation error: {error}")
    else:
        print(f"Error {status}: {error}")
```

## Customer Operations (via PUT)

Customers are typically created via MySQL, but updated via API:

```python
# Update customer (set portal password)
result = client.put(f'admin/customers/customer/{customer_id}', {
    'id': customer_id,
    'name': 'John Doe',
    'login': 'johndoe',
    'password': 'new_password',
    'password_confirm': 'new_password'
})
```

## Schema Discovery

```python
# Get field definitions for an endpoint
schema = client.options('admin/tariffs/internet')
if schema['success']:
    fields = schema['data']
    for field_name, field_info in fields.items():
        print(f"{field_name}: {field_info.get('type')}")
```

## When to Use API vs MySQL

| Use API | Use MySQL |
|---------|-----------|
| Creating documents | Bulk customer imports |
| Setting passwords | Reading large datasets |
| Validated writes | Invoice/payment inserts |
| Schema discovery | Service assignments |
| Router updates | Custom field values |

## Reference

- Client implementation: `src/apis/splynx_client.py`
- Config: `src/config/settings.py`
- Test: `python -c "from src.apis.splynx_client import SplynxAPIClient, SplynxConfig; from src.config.settings import config; c = SplynxAPIClient(SplynxConfig(config.splynx_url, config.splynx_api_key, config.splynx_password)); print(c.test_connection())"`
