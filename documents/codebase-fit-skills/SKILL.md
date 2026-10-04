---
name: codebase-fit-skills
description: Maps the repo using docs/ADVANCED_BUSINESS.md and docs/ADVANCED_TECHNICAL.md first, then code, to propose and author project-scoped skills and rules under .cursor/. Use when bootstrapping skills, refreshing after refactors, or aligning agents with Wengz documentation.
---

# Codebase-fit project skills (Wengz)

## Goal

Turn what is **documented and true in the repo** into **small, discoverable skills** under `.cursor/skills/<name>/SKILL.md` and keep **`.cursor/rules/*.mdc`** as short distillations. Agents should default to Wengz conventions (credits, roles, locales, tRPC) instead of generic patterns.

**Canon:** `docs/ADVANCED_BUSINESS.md` → `docs/ADVANCED_TECHNICAL.md` → `src/lib/error-handler.ts` / `notifications/` / `roles.ts`. See also `.cursor/README.md`.

## Current skill inventory

| Skill                        | Trigger                                                      |
| ---------------------------- | ------------------------------------------------------------ |
| `wengz-domain-workflows`     | Request lifecycle, multi-role dashboards, SLA, contact leaks |
| `wengz-credits-payments`     | Packages, subscriptions, proofs, wallet, withdrawals         |
| `wengz-notifications-locale` | Email / in-app / SSE locale                                  |
| `codebase-fit-skills`        | This meta skill — refresh config from docs                   |

## When to use

- User asks to study the codebase and create/refresh **project skills or rules**.
- Large refactor of `src/app/`, `src/server/`, or `prisma/`.
- Workflows diverge from **`docs/*.md`**.

## Storage rule

- Project skills: `.cursor/skills/<skill-name>/SKILL.md` (committed).
- Do **not** put project-specific skills in `~/.cursor/skills-cursor/`.

## Phase 1 — Map (read-only)

1. `docs/ADVANCED_BUSINESS.md`
2. `docs/ADVANCED_TECHNICAL.md`
3. Messaging: `error-handler`, `notifications/`, `messages/`
4. Code: `package.json`, `prisma/schema.prisma`, routers, dashboards
5. Existing `.cursor/rules/**` and `.cursor/skills/**`

## Phase 2 — Choose candidates

Prefer **one skill per fragile workflow**. Skip mega-skills that paste ADVANCED docs — **link** instead.

## Phase 3 — Author

1. Name: lowercase hyphens, max 64 chars.
2. Description: third person, WHAT + WHEN, trigger terms.
3. Body: steps + real paths + doc links; keep under ~500 lines.
4. Update `.cursor/README.md` inventory when adding/removing skills.
5. Keep always-apply rules short; put depth in skills.

## Phase 4 — Verify

- [ ] Descriptions have clear triggers
- [ ] Paths and doc filenames real
- [ ] No duplicate skills; cross-link related ones
- [ ] Rules do not contradict ADVANCED docs

## Output when analysis-only

1. Short inventory grounded in ADVANCED docs
2. Proposed skill/rule list
3. Highest-leverage next file

Implement files when the user confirms or explicitly asks to create/update config.
