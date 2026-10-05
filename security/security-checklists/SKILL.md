---
name: security-checklists
description: Progressive-disclosure security-depth modules for the security-reviewer. Holds boundary-keyed checklists (access-control, authn-session, injection, path-and-file, secrets-and-crypto, outbound-ssrf, supply-chain, config-misconfig, exceptional-conditions, llm-agent) as references/, each anchored on a current standard (OWASP Top 10:2025, ASVS 5.0, API Security Top 10:2023, Proactive Controls 2024, CWE Top 25, OWASP LLM Top 10:2025, OWASP Top 10 for Agentic Applications:2026). The work-loop's orchestrator loads only the boundary-matching modules and inlines them into the security-reviewer's brief; the subagent never self-discovers this skill. Not a reviewer prompt itself — it is the depth library the reviewer reasons from.
---

# Skill: security-checklists

This skill is the **depth library** behind the `security-reviewer` agent. The
reviewer's body carries the *universal method* (the three-bucket delegation
rule, load-context-first, the always-on STRIDE + LINDDUN open pass, the
established-helper-bypass meta-check, the severity rubric, the honest-limits
footer, the output format). The *shape-specific depth* — what to actually
check at each trust boundary — lives here, in the per-boundary `references/<module>.md`
modules, so the agent prompt stays lean and the depth scales without bloat.

> **Reliability-vs-security carve.** This library owns *security* config; the
> *reliability / ops* side of infrastructure (idempotent convergence, blast
> radius, environment isolation, cost/teardown, drift/rollback,
> observability/smoke) lives in the [`operational-safety`](../operational-safety/SKILL.md)
> skill, consumed by `quality-engineer`. The routing splits IaC-security →
> `config-misconfig`, IaC-reliability → `operational-safety`. The two are
> complementary lenses on the same infra diff — keep the split clean both ways.

## How it loads (orchestrator-driven, not self-discovered)

**The orchestrator drives loading; the subagent does not.** There is no
mechanism to force a subagent to invoke a skill, skill discovery is
model-invoked and adapter-variable, and the `security-reviewer`'s `tools:`
list does not even include a Skill tool. So depth must not depend on the
reviewer finding this library itself.

Concretely, at the work-loop's security-review step (and at the pre-EXECUTE
spec-stage pass), the orchestrator:

1. Detects which **trust boundaries** the diff or spec crosses.
2. Loads **only the matching modules** via the deterministic
   boundary→module routing authority — this skill's [Module index](#module-index)
   below (the `work-loop` security-review bullets dispatch against it rather than
   carrying their own copy).
3. **Inlines the selected modules' content** into the `security-reviewer`
   subagent's brief — so the reviewer receives a focused ~30-item checklist
   as prompt text, never a path to resolve.

Where an adapter *does* support subagent skill auto-discovery, that is a
redundant convenience layered on top — never the load-bearing mechanism.

## The three-bucket delegation legend

Every check in every module is tagged so the reviewer knows who owns it:

- **`tool`** — scanner-owned. Confirm the scanner is *wired*; don't re-check
  by hand. Detect the ecosystem's scanner rather than assuming one:
  `npm audit` / `pip-audit` / `govulncheck` / `cargo audit` / `bundler-audit`,
  or Snyk / Semgrep / CodeQL. If the delegated scanner is **absent**, do not
  silently skip (Tier-1 declare/detect/fail-clean): either reason the class
  best-effort and flag it `degraded: no scanner`, or state the gap explicitly
  ("class X is normally scanner-owned; none detected → wire one or accept the
  gap"). A silent skip is the worst outcome — it looks like coverage.
- **`hybrid`** — the scanner finds the flow; *you* judge the fix. Taint
  analysis can point at a sink, but whether the escaping, the confinement,
  or the safe-loader choice is correct is reasoning work.
- **`reason`** — reviewer-only. Logic-flaw access control, fail-open vs
  fail-closed, confused-deputy, privacy exposure — the classes scanners
  structurally cannot see. The highest-value findings live here.

## Established-helper bypass (the repo-aware meta-check)

For each boundary the change crosses, the most actionable real-world finding
is **"this code rolled its own instead of the repo's blessed helper."** Each
module names, in generic terms, the *kind* of helper that boundary usually
has. To resolve the repo's actual helper, the reviewer consults, in
precedence: the **`AGENTS.md`** "blessed security tools/helpers" list →
`CONVENTIONS.md` and any context other packs install (steering files, etc.)
→ **inference fallback** (grep the codebase for the de-facto helper). Flag
code that re-implements a boundary the repo already has a sanctioned helper
for. This skill carries the *mechanism* only — never any one repo's specific
helper names.

## Module index

This index is the **deterministic boundary→module routing authority** — the
`work-loop` security-review bullets (diff-stage and the pre-EXECUTE spec-stage
pass) dispatch against the **Boundary** column rather than carrying their own
copy. Match the trust boundary the change crosses to its module(s); the
**config-misconfig** row's *IaC / deploy-config* entry is the same one the
`work-loop` infra-flavored signal keys on.

| Module | Boundary (the change crosses) | Primary anchor |
|---|---|---|
| [`access-control`](references/access-control.md) | authz / object- & function-level access; a new or changed endpoint, handler, RPC | OWASP A01:2025 + API Security Top 10:2023 (BOLA/BFLA) |
| [`authn-session`](references/authn-session.md) | authentication, session, login, password, MFA, tokens (JWT / API key) | OWASP A07:2025 + ASVS 5.0 V6/V7 |
| [`injection`](references/injection.md) | untrusted input → interpreter / deserializer (SQL / shell / template / LDAP / HTML; deserialization) | OWASP A05:2025 (+ A08 deserialization) |
| [`path-and-file`](references/path-and-file.md) | filesystem path from input, file upload, archive extraction | CWE-22 / CWE-73 + ASVS 5.0 V12 |
| [`secrets-and-crypto`](references/secrets-and-crypto.md) | secrets, keys, hashing, signing, crypto, randomness | OWASP A04:2025 + ASVS 5.0 V11 |
| [`outbound-ssrf`](references/outbound-ssrf.md) | outbound HTTP / DNS / URL fetch, webhooks | OWASP A01:2025 (SSRF) + ASVS 5.0 V13 |
| [`supply-chain`](references/supply-chain.md) | dependency / lockfile / manifest change, build-artifact fetch (build trust) | **OWASP A03:2025 (new)** |
| [`config-misconfig`](references/config-misconfig.md) | CORS, IAM, IaC, server / framework / deploy config | OWASP A02:2025 |
| [`exceptional-conditions`](references/exceptional-conditions.md) | error handling, retries, fallbacks, fail-open paths | **OWASP A10:2025 (new)** (+ A09 logging) |
| [`llm-agent`](references/llm-agent.md) | prompts, model / tool exposure, MCP, model-output handling, agentic action | OWASP LLM Top 10:2025 + OWASP Top 10 for Agentic Applications:2026 |

Threat modeling (STRIDE + LINDDUN for privacy) and design-time Insecure
Design (A06 / Proactive Controls 2024) are **not** runtime modules: STRIDE +
LINDDUN ride the always-on open pass in the agent body, and Insecure Design
is realized by the spec-stage secure-design mode. Each module below carries a
**Spec-stage** section so the same depth backs the design-time pass in its
proactive-control framing.
