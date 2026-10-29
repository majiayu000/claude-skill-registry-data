---
name: dsr-automation
description: "Use when automating data subject requests: access, erasure, portability, and rectification at scale. Covers request intake and identity verification, orchestration across datastores, processor propagation, and SLA tracking. Also use when manual DSR handling is drowning the privacy team."
version: 1.0.0
domain: privacy
lifecycle: stable
last_verified: '2026-10-23'
requires: []
extends: []
relates: [gdpr-engineering, consent-management, privacy-impact-assessment]
tools:
  - name: Python
    version: '3.12'
  - name: PostgreSQL
    version: '17'
---
Data subject requests arrive by the hundred: "send me my data",
"delete everything". Manual handling does not scale and misses
stores. This skill covers building the automation: verified intake,
a fan out orchestrator that hits every datastore, propagation to
processors, and SLA tracking that proves compliance.

## Quick Workflow

1. Build verified intake: request types, identity proofing
   proportionate to the data's sensitivity, and fraud resistance.
2. Maintain the datastore inventory from the privacy registry; the
   orchestrator fans out to every entry.
3. Implement per store handlers: export, delete, rectify, and
   restrict, each idempotent.
4. Propagate to processors with receipts; retry failures visibly.
5. Handle conflicts: legal holds, other people's data in the
   export, and backup windows.
6. Track SLAs: deadlines per regulation, escalation before breach.
7. Log everything for the regulator: what was done, when, where.
8. Test with synthetic subjects quarterly, including the nasty
   cases.

## 1. Orchestrator sketch

```python
#!/usr/bin/env python3
"""DSR orchestrator: fans a request out to registered store handlers."""
import datetime

HANDLERS = {}  # store name -> handler object with export/delete methods

def register(name):
    def deco(fn):
        HANDLERS[name] = fn
        return fn
    return deco

@register("postgres_users")
def pg_users(action, subject_id):
    return {"store": "postgres_users", "action": action,
            "subject": subject_id, "status": "done",
            "at": datetime.datetime.now(datetime.timezone.utc).isoformat()}

def run_dsr(kind, subject_id):
    log = []
    for name, fn in HANDLERS.items():
        try:
            log.append(fn(kind, subject_id))
        except Exception as e:  # noqa: BLE001 - one store failing must not stop others
            log.append({"store": name, "status": "FAILED", "error": str(e)})
    return log

print(run_dsr("export", "user_123"))
# Production: persist the log, retry FAILED, alert on repeated failure
```

## 2. Identity verification and conflicts

```bash
# Verification proportional to risk:
# - export of basic profile: logged in session is enough
# - export of sensitive data: step up auth
# - erasure: confirm explicitly, warn about irreversibility
# Fraud watch: bursts of requests from one source, requests for others
echo "log verification method per request; regulators ask"
```

```bash
# Conflict handling:
# - legal hold: pause erasure for held data, document the hold
# - mixed data (photos with other people): redact third parties in exports
# - backups: erase from live now, purge backups on their cycle, document it
psql "$DB_URL" -c "SELECT * FROM legal_holds WHERE subject_id='user_123';"
```

## Edge cases

- The subject cannot be verified. You may refuse, but you must tell
  them why and what would suffice.
- Processors do not confirm. Escalate per contract; repeated failure
  is a vendor management issue.
- Request volume spikes (campaign driven). Queue with priority by
  deadline, never silently drop.
- The export format must be portable (JSON/CSV), not a PDF
  screenshot.

## Escalation

- SLA breach imminent: manual triage of the oldest requests while
  automation catches up.
- Systemic handler failure: fix the handler, then re run affected
  requests; notify subjects if the delay breaches the deadline.
- Regulator inquiry: the per request log is your evidence; keep it
  complete and tamper evident.

## Detection and defender view

Detect DSR automation gaps with synthetic subjects: submit export,
rectify, and erase requests and verify every store. Monitor handler
failure rates, SLA burn down, and verification fraud signals. The
durable design treats DSR as a product feature with owners and
tests, not a legal chore done in spreadsheets.

## Key references

- GDPR Articles 12-22: rights and modalities.
- EDPB guidance on data subject rights.
- Related skills: gdpr-engineering, consent-management.
