---
name: seed-test-env
description: Scaffold a fresh isolated Superagent data dir under ~/Downloads, seed agents, copy curated settings from the prod install, and print the launch command. Use when manually testing a feature against a clean state without touching the real install.
---

# Seed Test Environment

Creates a sandbox data directory so the user can launch the Superagent dev build against a clean, populated state — without polluting their real install at `~/Library/Application Support/Superagent/`.

## Inputs

`$ARGUMENTS` — free-form. Parse it for:
- **dir name** (first word, optional) — defaults to `superagent-test`. Used as `~/Downloads/<dir-name>/`.
- **agent specs** (the rest) — comma-separated `slug:description` pairs to seed. If absent, seed two default agents `agent-a` and `agent-b` instructed to use the x-agent (`mcp__agents__*`) tools on each other.
- **`--mode=web|electron`** flag — picks `npm run dev` (web/Vite) or `npm run dev:electron`. Defaults to `electron`.

Examples:
- `/seed-test-env` → defaults: dir `superagent-test`, agents A+B, electron
- `/seed-test-env xagent-test` → dir name only
- `/seed-test-env xagent-test triager:Email triager,replier:Reply drafter` → custom agents
- `/seed-test-env xagent-test --mode=web` → web dev server

If `$ARGUMENTS` is empty or ambiguous, briefly state the defaults you're using and proceed (don't ask). Confirm only if the target directory already exists with files (offer to delete-and-recreate vs abort).

## Procedure

### 1. Locate the source settings

**Source priority (settings.json):**
1. `~/Library/Application Support/Superagent-Dev/settings.json` — **prefer this**. The dev install has hardcoded direct LLM keys (Anthropic, OpenAI, OpenRouter, etc.) instead of relying on the `platform` LLM provider, which is flakey.
2. `~/Library/Application Support/Superagent/settings.json` — fall back only if Superagent-Dev doesn't exist. The prod install often uses `llmProvider: "platform"` which depends on a flakey remote auth; tests want direct keys.
3. `~/.superagent/settings.json` — last-resort fallback.

Pick the first that exists AND has a populated `apiKeys.anthropicApiKey` (or another working LLM key). If none have an LLM key, write the settings anyway and surface this loudly in the final summary.

### 2. Resolve target dir

`TARGET=~/Downloads/<dir-name>` (expand `~`). If it already exists and contains files, prompt the user once: delete & recreate or abort. After confirmation, `rm -rf` and recreate.

### 3. Create structure

For each agent, create `agents/<slug>/workspace/AGENTS.md`. Write them before the first launch of the data dir: the app imports agent directories into its catalog table once, by a data migration when the database is first opened, and does not scan the directory again. An agent directory added to an already-launched data dir will not show up. **Important:** the AGENTS.md lives inside `workspace/`, NOT directly under the agent dir. The file-storage layer (`src/shared/lib/utils/file-storage.ts:getAgentInstructionsPath`) hard-codes that path — putting it elsewhere makes the agent invisible.

AGENTS.md uses YAML frontmatter delimited by `---`. Required fields: `name`, `createdAt` (ISO string). Optional: `description`. Body is the agent's instructions. Mirror the format from `src/shared/lib/services/agent-service.ts:createAgent`. Example:

```markdown
---
name: Agent A
createdAt: "2026-04-21T12:00:00.000Z"
description: Test agent A
---

You are Agent A. (instructions body)
```

### 4. Copy settings.json (curated)

Read prod `settings.json` and write a filtered copy to `<TARGET>/settings.json`.

**Copy:**
- `apiKeys` (anthropicApiKey, deepgramApiKey, openaiApiKey, composioUserId — whatever is present)
- `llmProvider` and any provider-specific config
- `models` (agentModel, browserModel, summarizerModel)
- `app` — but **strip** `chromeProfileId` (path won't apply) and any path-bound fields
- `container` (lima/docker runner config — without this the container won't start). **Always override `container.agentImage` to `superagent-container:latest`** so the test instance uses the locally-built dev image instead of pulling the published one from `ghcr.io/skillfulagents/...`. That tag is what `npm run build:container` produces. If the user has tagged it differently, they'll tell you — otherwise default to `superagent-container:latest`.
- `skillsets` (so the test instance has the same skill catalog)
- `platformAuth` token block if present (so platform LLM provider keeps working)
- `auth`, `voice`, `shareAnalytics`, `customEnvVars` if present

**Skip:**
- `mounts` (host paths won't apply to a fresh test agent)
- `chromeProfileId`
- Any session-specific or per-agent state

If a key is missing in prod, just omit it — don't invent values. If `apiKeys.anthropicApiKey` is missing, surface that loudly in the final summary so the user knows to add one.

### 5. Final output

Show:
1. **Tree** of what you created (one `ls -R` or equivalent, terse)
2. **Settings keys copied** (just the top-level keys, not values — never echo secrets)
3. **Launch command** — exact one-liner, e.g.:
   ```bash
   SUPERAGENT_DATA_DIR=/Users/iddogino/Downloads/<dir-name> npm run dev:electron
   ```
4. **Notes** — anything skipped or missing (e.g. "no Anthropic key in prod settings — add one before testing").

Migrations auto-run on first launch via `migrate()` in `src/shared/lib/db/index.ts` — no separate `db:migrate` step needed.

## Implementation notes

- Use Bash + Write tools directly, don't print the commands and stop. Actually create the files.
- Never echo full secret values back to the user — show key names only.
- The `dev:electron` command is `install-electron && electron-vite dev` (the first part fetches the Electron binary if missing). The `dev` (web) command is `vite`. Both honor `SUPERAGENT_DATA_DIR` via `getDataDir()` in `src/shared/lib/config/data-dir.ts`.
- Don't modify the real prod data dir under any circumstances. All writes go to `~/Downloads/<dir-name>/` only.

## When NOT to use

- The user wants to test against their real data — they should just run the app directly.
- The user wants to write Drizzle migrations or run integration tests — those use in-memory SQLite, not a real data dir.
