---
name: add-feature
description: >-
  End-to-end workflow to build a user-facing feature or matter: know where we are, plan with pwa-architect,
  build by owner agents in dependency order, verify, review (code + accessibility), close out. Holds the
  OWNERSHIP MAP (path → owner agent → skills). Use for "build X", "implement", "add a feature/matter/screen",
  "next feature", "continue", or "who owns this path?".
---

# Add a feature

## 0. Know where we are

- Read `CLAUDE.md` (rules, stack, layout) and `docs/product/competition-brief.md` (the `product-knowledge`
  skill).
- Backlog: `NOTEBOOK.md` if it exists, otherwise `docs/product/` and open PRs (`gh pr list`).
- A feature that still needs shaping (who it's for, which angle it wins: simpler / more convenient / more
  accessible / more matters) goes to the `product-manager` agent first. A new matter is designed by the
  `service-designer` agent (the `service-journeys` skill) before code.
- Check the deadline (session-start note). Near 30.11.2026, prefer finishing and polishing over starting.

## 1. Plan (pwa-architect)

Delegate to the `pwa-architect` agent with the request. It returns the user flow, files, data and
state-machine changes, owners per row, risks, and acceptance criteria with the proof for each. **If the plan
touches more than three files, show it to the user before writing code.**

## 2. Build (owners, in dependency order)

### §2 Ownership map

One owner per path. Every agent's "what you own" points here. The implementing agent writes the unit tests for
its own code.

| Path                                                                                                                                                                             | Owner                                       | Skills it follows                         |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ----------------------------------------- |
| `packages/core/` (except `src/assistant/`), `packages/content/` data (personas, registries, knowledge)                                                                           | `domain-engineer`                           | service-journeys, prototype-guardrails    |
| `packages/core/src/assistant/`, `apps/pwa/src/features/assistant/`, `apps/pwa/api/`                                                                                              | `assistant-engineer`                        | ai-assistant, accessibility               |
| `apps/pwa/src/{app,pwa,platform}/`, `apps/pwa/vite.config.ts`, `apps/pwa/index.html`, `apps/pwa/public/` (except `icons/`), `apps/pwa/vercel.json`, app `package.json`           | `pwa-engineer`                              | pwa-platform, scaffold-app                |
| `packages/ui/`, `apps/pwa/src/features/*` (except `assistant/`), `apps/video/` (demo video scenes)                                                                               | `ui-engineer`                               | design-system, accessibility              |
| `packages/brand/`, `apps/pwa/public/icons/`                                                                                                                                      | `brand-designer`                            | design-system, prototype-guardrails       |
| `docs/services/`, `apps/pwa/messages/pl/` (wording), voice sections of `docs/product/brand-voice.md`                                                                             | `service-designer`                          | service-journeys, plain-polish            |
| `apps/pwa/messages/{en,uk,de,cs,sk,lt,be}/`, `apps/pwa/messages/translations.lock.json`, `docs/i18n/`                                                                            | `language-engineer`                         | plain-polish, prototype-guardrails        |
| `packages/content/src/scenarios/` (text), `packages/content/src/assistant/` (persona, prompt text)                                                                               | `conversation-designer`                     | ai-assistant, plain-polish                |
| `docs/product/`                                                                                                                                                                  | `product-manager`                           | product-knowledge, competition-submission |
| `apps/pwa/e2e/`, `docs/quality/`                                                                                                                                                 | `qa-engineer`                               | verify-change, accessibility              |
| `.claude/`, `tools/`, `.github/`, `.husky/`, root configs (`package.json`, `turbo.json`, `pnpm-workspace.yaml`, `.prettierrc.json`, `commitlint.config.mjs`), `packages/config/` | `harness-engineer`                          | ai-harness                                |
| `docs/decisions/`                                                                                                                                                                | the owner of the area the decision is about |                                           |

Read-only roles: the `pwa-architect` agent (plans), the `code-reviewer` agent (diff review), the
`accessibility-auditor` agent (a11y audits) and the `plain-language-editor` agent (copy review). They report
and never fix.

Shared seams:

- **Scenario files** in `packages/content/src/scenarios/`: structure and machine wiring belong to the
  `domain-engineer` agent, and the words to the `conversation-designer` agent. Agree on the turn format first.
- **`docs/product/brand-voice.md`** is shared by section: values with the `product-manager` agent, voice, tone
  and word list with the `service-designer` agent, the assistant section with the `conversation-designer`
  agent. `docs/product/visual-identity.md` belongs to the `brand-designer` agent. Each edits only its own
  part.
- **Message keys:** engineers add keys with a draft Polish text. The `service-designer` agent owns the final
  wording. The `language-engineer` agent then carries it into the other 7 locales in the same change.
- **Integration** (commit, PR) is done by the main session (the `ship-branch` skill); the user merges.
- If an agent is unavailable, follow its skills directly in the main session.

### Order

Inside out: `packages/core` (machine + tests) → `packages/content` (persona data, scenario) → `packages/brand`
/ `packages/ui` (tokens, components) → `apps/pwa/src/features/*` (screens, wiring) → assistant hooks → e2e
flow. Independent pieces (a component and a machine against an agreed type) can run as parallel agents.

## 3. Verify

Follow the `verify-change` skill. For anything a user sees, that means a build + preview on phone viewports,
screenshots you actually look at, the Playwright flow with axe, and senior mode checked.

## 4. Review

- The `code-reviewer` agent on the diff. Fix **blocking** findings and re-run the checks.
- UI changes: the `accessibility-auditor` agent too.
- New copy: the owner signs off the wording (`service-designer` for screens, `conversation-designer` for the
  assistant), and the `plain-language-editor` agent reviews it against `docs/product/brand-voice.md`.

## 5. Close out

- Tick the item in `NOTEBOOK.md` (if used) and set `status: built` in the matter's `docs/services/<matter>.md`
  with the measured step count.
- Report what was verified and what wasn't.
- Ship with the `ship-branch` skill when the user wants it.
