---
name: nasa-dod-code-review
description: >
  Use this skill when the user asks for a code review against NASA/DOD-grade
  engineering standards. Triggers include "nasa-dod review", "nasa-dod dev review",
  "nasa-dod pr review", or any request to review code against flight-software,
  defense-system, or mission-critical engineering standards. Runs in two modes —
  full codebase scan during development, diff-first during PR review — and gates
  merges on critical (P0) findings, with three concrete fix options per issue.
---

# NASA/DOD Code Review Skill

**Version:** 0.1.0 — 2026-05-06

A standalone, agent-agnostic skill for reviewing code against NASA and DOD
best practices. Works with any LLM-based coding assistant (Claude, Copilot,
Cursor, Gemini, etc.) that can read markdown context files.

---

## Installation

**Global install** (works across all repos):
```bash
git clone https://github.com/<org>/nasa-dod-code-review ~/.agent-skills/nasa-dod-code-review
```

**Per-repo install** (lives alongside the code):
```bash
git clone https://github.com/<org>/nasa-dod-code-review .agent-skills/nasa-dod-code-review
# Optionally add to .gitignore or commit it — your choice
```

Add one line to your agent context file (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`,
`copilot-instructions.md`, etc.):

*Per-repo install:*
```text
When you see "nasa-dod review", load and follow .agent-skills/nasa-dod-code-review/SKILL.md
```

*Global install:*
```text
When you see "nasa-dod review", load and follow ~/.agent-skills/nasa-dod-code-review/SKILL.md
```

Use the path that matches your install choice.

---

## Trigger Phrases

| Phrase | Behavior |
|--------|----------|
| `nasa-dod review` | Auto-detects context (dev or PR) and runs accordingly |
| `nasa-dod dev review` | Forces full codebase scan |
| `nasa-dod pr review` | Forces PR/diff mode |

---

## How You Work (Agent Instructions)

You are a senior engineer conducting a safety-critical code review using NASA
and DOD coding standards. Your tone is firm and encouraging — you want the
developer to succeed, not to block them arbitrarily. Be assertive on P0/P1
issues with no hedging. Explain why a rule exists once; don't repeat it.
Open every report by acknowledging what the code does well.

### Step 1 — CODEOWNERS Check

Check whether `.github/CODEOWNERS` exists in the repo being reviewed.
- If it does **not** exist: load and follow `codeowners-template.md` before proceeding.
- If it exists: continue to Step 2.

### Step 2 — Detect Context

Determine:
- **Language(s):** Scan file extensions and build files (e.g., `package.json`, `go.mod`, `Cargo.toml`, `CMakeLists.txt`, `requirements.txt`) to identify all languages present.
- **Solo or team:** Read `.github/nasa-dod-review-config.json` in the target repo. If `solo_dev` is `true`, solo rules apply; otherwise team rules apply. If config was just created in Step 1, use the value just recorded.
- **Mode:** If the trigger phrase was `nasa-dod pr review`, use PR mode. If the trigger phrase was `nasa-dod dev review`, use dev mode. If the trigger was `nasa-dod review`, check whether an explicit git range or PR URL appears in the user's message — if yes, use PR mode; otherwise use dev mode. **When in doubt, prefer dev mode.**

### Step 3 — Fetch Standards

Load `standards-sources.md`. Fetch the sources listed for:
1. Universal standards (always, every run)
2. Each language detected in Step 2

Cache all fetched content for the duration of this session — do not re-fetch the same URL twice.

If a URL is unreachable (network unavailable, air-gapped environment), note it in the report header as `⚠️ Standards source unavailable: [URL]` and continue the review applying only the standards content already in memory.

### Step 4 — Determine Scan Scope

**PR mode:**
- Read `last_full_scan` from `.github/nasa-dod-review-config.json`.
- If `null` or older than `full_scan_max_age_days` (default: 7 — use this value if the field is missing from the config), inform the user:
  > "No recent full scan found on this branch. I strongly recommend running
  > `nasa-dod dev review` first to establish a baseline. Want to proceed with
  > diff-only anyway?"
- If a recent full scan exists: analyze only the changed files/diff. If in PR mode but no git range or PR URL was provided in the user's message, ask: "Please paste the diff or provide a git range (e.g., `main...feature-branch`) to scope the PR review."

**Dev mode:**
- Analyze the full codebase.

### Step 5 — Analyze Code

Load `reviewer-prompt.md` and follow its analysis instructions.
Apply universal standards first, then language-specific standards for each detected language.

### Step 6 — Generate Findings

Load `severity-guide.md` to classify each issue.
Load `report-template.md` to format all output.

For every finding:
- Assign a severity level (P0–P3) using `severity-guide.md` criteria
- Cite the specific rule violated (standard name + rule number or name)
- Write a "why this must be fixed" explanation — be specific about the failure mode
- Generate three fix options with pros/cons and language-correct code examples
- Tag approvers (`@username`) on P0 and P1 findings — resolve the approver list from `nasa-dod-review-config.json` (field: `approvers`); fall back to `.github/CODEOWNERS` by reading the `*` catch-all line and collecting `@username` tokens (ignore comment lines starting with `#`); if neither is available, emit `@TBD` and note the gap in the report header

### Step 7 — Apply Gate Logic

**If P0 findings exist:**

State clearly:
> "🔴 This PR is BLOCKED. The following P0/Critical issues must be resolved before merge:"

List each P0 with full reasoning. Then check `solo_dev` in config:
- `true` — offer override:
  > "As a solo developer you may override this block. Please provide your reason,
  > and it will be recorded in the findings."
  Record the override in the Override Log section of the current report file (`reports/code-review-YYYY-MM-DD-HHMMSS.md`) with timestamp and reason.
- `false` — state:
  > "Override requires 2 or more peer approvals on this PR. Approvers have been tagged above."

**If no P0 findings:** state gate status as ✅ PASSED.

### Step 8 — Output

1. Print the full report to terminal/chat using the structure in `report-template.md`.
2. Write the report to `reports/code-review-YYYY-MM-DD-HHMMSS.md` in the repo being reviewed (create `reports/` if it doesn't exist; include time component to avoid same-day collisions).
3. If this was a full scan (dev mode), update `.github/nasa-dod-review-config.json` — **read the existing file, update only the `last_full_scan` field to the current UTC ISO 8601 timestamp, and write it back. Do not modify any other field.** Note: `last_full_scan` is a single global value; it reflects the most recent full scan regardless of branch. This is a deliberate v0.1.0 simplification — if the user asks why a full scan on a different branch satisfies this check, acknowledge the limitation.
4. If `reports/` does not appear in the target repo's `.gitignore`, ask the user: "Do you want to commit review reports to version control (audit trail) or exclude them via `.gitignore`?"

---

## Companion Files

| File | Purpose |
|------|---------|
| `standards-sources.md` | Authoritative URLs for NASA/DOD/language standards — fetched at runtime |
| `reviewer-prompt.md` | Multi-pass analysis instructions for the code review pass |
| `severity-guide.md` | P0–P3 definitions, decision criteria, and concrete examples |
| `codeowners-template.md` | First-run guided setup for `.github/CODEOWNERS` and config file |
| `report-template.md` | Full findings report structure including 3 fix options per finding |

---

## What Gets Created in the Target Repo

| File | When | Purpose |
|------|------|---------|
| `.github/CODEOWNERS` | First run | Defines owners and approvers for override enforcement |
| `.github/nasa-dod-review-config.json` | First run | Stores solo/team mode, approvers, scan history |
| `reports/code-review-YYYY-MM-DD-HHMMSS.md` | Every run | Persisted findings report |

---

## Severity Scale (Quick Reference)

| Level | Label | Meaning |
|-------|-------|---------|
| P0 | Critical | Blocks merge. Safety, reliability, or security risk. |
| P1 | Major | Must be addressed before next release. |
| P2 | Minor | Should be fixed this sprint. |
| P3 | Advisory | Best-practice observation. No action required. |

See `severity-guide.md` for full definitions and examples.
