---
name: qa-tooling
description: Recommend context-appropriate QA tools while preserving observed availability, constraints, and safer alternatives.
---

# QA tooling recommendation

Use this skill when `qa`, `qa-init`, or `qa-strategy` needs to select tools for a
specific surface. It recommends; it does not install, configure, or pretend to run
tools. Read the [Tooling catalog](../../references/tooling.md) before producing a
recommendation.

## Inputs

- Observed stack and the surface or objective to test.
- Runtime and operating system, including the mobile target platform when applicable.
- A probe inventory keyed by executable or prerequisite. Every supplied probe has
  `state` (`positive`, `negative`, or `not_run`), `result`, and `evidence` containing
  the exact command/check and its observed output.
- CI environment, available devices/browsers, budget, data restrictions, and explicit
  authorization boundaries.

An absent probe means `unverified`; it is never rewritten as a negative result.

## Procedure

1. Match the requested surface and platform against `Recommendation rules` in the
   catalog. Do not return platform-incompatible mobile entries.
2. Prefer an existing tool. Recommend migration only when a concrete coverage,
   reliability, or evidence benefit outweighs its adoption cost.
3. Assign `available` only when the tool probe and every required probe in the catalog
   are `positive`. Assign `missing` only when the tool's own supplied probe is
   `negative`. Assign `unverified` when a probe is absent, `not_run`, or when a required
   prerequisite is negative. Preserve every supplied `result` and `evidence`; never
   synthesize a command result from an absent key.
4. For Web/UI exploration, distinguish `playwright-cli` from Playwright Test:
   `playwright-cli` operates an isolated interactive session using observed refs,
   snapshots, actions, and screenshots; Playwright Test owns repeatable suites and CI.
   Interactive CLI work does not replace a deterministic test suite.
5. Before stating a current version, compatibility, cost, or license, consult the
   official publisher documentation and record its URL and the verification date.
   Otherwise label that claim `unverified`; do not infer it from memory.
6. Return all candidates, including useful missing candidates, with a usable
   alternative and a context-specific reason. State limitations rather than widening
   scope or authorization.

The documented detection probes for the Web/UI CLI are `playwright-cli --version` and,
for a project-local package, `npx --no-install playwright --version`; the documented
local entry is `npx playwright cli`. These commands were reconciled with the official
publisher documentation on 2026-09-12. If an already available CLI is explicitly
authorized for exploration, the supported isolated-session sequence is
`playwright-cli -s=qa-report open`, `playwright-cli -s=qa-report snapshot`,
`playwright-cli -s=qa-report screenshot --filename=report.png`, and
`playwright-cli -s=qa-report close`.

## Output

Return one Markdown table with exactly these keys, in this order:

| tool | purpose | availability | evidence | prerequisites | alternative | reason |
|---|---|---|---|---|---|---|
| tool name | bounded use | available, missing, or unverified | exact detection result or `not probed` | platform, runtime, access, and verified cost/license facts | feasible fallback | why it fits this context |

Do not add hidden recommendation fields. Put official source URLs and verification
dates next to any verified current claim inside `prerequisites` or `evidence`.

## Failure modes

- Missing stack, surface, platform, or constraints: return candidates as `unverified`
  and identify the missing input in `evidence` and `reason`.
- Positive tool probe without a positive required device, browser, driver, SDK,
  service, credential, or authorization probe: preserve the supplied evidence but
  report the full tool as `unverified`.
- Unsupported platform: do not recommend the incompatible tool; return the compatible
  alternative or explain why none was verified.
- No suitable tool: return a row with `tool` set to `none verified`, availability
  `unverified`, and the next safe manual or built-in alternative.

## Safety

- Never install any tool automatically, never emit an installation command as an
  action, and never change personal or repository configuration.
- Require explicit authorization for load, penetration testing, production access, or
  external effects. Tool availability does not grant that authorization.
- For `playwright-cli`, use a task-owned named session. Never reuse personal profiles,
  export cookies or storage, or close sessions belonging to someone else.
- Review screenshots before attaching them. Treat snapshots as normalized text.
  Traces and videos are outside the v1 evidence attachment whitelist.
- Preserve data restrictions and do not send sensitive inputs to external services.

## Related skills

- `qa` routes an explicit tooling request here only when this installed skill is a
  regular local file.
- `qa-init` inventories observed tools and limitations before planning execution.
- `qa-strategy` consumes recommendations when selecting coverage and environments.
- `qa-specialist-web`, `qa-specialist-mobile`, and `qa-specialist-automation` apply the
  chosen tool within their narrower surface contracts.
