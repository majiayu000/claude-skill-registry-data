---
name: wizard
category: developer-experience
description: Generate an interactive bash wizard that walks a human step by step through a manual procedure. Use when provisioning infrastructure, setting up credentials or CI secrets, walking someone through an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke it for steps the agent can perform itself.
codex-short-description: "Generate a bash wizard that walks a human through a manual procedure"
related-skills:
  - readme-generator
loop-eligible: false
compatibility: claude-code codex opencode
---

# Wizard

A **wizard** is a bash script that walks a human, step by step, through a manual procedure that's tedious to do by hand and tedious to re-explain to an AI every time. It opens each URL, says exactly what to click and copy, captures the values, writes them where they belong (`.env`, CI secrets), confirms at every stage, and shows how many stages are left. It might configure third-party services, run a one-off migration, or move the project from one state to another.

The UX is already solved by [template.sh](template.sh) — stage-by-stage progress, confirmation gates, cross-platform URL opening (including WSL), hidden secret entry, idempotent `.env` upserts, `gh secret`/`gh variable` writes, and a closing summary. **Your job is only to scope the procedure and author its stages.** The library above the `STAGES` marker is identical in every wizard; that consistency is the point — never hand-edit it.

A wizard is ephemeral by default — built for one run, saved to a scratch or `scripts/` path, deleted when the job's done. Commit it only when the user wants a repeatable setup path that should live in the repo.

## Process

### 1. Scope the procedure

Work out every manual step the human must take and every value captured along the way. Read the repo first — don't ask cold:

- For setup: `.env`, `.env.example`, `.env.*`, `README`, `docker-compose*`, framework config, and CI workflow files (every `secrets.*` / `vars.*` reference is a value the wizard must produce).
- For a migration or transition: the current state, the target state, and the irreversible actions between them.

Then show the user the ordered list of stages and the values each produces, and confirm — they may add, drop, or reorder.

**Done when:** every stage is named in order, and for each captured value you know (a) where the human gets it, (b) where it's written (`.env`, a CI secret, both, or nowhere — some stages are pure actions), and (c) whether it's secret (hidden entry) or public.

### 2. Map each stage's journey

For each stage, write the precise path a human follows: which URL to open, what to do there, where the value is shown, which variable it fills — e.g. "Dashboard → Developers → API keys → Reveal test key → copy". Where you don't actually know the current UI or the exact command, say so and ask the user or check the docs — never invent steps that may not exist.

**Done when:** every stage traces to concrete instructions a stranger could follow.

### 3. Author the wizard

Copy `template.sh` to the target path. Replace the example stage with one `stage` per step, in dependency order. Use the library helpers — `stage`, `say`/`step`, `open_url`, `ask`/`ask_secret`, `write_env`, `set_secret`/`set_var`, `pause`/`confirm` — and set `TOTAL_STAGES` to the number of stages you wrote.

Hold the bar the template sets: open the URL before asking for its value, use `ask_secret` for anything secret, `write_env` every persisted value, `set_secret` only the values CI actually needs, and `confirm` before any irreversible action. Each `stage` clears the screen so only the current step is visible — keep a stage to one focused task so nothing the human needs scrolls away. Don't touch the library above the marker.

**Windows note:** the template is bash. On Windows it runs under Git Bash or WSL — the `open_url` helper already handles `wslview` and `explorer.exe`. Say which shell to run it in when you hand it over.

### 4. Verify and hand off

- Run a syntax check (`bash -n <script>`); run `shellcheck` if available.
- Make it executable (`chmod +x <script>`; on Windows this matters only inside WSL/Git Bash).
- Don't run it end-to-end yourself — it opens browsers and blocks on human input. Trace it statically instead: every value from step 1 is captured and lands where step 1 said, and every `set_secret` name exactly matches a `secrets.*` reference in CI.
- Tell the user how to run it. If it's a repeatable setup path, commit it and link it from the README so the next person runs the script instead of asking an AI.

## Quality Loop

Before handing the wizard over, check it against the procedure it encodes:

1. **Complete** — every value the repo needs is captured by some stage; nothing is left for the human to guess.
2. **Traceable** — every instruction names a real URL, screen, or command; nothing is invented.
3. **Re-runnable** — a second run is safe: `.env` upserts replace rather than duplicate, and existing values offer themselves as defaults.
4. **Guarded** — every irreversible action sits behind a `confirm`, and every secret uses `ask_secret`.
5. **Library untouched** — everything above the `STAGES` marker is byte-identical to `template.sh`.

If two or more fail, fix and re-check. Cap at two passes.

## Delegation Map

| User need | Delegate via | Notes |
| :--- | :--- | :--- |
| The script needs non-trivial shell logic beyond the helpers | Write the shell directly | Keep the added logic below the `STAGES` marker |
| The wizard should graduate into a real CLI | Build a proper CLI instead | A wizard is a one-off; a CLI is a product |
| The procedure should become CI automation instead | Move it into the CI pipeline | If no human judgement is required, automate it rather than wizard it |
| The committed wizard needs a front-door mention | Invoke `readme-generator` | So the next person runs the script instead of asking an AI |

**Loop eligibility:** false — a wizard encodes one procedure and is run by a human on demand.

> **Host portability:** this skill writes a bash script and asks the user questions — no host-specific tools. See [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/wizard.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
