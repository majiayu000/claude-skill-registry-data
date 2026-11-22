---
name: "report"
description: "Generate submission-ready reports for all confirmed findings. Runs dedup, PoC builder, quality check, and report writer. Usage: /report bounty or /report pentest"
---

# Report

*Sourced from h-mmer-pentest-agents*

Generate reports for confirmed findings. Format: $ARGUMENTS (default: bounty)

This runs the full reporting pipeline. Run this AFTER /pipeline and /validate.

## Step 1: Dedup and Inventory
Run `uv run python3 ../../tools/dedup_findings.py --scan-dir scans/ --db findings.json --stats`
Read findings.md and brain effective techniques.
Show the user a numbered list of confirmed findings.

## Step 2: For EACH confirmed finding (one at a time):

### 2a: Check if PoC exists
Look in poc/ directory. If no PoC for this finding, launch `poc-builder` agent:
"Create PoC for: [finding details]. You MUST write files to poc/<finding-slug>/. Create reproduce.sh and poc.html (if client-side). Do NOT just output to terminal — write the actual files."

### 2b: Check if evidence exists
Look in evidence/ directory. If no screenshots/recordings exist:
- Do NOT claim screenshots exist if they haven't been taken
- Do NOT hallucinate file paths — verify files exist with `ls` before referencing them
- Tell the user: "No evidence captured yet. Run /evidence screenshot to capture, or note 'evidence pending' in the report."

### 2c: Determine CVSS version
Read `scope.yaml` to check the `platform:` field.
- If `platform: hackerone` → use **CVSS 3.1** (HackerOne does not support CVSS 4.0)
- All other platforms → use **CVSS 4.0**

### 2d: Draft the report
Launch `report-writer` agent:
"Write a bug bounty report for: [finding details]. Format: $ARGUMENTS.
Platform: [platform from scope.yaml]. CVSS version: [3.1 if hackerone, 4.0 otherwise].
CRITICAL INSTRUCTIONS:
1. You MUST write the report to reports/drafts/<finding-slug>.md using the Write tool. Do NOT just output to terminal.
2. Use the CVSS version specified above. HackerOne requires CVSS 3.1. All other platforms use CVSS 4.0.
3. Title formula: [Vuln] in [Component] Enables [Impact].
4. Only reference PoC files and screenshots that ACTUALLY EXIST on disk — verify with ls before citing.
5. Include PoC at [path] and evidence at [path] ONLY if those files exist.
6. NEVER hardcode the researcher username, email, password, or token. If you need to embed the reporter identity (e.g., in a sample signup or PoC), write the env-var symbol like `${HACKERONE_EMAIL_ALIAS}` (HackerOne), `${BUGCROWD_EMAIL_ALIAS}` (Bugcrowd), `${INTIGRITI_EMAIL_ALIAS}` (Intigriti), or `${YESWEHACK_EMAIL}` (YesWeHack). Substitution happens at submit time. See `rules/identities.md` for the full table."

### 2e: Quality check
Launch `quality-check` agent on the draft. If score < 7, show issues and ask user if they want to fix and re-check.

## Step 3: Summary
After all findings are processed, show:
```
Reports generated:
  1. [title] — score: X/10 — reports/drafts/finding-1.md
  2. [title] — score: X/10 — reports/drafts/finding-2.md
  ...

Ready for submission:
  /dupcheck <finding> — check for duplicates
  /submit <finding>   — submit to platform
```

## Step 4: Sync
Run `uv run python3 ../../tools/global_brain.py sync-from-local`
Run `uv run python3 ../../tools/statusline.py`

## Top-Tier Report Standard

A report is ready when a tired triager can reproduce and justify it without guessing.

Hard requirements:
- title states vuln, component, and proven impact
- summary explains the business risk in two sentences
- steps use exact accounts, URLs, headers, payloads, and expected markers
- impact section maps the primitive to customer, tenant, financial, admin, secret, or execution consequence
- evidence paths exist and are referenced accurately
- CVSS version follows platform rules and vector matches final proven impact
- duplicate risk and known prior art are addressed when relevant
- remediation names the broken control, not just "validate input"

If any confirmed finding lacks PoC or evidence, stop report generation for that finding and send it back to `/validate` or `/chain`.

