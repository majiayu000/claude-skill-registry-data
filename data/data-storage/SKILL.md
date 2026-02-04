---
name: data-storage
description: Implement client-side data storage with localStorage, IndexedDB, or SQLite WASM. Use when storing user preferences, caching data, or building offline-first applications.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Frontend Data Storage Skill

Implement client-side data storage using localStorage, IndexedDB, or SQLite WASM for offline-capable web applications.

---

## When to Use

- Storing user preferences and settings
- Caching API responses
- Implementing offline-first applications
- Managing large client-side datasets
- Syncing data between sessions

---

## Storage Options

| Storage | Best For | Size Limit | Persistence |
|---------|----------|------------|-------------|
| localStorage | Small key-value data, settings | ~5MB | Persistent |
| sessionStorage | Temporary session data | ~5MB | Tab only |
| IndexedDB | Larger datasets, offline apps | ~50MB+ | Persistent |
| SQLite WASM | Complex queries, relational data | ~50MB+ | Persistent |

---

## LocalStorage Wrapper

### Type-Safe Storage

```javascript
/**
 * Type-safe localStorage wrapper with JSON serialization
 */
export const storage = {
  /**
   * Get value from storage
   * @template T
   * @param {string} key - Storage key
   * @param {T} defaultValue - Default if not found
   * @returns {T} - Stored value or default
   */
  get(key, defaultValue = null) {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch {
      return defaultValue;
    }
  },

  /**
   * Set value in storage
   * @param {string} key - Storage key
   * @param {*} value - Value to store
   */
  set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      // Handle quota exceeded
      if (error.name === 'QuotaExceededError') {
        console.warn('Storage quota exceeded');
        this.cleanup();
        // Retry once
        localStorage.setItem(key, JSON.stringify(value));
      }
    }
  },

  /**
   * Remove value from storage
   * @param {string} key - Storage key
   */
  remove(key) {
    localStorage.removeItem(key);
  },

  /**
   * Clear all storage
   */
  clear() {
    localStorage.clear();
  },

  /**
   * Get all keys matching prefix
   * @param {string} prefix - Key prefix
   * @returns {string[]} - Matching keys
   */
  keys(prefix = '') {
    const keys = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key.startsWith(prefix)) {
        keys.push(key);
      }
    }
    return keys;
  },

  /**
   * Cleanup old/expired items
   */
  cleanup() {
    const now = Date.now();
    for (const key of this.keys()) {
      const item = this.get(key);
      if (item?.expiresAt && item.expiresAt < now) {
        this.remove(key);
      }
    }
  }
};
```

### Settings Pattern

```javascript
/**
 * User settings with defaults and persistence
 */
const DEFAULTS = {
  theme: 'system',
  language: 'en',
  fontSize: 'medium',
  notifications: true
};

export const settings = {
  _cache: null,

  /**
   * Load all settings
   * @returns {object} - Settings object
   */
  getAll() {
    if (!this._cache) {
      this._cache = {
        ...DEFAULTS,
        ...storage.get('user-settings', {})
      };
    }
    return this._cache;
  },

  /**
   * Get single setting
   * @param {string} key - Setting key
   * @returns {*} - Setting value
   */
  get(key) {
    return this.getAll()[key];
  },

  /**
   * Update settings
   * @param {object} updates - Settings to update
   */
  update(updates) {
    this._cache = { ...this.getAll(), ...updates };
    storage.set('user-settings', this._cache);

    // Emit change event
    window.dispatchEvent(new CustomEvent('settings-change', {
      detail: updates
    }));
  },

  /**
   * Reset to defaults
   */
  reset() {
    this._cache = { ...DEFAULTS };
    storage.set('user-settings', this._cache);
  }
};
```

---

## IndexedDB Wrapper

### Simple Store

