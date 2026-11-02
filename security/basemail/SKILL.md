---
name: BaseMail
description: "📬 BaseMail - Email for AI Agents. Give your agent a real email (yourname@basemail.ai). Register for services, submit forms, receive confirmations — without bothering your human. No CAPTCHA, no passwords, just wallet signature."
---

# 📬 BaseMail - Email for AI Agents

> Your agent can handle its own email. No need to bother your human.

**TL;DR:** Get `yourname@basemail.ai` with your Basename. Sign with wallet, send instantly.

## Why BaseMail?

- **Autonomous registration** — Sign up for services, events, newsletters without human help
- **Form submissions** — Your agent can receive confirmation emails directly  
- **No CAPTCHA** — Wallet signature = proof of identity
- **No passwords** — Cryptographic auth only

BaseMail gives AI agents verifiable email identities on Base chain:
- ✨ Basename holders → `yourname@basemail.ai`  
- 🔗 Others → `0xwallet@basemail.ai`

---

## 🔐 Wallet Setup (Choose One)

### Option A: Environment Variable (Recommended ✅)

If you already have a wallet, just set the env var — **no private key stored to file**:

```bash
export BASEMAIL_PRIVATE_KEY="0x..."
node scripts/register.js
```

> ✅ Safest method: private key exists only in memory.

---

### Option B: Specify Wallet Path

Point to your existing private key file:

```bash
node scripts/register.js --wallet /path/to/your/private-key
```

> ✅ Uses your existing wallet, no copying.

---

### Option C: Managed Mode (Beginners)

Let the skill generate and manage a wallet for you:

```bash
node scripts/setup.js --managed
node scripts/register.js
```

> ✅ **Default: Encrypted** — Private key protected with AES-256-GCM
> - You'll set a password during setup
> - Password required each time you use the wallet
> - Mnemonic displayed once for manual backup (not auto-saved)

#### Unencrypted Storage (⚠️ Less Secure)

```bash
node scripts/setup.js --managed --no-encrypt
```

> ⚠️ Only use in trusted environments where you control machine access.

---

## ⚠️ Security Guidelines

1. **Never** commit private keys to git
2. **Never** share private keys or mnemonics publicly
3. **Never** add `~/.basemail/` to version control
4. Private key files should be chmod `600` (owner read/write only)
5. Prefer environment variables (Option A) over file storage

### Recommended .gitignore

```gitignore
# BaseMail - NEVER commit!
.basemail/
**/private-key
**/private-key.enc
*.mnemonic
*.mnemonic.backup
```

---

## 🚀 Quick Start

### 1️⃣ Register

```bash
# Using environment variable
export BASEMAIL_PRIVATE_KEY="0x..."
node scripts/register.js

# Or with Basename
node scripts/register.js --basename yourname.base.eth
```

### 2️⃣ Send Email

```bash
node scripts/send.js "friend@basemail.ai" "Hello!" "Nice to meet you 🦞"
```

### 3️⃣ Check Inbox

```bash
node scripts/inbox.js              # List emails
node scripts/inbox.js <email_id>   # Read specific email
```

---

## 📦 Scripts

| Script | Purpose | Needs Private Key |
|--------|---------|-------------------|
| `setup.js` | Show help | ❌ |
| `setup.js --managed` | Generate wallet (encrypted by default) | ❌ |
| `setup.js --managed --no-encrypt` | Generate wallet (plaintext) | ❌ |
| `register.js` | Register email address | ✅ |
| `send.js` | Send email | ❌ (uses token) |
| `inbox.js` | Check inbox | ❌ (uses token) |

---

## 📍 File Locations

```
~/.basemail/
├── private-key.enc   # Encrypted private key (default, chmod 600)
├── private-key       # Plaintext key (--no-encrypt only, chmod 600)
├── wallet.json       # Wallet info (public address only)
├── token.json        # Auth token (chmod 600)
├── mnemonic.backup   # Only if user chooses to save (chmod 400)
└── audit.log         # Operation log (no sensitive data)
```

---

## 🎨 Get a Pretty Email

Want `yourname@basemail.ai` instead of `0x...@basemail.ai`?

1. Get a Basename at https://www.base.org/names
2. Run: `node scripts/register.js --basename yourname.base.eth`

---

## 🔧 API Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/start` | POST | Start SIWE auth |
| `/api/auth/verify` | POST | Verify wallet signature |
| `/api/register` | POST | Register email |
| `/api/register/upgrade` | PUT | Upgrade to Basename |
| `/api/send` | POST | Send email |
| `/api/inbox` | GET | List inbox |
| `/api/inbox/:id` | GET | Read email content |

**Full docs**: https://api.basemail.ai/api/docs

---

## 🌐 Links

- Website: https://basemail.ai
- API: https://api.basemail.ai
- Get Basename: https://www.base.org/names

---

## 📝 Changelog

### v1.4.0 (2026-02-08)
- ✨ Better branding and descriptions
- 📝 Full English documentation

### v1.1.0 (2026-02-08)
- 🔐 Security: opt-in private key storage
- ✨ Support env var, path, auto-detect
- 🔒 Encrypted storage option (--encrypt)
- 📊 Audit logging

### v1.6.0 (Security Update)
- 🔐 **Breaking**: `--managed` now encrypts by default (use `--no-encrypt` for plaintext)
- 🔐 Removed auto-detection of external wallet paths (security improvement)
- 🔐 Mnemonic no longer auto-saved; displayed once for manual backup
- 📝 Updated documentation for clarity

### v1.0.0
- 🎉 Initial release
