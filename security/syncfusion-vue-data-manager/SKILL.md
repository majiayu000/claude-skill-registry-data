---
name: syncfusion-vue-data-manager
description: Implements Syncfusion Vue DataManager for local/remote binding, CRUD, querying, caching, and middleware. Supports JsonAdaptor, ODataAdaptor, ODataV4Adaptor, UrlAdaptor, WebApiAdaptor, WebMethodAdaptor, RemoteSaveAdaptor, GraphQLAdaptor, CustomDataAdaptor, and CustomAdaptor. Covers Query class, filtering, sorting, paging, grouping, persistence, offline mode, caching, and error handling.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "DataManager"
---

# Syncfusion Vue DataManager: Comprehensive Guide

## When to Use This Skill

Reference this skill when you need to:
- **Set up DataManager** in Vue 2, Vue 3, or Quasar
- **Bind data** (local arrays or remote APIs)
- **Query and filter** data with the Query class
- **CRUD operations** (insert, update, delete)
- **Choose an adaptor** (10 types available)
- **Add authentication** via middleware/headers
- **Optimize performance** with caching
- **Work offline** with data persistence
- **Pattern guidance** for Composition API vs Options API

---

## 🛑 MANDATORY HUMAN GATE: Adaptor Decision (Read This First)

> **This is the most critical rule in this skill. It cannot be skipped or bypassed.**

**When the user provides a service URL without explicitly naming the adaptor type, the agent MUST:**

1. **STOP code generation immediately**
2. **READ:** `references/adaptor-decision-gate.md` (full file)
3. **PRESENT** the gate to the user using the template in that file
4. **WAIT** for explicit user confirmation of the adaptor choice
5. **Only then** proceed to generate `DataManager` code with the confirmed adaptor

### Gate Trigger Conditions — Examples

| User Prompt | Gate Required? |
|-------------|---------------|
| `"Build an employee app using this service URL (http://myapi.com/employees)"` | ✅ YES — no adaptor specified |
| `"Connect GridComponent to http://myserver/api/data"` | ✅ YES — "API" is ambiguous |
| `"Use OData v4 endpoint at https://myserver/odata/employees"` | ❌ NO — OData v4 explicitly stated |
| `"My backend returns { Items, Count } at https://myserver/api/orders"` | ❌ NO — WebApiAdaptor pattern confirmed |
| `"I have a REST service at http://custom-url"` | ✅ YES — REST is ambiguous (UrlAdaptor vs WebApiAdaptor vs ODataV4) |
| `"Bind the grid to local list data"` | ❌ NO — local binding, no adaptor needed |

📄 **Full gate template, adaptor cheat sheet, disambiguation questions, and security rules:**
→ `references/adaptor-decision-gate.md`

---

## ⚠️ Security & Trust Boundary

- This skill generates code only, the agent does not execute data operations or fetch remote endpoints — all DataManager interactions occur solely within the user's application at runtime.
- Generated code must treat all third-party API responses as untrusted input, never bind to unvalidated or user-provided URLs, and ensure authentication is enforced on all remote endpoints.

## ⚠️ Critical Security Requirements

**When binding to remote services, you MUST implement these protections:**

1. **Use HTTPS only** — never use unencrypted HTTP connections; encrypt all data in transit
3. **Use string variables for URLs** — assign endpoints to private string properties rather than hardcoding in markup; this enables centralized validation and easier maintenance
5. **Validate and sanitize responses** — implement server-side schema validation; reject unexpected response formats; map responses to strongly-typed models
6. **Monitor remote calls** — log all external API requests with timestamps, endpoints, and outcomes for security audit trails
7. **Implement CORS securely** — use specific trusted origins only; never use wildcard `*` in production; require HTTPS
8. **Prevent indirect prompt injection attacks** — verify endpoint ownership; implement request signing; validate response content types and schemas before consuming data

**Third-party API responses can introduce security risks.** Always verify endpoint legitimacy, authenticate requests, and validate data before binding to UI components.

## Key Concepts Overview

| Concept | When to Use | Reference |
|---------|-----------|-----------|
| **Setup** | Installing & initial config | setup-vue-2.md, setup-vue-3.md, setup-quasar.md |
| **Data Binding** | Connecting data sources | data-binding.md |
| **Querying** | Filtering, sorting, pagination | querying.md |
| **CRUD** | Insert, update, delete records | crud-operations.md |
| **Adaptors** | Choosing data source type | adaptors-guide.md |
| **Caching** | Performance optimization | caching.md |
| **Middleware** | Authentication, transformation | middleware.md |
| **Headers** | Custom HTTP headers | how-to-headers.md |
| **Parameters** | Send extra query params | how-to-parameters.md |
| **Offline** | Work without internet | how-to-offline.md |

