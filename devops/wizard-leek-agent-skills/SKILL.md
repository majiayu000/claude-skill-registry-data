---
name: wizard
description: Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, creating credentials or CI secrets in a third-party dashboard, or running a one-off migration or cutover. For steps the agent can perform itself, perform them.
argument-hint: "The procedure to script (e.g. 'Stripe + Postmark setup for staging'); omitted, it is inferred from the conversation"
---

# Wizard

A **wizard** is a bash script that walks a human, stage by stage, through a manual procedure that is tedious to do by hand and tedious to re-explain to an agent every time. It opens each URL, says exactly what to click and copy, captures the values, writes them where they belong (`.env`, GitHub secrets), confirms at every stage, and shows how many stages remain. It might configure third-party services, run a one-off migration, or move the project from one state to another.

The UX is already solved by [template.sh](template.sh): stage-by-stage progress, confirmation gates, cross-platform URL opening (including WSL), hidden secret entry, idempotent `.env` upserts, `gh secret` / `gh variable` writes, and a closing summary. **Your job is only to scope the procedure and author its stages.** The library above the `STAGES` marker is identical in every wizard; that consistency is the point: never hand-edit it.

A wizard is ephemeral by default: built for one run, saved under `.scratch/` or `scripts/`, deleted when the job is done. Commit it only when the user wants a repeatable setup path that lives in the repo.

## Process

### 1. Scope the procedure

Work out every manual step the human must take and every value captured along the way. Read the repo first, don't ask cold:

- For setup: `.env`, `.env.example`, `.env.*`, `README`, `docker-compose*`, framework config (in Laravel, every `env('X')` call under `config/` is a value the wizard may need to produce), and `.github/workflows/*` (every `secrets.*` / `vars.*` reference is a value the wizard must produce).
- For a migration or transition: the current state, the target state, and the irreversible actions between them.

For each non-secret value, also look for what you already know or can derive: the repo name from `git remote`, the app name or URL from config, a region or project ID from infra files, a non-placeholder value in `.env.example`, a value the user said earlier in the conversation, or a conventional default (`us-east-1`, `main`). That becomes the value's **default**, so the human confirms it with Enter instead of retyping it.

Then show the user the ordered list of stages and the values each produces, with any defaults, and confirm: they may add, drop, or reorder.

**Done when:** every stage is named in order, and for each captured value you know (a) where the human gets it, (b) where it is written (`.env`, a GitHub secret, both, or nowhere; some stages are pure actions), (c) whether it is secret (hidden entry) or public, and (d) its default, if you know or can derive one.

### 2. Map each stage's journey

For each stage, write the precise path a human follows: which URL to open, what to do there, where a value is shown, which variable it fills: e.g. "Dashboard → Developers → API keys → Reveal test key → copy". Where you do not know the current UI or the exact command, say so and ask the user or check the docs (the `research` skill, where available). A step you are not sure exists is a question, not a stage.

**Done when:** every stage traces to concrete instructions a stranger could follow.

### 3. Author the wizard

Copy `template.sh` to the target path. Replace the example stage with one `stage` per step, in dependency order. Use the library helpers: `stage`, `say`/`step`, `open_url`, `ask`/`ask_secret`, `write_env`, `set_secret`/`set_var`, `pause`/`confirm`. Set `TOTAL_STAGES` to the number of stages you wrote.

Hold the bar the template sets: pass every known default as `ask`'s third argument (`ask APP_URL "App URL:" "https://staging.example.com"`), open the URL before asking for its value, `ask_secret` for anything secret, `write_env` every persisted value, `set_secret` only the values CI actually needs, and `confirm` before any irreversible action. Never put a secret in the script as a default: `ask_secret` takes none, and re-runs already offer the saved `.env` value. Each `stage` clears the screen so only the current step is visible: keep a stage to one focused task so nothing the human needs scrolls away. The library above the marker stays untouched.

**Done when:** every value from step 1 has an `ask` (carrying its default, where step 1 found one), a `write_env`, and (where CI needs it) a `set_secret` whose name exactly matches a `secrets.*` reference in a workflow.

### 4. Verify and hand off

- `bash -n <script>`; run `shellcheck` if available.
- `chmod +x <script>`.
- Trace it statically rather than running it: it opens browsers and blocks on human input. Check the step 3 criterion line by line.
- Tell the user how to run it. If it is a repeatable setup path, commit it and link it from the README so the next person runs the script instead of asking an agent.

**Done when:** the script parses, is executable, and the user has the one command that starts it.
