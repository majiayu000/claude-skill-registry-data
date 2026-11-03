---
name: menuyukti-graphql-security-audit
description: >
  Evidence-based GraphQL API security audit for MenuYukti (apps/graphql and
  trusted callers in apps/web and apps/agents). Evaluates identity trust,
  authorization / IDOR / tenant isolation, abuse controls, information
  disclosure, injection surfaces, secrets handling, BFF trust boundaries, and
  authz test coverage. Generates scores, risk decisions, comparisons, and
  remediation roadmaps. Use when the user asks for a GraphQL security audit,
  API authz review, IDOR review, or GraphQL hardening assessment.
---

# MenuYukti GraphQL Security Audit

**Skill version:** `1.0.0`  
**Scoring version:** `1.0.0` (see [references/scoring-methodology.md](references/scoring-methodology.md))  
**Purpose:** Engineering security assessment of the GraphQL API and its trust boundaries — **not** a penetration test, legal opinion, or production red-team engagement.

Companion skills: [`menuyukti-graphql`](../menuyukti-graphql/SKILL.md) (layout), [`graphql-architect`](../graphql-architect/SKILL.md) (generic GraphQL security patterns in `references/security.md`), auth conventions in [`.cursor/rules/python-graphql-conventions.mdc`](../../../.cursor/rules/python-graphql-conventions.mdc).

## Do not run an audit unless requested

Creating or updating this skill is not an audit. Run an audit only when the user explicitly asks for **FULL**, **DELTA**, or **FOCUSED** mode.

## Primary questions every audit must answer

1. Can an unauthenticated or spoofed caller reach GraphQL operations that should require a real user?
2. Can user A read or mutate location/workspace/CRM/POS/analytics data belonging to user B (IDOR / tenant isolation)?
3. Are query abuse controls (depth, complexity, aliases, tokens, field selection) present and effective?
4. Does the API leak sensitive schema, stack traces, or cross-tenant existence signals?
5. Are JSON/`Node` and other flexible inputs safe against mass-assignment / injection style abuse?
6. Is the BFF / agents trust model (`X-User-Id` + `X-Internal-Api-Key`) correctly enforced end-to-end?
7. How has the risk posture changed since the previous comparable audit?
8. What is the minimum remediation set to clear P0/P1 findings?

Every comparable audit produces an evidence-backed score **0–100** from the **current repository state**. Never reuse prior conclusions without re-verification.

## Audit execution safety (mandatory)

**Read-only** with respect to application source and operational systems.

| Allowed                                                         | Forbidden without explicit approval                               |
| --------------------------------------------------------------- | ----------------------------------------------------------------- |
| Repository inspection                                           | Application source modification                                   |
| Safe static analysis                                            | Production DB changes                                             |
| Safe local tests (existing suite, no destructive fixtures)      | Live attacks against production / shared staging without approval |
| Report generation under `backlog/docs/audits/graphql-security/` | Exfiltrating secrets, sending tenant data externally              |
| Historical comparison                                           | Dependency installs, deployments, credential rotation             |

Do **not** invent exploit PoCs that write payloads or attack procedures into the repo. Describe risk and remediation at a high level; cite code paths as evidence. Record any test that could not run and why.

## Audit modes

### FULL AUDIT

Inspect the GraphQL API, auth helpers, server middleware, representative queries/mutations across domains, and trusted callers (`apps/web` GraphQL client + BFF, `apps/agents` `graphql_post`).

Produce all reports, overwrite `backlog/docs/audits/graphql-security/latest/`, and write an immutable snapshot under `history/`.

### DELTA AUDIT

Compare current codebase to the previous comparable full (or last full-baseline) audit.

Identify: improvements, resolved issues, new problems, regressions, score changes, new risk blockers. Revalidate affected workflows; do not assume a finding is resolved because code changed.

Recalculate only categories with sufficient current evidence; label other category scores **historical**.

### FOCUSED AUDIT

Target one or more scopes:

`identity` | `authorization` | `abuse-controls` | `disclosure` | `injection` | `secrets` | `trust-boundary` | `testing`

