---
name: backup-disaster-recovery
description: Design backups that actually work when they are needed. Covers RPO and RTO definition, the 3-2-1 rule, encryption before leaving the host, ransomware-resistant immutable storage, restore drills, and the split between operational and legal retention. Invoke when 'we have backups but nobody has restored them' is true, after a near-miss, or before a major migration.
---

# Backups & Disaster Recovery

The line that defines a backup strategy: **"a backup you have not restored is a wish, not a backup."** Most teams have something called "backups" that have never been restored end-to-end. Sometimes they don't actually work; sometimes they work but are too slow; sometimes they work but the team forgot a critical piece of state and ends up with a half-restored system.

This skill builds a strategy that survives the first real incident — not the strategy that looks good in a slide deck.

Pairs with [`incident-response`](../incident-response/SKILL.md) (where backups get used) and [`postgres-hardening`](../postgres-hardening/SKILL.md) / [`backend-architecture`](../backend-architecture/SKILL.md) (where the data lives).

## When to invoke

- "We have backups but nobody has ever restored them"
- Adding a new system that holds production data
- After a near-miss (almost lost data) or an actual data-loss incident
- Before a major migration, version upgrade, or refactor that touches storage
- Ransomware attack in the news that affects your stack (always periodic, treat as a prompt)
- Periodic re-audit (quarterly is reasonable)

## Step 1 — Define what you're protecting against

The right strategy depends on the failure class. Backups for ransomware look different from backups for "developer dropped the table accidentally."

| Failure class | What you need |
|---|---|
| Hardware failure (disk, server) | Replica or snapshot in a different physical location |
| Accidental delete (DROP TABLE, rm -rf, bad migration) | Point-in-time backup, retained N days |
| Application bug corrupting data | Point-in-time backup + ability to surgically restore subsets |
| Ransomware encrypting everything reachable from the app | Backups the ransomware cannot reach — immutable or offline |
| Cloud-account compromise | Backups in a separate account / provider, separate credentials |
| Provider going under / region outage | Backups in a different provider / region |
| Legal hold / subpoena / SAR request | Selective archive, retention policy that complies with your jurisdiction |
| Force majeure (data center fire, country-level outage) | Off-region / off-provider backups, restore plan that does not assume continuity |

A real strategy covers at least the first four. Production systems with revenue at stake should cover the first six. Regulated environments cover all eight.

## Step 2 — Define RPO and RTO

**RPO (Recovery Point Objective)**: how much data can you afford to lose? Measured in time. RPO = 1 hour means you can lose up to the last hour of writes.

**RTO (Recovery Time Objective)**: how long can you be down during recovery? RTO = 4 hours means a full restore must complete within four hours.

These two drive every other decision. A 1-minute RPO requires continuous replication; a 1-day RPO can be daily snapshots. A 5-minute RTO requires hot standby; a 24-hour RTO can be cold storage on a different provider.

Most small-team production systems land at:

- **RPO**: 1–24 hours
- **RTO**: 4–24 hours

Pick yours. Write it down. Test against it.

## Step 3 — The 3-2-1 rule

The classic backup mantra, still correct:

- **3 copies** of the data (production + 2 backups)
- **2 different media** (so a single failure mode does not affect both)
- **1 off-site** (so a site-level disaster does not take everything)

In modern cloud terms:

- **Production data**: managed Postgres / Mongo / S3 — copy 1
- **Same-region backup**: provider's automated backups (e.g. RDS snapshots, R2 versioning) — copy 2, fast restore
- **Off-site / off-provider backup**: scheduled dump to a different provider / different account — copy 3, slow but independent

You can extend (3-2-1-1-0: plus 1 immutable, 0 errors after restore test), but 3-2-1 is the minimum that survives realistic failures.

## Step 4 — Encrypt every backup, end-to-end

A leaked plaintext backup is a leaked database. Encrypt **before** the data leaves the production host, with a key the backup destination does not hold.

```bash
# pg_dump piped through compression + age encryption, then to off-site storage
pg_dump -Fc app_db \
  | gzip \
  | age -r age1q3...recipientpublickey... \
  > /tmp/app_db-$(date +%F).sql.gz.age

# Upload to off-provider storage (Cloudflare R2, B2, S3) with rclone
rclone copy /tmp/app_db-$(date +%F).sql.gz.age remote:backups/
```

