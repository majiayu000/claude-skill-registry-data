---
name: using-security-audit
description: Pointer to Cloudflare's security-audit skill (cloudflare/security-audit-skill, MIT), which this library does not copy because upstream changes continuously. Use when asked for a security audit, a pen-test style review, "find vulnerabilities in this codebase", or a multi-phase vulnerability hunt with independently verified findings; it says whether the skill is already installed, how to install it safely, what it needs to run, and what to use instead when those needs are not met. Triggers include "security audit", "pen test", "find vulnerabilities", "vulnerability harness", "audit this repo for security".
---

# Using Security Audit

**A pointer, not a copy.** The skill is `security-audit` from [`cloudflare/security-audit-skill`](https://github.com/cloudflare/security-audit-skill) (MIT). It runs reconnaissance → coverage-led hunting → candidate validation → structured findings → independent verification → report, with fresh agents checking every finding. Upstream changes it continuously, so nothing of it is vendored here. Requirements below were read from upstream's README at commit `c1c8a8c`; if upstream's README says otherwise, upstream wins.

## 1. Is it already installed?

Look for `security-audit` in your available skills. **If it is listed, load it and follow it — stop reading this file.** It is the current version; this file is not.

## 2. If it is not, install it

```bash
npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit
```

Add `--global` for a user-level install (upstream README).

**Run it from outside xeno-skills.** On 2026-08-12 `npx skills add xenodeve/xeno-skills`, run inside this repo, destroyed its `skills/` tree (14 deletions). Installing `security-audit` from inside is unverified, but at best it writes a copy of upstream into the working tree, which is what this pointer exists to avoid. Change to your home directory or the project you are auditing, then check that the path the installer prints exists rather than trusting its success banner.

**Verified 2026-10-12:** from outside this repo, `npx skills add <url> --list` names exactly one skill, `security-audit`.

**Start a new session afterwards:** a skill installed mid-session may not be in the already-loaded list. Tell the developer that instead of loading it blind.

**Version:** the command installs the latest upstream, which is the point of not vendoring. Pinning to a commit or tag through `npx skills add` is **unverified**; do not report a pinned URL as working until you have run it.

## 3. What it needs — check before you start, not mid-audit

| Requirement | If missing |
|---|---|
| A model with tool use and **parallel sub-agents** | the independent-verifier phases cannot run; say so |
| **Node.js** | its `validate-findings.cjs` and `validate-coverage-ledger.cjs` cannot run |
| An **OS-enforced sandbox** for any target-controlled build, test, process or fixture — no external network, sanitized env, resource limits, writes only to scratch | it keeps the lead as `needs_validation` instead of running target code. That is correct behaviour, not a failure |

On Windows, establish whether a sandbox exists; do not assume one. If you cannot show it, the audit is read-only.

## 4. When not to use it

For a review of one diff or branch, or when a requirement above is missing and not fixable now, use `security-review` or `mcp__pal__secaudit` instead — and say that the full audit was not run and why. The full workflow is for an explicit codebase audit or pen-test request and is expensive (many agents, many phases).

## 5. Trust

Installing a skill puts another party's instructions in front of your agents; this one orchestrates sub-agents and may run target code. On the first install in a session, read the installed `SKILL.md` before running the workflow, and do not widen what it may execute.

Upstream's `needs_validation` is a lead, not a vulnerability — carry that register into any report.
