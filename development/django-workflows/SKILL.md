---
name: "django-workflows"
description: "Master Django-FixiPlug integration workflows. Learn how to build full-stack CRUD applications by orchestrating table, form, state, and fx-attribute plugins together. Essential for working with dj-fixi backends."
tags:
  - "django"
  - "dj-fixi"
  - "crud"
  - "workflows"
  - "orchestration"
  - "full-stack"
  - "backend-integration"
  - "data-management"
version: "1.0.0"
level: "advanced"
author: "FixiPlug Team"
references:
  - "tablePlugin"
  - "formSchemaPlugin"
  - "agentCommands"
  - "stateTrackerPlugin"
  - "fixiAgentPlugin"
---

# Django Integration Workflows Skill

## Overview

This skill teaches you how to build complete Django-FixiPlug applications by **orchestrating multiple plugins together**. You'll learn proven workflow patterns for CRUD operations, table management, form handling, and state synchronization with Django backends.

**Key Principle**: Don't use plugins in isolation - compose them into cohesive workflows.

**What You'll Master**:
1. **Loading Django Tables** - Fetch, render, sort, filter, paginate
2. **CRUD Operations** - Create, Read, Update, Delete with dj-fixi
3. **Form Submission with Validation** - Extract schema, validate, fill, submit
4. **Master-Detail Views** - Coordinated table + detail display
5. **Multi-Step Operations** - State management across async workflows

---

## Core Django Stack

### dj-fixi Backend

**Django View (FxCRUDView)**:
```python
# views.py
from dj_fixi import FxCRUDView
from .models import Product

class ProductView(FxCRUDView):
    model = Product
    fields = ['id', 'name', 'price', 'category', 'in_stock']
    template_name = 'products.html'
```

**URL Configuration**:
```python
# urls.py
from django.urls import path
from .views import ProductView

urlpatterns = [
    path('api/products/', ProductView.as_view(), name='products'),
]
```

**What dj-fixi Provides**:
- `GET /api/products/` - List all products (returns `{data: [...], columns: [...], meta: {}}`)
- `POST /api/products/` - Create new product
- `PATCH /api/products/<id>/` - Update existing product
- `DELETE /api/products/<id>/` - Delete product
- Automatic CSRF handling
- Validation with Django forms
- JSON + HTML responses

---

## Pattern 1: Load Django Table

**Goal**: Fetch Django model data and render as interactive table

### Step-by-Step Workflow

```javascript
// 1. Track loading state
await fixiplug.dispatch('api:setState', {
  state: 'loading',
  data: { operation: 'load-products-table' }
});

// 2. Inject table container with fx-attributes
await fixiplug.dispatch('api:injectFxHtml', {
  html: `
    <div id="products-table"
         fx-table
         fx-action="/api/products/"
         fx-trigger="load"
         fx-table-sortable
         fx-table-search
         fx-page-size="20"
         fx-export-filename="products.csv"
         data-model="Product">
    </div>
  `,
  selector: '#app',
  position: 'innerHTML'
});

// 3. Wait for table to load (fx:after event fires when AJAX completes)
// Listen for the specific action endpoint
ctx.on('fx:after', async (event) => {
  if (event.cfg.action === '/api/products/') {
    // 4. Update state to ready
    await fixiplug.dispatch('api:setState', {
      state: 'table-ready',
      data: {
        model: 'Product',
        endpoint: '/api/products/',
        recordCount: event.detail?.data?.length || 0
      }
    });

    // 5. Query the loaded table data (optional)
    const tableData = await fixiplug.dispatch('agent:queryTable', {
      table: 'products'
    });

    console.log(`Loaded ${tableData.count} products`);
  }
});
```

**What Happens**:
1. State tracker marks app as "loading"
2. Fixi-agent injects HTML with `fx-table` and `fx-action`
3. `fx-trigger="load"` causes immediate GET request to `/api/products/`
4. Django's FxCRUDView returns `{data: [...], columns: [...]}`
5. Table plugin receives `fx:data` event and renders table
6. `fx:after` event fires → state updated to "table-ready"
7. Agent can now query the table data with `agent:queryTable`

