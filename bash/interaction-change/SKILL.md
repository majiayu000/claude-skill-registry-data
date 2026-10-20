---
name: interaction-change
description: Change how users talk to agents in agent-office — message states, InboxService, the HTTP inbox/replies routes, the IPC send path, the chat panel, the Claude Code hook (hooks/agent-office-hook.mjs), its wrapper (FsHookRunner) or HookService/installer. Use for edits in core message/hook domain, inbox-service, http-api, ipc-api, panel adapters, hooks/ or scripts/hook-install.ts.
---

# Change agent interaction

Rules: `PRIVACY_SECURITY.md` (the hook fails open; auth fails closed), `ARCHITECTURE.md` (contracts are additive), `TESTING.md`.

1. **Red** — state machine in `core/src/domain/message.test.ts`; behavior in `core/src/application/inbox-service.test.ts` (claim exactly once, `requireAwaiting`, long-poll via `ManualScheduler`).
2. **Transports** — `adapters/src/http/http-api.test.ts` (401/403/404/429/success) and `desktop/src/main/ipc-api.test.ts` (validation, error mapping).
3. **Hook** — `hooks/agent-office-hook.test.ts`:
   - Stop → `{"decision":"block","reason":…}` only when messages exist; posts `last_assistant_message` with `requireAwaiting: true` first.
   - UserPromptSubmit → `hookSpecificOutput.additionalContext`.
   - Server down / bad JSON / missing token / timeout → **no output, exit 0**, within 1.5s.
   - Message text is only ever passed to Claude as text — never to a shell.
4. **Install** — `core/src/domain/hook-config.test.ts` + `hook-service.test.ts` (idempotent, outdated → heal, foreign hooks untouched), `FsHookRunner` contract (wrapper runs the app binary with `ELECTRON_RUN_AS_NODE=1`), `scripts/hook-install.test.ts` (dev CLI).
5. **E2E** — `packages/adapters/test/e2e.chat.test.ts` (generic agent) and `e2e.claude-code.test.ts` (tailer + real hook script); `e2e.security.test.ts` stays green; app specs `desktop/e2e/{chat,settings}.spec.ts`.
6. **UI** — `web/src/app/view-models.ts` (`panelVM`, `hintFor`, `connectVM`, `emptyStateVM`) tests, then `adapters/dom/{panel,connect-panel,empty-state}.ts` with `textContent` only. Strings live in `web/src/app/connect-copy.ts`. Connection status reaches the UI as `ConnectionInfo` (`shared/src/desktop-api.ts`, built in `desktop/src/main/composition.ts`); it must never carry the token. The hook wrapper sets `AGENT_OFFICE_URL` from the live port (`FsHookRunner`), and a port change heals it.
7. **Manual check with a real session** (ask the user first — it edits their real `~/.claude/settings.json`): `make dev`, Settings → Install hook, message a working Claude Code session; the reply should appear when its turn ends. Uninstall afterwards if it was only for testing.

Known limit: Claude Code has no hook that can wake an idle session; messages to a waiting session arrive on the user's next prompt. Keep the UI hint honest about this.

Managed sessions (`/interaction-change` also covers them): the core service is `core/src/application/managed-session-service.ts` behind `ManagedSessions` and `ComposeMessage`; the SDK adapter is `adapters/src/agents/claude-sdk-runner.ts` (contract `agentRunnerContract`; the scripted runner `AGENT_OFFICE_FAKE_RUNNER=1` drives `desktop/e2e/session.spec.ts`). Context paths stay in main behind `ctx_` refs. The hook exits early when `AGENT_OFFICE_MANAGED=1`. Strings live in `web/src/app/session-copy.ts`.
