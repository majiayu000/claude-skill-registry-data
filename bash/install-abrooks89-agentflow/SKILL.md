---
name: install
description: The guided onboarding for agentflow — sets up a fresh machine AND orients the user on running the fleet. Interviews for the environment + first project profile, writes the typed config, provisions the Python/PyYAML/autodoc venv, installs the hooks, makes the venv the box's default python, hard-fails on missing required config, then walks the user through launching and operating the seven loops. The single hands-on guide (install + first use). Triggers on "set up agentflow", "install agentflow", "onboard this machine", "add a project to agentflow", "how do I use agentflow", "how do I run the fleet". (There is no `/install` command — this skill is read by path, not invoked as a slash command.)
---

# agentflow installer

The complete hands-on guide — the one place a person goes from a bare machine to a running
fleet. **Part 1 (install)**: interview → write config → write secrets one-way → provision the
venv → install hooks → make the venv the box's default python → presence-check and hard-fail.
**Part 2 (use)**: once the machine is green, orient the user on launching the seven loops and
operating the system day to day. Runtime contract lives in `manifest.md`; the mechanical
provisioning is `provision.py`. (The repo `README.md` is the *why/what* — manifesto, evidence,
architecture; **this skill is the *how*.**)

**Announce at start:** "I'm using the agentflow install skill to set this machine up — then I'll
walk you through running the fleet."

## When to use

- First-time setup on a new machine (no `~/.agentflow/config/` yet).
- Adding a new project profile (`projects/<name>.md`) to an existing install.
- Re-provisioning after moving the repo or changing the settings file.

## When NOT to use

- Routine config edits — edit `~/.agentflow/config/*.md` directly; the `SessionStart` hook
  re-resolves at the next session open.
- Runtime-only re-provision with no interview — run `provision.py` directly.

## Fresh-machine pre-reqs

Two things must exist BEFORE running `provision.py` on a brand-new machine:

1. **The named env vars must be set in the provisioning shell.** The config markdown holds
   env-var NAMES only (e.g. `notify.url_env: "NTFY_URL"` → `NTFY_URL`/`NTFY_TOPIC`); both
   provision step 3 and the resolver membership-test those names against `os.environ` and
   fail loudly when one is absent. Export them in the shell you run `provision.py` from
   (values persist in the `settings.local.json` `"env"` block / `.env` per Step 3 below, and
   in the login profile per Step 7, because the `"env"` block never reaches a shell).
2. **The Claude settings file must exist** (`~/.claude/settings.local.json` by default).
   Provision step 9 (the SessionStart hook) always reads it, and step 8 (`bootstrap.py`)
   reads it when the auto-allow hooks are kept (it is skipped under `--no-auto-allow`); either
   one **hard-fails if it is absent**, so the file must exist on both paths. Step 1
   (preflight) checks the same resolved path and refuses before anything is written. Do not assume signing in to Claude Code left one there —
   look, and if it is missing, create it yourself before provisioning:

   ```bash
   # posix — create the directory first; ~/.claude may not exist yet
   mkdir -p ~/.claude
   [ -f ~/.claude/settings.local.json ] || echo '{}' > ~/.claude/settings.local.json
   ```
   ```powershell
   # powershell — create the directory first, and write the file BOM-FREE.
   # Out-File -Encoding utf8 prepends EF BB BF on Windows PowerShell, and both readers
   # do json.loads(path.read_text(encoding="utf-8")) — install/provision.py step 9 and
   # skills/orchestrator/bootstrap.py — which rejects a BOM ("Unexpected UTF-8 BOM").
   $dir = Join-Path $HOME '.claude'
   New-Item -ItemType Directory -Force $dir | Out-Null
   $f = Join-Path $dir 'settings.local.json'
   if (-not (Test-Path $f)) {
     [System.IO.File]::WriteAllText($f, '{}', (New-Object System.Text.UTF8Encoding($false)))
   }
   ```

   An empty `{}` is enough: each step that runs parses the JSON and adds its own hook block to it.
   If it already has a `"hooks"` key, that must map each event to an array of matcher-block
   objects (`{"matcher": ..., "hooks": [ ... ]}`), as Claude Code's hooks schema requires; step 1
   refuses any other shape, naming the offending key, before anything is written.
   Alternatively pass `--settings-file` / `CLAUDE_SETTINGS_FILE` to point at an existing file.

---

## Step 1 — Interview (dialed-up asking-questions)

Load the **`asking-questions`** skill and run it dialed up: this is a weighted, multi-fact
setup. No config exists yet, so there is no injected `question_style` to read — use the
default, **`mobile-two-turn`**: the prose laying out the decision (options lettered,
pro/con, a recommendation) is its own turn, and the `AskUserQuestion` capture is the next
one — never both in one turn. Switch to **`inline`** only if the person says their client
shows prose and cards together; then the prose and the `AskUserQuestion` call may share one
turn, prose first. **Ask `question_style` early** and honor
the answer for the rest of the interview; it is a config field, not a guess.

Collect, in order:

