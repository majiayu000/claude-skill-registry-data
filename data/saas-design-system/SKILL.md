---
name: saas-design-system
description: "Section-by-section PRD authoring for one system — walks through each required section, cross-references dependencies."
argument-hint: "<system-name> [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Agent, AskUserQuestion, TaskCreate, TaskGet, TaskList, TaskUpdate, Bash(bash "*/.claude/skills/saas-design-system/../../hooks/yaml-helper.sh" resolve_config *), Bash(bash .claude/scripts/registry.sh *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,review_mode,automation,workflow,docs.density,system_overrides`

Resolved above — use as-is; `--review` overrides `review_mode`. No block →
defaults in `.claude/docs/config-resolution.md`.

# Design System

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

When this skill is invoked:

## 1. Parse Arguments & Validate

**Read `references/1-parse-arguments.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 2. Gather Context (Read Phase)

**Read `references/2-gather-context.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 3. Create File Skeleton

**Read `references/3-file-skeleton.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 4. Section-by-Section Design

**Read `references/4-section-design.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 5. Post-Design Validation

**Read `references/5-post-design.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 6. Specialist Agent Routing

This skill delegates to specialist agents for domain expertise. The main session
orchestrates the overall flow; agents provide expert content.

**Rows here are finer-grained than the nine `Category` values on purpose** — the
right specialist for billing is not the right specialist for auth, and both
are `Core Business Workflow`. Resolve in two steps: take the system's `Category` from
`features-modules-index.md`, then pick the row within it that matches what the system
actually does. Every category has at least one row, so nothing falls through.

| `Category` | Rows below to choose from |
|---|---|
| `Core Business Workflow` | Auth/sessions/RBAC · Billing/subscriptions · Core workflow/data pipelinevement · Character systems · Camera/input/controls |
| Core | Foundation/Infrastructure — Auth/RBAC/Multi-tenancy |
| Persistence | Foundation/Infrastructure — Database models, ORM, RLS, Redis |
| Billing | Billing — Subscriptions, Stripe checkout, customer portal, usage quotas |
| Workflows | Domain logic — Core business workflows, background jobs, workers |
| UI | UI systems — App Shell, design tokens, forms, tables, modals |
| Integrations | External APIs — Webhooks, third-party connectors |
| Content | Communication — UX writing, transactional emails, API documentation |
| Meta | Platform — Telemetry, analytics, error monitoring, audit logs |

If two rows fit, spawn the union of their Primary agents and say why.

| **Domain Category** | Primary Author | Key Specialists to Consult |
|----------------|---------------|---------------------|
| **Foundation/Infrastructure** (auth, multi-tenancy, database, queue, cache) | `database-architect` | `backend-engineer` (API design), `cloud-infra-engineer` (cloud infrastructure) |
| **Core Business Workflows** (primary CRUD, data pipelines, domain logic) | `lead-product-manager` | `backend-engineer` (architecture), `frontend-engineer` (UI), `database-architect` (schema) |
| **Billing & Monetization** (Stripe plans, subscriptions, usage quotas, invoices) | `billing-engineer` | `pricing-economist` (tier modeling), `database-architect` (quota tracking) |
| **Onboarding & User Lifecycle** (invites, activation steps, plan upgrades) | `lead-product-manager` | `onboarding-specialist` (friction reduction), `ux-content-strategist` (copy) |
| **Content, Microcopy & Docs** (transactional emails, empty states, API reference) | `technical-writer` | `ux-content-strategist` (voice/tone), `frontend-engineer` (templates) |
| **UI Systems & App Shell** (navigation, sidebar, breadcrumbs, responsive layout) | `ux-designer` | `design-system-director` (tokens/Tailwind), `frontend-engineer` (shadcn/Radix) |
| **AI & Automation Systems** (LLM pipelines, embeddings, prompt orchestration) | `ai-engineer` | `backend-engineer` (streaming/async), `database-architect` (vector storage) |
| **Integrations & Webhooks** (third-party APIs, OAuth providers, webhook dispatch) | `api-integrations-specialist` | `appsec-engineer` (signature verification), `backend-engineer` (retry queues) |
| **Realtime & Collaboration** (WebSockets, presence, live sync, notifications) | `realtime-websockets-specialist` | `frontend-engineer` (optimistic UI), `cloud-infra-engineer` (scaling) |
| **Analytics & Telemetry** (event tracking, funnel metrics, usage dashboards) | `data-telemetry-engineer` | `web-perf-analyst` (Core Web Vitals), `growth-director` (activation metrics) |
| **Security & Compliance** (RBAC, audit logs, tenant isolation, RLS) | `appsec-engineer` | `auth-security-specialist` (JWT/sessions), `database-architect` (RLS policies) |

**When delegating via the `Agent` tool**:
- Provide: system name, product concept summary, dependency PRD excerpts, the specific
  section being worked on, and what question needs expert input
- The agent returns analysis/proposals to the main session
- The main session presents the agent's output to the user via `AskUserQuestion`
- The user decides; the main session writes to file
- Agents do NOT write to files directly — the main session owns all file writes

---

## 7. Recovery & Resume

If the session is interrupted (compaction, crash, new session):

1. Read `production/session-state/active.md` — it records the current system and
   which sections are complete
2. Read `design/prd/[system-name].md` — sections with real content are done;
   sections with `[To be designed]` still need work. Read it by section: check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise find the headings: if `.basinfy/` exists, use `basinfy_search` and `basinfy_read`; otherwise use the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Grep tool (pattern `^#`, content mode) and Read those ranges with offset and limit.