Patterns:

- **`age`** (https://age-encryption.org) is the modern simple choice — small binary, asymmetric, no PGP-keyring pain
- **Public-key encryption** at the backup destination — the production host has the public key, the restore host (separate, secured) has the private key. Compromise of the production host does not compromise the ability to read past backups.
- **Rotate encryption keys** periodically; keep retired keys long enough to decrypt all retained backups
- **Test that you can decrypt** — a backup encrypted with a key you no longer have is useless

## Step 5 — Make backups ransomware-resistant

Ransomware that compromises the production environment will look for backups to encrypt or delete next. Standard daily-rsync-to-NAS backups die in this scenario.

Defenses:

- **Immutable storage** — write-once, retention-locked. S3 Object Lock (Compliance mode), R2 Object Versioning + retention rules, Backblaze B2 with object lock. Once written, the object cannot be modified or deleted before the retention period expires — even by the account owner.
- **Separate credentials** for the backup pipeline that have *write but not delete* permission on the backup bucket
- **Separate account / provider** so a credential leak in production cannot reach the backup destination
- **Air-gapped weekly archives** for the strictest cases — periodic dumps onto offline media, manually rotated

Avoid:

- Backup destinations writable by the same credentials the app uses
- "Soft-delete" features mistaken for immutability — they have an "actually delete" sibling
- Backup processes that the app itself can pause / disable

## Step 6 — Restore drills (the part everyone skips)

A backup you have not restored is not a backup. Schedule and execute drills.

**Quarterly drill** (every team):

1. Pick a backup at random from the last 90 days
2. Restore it to a clean environment (not production)
3. Verify data integrity — row counts, recent records present, schema matches
4. Time the restore — record the actual RTO
5. Document anything that went wrong

**Annual full DR exercise** (production-critical systems):

1. Simulate a full data loss scenario
2. Restore production from off-site backup to a parallel environment
3. Run the application end-to-end against the restored data
4. Measure: how long did this take? What broke? What was missing?

Common findings from real drills:

- Backups are present but the encryption key is on the same machine as the backup
- Restore scripts assume tools (`pg_restore`, `mongorestore`) that are not installed on the restore host
- Application secrets / configuration are not backed up; restoring the DB does not get the app back
- DNS / certificates / load-balancer config not in version control — recreating the running app from a DB dump takes days
- "Daily backups" turn out to be daily for one DB and weekly for another, undocumented
- Backup files have been silently failing for months — nobody monitored the cron output

## Step 7 — Back up the things that aren't the database

The database is the most obvious. The less-obvious matters too:

- **Object storage** — user uploads, generated files. Cloudflare R2 versioning, S3 versioning + lifecycle policies.
- **Configuration / secrets** — env vars, secret-manager contents. Export periodically (encrypted) so you can recreate without the original system.
- **DNS / certificates** — export DNS zones, document cert rotation. Losing a domain takes a service offline.
- **CI/CD configuration** — your `.github/workflows/`, deploy scripts. Live in the repo, but make sure the repo itself has off-platform backups (GitHub itself can lock you out).
- **Email / messaging history** — for legal-discovery readiness
- **Documentation, runbooks, architecture diagrams** — if Notion / Confluence vanishes, you need them
- **Customer-facing state** — Stripe webhook subscriptions, third-party integrations. Document so you can recreate.

The "everything else" tier is often where the recovery time actually goes. The DB restore is 30 minutes; reconstructing the deploy pipeline from memory is 3 days.

## Step 8 — Retention policies

Two different needs, two different policies:

### Operational retention (for restoring)

Roughly: more granular for recent, less for older.

- **Hourly snapshots** for the last 24 hours
- **Daily backups** for the last 30 days
- **Weekly backups** for the last 12 weeks
- **Monthly backups** for the last 12 months

Tune to your RPO and to the cost.

### Legal retention (for compliance / discovery)

Different rules. Tax data: 10 years (DE/AT). Some user data: only as long as needed under GDPR — see [`gdpr-technical-controls`](../gdpr-technical-controls/SKILL.md). Some data has affirmative deletion requirements (right to be forgotten, accounts closed).

These two policies conflict for personal data. The accepted approach: maintain a "delete on restore" pipeline so any restore re-applies deletion requests issued since the backup was taken. Document this in your privacy policy and DPA.

## Step 9 — Automation and monitoring

A backup process that requires manual action will silently break.

```bash
# Cron entry — daily at 03:00 UTC
0 3 * * * /usr/local/bin/backup-app.sh 2>&1 | logger -t backup-app

# In /usr/local/bin/backup-app.sh — exits non-zero on any failure,
# pings a healthcheck URL on success (so absence is itself an alert)
set -euo pipefail
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
BACKUP_PATH=/tmp/app_db-$TIMESTAMP.sql.gz.age

pg_dump -Fc app_db | gzip | age -r "$AGE_RECIPIENT" > "$BACKUP_PATH"
rclone copy "$BACKUP_PATH" remote:backups/ --no-traverse
rm "$BACKUP_PATH"

# Healthcheck — https://healthchecks.io / Better Stack heartbeats / your monitoring
curl -fsS -m 10 --retry 3 "$HEARTBEAT_URL"
```

Monitor:

- **Last successful backup timestamp** — alert if older than RPO + grace
- **Backup file size** — alert if it deviates significantly from baseline (small ⇒ broken; huge ⇒ unexpected growth or compromise)
- **Restore-drill date** — alert if more than 90 days since last drill

A heartbeat-based pattern catches more failures than a "got an alert on error" pattern. If the cron job died entirely, error-alerts never fire; absence does.

## Step 10 — Document the recovery procedure

In a place that exists when production is gone:

- **A printed copy** or copy on a phone you can read offline
- **A repo you can clone outside the affected infrastructure**
- **A document in a personal email / drive that does not depend on company SSO**

Should answer:

- Who has the keys to do the restore?
- Where is each backup stored? What credentials do you need?
- What's the exact command sequence to restore? (Tested in your last drill.)
- What infrastructure must exist first (DNS, DB instance, secrets)?
- What's the order of operations if multiple systems are down?
- Who do you notify, when?

A good recovery doc is the result of a real drill, not theory.

## Step 11 — Special cases

### Database snapshots vs `pg_dump`

Both have a place. Cloud-provider snapshots are fast to restore but tied to the provider. Logical dumps (`pg_dump`, `mongodump`) are slower but portable to any environment. Run both. Cloud snapshots for fast intra-provider restore; off-provider logical dumps for the bad-day scenario.

### S3 / object-storage backups

S3 versioning + lifecycle is the easy path. With versioning on, deleted objects can be restored by removing the delete marker. Lifecycle policies move old versions to cheaper storage.

But: versioning is account-internal. A compromised account credential can still delete versions (unless Object Lock is on). For ransomware resistance, mirror to a separate account / provider.

### Backing up an entire VPS

For self-hosted single-VPS deployments, provider-level snapshots are the right complement to app-level backups. They capture *everything* — DB, files, config — at one moment. They're not granular for "restore one row" but they're great for "restore the whole machine."

Restore at least one VPS snapshot per quarter to verify the provider's snapshot mechanism works for your case.

### Backup of backups?

For high-stakes data, yes. A weekly export from the primary backup destination to a tertiary location. Three's the magic number; rarely worth four.

## Checklist — production-ready backup strategy

- [ ] RPO and RTO are written down and known to the team
- [ ] At least 3 copies of the data, on 2 media, with 1 off-site (or off-provider)
- [ ] Backups are encrypted before leaving the production host
- [ ] Encryption keys are not on the same machine as the backups
- [ ] Backup destination has write-but-not-delete permission for the backup pipeline, or uses Object Lock
- [ ] An off-provider / off-account copy exists for ransomware resistance
- [ ] Backups happen via automation, with heartbeat monitoring
- [ ] Last successful backup timestamp is monitored — alert if older than RPO + grace
- [ ] Restore drills are scheduled quarterly; results documented
- [ ] Full DR exercise scheduled annually for production-critical systems
- [ ] Object storage (uploads), configuration, secrets, DNS, certificates are also backed up
- [ ] Retention policy distinguishes operational from legal needs; deletion-on-restore handled
- [ ] Recovery procedure is documented in a place that survives production loss
- [ ] At least one team member other than the original implementer can perform the restore

## What this skill will not do

- Help recover data from systems you do not own
- Recommend backup strategies that store production credentials at the backup destination
- Substitute for a regulated-environment DR program with auditor-defined requirements