**Key Features Enabled**:
- ✅ Sortable columns (click headers)
- ✅ Client-side search (search box auto-injected)
- ✅ Pagination (20 rows per page)
- ✅ CSV export
- ✅ Django model metadata tracking

---

## Pattern 2: CRUD - Create New Record

**Goal**: Display form, validate input, submit to Django, refresh table

### Step-by-Step Workflow

```javascript
// Prerequisite: Table already loaded (Pattern 1)

// 1. Inject "Add Product" button
await fixiplug.dispatch('api:injectFxHtml', {
  html: '<button id="add-product-btn" fx-action="/products/new/" fx-target="#form-modal">Add Product</button>',
  selector: '#toolbar',
  position: 'beforeend'
});

// 2. User clicks button → Django returns form HTML
// (Alternatively, build form on client side if you have the schema)

// Listen for form load
ctx.on('fx:swapped', async (event) => {
  if (event.target.id === 'form-modal') {
    // 3. Extract form schema from Django form
    const schema = await fixiplug.dispatch('api:getFormSchema', {
      form: 'product-form'
    });

    console.log('Django form schema:', schema.schema);

    // 4. Generate sample data (for testing/demo)
    const sample = await fixiplug.dispatch('api:generateSampleData', {
      form: 'product-form'
    });

    console.log('Sample data:', sample.sample);

    // 5. Prepare user data (or use sample)
    const userData = {
      name: 'New Premium Laptop',
      price: 1299.99,
      category: 'Electronics',
      in_stock: true
    };

    // 6. Validate before submitting
    const validation = await fixiplug.dispatch('api:validateFormData', {
      form: 'product-form',
      data: userData
    });

    if (!validation.valid) {
      console.error('Validation failed:', validation.errors);
      // Show errors to user or auto-fix
      return;
    }

    // 7. Fill form
    await fixiplug.dispatch('agent:fillForm', {
      form: 'product-form',
      data: validation.data
    });

    // 8. Submit form
    await fixiplug.dispatch('agent:clickButton', {
      text: 'Save'
    });

    // 9. Wait for submission success
    await fixiplug.dispatch('api:waitForState', {
      state: 'product-created',
      timeout: 5000
    });

    // 10. Refresh table to show new record
    await fixiplug.dispatch('api:triggerFxElement', {
      selector: '#products-table'
    });
  }
});

// Listen for successful creation (Django returns success response)
ctx.on('fx:after', async (event) => {
  if (event.cfg.action.includes('/products/') && event.cfg.method === 'POST') {
    await fixiplug.dispatch('api:setState', {
      state: 'product-created',
      data: { id: event.detail?.id }
    });
  }
});
```

**Django POST Handler** (automatic with FxCRUDView):
```python
# FxCRUDView automatically handles POST:
# 1. Validates data with Django form
# 2. Creates model instance
# 3. Returns JSON: {"id": 123, "success": true}
# 4. Or returns validation errors: {"errors": {"name": ["This field is required"]}}
```

---

## Pattern 3: CRUD - Update Record (Inline Edit)

**Goal**: Double-click table cell → edit → save to Django

### Step-by-Step Workflow

```javascript
// Prerequisite: Table with fx-table-editable enabled

// 1. Load table with editable columns
await fixiplug.dispatch('api:injectFxHtml', {
  html: `
    <div fx-table
         fx-action="/api/products/"
         fx-trigger="load"
         fx-table-editable
         fx-table-save-url="/api/products/">
    </div>
  `,
  selector: '#app'
});

// 2. Django returns columns with editable: true
// Example response:
// {
//   data: [{id: 1, name: "Laptop", price: 999}],
//   columns: [
//     {key: "id", label: "ID", editable: false},
//     {key: "name", label: "Name", editable: true},
//     {key: "price", label: "Price", editable: true, type: "number"}
//   ]
// }

// 3. User double-clicks cell → table plugin shows input
// 4. User edits → presses Enter
// 5. Table plugin sends PATCH request:
//    PATCH /api/products/1/
//    Body: {"column": "price", "value": 1099}

// 6. Listen for successful update
ctx.on('table:cellSaved', (event) => {
  console.log(`Updated ${event.column} to ${event.value} for row ${event.rowId}`);

  // Update app state
  fixiplug.dispatch('api:setState', {
    state: 'product-updated',
    data: {
      id: event.rowId,
      field: event.column,
      newValue: event.value
    }
  });
});

// 7. Handle errors
ctx.on('table:cellSaveError', (event) => {
  console.error(`Failed to update ${event.column}:`, event.error);

  // Show user-friendly error
  alert(`Update failed: ${event.error.message}`);
});
```

