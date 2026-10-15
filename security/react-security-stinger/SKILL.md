---
name: react-security-stinger
description: "Review React 18/19 security, including Next.js clients. Covers XSS, secrets and client trust. Delegate Next.js server surfaces to nextjs-security-stinger. Read-only."
license: AGPL-3.0-or-later
compatibility: Claude Code 2.1 or newer, Cursor 2.4 or newer, Codex, Cowork. Scripts need Python 3.9 or newer (standard library only). ripgrep recommended, not required.
metadata:
  author: Legion Code Inc.
  hive-drone: react-security-wasp-drone
  pair-drone: react-security-wasp-drone
  domain: React security audit
  version: 1.0.0
  research-window: 2026-03-30 to 2026-09-30
---

# React Security Stinger

Designed and built by Legion Code Inc.

## Where this skill's files are

Every path below (`guides/`, `references/`, `scripts/`) is relative to the folder that contains this `SKILL.md`. In Claude Code that folder is `${CLAUDE_SKILL_DIR}`. If that text was not replaced with a real path, find the folder yourself (for example with Glob for `**/react-security-stinger/SKILL.md`) and use it as `<skill>` in every command.

## Purpose

Find, confirm, and report the security weaknesses that are specific to React application code, for the security dimension of an `/audit-my-code` run (contract 1.0). It covers React 18 and 19 client components, server rendering, and React Server Components with Server Functions where they run outside Next.js (Vite with `@vitejs/plugin-rsc`, React Router RSC and Framework Mode, Waku, Parcel, RedwoodSDK, hand-rolled `react-server-dom-*` servers). It produces `02-security/findings-react-security-wasp-drone.jsonl`, `metrics-react-security-wasp-drone.json`, and `notes-react-security-wasp-drone.md`, with every finding backed by evidence, and changes nothing in the audited repository.

## When to use

- The orchestrator's stack routing says `react` (or `nextjs`, for the client half) and dispatches `react-security-wasp-drone`
- "Security audit this React app", "check our Vite SPA for XSS", "are we exposed to React2Shell", "is CVE-2025-55182 patched here"
- "Audit our Server Functions", "are our `'use server'` actions safe", "do we leak secrets in the bundle"
- Reviewing an AI-built React app (Lovable, Bolt, v0, Cursor, Claude Code scaffolds) for the usual generator mistakes

## When not to use

- Next.js server surfaces (Server Actions, route handlers, middleware or proxy, `next.config`, Next.js version advisories): `nextjs-security-stinger`
- Generic OWASP pass, repository-wide and git-history secret scanning, dependency advisories outside React: `security-stinger`
- Svelte or SvelteKit: `sveltekit-security-stinger`. Non-JavaScript backends: `polyglot-security-stinger`
- Fixing the issues: this Stinger is research-only and never edits the audited repository; remediation planning is the `mario` tier's job
- Architecture review without a security question: `react-stinger`

## Procedure

1. **Read the arming line and the contract** (`audit-my-code-stinger/references/audit-contract.md`). Write only inside `<workspace>/02-security/` and only to your per-source files.
2. **Scope and versions:** run [guides/00-scoping-and-version-detection.md](guides/00-scoping-and-version-detection.md). It runs `scripts/react_version_check.py` (lockfiles against the advisory table) and `scripts/sink_scan.py` (candidate lines), maps the stack per path, and decides which guides apply.
3. **XSS and SSR injection:** [guides/01-xss-and-injection-sinks.md](guides/01-xss-and-injection-sinks.md).
4. **RSC and Server Functions** (when present outside Next.js): [guides/02-rsc-and-server-functions.md](guides/02-rsc-and-server-functions.md).
5. **Secrets and data exposure:** [guides/03-secrets-and-data-exposure.md](guides/03-secrets-and-data-exposure.md).
6. **Auth, routing, client trust:** [guides/04-auth-routing-client-trust.md](guides/04-auth-routing-client-trust.md).
7. **Supply chain and AI-generated patterns:** [guides/06-supply-chain-and-ai-patterns.md](guides/06-supply-chain-and-ai-patterns.md).
8. **Write findings, metrics, and notes:** [guides/05-writing-findings.md](guides/05-writing-findings.md). Every candidate becomes a finding, a "Not confirmed" note, or a dismissed count; never a finding without evidence.
9. **Return** the verdict, finding counts by severity, every coverage cap, and the list of raw files written.

## References map

| Path | Load when |
| --- | --- |
| `references/REFERENCE.md` | finding which file holds a check, table, or script option |
| `references/checks-xss-and-ssr.md` | guide 01: RX and RS checks with detection, confirmation, severity, code pairs, refs |
| `references/checks-rsc.md` | guide 02: RC checks |
| `references/checks-secrets-and-data.md` | guide 03: SD checks |
| `references/checks-auth-routing.md` | guide 04: AR checks |
| `references/checks-supply-chain-and-ai.md` | guide 06, and any AI-built app: SC checks, AI patterns, React 19 behavior table |
| `references/advisory-table.md` | explaining or hand-checking a version finding; updating the script's table |
| `references/detection-patterns.md` | ripgrep commands per check id |
| `references/finding-rules.md` | before writing any finding, metrics, or notes |
| `references/research/distilled-react-security.md` | verifying a domain claim or settling a dispute |
| Source research archive (not shipped with the plugin) | Source-repository only; the shipped distillation summarizes it, do not require it |
| `scripts/react_version_check.py` | guide 00, every run |
| `scripts/sink_scan.py` | guide 00, every run; reruns with `--checks` to lift caps |
| `scripts/test/run_tests.py` | after editing either script or the advisory table |

## Related drones and stingers

- [react-security-wasp-drone](../../agents/react-security-wasp-drone.md) - The paired Drone in this pack; the orchestrator dispatches it with an arming line.
- [nextjs-security-stinger](../nextjs-security-stinger) - Next.js server boundaries; runs beside this Stinger on Next.js apps.
- [audit-my-code-stinger](../audit-my-code-stinger) - The run contract, tiers, routing, and the security merge script.
- `security-stinger` (core, when installed) - Generic OWASP pass, repository secrets, non-React dependency advisories.
- `polyglot-security-stinger` and `sveltekit-security-stinger` (this pack) - Other stacks in a monorepo.
- `react-stinger` in `web-development-tools` (confirm installed) - React architecture questions that come up during the audit.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [nextjs-security-stinger](../nextjs-security-stinger) - Next.js Server Actions, route handlers, middleware, config, and Next.js version advisories.
  - [audit-my-code-stinger](../audit-my-code-stinger) - Audit My Code contract, tiers, security routing, and merge.

<!--
Ship Gate removed: research-only stinger, produces no committable code.
-->

---

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.