Generate findings for the scope. **Do not** replace the most recent full-audit baseline scorecard. Store focused outputs under `history/` with mode `FOCUSED` and update `progress.md` only for scoped notes.

## Category weights (fixed — scoring v1.0.0)

| Category                                |   Weight |
| --------------------------------------- | -------: |
| Identity and authentication trust       |      20% |
| Authorization / IDOR / tenant isolation |      30% |
| Abuse and DoS controls                  |      10% |
| Information disclosure                  |      10% |
| Injection and unsafe resolvers          |      10% |
| Secrets and sensitive data handling     |       5% |
| Client / BFF / agents trust boundary    |      10% |
| Authz automated testing                 |       5% |
| **TOTAL**                               | **100%** |

`Overall = Σ(CategoryScore × Weight / 100)`

If any weighted category lacks sufficient evidence, report a **provisional** overall score or `UNKNOWN` and state whether a reliable overall score can be calculated.

## Evidence rules

Never score from field names, TODOs, docs claims, or “looks guarded” alone.

Trace each check through the **request path**: caller → (optional BFF) → GraphQL context → auth helper → DB filter / ownership check → response.

For every finding record fields in [references/audit-report-schema.md](references/audit-report-schema.md).

**Statuses:** `VERIFIED` | `IMPLEMENTED_NOT_TESTED` | `PARTIAL` | `MISSING` | `UNKNOWN` | `NOT_APPLICABLE`

Do not invent evidence. Distinguish code inspection, automated tests, and operational verification.

## Risk decision (independent of score)

Emit exactly one: `ACCEPTABLE` | `CONDITIONAL` | `AT RISK` | `INSUFFICIENT EVIDENCE`

- Confirmed unresolved **P0** (auth bypass, cross-tenant read/write, internal key optional in prod-like config, trivial IDOR on money/PII) → cannot be `ACCEPTABLE` (`AT RISK` or `CONDITIONAL` with blockers listed).
- Unverified mandatory controls → cannot be unconditional `ACCEPTABLE`.
- High score cannot override P0 blockers.

## Execution workflow

Copy and track:

```text
Audit Progress:
- [ ] 1. Confirm mode (FULL | DELTA | FOCUSED) and scopes
- [ ] 2. Capture git metadata (branch, SHA, dirty flag)
- [ ] 3. Load prior comparable audit (if any) from history/
- [ ] 4. Inspect identity path (server context, internal key middleware)
- [ ] 5. Sample authorization across location/workspace/CRM/POS/analytics/Node APIs
- [ ] 6. Verify abuse extensions and limits
- [ ] 7. Review error shaping, introspection, public surfaces
- [ ] 8. Review flexible inputs (Node JSON, bulk mutations) and secrets handling
- [ ] 9. Trace web BFF + agents callers for header trust assumptions
- [ ] 10. Inventory authz tests (positive + negative / cross-tenant)
- [ ] 11. Score categories with check IDs from scoring-methodology.md
- [ ] 12. Evaluate attack scenarios (FULL; subset for FOCUSED)
- [ ] 13. Compute risk decision
- [ ] 14. Write reports from templates/ into latest/ + history/
- [ ] 15. Update progress.md (FULL / comparable DELTA only)
- [ ] 16. Validate report completeness against audit-report-schema.md
```

### Repo map (starting points)

| Area                  | Paths                                                                                     |
| --------------------- | ----------------------------------------------------------------------------------------- |
| ASGI / context        | `apps/graphql/server.py`, `apps/graphql/context.py`                                       |
| Auth helpers          | `apps/graphql/schema/auth.py`, `apps/graphql/access.py`                                   |
| Limits / complexity   | `apps/graphql/limits.py`, `apps/graphql/schema/__init__.py`, `schema/query_complexity.py` |
| Queries / mutations   | `apps/graphql/schema/queries/`, `apps/graphql/schema/mutations/`                          |
| Node handlers         | `apps/graphql/schema/node_handlers/`                                                      |
| CRM public / customer | `apps/graphql` CRM routes (`/crm/v1/…`), related schema modules                           |
| Tests                 | `apps/graphql/tests/` (esp. cross-user contexts), `apps/graphql/tests/auth_context.py`    |
| Web BFF client        | `apps/web/lib/graphql/client.ts`, `apps/web/app/api/**`                                   |
| Agents caller         | `apps/agents` GraphQL HTTP helpers (`graphql_post` or equivalent)                         |
| Conventions           | `.cursor/rules/python-graphql-conventions.mdc`                                            |