**Django PATCH Handler** (automatic with FxCRUDView):
```python
# FxCRUDView handles PATCH /api/products/<id>/
# Request: {"column": "price", "value": 1099}
# Response: {"success": true} or {"error": "Validation failed"}
```

---

## Pattern 4: CRUD - Delete Record

**Goal**: Delete button → confirm → DELETE request → refresh table

### Step-by-Step Workflow

```javascript
// Prerequisite: Table loaded with row IDs

// 1. Add delete buttons to each row (via Django template or client-side)
// Option A: Django template includes delete button
// Option B: Inject buttons client-side after table loads

ctx.on('fx:swapped', async (event) => {
  if (event.target.querySelector('[fx-table]')) {
    // 2. Find all table rows
    const rows = event.target.querySelectorAll('tr[data-row-id]');

    rows.forEach(row => {
      const rowId = row.getAttribute('data-row-id');

      // 3. Inject delete button
      const deleteBtn = document.createElement('button');
      deleteBtn.textContent = 'Delete';
      deleteBtn.className = 'delete-btn';
      deleteBtn.setAttribute('fx-action', `/api/products/${rowId}/`);
      deleteBtn.setAttribute('fx-method', 'DELETE');
      deleteBtn.setAttribute('fx-swap', 'none');

      // Add to row
      const actionsCell = row.querySelector('td:last-child');
      if (actionsCell) {
        actionsCell.appendChild(deleteBtn);
      }
    });

    // 4. Re-process fx-attributes
    event.target.dispatchEvent(new CustomEvent('fx:process', { bubbles: true }));
  }
});

// 5. Listen for delete button clicks (before request)
ctx.on('fx:before', (event) => {
  if (event.cfg.method === 'DELETE' && event.cfg.action.includes('/api/products/')) {
    // 6. Confirm deletion
    const confirmed = confirm('Are you sure you want to delete this product?');

    if (!confirmed) {
      // Cancel the request
      event.preventDefault();
    } else {
      // Track deletion state
      fixiplug.dispatch('api:setState', {
        state: 'deleting',
        data: { endpoint: event.cfg.action }
      });
    }
  }
});

// 7. Listen for successful deletion
ctx.on('fx:after', async (event) => {
  if (event.cfg.method === 'DELETE' && event.cfg.action.includes('/api/products/')) {
    console.log('Product deleted successfully');

    // 8. Update state
    await fixiplug.dispatch('api:setState', {
      state: 'product-deleted',
      data: { id: event.cfg.action.match(/\/api\/products\/(\d+)\//)?.[1] }
    });

    // 9. Refresh table to remove deleted row
    await fixiplug.dispatch('api:triggerFxElement', {
      selector: '[fx-action="/api/products/"]'
    });
  }
});

// 10. Handle errors
ctx.on('fx:error', (event) => {
  if (event.cfg.method === 'DELETE') {
    console.error('Delete failed:', event.detail.error);

    alert('Failed to delete product');

    fixiplug.dispatch('api:setState', {
      state: 'delete-error',
      data: { error: event.detail.error.message }
    });
  }
});
```

**Django DELETE Handler** (automatic with FxCRUDView):
```python
# FxCRUDView handles DELETE /api/products/<id>/
# Response: {"success": true} or {"error": "Cannot delete"}
```

---

## Pattern 5: Master-Detail View

**Goal**: Table of records + detail panel (click row → load details)

### Step-by-Step Workflow