```javascript
/**
 * Simple IndexedDB wrapper for object stores
 */
export class IDBStore {
  /**
   * @param {string} dbName - Database name
   * @param {string} storeName - Object store name
   * @param {number} version - Database version
   */
  constructor(dbName, storeName, version = 1) {
    this.dbName = dbName;
    this.storeName = storeName;
    this.version = version;
    this.db = null;
  }

  /**
   * Open database connection
   * @returns {Promise<IDBDatabase>}
   */
  async open() {
    if (this.db) return this.db;

    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve(this.db);
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: 'id' });
        }
      };
    });
  }

  /**
   * Get item by ID
   * @param {string} id - Item ID
   * @returns {Promise<*>}
   */
  async get(id) {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, 'readonly');
      const request = tx.objectStore(this.storeName).get(id);
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);
    });
  }

  /**
   * Get all items
   * @returns {Promise<Array>}
   */
  async getAll() {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, 'readonly');
      const request = tx.objectStore(this.storeName).getAll();
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);
    });
  }

  /**
   * Put item (insert or update)
   * @param {object} item - Item with id property
   * @returns {Promise<void>}
   */
  async put(item) {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, 'readwrite');
      const request = tx.objectStore(this.storeName).put(item);
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  /**
   * Delete item by ID
   * @param {string} id - Item ID
   * @returns {Promise<void>}
   */
  async delete(id) {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, 'readwrite');
      const request = tx.objectStore(this.storeName).delete(id);
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  /**
   * Clear all items
   * @returns {Promise<void>}
   */
  async clear() {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(this.storeName, 'readwrite');
      const request = tx.objectStore(this.storeName).clear();
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }
}

// Usage
const todosStore = new IDBStore('my-app', 'todos');

await todosStore.put({ id: '1', title: 'Learn IDB', done: false });
const todos = await todosStore.getAll();
```

---

## SQLite WASM

### Using sql.js

```javascript
/**
 * SQLite WASM wrapper using sql.js
 * @see https://sql.js.org/
 */
import initSqlJs from 'sql.js';

let SQL = null;

/**
 * Initialize SQL.js
 * @returns {Promise<void>}
 */
async function initSQL() {
  if (SQL) return;
  SQL = await initSqlJs({
    locateFile: file => `https://sql.js.org/dist/${file}`
  });
}

export class SQLiteDB {
  constructor(name) {
    this.name = name;
    this.db = null;
  }

  /**
   * Open or create database
   * @returns {Promise<void>}
   */
  async open() {
    await initSQL();

    // Try to load existing database from IndexedDB
    const stored = await this.loadFromStorage();
    if (stored) {
      this.db = new SQL.Database(stored);
    } else {
      this.db = new SQL.Database();
    }
  }

  /**
   * Execute SQL query
   * @param {string} sql - SQL statement
   * @param {Array} params - Query parameters
   * @returns {Array} - Result rows
   */
  exec(sql, params = []) {
    const stmt = this.db.prepare(sql);
    stmt.bind(params);

    const rows = [];
    while (stmt.step()) {
      rows.push(stmt.getAsObject());
    }
    stmt.free();
    return rows;
  }

  /**
   * Run SQL statement (no results)
   * @param {string} sql - SQL statement
   * @param {Array} params - Query parameters
   */
  run(sql, params = []) {
    this.db.run(sql, params);
  }

  /**
   * Save database to IndexedDB
   * @returns {Promise<void>}
   */
  async save() {
    const data = this.db.export();
    const buffer = new Uint8Array(data);

    const store = new IDBStore('sqlite-storage', 'databases');
    await store.put({ id: this.name, data: buffer });
  }

  /**
   * Load database from IndexedDB
   * @returns {Promise<Uint8Array|null>}
   */
  async loadFromStorage() {
    const store = new IDBStore('sqlite-storage', 'databases');
    const record = await store.get(this.name);
    return record?.data || null;
  }

  /**
   * Close database
   */
  close() {
    this.db?.close();
    this.db = null;
  }
}