Expand search as needed; do not limit evidence to this map.

### Attack scenarios (minimum set)

1. Spoofed `X-User-Id` without valid internal API key (or with key leaked)
2. Authenticated user A passes user B’s `locationId` / analytics run id / node id
3. Mutation without `require_location_owner` / workspace check
4. Query returns empty for denial but nested fields still resolve foreign data
5. Batch / aliased query to bypass complexity or amplify cost
6. Introspection or error extensions leak internals in production config
7. Flexible `Node` / JSON create-update mass-assigns privileged fields
8. Agents or web BFF forwards attacker-controlled user id
9. CRM public path bypasses internal key and escalates to operator data
10. ID enumeration via sequential integer IDs + distinguishable error responses

Details: [references/attack-scenarios.md](references/attack-scenarios.md), [references/checklist.md](references/checklist.md).

## Sampling strategy (authorization)

For FULL audits, do **not** claim 100% resolver coverage unless enumerated. Instead:

1. Inventory root Query/Mutation mixins from `schema/query.py` / `schema/mutation.py`.
2. Classify each as: location-scoped, workspace-scoped, user-scoped, public/CRM, internal/admin, or unclear.
3. Deep-inspect a **representative sample** plus any high-risk domains (POS money, CRM PII, delete mutations, bulk upserts, analytics runs).
4. Flag unsampled mixins as residual risk in `executive-summary.md` (coverage %).

Prefer negative tests (`OTHER_USER` / foreign `location_id`) as strongest evidence.

## Report outputs

**Canonical output root:** `backlog/docs/audits/graphql-security/`

```text
backlog/docs/audits/graphql-security/
├── latest/          # overwritten by FULL (and comparable DELTA that publishes a new baseline)
├── history/YYYY-MM-DD_HH-mm_<commit>/   # immutable
└── progress.md
```

Fill templates from `templates/`. Machine-readable snapshot: `history/.../audit.json` per [references/audit-report-schema.md](references/audit-report-schema.md).

Historical audits are **immutable**. Never overwrite prior `history/` snapshots. Use stable finding IDs across audits (`FIND-GQL-…`).

**Do not implement remediation tasks** unless the user separately requests implementation.

## Progressive disclosure (read when needed)

| Topic                         | File                                                                   |
| ----------------------------- | ---------------------------------------------------------------------- |
| Check IDs and what to inspect | [references/checklist.md](references/checklist.md)                     |
| Attack scenarios              | [references/attack-scenarios.md](references/attack-scenarios.md)       |
| Scoring rubric                | [references/scoring-methodology.md](references/scoring-methodology.md) |
| JSON + markdown report schema | [references/audit-report-schema.md](references/audit-report-schema.md) |

### Templates

- [templates/executive-summary.md](templates/executive-summary.md)
- [templates/scorecard.md](templates/scorecard.md)
- [templates/findings-register.md](templates/findings-register.md)
- [templates/engineering-roadmap.md](templates/engineering-roadmap.md)
- [templates/audit-comparison.md](templates/audit-comparison.md)

## How to invoke

| Mode    | Example user phrasing                                                      |
| ------- | -------------------------------------------------------------------------- |
| FULL    | “Run a FULL GraphQL security audit”                                        |
| DELTA   | “Run a DELTA GraphQL security audit vs last full audit”                    |
| FOCUSED | “Run a FOCUSED GraphQL security audit on authorization and trust-boundary” |

After each FULL (or comparable DELTA that republishes baseline), update `progress.md` with score delta, P0 changes, regressions, and risk-decision changes. If scoring methodology version changed, do **not** show an unqualified score comparison.
