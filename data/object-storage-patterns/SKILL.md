---
name: object-storage-patterns
description: "Almost every object-storage mistake comes from carrying filesystem instincts into"
---

# Object Storage Patterns (Verbose)

## Core Patterns

### Object Storage Is Not a Filesystem

Almost every object-storage mistake comes from carrying filesystem instincts into
a system that only superficially resembles one. Object storage (S3, GCS, Azure
Blob) is a flat map from a string key to an immutable blob of bytes, reached over
HTTP. That is the whole model. What looks like a directory tree is an illusion the
tooling paints over a flat namespace.

```
bucket: analytics-prod
  key: raw/2026/07/26/events-0001.parquet
  key: raw/2026/07/26/events-0002.parquet
  key: raw/2026/07/27/events-0001.parquet
```

Those slashes are ordinary characters in a single key. There is no directory node.
The consequences are concrete and non-negotiable:

- **No cheap rename or move.** Changing a key means server-side *copy to the new
  key, then delete the old one* — a full rewrite of the bytes. "Renaming a folder"
  of a million objects is a million copy+delete operations.
- **No in-place append or edit.** Objects are immutable. Adding a line to a log
  object rewrites the entire object. Design for write-once, read-many.
- **No partial update.** To change one field you replace the whole object (aside
  from purpose-built multipart/range mechanics for large uploads/reads).

Model your writes as new immutable objects. If you need append semantics, write
many small objects and compact them in a batch job; if you need mutability, the
bytes belong in a database, not object storage.

### The Consistency Model

Object stores have converged on strong read-after-write **for new objects**: PUT a
new key, and a subsequent GET returns it. That is the guarantee you can lean on.

Two edges remain sharp:

1. **Overwrites and deletes** can be subtler than new writes. After overwriting an
   existing key, or deleting one, a reader may briefly observe the previous state
   depending on the store. Do not build correctness on immediately reading back an
   overwrite.
2. **Listing** is the classic lag. A `LIST` of a prefix may not include an object
   you wrote a moment ago, and may still show one you deleted. Listing is
   optimized for enumeration, not for point-in-time truth.

The pattern that avoids all of this: **object storage holds bytes; a database
holds truth.** Record "object X exists, here is its key and metadata" in a
transactional store, and use that as the index. Never drive control flow off a
live `LIST` in a tight loop — it is slow, paginated, eventually consistent, and
billed per request.

### Storage Classes and the Retrieval Trap

Storage classes trade storage price against retrieval price and latency. The names
differ per provider; the shape is universal.

| Class | Storage price | Retrieval | Latency | Fits |
|---|---|---|---|---|
| Standard / hot | Highest | None | Instant | Actively served data |
| Infrequent access | Lower | Per-GB fee + minimum storage duration | Instant | Backups, older data read occasionally |
| Archive / cold | Lowest | Fee + delay | Minutes to hours | Compliance, rarely-touched history |

The trap is retrieval cost, and it runs in both directions:

- Put **frequently-read** data in a cold/IA tier and the per-retrieval fees quickly
  exceed what you saved on storage — you optimized the cheap axis and blew up the
  expensive one.
- Cold tiers also carry a **minimum storage duration**: delete an object early and
  you are billed as if it lived the minimum. Churny short-lived data does not
  belong in archive tiers.

Choose the class from how often the object is actually read, and how much latency a
read can tolerate — not from its age alone.

### Lifecycle Automation

Data value decays with age for most workloads, and cost should decay with it —
automatically, not through someone remembering to clean up.

```
lifecycle rules on prefix  logs/
  - transition to Infrequent-Access at age 30d
  - transition to Archive           at age 90d
  - expire (delete)                 at age 365d

lifecycle rules on prefix  tmp/
  - expire at age 7d
  - abort incomplete multipart uploads at age 1d   # silent cost otherwise
```

Two rules people forget: expire genuinely dead data (a bucket that only grows is a
bill that only grows), and abort incomplete multipart uploads — failed large
uploads leave orphaned parts that accrue storage cost invisibly because they never
appear as a finished object.

