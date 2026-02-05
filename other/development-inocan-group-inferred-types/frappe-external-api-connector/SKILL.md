---
name: frappe-external-api-connector
description: Generate code to integrate Frappe with external REST APIs. Use when connecting to third-party services, payment gateways, or external data sources.
---

# Frappe External API Connector

Generate robust API client code for integrating Frappe with external REST APIs, handling authentication, error recovery, and data transformation.

## When to Use This Skill

Claude should invoke this skill when:
- User wants to integrate external REST APIs
- User needs to call third-party services
- User mentions API integration, external system connection
- User wants to integrate payment gateways, shipping APIs, etc.
- User needs OAuth or API key authentication

## Capabilities

### 1. API Client Class

**REST API Client Template:**
```python
import requests
import frappe
from frappe import _

class ExternalAPIClient:
    def __init__(self):
        self.base_url = frappe.conf.get('external_api_url')
        self.api_key = frappe.conf.get('external_api_key')
        self.timeout = 30

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'Frappe/1.0'
        }

    def get(self, endpoint, params=None):
        """GET request with error handling"""
        try:
            response = requests.get(
                f'{self.base_url}/{endpoint}',
                params=params,
                headers=self.get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            frappe.throw(_('Request timeout'))
        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e)
        except Exception as e:
            frappe.log_error(frappe.get_traceback(),
                'External API Error')
            frappe.throw(_('API request failed'))

    def post(self, endpoint, data):
        """POST request"""
        response = requests.post(
            f'{self.base_url}/{endpoint}',
            json=data,
            headers=self.get_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def _handle_http_error(self, error):
        """Handle HTTP errors"""
        status_code = error.response.status_code
        if status_code == 401:
            frappe.throw(_('API authentication failed'))
        elif status_code == 404:
            frappe.throw(_('Resource not found'))
        elif status_code == 429:
            frappe.throw(_('Rate limit exceeded'))
        else:
            frappe.throw(_(f'API error: {status_code}'))
```

### 2. OAuth Integration

**OAuth 2.0 Flow:**
```python
def get_oauth_token():
    """Get OAuth access token with refresh"""
    # Check cache first
    token = frappe.cache().get_value('oauth_token:provider')
    if token:
        return token

    # Get from settings
    settings = frappe.get_single('OAuth Settings')

    response = requests.post(
        settings.token_url,
        data={
            'grant_type': 'client_credentials',
            'client_id': settings.client_id,
            'client_secret': settings.get_password('client_secret')
        }
    )

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']

        # Cache token
        frappe.cache().set_value(
            'oauth_token:provider',
            access_token,
            expires_in_sec=token_data.get('expires_in', 3600) - 60
        )

        return access_token

    frappe.throw(_('OAuth authentication failed'))
```

## References

**Frappe Integration Patterns:**
- Integrations: https://github.com/frappe/frappe/tree/develop/frappe/integrations
- ERPNext Integrations: https://github.com/frappe/erpnext/tree/develop/erpnext/erpnext_integrations
