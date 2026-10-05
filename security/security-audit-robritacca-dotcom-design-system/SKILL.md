---
name: security-audit
description: "Independent security, privacy, and data-protection sweep of the repo and the live site: dependency and secret scans, API and AI-chat review against the OWASP LLM Top 10, HTTP hardening, CI/release posture, and analytics/privacy. Verifies findings against source or a live request, then reports — never fixes without a separate ask. Use when asked to run the security audit, check how secure the site is, or review privacy/data protection."
icon: security
invoke: ["run the security audit","/security-audit"]
---

# security-audit

A skeptical, evidence-first review of the whole system — the `@robr0/design-system` package, the Next.js website, the AI chat layer, the CI/release pipeline, and the analytics/privacy posture. Every claim is confirmed against source or a live request before it reaches the report; nothing is taken on trust.

## When invoked

Run when asked to "run the security audit" (`/security-audit`), or to check how secure/private the site is.

## Scope guardrails (read first)

- **Report only, by default.** This skill audits and reports; it does not change code. Applying fixes is a separate, explicit request. Say what is wrong and how to fix it, not "I fixed it."
- **Read-only and non-destructive.** Scans, reads, and a small, bounded set of live requests. No state-changing calls to any service.
- **Live probing is light and bounded.** A handful of requests to the production chat endpoint (injection, rate-limit, oversized-body, malformed-body). Stop the moment rate limiting kicks in — being throttled is the positive result, not a reason to push harder. Each request bills real API tokens, so keep the count low.
- **A clean pass is a valid outcome.** If a category has nothing worth flagging, say so and credit what is already strong. Never invent a finding to have something to report.
- **Evidence or it doesn't ship.** Every finding needs a `file:line`, a command result, or a captured live response. Kill false positives in a verification pass before writing anything up.

## The sweep

Work the surfaces below. The list says where to look, not what is there — read everything fresh each run, because the code moves.

### 1. Dependencies & secrets (automated)

- `npm audit --json` at the repo root (the single lockfile covers the `website` workspace too; run it in `website/` as well to be sure). Capture vuln counts and whether fixes exist.
- Secret scan of the working tree — `secretlint` with the recommended preset (write its config to a scratch dir, not the repo), or an equivalent scanner if one is installed.
- Secret sweep of the **full git history** (`git log -p --all`) for key patterns (`sk-ant-`, `ghp_`, `github_pat_`, `AIza…`, PEM headers, AWS keys) — the repo is public, so history matters as much as the tree. Confirm no `.env` file was ever committed (`git log --all --diff-filter=A --name-only`).
- Probe for the scanner binaries (gitleaks, trufflehog, osv-scanner, semgrep, trivy) and Docker before planning the sweep rather than assuming either way — on the Windows checkout they are generally absent (see the memory on Windows checkout quirks). Where they are missing, lean on `npm audit`, `npx secretlint`, and `git` history greps, which need no install, and offer to download a standalone scanner only with permission.

### 2. API routes & the AI chat (OWASP LLM Top 10)

The routes live under `website/src/app/api/` — read the directory fresh rather than working from a remembered list, it grows. The guardrails are in `website/src/app/api/chat/guardrails.ts`; the system-prompt boundary is `website/src/app/api/chat/persona.ts` (plus the easter-eggs file beside it). The `/api/mcp` route is a different animal: it calls no model, so the LLM Top 10 does not apply — check instead that every tool still reads only generated, already-published data, that tool arguments stay bounded, and that the deliberate absence of auth and rate limiting (recorded in that doc block) still holds up against what the tools now cost. The tool implementations themselves live outside the routes directory, in `website/src/lib/site-tools.ts` — the shared module behind both the MCP registrations and the chat's model-invokable tools, whose own doc block asserts the read-only-published boundary; a sweep confined to `app/api/` never opens it, so open it. Check:

