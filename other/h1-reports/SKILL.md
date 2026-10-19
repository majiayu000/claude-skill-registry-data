---
name: h1-reports
description: Query a local corpus of 14,878 disclosed HackerOne reports (program, title, link, bounty, upvotes, vuln_type) from reddelexc/hackerone-reports. Use for PROGRAM-SPECIFIC bounty calibration ("what does GitLab pay for IDOR?"), escalation-idea mining by vulnerability class, and reward-table reality checks before submitting any report. Trigger when picking severity for a report, studying a program's payout history, hunting ideas for a known vuln class, or when the user mentions HackerOne top reports / hackerone-reports / reddelexc.
---

# h1-reports — Program-Specific HackerOne Payout Corpus

Companion to `bb-disclosures` (multi-platform severity corpus) and `h1-playbooks` (per-class attack-pattern playbooks distilled from this same corpus — read those when planning a hunt for a specific class). This one's unique strength: **program names + upvotes**, so it answers "what does THIS program historically pay for THIS bug class?"

## Queries

```bash
python <skill_dir>/scripts/query.py --program gitlab --vuln idor --min-bounty 1000
python <skill_dir>/scripts/query.py --vuln "business logic" --min-bounty 5000 --limit 20
python <skill_dir>/scripts/query.py --q "graphql" --program github
python <skill_dir>/scripts/query.py --stats          # top programs/vuln types by total payout
python <skill_dir>/scripts/query.py --refresh        # pull latest data.csv from GitHub
```

Columns: `program, title, link, upvotes, bounty, vuln_type` (links are hackerone.com/reports/N — read the full writeup for escalation patterns when a record is relevant).

## Use it in the hunt workflow

1. **Before reporting any finding** (with bb-disclosures): query `--program <target> --vuln <class>` → if the program appears, its own history is the strongest severity argument available. If not, query `--vuln <class> --min-bounty <expected>` for cross-program precedent.
2. **When scoping a new program:** `--program <name> --sort bounty` shows what that program pays for — tells you which hunting skills to lead with (IDOR-heavy → bb-authz/idor-runner; business-logic-heavy → bb-bizlogic).
3. **For escalation ideas on a confirmed primitive:** `--vuln <class> --min-bounty 5000` → read the top-paid writeups for that class; chains that reached 4-5 figures show the missing links worth adding to your own finding.

## Discipline

- Payout history is an argument, not a guarantee — pair with CVSS and program policy, never substitute.
- Bounty `0.0` usually means disclosed-but-unrewarded (or reward hidden); don't treat as "program pays nothing".
- Corpus snapshot ages; `--refresh` before any serious calibration session.
