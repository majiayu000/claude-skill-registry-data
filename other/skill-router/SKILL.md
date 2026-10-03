---
name: skill-router
description: Use when picking which skill to invoke and more than one could apply, when a task spans several domains, or when the user asks "skill apa yang cocok", "ada skill untuk X?", "pakai skill yang relevan". Resolves overlap between the 200+ installed skills, sets precedence, and maps the Wedspirasi stack to concrete skill names. Also use after installing or removing skills, to regenerate the catalog.
---

# Skill Router

There are 200+ skills installed globally. Their names and descriptions are already
in context every session — this skill does not re-list them. It answers the harder
question: **when several skills could apply, which one wins, and in what order.**

## Precedence

Apply in this order. Higher tiers override lower ones on conflict.

1. **User instructions** — CLAUDE.md, AGENTS.md, direct requests. Always first.
2. **Project skills** (`<repo>/.claude/skills/`) — written for this codebase, so
   they beat any generic equivalent. In Wedspirasi that means `wedspirasi-dev`,
   `code-review`, `debug-helper`, `deploy-checklist`, `phase-guide`,
   `sprint-breakdown`, `template-conversion`.
3. **Process skills** — decide *how* to approach the work before touching it:
   `superpowers:brainstorming`, `superpowers:systematic-debugging`,
   `superpowers:test-driven-development`, `superpowers:writing-plans`.
4. **Implementation skills** — the stack- or domain-specific ones (`react-patterns`,
   `postgres-patterns`, `api-design`, …).

Process before implementation, always. "Bikin fitur X" starts with brainstorming,
not with `react-patterns`. "Fix bug Y" starts with `debug-helper` (project) or
`superpowers:systematic-debugging`, not with a patterns skill.

## Resolving the common overlaps

The 200+ skills come from three sources (personal, ECC bundle, superpowers plugin),
so several pairs genuinely collide. Defaults:

| Situation | Use | Not |
|---|---|---|
| Ideation before building | `brainstorm` (Indonesian, output: keputusan + asumsi) | `superpowers:brainstorming` unless you want the stricter English flow |
| Writing an implementation plan | `plan-writer` (writes to `docs/superpowers/plans/`) | `blueprint` — only for multi-session, multi-PR efforts |
| Writing a design doc / spec | `spec-writer` | `plan-writer` — that consumes a spec, it does not produce one |
| Debugging Wedspirasi | `debug-helper` (knows subdomain/Xendit/RLS/OTP failure modes) | `superpowers:systematic-debugging` for anything outside this repo |
| Debugging an agent or LLM loop | `agent-introspection-debugging` | the generic debugging skills |
| Reviewing a diff before merge | `code-review` (project) | `plankton-code-quality` for pure code-smell sweeps |
| Auditing auth / payment / secrets | `ecc-security-review` | `/security-review` (built-in, branch-scoped) or `security-scan` (dependency/secret scanning) |
| TDD discipline | `superpowers:test-driven-development` | `tdd-workflow` — overlapping ECC variant |
| Claiming work is done | `superpowers:verification-before-completion` | `verification-loop`, `qa-master` (heavier, pre-deploy GO/NO-GO) |
| Deciding visual direction | `frontend-design` | `frontend-design-direction` and `frontend-patterns` are for execution detail |
| Writing UI text | `natural-ui-copy` | any generic writing skill |

When two still look equal, prefer the more specific one, and say which you picked
and why in one line before proceeding.

## Wedspirasi stack map

| Working on | Reach for |
|---|---|
| Next.js / React components | `react-patterns`, `react-performance`, `frontend-patterns` |
| UI polish, spacing, motion | `make-interfaces-feel-better`, `motion-ui` |
| UI copy (ID/EN) | `natural-ui-copy` |
| Supabase schema, RLS, migrations | `postgres-patterns`, `database-migrations` |
| API routes, `ApiResponse<T>` | `api-design`, `backend-patterns`, `error-handling` |
| Xendit webhook, auth, OTP, secrets | `ecc-security-review`, `security-scan` |
| Coolify / Docker / Traefik deploy | `deploy-checklist` (project), `deployment-patterns`, `docker-patterns` |
| New invitation template | `template-conversion` (project) — has the mandatory 5-place registration |
| Playwright / E2E | `e2e-testing`, `react-testing` |
| Where are we, what is next | `phase-guide`, `sprint-breakdown` |

## Looking up the full list

Names and descriptions are already in context, so read them there first. For a
grep-able dump — useful when scanning by keyword rather than by memory:

- [references/catalog.md](references/catalog.md) — all installed skills, name + purpose.

## Keeping the catalog honest

The catalog is generated, not maintained by hand. After installing, renaming, or
removing skills:

```powershell
powershell -NoProfile -File "$env:USERPROFILE\.claude\skills\skill-router\scripts\build-catalog.ps1"
```

## Installation rules that keep skills discoverable

Skills are discovered **one level deep only**. This is the single most common
reason a skill "disappears":

- Correct: `~/.claude/skills/<skill-name>/SKILL.md`
- Broken: `~/.claude/skills/<bundle>/<skill-name>/SKILL.md` — the whole bundle is
  invisible. Flatten it, or install it as a plugin instead.
- The directory name is what gets registered, not the `name:` in frontmatter.
  Keep the two identical to avoid confusion.
- Gemini CLI does not read `~/.claude/skills/` at all. It scans `~/.gemini/skills/`
  (global) and `<repo>/.gemini/skills/` (workspace). Directory junctions into those
  paths work and stay in sync with the source. Verify with `gemini skills list --all`.