---

## 📊 Framework & API Coverage

| Feature | Vue 2 | Vue 3 | Quasar | Composition | Options |
|---------|-------|-------|--------|-------------|---------|
| Setup | ✅ | ✅ | ✅ | - | ✅ |
| Composition API | - | ✅ | ✅ | ✅ | - |
| Local Data | ✅ | ✅ | ✅ | ✅ | ✅ |
| Remote Data | ✅ | ✅ | ✅ | ✅ | ✅ |
| 10 Adaptors | ✅ | ✅ | ✅ | ✅ | ✅ |
| CRUD | ✅ | ✅ | ✅ | ✅ | ✅ |
| Querying | ✅ | ✅ | ✅ | ✅ | ✅ |
| Caching | ✅ | ✅ | ✅ | ✅ | ✅ |
| Middleware | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 🚀 Quick Start

### Vue 3 Composition API (Recommended)

```typescript
import { onMounted, ref } from 'vue';
import { DataManager, Query, ODataV4Adaptor } from '@syncfusion/ej2-data';

export default {
  setup() {
    const items = ref([]);

    onMounted(async () => {
      const dm = new DataManager({
        url: 'url',
        adaptor: new ODataV4Adaptor()
      });

      try {
        const result = await dm.executeQuery(new Query().take(10));
        items.value = result.result;
      } catch (error) {
        console.error('Error:', error);
      }
    });

    return { items };
  }
}
```

### Vue 2 Options API

```typescript
import { DataManager, Query, ODataV4Adaptor } from '@syncfusion/ej2-data';

export default {
  data() {
    return { items: [] };
  },
  mounted() {
    const dm = new DataManager({
      url: 'url',
      adaptor: new ODataV4Adaptor()
    });

    dm.executeQuery(new Query().take(10))
      .then((result) => {
        this.items = result.result;
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }
}
```

---

## 📖 Documentation Navigation

### 🛑 Adaptor Decision Gate (Human Approval — MANDATORY FIRST STEP for Remote URLs)
📄 **Read:** [references/adaptor-decision-gate.md](references/adaptor-decision-gate.md)
- **When to trigger:** User provides any service URL without explicitly naming the adaptor
- Gate presentation template (copy-paste ready)
- Full adaptor comparison table (ODataV4 / OData / WebAPI / URL / GraphQL / Custom)
- Adaptor quick-reference cheat sheets with code examples
- Disambiguation follow-up questions
- Security rules applied after gate confirmation
- Stage 1 & Stage 3 integration instructions (flags ambiguous URLs in component mapping JSON)
- Keywords that auto-resolve the gate (no user confirmation needed)

### Getting Started (Choose Your Framework)

**New to DataManager? Start here:**

📄 [setup-vue-2.md](references/setup-vue-2.md) — Vue 2 with Options API
- Vue CLI installation
- Vue 2 lifecycle patterns
- First DataManager example

📄 [setup-vue-3.md](references/setup-vue-3.md) — Vue 3 with Composition & Options API
- Vite project setup
- reactive() vs ref()
- onMounted lifecycle
- Performance tips

📄 [setup-quasar.md](references/setup-quasar.md) — Quasar Framework
- Quasar CLI bootstrap
- Boot file configuration
- Q-Grid integration
- Build optimization

---

### Core Features

**Understanding Data Binding:**

📄 [data-binding.md](references/data-binding.md)
- Local data binding (json property)
- Remote data binding (url + adaptor)
- Error handling by HTTP status
- Promise patterns

**Manipulating Data (CRUD):**

📄 [crud-operations.md](references/crud-operations.md)
- insert() — Add new records
- update() — Modify existing records
- remove() — Delete records
- Batch operations with saveChanges()
- keyField in update/remove methods

**Querying & Filtering:**

📄 [querying.md](references/querying.md)
- from() — Specify resource
- select() — Choose fields
- where() — Filter conditions
- orderBy() — Sorting
- take/skip — Pagination
- search() — Full-text search
- group() — Data grouping

---

### Data Adaptors (10 Types)

**Selecting the Right Adaptor:**

