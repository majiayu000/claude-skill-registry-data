---
name: configure
description: Use this skill when the user runs /configure, /configure --needs, or /configure --check. Also auto-invoked by env-detect.sh on fresh install (Layer 0) and by skills that find required config missing at runtime (Layer 2). Guides setup of config/tools.json and config/tools.local.json through a question bank; handles public/local split, diff-before-write, and resume semantics for interrupted commands.
config_requirements: []
next_suggestions:
  - when: no_active_work
    suggest: "run /start to begin a new task, or /plan if you already know what to build"
  - when: plan_drafted_and_unsigned
    suggest: "run /status to see your in-flight task"
  - when: always
    suggest: "run /status to see current state, or /start to begin a task"
---

# Configure — Guided Setup

Replace manual `config/tools.json` editing with a conversational wizard. Power users can still edit files by hand — this is an on-ramp, not a replacement.

## Before starting: check env.json flags

Read `.claude/sdlc/env.json` if it exists.

- If `config_corrupted: true` → skip the normal wizard; go to **Layer 3: rebuild** below.
- If `layer_0_pending: true` → this is a fresh install; run the full wizard and offer `/start` on completion.
- Otherwise → run normally.

## Invocation modes

**Full wizard** (`/configure` with no flags): ask all applicable questions.

**Scoped mode** (`/configure --needs tracker.type,tracker.host`): ask only the questions that map to the specified keys. Skip everything else. On completion, resume the original command that triggered this invocation.

**Dry-run** (`/configure --check`): read `config/tools.json` and `config/tools.local.json`, validate against the schema in `config/tools.example.json`, print a report of what is set, what is null/missing, and what would be asked. No prompts, no writes. Exit when done.

## Context-aware defaults

Before asking any question, inspect the environment to pre-select the most likely answer:

| Signal | Pre-selected default |
|---|---|
| `.github/` directory present | GitHub Issues |
| `git remote -v` contains `github.com` | GitHub Issues |
| `.linear.yml` present or `linear` on PATH | Linear |
| `jira` on PATH or `atlassian` in git remote | Jira |

User can always override; the default is a keystroke save, not a lock-in.

## Question bank (8 questions maximum)

Ask one at a time. Do not front-load.

**Q1 — Tracker type**
> Which issue tracker does this project use?
> A) GitHub Issues  B) GitLab Issues  C) Jira  D) Linear  E) None
> (pre-selected: \<detected default or "None">)

**Q2 — Auth token** *(only if Q1 ≠ None)*
> Paste your \<tracker> auth token. (Stored in `config/tools.local.json` — never committed.)
> Skip with Enter to omit; the plugin will accept any URL without host validation.

**Q3 — Tracker project** *(only if Q1 ≠ None)*
> Project key, repo slug, or team ID in \<tracker>?
> (e.g. `MY-PROJECT`, `owner/repo`, `eng-team-id`)

**Q4 — Multi-team sign-off**
> Will this project require sign-off from multiple roles before advancing phases? (Y/n)
> **If n: skip Q5–Q8 and finish.**

**Q5 — Role vocabulary** *(only if Q4 = Y)*
> Which sign-off roles does this project use?
> A) Suggested 9-role set: security, product, compliance, sre, legal, privacy, architecture, qa, ba
> B) Custom — enter a comma-separated list
> (No per-role email assignments here — signer identity lives in each sign-off file.)

**Q6 — Sync transport** *(only if Q4 = Y)*
> How should sign-off files be shared across machines?
> A) None — all signers commit directly to this repo
> B) Network share — a shared folder path
> C) Central git repo — a separate git repo URL
> D) MCP connector — a connector loaded in your Claude Code session
> E) Defer — decide later

**Q7 — Share path, repo URL, or connector name** *(only if Q6 = B, C, or D)*
> Enter the \<network share path | central git repo URL | MCP connector name>:
> *(For MCP: connector contract is deferred — RFC §3.7. Enter a placeholder name now or choose E to decide later.)*

