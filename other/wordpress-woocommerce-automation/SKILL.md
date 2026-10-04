---
name: wordpress-woocommerce-automation
description: Automate WordPress and WooCommerce operations via REST API. Use when managing products, orders, content, or site configuration programmatically. Triggers on requests to create/update products, manage inventory, generate Elementor layouts, handle WooCommerce orders, or automate any WordPress operations. Includes Elementor JSON generation patterns for skyyrose.co.
---

# WordPress WooCommerce Automation

Programmatic control of WordPress and WooCommerce via REST API.

## Authentication Setup

```python
import requests
from requests.auth import HTTPBasicAuth

class WPClient:
    # CANON: skyyrose.co (WP.com Atomic) returns 401 on /wp-json/ paths. The
    # ?rest_route= query-param form is MANDATORY (project CLAUDE.md). Pass the
    # bare route as `endpoint`, e.g. "wc/v3/products" → {site}/?rest_route=/wc/v3/products.
    def __init__(self, site_url: str, username: str, app_password: str):
        self.site_url = site_url.rstrip("/")
        self.auth = HTTPBasicAuth(username, app_password)
        self.headers = {"Content-Type": "application/json"}

    def _url(self, endpoint: str) -> str:
        # requests appends `params` with & since the URL already has a query string.
        return f"{self.site_url}/?rest_route=/{endpoint.lstrip('/')}"

    def get(self, endpoint: str, params: dict = None):
        return requests.get(self._url(endpoint), auth=self.auth, headers=self.headers, params=params)

    def post(self, endpoint: str, data: dict):
        return requests.post(self._url(endpoint), auth=self.auth, headers=self.headers, json=data)

    def put(self, endpoint: str, data: dict):
        return requests.put(self._url(endpoint), auth=self.auth, headers=self.headers, json=data)
```

## WooCommerce Products

### Create Product

```python
def create_product(client: WPClient, product_data: dict) -> dict:
    """
    Required fields: name, type, regular_price
    Optional: description, short_description, categories, images, attributes
    """
    response = client.post("wc/v3/products", product_data)
    return response.json()

# Example: SkyyRose product
product = {
    "name": "BLACK ROSE HEAVYWEIGHT TEE",
    "type": "variable",  # or "simple"
    "regular_price": "85.00",
    "description": "Built for those who move through darkness like it's home.",
    "short_description": "Double-stitched seams. 280gsm cotton. Oakland-made mentality.",
    "categories": [{"id": 15}],  # BLACK ROSE category ID
    "images": [{"src": "https://skyyrose.co/wp-content/uploads/black-rose-tee.jpg"}],
    "attributes": [
        {
            "name": "Size",
            "visible": True,
            "variation": True,
            "options": ["S", "M", "L", "XL", "2XL"]
        },
        {
            "name": "Color",
            "visible": True,
            "variation": True,
            "options": ["Void Black", "Charcoal"]
        }
    ]
}
```

### Product Variations

```python
def create_variation(client: WPClient, product_id: int, variation: dict) -> dict:
    return client.post(f"wc/v3/products/{product_id}/variations", variation).json()

variation = {
    "regular_price": "85.00",
    "attributes": [
        {"name": "Size", "option": "L"},
        {"name": "Color", "option": "Void Black"}
    ],
    "stock_quantity": 25,
    "manage_stock": True
}
```

### Bulk Operations

```python
def batch_update_products(client: WPClient, updates: list[dict]) -> dict:
    """Update multiple products in one request."""
    return client.post("wc/v3/products/batch", {
        "update": updates
    }).json()

# Example: Update inventory for multiple products
updates = [
    {"id": 123, "stock_quantity": 50},
    {"id": 124, "stock_quantity": 30},
    {"id": 125, "stock_status": "outofstock"}
]
```

## WooCommerce Orders

```python
def get_orders(client: WPClient, status: str = "processing", per_page: int = 20):
    return client.get("wc/v3/orders", {
        "status": status,
        "per_page": per_page
    }).json()

def update_order_status(client: WPClient, order_id: int, status: str):
    return client.put(f"wc/v3/orders/{order_id}", {
        "status": status
    }).json()
```

## WordPress Content

### Posts and Pages

```python
def create_post(client: WPClient, title: str, content: str, status: str = "draft"):
    return client.post("wp/v2/posts", {
        "title": title,
        "content": content,
        "status": status
    }).json()

def update_page(client: WPClient, page_id: int, content: str):
    return client.put(f"wp/v2/pages/{page_id}", {
        "content": content
    }).json()
```

### Media Upload

```python
def upload_media(client: WPClient, file_path: str, alt_text: str = ""):
    with open(file_path, "rb") as f:
        filename = os.path.basename(file_path)
        response = requests.post(
            f"{client.base_url}/wp/v2/media",
            auth=client.auth,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
            data=f.read()
        )
        
        if alt_text and response.ok:
            media_id = response.json()["id"]
            client.put(f"wp/v2/media/{media_id}", {"alt_text": alt_text})
        
        return response.json()
```

## Elementor Integration

Generate Elementor-compatible JSON for page layouts:

```python
def generate_elementor_section(content: dict) -> dict:
    """Generate Elementor section structure."""
    return {
        "id": generate_element_id(),
        "elType": "section",
        "settings": {
            "layout": "full_width",
            "gap": "no",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0"}
        },
        "elements": content.get("columns", [])
    }

def generate_element_id() -> str:
    import random
    import string
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
```

See [references/elementor-json.md](references/elementor-json.md) for complete Elementor JSON patterns.

## Common Endpoints

| Resource | Endpoint | Methods |
|----------|----------|---------|
| Products | `wc/v3/products` | GET, POST, PUT, DELETE |
| Variations | `wc/v3/products/{id}/variations` | GET, POST, PUT, DELETE |
| Orders | `wc/v3/orders` | GET, POST, PUT, DELETE |
| Customers | `wc/v3/customers` | GET, POST, PUT, DELETE |
| Categories | `wc/v3/products/categories` | GET, POST, PUT, DELETE |
| Posts | `wp/v2/posts` | GET, POST, PUT, DELETE |
| Pages | `wp/v2/pages` | GET, POST, PUT, DELETE |
| Media | `wp/v2/media` | GET, POST, PUT, DELETE |

## Error Handling

```python
def safe_request(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": str(e), "status": e.response.status_code}
        except Exception as e:
            return {"success": False, "error": str(e)}
    return wrapper
```

## References

See [references/elementor-json.md](references/elementor-json.md) for Elementor layout patterns.

See [references/woo-schemas.md](references/woo-schemas.md) for WooCommerce data schemas.
