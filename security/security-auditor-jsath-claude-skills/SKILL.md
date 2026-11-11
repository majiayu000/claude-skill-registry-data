---
name: security-auditor
description: "Runs an evidence-backed security audit of a code repository (secrets, dependency advisories, commit history, then a Claude code review against a threat model) and produces a findings JSON plus a report with a remediation roadmap. Also covers read-only triage of a suspected live incident such as stored XSS, Docker/UFW host exposure reviews, LLM email-to-SMS automation design, identity-export sanitising, 2FA setups and pre-transfer repo backups. Use when someone says 'security audit this repo', 'check for leaked secrets', 'is this host exposed', 'review this automation for prompt injection', or 'someone put a script tag in our booking form'. Needs Claude Code (or any shell) with bash, git and python3; extra scanners are used if installed."
---

# Security Auditor

Deterministic scanners first, Claude's code review second, a human decides on fixes.
Never print a secret value anywhere: reports carry file, line and rule only.

## Pick the job

| Ask | Go to |
|---|---|
| Audit a repo / find leaked secrets / vulnerable deps | Repository audit (below) |
| Something odd showed up in a booking, CRM, calendar or email field | `references/stored-xss-booking-triage.md` |
| Docker host with UFW, Tailscale or a cloud firewall | `references/docker-ufw-tailscale-host-hardening.md` |
| LLM that reads email or messages and sends SMS, push or voice | `references/secure-llm-communications-architectures.md` |
| Agent that monitors public meetings or hearings | `references/secure-public-meeting-monitoring.md` |
| User export (Clerk, Auth0, Firebase, Supabase) for outreach or research | `references/identity-export-sanitization.md` |
| Password manager, TOTP, passkeys, lost phone | `references/personal-identity-2fa.md` |
| Saving a secret from a one-time-secret link | `references/secure-one-time-secret-ingestion.md` |
| Backing up a repo before transferring ownership | `references/repository-pre-transfer-backup.md` |
| Approving generated SOC 2 / ISO policies | `references/compliance-policy-review.md` |

All of these are read-only until the user approves a specific change.

## Repository audit

Requirements: bash, git, python3. Optional, used when present: `osv-scanner`
(all ecosystems), `npm`, `pip-audit`, `govulncheck`, `bundle-audit`. For deeper
secret coverage, `gitleaks` or `trufflehog` if installed.

1. **Run the deterministic stages:**
   ```bash
   bash scripts/audit-repo.sh <github-url-or-path> ./security-report standard --commits
   ```
   Depth: `quick` (20 files), `standard` (50), `deep` (100 files, more lines each).
   Flags: `--commits` (last 50 commits), `--secrets-only`, `--deps-only`.
   Outputs: `tech-stack.txt`, `secrets-findings.txt`, `dependency-findings.txt`,
   `commit-findings.txt`, `threat-model-prompt.txt`, `chunk-*.txt`, `metadata.json`.
2. **Check stage completion, not just exit code.** Nonzero exit means a stage
   failed: find which one, rerun it directly (`scripts/scan-secrets.sh`,
   `scripts/scan-dependencies.sh`), and report the wrapper problem separately. An
   empty findings file only means "clean" if that stage actually finished.
   `TOOL MISSING` lines are coverage gaps, not passes.
3. **Threat model.** Read `threat-model-prompt.txt` and write `threat-model.md`
   (assets, entry points, auth boundaries, STRIDE per component, top 5 risk areas,
   naming real files and routes).
4. **Code review.** For each `chunk-*.txt`, apply
   `templates/vulnerability-scan-prompt.md` with the threat model as context.
   Merge results into `findings.json` (`{"findings": [...]}`). Open the real file
   to confirm each High or Critical before keeping it; mark the rest
   `needs-verification`.
5. **Triage scanner hits.** For each secrets line, open the file and decide: real
   credential, test fixture, or placeholder. A real credential that was ever
   committed is leaked: recommend rotation first, history rewrite second.
6. **Report.** Fill `templates/report-template.md` into `security-report.md`.
   Severity counts must equal `findings.json`. Fill "Coverage and limits" honestly.
7. **Clean up.** `chunk-*.txt` contain raw source (and any secrets in it). Delete
   them, or keep the folder `chmod 700`, once the review is done.

### Severity rules

- Critical: exploitable now without auth (RCE, auth bypass, live production secret, SQLi on a public route).
- High: exploitable with a normal account or one precondition (IDOR, stored XSS, SSRF to metadata).
- Medium: needs unusual conditions or limited impact (missing rate limit on login, permissive CORS with credentials off).
- Low / Info: hardening and hygiene (headers, outdated but unaffected deps).
- A dependency advisory is only High or Critical if the vulnerable function is reachable; otherwise say so and drop one level.

### Output example (chat summary)

```
Audited acme/api at standard depth, stages: secrets, deps, commits, review (50 files).
Critical 1, High 2, Medium 3, Low 4.
1. CRITICAL  src/api/pay.js:1  live Stripe secret key committed (also in commit 7e10ec6). Rotate now.
2. HIGH      src/routes/users.ts:88  user id from query, no ownership check (IDOR).
Coverage gaps: osv-scanner not installed, Python deps not scanned.
Report: ./security-report/security-report.md
```

## Incident and change rules

- Separate **stored**, **rendered as text**, **executed** and **compromised**.
  Raw markup in an API proves storage only.
- Never visit a suspicious payload host or URL. Use passive DNS, WHOIS and
  reputation services.
- Preserve evidence before containment. Cancelling events, blocking accounts,
  rotating credentials, firewall or SSH changes all need explicit approval.
- On hosts: read-only review first, one layer of change per window, a tested
  rollback ready, and real post-change health checks. A failing verifier means
  roll back, even if the service looks fine.

## Scheduled scans (optional)

```bash
# daily quick scan, weekly deep scan with history
0 2 * * *  bash ~/.claude/skills/security-auditor/scripts/audit-repo.sh /path/to/repo /path/to/reports/daily quick
0 3 * * 0  bash ~/.claude/skills/security-auditor/scripts/audit-repo.sh /path/to/repo /path/to/reports/weekly deep --commits
```

Cron runs only the deterministic stages; the Claude review step needs a session.
