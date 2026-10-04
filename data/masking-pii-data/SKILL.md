---
name: masking-pii-data
description: Protect personally identifiable information in data pipelines — classifying PII, choosing masking vs tokenization vs hashing vs encryption, dynamic data masking and column-level access control, and handling deletion/right-to-be-forgotten. Use when handling sensitive data, masking or anonymizing PII, meeting GDPR/CCPA/HIPAA requirements, or restricting column access in a warehouse.
---

# Masking PII Data

## When to use

- A pipeline or table contains personal/sensitive data (names, emails, SSNs,
  payment, health).
- Choosing how to de-identify data for analytics or lower environments.
- Restricting who can see raw sensitive columns.
- Handling deletion / right-to-be-forgotten requests.
- Do NOT use for general access control unrelated to sensitive data.

## Choose the right technique

| Technique           | Reversible      | Keeps analytics utility | Use for                               |
| ------------------- | --------------- | ----------------------- | ------------------------------------- |
| Masking / redaction | No              | Low                     | Display, lower envs (`j***@x.com`)    |
| Hashing (salted)    | No              | Join/match only         | Pseudonymous keys, dedup              |
| Tokenization        | Yes (via vault) | Referential joins       | Reversible pseudonymization           |
| Encryption          | Yes (with key)  | None until decrypt      | At-rest protection, restricted fields |

## Workflow

```
- [ ] Classify columns: what is PII/sensitive and its risk level
- [ ] Pick technique per column by whether you need reversibility/joins
- [ ] Apply as early as possible (mask on ingest for lower environments)
- [ ] Enforce column-level access / dynamic masking for raw data
- [ ] Support deletion: know every location a subject's data lives
```

1. **Classify first.** You can't protect what you haven't identified; tag columns
   by sensitivity. Pair with `designing-data-contracts` to declare PII fields.
2. **Pick per column.** Need to join across systems but not reverse? Salted hash.
   Need to recover the value later? Tokenization/encryption. Just hide it? Mask.
3. **Apply early.** Mask/tokenize before data reaches analysts or dev/test
   environments; never copy raw PII into lower environments.
4. **Access control.** Use warehouse dynamic data masking and column-level grants
   so only authorized roles see raw values.
5. **Deletion.** Track where each subject's data lives (lineage helps) so
   erasure requests are complete.

## Patterns

**Snowflake dynamic masking policy** (unmask only for a privileged role):

```sql
CREATE MASKING POLICY email_mask AS (val string) RETURNS string ->
  CASE WHEN CURRENT_ROLE() IN ('PII_READER') THEN val
       ELSE REGEXP_REPLACE(val, '^[^@]+', '***') END;
ALTER TABLE customers MODIFY COLUMN email SET MASKING POLICY email_mask;
```

**Salted hash for pseudonymous joins** — hash with a secret salt so the same
person matches across tables without exposing the raw identifier; keep the salt in
a secrets manager.

**Tokenization** — replace the value with a token and store the mapping in a
restricted vault; analytics use the token, authorized systems detokenize.

## Common pitfalls

- **Copying raw PII to dev/test** — the most common leak; mask on the way down.
- **Unsalted hashes** — vulnerable to rainbow tables and re-identification; always
  salt.
- **Masking at display only** while storing raw everywhere — breach still exposes
  data; protect at rest and restrict access.
- **Forgetting free-text/logs** — PII hides in comments, logs, and JSON blobs, not
  just typed columns.
- **No deletion plan** — right-to-be-forgotten fails if you can't locate all
  copies; use lineage.
- **Reversible where you meant irreversible** — don't tokenize when the requirement
  is true anonymization.