**Q8 — Session sign-off hints** *(only if Q4 = Y)*
> Show personalized sign-off hints at session start? (Y/n — default Y)
> (Matches your git email against historical sign-offs to surface pending signatures.)

## Writing config

Before writing any file, show a diff:

```
Proposed changes to config/tools.json:
+ "tracker": { "type": "github", "host": "github.com", "project": "owner/repo" }
+ "approvals": { "roles": ["security", "product"], "share_path": null, "git_repo": null }

Write these changes? [Y/n]
```

On confirm:

1. Write non-secret keys to `config/tools.json`. If it doesn't exist, create it from `config/tools.example.json` as base.
2. Write secret keys (auth token) to `config/tools.local.json`.
3. If `config/tools.local.json` was written and `.gitignore` does not already exclude it, append `config/tools.local.json` to `.gitignore`.
4. Print: `Config saved. Run /configure --check to verify.`

On cancel: print "No changes written." and return.

## Layer 0 completion

After a successful full-wizard run when `layer_0_pending` was true in `env.json`:

> Setup complete. Start a task now? [Y/n]

If Y: invoke the `start` skill.
If N: print "Run /start or /plan when ready." and stop.

## Layer 2 resume

After a successful scoped run (`--needs`), print:

> Config saved. Resuming \<original command>…

Then re-invoke the original skill or command that triggered this invocation, with the new config in scope.

If the user cancels scoped configure, print:

> Cannot proceed without `<key>`. \<original command> aborted.

## Layer 3: rebuild

When `config_corrupted: true` in `env.json` (or when `config/tools.json` fails to parse):

> `config/tools.json` is not valid JSON. Options:
> A) Rebuild from scratch — backs up current file to `config/tools.json.bak` and runs the full wizard
> B) Open the file path for manual repair: `config/tools.json`
> C) Cancel

On A: copy `config/tools.json` to `config/tools.json.bak`, delete `config/tools.json`, then run the full wizard.

## Graceful degradation

- No git repo → skip context-aware defaults; still run the wizard.
- `config/tools.example.json` absent → use hardcoded question bank; do not block.
- Write fails (permissions) → surface the error verbatim; do not retry silently.

## What this skill must NOT do

- Do not write config without showing a diff and getting explicit confirmation.
- Do not store auth tokens in `config/tools.json` — always route secrets to `tools.local.json`.
- Do not ask more than 8 questions in a single wizard run.
- Do not auto-advance phases or run skills other than `start` (Layer 0 completion).

## Config key reference

| Question | Key | File |
|---|---|---|
| Q1 tracker type | `tracker.type` | `tools.json` |
| Q2 auth token | `tracker.auth_token` | `tools.local.json` |
| Q3 project | `tracker.project` | `tools.json` |
| Q5 roles | `approvals.roles` | `tools.json` |
| Q6+Q7 network share | `approvals.share_path` | `tools.json` |
| Q6+Q7 central git | `approvals.git_repo` | `tools.json` |
| Q6+Q7 MCP connector | `approvals.mcp.connector` | `tools.json` |
| Q8 hints | `display.session_signoff_hints` | `tools.json` |

## References

- `config/tools.example.json` — full schema reference
- `docs/rfcs/guided-entry-session-resume-multi-role.md` §8 — PR 8 spec and four-layer model
- `docs/rfcs/multi-team-approval.md` §3.1, §3.6 — why identity stays in sign-off files, not config

## Next step hint

**Layer 2 exception:** When this skill completes via Layer 2 scoped-run and resumes the original command, skip this step entirely — the resumed command's output is the next step.

For standalone `/configure` runs (full wizard or `--check`), pipe the `next_suggestions` conditions to `skills/_shared/next-hint.sh` and print any output:

```bash
printf '%s\n' \
  'no_active_work|run /start to begin a new task, or /plan if you already know what to build' \
  'plan_drafted_and_unsigned|run /status to see your in-flight task' \
  'always|run /status to see current state, or /start to begin a task' \
  | bash skills/_shared/next-hint.sh
```

Print any output verbatim. If the script outputs nothing, add nothing.
