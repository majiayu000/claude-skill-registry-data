---
name: add-event-source
description: Add a new agent source/provider to agent-office (e.g. LangGraph, OpenAI Agents SDK, OpenTelemetry GenAI spans, Claude Code hooks). Use when asked to support or ingest agents from another framework or data source.
---

# Add an event source

Rules that apply: `TESTING.md` (TDD, ≥70%), `ARCHITECTURE.md`, `PRIVACY_SECURITY.md`.

First ask: can the producer just `POST /api/events`? If yes, document it in the README instead of adding code.

1. **Red** — `packages/adapters/src/sources/<name>/*.test.ts`: fixtures shaped like the real data with **invented** content. Test a pure mapper `toEvent(raw, ctx): AgentEvent | null`:
   - identity (`agentId` stable and namespaced, e.g. `lg:<id>`), `parentId` for sub-agents
   - `provider` (the zone) and `topic` (the row) — what would a user call this conversation?
   - status mapping onto `idle | thinking | tool | waiting | error | done`
   - malformed input → `null`
2. **Green** — `packages/adapters/src/sources/<name>/`: a pure mapper plus a driving adapter with `start()` / `stop()` / a testable `tick()`. It depends only on core ports (`ReportActivity`, optionally `AgentInbox`, `Clock`, `Scheduler`); put file/network access behind an adapter-local interface (like `TranscriptFiles`) so it can be tested in memory. Never throw out of `tick()`.
3. **Config** — a setting in `shared/src/desktop-api.ts` `SettingsSchema` (additive, with a default, and a restart field in `core/src/domain/settings.ts`), plus an env override in `adapters/src/config.ts` and `.env.example`. Start or stop it in `startBackend` in `desktop/src/main/composition.ts`.
4. **E2E** — `packages/adapters/test/e2e.<name>.test.ts`: real source → real core → `observe(office)` sees the agent in the right zone and row.
5. **Docs** — README "Sources" section: what is read, what is ignored, privacy notes.
6. **Privacy check** — only status, tool, title, model and ≤80-char snippets leave the source; nothing is logged raw.
7. `make check` (including `make arch`), then `/run-office` to see the new zone.

**Runtime-based providers** (a CLI agent-office can also start and manage, such as Codex or an ACP agent): this skill is not enough. Follow the checklist in `docs/provider-integrations.md` §8 (declaration, profile or runner, probe, optional observation hooks, composition, contract suites).
