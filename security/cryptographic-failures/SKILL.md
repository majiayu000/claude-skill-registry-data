---
name: cryptographic-failures
description: >
  Detect, audit, and remediate A04:2025 Cryptographic Failures in Python web applications
  (FastAPI and Flask). Use this skill whenever the user asks about crypto security, password
  hashing, JWT configuration, TLS/SSL verification, weak randomness, hardcoded secrets,
  or any code using hashlib, random, ssl, jwt, passlib, or cryptography modules. Also trigger
  when the user wants to audit security, scan for OWASP A04 issues, fix crypto bugs, or
  review authentication-related cryptographic code. If there's any chance a crypto weakness
  is involved — trigger this skill.
---

# A04:2025 — Cryptographic Failures

**OWASP Rank:** #4 (dropped from #2 due to improved TLS adoption)
**Incidence:** 3.80% of applications, 1.6M+ occurrences, 32 CWEs

Cryptographic Failures cover the **absence, misuse, or weakness of cryptography** protecting data
at rest and in transit. In Python, there is a distinctive set of pitfalls that differ from Java/.NET.

---

## What This Skill Covers

| Area | Key Risk | Python-Specific Pitfall |
|---|---|---|
| Password hashing | Weak/missing algorithm | Using `hashlib.md5`/`sha1` instead of bcrypt/Argon2 |
| Randomness | Predictable values | `import random` instead of `import secrets` |
| Hardcoded keys | Key leakage | `SECRET_KEY = "..."` literals in source |
| TLS/SSL | Cert bypass | `verify=False` in requests/httpx |
| JWT secrets | Key strength/algorithm | Weak secret, missing algo pinning |
| Symmetric encryption | Deprecated modes | ECB mode, no authenticated encryption |

---

## Step-by-Step Audit Workflow

### 1. Static Scan with Bandit

Run Bandit — the primary Python SAST tool for catching crypto issues automatically:

```bash
pip install bandit
bandit -r . -t B303,B304,B305,B306,B311,B324,B501,B502,B503,B504,B505,B506 -f json -o bandit_crypto.json
```

Key Bandit test IDs for cryptographic failures:

| Bandit ID | What It Catches | Severity |
|---|---|---|
| B303 | MD5/SHA1 usage | Medium |
| B304/B305 | Weak cipher modes (ECB, DES) | High |
| B311 | `random` module in security context | Low |
| B324 | Hashlib use of weak hash | Medium |
| B501 | `verify=False` in SSL context | High |
| B502/B503/B504 | Insecure SSL/TLS versions | Medium–High |
| B105/B106 | Hardcoded password/secret | Medium |

### 2. Manual Code Pattern Review

Work through these patterns in priority order:

#### 🔴 CRITICAL — Password Hashing

```python
# BAD — MD5/SHA1 for passwords: CWE-328, CWE-759, CWE-916
hashlib.md5(password.encode()).hexdigest()
hashlib.sha1(password.encode()).hexdigest()
hashlib.sha256(password.encode()).hexdigest()  # also bad — no salt, no stretching

# GOOD — use passlib with bcrypt or argon2
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
# OR
pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=12, deprecated="auto")
hashed = pwd_context.hash(plain_password)
```

**Check for:**
- Any `hashlib.*` call used to hash a password or token
- Missing salt (hash of raw password without `hashlib.pbkdf2_hmac`)
- bcrypt with `rounds < 12` — should be ≥12 to resist brute force

#### 🔴 CRITICAL — Weak Randomness (CWE-330)

```python
# BAD — random is NOT cryptographically secure
import random
token = random.randint(100000, 999999)       # predictable OTP
reset_key = random.choice(string.ascii_letters + string.digits)  # guessable

# GOOD
import secrets
token = secrets.randbelow(900000) + 100000   # secure OTP
reset_key = secrets.token_urlsafe(32)        # secure reset token
session_id = secrets.token_hex(16)           # secure session ID
```

**Check for:** Any `random.random()`, `random.randint()`, `random.choice()`, `random.shuffle()`
in code paths involving tokens, OTPs, session IDs, keys, or nonces.

#### 🔴 HIGH — Hardcoded Cryptographic Keys (CWE-321)

```python
# BAD — key in source code
SECRET_KEY = "my-super-secret-key"
JWT_SECRET = "hardcoded_jwt_secret_123"
app.config['SECRET_KEY'] = "flask_secret"

# GOOD — load from environment
import os
SECRET_KEY = os.environ["SECRET_KEY"]        # raises KeyError if missing (intentional)
SECRET_KEY = os.getenv("SECRET_KEY")         # returns None silently (verify it's not None)
```

Minimum key lengths:
- Flask `SECRET_KEY`: ≥32 random bytes (use `secrets.token_hex(32)`)
- JWT HMAC secrets: ≥32 characters
- AES keys: 128, 192, or 256 bits (16, 24, or 32 bytes)

#### 🔴 HIGH — TLS/SSL Certificate Bypass (CWE-295)

