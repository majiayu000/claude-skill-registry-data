---
name: skills-finder
description: Find Agent Skills on skills.sh and adopt only the ones that pass a security audit. Use when the user wants to discover, search for, evaluate, or install a third-party skill ("find a skill for X", "is this skill safe to install", "search skills.sh", "what skill should I use for Y"). Always runs the skills.sh security audit before recommending or installing anything, and refuses to adopt skills that fail the audit.
---

# Skills Finder

Discover skills on [skills.sh](https://skills.sh) and **gate every candidate
through a security audit before adopting it**. The user's rule is firm: only
adopt skills with no security problems. Never install a skill that has not
cleared the audit.

## Workflow

```
1. DISCOVER   npx skills find "<query>"          → candidate list
2. GATE       scripts/audit.py <candidate>...     → ADOPT / REVIEW / REJECT
3. DECIDE     adopt only ADOPT (or REVIEW after explicit user OK)
4. INSTALL    npx skills add <owner/repo@skill>   → only for approved skills
```

## Step 1 — Discover (no token needed)

Use the `skills` CLI; it handles auth internally, so no Vercel token is required:

```bash
npx -y skills@latest find "<query>"            # e.g. "pdf", "postgres backup"
npx -y skills@latest find "<query>" --owner <github-owner>   # scope to an owner
```

Output lines look like `owner/repo@skill   <N> installs` plus a
`https://skills.sh/owner/repo/skill` URL. Higher installs ≠ safer — still gate.

Other CLI verbs: `npx skills list` (installed), `npx skills add <owner/repo@skill>`
(install), `npx skills use <owner/repo@skill>` (one-off prompt, no install).

## Step 2 — Security gate (MANDATORY, no token needed)

Run every candidate through the audit script. The audit endpoint is public, so
this always works:

```bash
python3 scripts/audit.py <candidate> [<candidate> ...]   # human-readable
python3 scripts/audit.py <candidate> --json              # machine-readable
```

A `<candidate>` is any of: `owner/repo@skill`, `owner/repo/skill`,
`github/owner/repo@skill`, or a full `https://skills.sh/...` URL — paste the
identifier or URL straight from `find` output.

The script queries all providers (Gen Agent Trust Hub, Socket, Snyk, Runlayer,
ZeroLeaks) and prints one verdict per skill. Process exit code = the worst
verdict across all inputs.

## Step 3 — Decide (the policy)

| Verdict | Exit | Meaning | Action |
|---|---|---|---|
| **ADOPT** | 0 | Every provider `pass`; no risk above `NONE`/`SAFE` | Safe to install |
| **REVIEW** | 10 | No `fail`, but a `warn` or `LOW`/`MEDIUM` risk | Do **not** auto-install — show the user the flagged provider + summary and ask before proceeding |
| **REJECT** | 20 | A provider returned `fail`, or risk is `HIGH`/`CRITICAL` | **Refuse.** Do not install. Report which provider failed and why |
| **UNVERIFIED** | 30 | No audits exist yet (`404`) | Treat as not-yet-safe. Do not auto-install; offer to inspect the source first |

Rules:
- **Default to safety.** Only ADOPT installs without asking. REJECT and
  UNVERIFIED are never installed. REVIEW requires explicit user consent and you
  must surface the specific risk (provider, riskLevel, summary).
- When recommending from a list, prefer ADOPT skills. If only REVIEW/REJECT
  skills exist, say so plainly rather than installing a borderline one.
- Always tell the user the verdict and the deciding provider(s) — don't hide a
  warn/fail behind a recommendation.

## Step 4 — Install approved skills

```bash
npx -y skills@latest add <owner/repo@skill>          # project scope
npx -y skills@latest add <owner/repo@skill> --global # user scope
```

To inspect source before trusting a borderline (REVIEW/UNVERIFIED) skill without
installing, use `npx skills use <owner/repo@skill>` or read the files via the
detail endpoint (see references/api-reference.md — needs a Vercel token).

## API details

For raw endpoints, response fields, identifier mapping, and how to obtain a
Vercel OIDC token for the token-gated discovery endpoints, read
**references/api-reference.md**. The everyday flow above needs no token.
