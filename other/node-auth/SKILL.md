---
name: node-auth
description: Password and session-cookie authentication for a Node Web Only server, built entirely on node:crypto. Use when adding a login flow, hashing or verifying a password, issuing or validating a session, setting a cookie, or protecting a route. Triggers on scrypt, timingSafeEqual, createHmac, Set-Cookie, HttpOnly, SameSite, users.json, session tokens, and any mention of bcrypt, jsonwebtoken, or passport.
user-invocable: false
---

# Node Auth

**scrypt for passwords, an HMAC-signed token for sessions, and an `HttpOnly` cookie to carry it. No auth framework and no database.**

`node:crypto` covers all of it, so the login path adds no dependency, no middleware chain, and no session store to operate.

## Password Hashing

`scrypt` is the memory-hard key derivation function `node:crypto` exposes. Memory hardness is what makes a stolen hash expensive to attack on a GPU, which a plain SHA-256 is not.

Each password gets a fresh 16-byte salt, and the stored value is `salt:derivedKey` in hex. A per-user salt means two users with the same password produce different hashes, so one cracked hash reveals nothing about the other account.

Verification compares with `timingSafeEqual`, because a normal comparison returns faster the earlier it finds a mismatched byte, and that timing difference is enough to recover the expected value one byte at a time.

```js
import { randomBytes, scrypt, timingSafeEqual } from 'node:crypto';
import { promisify } from 'node:util';

const scryptAsync = promisify(scrypt);
const KEY_LEN = 64;

export async function hashPassword(password) {
    const salt = randomBytes(16);
    const derived = await scryptAsync(password, salt, KEY_LEN);
    return `${salt.toString('hex')}:${derived.toString('hex')}`;
}

export async function verifyPassword(password, stored) {
    const [saltHex, keyHex] = stored.split(':');
    if (!saltHex || !keyHex) return false;
    const expected = Buffer.from(keyHex, 'hex');
    const derived = await scryptAsync(password, Buffer.from(saltHex, 'hex'), expected.length);
    return expected.length === derived.length && timingSafeEqual(expected, derived);
}
```

The length is checked before `timingSafeEqual`, which throws on mismatched buffer lengths rather than returning false.

## Sessions

A session is a signed token rather than an entry in a server-side store, so there is nothing to expire, evict, or replicate.

The signing secret is generated with `randomBytes(32)` at boot and never written to disk. Every restart mints a new secret and invalidates all outstanding sessions, which is the accepted trade-off for a single-process app: a persisted secret would outlive the process and need rotating by hand.

The token is `base64url(payload).hmacSignature`. Validation recomputes the HMAC, compares it with `timingSafeEqual`, and only then parses the payload and checks expiry. Verifying before parsing means attacker-controlled bytes never reach `JSON.parse` unless they were signed by this process.

```js
import { randomBytes, createHmac, timingSafeEqual } from 'node:crypto';

const SESSION_SECRET = randomBytes(32);
const SESSION_TTL_MS = 12 * 60 * 60 * 1000;

function sign(body) {
    return createHmac('sha256', SESSION_SECRET).update(body).digest('base64url');
}

export function createSession(username) {
    const payload = JSON.stringify({ username, exp: Date.now() + SESSION_TTL_MS });
    const body = Buffer.from(payload).toString('base64url');
    return `${body}.${sign(body)}`;
}

export function validateSession(token) {
    if (!token) return null;
    const [body, sig] = token.split('.');
    if (!body || !sig) return null;

    const expected = sign(body);
    const given = Buffer.from(sig);
    if (given.length !== expected.length || !timingSafeEqual(given, Buffer.from(expected))) {
        return null;
    }

    let claims;
    try {
        claims = JSON.parse(Buffer.from(body, 'base64url').toString());
    } catch {
        return null;
    }
    return claims.exp > Date.now() ? claims.username : null;
}
```

Every failure path returns `null` rather than throwing, so a caller has one check instead of a `try` around every validation.

## Cookies

```js
const MAX_AGE = 12 * 60 * 60;

export function sessionCookie(token) {
    return `session=${token}; HttpOnly; SameSite=Lax; Path=/; Max-Age=${MAX_AGE}`;
}

export function clearedCookie() {
    return `session=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0`;
}

export function readCookie(req, name) {
    const header = req.headers.cookie;
    if (!header) return null;
    for (const part of header.split(';')) {
        const eq = part.indexOf('=');
        if (eq === -1) continue;
        if (part.slice(0, eq).trim() === name) return part.slice(eq + 1).trim();
    }
    return null;
}
```

| Attribute | Why |
|---|---|
| `HttpOnly` | keeps the token out of `document.cookie`, so a script injected into the page cannot read it |
| `SameSite=Lax` | blocks the cookie on cross-site subrequests while still allowing top-level navigation, which is CSRF mitigation without breaking inbound links |
| `Path=/` | the whole app is behind the same session |
| `Max-Age` | bounds how long a stolen cookie is useful |

`Secure` is added whenever the server sits behind TLS, which stops the cookie from ever crossing a plaintext connection.

Clearing sets `Max-Age=0` with the same attributes, since a browser only replaces a cookie when the name, path, and domain all match.

## users.json

Credentials live in a JSON file the server reads and never writes.

```json
{
    "admin": { "password": "a1b2...:9f8e..." }
}
```

The file is re-read on every login attempt rather than cached at boot, so an operator can add or remove a user without restarting the process.

An unknown username still runs a verification against a fixed dummy hash. Skipping it would return noticeably faster than a wrong password does, and that difference tells an attacker which usernames exist.

```js
import { readFile } from 'node:fs/promises';

const DUMMY_HASH = '0'.repeat(32) + ':' + '0'.repeat(128);

export async function authenticate(usersFile, username, password) {
    const users = JSON.parse(await readFile(usersFile, 'utf8'));
    const record = users[username];
    if (!record) {
        await verifyPassword(password, DUMMY_HASH);
        return false;
    }
    return verifyPassword(password, record.password);
}
```

Stored values are produced with `hashPassword`, from a one-off script or an admin endpoint. A plaintext password in the file defeats every other measure here.

## Wiring

The helpers throw or return, and the request handler decides the HTTP response. Keeping the decision at the boundary is what lets the same `authenticate` back a login form, a token endpoint, and a test.

```js
import { authenticate, createSession, sessionCookie, readCookie, validateSession } from './auth.js';

export async function handleLogin(req, res, body, config) {
    const ok = await authenticate(config.usersFile, body.username, body.password);
    if (!ok) {
        res.writeHead(401).end();
        return;
    }
    res.writeHead(204, { 'Set-Cookie': sessionCookie(createSession(body.username)) }).end();
}

export function requireSession(req) {
    return validateSession(readCookie(req, 'session'));
}
```

A failed login returns a bare 401 with no message distinguishing an unknown user from a wrong password, so the response leaks no more than the timing already does not.
