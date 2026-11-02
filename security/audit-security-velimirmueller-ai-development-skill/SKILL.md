---
name: audit-security
description: Use when asked to review a repo's security, before a release or go-live, or after adding auth, uploads, or a new integration. Scans secrets, dependencies, authz, headers and CI supply chain against security-baseline.md; reports ranked findings, fixes only what is approved.
---

# Audit Security

Cross-stack review against [security-baseline.md](../_shared/security-baseline.md) (OWASP Top 10:2025, ASVS 5.0). Commands per ecosystem and the authz checklist: [security-checks.md](security-checks.md).

## 1. Audit scope (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null
git rev-parse --show-toplevel && git status --porcelain | head
ls pnpm-lock.yaml package-lock.json bun.lock uv.lock go.mod Cargo.toml Dockerfile* docker-compose*.yml vercel.json supabase/config.toml *.tf .github/workflows 2>/dev/null
```

Take languages, framework, backend track, database, hosting, IaC and CI from the profile; detect the rest per [stack-profile.md](../_shared/stack-profile.md). Ask one question only when an ambiguity changes what to scan (for example "which of these two services is public-facing?"), and suggest `set-up-stack-profile`.

State the scope back in one line: what you will scan and what you skip.

## 2. Decide

Pick the checks that apply from [security-checks.md](security-checks.md) by profile: always secrets, dependencies, CI; headers if a web frontend or API exists; authz if there is any user data; IaC if `*.tf`; containers if a Dockerfile exists.

## 3. Check tool versions live

Scanners move. Verify the current version and flags per [version-protocol.md](../_shared/version-protocol.md) before running or recommending one (`gh api repos/gitleaks/gitleaks/releases/latest --jq .tag_name`). If a tool is not installed, say so and give the install line; run only read-only scanners. Do not install anything without approval.

## 4. Run the checks

For each applicable group in [security-checks.md](security-checks.md): run the command, then **read the code** the scanner cannot judge (authorization is almost never found by a scanner). Collect evidence as `path:line`. Never print secret values: show the file, line, rule id and the first 4 characters at most.

Groups: (A) secrets in tree and history, (B) dependencies, (C) authorization at the data boundary, (D) input validation and output encoding, (E) headers, cookies, CORS, (F) CI/CD supply chain, (G) config, IaC and containers, (H) logging and errors.

## 5. Report

Rank by severity: **Critical** (exploitable now, takeover or data exposure), **High** (exploitable with a precondition), **Medium** (weakens a layer), **Low** (hygiene). Each finding:

```
[Severity] <title>
Evidence: <path>:<line>  (<rule id or tool>)
Baseline: rule <n>; OWASP <A0x:2025>; ASVS v5.0.0-<chapter>
Impact: <one sentence: what an attacker gets>
Fix: <the exact change>
Effort: S/M/L
```

End with: counts per severity, what was **not** checked (and why), and any finding that needs a human decision (for example, "rotate this key": a secret in history is rotated, not removed).

Do not pad. No finding without evidence; no "might be vulnerable" without a concrete path. Mark uncertain items as "needs verification" with what to check.

## 6. Fix only what is approved

Ask the user which findings to fix (AskUserQuestion, up to 4 per round, Critical and High first). Then, per approved item: make the minimal change, one concern per commit or PR, add a regression test where the check is testable (for example user A cannot read user B's record). Never rewrite git history or rotate credentials without an explicit instruction. A leaked secret: tell the user to rotate it first, then remove it.

## 7. Verify

```bash
gitleaks dir . --no-banner --redact   # current subcommand per its release notes (v8: `dir`; older: `detect --no-git`); expected: no leaks found
```

Re-run each scanner you ran in step 4 and the tests you added. Expected: approved findings gone, the report's other findings unchanged, no new findings. State the commands and results. A second run of this skill on the same tree reports the same open items.
