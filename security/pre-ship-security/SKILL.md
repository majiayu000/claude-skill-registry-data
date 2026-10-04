---
name: pre-ship-security
description: This skill should be used right before deploying or shipping to production — a fast security review of the finished code, not a deep audit. Trigger phrases include "ready to ship", "before I deploy", "security check before launch", "is this safe to ship", "pre-launch checklist", "review security", "did I miss anything", "production-ready", "harden before launch", "antes de subir a producción". It runs npm audit + a secret scan, re-checks the code against the OWASP prevention checklist, and escalates to specialized audit tools only when the app is high-risk.
---

# Pre-Ship Security

This is the last security gate before production: a quick, repeatable review of the finished code. It verifies that nothing slipped through what `secure-coding` prevented during the build.

Analogy: `secure-coding` is the seatbelt you wear *while* driving. A deep audit (Trail of Bits, fuzzing) is the garage that x-rays every part. This skill is the **walk-around inspection before a road trip** — lights, tire pressure, fuel. Quick, done every time, catches the obvious before you pull out of the driveway.

**It does not replace a professional audit for high-risk apps — its job is to tell you when you need one.** Security is never 100%; this skill is honest about that.

## Trigger

Run when the user is about to deploy, merge to `main`, launch, or asks "is this safe to ship?". It pairs with `secure-coding` (which ran during the build) and `deployment` (which ships it).

## Discovery (max 3 questions, only if unknown)

1. What does the app handle — **payments, personal data (PII), health, or crypto/keys**?
2. Is this the first production launch, or an incremental deploy?
3. Public-facing or internal-only?

## Step 1 — Automated quick scans

- **`npm audit --omit=dev`** (or `pnpm audit`) → fix high/critical advisories; don't ship known-vulnerable dependencies.
- **Secret scan**: `npx gitleaks detect` (and check git history) → no API keys, tokens, or `.env` committed. If something is found, **rotate the secret** — deleting the commit is not enough, it's in the history.
- Confirm `.env`, `.env*.local`, `*.pem`, `*.key` are git-ignored.
- **Client-bundle leak check**: grep the built JS for known key prefixes; on Vite, anything that isn't `VITE_`-prefixed must be absent from the bundle.

## Step 2 — Review the diff against the prevention checklist

Re-check the finished code — the `secure-coding` rules, now **verified instead of assumed**:

- **Authz on every endpoint?** Each route checks the user and resource ownership (no IDOR). A route with no explicit check is the bug.
- **Input validated?** Every handler parses input with a `zod` `.strict()` schema; no `req.body` spread into a DB write (mass assignment).
- **No raw SQL concatenation** — parameterized queries / ORM only.
- **CORS** is an explicit allowlist, not `*` with credentials.
- **Security headers** present (Helmet or platform headers): CSP, HSTS, X-Content-Type-Options.
- **Webhooks** verify signatures (Stripe, etc.) and read the raw body correctly.
- **Errors** don't leak stack traces in prod; **logs** contain no PII, tokens, or passwords.
- **Auth routes rate-limited**; passwords hashed with bcrypt/argon2.

## Step 3 — Risk gate (escalate when needed)

Based on Discovery answer 1, decide whether a deeper review is required — and be explicit that deep auditing is **out of this plugin's scope on purpose**:

- **Handles money, PII at scale, health data, or crypto/keys → recommend a deep audit** before or shortly after launch, and point to specialized tooling:
  - Static analysis: **Semgrep / CodeQL** (e.g. the `static-analysis` or Trail of Bits skills).
  - Dependency / supply-chain: **Dependabot, Snyk**, supply-chain auditors.
  - Fuzzing: only if there's parsing, crypto, or native code — **AFL++, libFuzzer** (the testing-handbook skills). Not relevant to a typical CRUD SaaS.
- **Standard low-risk CRUD SaaS → the checks above are a reasonable bar for launch.** Say so honestly: this is a *review*, not a guarantee.

## Legal exposure

If the product has users or a legal entity in Argentina, the EU, the US, Brazil or the UK, run the **`legal-docs`** plugin (`/plugin marketplace add MartinOlivero/saas-legal-docs`) in audit
mode before shipping. Two obligations from 2025 that almost no product has implemented yet,
because they are newer than most templates:

- **Botón de arrepentimiento** and **botón de baja de servicio** (Disposición 954/2025) —
  both required "a simple vista, en lugar destacado y en el primer acceso", with no prior
  login. A link in the footer no longer satisfies this.
- Any provider outside the AAIP adequacy list (**the US is not on it**) needs the
  international transfer declared with a legal basis.

That skill also compares the published legal text against the actual code, which catches the
worst class of problem: a policy promising encryption, deletion or "we don't share data" that
the codebase contradicts.

## Output

Deliver: the scan results (audit + secrets), a pass/fail list against the checklist with the exact `file:line` of anything to fix, and a clear verdict — **"safe to ship at this risk level"**, **"fix these N items first"**, or **"high-risk: get a deep audit"**. Never claim the app is fully secure.

## Reference

OWASP Cheat Sheet Series (~29k⭐), `npm audit`, gitleaks (~18k⭐), Helmet. Escalation targets: Semgrep/CodeQL, Trail of Bits skills, testing-handbook (fuzzing), Snyk/Dependabot.
