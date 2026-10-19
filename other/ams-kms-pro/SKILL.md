---
name: kms-pro
description: Design key management with KMS/HSM — envelope encryption, key hierarchy, rotation, and access governance.
category: security
---

## Overview

Encryption is only as strong as key management. KMS (Key Management Service) and HSM (Hardware Security Module) practice answers: where keys live, who can use them, how they rotate, and what happens when they are compromised. Done right, a stolen database is unreadable; done wrong, the key sits next to the lock.

This skill covers key-management architecture: envelope encryption, key hierarchies, rotation, separation of duties, and the operational realities (backup, disaster recovery, cost) teams forget until they matter.

Key management is the rare security domain where the failure mode is total and silent: lose the keys and the data is gone; leak the keys and the encryption was theater. Both failures are operational, not cryptographic — which is why the boring parts (backup drills, access reviews, rotation automation) matter more than algorithm choice.

## When to use

- Designing encryption for data at rest (databases, object storage, backups).
- Choosing between cloud KMS, self-managed vault, and HSM.
- Implementing envelope encryption in applications.
- Planning key rotation, compromise response, and multi-region key strategy.
- Meeting compliance requirements for key custody (PCI DSS, FIPS 140-3).

## Core concepts

- **Envelope encryption:** a data-encryption key (DEK) encrypts the data; a key-encryption key (KEK) encrypts the DEK. DEKs stay near the data (encrypted), KEKs stay in the KMS/HSM. Compromise of a DEK affects one dataset; compromise handling stays centralized.
- **Key hierarchy:** master/root keys → KEKs → DEKs. Higher keys change rarely and are heavily protected; lower keys rotate freely.
- **Never hardcode keys:** keys live in KMS/HSM/vault, referenced by ID or alias — never in code, config files, or environment dumps.
- **Separation of duties:** those who manage keys should not be those who use the data, and ideally cannot decrypt it. Dual control for root-key operations.
- **HSM vs cloud KMS:** HSMs give dedicated FIPS-validated hardware and strongest custody story (often required for payments/PKI roots); cloud KMS gives managed rotation, IAM integration, and audit with less operational burden. Many orgs use both: HSM for roots, KMS for working keys.
- **Crypto-agility:** algorithms and key lengths change (post-quantum is coming). Design key IDs, versioning, and rotation so migration does not require re-architecture.

- **Key usage policies.** Bind keys to specific purposes and algorithms at creation; a key minted for AES-GCM should never be usable for RSA signing. Purpose-binding limits blast radius.
- **Bring-your-own-key (BYOK) trade-offs.** BYOK gives customers control and you operational complexity — key import ceremonies, dual control, and revocation semantics all need design.
- **Envelope encryption at scale.** Per-tenant or per-record DEKs with centralized KEKs give you revocation granularity (revoke one tenant) without key-management sprawl.

## Practical workflow

1. **Classify and map:** which data needs encryption at rest, where it lives, and what regulations apply. This sets whether you need HSM-grade custody or KMS suffices.
2. **Design the hierarchy:** root/KEK in HSM or KMS with restricted admin roles; per-service or per-tenant DEKs via envelope encryption; aliases for stable references across rotation.
3. **Define rotation policy:** automatic rotation for KEKs (e.g., annual) and DEKs (per write or scheduled); versioned keys so old data remains decryptable during transition; tested re-encryption procedures.
4. **Lock down access:** IAM policies granting decrypt to specific service identities only; key-administration separated from key-use; all key operations logged to immutable audit storage with alerts on unusual use.
5. **Plan for failure:** tested backup of key material (HSM backup devices, KMS multi-region replication); documented compromise response (rotate, re-encrypt, assess exposure window); disaster-recovery drills that include key recovery.
6. **Monitor and review:** dashboards for key age, rotation compliance, and anomalous decrypt volume; periodic review that each key is still needed and correctly scoped.

### Key-management checklist

- [ ] Data classification mapped to encryption requirements
- [ ] Envelope encryption with versioned keys; no hardcoded keys anywhere
- [ ] Rotation automated and verified (old versions retained per policy, then destroyed)
- [ ] Separation of duties: key admins ≠ data users; dual control on root operations
- [ ] All key usage logged immutably; alerts on anomalies
- [ ] Backup/restore tested; compromise runbook written and drilled
- [ ] Crypto-agility: key IDs and versioning support algorithm migration

### Sustaining the practice

- Audit key inventory annually: every key needs an owner, purpose, and rotation status
- Drill key compromise response — rotation under fire is a skill, not a document
- Track algorithm inventory for post-quantum migration planning
- Review KMS IAM policies with the same rigor as data-access policies

### Metrics that prove it works

- Key rotation compliance % (keys rotated within policy)
- % of keys with a named owner and documented purpose
- Anomalous key-usage alerts investigated within SLA
- Key-recovery drill success rate

## Common pitfalls

- **Encrypting without a key plan.** Data encrypted with keys nobody can rotate, back up, or revoke is a future outage, not security.
- **Keys next to data.** Storing the decryption key in the same repo, bucket, or config as the encrypted data negates the encryption.
- **Single admin with root access.** One person who can export the master key is a single point of compromise and coercion. Dual control.
- **Forgetting old key versions.** Rotating the KEK without retaining prior versions (per retention policy) makes historical backups unreadable.
- **No compromise runbook.** Discovering during an incident that you have no tested key-rotation-under-fire procedure.
- **Ignoring post-quantum timelines.** Inventory where long-lived encrypted data and key exchange happen now; track PQC migration guidance so you are not redesigning under pressure later.
- **Single-provider key dependency with no exit plan.** If you cannot migrate keys, the provider owns your data availability. Document and periodically test portability.
- **Over-granular key sprawl.** A unique key per row with no lifecycle tooling becomes unmanageable. Granularity should match your rotation and revocation capability.
- **Confusing encryption with access control.** Encrypted data that every service account can decrypt is not protected — key access policy is the real control.
- **Manual key ceremonies without witnesses.** Root-key operations need dual control and logged ceremony procedures, or you have a single point of trust and failure.