**Environment (per machine)** — maps 1:1 onto `templates/environment.md`:
- `person.name`, `question_style` (`mobile-two-turn` (default) | `inline`)
- `data_root` (the single root all project files live under). **Do not ask for a machine-level
  `autodoc_root` as a matter of course — leave it `null`.** In `resolve_autodoc_root` it is the
  *fallback*, below a per-project `autodoc_root` in `projects/<name>.md` and above a
  derived `<data_root>/projects/<name>/autodoc/`, and a value here applies to EVERY project without its
  own override: until a corpus built there names its project, a two-fleet machine points both
  projects' code wiki at the same directory.
  Set it only when the operator has one code wiki for the whole machine and says so. Nothing
  creates the derived directory either — **and `/autodoc-init` does not create it**: it
  resolves its root through `resolve_autodoc_root`, as `/autodoc-update` does, and exits with
  `SystemExit` when none resolves. So "no autodoc root configured or derived" is the correct
  state for a fresh install and not a gap to fill in the interview — but tell the operator
  plainly that `/autodoc-init` will exit on that install until an `autodoc_root` is set (in the
  project profile, preferably, or here) — and that setting it later is not enough on its own:
  provision step 6 (the
  autodoc runtimes) was skipped, so they must install Node (with npm) and re-run
  `python install/provision.py --autodoc` before `/autodoc-init`, whose Step 0 guard otherwise
  stops the run. That re-run obeys the same auto-allow rule as any other: run the count
  probe in *Add another project later* first and add `--no-auto-allow` when it prints 0
- `git_host.kind` (github | gitea | gitlab | local) and `cli` (gh | glab | none). **The schema is wider than the implementation — only `gh` is verified.** `glab` is accepted here and then refused at the first tracker call, and `none` silences only the shared intake helper — steward's `issue create`, lead-dev's `issue comment` and every hardcoded `gh pr` call still shell out. Unless the operator is on GitHub, say so rather than letting them find out at first use; `docs/INSTALL.md` *Supported git hosts* has the three groups.
- `notify.kind` (ntfy | none) and, if ntfy, the env-var NAMES for URL + topic (`ascii_only`)
- `lock_dir`, `shell` (posix | powershell), `suite_root`. **Write `lock_dir` as an
  expanded absolute path, never a literal `%TEMP%/scratch`**: neither provision nor the resolver
  expands `%VAR%`, so the literal is read as a relative path, provision refuses to
  pre-create it, and the step-10 resolver dies on it after the venv and editable install have
  run. On Windows resolve it first — e.g.
  `python -c "import os; print(os.path.join(os.environ['TEMP'], 'scratch'))"` — and write the
  result with forward slashes; `~/...` is also fine, it is expanded the same way by both
- `worktree_root` — the root every lane's per-epic worktree is created under
  (`<worktree_root>/<project>/<epic-slug>`). Required, never defaulted, and the directory
  must already exist: a lane launches from the machine's launch directory, which sits in
  no repo, so a worktree path cannot be inferred from the working directory
- **the vault question — ask it ONCE, never block on it, never ask again — but ask it after
  Step 4, not here.** Its detector, `find_vault_candidates`, lives in `agentflow.config`, which
  imports PyYAML, so unlike `project_probe` below it has no script form that runs before the venv
  exists: during Step 1 it dies with `ModuleNotFoundError`, and `PYTHONPATH=skills/_shared` does
  not rescue it. Write Step 2's `environment.md` without a `vault` key (absent is valid and means
  "not asked yet"), then, once Step 4 has built the venv, run it with the venv interpreter by path
  and add the answer to `environment.md` before Step 6 checks the config:

  ```bash
  <suite_root>/.venv/bin/python -c "from agentflow.config import find_vault_candidates as f; print(chr(10).join(f()))"
  # Windows: <suite_root>\.venv\Scripts\python.exe -c "..." (same argument)
  ```

  OFFER what it found: it detects a `.obsidian/` directory, which Obsidian itself writes, so
  the hits are real vaults rather than folders named hopefully. Check the path before accepting one
  — a stale backup copy looks exactly like a live vault to that check, and picking it mirrors
  every future document into a dead tree.
  Three outcomes, and the third is the one that usually gets skipped:
  - **a path** — write the `vault` block (root + optional subdir + the delegated
    save/autodoc/mirror/hot paths).
  - **none found, and the user has one elsewhere** — take the typed path.
  - **no vault** — write `vault: null` EXPLICITLY. An absent key means "never asked" and a null
    one means "asked, answered no". Every mirror site no-ops either way, so nothing about
    mirroring changes; what the null buys is that `doctor` reads it and stops offering vault
    candidates to somebody who already declined. Leave the key out and that offer reappears on
    every run, which is how a diagnostic teaches people to skim it.
  Never block the install on any of it. Every mirror site already no-ops without a vault, so "no"
  is a first-class answer rather than a degraded mode.
