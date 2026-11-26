---
name: agentHooks
description: Keep log-cli's CLI commands, MCP tools, agent hooks (Claude Code and Codex) and the live log in step (rule 55). Use when adding or changing a hook, a CLI command, an MCP tool, a page state or anything that writes progress lines, or when `bun run check:agentHooks` refuses a commit.
---

# agentHooks

One list drives every hook: `src/agentHooks/registry/index.ts` (`AGENT_HOOKS`).
Claude Code reads `.claude/settings.json`, Codex reads `.codex/hooks.json`; both
are written from the list and never edited by hand. Both hosts take the same
hook shape (TinyFish, 2026-10-20: code.claude.com/docs/en/hooks,
learn.chatgpt.com/docs/hooks): `hookSpecificOutput.additionalContext`,
`{"decision":"block","reason":…}` on Stop, exit 2 with stderr to refuse.

| Script | Events | What it does |
|---|---|---|
| `scripts/hooks/pageState.ts` | SessionStart, UserPromptSubmit, PostToolUse, Stop | Where every open browser is; after a log or shell call, a new known state with its resolver, or a failed step (unconfirmed page: snapshot, then resolve); on Stop, keeps the turn going while a browser sits on a state log-cli resolves, never on a person's state, and lets go when sent back once and nothing changed |
| `scripts/hooks/liveLogs.ts` | PreToolUse (Bash, PowerShell, Monitor) | Refuses a log run piped through tail/head and any hand-run `log …` (rules 26, 163); reminds a long one off a Monitor |
| `scripts/hooks/storage.ts` | SessionStart, UserPromptSubmit | `~/.logCli/runs` over 2 GB or the disk nearly full (rule 66) |
| `scripts/hooks/engines.ts` | SessionStart, UserPromptSubmit | The direct-API engines and each account's session and governor; a stale MCP server and uncommitted local changes, loudly (rule 163) |
| `scripts/hooks/knowledge.ts` | SessionStart | The knowledge base is there and how to search it |
| `scripts/hooks/inbox.ts` | SessionStart, UserPromptSubmit, PostToolUse | Anyone who wrote to a signed-in account's inbox since the last look |
| `scripts/hooks/queue.ts` | SessionStart, UserPromptSubmit, PostToolUse | What every account's queue did since the last look (rule 109) |
| `scripts/hooks/xLive.ts` | SessionStart, UserPromptSubmit, PostToolUse | What X's own client shows on each X account, new for this session |

SessionStart fires on startup, resume, clear and compact; PostToolUse on Bash,
PowerShell, Monitor and every `mcp__log__` tool (`TOOL_MATCHER`). The list itself,
with why each hook is there, is `AGENT_HOOKS`.

What each hook decides is pure and tested: `src/agentHooks/pageState` (`hookReply`),
`src/agentHooks/liveLog` (`liveLogVerdict`), `src/agentHooks/agentHooks.test.ts`.
The known states and their resolvers are `PAGE_STATES` in
`src/browser/flow/helpers/pageState.ts`, and each one's resolver as a ready
tool call is `RESOLVE_CALLS` (`{ tool, input }`, a click's ref read from the
step's snapshot; none for a person's state).

The hooks and the MCP read the open browsers the same way:
`readOpenBrowsers` and `browserView` (`src/browser/inspect/helpers/browserStates.ts`).
So a client without hooks (a claude.ai connector) gets the same thing in
every tool result: `browsers` (each open browser's step, page and known state),
`next` (the call that resolves it: make it, do not stop), `needsOwner`
(what only the owner clears) and `progress` (every streamed line, timed), with the
first lines of its text saying the same. `log browsers` (tool `browsers`) reads
them on demand.

## The live log

Every run writes `~/.logCli/mcp/<UTC day>.log` (`src/observability/liveLog`):
the MCP server as `<tool>`, the terminal CLI (`bin/log.ts`, including a detached
`inspect start`) as `cli:<command>`, Python lines as `worker`/`session`. One
Monitor shows a run however it started:

```bash
tail -f ~/.logCli/mcp/$(date -u +%F).log
```

A command run under Monitor itself: `<command> 2>&1 | tee <runFolder>/<name>.log`,
never through `tail`/`head` (the PreToolUse hook refuses it).

## Adding something

- **A hook:** add it to `AGENT_HOOKS`, write its script under `scripts/hooks/`
  with its decision in `src/agentHooks/<domain>/` and a test, then
  `bun run check:agentHooks --write` to rewrite both hosts' files.
- **A CLI command:** it becomes an MCP tool automatically (`toolsFromCommands`);
  if it can't be one, add it to `TERMINAL_ONLY` with why. If it runs long, add it
  to `LONG_RUNNING` (its description then points at the live log).
- **A page state:** add it to `PAGE_STATES` and its call to `RESOLVE_CALLS`; a
  resolver that names a command (`` `log inspect do solve` ``) must name a real
  one, and a call must name a real MCP tool. When Facebook's answers can
  decide it, give it an `answer` test on the step's exchanges (rule 73): with
  the answers there they decide, and its `text` is only used without them.
  `marketplaceCreateLimitReached` (`marketplace_new_seller_can_post_item:
  false`) and `marketplacePartnerFeed` (`product_details_type:
  PARTNER_LISTING`) are decided this way.
- **A new MCP server name:** change `MCP_SERVER_NAME` with `.mcp.json`.

## The check

`bun run check:agentHooks` (lefthook pre-commit and pre-push) refuses a commit
when the hooks, the CLI and the MCP tools drift apart: what it checks is in the
spec, [Agent hooks](../../docs/specs/agentHooks.md). It also refuses a
`.mcp.json` or a server name that differ from `MCP_SERVER_NAME`. Hook scripts
run against a scratch memory (`LOG_HOOK_MEMORY`), so the check never changes
what the real hook remembers.

## The context layer

On Claude Code, every hook that only adds context (prompt, after a tool, stop) is one http request to one warm service, not a `bun` start. Only the two refusing PreToolUse hooks start `bun`, in exec form with no shell. The conventions are in `docs/contextLayer.md`.

- **Is it up?** `curl -s http://127.0.0.1:47317/health`. If it isn't, the http hooks add nothing (they never block). The next session start, or the next shell call's `liveLogs` hook, starts it (`scripts/contextLayer/service.ts`, its log at `~/.logCli/contextLayer/service.log`).
- **How fast is it, and what did it decide?** One line per hook run in `~/.logCli/contextLayer/timings.jsonl`: event, provider, ms, chars and outcome.
- **Did a router change make it better or worse?** Run `bun scripts/useCases/benchRouter.ts`, add `--fit` to write the threshold, and compare plays caught, wrong fires and p95 with the last bench run.
- **A new play or a new way the owner asks** goes into the page's "How the owner asks for it", or as a labelled prompt in `~/.logCli/contextLayer/labelledPrompts.json`, kept on the owner's machine and never committed because the repo is public. The service reloads by itself.