// Usage
const db = new SQLiteDB('my-app');
await db.open();

// Create table
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

// Insert
db.run('INSERT INTO users (name, email) VALUES (?, ?)', ['John', 'john@example.com']);

// Query
const users = db.exec('SELECT * FROM users WHERE name LIKE ?', ['%John%']);

// Save to IndexedDB
await db.save();
```

---

## Storage Abstraction

### Unified Storage Interface

```javascript
/**
 * Unified storage interface
 * Allows switching backends without changing code
 */
export class StorageAdapter {
  constructor(backend) {
    this.backend = backend;
  }

  async get(key) {
    return this.backend.get(key);
  }

  async set(key, value) {
    return this.backend.set(key, value);
  }

  async remove(key) {
    return this.backend.remove(key);
  }

  async getAll() {
    return this.backend.getAll();
  }
}

// LocalStorage backend
const localBackend = {
  get: (key) => Promise.resolve(storage.get(key)),
  set: (key, value) => Promise.resolve(storage.set(key, value)),
  remove: (key) => Promise.resolve(storage.remove(key)),
  getAll: () => Promise.resolve(/* ... */)
};

// IndexedDB backend
const idbBackend = {
  store: new IDBStore('app', 'data'),
  get: (key) => this.store.get(key),
  set: (key, value) => this.store.put({ id: key, value }),
  remove: (key) => this.store.delete(key),
  getAll: () => this.store.getAll()
};

// Use same interface
const appStorage = new StorageAdapter(
  'indexedDB' in window ? idbBackend : localBackend
);
```

---

## Quota Management

```javascript
/**
 * Check storage quota
 * @returns {Promise<{usage: number, quota: number, percent: number}>}
 */
async function checkStorageQuota() {
  if ('storage' in navigator && 'estimate' in navigator.storage) {
    const { usage, quota } = await navigator.storage.estimate();
    return {
      usage,
      quota,
      percent: Math.round((usage / quota) * 100)
    };
  }
  return { usage: 0, quota: 0, percent: 0 };
}

/**
 * Request persistent storage
 * @returns {Promise<boolean>} - Whether granted
 */
async function requestPersistence() {
  if ('storage' in navigator && 'persist' in navigator.storage) {
    return navigator.storage.persist();
  }
  return false;
}
```

---

## Sync Patterns

### Last-Write-Wins Sync

```javascript
/**
 * Simple sync with last-write-wins conflict resolution
 */
async function syncWithServer(localData, serverEndpoint) {
  // Get server data
  const serverData = await fetch(serverEndpoint).then(r => r.json());

  // Merge: prefer newer timestamps
  const merged = {};

  for (const item of [...localData, ...serverData]) {
    const existing = merged[item.id];
    if (!existing || item.updatedAt > existing.updatedAt) {
      merged[item.id] = item;
    }
  }

  // Push changes to server
  const localChanges = Object.values(merged).filter(item =>
    !serverData.find(s => s.id === item.id && s.updatedAt >= item.updatedAt)
  );

  if (localChanges.length > 0) {
    await fetch(serverEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items: localChanges })
    });
  }

  return Object.values(merged);
}
```

---

## Checklist

When implementing data storage:

- [ ] Choose appropriate storage for data size and complexity
- [ ] Wrap storage APIs for testability
- [ ] Handle quota exceeded errors
- [ ] Implement data expiration for caches
- [ ] Add schema versioning for IndexedDB
- [ ] Consider encryption for sensitive data
- [ ] Request persistent storage for important data
- [ ] Implement sync strategy for offline-first
- [ ] Test with storage cleared/disabled
- [ ] Monitor storage usage
- [ ] Provide clear all/reset functionality

## Related Skills

- **state-management** - Client-side state patterns for Web Components
- **service-worker** - Service worker patterns for offline support, caching stra...
- **api-client** - Fetch API patterns with error handling, retry logic, and ...
- **security** - Write secure web pages and applications
