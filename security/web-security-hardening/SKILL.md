---
name: web-security-hardening
description: Security best-practices and hardening review for JavaScript/TypeScript web and Electron desktop applications. Use when asked to harden an app, review security posture or secure defaults, assess OWASP ASVS or Electron security-checklist alignment, improve HTTP headers or CSP, review forms/input validation/sanitization/uploads, strengthen authentication/passwords/sessions/secrets, secure Electron windows/preloads/IPC/navigation/permissions/protocols/updates/packaging, or evaluate deployment/operations controls. Produces an applicability-aware baseline gap analysis (Met / Gap / Not applicable / Needs verification), not exploit severity findings.
metadata:
  website: "https://photostructure.com/coding/"
---

# Web and Electron Security Hardening

Assess JavaScript/TypeScript web and Electron desktop applications against practical,
evidence-based security baselines. Report applicable preventive-control gaps even when
no exploit path is currently proven, while clearly distinguishing hardening advice from
vulnerabilities.

Use OWASP ASVS 5.0.0 as the pinned requirements backbone. Use OWASP Cheat Sheets,
current framework/library documentation, MDN, and NIST SP 800-63B-4 to explain and
implement web/service controls. When Electron is present, also use Electron's current
security checklist and official runtime, packaging, and platform documentation for the
desktop boundary. See [ATTRIBUTION.md](./ATTRIBUTION.md).

For web-only work, call the result an **ASVS-guided hardening review**, not ASVS
compliance or certification, unless every requirement at the selected level has been
enumerated, assessed for applicability, and supported by the evidence ASVS requires.
Electron reviews use the dual-baseline name defined below.

## Boundary with vulnerability review

Keep this skill separate from `web-security-review`:

| This skill | `web-security-review` |
| --- | --- |
| Asks whether applicable controls meet a baseline | Asks whether an attacker can exploit the code |
| Reports evidence-backed best-practice gaps | Reports only proven vulnerabilities |
| Uses Met / Gap / Not applicable / Needs verification | Uses Critical / High / Medium / Low |
| Prioritizes Essential / Recommended / Optional | Prioritizes exploit impact |

Do not call a missing control a vulnerability or assign CVSS-style severity without a
concrete attack path. If the review uncovers a proven exploit, list it separately under
**Escalate to vulnerability review** and recommend the `web-security-review` skill; do
not mix it into hardening counts.

## Core rules

- **Applicability before compliance.** Profile the application and select only controls
  that match its actual browser, API, identity, data, and deployment surfaces.
- **Effective behavior over package presence.** `helmet()` installed, a schema library
  imported, or a proxy named in docs is not proof that the control applies to every
  relevant route in the shipped configuration.
- **Research beyond report scope when needed.** Trace relevant callers, middleware,
  framework defaults, deployment config, and shared helpers; report only on the scope
  requested by the user. Do not load unrelated monorepo areas merely for completeness.
- **Credit framework protections.** Mark a control Met when a detected framework/version
  provides it effectively and no bypass disables it.
- **No cargo-cult controls.** Record Not applicable when a control has no relevant
  surface (for example CSP on a JSON-only API), with one-line reasoning.
- **No generic “sanitize everything.”** Validate syntax and business semantics at trust
  boundaries, encode for the output context, and sanitize only formats that intentionally
  accept active/rich content.
- **No live attacks.** Use static evidence and safe local tests only. Never probe shared,
  configured, or production services as part of a hardening review.
- **No auto-apply.** Propose changes; edit only when the user explicitly asks.

## Control states and priorities

Every assessed control has exactly one state:

| State | Meaning |
| --- | --- |
| **Met** | Effective implementation is evidenced in code/config/framework behavior |
| **Gap** | Control applies and evidence shows it is absent, disabled, or materially incomplete |
| **Not applicable** | The application lacks the surface or the threat model excludes it |
| **Needs verification** | The control applies, but a required fact cannot be established statically |

Prioritize gaps independently of ASVS assurance level:

| Priority | Use when |
| --- | --- |
| **Essential** | A broadly expected boundary is missing for an exposed, sensitive, or identity-bearing surface |
| **Recommended** | Meaningful risk reduction or resilience with clear applicability |
| **Optional** | Context-dependent defense-in-depth, operational maturity, or higher-assurance control |

