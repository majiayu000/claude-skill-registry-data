---
description: Review and upgrade Claude Code CLI, Claude Agent SDK, and Anthropic SDK versions used in the project
---

# Update Claude Dependencies

Review the current versions of Claude-related packages and create an upgrade plan.

## Steps

1. **Find current versions** by reading these files:
   - `agent-container/package.json` — find `@anthropic-ai/claude-agent-sdk` and `@anthropic-ai/sdk` versions. The agent SDK version IS the CLI version (the CLI ships inside it as native-binary optional deps; SDK 0.3.x ↔ CLI 2.1.x by patch number)
   - `package.json` (root) — find `@anthropic-ai/sdk` version

2. **Check latest versions** by searching the web for:
   - Latest `@anthropic-ai/claude-code` version on npm / GitHub releases
   - Latest `@anthropic-ai/claude-agent-sdk` version on npm
   - Latest `@anthropic-ai/sdk` version on npm
   - Changelogs / release notes for each

3. **Analyze the diff** between current and latest:
   - List new features added between current and latest versions
   - Identify any breaking changes or deprecations
   - Note bug fixes relevant to our usage (especially memory leaks, stability)
   - Check if the npm install method is still supported or if native binary is required

4. **Assess risk** based on our actual SDK usage in the codebase:
   - `agent-container/src/claude-code.ts` uses `query()`, `tool()`, `createSdkMcpServer()`, message types
   - Root project uses `new Anthropic()` and `client.messages.create()`
   - Check if any APIs we use have changed

5. **Present findings** as a table showing:
   - Package name, current version, latest version, delta
   - Risk level (low/medium/high) with justification
   - Key new features and bug fixes worth upgrading for
   - Any breaking changes that would require code modifications

6. **Ask the user** if they want to proceed with the upgrade before making changes.

## Key files to update when upgrading

- `agent-container/package.json` — `@anthropic-ai/claude-agent-sdk` (which carries the CLI binary — no separate Dockerfile pin) and `@anthropic-ai/sdk`
- `package.json` (root) — `@anthropic-ai/sdk`
- `src/api/llm-sdk-bundle.ts` — **Regenerate after upgrading `@anthropic-ai/sdk`**. This is a pre-built browser bundle of the SDK served to dashboard iframes. Regenerate with:
  ```bash
  npx esbuild node_modules/@anthropic-ai/sdk/index.mjs --bundle --minify --format=iife --global-name=__AnthropicSDK_ns --platform=browser --external:'node:*' > /tmp/sdk-bundle.js
  echo 'window.__AnthropicSDK = __AnthropicSDK_ns.default || __AnthropicSDK_ns.Anthropic;' >> /tmp/sdk-bundle.js
  ```
  The `--external:'node:*'` flag is required since SDK 0.116+: the credential-chain code lazily `import()`s `node:fs`/`node:path` behind runtime guards that never fire in a browser, and esbuild errors on them without the external marker.
  Then replace the template literal in `src/api/llm-sdk-bundle.ts` with the contents of `/tmp/sdk-bundle.js` (escape backslashes first, then backticks and `${`), and verify the escaped literal evaluates back to the exact raw bundle

## Validation after upgrading

1. **Re-record the protocol fixtures, then run the container unit suite.** Frame ORDER (idle vs result, `background_tasks_changed` vs the `task_*` bookends) changes between CLI releases without a changelog line — 2.1.296 moved a finishing task's snapshot removal from before its terminal signals to after them — and only a live CLI shows it. After `npm ci` in `agent-container/`:
   ```bash
   ANTHROPIC_API_KEY=... node .claude/skills/update-claude-deps/capture-fixtures.mjs   # ~1.5 min, a few cents on haiku
   ```
   It records each scenario (`--list`: background Bash, background subagent, Stop with only a background subagent live, a subagent's own background Bash, SendMessage resume) into `src/shared/lib/container/__fixtures__/sdk<patch>-<name>/` in the host capture wrapper (`{t, message: {content: <frame>}}`), with a private `CLAUDE_CONFIG_DIR` so nothing from your `~/.claude` leaks in. Diff each new timeline against the previous `sdk<patch>-*` capture of the same scenario before anything else — that diff is the protocol change. Then add the new directories to `FIXTURE_EXPECTATIONS` in `agent-container/src/session-settlement.test.ts` (the discovery test fails until you do) and to the `SDK<patch>_FIXTURES` replay block in `src/shared/lib/container/sdk206-fixtures-replay.test.ts`, and run `cd agent-container && npx vitest run` plus the host replay files (`npx vitest run src/shared/lib/container`). Keep the older captures: they are the regression history for runtimes still on older CLIs.

2. **Gated session-GC E2E suites** (MANDATORY on any `@anthropic-ai/claude-agent-sdk` / CLI bump — CI never runs these, and they guard CLI-behavior assumptions the idle-eviction reaper depends on):
   ```bash
   cd agent-container
   RUN_SESSION_GC_E2E=1 ANTHROPIC_API_KEY=... npx vitest run src/session-gc.e2e.test.ts
   RUN_SESSION_GC_E2E=1 ANTHROPIC_API_KEY=... npx vitest run src/session-gc-durability.e2e.test.ts
   RUN_SESSION_GC_E2E=1 ANTHROPIC_API_KEY=... npx vitest run src/session-gc-background-stop.e2e.test.ts
   ```
   - Run the three files **separately**, never in one vitest invocation: the pgrep zero-process assertions in each see the other worker's CLI subprocesses.
   - Costs real API tokens (~$0.08, ~2.5 min total on haiku).
   - What they hold in place, and what breaks silently if an SDK/CLI change violates it:
     - the CLI does NOT emit `session_state_changed:idle` between a finished turn and a queued follow-up (violation → the reaper kills queued messages);
     - an interrupt of a live turn yields a `result` + `idle` so the session settles (violation → every user Stop pins a ~250MB parked subprocess forever);
     - the CLI exits cleanly on stdin EOF, flushing its transcript (violation → eviction silently loses the latest turns / `shouldQuery:false` appends on the next `--resume`);
     - `--resume` resumes in-place with the same session id, with prior context intact;
     - (background-stop file) while a background SUBAGENT is live the CLI emits NO idle after the lead turn's result (CLI 2.1.269+; backgrounded Bash still gets the premature idle), the reaper leaves the session alone, a Stop (`scope: 'turn'`) then is a fast no-op that keeps the process and the subagent (`claude-code.ts foregroundTurnEnded` / `pendingSends` decide "no foreground turn" — an interrupt sent in that state gets a receipt but never a result, and the fallback restart would kill the subagent), and the completion wake still runs to a result + idle.

3. **Task-tools opt-in** (MANDATORY re-verify on any CLI bump): `claude-code.ts buildQueryOptions()` lists TaskCreate/TaskGet/TaskList/TaskUpdate in `allowedTools` because CLI 2.1.233+ registers them by default only on older models (Claude 3.x, Opus 4.0–4.7, Sonnet 4.0–4.6, Haiku 4.5). Since 0.3.268 this is the documented path (SDK changelog: "elsewhere list them in `tools`/`allowedTools`"); the `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` env var is the documented CLI-side equivalent and works too (verified live on claude-opus-4-8 with 0.3.272: either path registers all four; TodoWrite is never registered alongside them). The in-chat task-list UI (`derive-task-list.ts`) and existing agent workflows depend on those tools, and the failure is silent (tools just stop appearing; nothing errors). To re-verify: run the `claude-prompt-drift` skill's capture after the bump and confirm the superagent-axis `tools.md` still lists all four Task tools. If they've vanished, try the env var as a fallback; if that is gone too, the CLI's only other re-enable path is a server-side feature flag that our `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` blocks — so escalate to a product decision (patch the gate, or retire the task-list UI's wire dependency) rather than shipping silently.

