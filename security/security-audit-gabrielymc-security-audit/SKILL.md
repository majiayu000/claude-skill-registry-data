---
name: security-audit
description: "Pre-deployment security audit for web projects, especially vibe-coded ones. Use this skill whenever the user asks to review their project for security issues, wants a vulnerability scan before deploying, mentions 'security check', 'is my app secure', 'check for vulns', or any pre-launch safety concern. Also trigger for 'I built this with AI, is it safe?', 'review before production', or 'check for hardcoded secrets'. Covers secrets, auth, input validation, data protection, infrastructure, headers, and AI/LLM security. Works on any scope: full repo, single module, single file, or code snippet."
---

# Pre-Deploy Security Audit

A structured, evidence-based security audit for web projects. Prioritizes CRITICAL/HIGH findings early, demands concrete attacker evidence for every finding, and produces low-noise reports.

Designed for vibe-coded projects where AI-generated code may contain unreviewed security gaps.

## Reference Files

This skill uses modular documentation. Read files as needed, not all upfront:

| File | When to read | Content |
|------|-------------|---------|
| `references/checklist.yaml` | Always — core rules | 50 security rules in 7 categories with detection hints |
| `references/methodology.md` | For full repo audits | Phase-by-phase workflow, bash commands, tool fallbacks |
| `references/evidence-guide.md` | When writing findings | How to format findings with attacker prerequisites and exploit chains |

## Scope Intake

Before scanning, clarify the scope. The user may provide:

**Full repo** — audit the entire codebase. Proceed with all phases.

**Single module or directory** — audit a specific area (e.g., "check the auth module"). Focus checks on that directory but also check its dependencies and callers.

**Single file** — audit one file. Explicitly list your assumptions about context (what calls this file, what data flows in, what auth wraps it). These assumptions change the risk rating.

**Code snippet** — audit pasted code. State assumptions about the surrounding context. Flag what would change if assumptions are wrong.

For anything smaller than a full repo, start your report with an **Assumptions** section.

## Audit Workflow (Summary)

Detailed steps with bash commands are in `references/methodology.md`. Here is the high-level flow:

### Phase 1: Recon
Identify tech stack, map project structure, determine which checklist categories apply. Skip irrelevant categories — a static site doesn't need auth checks, a Vercel deploy doesn't need SSH hardening.

### Phase 2: Automated Scan
Run bash commands to detect the most common issues fast. This catches secrets, known vulnerable dependencies, debug mode, CORS misconfiguration, dangerous code patterns, missing security headers, and cookie misconfigurations. See `references/methodology.md` for all commands.

### Phase 3: Code Review
Read the code for issues that grep can't catch. Walk through each applicable rule from `references/checklist.yaml` where `check_method` is `semi`. Focus on:
- Auth middleware coverage (list all routes, mark which have guards)
- IDOR (do queries filter by current user?)
- Payment logic (is price calculated server-side?)
- File uploads (type, size, storage location)
- Error handling (what leaks to the client?)

### Phase 4: Report
Generate the report following `references/evidence-guide.md` format. Save as `security-audit-report.md`.

## Deployment Recommendation

Based on findings, give exactly one recommendation:

| Condition | Recommendation |
|-----------|---------------|
| Any CRITICAL `fail` | 🚫 **BLOCK** — do not deploy until fixed |
| Any HIGH `fail` (no critical) | ⚠️ **REVIEW** — strongly recommend fixing before deploy |
| Only MEDIUM/LOW findings | ✅ **PASS** — safe to deploy, fix when possible |

## Core Principles

**Evidence over volume.** Every finding needs: (1) what the attacker needs as a prerequisite, (2) the source→sink chain or concrete exploitation path, (3) the specific file and line. If you can't show how an attacker exploits it, downgrade or drop it.

**No fixes by default.** Report problems, don't auto-fix them. The developer decides how to remediate. You may suggest approaches in the remediation field, but never modify their code unless explicitly asked.

**Don't cry wolf.** Stripe publishable keys, NEXT_PUBLIC_ env vars, and test fixtures are not findings. If something looks dangerous but is intentionally public, mark it `pass` with a note explaining why.

**Respect severity.** A missing HSTS header is not critical. A hardcoded database password is. Follow the severity definitions in `checklist.yaml`.

**Acknowledge limits.** This is a code review, not a penetration test. Be transparent about what you checked and what you couldn't verify (e.g., runtime behavior, cloud IAM policies, network configuration that isn't in the repo).

**Match the user's language.** If they write in Chinese, report in Chinese. The checklist has bilingual titles to support this.