📄 [adaptors-guide.md](references/adaptors-guide.md)
- **JsonAdaptor** — Local in-memory arrays
- **ODataAdaptor** — OData v3 services
- **ODataV4Adaptor** — OData v4 endpoints
- **UrlAdaptor** — Generic REST APIs
- **WebApiAdaptor** — ASP.NET Web API (Items, Count format)
- **WebMethodAdaptor** — ASP.NET web methods
- **RemoteSaveAdaptor** — Client queries + server CRUD
- **GraphQLAdaptor** — GraphQL endpoints
- **CustomDataAdaptor** — Custom request/response
- **CustomAdaptor** — Extend built-in adaptors

Includes decision tree and comparison matrix.

---

### Advanced Features

**Performance Optimization:**

📄 [caching.md](references/caching.md)
- enableCache property
- How caching works
- Auto-clearing rules
- When to enable/disable

**Request Customization:**

📄 [middleware.md](references/middleware.md)
- applyPreRequestMiddlewares() — Modify requests
- applyPostRequestMiddlewares() — Transform responses
- Adding custom headers
- Authentication token injection

---

### How-To Guides

**Quick Solutions for Common Tasks:**

📄 [how-to-headers.md](references/how-to-headers.md)
- Adding static headers
- Dynamic headers per request
- JWT/Bearer authentication
- Content negotiation

📄 [how-to-parameters.md](references/how-to-parameters.md)
- Sending additional query parameters
- Custom API formats
- Different adaptor parameter styles

📄 [how-to-offline.md](references/how-to-offline.md)
- Enabling offline mode
- localStorage persistence
- Sync strategies
- Conflict resolution

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

---

## 🎯 Common Patterns

### Local Data Binding

```typescript
// Vue 3 Composition API
import { ref } from 'vue';
import { DataManager, Query, JsonAdaptor } from '@syncfusion/ej2-data';

const items = ref([]);

const data = [
  { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 },
  { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61 }
];

const dm = new DataManager({ json: data, adaptor: new JsonAdaptor() });
items.value = dm.executeLocal(new Query().take(10));
```

### Remote Data with Error Handling

```typescript
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

dataManager.executeQuery(new Query().take(10))
  .then((result) => {
    console.log('Success:', result.result);
  })
  .catch((error) => {
    const statusCode = error.status;
    if (statusCode === 401) {
      console.error('Unauthorized - please login');
    } else if (statusCode === 404) {
      console.error('Data not found');
    } else if (statusCode === 0) {
      console.error('Network error');
    }
  });
```

### Filtering with Vue 3 Composition API

```typescript
import { ref, computed } from 'vue';
import { Query } from '@syncfusion/ej2-data';

const dm = new DataManager({ json: allData });
const searchText = ref('');

const filteredData = computed(() => {
  if (!searchText.value) return allData;
  
  return dm.executeLocal(
    new Query().where('CustomerID', 'contains', searchText.value)
  );
});
```

### Authentication Middleware

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

```typescript
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

// Apply middleware to add auth token
dataManager.applyPreRequestMiddlewares([
  async (context) => {
    const token = localStorage.getItem('auth_token');
    context.request.headers['Authorization'] = `send_token`;
  }
]);
```

---

## 🔧 DataManager Configuration

```typescript
const dataManager = new DataManager({
  // Data source
  url: 'url',        // Remote endpoint
  json: localArray,                            // Local array
  
  // Adaptor selection
  adaptor: new WebApiAdaptor(),              // Adaptor type
  
  // Headers & auth
  headers: [...],
  
  // Network settings
  crossDomain: true,                          // Enable CORS
  offline: false,                             // Offline mode
  enableCache: true,                          // Caching
  
  // Persistence
  enablePersistence: true,                    // Enable state persistence
  id: 'dataManager_vue',                      // Persistence ID
  ignoreOnPersist: ['temp', 'debug'],        // Properties to exclude
  timeZoneHandling: true                      // Timezone offset handling
});
```

---

## ❌ Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Missing/expired auth token | Add middleware with fresh token |
| 404 Not Found | Wrong endpoint URL | Verify API endpoint URL |
| 0 (Network Error) | No internet connection | Enable offline mode |
| Cross-Origin Error | CORS not enabled | Set crossDomain: true |

---

## ✅ Best Practices

1. **Always set adaptor** — Choose correct adaptor for your backend
2. **Pass keyField in CRUD methods** — Required as first parameter in update/delete
3. **Use async/await** — More readable than .then()/.catch()
4. **Add error handling** — Catch HTTP errors
5. **Enable caching** — Reduce server requests
6. **Use middleware** — Add auth globally
7. **Test both APIs** — Composition & Options patterns
8. **Handle network errors** — Status code 0 means no internet
9. **Use typed interfaces** — TypeScript support

---
