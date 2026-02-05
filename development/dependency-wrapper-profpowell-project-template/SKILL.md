---
name: dependency-wrapper
description: Wrap third-party libraries for testability and replaceability. Use when integrating external APIs, creating testable code, or building swappable implementations.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Dependency Wrapper Skill

Wrap third-party libraries for testability, replaceability, and controlled dependency injection.

---

## When to Use

- Integrating third-party APIs or libraries
- Creating testable code with external dependencies
- Building swappable implementations
- Managing configuration for external services
- Isolating vendor-specific code

---

## Philosophy

**Never call third-party libraries directly in business logic.**

Instead:
1. Create a wrapper module that exposes only what you need
2. Inject the wrapper where needed
3. Mock the wrapper in tests
4. Swap implementations without changing business code

---

## Wrapper Patterns

### Simple Wrapper

Wrap a library to expose a simplified interface:

```javascript
// lib/date.js
// Wrapper around date-fns (or any date library)

import { format, parseISO, addDays, differenceInDays } from 'date-fns';

/**
 * Date utilities wrapper
 * Swap date-fns for another library by changing only this file
 */
export const dateUtils = {
  /**
   * Format date for display
   * @param {Date|string} date
   * @param {string} formatStr - e.g., 'yyyy-MM-dd'
   * @returns {string}
   */
  format(date, formatStr = 'yyyy-MM-dd') {
    const d = typeof date === 'string' ? parseISO(date) : date;
    return format(d, formatStr);
  },

  /**
   * Add days to a date
   * @param {Date} date
   * @param {number} days
   * @returns {Date}
   */
  addDays(date, days) {
    return addDays(date, days);
  },

  /**
   * Get days between two dates
   * @param {Date} dateA
   * @param {Date} dateB
   * @returns {number}
   */
  daysBetween(dateA, dateB) {
    return differenceInDays(dateA, dateB);
  },

  /**
   * Parse ISO string to Date
   * @param {string} isoString
   * @returns {Date}
   */
  parse(isoString) {
    return parseISO(isoString);
  }
};
```

### Factory Pattern

Create instances with configuration:

```javascript
// lib/http-client.js
// Wrapper around fetch or axios

/**
 * Create configured HTTP client
 * @param {object} config
 * @returns {object} HTTP client
 */
export function createHttpClient(config = {}) {
  const {
    baseUrl = '',
    timeout = 10000,
    headers = {}
  } = config;

  async function request(path, options = {}) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(`${baseUrl}${path}`, {
        ...options,
        headers: { ...headers, ...options.headers },
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new HttpError(response.status, await response.text());
      }

      return response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }

  return {
    get: (path, options) => request(path, { ...options, method: 'GET' }),
    post: (path, body, options) => request(path, {
      ...options,
      method: 'POST',
      body: JSON.stringify(body),
      headers: { 'Content-Type': 'application/json', ...options?.headers }
    }),
    put: (path, body, options) => request(path, {
      ...options,
      method: 'PUT',
      body: JSON.stringify(body),
      headers: { 'Content-Type': 'application/json', ...options?.headers }
    }),
    delete: (path, options) => request(path, { ...options, method: 'DELETE' })
  };
}

class HttpError extends Error {
  constructor(status, body) {
    super(`HTTP ${status}`);
    this.status = status;
    this.body = body;
  }
}
```

### Adapter Pattern

Normalize different implementations behind a common interface:

```javascript
// lib/storage-adapter.js
// Adapter for different storage backends

/**
 * @typedef {object} StorageAdapter
 * @property {(key: string) => Promise<*>} get
 * @property {(key: string, value: *) => Promise<void>} set
 * @property {(key: string) => Promise<void>} remove
 */

/**
 * LocalStorage adapter
 * @returns {StorageAdapter}
 */
export function createLocalStorageAdapter() {
  return {
    async get(key) {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    },
    async set(key, value) {
      localStorage.setItem(key, JSON.stringify(value));
    },
    async remove(key) {
      localStorage.removeItem(key);
    }
  };
}

/**
 * IndexedDB adapter
 * @param {string} dbName
 * @returns {StorageAdapter}
 */
export function createIndexedDBAdapter(dbName) {
  // ... IndexedDB implementation
  return {
    async get(key) { /* ... */ },
    async set(key, value) { /* ... */ },
    async remove(key) { /* ... */ }
  };
}

/**
 * In-memory adapter (for testing)
 * @returns {StorageAdapter}
 */
export function createMemoryAdapter() {
  const store = new Map();
  return {
    async get(key) {
      return store.get(key) ?? null;
    },
    async set(key, value) {
      store.set(key, value);
    },
    async remove(key) {
      store.delete(key);
    }
  };
}
```

---

## Dependency Injection

### Service Container

Simple dependency container:

