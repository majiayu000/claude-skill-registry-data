---
name: security-threat-analysis
description: "Use when analyzing a specific security threat from a referenced source (CVE, GHSA, security advisory, blog post, or write-up). Produces a human-readable remediation report with step-by-step instructions an AI agent can follow to eliminate the threat in the current project."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/php/core-standards.md`
- Apply `@rules/php/dependency-selection.md` — when the remediation playbook proposes adopting a **new** Composer package (e.g. a hardened replacement for a vulnerable library, or a security helper not previously installed), run the Activity gate + Compatibility gate from that rule and embed the selection note in the playbook step. Pin upgrades of an already-installed package do not need the full selection process.
- Apply `@rules/security/backend.md`
- Apply `@rules/security/frontend.md`
- Apply `@rules/security/mobile.md`
- Apply `@rules/reports/general.md`. When the remediation report is published as a **GitHub PR comment** (technical channel — the PR is the codebase tracker), it stays in canonical English per the rule's *Exception — technical CR findings on the GitHub PR* — or in the language the project manifest sets in `language.github` (*Project override — `language.github` in the manifest*). When it is published as a comment on the originating tracker issue / JIRA ticket (non-technical channel), it follows the language of the source assignment. CVE / GHSA identifiers, CWE / OWASP labels, package names, and code identifiers stay verbatim regardless of the surrounding prose language.
- Never include exploit payloads in a form ready for live attack; always redact secrets, PII, and identifying tokens
- Do not modify code in this skill — it produces a report only
- Do not duplicate `@skills/security-review/SKILL.md`; that skill reviews a change set for exploitable issues, this skill analyzes one referenced external threat

## Use when
- The user provides a URL or identifier (CVE-…, GHSA-…, advisory link, blog post, write-up) describing a specific security threat
- The user wants a remediation report that an AI agent can act on without re-deriving the attack
- The user asks to "analyze this CVE / advisory / vulnerability" in the context of the current project

## Inputs the agent must collect
Before generating the report, capture:
- **Source** — the URL or identifier of the threat
- **Affected component (claimed)** — package, framework, protocol, or pattern named in the source
- **Project context** — language/framework of the current repository (read from `composer.json`, `package.json`, lockfiles)
- **Scope** — whether the user wants threat analysis only, or analysis plus a fix plan tailored to the current project

If running interactively, confirm the inputs with the user. If running autonomously (e.g. invoked by `leonardo` in security analysis mode), infer them from the triggering issue and state the assumptions at the top of the report.

## Execution

### 1. Load the threat source
- Fetch the referenced URL with `WebFetch` (or the available MCP equivalent). If the source is a CVE/GHSA identifier without a URL, resolve it against `https://nvd.nist.gov/vuln/detail/<CVE>` or `https://github.com/advisories/<GHSA>` first.
- Extract: title, identifiers (CVE, GHSA, vendor ID), affected versions, attack vector, prerequisites, impact, patched versions, and the official fix or workaround.
- If the source is unreachable or paywalled, stop and report the gap — do not fabricate threat details.

### 2. Classify the threat
- **Category** — map to OWASP Top 10 / CWE where possible.
- **Severity** — Critical / High / Medium / Low, justified by impact and exploitability (CVSS if published).
- **Attack vector** — network / adjacent / local / physical; authenticated or unauthenticated.
- **Preconditions** — configuration, feature flags, exposed endpoints, or user roles required.

### 3. Match the threat against the current project
- Identify whether the project actually exposes the threat:
  - For dependency-based threats: read `composer.lock` / `package-lock.json` / `yarn.lock` and report exact installed versions; mark as **Affected** / **Not affected** / **Indeterminate**.
  - For pattern-based threats (XSS sink, SSRF, deserialization, etc.): grep for the named functions, classes, or syntactic patterns and list concrete file:line hits.
  - For configuration threats: inspect `.env.example`, framework config files, web-server config, or CI files for the dangerous setting.
- Never claim "not affected" without showing the evidence that was checked.

### 4. Draft the remediation playbook
- Prefer the official upstream fix (version bump, patch, configuration change) over ad-hoc mitigations.
- Provide an ordered, copy-pasteable instruction list an AI agent can execute end-to-end (commands, file edits, config keys, follow-up tests).
- For each step, name the file or command exactly; do not write "update the relevant config".
- Add a verification step (test, request, assertion, log line) that proves the threat is closed.

## Output Format

Render the report as Markdown using this structure:

```markdown
# Security Threat Analysis — <Threat Title>

## Source
- **URL / Identifier**: <link or CVE/GHSA id>
- **Published**: <date>
- **Patched in**: <upstream fixed version(s)>

## Summary (non-technical)
One short paragraph in plain language: what the threat is, why it matters, and what happens if it is not fixed. No code, no jargon.

## Classification
- **Category (OWASP / CWE)**: <e.g. A03:2021 / CWE-89>
- **Severity**: Critical | High | Medium | Low
- **CVSS**: <score if published>
- **Attack vector**: <network/local/…>, <authenticated/unauthenticated>
- **Preconditions**: <feature, role, configuration>

## Project Exposure
- **Status**: Affected | Not affected | Indeterminate
- **Evidence**:
  - `<file>:<line>` — <what was found>
  - `<dependency>@<version>` — <vulnerable range comparison>
- If status is *Not affected*, state which check disproved exposure.

## Remediation Plan
Ordered steps an AI agent can execute:
1. <Exact action — e.g. `composer require vendor/package:^X.Y`>
2. <Exact action — e.g. update `config/security.php` key `…` to `…`>
3. <Exact action — e.g. add middleware `…` to route group `…`>

For each step, include:
- **Target**: <file or command>
- **Change**: <minimal diff or command>
- **Why**: <one sentence linking the step to the threat>

## Verification
- **Manual check**: <request, screen, or log line that confirms the fix>
- **Automated test**: <test name and assertion that fails before the fix and passes after>
- **Coverage note**: <which changed code paths must reach 100 %>

## Residual Risks and Follow-ups
- <Anything the upstream fix does not cover>
- <Compensating controls if the upstream fix is not yet available>
```

Every section must be filled. If a section has nothing to report, write a short explicit note (e.g. `No residual risk identified.`) instead of leaving placeholders.

## Principles
- Evidence over assumption — never claim affected or not affected without a concrete check
- Prefer the upstream fix over hand-rolled mitigations
- Keep the playbook small, ordered, and copy-pasteable
- Surface uncertainty explicitly; do not fabricate CVSS scores or patch versions
- Redact secrets, tokens, and PII from any example payload

## Done when
- The referenced source was successfully loaded and summarized
- Classification, exposure, remediation, and verification sections are filled with concrete evidence
- The remediation plan lists ordered, executable steps targeting real files or commands in the current project
- The non-technical summary is readable without security background
- No sensitive data is exposed in the report

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