Do not use priority as a disguised vulnerability severity. Consider exposure, data
sensitivity, user impact, existing compensating controls, implementation cost, and the
application's selected assurance level.

## Review workflow

Run these steps in order. Load reference files only when their domains apply.

### 1. Resolve scope

- If the user names paths or a diff, report only on those paths while researching
  callers/config elsewhere.
- Otherwise review working changes, including untracked files:
  ```bash
  if git rev-parse --verify --quiet origin/HEAD >/dev/null; then
    git diff --merge-base origin/HEAD
  else
    git diff HEAD
  fi
  git ls-files --others --exclude-standard
  ```

### 2. Build the application profile

Establish from code/config rather than assumptions:

- browser-rendered UI, SSR, API-only, webhooks, WebSockets, or mixed;
- public internet, trusted network, desktop/local-only, or self-hosted deployment;
- cookie session, bearer token, API key, OAuth/OIDC, password, passkey, or no identity;
- anonymous, personal, multi-user, multi-tenant, admin, and privileged workflows;
- sensitive data, uploads, payments, secrets, regulated/high-impact operations;
- reverse proxy, CDN, containers, database/cache/embedded storage, CI/CD;
- frameworks and installed versions from manifests/lockfiles.
- for Electron: the exact runtime version, target operating systems and package formats;
  all main/preload/renderer/worker/utility-process entry points, windows/views/webviews,
  content origins, IPC capabilities, sessions/partitions, deep links, custom protocols,
  signing/updater configuration, ASAR protections, and fuses.

State unresolved threat-model assumptions in the report.

### 3. Select the assurance baseline

Read [`references/baseline-and-reporting.md`](./references/baseline-and-reporting.md).

- Honor a user-selected ASVS level.
- Default to **ASVS Level 2** for production apps with authentication, private data,
  administration, or multi-user behavior.
- Use **Level 1** for a lightweight pass, low-risk public content, or broad portfolio
  screening.
- Use **Level 3** only for explicitly high-value/high-assurance systems.

Pin reports to **OWASP ASVS 5.0.0**. Cite a versioned ASVS requirement ID only after
verifying the exact ID against the official 5.0.0 source; never infer or invent IDs.
Selecting Level 2 also selects its MFA requirements; do not silently downgrade them
because MFA is uncommon in the reviewed product.

When Electron is present, also select the current official Electron Security Checklist
and platform guidance as the desktop-runtime baseline. Resolve the exact installed
Electron version and verify version-sensitive defaults and advisories against live
official sources when internet access is available. Report this as a dual **ASVS- and
Electron-guided hardening review**; do not imply that ASVS certifies the desktop runtime,
installer, updater, OS entitlements, or signing pipeline.

### 4. Select applicable domains

| Detected surface | Load |
| --- | --- |
| Always | `baseline-and-reporting.md`, `javascript-frameworks.md` |
| Browser UI, SSR, cookies, forms, cross-origin use | `browser-and-http.md` |
| Routes, request data, rendering, uploads, URLs/paths | `input-output-and-files.md` |
| Login, accounts, sessions, tokens, recovery, secrets | `identity-sessions-and-secrets.md` |
| Proxy/TLS, Docker/IaC, CI/CD, DB/cache/files, logs/backups | `deployment-and-operations.md` |
| Electron dependency, main/preload entry, window/view/webview, IPC, desktop packaging | `electron-controls.md` plus the relevant web/service references above |

Each domain reference file lists the **technique cards** filed under it. When you assess a
specific control, also load its card from
[`references/techniques/`](./references/techniques/) for concrete Node/JS anti-patterns,
named fixes, and version/CVE caveats. Load only the cards for controls actually in
scope—do not read the whole set.

### 5. Gather evidence

For each applicable control:

- trace middleware ordering and route coverage;
- inspect effective production config, not examples alone;
- account for reverse proxies/CDNs and framework defaults by version;
- identify compensating controls and intentional exceptions;
- record `file:line` evidence for Met and Gap states;
- use Needs verification only for a concrete missing fact, phrased as a question.

For Electron, gather evidence for every `WebContents` factory and child, preload/IPC
surface, session or partition, target platform, and production package configuration.
One secure window or development-mode observation does not prove the others.

Presence-only grep hits are leads. Absence from one file is not proof of a repository-wide
gap; check shared middleware, platform config, and deployment manifests first.

### 6. Consolidate root causes