```javascript
// lib/container.js

/**
 * Simple dependency injection container
 */
class Container {
  constructor() {
    this.services = new Map();
    this.singletons = new Map();
  }

  /**
   * Register a service factory
   * @param {string} name
   * @param {Function} factory
   * @param {object} options
   */
  register(name, factory, { singleton = false } = {}) {
    this.services.set(name, { factory, singleton });
  }

  /**
   * Get a service instance
   * @param {string} name
   * @returns {*}
   */
  get(name) {
    const service = this.services.get(name);
    if (!service) {
      throw new Error(`Service not registered: ${name}`);
    }

    if (service.singleton) {
      if (!this.singletons.has(name)) {
        this.singletons.set(name, service.factory(this));
      }
      return this.singletons.get(name);
    }

    return service.factory(this);
  }
}

export const container = new Container();

// Register services
container.register('config', () => ({
  apiUrl: process.env.API_URL,
  // ...
}), { singleton: true });

container.register('httpClient', (c) => {
  const config = c.get('config');
  return createHttpClient({ baseUrl: config.apiUrl });
}, { singleton: true });

container.register('userService', (c) => {
  return createUserService(c.get('httpClient'));
});
```

### Constructor Injection

Pass dependencies to constructors:

```javascript
// services/user-service.js

/**
 * User service with injected HTTP client
 * @param {object} httpClient - HTTP client instance
 */
export function createUserService(httpClient) {
  return {
    async getUser(id) {
      return httpClient.get(`/users/${id}`);
    },

    async createUser(data) {
      return httpClient.post('/users', data);
    },

    async updateUser(id, data) {
      return httpClient.put(`/users/${id}`, data);
    }
  };
}
```

---

## Testing with Wrappers

### Mock Factory

Create test doubles easily:

```javascript
// test/mocks/http-client.js

/**
 * Create mock HTTP client for testing
 * @param {object} responses - Map of path to response
 */
export function createMockHttpClient(responses = {}) {
  const calls = [];

  return {
    async get(path) {
      calls.push({ method: 'GET', path });
      const response = responses[`GET ${path}`] ?? responses[path];
      if (response instanceof Error) throw response;
      return response;
    },

    async post(path, body) {
      calls.push({ method: 'POST', path, body });
      const response = responses[`POST ${path}`] ?? responses[path];
      if (response instanceof Error) throw response;
      return response;
    },

    // ... other methods

    // Test helpers
    getCalls() {
      return calls;
    },

    wasCalledWith(method, path) {
      return calls.some(c => c.method === method && c.path === path);
    }
  };
}
```

### Testing Example

```javascript
// test/services/user-service.test.js
import { describe, it } from 'node:test';
import assert from 'node:assert';
import { createUserService } from '../../src/services/user-service.js';
import { createMockHttpClient } from '../mocks/http-client.js';

describe('UserService', () => {
  it('fetches user by id', async () => {
    const mockHttp = createMockHttpClient({
      'GET /users/123': { id: '123', name: 'John' }
    });

    const userService = createUserService(mockHttp);
    const user = await userService.getUser('123');

    assert.equal(user.name, 'John');
    assert.ok(mockHttp.wasCalledWith('GET', '/users/123'));
  });

  it('handles errors', async () => {
    const mockHttp = createMockHttpClient({
      'GET /users/999': new Error('Not found')
    });

    const userService = createUserService(mockHttp);

    await assert.rejects(
      () => userService.getUser('999'),
      /Not found/
    );
  });
});
```

---

## Common Wrappers

### Email Service

```javascript
// lib/email.js
// Swap SendGrid, Mailgun, SES by changing this file

/**
 * Create email service
 * @param {object} config
 */
export function createEmailService(config) {
  const { provider = 'console', apiKey } = config;

  const providers = {
    console: {
      async send({ to, subject, html }) {
        console.log(`Email to ${to}: ${subject}`);
        return { id: 'console-' + Date.now() };
      }
    },
    sendgrid: {
      async send({ to, subject, html }) {
        // SendGrid implementation
      }
    }
  };

  return providers[provider] || providers.console;
}
```

### Payment Service

```javascript
// lib/payments.js

/**
 * Payment gateway adapter
 */
export function createPaymentService(config) {
  const { provider, apiKey } = config;

  return {
    async createPayment(amount, currency, metadata) {
      // Route to configured provider
    },

    async refund(paymentId, amount) {
      // ...
    },

    async getPayment(paymentId) {
      // ...
    }
  };
}
```

---

## Checklist

When wrapping dependencies:

- [ ] Create wrapper module in `lib/` or `adapters/`
- [ ] Expose only the interface you need
- [ ] Use factory functions for configuration
- [ ] Accept dependencies as constructor parameters
- [ ] Create mock factories for testing
- [ ] Document the wrapper's public API with JSDoc
- [ ] Keep vendor-specific code isolated in wrapper
- [ ] Use adapters for swappable implementations
- [ ] Register dependencies in container if using DI
- [ ] Write tests using mock implementations

## Related Skills

- **unit-testing** - Write unit tests for JavaScript files using Node.js nativ...
- **api-client** - Fetch API patterns with error handling, retry logic, and ...
- **authentication** - Implement secure authentication with JWT, sessions, OAuth...
- **nodejs-backend** - Build Node.js backend services with Express/Fastify, Post...