- `parallel_builders` — two fields: `enabled` is the module's on/off switch and `count` is how
  many junior builder lanes it opens. **`count` is what the junior gates actually read**:
  `count: 0` is `lead-dev` standalone, `count: 1` runs `jr-dev-1` only, `count: 2` runs
  `jr-dev-1` + `jr-dev-2`, `count: 3` adds `jr-dev-3` — the interim fourth builder, a hand-copy
  of `jr-dev-2` that a later epic retires along with the value. The resolver rejects a `count`
  outside `{0,1,2,3}` and rejects `count > 1` without `enabled: true`. Note the stock default is
  `enabled: false` with `count: 1`, so leave `count` at `0` unless you mean to run a junior —
  and launch a junior loop only when you have set the dial for it

**The auto-allow hooks — ask ONCE, install-time only.** This answer writes **no config field**
(`SCHEMA.md` is frozen; do not invent one). It becomes a provision flag in Step 4 and nothing
else, so it does not persist: *Adding the profile* below re-derives it from the settings file.
Present the trade before asking:
- **What the hooks allow.** Provision step 8 runs `skills/orchestrator/bootstrap.py`, which
  writes PreToolUse hooks that return `allow` for `Edit`, `Write` and `Agent` on every path, and
  for 44 `Bash(...)` prefix globs, plus any listed in `AGENTFLOW_EXTRA_AUTO_ALLOW`.
  `Bash(git *)` matches every git command, `git push --force` and `git reset --hard` included,
  and several entries launch arbitrary code (among them `python`, `python3`, `node`, `npm run`,
  `make`, `cargo`, `go`, `yarn`, `pytest`, `awk`, `sed`, `xargs`, `env`, `find`). A hook checks
  each subcommand of a compound command, so an unmatched command chained after a matched one
  (`cd x && rm -rf y`) runs without a prompt too.
