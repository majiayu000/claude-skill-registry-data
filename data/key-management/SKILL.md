---
name: key-management
description: "The central pattern."
---

# Key Management (Verbose)

## Core Patterns

### Envelope Encryption

The central pattern. Data is encrypted with a short-lived Data Encryption Key
(DEK); the DEK is encrypted ("wrapped") by a Key Encryption Key (KEK) held in a
KMS or HSM. Only the wrapped DEK is stored, next to the ciphertext.

```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_record(record_id: str, plaintext: bytes) -> dict:
    resp = kms.generate_data_key(KeyId="alias/app-kek", KeySpec="AES_256")
    dek, wrapped = resp["Plaintext"], resp["CiphertextBlob"]
    try:
        nonce = os.urandom(12)
        ct = AESGCM(dek).encrypt(nonce, plaintext, record_id.encode())
    finally:
        del dek                     # minimise the plaintext key's lifetime in memory
    return {"kv": CURRENT_KEK_VERSION, "alg": "AES-256-GCM",
            "wrapped_dek": wrapped, "nonce": nonce, "ct": ct}

def decrypt_record(record_id: str, row: dict) -> bytes:
    dek = kms.decrypt(CiphertextBlob=row["wrapped_dek"])["Plaintext"]
    return AESGCM(dek).decrypt(row["nonce"], row["ct"], record_id.encode())
```

Properties this gives you that direct KMS encryption cannot:

| Concern | Direct KMS encrypt | Envelope encryption |
|---|---|---|
| Payload size limit | ~4 KB | Unbounded |
| Throughput | One API call per operation | Local AES; cache DEKs per batch |
| KEK exposure | Never leaves KMS | Never leaves KMS |
| KEK rotation cost | Re-encrypt all data | Re-wrap DEKs only |

The last row is why envelope encryption exists: rotating a KEK over a petabyte of
data means rewriting a few bytes per record, not a petabyte.

Pass the record identifier as associated data. It binds the ciphertext to its
row, so an attacker with write access to the datastore cannot relocate one user's
encrypted field onto another user's record.

### Key Hierarchy

```
Root of trust (HSM / cloud KMS, non-exportable)
  └── KEK per (service, environment)          rotated ~annually
        └── DEK per record / object / batch   generated per write, never reused
```

Add a tenant layer where you need per-customer isolation or "crypto-shredding" —
deleting a tenant's KEK renders their ciphertext permanently unreadable, often
the only practical way to honour a deletion request against immutable backups.

Separate keys by purpose as well as scope: sessions, database columns, backups,
and signing each get their own. One key serving everything means one leak is a
total compromise with no partial containment.

### Generation and Storage

Generate inside the boundary that will hold the key. `generate_data_key` and
KMS-internal key creation mean the key never exists in a place you have to trust
yourself to clean up.

| Storage | Extractable | Use for |
|---|---|---|
| Cloud KMS (AWS/GCP/Azure) | No | KEKs, signing keys — the default |
| HSM / CloudHSM | No | Regulatory requirement, root CAs |
| Vault Transit | No (Vault operates on data) | Multi-cloud, on-prem |
| Encrypted file + passphrase | Yes | Local dev only |
| Environment variable, repo, config map | Yes | Never for key material |

Assume anything in the extractable rows has already leaked into logs, backups,
images, and a laptop somewhere.

### Rotation

Rotation must be routine and boring. A procedure you have never executed is not a
control, it is a document — and you will be finding its bugs during an incident.

```python
# Re-wrap without touching ciphertext: KEK rotation over an envelope-encrypted table
for row in rows_where(kv__lt=CURRENT_KEK_VERSION):
    dek = kms.decrypt(CiphertextBlob=row.wrapped_dek)["Plaintext"]
    new_wrapped = kms.encrypt(KeyId="alias/app-kek", Plaintext=dek)["CiphertextBlob"]
    update(row.id, wrapped_dek=new_wrapped, kv=CURRENT_KEK_VERSION)
```

| Key | Cadence | Trigger for immediate rotation |
|---|---|---|
| KEK | 12 months, automatic | Suspected KMS policy compromise |
| DEK | Every write | n/a — never reused |
| Signing key (JWT, artifacts) | 6–12 months | Key exposure, insider departure |
| TLS certificate | ≤ 90 days, ACME-automated | Private key exposure |
| Database / service credential | 30–90 days | See the secret-management skill |

