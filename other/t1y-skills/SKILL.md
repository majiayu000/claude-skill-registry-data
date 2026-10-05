---
name: t1yOS
description: >-
  Expert knowledge for the t1yOS Serverless platform. Use this skill whenever
  the user mentions t1yOS, cloud functions, .jsc files, serverless development,
  or needs help with t1yOS platform features (cloud database, MCP tools, SDKs,
  crypto, JWT, file storage, scheduled tasks). Also use when the user asks about
  writing or debugging t1yOS cloud functions, integrating t1yOS SDKs, managing
  platform resources via MCP, or understanding t1yOS security mechanisms
  (HMAC-SHA256 signing, AES-256-GCM encryption). This skill provides the
  authoritative rules, API references, and best practices that even experienced
  developers need — the platform has specific conventions (.jsc extension,
  onRequest entry point, require-based modules) that differ from standard
  Node.js or other serverless platforms.
---

# t1yOS Platform Skill

Expert knowledge for developing on the t1yOS Serverless cloud OS.

## When to consult reference files

This SKILL.md covers the essential rules, patterns, and mental model. Detailed
API tables and exhaustive option lists live in `references/`. Read them when you
need exact signatures:

| Reference                      | When to read                                                               |
| ------------------------------ | -------------------------------------------------------------------------- |
| `references/cloud-function.md` | Need exact function signatures for context, http, os, jwt modules          |
| `references/database.md`       | Database CRUD with exact parameter types, query operators, SQL ops         |
| `references/crypto.md`         | Hashing, AES-GCM, password hashing, encoding function names and signatures |
| `references/mcp.md`            | MCP Server configuration and tool catalog with parameters                  |
| `references/sdks.md`           | Client SDK integration (JS, Android, Swift, Flutter, C#, Go)               |
| `references/security.md`       | HMAC-SHA256 signing spec, AES-256-GCM safe mode, security best practices   |
| `references/constants.md`      | HTTP status codes, methods, MIME type constants                            |

---

## Platform mental model

t1yOS is a **Serverless cloud OS**. It bundles cloud functions, a NoSQL
database (with SQL-to-BSON), file storage, environment variables, scheduled
tasks, and an MCP Server into one platform.

**The runtime is Go/fasthttp** with an Express.js-like JavaScript API. Files use
`.jsc` extension under `/.functions/` directory.

### Cloud function URL format — CRITICAL

Cloud function URLs MUST include the **Application ID** in the path. The format
is:

```
https://myapp.t1y.net/<AppID>/<function-name>.jsc
```

**NOT** `https://myapp.t1y.net/<function-name>.jsc` (missing AppID → 404).

For example, if your AppID is `1001` and your function is `index.jsc`:

```
https://myapp.t1y.net/1001/index.jsc?name=Zhangsan
```

### How to get the AppID

**If the user's MCP Server is configured**, call the `app_info` MCP tool to
retrieve the Application ID:

```
Use the t1yOS MCP tool: app_info
→ Returns: { appId: "1001", name: "...", ... }
```

**If MCP is NOT configured**, ask the user for their AppID. Tell them to find it
in the [t1yOS Console](https://console.t1y.net/) under their application
settings.

### When testing or sharing URLs

Whenever you generate a cloud function URL for testing (curl, browser, etc.),
always:

1. **First** try to get the AppID via the `app_info` MCP tool
2. **If unavailable**, ask the user: "请提供你的 t1yOS 应用 ID（可在控制台中找到）"
3. Construct the URL as `https://myapp.t1y.net/<AppID>/<function>.jsc`

---

## Required workflow: Write → Deploy → Test (MANDATORY)

**After writing a cloud function, you MUST deploy and test it.** Do NOT just
write the code and stop — the job is not done until the function has been
verified working with a real request.

### Step 1: Deploy the function

**Always use MCP tools — the preferred and most efficient method:**

- **New function**: `function_create` with `name` and `code` — auto-compiles, no manual rebuild
- **Update existing**: `function_update` with `name` and updated `code` — auto-compiles

MCP tools handle compilation automatically. Do NOT write `.jsc` files via file
tools and then manually call `function_rebuild_all` — that wastes tokens.

⚠️ All cloud functions MUST be placed in the **`/.functions/`** directory (with
dot prefix). `/functions/` (without dot) is WRONG and will not work.

If MCP is not configured, guide the user to deploy via WebIDE or the platform
console.

### Step 2: Test the function (REQUIRED — do NOT skip)

Make a real HTTP request to the deployed cloud function. Use whatever HTTP tool
is available in the user's environment:

- **macOS / Linux**: `curl` or `httpie`
- **Windows**: `curl` (CMD/PowerShell) or `Invoke-WebRequest` (PowerShell)
- **Any platform**: `python -c "import urllib.request; ..."` or `fetch` (Node.js)

**Before testing**, you MUST construct the correct URL:

1. Get the AppID via MCP `app_info` tool (or ask the user)
2. Build the URL: `https://myapp.t1y.net/<AppID>/<function>.jsc`
3. Add query parameters or request body as appropriate for the endpoint

Example curl commands:

```bash
# GET request with query params
curl -s "https://myapp.t1y.net/<AppID>/index.jsc?name=TestUser"

# POST request with JSON body
curl -s -X POST "https://myapp.t1y.net/<AppID>/index.jsc" \
  -H "Content-Type: application/json" \
  -d '{"name": "TestUser"}'

# POST request with form data
curl -s -X POST "https://myapp.t1y.net/<AppID>/login.jsc" \
  -d "username=admin&password=123456"
```

### Step 3: Debug if the test fails

If the test request returns an error or unexpected result:

- **Check logs**: Use MCP `function_get_log` with the function name
  ```
  MCP tool: function_get_log
  Parameters: { name: "index", lines: 50 }
  ```
- **Redeploy if needed**: Use `function_update` after fixing the code
- **Common checks**: verify the URL includes AppID, verify the function is in
  `/.functions/` directory, verify `.jsc` extension, check HTTP method matches

### Step 4: Report the result

After testing, report to the user:

- ✅ What was tested and whether it passed
- 📋 The actual response/result
- 🐛 If failed: the error details and suggested fix

**If the test fails, fix the code and test again.** Do not leave the user with
untested code.

## Critical rules — read these first

1. **`.jsc` extension required**: Cloud functions MUST use `.jsc` (NOT `.js`).
2. **`onRequest()` takes NO parameters**: The entry function is `function
onRequest() { ... }` — no arguments.
3. **`ctx` comes from `require('context')`**: Always write `const ctx =
require('context')` at the top to access request/response methods.
4. **Everything on ctx is a FUNCTION**: `ctx.method()`, `ctx.query('key')`,
   `ctx.body()`, `ctx.get('Header-Name')`, `ctx.set('Header', 'value')` — all
   function calls, NOT property access.
5. **No ES modules**: Use `require()` not `import`. No `module.exports` for the
   entry function (but custom helper modules CAN use it).
6. **No npm**: Only built-in modules available: `context`, `http`, `mongo`,
   `crypto`, `os`, `jwt`. You CAN `require()` local/remote `.js` and `.json`
   files.
7. **Go templates**: `ctx.render()` uses Go `{{ .Field }}` syntax.
8. **Logging**: Use `console.log()`, `console.info()`, `console.debug()`,
   `console.warn()`, `console.error()`. NOT `ctx.log()`.
9. **Hidden files blocked**: All dot-prefixed files and directories are inaccessible via HTTP, except
   `.jsc` files within the `/.functions/` directory.
10. **MUST test after writing**: After deploying a cloud function, you are
    REQUIRED to test it with a real HTTP request (via MCP `function_run` or
    curl). Never just write code and stop — verify it works.

---

## Core cloud function structure

```javascript
// Always require context at the top
const ctx = require('context')
const http = require('http')

// onRequest takes NO parameters — all state comes from ctx
function onRequest() {
  // ctx.method() returns the HTTP method string
  if (ctx.method() === 'GET') {
    // ctx.query('key') gets a single query parameter
    const name = ctx.query('name', 'World') // Second arg = default
    return `Hello, ${name}!`
  }

  if (ctx.method() === 'POST') {
    // ctx.body() returns the parsed request body
    const body = ctx.body()
    return { received: body }
  }

  // Return any value — auto-serialized to response
  return { status: 'ok' }
}
```

### The onRequest return pattern

`onRequest()` returns a value OR calls a ctx response method and returns `null`:

| Pattern                      | Code                                                     |
| ---------------------------- | -------------------------------------------------------- |
| Return data (auto-serialize) | `return { key: 'value' }`                                |
| Return string                | `return 'Hello'`                                         |
| Render template              | `ctx.render('/.templates/page.tmpl', data); return null` |
| Send file                    | `ctx.sendFile('/path/to/file.png'); return null`         |
| Trigger download             | `ctx.download('/path/to/file.pdf'); return null`         |
| Redirect                     | `ctx.redirect(302, 'https://example.com'); return null`  |
| XML response                 | `ctx.XML(data); return null`                             |
| JSONP response               | `ctx.jsonp(data); return null`                           |
| Custom status only           | `ctx.sendStatus(404); return null`                       |

**Rule**: when using `ctx.render()`, `ctx.sendFile()`, `ctx.download()`,
`ctx.redirect()`, `ctx.XML()`, `ctx.jsonp()`, or `ctx.sendStatus()`, always
`return null` after — you've already sent the response.

---

## Context (ctx) API quick reference

Every method on ctx is a **function call**. Here are the most common ones:

### Reading the request

```javascript
const ctx = require('context')

function onRequest() {
  ctx.method() // → "GET", "POST", etc.
  ctx.query('name') // → query param value (string)
  ctx.query('name', 'default') // → with default value
  ctx.queries() // → ALL query params as object
  ctx.body() // → parsed request body (JSON→object, else string)
  ctx.hasBody() // → true/false: is there a body?
  ctx.isJSON() // → true/false: is Content-Type application/json?
  ctx.isForm() // → true/false: is it form data?
  ctx.formValue('field') // → form field value
  ctx.formValue('field', 'default') // → with default
  ctx.get('Header-Name') // → single request header value
  ctx.get('X-Forwarded-For', '0.0.0.0') // → with default
  ctx.getReqHeaders() // → ALL request headers as object
  ctx.hasHeader('Header-Name') // → true/false: header exists?
  ctx.ip() // → client IP string
  ctx.ips() // → X-Forwarded-For IP array
  ctx.userAgent() // → User-Agent string
  ctx.cookies('name') // → get cookie value
  ctx.cookies('name', 'default') // → with default
}
```

### Writing the response

```javascript
function onRequest() {
  ctx.set('Content-Type', 'text/plain') // set response header
  ctx.sendStatus(200) // set HTTP status code
  ctx.sendStatus(http.StatusNotFound) // use constants from require('http')
  ctx.cookie({
    // set a cookie
    name: 'session',
    value: 'abc123',
    max_age: 86400,
    http_only: true,
    secure: true,
    same_site: 'Strict',
  })
  ctx.ClearCookie('session') // clear specific cookie (note: capital C)
  ctx.ClearCookie() // clear ALL cookies
  ctx.redirect(302, 'https://example.com') // redirect (statusCode FIRST)
  ctx.render('/.templates/page.tmpl', {
    // render Go template
    Title: 'My Page',
    User: { Name: 'WangHua', Age: 23 },
  })
  ctx.sendFile('/path/to/file.png') // send file content
  ctx.download('/path/to/file.pdf') // trigger browser download
  ctx.XML({ name: 'WangHua', age: 23 }) // send XML response
  ctx.jsonp({ name: 'WangHua' }) // send JSONP, auto callback
  ctx.jsonp({ name: 'WangHua' }, 'cb') // custom callback name
}
```

### File upload

```javascript
function onRequest() {
  const fileInfo = ctx.formFileInfo('file') // get upload file info
  // fileInfo: { filename, size, header }
  ctx.saveFile('file', '/.private/uploads/' + fileInfo.filename) // save file
  return 'uploaded'
}
```

### Request-level storage

```javascript
function onRequest() {
  ctx.locals('uid', 123456) // store
  ctx.locals('name', 'WangHua') // store
  const uid = ctx.locals('uid') // retrieve → 123456
}
```

### Security methods

```javascript
function onRequest() {
  // Verify HMAC-SHA256 signature (returns true/false, does NOT throw)
  if (!ctx.sign()) {
    return '签名验证失败'
  }

  // Enable AES-256-GCM safe mode (encrypts response, decrypts request)
  ctx.enableSafeMode()
}
```

---

## Database usage patterns

```javascript
const db = require('mongo')

function onRequest() {
  const users = db.collection('users')

  // ── Create ──────────────────────────────────────────────
  // insertOne returns the ObjectID (single ID string), NOT the full document
  const objectId = users.insertOne({
    name: 'WangHua',
    age: 23,
    email: 'test@example.com',
  })
  // → "60d5f7c8a1b2c3d4e5f6a7b8"

  // insertMany returns array of ObjectIDs
  const ids = users.insertMany([
    { name: 'ZhangSan', age: 25 },
    { name: 'LiSi', age: 30 },
  ])
  // → ["60d5...b8", "60d5...b9"]

  // ── Read ────────────────────────────────────────────────
  // ⚠️ findOne THROWS an exception when no document matches — NOT returns null!
  // Always wrap findOne in try-catch to handle the 'no documents in result' error:
  let user
  try {
    user = users.findOne({ name: 'WangHua' })
  } catch (e) {
    // No matching document — handle gracefully
    user = null
  }
  if (!user) {
    return { code: 404, message: '用户不存在' }
  }

  // find(page, size, filter, sort) — page starts at 1
  const result = users.find(1, 10, {}, { createdAt: -1 })
  // → { results: [...], page: 1, size: 10, pagination: { totalItems, totalPages } }

  // find with filter
  const adults = users.find(1, 20, { age: { $gt: 18 } }, { name: 1 })

  // ── Update ──────────────────────────────────────────────
  // updateOne(filter, data) — data is the replacement fields directly
  // Returns modified count (Number)
  const modified = users.updateOne(
    { name: 'WangHua' }, // filter
    { age: 24, city: '深圳' } // new field values (NO $set wrapper!)
  )

  // updateMany: same pattern, affects all matching docs
  const count = users.updateMany({ role: 'viewer' }, { role: 'member' })

  // ── Delete ──────────────────────────────────────────────
  const deleted1 = users.deleteOne({ name: 'WangWu' }) // returns count
  const deleted2 = users.deleteMany({ status: 'inactive' }) // returns count

  // ── Count & Distinct ────────────────────────────────────
  const total = users.count({}) // filter REQUIRED
  const active = users.count({ status: 'active' })
  const cities = users.distinct('city', {}) // (field, filter)
  const adminCities = users.distinct('city', { role: 'admin' })

  // ── Aggregate ───────────────────────────────────────────
  const pipeline = [{ $group: { _id: '$city', count: { $sum: 1 } } }, { $sort: { count: -1 } }]
  const aggResult = orders.aggregate(pipeline)

  // ── Collection management ───────────────────────────────
  db.collection('logs').create() // explicitly create collection
  db.getCollections() // list all collection names → String[]
  db.collection('logs').clear() // clear all docs, keep structure → count
  db.collection('temp').drop() // DESTROY collection entirely

  // ── Utility ─────────────────────────────────────────────
  const oid = db.toObjectID('60d5f7c8a1b2c3d4e5f6a7b8')
  let userByOid
  try {
    userByOid = users.findOne({ _id: oid })
  } catch (e) {
    userByOid = null
  }
}
```

### SQL operations (on db directly — NOT on collection)

```javascript
const db = require('mongo')

function onRequest() {
  // These are called on `db`, not on a collection reference
  db.insertBySQL("INSERT INTO users (name, age) VALUES ('ZhaoLiu', 27)")
  db.selectBySQL('SELECT name, age FROM users WHERE age > 18 ORDER BY age DESC')
  db.updateBySQL("UPDATE users SET status = 'active' WHERE age >= 18")
  db.deleteBySQL("DELETE FROM users WHERE status = 'inactive'")
}
```

### Key database rules

- **insertOne returns ObjectID** (string), NOT the full document
- **insertMany returns ObjectID[]** (array of strings)
- **⚠️ findOne THROWS on no match**: When no document matches the filter,
  `findOne` throws an exception (`mongo: no documents in result`). Always wrap
  it in try-catch instead of checking for null. `find()` also throws when the
  result set is empty.
- **find signature**: `find(page, size, filter, sort)` — 4 positional args. Page
  starts at **1** (not 0).
- **updateOne/updateMany**: second arg is direct field values. No `$set`
  wrapper needed.
- **count(filter)**: filter is REQUIRED. Use `{}` for all documents.
- **distinct(field, filter)**: two args, both required. Use `{}` for no filter.
- System auto-creates `createdAt` and `updatedAt` fields on insert/update.
- Collections auto-create on first insert.

---

## JWT authentication

**The t1yOS JWT API is completely different from standard jsonwebtoken:**

```javascript
const jwt = require('jwt')
const ctx = require('context')
const http = require('http')

function onRequest() {
  // ── Generate token ──────────────────────────────────────
  // jwt.generateToken(userId, roles, expiresAtMinutes)
  const MINUTES_7_DAYS = 7 * 24 * 60
  const token = jwt.generateToken('uid123', ['user', 'super_admin'], MINUTES_7_DAYS)

  // ── Verify token ────────────────────────────────────────
  // jwt.verifyToken() — NO arguments! Auto-reads from request context
  // Returns { userId, roles } or throws on invalid/missing token
  const payload = jwt.verifyToken()

  if (payload.userId !== 'uid123') {
    ctx.sendStatus(http.StatusUnauthorized)
    return { code: http.StatusUnauthorized, message: '权限不足', data: null }
  }

  if (!payload.roles.includes('super_admin')) {
    ctx.sendStatus(http.StatusUnauthorized)
    return { code: http.StatusUnauthorized, message: '权限不足', data: null }
  }

  return `Hello, ${payload.userId}!`
}
```

**Key JWT rules:**

- `generateToken(userId, roles, expiresAtMinutes)` — 3 args, expiry in MINUTES
- `verifyToken()` — NO arguments, auto-verifies from request Authorization
  header
- The `roles` parameter is an **array of strings**: `['user', 'admin']`

---

## Crypto module

```javascript
const crypto = require('crypto')

function onRequest() {
  // ── Hashing (all take one string, return hex) ───────────
  crypto.md5('hello')
  crypto.sha256('hello')
  crypto.sha512('hello')
  crypto.sha3_256('hello')
  crypto.sha3_512('hello')
  crypto.blake2b_256('hello')
  crypto.blake2b_512('hello')

  // ── HMAC (key FIRST, then data) ─────────────────────────
  crypto.hmac_sha256('my-secret-key', 'hello')
  crypto.hmac_sha512('my-secret-key', 'hello')

  // ── Encoding ────────────────────────────────────────────
  crypto.base64_encode('Hello')
  crypto.base64_decode('SGVsbG8=')
  crypto.base58_encode('Hello')
  crypto.base58_decode('...')
  crypto.hex_encode('Hello')
  crypto.hex_decode('48656c6c6f')

  // ── Password hashing ────────────────────────────────────
  // Note: compare functions take (hash, password) — hash FIRST
  const hash = crypto.bcrypt_hash('myPassword123')
  const match = crypto.bcrypt_compare(hash, 'myPassword123') // → true

  const hash2 = crypto.argon2id_hash('myPassword123')
  const match2 = crypto.argon2id_compare(hash2, 'myPassword123') // → true

  // ── AES-256-GCM ─────────────────────────────────────────
  // Function names: aes_gcm_encrypt / aes_gcm_decrypt
  // Key MUST be exactly 32 bytes
  const key = '12345678901234567890123456789012' // 32 bytes
  const encrypted = crypto.aes_gcm_encrypt('sensitive data', key)
  // → JSON string: {"n":"...","j":"...","t":"..."}
  const decrypted = crypto.aes_gcm_decrypt(encrypted, key)
  // → 'sensitive data'

  // ── UUID v4 ─────────────────────────────────────────────
  crypto.uuid() // → "550e8400-e29b-41d4-a716-446655440000"
}
```

**Key crypto rules:**

- HMAC: key first, data second → `hmac_sha256(key, data)`
- Compare: hash first, password second → `bcrypt_compare(hash, password)`
- AES names: `aes_gcm_encrypt` / `aes_gcm_decrypt` (NOT `encryptAES256GCM`)
- AES key must be exactly 32 bytes

---

## HTTP client and constants

```javascript
const http = require('http')

function onRequest() {
  // ── Outbound HTTP request ───────────────────────────────
  // http.send(method, url, headers, body) — 4 positional args
  const resp = http.send('GET', 'https://myapp.t1y.net/timestamp', {}, '')
  // resp: { status, statusCode, proto, headers, body, contentLength }
  if (resp.statusCode !== http.StatusOK) {
    return 'request failed'
  }
  return resp.body // auto-parsed if JSON

  // POST with body
  const resp2 = http.send(
    'POST',
    'https://api.example.com/data',
    { Authorization: 'Bearer token', 'Content-Type': 'application/json' },
    JSON.stringify({ name: 'WangHua' })
  )
}
```

### Commonly used HTTP constants

```javascript
// Methods
;(http.MethodGet, http.MethodPost, http.MethodPut, http.MethodPatch, http.MethodDelete)

// Status codes
;(http.StatusOK(200), http.StatusCreated(201), http.StatusBadRequest(400))
;(http.StatusUnauthorized(401), http.StatusForbidden(403), http.StatusNotFound(404))
;(http.StatusMethodNotAllowed(405), http.StatusConflict(409))
http.StatusInternalServerError(500)

// MIME types
;(http.MIMEApplicationJSON, http.MIMETextHTML, http.MIMETextPlain)
```

Read `references/constants.md` for the complete list.

---

## File and environment operations (os module)

```javascript
const os = require('os')

function onRequest() {
  // ── Read file ───────────────────────────────────────────
  // os.readFile(path, encoding, options)
  // Supported encodings: 'utf-8', 'gb18030', 'gbk'
  const content = os.readFile('/.private/config.txt', 'utf-8', {})

  // With checksum verification
  const verified = os.readFile('/.private/data.txt', 'utf-8', {
    verify_checksum: true,
    expected_checksum: '5d41402abc4b2a76b9719d911017c592',
  })

  // ── Write file ──────────────────────────────────────────
  // os.writeFile(path, data, options)
  // Options: { atomic, sync, return_checksum }
  // Returns: { bytes_written, checksum }

  // Simple write
  os.writeFile('/.private/hello.txt', 'hello world', {})

  // Atomic write (recommended — prevents partial reads)
  const res = os.writeFile('/.private/data.json', JSON.stringify({ id: 1 }), {
    atomic: true,
  })
  // res.bytes_written, res.checksum

  // Write with checksum returned
  const res2 = os.writeFile('/.private/data.txt', 'content', {
    return_checksum: true,
  })
  // res2.checksum → md5 hex string

  // Force fsync (critical data)
  os.writeFile('/.private/log.txt', 'critical', { sync: true })

  // ── Environment variables ────────────────────────────────
  os.getEnv('API_KEY') // returns value or undefined
  os.setEnv('API_KEY', 'sk-xxx') // set variable
  os.unSetEnv('API_KEY') // delete variable
}
```

---

## Security

### Request signature verification

```javascript
const ctx = require('context')

function onRequest() {
  // ctx.sign() returns BOOLEAN (true/false). Does NOT throw.
  if (!ctx.sign()) {
    return '签名验证失败'
  }
  // Request is authentic — proceed
  return '你好！'
}
```

### Safe mode (AES-256-GCM encryption)

```javascript
const ctx = require('context')

function onRequest() {
  ctx.enableSafeMode()
  // Request body is auto-decrypted, response is auto-encrypted
  return { data: 'secure response' }
}
```

Read `references/security.md` for HMAC signing specification and detailed
security best practices.

---

## Custom modules

### Require path rules — critical

| File type                | Path rule                                                    | Example                                     |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------- |
| `.jsc` (cloud function)  | Omit `/.functions/` prefix — path relative to `/.functions/` | `require("/pkg/response.jsc")`              |
| `.js` (plain JavaScript) | MUST use full path from root                                 | `require("/.librarys/crypto-js.min.js")`    |
| `.json`                  | MUST use full path from root                                 | `require("/.private/config.json")`          |
| Remote URL               | Full HTTPS URL                                               | `require("https://cdn.example.com/lib.js")` |

**Why**: `.jsc` files are pre-compiled and the platform resolves them relative
to `/.functions/`. `.js` and `.json` files are file-system imports that need the
absolute path.

⚠️ `/.functions/` supports **2-level subdirectories**. You can organize your
code like `/.functions/api/users.jsc` or `/.functions/pkg/response.jsc`.

### Writing a helper module (.jsc)

```javascript
// /.functions/pkg/response.jsc
const http = require('http')

// Use module.exports for helper modules (NOT for entry functions)
module.exports = {
  fail: (code, message, data) => {
    return { code, message, data }
  },
  success: (message, data) => {
    return { code: http.StatusOK, message, data }
  },
}
```

### Using a helper module

```javascript
// /.functions/index.jsc
// .jsc files: omit /.functions prefix
const resp = require('/pkg/response.jsc')

function onRequest() {
  return resp.success('ok', null)
}
```

### Importing JSON

```javascript
// .json files: MUST use full path
const config = require('/.private/config.json')

function onRequest() {
  return config.apiKey
}
```

### Remote imports

```javascript
const CryptoJS = require('https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.2.0/crypto-js.min.js')

function onRequest() {
  clearCache() // call only when you need to force re-fetch cached modules
  return CryptoJS.MD5('Hello').toString()
}
```

- Local/remote imports are cached. Use `clearCache()` to force refresh.
- Remote imports: first load is slower, subsequent loads use cache.
- `.jsc` cloud function files are pre-compiled (not cached), changes take effect immediately.

---

## SDK integration pattern (all platforms)

```
1. Install SDK → 2. Create client → 3. client.init() → 4. client.db.collection().operation()
```

```javascript
// JavaScript/TypeScript example
import T1YOS from 't1yos'

const client = new T1YOS({
  appId: 'your-app-id',
  apiKey: 'your-api-key',
  secretKey: 'your-secret-key',
})

await client.init()
const users = client.db.collection('users')
await users.insertOne({ name: 'Alice' })
```

Read `references/sdks.md` for platform-specific details.

---

## MCP Server overview

URL: `https://ai.t1y.net/mcp`
Type: `streamable-http`
Required headers: `X-T1Y-Application-ID`, `X-T1Y-API-Key`, `X-T1Y-Secret-Key`,
`X-T1Y-Access-Token`

Tools: Database CRUD, env vars, file management, cloud functions, app settings,
scheduled tasks (Pro).

**Key tool for URL construction**: Use `app_info` to get the user's Application
ID. This is essential for building correct cloud function URLs and debugging
access issues.

Read `references/mcp.md` for complete tool catalog with parameters.

---

## Common mistakes checklist

1. ❌ Using `.js` extension → ✅ Must be `.jsc`
2. ❌ `function onRequest(ctx)` → ✅ `function onRequest()` (no params)
3. ❌ `ctx.method` (property) → ✅ `ctx.method()` (function)
4. ❌ `ctx.query.name` (property) → ✅ `ctx.query('name')` (function)
5. ❌ `ctx.body` (property) → ✅ `ctx.body()` (function)
6. ❌ `ctx.headers['X']` (property) → ✅ `ctx.get('X')` (function)
7. ❌ `ctx.setHeader(k, v)` → ✅ `ctx.set(k, v)`
8. ❌ `ctx.setCookie(name, value)` → ✅ `ctx.cookie({ name, value, ... })`
9. ❌ `ctx.log(...)` → ✅ `console.log(...)`
10. ❌ `jwt.sign(payload, secret)` → ✅ `jwt.generateToken(userId, roles, minutes)`
11. ❌ `jwt.verify(token, secret)` → ✅ `jwt.verifyToken()` (no args!)
12. ❌ `collection.find(filter, { skip, limit })` → ✅ `collection.find(page, size, filter, sort)`
13. ❌ `insertOne` returns document → ✅ returns `ObjectID` string
14. ❌ `updateOne(filter, { $set: data })` → ✅ `updateOne(filter, data)` (no $set)
15. ❌ `ctx.redirect(url, code)` → ✅ `ctx.redirect(code, url)` (code first!)
16. ❌ `ctx.sign()` throws → ✅ `ctx.sign()` returns boolean
17. ❌ `crypto.encryptAES256GCM()` → ✅ `crypto.aes_gcm_encrypt()`
18. ❌ `hmac_sha256(data, key)` → ✅ `hmac_sha256(key, data)` (key first!)
19. ❌ `bcrypt_compare(password, hash)` → ✅ `bcrypt_compare(hash, password)` (hash first!)
20. ❌ URL `https://myapp.t1y.net/test.jsc` (missing AppID → 404) → ✅ `https://myapp.t1y.net/<AppID>/test.jsc` — always include AppID in the URL path. Get AppID via MCP `app_info` tool or ask the user.
21. ❌ Write code and stop without testing → ✅ After deploying, ALWAYS test with an HTTP request. Untested code is incomplete code.
22. ❌ `const user = users.findOne(...); if (!user)` → ✅ Wrap in try-catch — `findOne` THROWS on no match, does NOT return null.
23. ❌ Deploy via file write + manual rebuild → ✅ Use MCP `function_create`/`function_update` — auto-compiles, no manual rebuild.
24. ❌ require path `/.functions/pkg/x.jsc` → ✅ `require("/pkg/x.jsc")` — omit `/.functions` prefix for .jsc files.