3. Resume from the next incomplete section — no need to re-discuss completed ones

This is why incremental writing matters: every approved section survives any
disruption.

---

## Collaborative Protocol

**In `collaborative` mode (the default).** For `guided` and `autonomous`
modes, see the per-mode rules in `.claude/docs/automation-modes.md` — the
"Never" lines below describe what collaborative mode requires, not what
applies universally.

This skill follows the collaborative design principle at every step:

1. **Question -> Options -> Decision -> Draft -> Approval** for every section
2. **AskUserQuestion** at every decision point (Explain -> Capture pattern):
   - Phase 2: "Ready to start, or need more context?"
   - Phase 3: "May I create the skeleton?"
   - Phase 4 (each section): Design questions, approach options, draft approval
   - Phase 5: "May I update the entity registry? May I update the systems
     index? What's next?" — **not** "Run design review?": §5c forbids offering
     `/saas-design-review` inline, because the reviewing agent must not inherit this
     session's design history. Phase 5c presents the hand-off; it never asks.
3. **"May I write to [filepath]?"** before the skeleton and before each section write
4. **Incremental writing**: Each section is written to file immediately after approval
5. **Session state updates**: After every section write
6. **Cross-referencing**: Every section checks existing PRDs for conflicts
7. **Specialist routing**: Complex sections get expert agent input, presented to
   the user for decision — never written silently

**Never** auto-generate the full PRD and present it as a fait accompli.
**Never** write a section without user approval.
**Never** contradict an existing approved PRD without flagging the conflict.
**Always** show where decisions come from (dependency PRDs, pillars, user choices).

## Context Window Awareness

This is a long-running skill. After writing each section, check if the status line
shows context at or above 70%. If so, append this notice to the response:

> **Context is approaching the limit (≥70%).** Your progress is saved — all approved
> sections are written to `design/prd/[system-name].md`. When you're ready to continue,
> open a fresh Claude Code session and run `/saas-design-system [system-name]` — it will
> detect which sections are complete and resume from the next one.

---

## Recommended Next Steps

- Run `/saas-design-review design/prd/[system-name].md` in a **fresh session** to validate the completed PRD independently
- Run `/saas-consistency-check` to verify this PRD's values don't conflict with other PRDs
- Run `/saas-map-features next` to move to the next highest-priority undesigned system
- Run `/saas-gate-check technical-setup` when all MVP PRDs are authored and reviewed