Every rotation is a two-phase rollout. Phase one: the new key is *accepted* but
not used — verifiers trust both, decryptors can unwrap with both. Phase two: the
new key becomes *active* for new writes. Only after every artifact signed or
encrypted under the old key has expired or been migrated do you retire it.

For signing keys the mechanism is the JWKS: publish both keys with distinct `kid`
values, let the token header name which one signed it, and consumers select by
`kid`. The cutover is then invisible to every client.

### Access Control and Auditing

```json
{
  "Effect": "Allow",
  "Principal": {"AWS": "arn:aws:iam::111122223333:role/orders-api"},
  "Action": ["kms:Decrypt", "kms:GenerateDataKey"],
  "Resource": "*",
  "Condition": {"StringEquals": {"kms:EncryptionContext:tenant": "${aws:PrincipalTag/tenant}"}}
}
```

Grant the narrowest verb set to a named role — most services need
`GenerateDataKey` and `Decrypt`, nothing else. Encryption context lets you enforce
tenant scoping in the key policy itself, so a compromised service still cannot
decrypt across the tenant boundary.

Alert on `ScheduleKeyDeletion` and `DisableKey` (always), decrypt calls from an
unexpected role or region, and sustained decrypt-rate anomalies — bulk
exfiltration of an encrypted table shows up as a decrypt spike long before anyone
notices missing data.

### Destruction

Deleting a key destroys the data it protects. Cloud KMS enforces a mandatory
waiting period (7–30 days on AWS) precisely because this mistake is unrecoverable.
Before scheduling deletion, confirm no ciphertext references that key version —
the `kv` field on every record is what makes that query possible.

## Common Anti-Patterns

❌ **Calling KMS `Encrypt` directly on application payloads** — a 4 KB limit, a
network round trip per record, and rotation that means re-encrypting everything.
✅ Envelope encryption with per-record DEKs.

❌ **One key for all data, all environments** — no blast-radius containment, and
staging access becomes production access.
✅ A key per (purpose, environment), separated at the account/project level.

❌ **Ciphertext with no key version or algorithm recorded** — rotation becomes
impossible because nothing can tell you what decrypts what.
✅ Store `{kv, alg}` with every ciphertext and select the key by that field.

❌ **Rotating by replacing the key in place** — every existing ciphertext and
every in-flight token instantly fails.
✅ Two-phase rollout: accept both, then activate the new one, then retire the old.

❌ **Private keys in the repo, the container image, or a CI variable** — images
get pushed to shared registries and CI logs get archived.
✅ Non-exportable keys in KMS/HSM, referenced by alias.

❌ **Caching plaintext DEKs indefinitely** — a heap dump or crash report becomes a
key disclosure.
✅ Cache per batch with a short TTL; drop the reference promptly.

❌ **A rotation runbook that has never been executed, or `kms:*` on `Resource: "*"`.**
✅ Rotate annually in production as a normal change; grant specific verbs to
specific roles with encryption-context conditions.

## Key Management Checklist

- [ ] All bulk encryption uses envelope encryption with per-record DEKs
- [ ] KEKs are non-exportable and generated inside a KMS or HSM
- [ ] No private key material in repos, images, CI config, or environment variables
- [ ] Keys are separated by purpose, environment, and tenant where isolation is required
- [ ] Every ciphertext records its key version and algorithm
- [ ] Associated data / encryption context binds ciphertext to its record and tenant
- [ ] KEK rotation is automated and has been executed at least once in production
- [ ] Signing key rollover publishes both keys with distinct `kid` during overlap
- [ ] Plaintext DEKs are short-lived in memory and never logged or serialized
- [ ] KMS IAM grants name specific verbs and specific roles
- [ ] Alerts fire on key disable/delete and on decrypt-rate anomalies
- [ ] Key deletion is gated on verifying no ciphertext references that version
- [ ] Crypto-shredding path exists and is tested where deletion guarantees are promised
- [ ] Break-glass key recovery is documented, access-controlled, and rehearsed