```javascript
// 1. Inject master-detail layout
await fixiplug.dispatch('api:injectFxHtml', {
  html: `
    <div class="master-detail">
      <div class="master">
        <h2>Products</h2>
        <div id="products-list"
             fx-table
             fx-action="/api/products/"
             fx-trigger="load">
        </div>
      </div>
      <div class="detail">
        <h2>Details</h2>
        <div id="product-details">
          <p>Select a product to view details</p>
        </div>
      </div>
    </div>
  `,
  selector: '#app'
});

// 2. Wait for table to load
ctx.on('fx:swapped', async (event) => {
  if (event.target.id === 'products-list') {
    // 3. Make table rows clickable
    const rows = event.target.querySelectorAll('tr[data-row-id]');

    rows.forEach(row => {
      const rowId = row.getAttribute('data-row-id');

      // 4. Add fx-action to load details
      row.setAttribute('fx-action', `/api/products/${rowId}/`);
      row.setAttribute('fx-target', '#product-details');
      row.style.cursor = 'pointer';
    });

    // 5. Re-process to wire up new fx-actions
    event.target.dispatchEvent(new CustomEvent('fx:process', { bubbles: true }));
  }
});

// 6. Track selected product
ctx.on('fx:before', (event) => {
  if (event.cfg.action.match(/\/api\/products\/\d+\//)) {
    fixiplug.dispatch('api:setState', {
      state: 'loading-details',
      data: { productId: event.cfg.action.match(/\d+/)?.[0] }
    });
  }
});

// 7. Details loaded
ctx.on('fx:after', async (event) => {
  if (event.cfg.action.match(/\/api\/products\/\d+\//)) {
    await fixiplug.dispatch('api:setState', {
      state: 'details-loaded',
      data: {
        productId: event.cfg.action.match(/\d+/)?.[0],
        product: event.detail
      }
    });

    console.log('Product details loaded');
  }
});
```

**Django Detail View**:
```python
# views.py
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

# urls.py
path('api/products/<int:pk>/', ProductDetailView.as_view(), name='product-detail')
```

---

## Pattern 6: Search and Filter

**Goal**: Search form → filter table by Django query

### Step-by-Step Workflow

```javascript
// 1. Inject search form + table
await fixiplug.dispatch('api:injectFxHtml', {
  html: `
    <div class="search-interface">
      <form fx-action="/api/products/search/" fx-target="#results">
        <input name="q" placeholder="Search products..." />
        <input name="min_price" type="number" placeholder="Min price" />
        <input name="max_price" type="number" placeholder="Max price" />
        <select name="category">
          <option value="">All categories</option>
          <option value="electronics">Electronics</option>
          <option value="clothing">Clothing</option>
        </select>
        <button type="submit">Search</button>
      </form>
      <div id="results"></div>
    </div>
  `,
  selector: '#app'
});

// 2. Form submits → Django receives query params
// GET /api/products/search/?q=laptop&min_price=500&max_price=2000&category=electronics

// 3. Django filters QuerySet and returns table data
// {
//   data: [...filtered products...],
//   columns: [...],
//   meta: {count: 15, filters: {...}}
// }

// 4. Track search state
ctx.on('fx:before', (event) => {
  if (event.cfg.action === '/api/products/search/') {
    fixiplug.dispatch('api:setState', {
      state: 'searching',
      data: { query: event.cfg.data }
    });
  }
});

// 5. Results returned
ctx.on('fx:after', async (event) => {
  if (event.cfg.action === '/api/products/search/') {
    const resultCount = event.detail?.data?.length || 0;

    await fixiplug.dispatch('api:setState', {
      state: 'search-results',
      data: {
        count: resultCount,
        filters: event.detail?.meta?.filters
      }
    });

    console.log(`Found ${resultCount} results`);
  }
});
```

**Django Search View**:
```python
# views.py
class ProductSearchView(FxCRUDView):
    model = Product
    fields = ['id', 'name', 'price', 'category']

    def get_queryset(self):
        qs = super().get_queryset()

        # Search query
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(name__icontains=q)

        # Price range
        min_price = self.request.GET.get('min_price')
        if min_price:
            qs = qs.filter(price__gte=min_price)

        max_price = self.request.GET.get('max_price')
        if max_price:
            qs = qs.filter(price__lte=max_price)

        # Category
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category=category)

        return qs
```

---

## Best Practices

### ✅ DO

1. **Always track state transitions**
```javascript
await fixiplug.dispatch('api:setState', { state: 'loading' });
// ... perform operation ...
await fixiplug.dispatch('api:setState', { state: 'ready' });
```