### Access Control and Sharing

The default posture is private, with public access explicitly blocked at the
account and bucket level. Data leaks from object storage are overwhelmingly
misconfigured public buckets. Grant access three ways instead:

- **IAM roles** for services — the app's role is allowed to read/write specific
  prefixes. No credentials in code, nothing public.
- **Pre-signed URLs** for browsers/clients — a time-limited, signed URL that grants
  read or write to *one specific object* for a short window. The browser uploads or
  downloads directly, so bytes never proxy through your servers, and the grant
  expires on its own.

```
# server mints a short-lived signed URL; client PUTs directly to storage
url = storage.presign_put(bucket, key, expires_in=300)   # 5 minutes, one object
```

- **Bucket policies** scoped to specific principals and prefixes for cross-account
  or cross-service sharing — never a blanket public grant.

Encrypt at rest (provider-managed or your own KMS keys — see **key-management**)
and enforce TLS in transit via policy.

### Key Design

The key namespace is the only index object storage gives you, so design it for how
you read and manage the data. Prefix by the dimension you list or scope on:

```
tenant=42/date=2026-07-27/type=invoice/<id>.json
```

This makes per-tenant listing, per-date lifecycle rules, and per-prefix IAM
policies all natural. Historically some stores partitioned request throughput by
key prefix, so high-entropy prefixes were needed to avoid hot partitions; modern
stores largely auto-scale that, so optimize the prefix for **querying, lifecycle
scoping, and access control** rather than for throughput. Reserve dedicated
prefixes (or buckets) for scratch/temp data so a single lifecycle rule can expire
all of it.

For serving these objects to end users at scale, front the bucket with a CDN — see
**edge-and-cdn-delivery** — so repeated reads hit the edge instead of billing an
origin GET each time. For overall spend, see **cloud-cost-optimization**.

## Common Anti-Patterns

❌ **Renaming or moving objects as if it were cheap.** Every rename is copy + delete
of the full object.
✅ Choose keys correctly up front; treat objects as immutable and write new ones.

❌ **Appending to or partially editing large objects.** Each change rewrites the
whole blob.
✅ Write many immutable objects and compact in a batch job; keep mutable state in a DB.

❌ **Using a bucket `LIST` as the source of truth** for existence or as a work queue.
It is eventually consistent, paginated, and billed per request.
✅ Track object state in a database; use storage for bytes only.

❌ **One storage class for everything** — hot data in cold tiers (retrieval fees) or
cold data in hot tiers (storage waste).
✅ Set the class from real read frequency and latency tolerance; automate transitions.

❌ **Manual cleanup, or none.** Buckets grow forever and orphaned multipart parts
accrue silently.
✅ Lifecycle rules for transition, expiry, and aborting incomplete uploads.

❌ **Public buckets or long-lived credentials in clients.** The classic breach.
✅ Private by default; IAM roles for services, short-lived pre-signed URLs for clients.

❌ **A single flat prefix for everything.** Listing, lifecycle scoping, and access
policies all become painful.
✅ Prefix by tenant/date/type so listing, lifecycle, and IAM apply cleanly.

## Object Storage Checklist

- [ ] Objects treated as immutable, write-once — no rename/append assumptions
- [ ] Existence and metadata tracked in a database, not derived from live `LIST`
- [ ] Read-after-write vs listing-lag behavior understood for the chosen store
- [ ] Storage class chosen from actual read frequency and latency tolerance
- [ ] Lifecycle rules transition, expire, and abort incomplete multipart uploads
- [ ] Public access blocked at account and bucket level
- [ ] Services use IAM roles; clients use short-lived pre-signed URLs
- [ ] Encryption at rest and TLS in transit enforced by policy
- [ ] Key layout prefixed by the dimension you query, scope, and secure on
- [ ] Frequently-read objects fronted by a CDN to avoid per-GET origin cost
- [ ] Bucket growth and retrieval/request costs monitored