- **Where they apply.** Every Claude Code session started from the launch directory (the
  settings file is that directory's project settings), `/dev-manager` included — not only the
  fleet's unattended lanes.
- **What declining costs.** From bootstrap.py's own *Why this exists*: an unattended
  orchestrator run stops at every permission prompt a subagent's Bash, Edit or Write call
  raises, and the hooks are what let those calls run without one. Whether a lane launched with
  `--dangerously-skip-permissions` needs them has not been verified; tell the operator this is
  unverified rather than guessing either way.

The default is **keep** (today's behaviour). A "no" becomes `--no-auto-allow` on the Step 4
provision command.

**First project (per product)** — maps 1:1 onto `templates/projects.example.md`:
- `name` (MUST equal the filename stem), `canonical_repo.{host_ref,local_checkout,base_branch}`
- **`verification.strategy` — do not accept the first answer.** This field *is* the
  definition of `done` (the `lead-dev` §6 gate and the auditor both branch on it), so ask
  what would have caught their last real bug, not what test command they happen to have.

  **"I don't know" is a valid answer, and the expected one.** Most people cannot answer
  this cold, and a shrug is more honest than a guess. When it comes — or when an answer
  sounds like a guess — read the checkout instead of pressing. The reader is
  `agentflow.project_probe`, and **you can run it right here**: the module imports only the
  standard library (`json`, `sys`, `dataclasses`, `pathlib`) and has a `__main__` guard, so
  the FILE runs as a script on any Python 3.11+ before anything is installed. Only the
  **module** form (`python -m agentflow.project_probe`) needs the `agentflow` package, which
  the venv does not get until Step 4:

  ```bash
  # during Step 1, from the suite checkout — nothing installed yet, script form:
  python skills/_shared/agentflow/project_probe.py <canonical_repo.local_checkout>

  # after Step 4 the module form works too — but bare `python` does not reach the package
  # until Step 7 puts the suite venv on PATH, so call the venv interpreter by path:
  <suite_root>/.venv/bin/python -m agentflow.project_probe <canonical_repo.local_checkout>
  # Windows: <suite_root>\.venv\Scripts\python.exe -m agentflow.project_probe <checkout>
  ```

  It reports the languages, UI frameworks, browser tooling, test commands and dev commands
  it found, then proposes a strategy **with the evidence attached**. Show them that block,
  say which line drove the recommendation, and let them overrule it. Never paste the
  recommendation into the config as though they had chosen it — a proposal they accepted
  and a default they never saw produce the same YAML and very different confidence.

  If the probe finds nothing to go on, it says so rather than guessing; fall back to asking
  what breaking this project would look like to a user. If that still lands nowhere, the
  field is required, so Step 2 has to write something — write `none`, the enum value that
  asserts nothing (and what the probe itself recommends when it finds no evidence) — then
  come back and correct `projects/<name>.md` once you know.

  The strategies themselves:
  - **A green unit suite over a broken app is the failure this question exists to prevent.**
    Unit tests call functions directly, so they pass whether or not anything calls them. If
    the product has a user-facing surface, the suite is a regression floor, not the gate.
  - `web-journey` — requires `staging.url`; also collect `roles` + `test_login`.
  - **A `SKILL.md` path is a first-class answer**, and it is the right one whenever
    verification is *both* an automated suite *and* a browser journey: the skill runs the
    suite, then drives the journeys, and `strategy` points at it. Offer this explicitly —
    the enum values are single-mode, and most real projects are not.
  - `test-suite` / `smoke-cli` — only when there is genuinely no surface to drive.
- **The deploy story — ask for it, and don't let it default to nothing.** A browser gate is
  worthless without a running instance to point it at:
  - `staging.url` — the first-level test environment the gate drives. If none exists yet,
    say so plainly rather than skipping past it: the gate degrades to whatever the loop can
    start for itself each firing, paying a cold start every time and persisting nothing
    between runs. Standing one up is worth doing *before* first launch.
  - `staging.deploy_recipe` — how a merge reaches that environment, as verbatim prose or a
    Delegated SKILL.md path. Capture what invalidates it too: a rebuild that wipes host
    patches, a checkout that must be drift-checked first.
  - `staging.deploy_host_ssh` / `staging.checkout_path` — when a separate box serves it.
- optional `domains`, `aliases`, `work_source`, `generation_skills`

The typed schema and every validation rule are frozen in `skills/_shared/SCHEMA.md` — do not
invent fields.

## Step 2 — Write the config markdown

Write the interview answers into the config home (`$AGENTFLOW_CONFIG` or `~/.agentflow/config/`):

- `environment.md` — copy `templates/environment.md`, fill the fenced YAML block, keep the
  prose notes.
- `projects/<name>.md` — copy `templates/projects.example.md`, fill it; **filename stem ==
  `name`** (the resolver hard-fails otherwise).

Each file is a typed YAML block **plus** human prose. The resolver reads only the FIRST fenced
`yaml` block; prose after it is ignored.

A config home other than `~/.agentflow/config/` (chosen by `--config-home` or a shell-level
`$AGENTFLOW_CONFIG`) is persisted for you: step 9 writes `env.AGENTFLOW_CONFIG` into the same
settings file as the SessionStart hook, so a lane reads that home without anything set in its
shell. The default home writes no `env` key. If the settings file already carries a DIFFERENT
`AGENTFLOW_CONFIG`, provision refuses at step 1 rather than overwrite it — re-run with that home,
or remove the entry. The closing output says when it wrote the value.

## Step 3 — Write secrets ONE-WAY

The config markdown holds only env-var **NAMES** (e.g. `notify.url_env: "NTFY_URL"`). Write the
true values ONE-WAY into the machine's secret store — **single source of truth per fact, no
dual-write, secrets NEVER in markdown**:

- Env vars the harness injects → `settings.local.json` `"env"` block (e.g. `NTFY_URL`,
  `NTFY_TOPIC`, `GITEA_URL`, tokens).
- Shell/tooling env → `.env` if the project uses one.

Write each fact in exactly ONE place **per consumer**: the `"env"` block serves the fleet's
sessions, and the login profile serves the shell (the ntfy names only, see below). Do not
"fix" that pair into one copy — dropping either brings back the doctor FAIL below. The resolver looks the NAME up in `os.environ` at resolve
time; a missing named var is a loud hard-fail, never a silent default.

**The `"env"` block does not reach this install, or a plain terminal.** `settings.local.json`
is loaded only by a Claude Code session rooted at the launch directory (home). This session is
rooted at the suite checkout, so neither it nor any shell the operator opens sees those values,
and with `notify.kind: ntfy` both provision step 3 (`_do_secrets`) and the resolver refuse a
named var absent from `os.environ`. So, when the operator said yes to ntfy, do two more things:

- **Pass the vars to every Step 4–6 command** — each Bash call is a fresh shell, so set them in
  the same call, e.g. `NTFY_URL='<url>' NTFY_TOPIC='<topic>' python install/provision.py`. On
  PowerShell, which cannot parse a `VAR=value command` prefix, set `$env:NTFY_URL='<url>';
  $env:NTFY_TOPIC='<topic>'` first in the same call.
- **Persist them in the login profile at Step 7**, next to the venv activation line, so the
  operator's own terminal — where `docs/INSTALL.md` §9 runs `doctor` — has them. That is a
  second copy of the value, and a necessary one: the `"env"` block serves the fleet's sessions,
  the profile serves the shell, and neither reaches the other.

## Step 4 — Provision runtimes

Preview, then apply:

**`python` here means the interpreter the box already has, not the suite venv — that only
becomes the default at Step 7.** Check which name your box answers to with `python --version`
before you start: Debian/Ubuntu ship the interpreter as `python3`, and plain `python` exists
there only if `python-is-python3` (or an activated venv) provides it — so read every `python`
before Step 7 as `python3` on Linux. The commands stay written as `python` because on Windows
that is the working name and `python3` is not.

```bash
python install/provision.py --dry-run     # ordered plan; mutates nothing
python install/provision.py               # venv+PyYAML, pip install -e _shared,
                                          # autodoc npm ci (autodoc only), skill deploy,
                                          # bootstrap.py, then scaffold the data_root subtree

# if the operator declined the auto-allow hooks in Step 1, add the flag to BOTH commands:
python install/provision.py --dry-run --no-auto-allow
python install/provision.py --no-auto-allow   # step 8 SKIPPED; everything else unchanged
```

`--no-auto-allow` removes no hook a previous run wrote; `docs/INSTALL.md` section 13 has the
manual removal.

Step 12, the missed-wake watchdog, is **off by default** and the interview does not ask about
it: add `--wake-watch` to both commands only if the operator asks for it (`docs/INSTALL.md`
step 7 says what it is). A run without the flag removes nothing a previous run registered.

> **The second command does not need an interpreter that already has PyYAML.** Step 4
> installs PyYAML into the suite venv rather than into the interpreter running the script, and
> five later steps import the resolver, so a new machine's interpreter cannot run them. Step 4
> therefore ends by asking whether the interpreter running it can import the dependencies, and
> when it cannot, hands the rest of the run over to the venv it has just built. One line of
> output names the handover, every step from 5 on continues in the venv, and the child's exit
> code is the install's. An interpreter that already has PyYAML spawns nothing. Limb 2 of
> `harness/fresh-clone-install-drill/` is the regression guard: it requires the PyYAML-less run
> to complete.
>
> **Step 2 refuses to pre-create a scraped `data_root` or `worktree_root` that is relative, or
> whose only existing ancestor is the drive root,** and leaves the loud failure to the step-10
> resolver. It still pre-creates a well-formed path under an existing directory before the
> resolver runs, by design, because a fresh `data_root` does not exist yet
> (`_unsafe_to_precreate` in `install/provision.py`; its tests are in
> `install/test_provision_fresh_machine.py`).

`provision.py` honors `CLAUDE_SETTINGS_FILE`; pass `--settings-file` / `--config-home` /
`--suite-root` if you are not using the defaults. Its final step scaffolds the consolidated
data layout — `<data_root>/projects/` plus the eight directories
`design/{specs,plans,use-cases,suggestions}/`, `status/` and `wiki/pages{,/done,/archived}/` for
every configured project (queue/ is retired — per-agent state lives at
`status/<agent>-state.md`; `autodoc/` is NOT scaffolded, and `/autodoc-init` does not create it either: it exits when no `autodoc_root` resolves), seeds each `status/registry.md` from `templates/registry.md`
(the fleet coordination surface, `docs/REGISTRY.md`), and seeds each `use-cases/` folder with `registry.jsonl` (empty),
`.counter` (`0`), and a `domains.md` tree stub for the use-case traceability spine (idempotent
write-if-absent — an already-allocated counter or registry is never clobbered; see
`docs/DATA-LAYOUT.md` and `skills/_shared/SCHEMA.md` §1). The skills and the disk epic-survey
read exactly this single-root subtree. Node tree-sitter is provisioned **only** when
autodoc is enabled (`autodoc_root` set, or `--autodoc`) — the pipeline itself needs no Node
(see `manifest.md`).

`provision.py` step 7 **deploys the suite's skills, command wrappers and one hook script** into
the Claude config dir (`--claude-root`, default `$CLAUDE_CONFIG_DIR` or `~/.claude`) so the fleet
is launchable — after install, all seven loop commands (`/lead-dev`, `/jr-dev-1`, `/jr-dev-2`,
`/jr-dev-3`, `/auditor`, `/steward`, `/dev-manager`) and the six supporting ones (`/report`,
`/graph-query`, `/wiki-save`, `/autodoc-init`, `/autodoc-update`, `/uc-touchpoints`) resolve
in a fresh Claude Code session. Junction (directories) or copy (files) on Windows, symlink on
Unix; the `skills/_shared` DIRECTORY
never deploys (it is the pip package) though `skills/_shared/scripts/plan-lint.sh` does, as an
individual file at the stable path `<claude_root>/scripts/plan-lint.sh`, so the host copy is
never unmanaged — provision registers no hook for it, so nothing runs it unless the
operator adds one;
`skills/_vendored` deploys too (skills reference it by relative sibling path). A pre-existing skill/command **not** owned by agentflow refuses loudly and is
never overwritten; `--force` refreshes agentflow-owned entries that were locally modified.
The run is recorded in `<claude_root>/.agentflow-deploy.json` (source → target + hash per
entry). Full policy: `manifest.md` §"Skill deployment".

**If Step 1 left `verification.strategy` unresolved, this is where you pick it up:** the
`agentflow` package is in the venv now, so either `project_probe` command in Step 1 works —
run it, show the person its evidence block, and correct `projects/<name>.md` before Step 6
checks it.

**This is also where the vault question is asked** (Step 1 says why it waits): run the
venv-interpreter `find_vault_candidates` command from Step 1, offer what it found, and write the
`vault` block — or `vault: null` for a no — into `environment.md` before Step 6.

## Step 5 — Install the SessionStart hook

`provision.py` step 9 registers `hooks/sessionstart-inject-config.py` in the settings file. This
is the enforcement point that replaces every "read config at step 0" instruction: config is
resolved once at session open, injected to STDOUT on success, and a `ConfigError` hard-fails the
session loudly. (See `hooks/hooks-manifest.md`.)

## Step 6 — Presence-check + hard-fail

`provision.py` step 10 runs the resolver over `environment.md` and every `projects/<name>.md`,
which presence-checks all delegated SKILL.md / script paths and hard-fails on any missing
required config. Confirm it exits clean:

```bash
# the venv interpreter by path — bare `python` has no agentflow package until Step 7,
# and no AGENTFLOW_CONFIG prefix is needed: the hook already defaults to ~/.agentflow/config
<suite_root>/.venv/bin/python hooks/sessionstart-inject-config.py      # exit 0 + resolved block
# Windows: <suite_root>\.venv\Scripts\python.exe hooks\sessionstart-inject-config.py
```

(Set `AGENTFLOW_CONFIG` only if your config home is somewhere else — and set it as a real
environment variable, not a `VAR=value command` prefix, which PowerShell cannot parse.)

If it exits non-zero, read the field / file / remediation on STDERR and fix the config —
**do not proceed with a broken config.**

Then run the diagnostic, and **show the operator its output rather than summarising it** — this
is the command they will run every time something looks wrong, so the first time they see it
should be a run you are standing next to and can read out line by line:

```bash
<suite_root>/.venv/bin/python -m agentflow.doctor --project <name>
# Windows: <suite_root>\.venv\Scripts\python.exe -m agentflow.doctor --project <name>
```

It prints one line per check — environment, each path, the project profile, the checkout and its base branch, the
publish split, the registry, the three document globs, autodoc, vault — and a closing verdict.
Four statuses, and two of them are healthy: `ok`, and `info` for something switched off on
purpose (no publish target, no autodoc root, no vault) or not written yet (an empty document
bucket). `warn` means a value resolved but not as written — a clamped dial, say, or an autodoc root whose
runtimes step 6 never installed — and still
exits 0; only `fail` exits 1. Walk them through the five `info` lines a fresh install shows —
publish, `glob:spec`, `glob:plan`, autodoc, vault — because all five look like gaps and none is
one. `glob:spec` and `glob:plan` say `info` only because their scaffolded bucket exists and is
still empty; they turn `ok` once the first spec and plan are written, and they `fail` only when
the bucket directory itself is missing — a layout that moved. `docs/INSTALL.md` §9 carries a
sample output annotated.

## Step 7 — Put the suite venv on the session's PATH (one-time) — and keep the product's own

The fleet skills call bare `python -m agentflow.registry` (and other `agentflow.*` modules)
with the *session's* `python`, so the suite venv must be first on PATH in every Claude Code
session. **This displaces whatever `python` the box had** — fine on a dedicated box, a trap on
a daily driver that also builds Python products: the product's test suite, run with bare
`python`, now imports from the suite venv (PyYAML only) and either fails or goes green over a
broken app. So do BOTH: wire the suite venv into the profile, AND set `canonical_repo.python`
in every Python product's profile to the product's own interpreter — the builders run product
commands through that path, never bare `python`. Wire the profile **once**, not per launch:

- **Unix:** add `source <suite_root>/.venv/bin/activate` to `~/.bashrc` / `~/.zshrc`.
- **Windows:** add `& <suite_root>/.venv/Scripts/Activate.ps1` to the PowerShell `$PROFILE`.
- **If `notify.kind` is `ntfy`,** add the two named vars beside that line (Step 3 says why):
  `export NTFY_URL='<url>'` and `export NTFY_TOPIC='<topic>'` on Unix, or
  `$env:NTFY_URL='<url>'` and `$env:NTFY_TOPIC='<topic>'` in `$PROFILE`. Use the names
  `notify.url_env` / `notify.topic_env` actually declare. The topic is the only access control
  on an unauthenticated ntfy server, so if the profile is tracked in a dotfiles repo or synced
  (OneDrive backs up `Documents`, where `$PROFILE` lives), put the two lines in an untracked
  file instead and source that from the profile.

Then, in a **fresh** shell, confirm the write path resolves:

```bash
python -m agentflow.registry validate --project <name>   # exit 0 + "registry valid"
```

If that errors with `ModuleNotFoundError`, the session isn't using the suite venv — the profile
line didn't take. On a machine where another tool already owns the default `python` (a daily
driver), run agentflow under its own user/box rather than displacing that python.

---

# Part 2 — Using agentflow

Once the presence-check and `validate` are green, **orient the person on operating the fleet** —
they installed a system; now show them how to drive it. Keep to the essentials below.

## Launch the fleet — one slash command per loop, once
Each loop launches **once** in its own Claude Code session and self-continues via
`ScheduleWakeup`; you do not re-open them.

**Every one of them launches from the machine's launch directory — the operator's home
directory, never the agentflow checkout, never a project repo and never a per-epic
worktree.** It is home because that is where provision wrote the settings
(`Path.home() / ".claude" / "settings.local.json"`), the *project* settings file for a
session rooted at home and for no other; `docs/INSTALL.md` §10 says the same. The launch directory is what selects the
session's `CLAUDE.md` chain and the memory the fleet has accumulated, so a lane started
somewhere else comes up without them and reads as stale rather than as broken. Which
project a lane works on is not the folder it was opened in; it is `--project` (below).
`cd` there before each launch and `pwd` to confirm.

**The six autonomous loops (everything but dev-manager) need `--dangerously-skip-permissions` to run unattended.
`dev-manager` doesn't require it.**

```bash
claude --dangerously-skip-permissions "/lead-dev"     # same for jr-dev-1, jr-dev-2, jr-dev-3, auditor, steward
claude "/dev-manager"                                 # your seat - normal permissions
```

With more than one `projects/<name>.md` profile, name the project **on the slash command** —
`claude --dangerously-skip-permissions "/lead-dev --project agentflow"`. It beats the session's
injected default and rides every self-wake. See *Add another project later*, below.

This is not a convenience. A loop self-continues while nobody is watching, and the first
command outside the auto-allow matchers stops it at an approval prompt with no one to answer
— it does not fail, it *hangs*, and a hung loop is indistinguishable from a working one
until you look. Half-autonomy is worse than either extreme: you get the exposure of an
unattended agent and none of the unattended operation.

So the containment is **the box, not the prompt**. Run the fleet on a machine or user
account holding nothing you cannot rebuild, with no credentials that reach further than the
project it works on. Read `https://code.claude.com/docs/en/security` before you decide the
box qualifies. If you are not willing to say that about the machine, run without the flag and
accept that you are the approval - answering prompts is then part of your job, not a
degraded mode.

`dev-manager` is left out of that for a reason. It exists to be driven by a human, so the
human is already the approval — the flag buys it little, and leaving it off keeps a checkpoint
in the one lane where someone is actually watching. Nothing stops you from launching it with
the flag; you would just be giving up that checkpoint for convenience.

**One-time acceptance:** the first launch with the flag shows a bypass-mode warning and waits
for an answer. Answer it once, interactively, *before* you rely on any auto-start — an
unattended restart cannot answer it, and the acceptance persists afterwards.

Launch, in order:

1. **`/dev-manager` — your seat.** The ONE session you interact with: it answers the fleet's
   questions, promotes specs to `approved-for-autonomous` (that promotion *is* your standing
   approval), assigns blockers, and serves the board. **Live here.** **It has no unattended
   mode** — there is no `--unattended` flag, and the liveness sweep, the cull and the
   malformed-row repair are all the steward's — so this seat does not
   self-wake and schedules nothing: it exists only while the window is open. Tell the operator
   that plainly, because the opposite belief is the expensive one: somebody who thinks this seat
   pumps overnight closes the laptop on a fleet whose questions nobody is answering. The steward
   is what runs between visits.
2. **`/lead-dev`** — the build hub: publishes work into the Queue lanes and builds the lead lane.
3. **`/jr-dev-1`, `/jr-dev-2`, `/jr-dev-3`** — optional junior builders, one per lane the
   `parallel_builders` dial opens: with `enabled: true`, `count: 1` launches `/jr-dev-1`
   alone, `count: 2` launches the first two, and `count: 3` launches all three; `count: 0` (or
   `enabled: false`) launches none. They claim disjoint work from their own lanes, never
   selecting their own. `jr-dev-3` is an interim lane — a hand-copy of `jr-dev-2` that
   `lead-dev-as-foreman-and-n-junior-lanes` replaces with a count-driven set — so say so rather
   than presenting it as permanent furniture.
4. **`/auditor`** — post-build intent feedback: audits done epics against their use cases and
   files drafted gap specs.
5. **`/steward`** — maintenance: sweeps what time (not work) breaks — stale frontmatter, orphaned
   locks, deploy/schema drift, silent failures, dead issues. Fixes only the evidence-checkable;
   backlogs the structural. Runs fine with no builder active.

All seven coordinate through **one file per project** — `status/registry.md` — writing only the
rows they own, through the mediated CLI. You rarely touch it by hand.

## How work flows — idea → merged code
**refine** (functional design → spec) → **solution** (technical plan) → **orchestrator** (runs
the plan as waves of parallel subagents with per-task review, regression auto-fix, and a status
board → built, tested, reviewed, merged). `project` / `choose-next` / `backlog` drive what gets
picked up. **You steer the *what* (approve specs); the fleet handles the *how*.**

## Your job as the human — small by design
- **Answer questions.** Any loop can raise a `## Questions` row (`halted` > `waiting` >
  `advisory`, always with a `default:`); dev-manager pumps them and surfaces only what its
  delegated authority can't decide. Ntfy pings you — **notification-only, never a reply channel.**
- **Promote specs.** Moving a spec `drafted → approved-for-autonomous` in the dev-manager session
  is the single approval — no per-epic dispatch confirm after that. The `## Directives` section
  is your standing-instruction veto.
- That's it. The other six loops run unattended.

## Add another project later — and how to pick the active one

With two or more `projects/<name>.md` profiles, every session needs to know which project it
serves. **Say it on the slash command — that is the documented way:**

```
claude --dangerously-skip-permissions "/lead-dev --project agentflow"
claude "/dev-manager --project agentflow"
```

Every loop command takes `--project <name>`, and the name **beats** whatever the SessionStart
banner injected — so one box runs several fleets without touching any settings file. The skill
strips `--project <name>` out of its arguments first and treats the remainder as its work
target, so `"/lead-dev --project agentflow app#123"` still means "build `app#123`, on
`agentflow`". Each self-waking loop carries the same argument into its own `ScheduleWakeup`
continuation (dev-manager schedules none: it runs only while a human has it open), so **every
wake after the launch stays on the project you named** — that is the whole point;
a launch that lands right and drifts back to the default on wake 1 is worse than not having
the argument at all.

Nothing in the install writes project selection for you — no `AGENTFLOW_PROJECT` in a settings
`env` block, no per-project settings file. `provision.py` installs runtimes and hooks; picking
the project is a launch-time choice, made on the command line.

**Do not tell people to export a shell variable.** Claude Code's settings `env` **overrides the
process environment**, so `AGENTFLOW_PROJECT=other claude ...` is silently ignored and the
session quietly resolves the default — the wrong-project failure that looks exactly like a
right one. That override is precisely *why* the argument exists: it travels on the prompt, not
in the environment, so nothing can shadow it.

**For people who script their launches — still the slash command.** With two or more projects
configured and no project resolved, the hook prints `[project] (no project)`, exits 0, and the
session looks healthy while every skill runs unprojected. A scripted launch closes that the same
way a typed one does: start plain `claude` from the launch directory and put the project on the
slash command, `/<loop> --project <name>`:

```
claude --dangerously-skip-permissions "/lead-dev --project other"
```

**Do not script it with `--settings`.** A `--settings` file's `env` block replaces
`settings.local.json`'s `env` instead of merging with it, so every env var this install
collected disappears and the lane fails at its first step, before it can write the registry row
that would have said so.

**Confirm which project a session actually resolved** before trusting it. The SessionStart
banner's `[project]` line reports the *injected* default, so on an argument-launched session it
can legitimately name a different project than the one the loop is working. A loop launched
that way makes the split visible on purpose — it appends
`PROJECT-OVERRIDE injected=<injected> active=<name>` to its first Ntfy of the wake and carries
it in its `## Agents` row `phase`, so a mis-launched lane is readable from the registry or the
phone instead of being discovered in a merged PR. To check the argument's project yourself,
print its resolved block with the same resolver and the same hard-fail:

```
python -m agentflow.config show --project <name>
```

### Adding the profile
Two steps, and neither is a slash command. Copy `templates/projects.example.md` to
`<config_home>/projects/<name>.md` (**filename stem == `name`**) and fill it the way Step 2
did, then re-run `python install/provision.py` — **but check the auto-allow hooks first**,
because the Step 1 answer was not saved and a re-run without the flag writes them back. Count
the PreToolUse hooks whose `statusMessage` begins `auto-allow: ` with this probe, which prints
only a number:

```
python -c "import json,os; p=os.environ.get('CLAUDE_SETTINGS_FILE') or os.path.expanduser('~/.claude/settings.local.json'); s=json.load(open(p,encoding='utf-8')); print(sum(1 for b in s.get('hooks',{}).get('PreToolUse',[]) for h in b.get('hooks',[]) if str(h.get('statusMessage','')).startswith('auto-allow: ')))"
```

Never print or Read the settings file itself; its env block holds tokens. If the count is 0,
the operator declined the hooks (or removed them): pass `--no-auto-allow` on the re-run and
tell the operator that is why. The re-run's scaffold step walks every
`projects/*.md` in the config home and creates the missing
`<data_root>/projects/<name>/{design/{specs,plans,use-cases,suggestions},status,wiki/pages{,/done,/archived}}`
plus a seeded `status/registry.md`, leaving the existing projects alone. To be walked through it instead,
open the suite checkout in Claude Code and say: *Read install/SKILL.md and add a project
profile for `<name>`.* (The `project` skill does **not** do this — it only asks which
already-installed profile a spec belongs to.) One registry per project; the fleet works them
in parallel.

## Turn a repo into a living code-wiki (autodoc)
`/autodoc-init` builds the two-tier knowledge graph + rendered wiki; `/autodoc-update` refreshes
it incrementally. `graph-query "<question>"` answers from the graph with a cited, provenance-tagged
traversal — exact AST facts, agent-written concepts, and hypothesized links are always
distinguishable. Prerequisites on a machine installed with autodoc off: Node LTS (with npm), an
`autodoc_root` naming an existing directory, a re-run of `python install/provision.py --autodoc`
(step 6 installs the runtimes; run the auto-allow count probe from *Add another project later*
first and add `--no-auto-allow` when it prints 0), and the `Workflow` session tool — both skills' mapping phase runs through it, with no
single-agent fallback. `doctor`'s autodoc line warns when a root resolves without the runtimes.

## When something looks off
- **`python -m agentflow.doctor --project <name>` first.** It reports the whole resolved surface
  and is built never to raise, so it answers when nothing else will. Read the `fail` lines from
  the top; each carries its own remediation and the first usually explains the rest.
- `python -m agentflow.registry validate --project <name>` — is the registry schema-valid?
  (loops run it at wake, fail-closed; re-run it any time.)
- A loop gone quiet on an empty lane is **broken, not by design.** Lanes never halt on empty
  input — an empty lane schedules its next check and keeps checking — so silence there means the
  process died or its wake was never scheduled. Relaunch it. (It picks the work up by itself once
  its lane is fed.)
- Config problems **hard-fail loudly at session open** (the SessionStart hook); read STDERR, fix
  the named field, reopen the session.