- **Input validation & limits** — body shape, per-message and total body size, turn count. A cap on only the *last* message leaves earlier history unbounded.
- **Rate limiting & cost control** — the per-IP, daily, and spend guardrails, and crucially their **failure mode** (fail-open vs fail-closed) when the store is unreachable.
- **Prompt-injection defense** — the persona's refusal clause, and the architectural containment: the chat's knowledge is the build-generated corpus (`website/src/data/site-corpus.generated.ts`) plus the two lookup tools over the generated prop and token data, all three generated from already-published sources, so a jailbreak should yield nothing private. Verify the tool layer too (`website/src/lib/site-tools.ts` — its doc block asserts the boundary), not just the corpus.
- **Insecure output handling** — how model output is rendered. Markdown-only with an internal-path link allowlist is the safe pattern; raw HTML (`dangerouslySetInnerHTML`, `rehype-raw`) is the thing to hunt for.
- **PII / retention** — what the exchange log stores and for how long, whether it is disclosed, and whether visitor keys are truly anonymised (an unsalted IP hash is reversible).

### 3. HTTP hardening (verify against the live site)

Read `website/next.config.ts` for the CSP and headers, then **confirm against what the server actually sends** (`curl -sI` the live domain — headers can be edge-supplied and differ from source). Look for: a CSP without `'unsafe-inline'`/`'unsafe-eval'`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, `base-uri`/`form-action`, and whether `X-Powered-By` leaks the framework (`poweredByHeader`). Note any route that fetches a third-party URL without a timeout or runtime validation.

### 4. CI, release & supply chain

Read everything under `.github/` — the workflows *and* `dependabot.yml`, which lives beside the workflows directory, not in it. Check each workflow for a least-privilege `permissions:` block (its absence hands builds the repo-default token scope) and whether actions are pinned to SHAs vs movable tags. For dependency-scanning automation, know that a scanner can exist with no file at all: CodeQL runs via GitHub's default setup here, so confirm with `gh run list --branch main --json workflowName` before concluding anything is absent — a files-only sweep reports a false gap. Credit the release workflow's posture (OIDC Trusted Publishing, provenance, pre-publish consumer smoke test) where it holds.

### 5. Analytics & privacy

Read the analytics embed in `website/src/app/layout.tsx`. Check whether tracking scripts load **before consent**, whether a consent banner / consent-mode default exists, whether a privacy policy page exists, and what other third parties load at runtime (fonts, embeds, CDNs). For a public, internationally-reachable site this is usually the highest-impact category even though it is compliance, not exploitation.

### 6. Existing self-defenses (credit them)

The repo has build-time guards worth verifying and crediting: the corpus leak validator (`scripts/validate-site-corpus.mjs`), the corpus coverage check (`scripts/validate-corpus-coverage.mjs` — it reads the prerendered HTML, so it catches prose the corpus extractor cannot see), and the token-usage validator. Note where a good guard has a coverage gap (e.g. it scans the corpus but not the other files sent to the model as system prompts).

## Verify, then report

Run a verification pass over every candidate finding: confirm it against the current source or a fresh live request, and downgrade or drop anything the scans contradict (a clean `npm audit` turns "no dependency scanning" from an exposure into a process note). Rank what survives by real-world impact, not theoretical severity.

Then write the report:

- **A private Artifact page** (default-private — this is security content; do not commit it to the public repo or publish it publicly), plus a markdown copy in the scratchpad.
- Lead with a plain-English executive summary for a non-expert owner: the overall posture, the two or three things that actually matter, and what is merely cosmetic hardening.
- Each finding: what it is, the evidence (`file:line` or captured response), the realistic impact, and a concrete suggested fix — described, not applied.
- A **"what's strong"** section. An honest audit says what is good, not only what is wrong.
- A methodology/scope footer and the standards referenced (OWASP LLM Top 10, Next.js/Vercel hardening checklists).

Never state a count of findings from a past run as if it were fixed truth — each run counts its own. Cite paths that exist; the build's `validate-doc-refs` check holds this file to real repo paths.
