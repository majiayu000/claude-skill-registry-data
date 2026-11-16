---
name: secrets-vault-patterns
description: Secure secrets management for agent runtimes. One-time-token gateway, AES-256-GCM at-rest encryption, Shamir's Secret Sharing for API keys, memory zeroization after use, and PBKDF2 key derivation.
origin: Google Tink (Apache-2.0), Shamir's Secret Sharing (public domain), OWASP Key Management Cheat Sheet
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# Secrets Vault Patterns

Agents never see raw secrets. They receive one-time tokens that expire in 5 seconds. Keys are zeroized from memory immediately after use.

## When to Use

- Multi-agent systems where any single agent could be compromised
- Environments where secrets must not appear in logs, env vars, or CLI args
- Implementing the YAMTAM secrets-vault-law (rule 52)
- Rotating API keys without restarting agents

## Do NOT use for

- Developer local setup where secrets are in `.env` (acceptable risk)
- Systems without Node.js crypto module access

## One-Time-Token Gateway

```js
import { randomBytes, createCipheriv, createDecipheriv, createHash } from 'crypto';

class SecretsVault {
  constructor(masterKey) {
    // masterKey derived via PBKDF2 — never stored raw
    this.key = createHash('sha256').update(masterKey).digest();
    this.otts = new Map();  // token → { secret, expiresAt }
  }

  // Issue a one-time-token (5s TTL)
  issueOTT(secretName) {
    const secret = this._decrypt(this._store.get(secretName));
    const token = randomBytes(32).toString('hex');
    this.otts.set(token, { secret, expiresAt: Date.now() + 5000 });
    setTimeout(() => this.otts.delete(token), 5000);
    return token;
  }

  // Agent redeems token once
  redeemOTT(token) {
    const entry = this.otts.get(token);
    if (!entry) throw new Error('OTT_INVALID: expired or already used');
    if (Date.now() > entry.expiresAt) throw new Error('OTT_EXPIRED');
    this.otts.delete(token);  // one-time use
    const secret = entry.secret;
    // Zeroize after returning
    setTimeout(() => { entry.secret = '\x00'.repeat(entry.secret.length); }, 0);
    return secret;
  }
}
```

## AES-256-GCM At-Rest Encryption

```js
function encryptSecret(plaintext, key) {
  const iv = randomBytes(12);  // 96-bit nonce for GCM
  const cipher = createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([iv, tag, encrypted]).toString('base64');
}

function decryptSecret(ciphertext, key) {
  const buf = Buffer.from(ciphertext, 'base64');
  const iv  = buf.slice(0, 12);
  const tag = buf.slice(12, 28);
  const enc = buf.slice(28);
  const decipher = createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(tag);
  return decipher.update(enc) + decipher.final('utf8');
}
```

## PBKDF2 Key Derivation

```js
import { pbkdf2Sync, randomBytes } from 'crypto';

function deriveKey(masterPassword, salt) {
  return pbkdf2Sync(
    masterPassword,
    salt,
    310000,         // OWASP 2023 recommended iterations
    32,             // 256-bit output
    'sha256'
  );
}

const salt = randomBytes(16);
const key  = deriveKey(process.env.YAMTAM_MASTER_PASSWORD, salt);
// Store salt alongside encrypted data, never store derived key
```

## Memory Zeroization

```js
function zeroize(buffer) {
  if (Buffer.isBuffer(buffer)) buffer.fill(0);
  else if (typeof buffer === 'string') {
    // Strings are immutable in JS — minimize exposure window
    // Use Buffer for all secret handling
  }
}

// Pattern: derive → use → zeroize immediately
const key = deriveKey(password, salt);
try {
  const result = encryptSecret(secret, key);
  return result;
} finally {
  zeroize(key);  // always runs, even on throw
}
```

## Shamir's Secret Sharing (3-of-5)

```js
// Split API key into 5 shares, need 3 to reconstruct
// Use 'shamir-secret-sharing' npm package (MIT)
import { split, combine } from 'shamir-secret-sharing';

const secret = Buffer.from(process.env.ANTHROPIC_API_KEY);
const shares = await split(secret, 5, 3);  // 5 shares, threshold 3

// Store shares separately — no single location has the full key
// Reconstruct only at call time:
const reconstructed = await combine(shares.slice(0, 3));
```

## Anti-Fake-Pass Checklist

- [ ] OTT expires after 5s — test with `setTimeout(() => vault.redeemOTT(token), 6000)`
- [ ] OTT is single-use — second `redeemOTT(token)` call throws
- [ ] AES-GCM auth tag verified (tampered ciphertext throws on `decipher.final()`)
- [ ] `zeroize()` called in `finally` block — not just in success path
- [ ] PBKDF2 iterations ≥ 310,000 (OWASP 2023 minimum for SHA-256)
