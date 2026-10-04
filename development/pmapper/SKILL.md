---
type: skill
name: pmapper
description: IAM privilege escalation analysis using Principal Mapper (PMapper). Builds an IAM graph and identifies escalation paths with deterministic evidence. Use when queries involve privilege escalation, lateral movement, or "who can reach admin".
last_updated: "2026-03-24"
doc_source: https://github.com/nccgroup/PMapper/wiki
---

# PMapper (Principal Mapper)

PMapper maps IAM principals and their relationships to identify privilege escalation paths. It builds a directed graph of who-can-become-whom and produces deterministic, reproducible evidence of escalation vectors.

---

## Table of Contents

- [Installation](#installation)
- [Core Concepts](#core-concepts)
- [Graph Lifecycle](#graph-lifecycle)
- [Analysis](#analysis)
- [Queries](#queries)
- [Output Storage](#output-storage)
- [Plugin Integration](#plugin-integration)
- [Interpreting Results](#interpreting-results)
- [Troubleshooting](#troubleshooting)
- [References](#references)

---

## Installation

```bash
pip install principalmapper
```

Requires AWS credentials with IAM read permissions (`iam:Get*`, `iam:List*`, `sts:GetCallerIdentity`).

---

## Core Concepts

- **Graph:** A snapshot of all IAM principals (users, roles) and the edges between them (who can assume/escalate to whom)
- **Edge:** A relationship showing one principal can access another — via `sts:AssumeRole`, `iam:PassRole`, Lambda code injection, EC2 user data, etc.
- **Node:** An IAM principal (user or role) with its attached policies and permissions
- **Admin:** A principal with effectively unrestricted access (`*` on `*`)
- **Escalation path:** A chain of edges from a non-admin to an admin node

---

## Graph Lifecycle

### Create (one-time per session)

```bash
pmapper graph create
```

Pulls all IAM data from the account and builds the edge graph. This is the expensive step — run once, query many times.

**Storage:** PMapper stores graphs locally at `~/.local/share/principalmapper/` by default.

### Display graph info

```bash
pmapper graph display
```

Shows account ID, number of nodes/edges, and admin principals.

---

## Analysis

### Full analysis (JSON) — primary output for plugin

```bash
pmapper analysis --output-type json
```

Returns structured findings:

```json
{
  "account": "123456789012",
  "date_and_time": "2026-03-24 10:30:00",
  "findings": [
    {
      "title": "IAM Principals Can Escalate Privileges",
      "severity": "High",
      "impact": "A lower-privilege IAM User or Role is able to gain administrative privileges.",
      "description": "...",
      "affected_principals": ["arn:aws:iam::123456789012:role/dev-role", "..."]
    }
  ]
}
```

### Privesc-only analysis (skip already-admin principals)

```bash
pmapper analysis --output-type json --skip-admin
```

This is the most useful for the plugin — shows only non-admin principals that can reach admin. Filters out noise from principals that are already admin.

### Text analysis (Markdown)

```bash
pmapper analysis --output-type text
```

Human-readable Markdown report. Use JSON for plugin automation, text for quick review.

---

## Queries

### Can a specific principal reach admin?

```bash
pmapper query "can arn:aws:iam::123456789012:role/dev-role do sts:AssumeRole with *"
```

### Who can perform a specific action?

```bash
pmapper query "who can do iam:PutRolePolicy with *"
pmapper query "who can do s3:GetObject with arn:aws:s3:::sensitive-bucket/*"
pmapper query "who can do iam:PassRole with *"
```

### Who can reach a specific principal?

```bash
pmapper query "who can do sts:AssumeRole with arn:aws:iam::123456789012:role/admin-role"
```

### Argument-based queries (structured)

```bash
pmapper argquery --principal arn:aws:iam::123456789012:role/dev-role --action iam:PassRole --resource "*"
```

### Useful flags

| Flag | Effect |
|:-----|:-------|
| `--skip-admin` | Exclude already-admin principals from output |
| `--include-unauthorized` | Show principals that CANNOT perform the action (useful for proving negative) |

---

## Output Storage

All PMapper output is stored in `data/pmapper/` using the naming convention `{account_id}-{YYYY-MM-DD}`. See `data/README.md` for full conventions.

```
data/pmapper/
├── graphs/                              # Graph snapshots
│   └── {account_id}-{date}/
├── analysis/                            # Full analysis output (JSON)
│   └── {account_id}-{date}.json
├── privesc/                             # Escalation-only (--skip-admin)
│   └── {account_id}-{date}.json
└── queries/                             # Ad-hoc query results
    └── {account_id}-{date}-{query}.txt
```

### Saving output

Get the account ID first, then use it in filenames:

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
TODAY=$(date +%Y-%m-%d)

# Full analysis
pmapper analysis --output-type json > data/pmapper/analysis/${ACCOUNT_ID}-${TODAY}.json

# Privesc-only
pmapper analysis --output-type json --skip-admin > data/pmapper/privesc/${ACCOUNT_ID}-${TODAY}.json

# Specific query
pmapper query "who can do iam:PassRole with *" > data/pmapper/queries/${ACCOUNT_ID}-${TODAY}-passrole.txt
```

---

## Plugin Integration

### When to trigger

The Director MUST trigger PMapper when the query involves any of:
- Privilege escalation ("can X escalate?", "priv esc", "who can reach admin?")
- Lateral movement ("can X pivot to Y?", "who can assume role Z?")
- PassRole abuse ("who can pass roles?", "PassRole scope")
- Broad IAM risk assessment ("IAM risks", "dangerous permissions")

### Pre-flight: Graph creation

Like SCP visibility, the graph MUST be created once per session before any PMapper query:

```yaml
pmapper_preflight:
  check: ls ~/.local/share/principalmapper/ 2>/dev/null
  on_exists: |
    Graph may already exist. Run `pmapper graph display` to check account and freshness.
    If the graph is for the current account, reuse it.
    If stale (>24h) or wrong account, recreate.
  on_missing: |
    Run `pmapper graph create` and wait for completion.
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    TODAY=$(date +%Y-%m-%d)
    Save analysis output:
      pmapper analysis --output-type json > data/pmapper/analysis/${ACCOUNT_ID}-${TODAY}.json
      pmapper analysis --output-type json --skip-admin > data/pmapper/privesc/${ACCOUNT_ID}-${TODAY}.json
```

### Pipeline integration

PMapper output is deterministic CLI evidence — treat it the same as `aws` CLI output in the pipeline:

1. **Director** classifies a priv-esc query → routes to Access Expert
2. **Expert** runs `pmapper analysis --output-type json --skip-admin` or a targeted `pmapper query`
3. **Expert** saves output to `data/pmapper/` and includes it in the response
4. **Critic** scores based on PMapper's graph evidence (Score 5 — deterministic graph traversal)
5. **Director** cross-references PMapper findings with exploit chain analysis

### Evidence in Claim Envelope

PMapper output counts as first-class CLI evidence. The Expert response format is the same:

```markdown
**CLI Command:** $ pmapper analysis --output-type json --skip-admin
**Output:** {{full JSON output}}

**Status:** CONFIRMED
**Summary:** PMapper identifies 3 non-admin principals with escalation paths to admin.
```

### Combining with existing validation rules

PMapper replaces speculation in escalation claims. When the existing validation rules (`compute.md` → `lambda_privesc_*`, `iam.md` → `iam_slr_*`) identify potential escalation, PMapper confirms or disproves the path:

| Existing check | PMapper confirmation |
|:---------------|:--------------------|
| `lambda_privesc_passrole` | `pmapper query "can {{role}} do iam:PassRole with *"` |
| `lambda_privesc_code_injection` | `pmapper query "can {{role}} do lambda:UpdateFunctionCode with *"` |
| `iam_slr_*` (SLR abuse) | `pmapper query "can {{role}} do iam:CreateServiceLinkedRole with *"` |
| Instance profile escalation | `pmapper query "can {{instance_role}} do sts:AssumeRole with {{target}}"` |

---

## Interpreting Results

### Analysis findings

| Finding title | What it means |
|:-------------|:--------------|
| IAM Principals Can Escalate Privileges | Non-admin principals have paths to admin — check `affected_principals` |
| IAM Principals With Admin Access | Already-admin principals (use `--skip-admin` to filter) |
| IAM Users Have Unused Access Keys | Stale credentials (overlaps with `qa-10`) |

### Query results

- **"Yes, ..."** — The principal CAN perform the action (directly or via escalation). This is a CONFIRMED finding.
- **"No, ..."** — The principal CANNOT. This is a FALSE_POSITIVE for the escalation claim.
- **Edge description** — PMapper shows the exact path (e.g., "through Lambda code injection on function X"). This is the evidence chain.

### Scoring guidance

| Evidence | Critic Score |
|:---------|:------------|
| PMapper confirms escalation path with edge chain | 5 (Verified) |
| PMapper confirms action possible, no edge detail | 4 (Strong) |
| PMapper graph stale (>24h), results may not reflect current state | 3 (Moderate) — recreate graph |
| PMapper cannot determine (missing permissions to build graph) | ERROR — flag for manual review |

---

## Troubleshooting

| Issue | Fix |
|:------|:----|
| `botocore.exceptions.ClientError: AccessDenied` | Credentials need `iam:Get*`, `iam:List*`, `sts:GetCallerIdentity` |
| Graph creation hangs | Large accounts take time — 1000+ principals can take several minutes |
| Stale graph | Delete and recreate: `pmapper graph create --force` |
| `ModuleNotFoundError: principalmapper` | Install: `pip install principalmapper` |
| Query returns unexpected "No" | Check if an SCP or permission boundary blocks the path — PMapper evaluates these |

---

## References

- [PMapper GitHub](https://github.com/nccgroup/PMapper)
- [CLI Reference](https://github.com/nccgroup/PMapper/wiki/CLI-Reference)
- [Query Reference](https://github.com/nccgroup/PMapper/wiki/Query-Reference)
- [Getting Started](https://github.com/nccgroup/PMapper/wiki/Getting-Started)