```python
# BAD — disables certificate validation entirely
requests.get(url, verify=False)
httpx.get(url, verify=False)
ssl._create_unverified_context()
urllib3.disable_warnings()  # companion to verify=False

# GOOD
requests.get(url)               # verify=True is the default
requests.get(url, verify="/path/to/ca-bundle.crt")  # custom CA
```

#### 🟡 MEDIUM — JWT Configuration (CWE-327)

```python
# BAD — algorithm confusion attacks
jwt.decode(token, key, algorithms=["none"])  # NEVER allow "none"
jwt.decode(token, key)                       # no algorithm pin = vulnerable

# BAD — weak secret loaded without validation
JWT_SECRET = os.getenv("JWT_SECRET", "default")  # fallback default is dangerous

# GOOD
JWT_SECRET = os.environ["JWT_SECRET"]        # fail hard if missing
assert len(JWT_SECRET) >= 32, "JWT secret too short"
jwt.decode(token, JWT_SECRET, algorithms=["HS256"])  # explicit allowlist
```

Also check:
- Token expiry (`exp` claim) — access tokens should be 15–30 min
- `aud` and `iss` claims are validated on decode

#### 🟡 MEDIUM — Deprecated Symmetric Encryption (CWE-327)

```python
# BAD — ECB mode leaks patterns in data
from Crypto.Cipher import AES
cipher = AES.new(key, AES.MODE_ECB)

# BAD — no authentication = vulnerable to tampering
cipher = AES.new(key, AES.MODE_CBC, iv)

# GOOD — authenticated encryption
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
aesgcm = AESGCM(key)
ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
# ChaCha20-Poly1305 is also acceptable
```

---

## FastAPI-Specific Checks

```python
# 1. Verify OAuth2/JWT middleware algorithm pinning
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

ALGORITHM = "HS256"  # must be explicit, not a variable that could be overridden
# Check: is ALGORITHM loaded from config where it could be tampered with?

# 2. Verify password hashing in user creation/login endpoints
@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed = pwd_context.hash(user.password)  # must NOT store plain or MD5

# 3. Token generation for password resets / email verification
def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)   # GOOD
    # NOT: str(uuid.uuid4())  — UUID v4 uses os.urandom, acceptable but secrets is preferred
    # NOT: random-based anything
```

## Flask-Specific Checks

```python
# 1. Session cookie signing uses SECRET_KEY — must be strong
app.secret_key = os.environ["SECRET_KEY"]  # GOOD
app.secret_key = "dev"                     # BAD — common in tutorials, dangerous in prod

# 2. Flask-Login password verification
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
bcrypt.generate_password_hash(password, rounds=12)  # rounds≥12

# 3. HTTPS enforcement via HSTS
from flask_talisman import Talisman
Talisman(app, force_https=True)  # adds HSTS header
```

---

## Key CWEs Reference

| CWE | Name | Common Manifestation |
|---|---|---|
| CWE-327 | Use of Broken/Risky Crypto Algorithm | MD5, SHA1, ECB, DES, RC4 |
| CWE-328 | Reversible One-Way Hash | MD5/SHA1 for passwords (reversible via rainbow tables) |
| CWE-330 | Insufficiently Random Values | `random` module for tokens/keys |
| CWE-321 | Hard-coded Cryptographic Key | Secrets in source code |
| CWE-759 | One-Way Hash Without a Salt | `hashlib.sha256(password)` — no salt |
| CWE-916 | Password Hash With Insufficient Effort | bcrypt rounds<12, PBKDF2 iterations<600k |
| CWE-295 | Improper Certificate Validation | `verify=False` in HTTP clients |

---

## Remediation Checklists

### Minimum Viable Crypto Stack (Python 2025)

```
Password hashing:   passlib[argon2] or passlib[bcrypt] (rounds≥12)
Token generation:   secrets module exclusively
Symmetric crypto:   cryptography library, AES-GCM or ChaCha20-Poly1305
JWT:                python-jose or PyJWT, algorithm pinned, secret≥32 chars
TLS:                verify=True always; pin CA bundle where needed
Config/secrets:     os.environ (fail-hard) or a secrets manager (Vault, AWS SSM)
HSTS:               flask-talisman (Flask) or custom middleware (FastAPI)
```

### Quick Regex Patterns for Code Search

```bash
# Find weak hashing
grep -rn "hashlib\.md5\|hashlib\.sha1\|hashlib\.sha224" --include="*.py"

# Find insecure random
grep -rn "import random\b" --include="*.py"
grep -rn "random\.randint\|random\.choice\|random\.random()" --include="*.py"

# Find hardcoded secrets
grep -rn "SECRET_KEY\s*=\s*['\"]" --include="*.py"
grep -rn "verify=False" --include="*.py"

# Find ECB mode
grep -rn "MODE_ECB\|AES\.MODE_ECB" --include="*.py"
```

---

## See Also

- `references/owasp-a04-full.md` — full OWASP A04:2025 spec and extended CWE list
- For supply chain crypto issues (pinned dependency hashes), see the `software-supply-chain` skill
- For JWT-related auth logic beyond crypto (expiry, claims), see the `authentication-failures` skill