Group repeated misses under the narrowest common remediation. For example, one missing
global cookie policy is one gap with affected cookies/routes, not twenty findings.
Separate controls when ownership, remediation, or applicability differs.

### 7. Report

Use this structure:

```markdown
## Web Security Hardening Review: <scope>

**Application profile:** <browser/API, identity, exposure, data, deployment>
**Baseline:** OWASP ASVS 5.0.0 Level <1|2|3>
**Desktop runtime baseline:** <when applicable: Electron Security Checklist and official platform guidance, verified on date against resolved Electron version>
**Assumptions:** <unresolved threat-model facts>

### Assessed-Control Summary
| Domain | Met | Gap | Needs verification | Not applicable |
|--------|----:|----:|-------------------:|---------------:|

**Coverage limitation:** <ASVS-guided subset, or complete requirement-by-requirement assessment>

### Essential Gaps
#### [HARDEN-001] <control> — Gap
- **Applicability:** Why this control applies here.
- **Evidence:** `file:line` and the effective behavior observed.
- **Recommendation:** Minimal concrete improvement.
- **Tradeoffs:** Compatibility, rollout, or operational caveats.
- **Source:** Versioned ASVS ID when verified, plus primary guidance.

### Recommended Gaps
...

### Optional Improvements
...

### Needs Verification
#### [VERIFY-001] <control>
- **Question:** What fact must be confirmed?
- **How to verify safely:** Static/config/local procedure.

### Controls Already Met
Concise bullets with evidence; do not reproduce the full checklist.

### Not Applicable
Concise control + reason.

### Remediation Roadmap
1. Now — essential boundaries and low-risk fixes.
2. Next — recommended controls and staged rollouts.
3. Later — optional/high-assurance improvements.

### Escalate to Vulnerability Review
Only concrete exploit candidates, excluded from hardening counts.
```

If no gaps remain, say which profile/baseline was assessed and that all applicable
controls **examined** were Met; do not imply that unexamined ASVS requirements passed.
Still list unresolved verification questions.

## Source freshness

Prefer primary sources in this order:

1. OWASP ASVS 5.0.0 for web/service control coverage and assurance level.
2. Electron's security checklist, API/runtime documentation, release timelines, and
   security advisories for Electron applications.
3. OWASP Cheat Sheet Series for implementation guidance.
4. Standards and platform documentation (NIST, RFCs, MDN, Node/framework docs).
5. Official library documentation such as Helmet.

When internet access is available, verify version-sensitive defaults against official
sources and the installed dependency version. Never use listicles as normative sources.
When offline, use the pinned references and state that current defaults were not
re-verified.

## References

| File | Covers |
| --- | --- |
| [`references/baseline-and-reporting.md`](./references/baseline-and-reporting.md) | ASVS levels, applicability, state/priority calibration, source policy |
| [`references/browser-and-http.md`](./references/browser-and-http.md) | Helmet/effective headers, CSP, cookies, CSRF/forms, CORS, browser isolation/cache |
| [`references/input-output-and-files.md`](./references/input-output-and-files.md) | Runtime validation, output encoding, rich-content sanitization, uploads, URLs/paths |
| [`references/identity-sessions-and-secrets.md`](./references/identity-sessions-and-secrets.md) | Passwords, MFA/passkeys, recovery, sessions, tokens, application crypto, secret lifecycle |
| [`references/deployment-and-operations.md`](./references/deployment-and-operations.md) | TLS/proxies, rate limiting, containers, storage, CI/dependencies, logging/errors, backups |
| [`references/javascript-frameworks.md`](./references/javascript-frameworks.md) | Express/Nest/Next/React/Vue/Angular evidence and secure-default checks |
| [`references/electron-controls.md`](./references/electron-controls.md) | Electron content/process isolation, preload/IPC, navigation, permissions, protocols, versions, packaging, updates, fuses, and storage |
| [`references/techniques/`](./references/techniques/) | 26 per-control cards: greppable Node/JS anti-patterns, named fixes, and CVE/version caveats; loaded per control in scope |

## Project adaptation

Treat repository security policy, threat models, architecture decisions, and documented
exceptions as input—not automatic exemptions. Record accepted risk and compensating
controls explicitly so future reviews do not reopen the same decision without new facts.
For Electron, adapt recommendations to content trust, native capability tiers, target
operating systems, packaging/update channels, and the behavior of the shipped artifact.
