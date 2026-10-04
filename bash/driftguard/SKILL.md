---
name: skill-drift-guard
description: DriftGuard Security Scanner+ is a local-first security drift scanner for repos, OpenClaw skills, and AI agent tools. Use to scan before trust, save trusted baselines, compare after updates, generate human review tickets, review file/hash drift, dependency drift, install-hook changes, symlink changes, prompt-injection signals, sensitive-path references, obfuscation, shell execution, network access, and risky capability diffs.
metadata: { "openclaw": { "emoji": "🛡️", "homepage": "https://clawhub.ai/david90232/driftguard/security/openclaw", "requires": { "bins": ["node"] } } }
---

# DriftGuard Security Scanner+

**Trust what you review. Compare what changed since trust.**

Use this skill for **local security/integrity checks** and **post-update drift detection** on repos, installed skills, and AI agent tool folders.

This skill is intentionally narrower than a generic security scanner. Its best use is:
- scan a local skill folder or repo before trust
- save a trusted baseline after review, including approver, note, git commit, package version, risk snapshot, and finding summary
- compare later to answer **what changed since trust**
- highlight risky new capabilities like shell, network, sensitive file access, symlinks, dependencies, prompt-injection signals, obfuscation, or install hooks

## Quick start

Run the scanner directly from the installed skill folder:

```bash
node {baseDir}/scripts/cli.js scan <path>
```

Save a trusted baseline after review:

```bash
node {baseDir}/scripts/cli.js trust <path>
```

Save a trusted baseline to a custom location:

```bash
node {baseDir}/scripts/cli.js trust <path> --baseline ./reports/skill-baseline.json
```

Compare a skill or repo against a saved baseline:

```bash
node {baseDir}/scripts/cli.js compare <path> --baseline ./reports/skill-baseline.json
```

Generate a reviewer approval ticket for a scan or comparison:

```bash
node {baseDir}/scripts/cli.js compare <path> --baseline ./reports/skill-baseline.json --review ./reports/review-ticket.md
```

## Recommended workflow

### 1. Scan before trust
Review the candidate repo or skill first.

```bash
node {baseDir}/scripts/cli.js scan /path/to/skill
```

Treat **high** or **critical** output as a stop sign until manually reviewed.

### 2. Trust after review
If the findings are acceptable, save a trusted baseline.

```bash
node {baseDir}/scripts/cli.js trust /path/to/skill
```

### 3. Compare after updates
After the skill changes or updates, compare it to the saved baseline.

```bash
node {baseDir}/scripts/cli.js compare /path/to/skill --baseline ./reports/baseline.json
```

Look especially for:
- newly added or changed files
- new shell or network findings
- dependency or install-hook drift
- new symlinks or sensitive file references

### 4. Create a review ticket before re-trusting
For marketplace publishing, PR review, or team handoff, write a human approval checklist:

```bash
node {baseDir}/scripts/cli.js compare /path/to/skill --baseline ./reports/baseline.json --review ./reports/review-ticket.md
```

The ticket includes:
- approve/reject/needs-review checkboxes
- required security checks based on detected drift
- trust recommendation and reasons
- risk deltas and new capability categories
- why each new finding received its severity and what the reviewer should check next
- a copy-paste approval note for PRs or release notes

## What it checks

- risky shell execution patterns like `curl | bash`, `eval`, `exec`, `subprocess`, `os.system`
- outbound network patterns like `fetch`, `axios`, `requests`, `curl`, webhook usage
- references to sensitive files like `.env`, SSH keys, `SOUL.md`, `MEMORY.md`, OpenClaw config
- prompt injection style content in `SKILL.md`, `SOUL.md`, `MEMORY.md`
- obfuscation hints like base64 helpers and long encoded blobs
- symlink drift without following symlinks
- dependency drift in `package.json`, `requirements.txt`, and `pyproject.toml`
- install-hook changes in `package.json`
- combo risks like:
  - shell + network
  - network + sensitive files
  - shell + prompt-injection signals
  - obfuscation + active capabilities

## Config suppressions

Prefer a reviewer-controlled config passed with `--config <file>`.
By default, the scanner does **not** automatically honor `.driftguard.json` inside the target being scanned, because an untrusted target could suppress its own risky findings.
Use `--use-target-config` only after reviewing the target-provided suppressions.

Example:

```json
{
  "ignorePaths": ["dist/", "fixtures/"],
  "ignoreRules": ["net.fetch", "shell.exec_generic", "shell.*"]
}
```

Use suppressions sparingly. If a rule is noisy, prefer narrowing it later instead of muting the whole category.

## Exit codes

- `0` for low risk and no drift
- `1` for medium risk or drift detected
- `2` for high or critical risk

Use this for CI or install gating.

## Review tickets

Use `--review <file>` when the output needs to be read by a human before refreshing trust.
This is the best default for publishing updates because it turns scanner output into an approval artifact instead of just a machine report.
Each finding should include severity rationale and reviewer guidance so users understand why something is high, medium, or low instead of treating the scanner as a black box.

## Positioning

Use this skill when you want a **transparent, local, deterministic trust workflow**.
Do not use it as the sole authority for safety. It is a heuristic scanner plus drift guard, not a guarantee.