2. **Validate before submitting forms**
```javascript
const validation = await fixiplug.dispatch('api:validateFormData', { form, data });
if (validation.valid) {
  await fixiplug.dispatch('agent:fillForm', { form, data });
}
```

3. **Refresh tables after mutations** (Create, Update, Delete)
```javascript
await fixiplug.dispatch('api:triggerFxElement', { selector: '#products-table' });
```

4. **Use fx-trigger="load" for auto-loading**
```javascript
<div fx-action="/api/products/" fx-trigger="load" fx-table></div>
```

5. **Leverage Django's column metadata**
```javascript
// Django defines which columns are editable, sortable, etc.
// Trust the server configuration
```

### ❌ DON'T

1. **Don't bypass validation**
```javascript
// Bad
await fixiplug.dispatch('agent:fillForm', { form, data });

// Good
const validation = await fixiplug.dispatch('api:validateFormData', { form, data });
if (validation.valid) {
  await fixiplug.dispatch('agent:fillForm', { form, data });
}
```

2. **Don't forget CSRF tokens** (dj-fixi handles this automatically)
```javascript
// You don't need to manually add CSRF - dj-fixi does it
```

3. **Don't mix client and server state**
```javascript
// Bad: Storing Django data in global variables
window.products = tableData;

// Good: Query table when needed
const data = await fixiplug.dispatch('agent:queryTable', { table: 'products' });
```

4. **Don't ignore errors**
```javascript
// Always listen for fx:error events
ctx.on('fx:error', (event) => {
  console.error('Request failed:', event.detail.error);
  fixiplug.dispatch('api:setState', { state: 'error', data: event.detail.error });
});
```

---

## Complete Example: Full CRUD App

```javascript
// Initialize complete product management app
async function initializeProductApp() {
  // 1. Set up main layout
  await fixiplug.dispatch('api:injectFxHtml', {
    html: `
      <div id="product-app">
        <div id="toolbar">
          <h1>Product Management</h1>
          <button id="add-btn">Add Product</button>
        </div>
        <div id="products-table"
             fx-table
             fx-action="/api/products/"
             fx-trigger="load"
             fx-table-sortable
             fx-table-search
             fx-table-editable
             fx-table-save-url="/api/products/"
             fx-page-size="20">
        </div>
      </div>
    `,
    selector: '#app'
  });

  // 2. Wait for initial load
  await fixiplug.dispatch('api:waitForState', {
    state: 'table-ready',
    timeout: 10000
  });

  // 3. Set up add button handler
  document.getElementById('add-btn').addEventListener('click', async () => {
    await showCreateForm();
  });

  console.log('Product app initialized');
}

async function showCreateForm() {
  // Create modal with form
  await fixiplug.dispatch('api:injectFxHtml', {
    html: `
      <div id="modal">
        <div fx-action="/products/new/" fx-trigger="load"></div>
      </div>
    `,
    selector: '#product-app',
    position: 'beforeend'
  });

  // Wait for form to load
  await new Promise(resolve => setTimeout(resolve, 500));

  // Get form schema
  const schema = await fixiplug.dispatch('api:getFormSchema', {
    form: 'product-form'
  });

  console.log('Form ready:', schema.schema);
}

// Event listeners for state management
ctx.on('fx:after', async (event) => {
  if (event.cfg.action === '/api/products/') {
    await fixiplug.dispatch('api:setState', { state: 'table-ready' });
  }
});

ctx.on('table:cellSaved', () => {
  console.log('Product updated');
});

ctx.on('fx:error', (event) => {
  console.error('Error:', event.detail.error);
  alert(`Operation failed: ${event.detail.error.message}`);
});

// Initialize app
initializeProductApp();
```

---

## Summary

This skill teaches you to:

1. **Load Django tables** with sorting, filtering, pagination
2. **Create records** with validated forms
3. **Update records** with inline editing
4. **Delete records** with confirmation
5. **Build master-detail views** with coordinated state
6. **Search and filter** with Django QuerySets
7. **Track state** across async operations
8. **Handle errors** gracefully

**Remember**: You're orchestrating 5 plugins (table, form-schema, agent-commands, state-tracker, fixi-agent) to build full-stack Django apps. Each plugin handles one concern - your job is to coordinate them.