4. If either E2E file fails, do not ship the bump — check the settlement tracker (`agent-container/src/session-settlement.ts`) and graceful-stop path (`claude-code.ts stop({graceful:true})`) against the new CLI's stream behavior.

5. **Vendored bundled skill/workflow drift** (MANDATORY on any `@anthropic-ai/claude-agent-sdk` / CLI bump): `claude-code.ts buildQueryOptions()` sets `disableBundledSkills: true`, which strips every skill and workflow that ships inside the CLI, and the image-baked Gamut plugin (`agent-container/plugin/`, see its README) carries copies of the ones we keep — the `deep-research` workflow and the `workflow-authoring` skill (the Workflow tool's own prompt tells the model to load it; without it the model writes workflow scripts blind). Those copies no longer track upstream, so after `npm ci` in `agent-container/` run
   ```bash
   node .claude/skills/update-claude-deps/extract-bundled.mjs
   ```
   - exit 0 → no drift, nothing to do;
   - exit 1 → it prints a unified diff per drifted entry against what is embedded in the new binary. Read the diff (prompt wording, vote thresholds, fetch budgets, schema changes, new script-API guidance), then adopt it with `--write` unless a change is clearly wrong for us — each file must stay identical to upstream apart from the entry's `patches` in the extractor's `VENDORED` table (mechanical one-line substitutions such as the `gamut:` workflow prefix), so any bigger local edit means forking under a new name instead;
   - a drift hunk that REMOVES guidance deserves suspicion before `--write`: the prompt text is a template whose conditions call gates and env getters, which the extractor stubs as unset (`() => undefined`). A condition that tests a getter some other way can flip into the wrong branch — grep the body chunk for the hunk's text to see whether it sits inside a `${…?…:…}` and pin that identifier under `constants` if so;
   - exit 2 → the extractor could not find or parse a chunk, could not resolve an identifier the prompt text interpolates (pin it under that entry's `constants`), or a patch no longer matches upstream. Fix the extractor (its header comment explains the expected shapes) rather than shipping blind.
   While there, list what the new CLI bundles (`grep -a -o 'var i="[a-z-]*",e=i,' <binary>` for workflows; the `skills` array in a headless run's `system:init` message for skills) and decide whether anything new is worth vendoring the same way — `disableBundledSkills` hides all of it, so a useful addition is invisible until someone looks. The reverse leak happens too: a *built-in* skill is not "bundled" and survives the flag (2.1.296's `plugin-authoring`), so check the superagent-axis `messages.md` skill list from the `claude-prompt-drift` capture for anything not ours (`gamut:*` or agent-created) and switch it off in `claude-code.ts` `settings.skillOverrides`.

## Important notes

- The Claude Code CLI ships inside `@anthropic-ai/claude-agent-sdk` as per-platform native-binary optional dependencies (`claude-agent-sdk-<os>-<arch>`); the Dockerfile symlinks the bundled binary onto PATH. There is no separate install.sh/npm CLI install to pin — bumping the SDK version bumps the CLI.
- SDK and CLI versions track in lockstep by patch number (SDK 0.3.x ↔ CLI 2.1.x, e.g. 0.3.238 ↔ 2.1.238)
- `DISABLE_AUTOUPDATER=1` is set in the Dockerfile to prevent runtime updates
- Bundled CLI skills/workflows are disabled in agent sessions (`disableBundledSkills`); `deep-research` and `workflow-authoring` are vendored under `agent-container/plugin/` and checked for drift by `extract-bundled.mjs` in this skill's directory (validation step 5)
- Do NOT run `npm build` — use typecheck + lint to verify changes
