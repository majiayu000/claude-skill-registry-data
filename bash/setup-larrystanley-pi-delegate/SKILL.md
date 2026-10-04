---
description: First-run guided setup for pi-delegate — checks pi and its provider, explains the discipline modes and asks which to use, offers to fix detected problems, offers a verification dispatch, and points to what's next
disable-model-invocation: true
---

# pi-delegate setup

This is a guided walkthrough for the person setting up pi-delegate, not a script to run
unattended. Work through the steps below in order. Report each check's result in plain
language before moving on. Wherever a step says **ask**, stop and wait for the user's answer
— do not barrel through to the next step on your own judgment.

## 1. Detect

Check whether `pi` is on PATH:

```bash
command -v pi
```

If this prints nothing, `pi` is not installed and nothing else in this plugin can work yet.
Tell the user:

- Install it with `npm install -g @earendil-works/pi-coding-agent`
  (https://www.npmjs.com/package/@earendil-works/pi-coding-agent)
- pi-delegate also needs Node ≥ 22.

Then **stop here** — do not continue to step 2 until `command -v pi` finds it.

If `pi` is found, check its version and run the environment check:

```bash
pi --version
node "${CLAUDE_PLUGIN_ROOT}/bin/pi-doctor" --check
```

Read the `effective` block in the JSON output — that's *who a dispatch will actually reach*.
Report it to the user plainly: which provider and model dispatches will use, and where that
came from (`source` is either `pi-delegate config.json` or `pi settings.json`).

- **This plugin emits no `--provider` / `--model` flags by default.** A dispatch simply
  inherits whatever `pi` itself is already pointed at — anthropic, openai, a local
  OpenAI-compatible server. There is no requirement to run a local inference server;
  whatever the user already uses with `pi` interactively is what dispatches will use too.
- If `effective.provider` and `effective.model` are both empty, pi has no
  `defaultProvider` / `defaultModel` set in `~/.pi/agent/settings.json`, and pi-delegate has
  no `~/.claude/pi-delegate/config.json` pinning one either. In that case dispatches will
  land on whatever pi's own resolver picks (the first model with a usable API key) — tell
  the user this is usually not what they want, and that configuring a provider for `pi`
  itself is outside this plugin's scope: run `pi` interactively once and complete its own
  provider setup, or set `defaultProvider` / `defaultModel` directly in
  `~/.pi/agent/settings.json`. Then re-run the check above before continuing.
- Note the `problems` array (if any) but don't act on it yet — that's step 3.

## 2. Discipline mode — ask which one

Explain the three modes, then **ask which one the user wants for this project** before doing
anything:

- **`off`** — pi-delegate's tools are available, nothing is enforced. Right for a project
  where delegating to pi isn't wanted at all.
- **`soft`** (the default) — you get a reminder when you edit existing product source by
  hand, but nothing is blocked.
- **`strict`** — a `PreToolUse` hook actually **denies** those edits and tells you to
  delegate instead. Worth explaining *why* this exists: with a written rule in place
  telling the model to delegate, roughly 80% of the characters that got committed were
  still typed by the main model by hand. `strict` is what made that stop.
  Be honest about its limit too: the hook only matches the `Write` and `Edit`
  tools, so the same edit made through `Bash` (`sed -i`, a heredoc, `python - <<EOF`, …)
  is never intercepted — it's a discipline rail against your own habit, not a security
  boundary.

The mode is stored against the project root and applied by the edited file's project
root, so it follows the project rather than your session's working directory.

If the user picks `strict`, do NOT just run the command — `strict` needs to know what to
protect, and its built-in fallback only fits a `src/` directory of TS/JS/Svelte/Python
files. Follow `/pi-delegate:mode`'s "Setting `strict`: survey the project first" section:
survey the layout, propose `protect` / `allow` globs with reasons, wait for the user to
approve them, and only then write the policy.

"Existing product code" means a file that already exists under the project's `src/`;
`tasks/`, `scripts/`, `docs/`, markdown, config files, and brand-new files are always
allowed through regardless of mode.

Once the user answers, apply it (this also confirms the choice was actually recorded, even
if they picked the default):

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/pi-mode" <mode>
```

Replace `<mode>` with `off`, `soft`, or `strict`. This is exactly what `/pi-delegate:mode
<mode>` does, and it can be changed later the same way.

## 3. Offer to fix what is fixable

Look at the `problems` array from step 1's `--check` output.

- If it's empty, say so and move on to step 4.
- Otherwise, explain each problem's real-world consequence in one line before asking
  anything:
  - **`reasoning-missing` / `compat-missing`** — this only shows up for a **local
    OpenAI-compatible server** (e.g. a self-hosted omlx, LM Studio, llama.cpp, or vLLM
    endpoint). The model is missing `reasoning: true` or the
    `compat.chatTemplateKwargs.enable_thinking` binding in `~/.pi/agent/models.json`, so
    `--thinking off` **silently has no effect** — the model keeps "thinking" instead of
    calling tools, and a dispatch can burn its whole timeout without ever writing anything.
    This class **can** be fixed automatically.
  - **`drafter-selected`** — the model a dispatch would actually reach looks like a
    speculative-decoding draft/assistant model (a co-pilot, not a target). Calling it
    directly returns HTTP 500. This is **never auto-fixed** — which model to point at is the
    user's decision, not something to guess. Point them at switching `defaultModel` (or
    pi-delegate's own `model` override), or adjusting `drafter_patterns` in
    `~/.claude/pi-delegate/config.json` if it's a false positive.

For any `reasoning-missing` / `compat-missing` problems, **ask before fixing**. If the user
agrees, run:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/pi-doctor" --fix
```

This backs up `~/.pi/agent/models.json` to `~/.pi/agent/models.json.pi-delegate.bak` before
writing, and only ever adds the thinking binding to a model that is already registered and
confirmed to be a local chat-template endpoint — it never invents a provider or a model.
Report the result (`fixed` / `remaining` in the output) back to the user.

Never run `--fix` without asking first, and never fix a `drafter-selected` problem — there is
nothing to fix, only a model choice for the user to make.

## 4. Offer a verification dispatch

**Ask first** — a real dispatch calls the user's actual provider, which costs real time and
(for a paid provider) real tokens. If they'd rather skip it, go straight to step 5.

If they want to try it, create a scratch task in a temp directory:

```bash
DIR=$(mktemp -d) && cat > "$DIR/TASK.md" <<'EOF'
Create a file named hello.txt in the current directory containing exactly the text:
pi-delegate setup verified
Do not create, read, or modify any other file.
EOF
echo "$DIR"
```

Then call the `pi_dispatch` tool yourself with `task_file` set to `<DIR>/TASK.md`, `cwd` set
to `<DIR>`, and `mode=sync` — leave `provider` / `model` unset so it exercises the exact same
resolution path a real dispatch would use. `sync` is deliberate here even though async is
the normal default: this one call exists so the user watches it finish, and there is nothing
else to get on with while it runs. Report the verdict plainly: status, files written,
duration. To show the user it's real, not just claimed:

```bash
cat "$DIR/hello.txt"
```

If the dispatch times out or never writes, that is itself informative — it's usually the
`reasoning-missing` symptom from step 3 (a local model stuck "thinking" instead of acting).
Point back at step 3's fix rather than guessing at a new cause.

## 5. Offer the status line indicator

**Ask first.** This one writes to `~/.claude/settings.json`, which is the user's own global
config and probably already has a status line in it.

Explain what it is: one row per running pi dispatch at the bottom of the screen, each showing
how long that dispatch has been going and which model it is on. It disappears entirely when
nothing is running. The rows are this session's own; another Claude Code window's dispatches
never appear in them.

Two things to say before they answer, because neither is visible from a screenshot:

- Claude Code allows exactly **one** `statusLine`, and a plugin cannot ship its own. If they
  already have one (claude-powerline, ccstatusline, a personal script), this composes with it
  rather than replacing it — their line runs untouched and the pi row goes underneath.
- It needs `refreshInterval`, which reruns **their** status line too, once a second for as long
  as Claude Code is open. On a status line that shells out to `git`, that is a real if small
  background cost — roughly 10% of one core for a status line taking ~100ms.

If they want it, invoke `/pi-delegate:statusline` and follow it — it probes their existing
command by actually running it, shows before and after, and backs up `settings.json` before
writing. Do not shortcut it from here — that skill assumes nothing about a setup it has
not looked at.

If they decline, say it can be added any time with `/pi-delegate:statusline`, and move on.

## 6. Close with what to do next

Tell the user setup is done, and summarize where things stand: the mode they picked, and
what a dispatch will resolve to. Then point at:

- The seven MCP tools this plugin adds: `pi_dispatch`, `pi_status`, `pi_steer`, `pi_abort`,
  `pi_result`, `pi_transcript`, `pi_stats` — see `skills/delegating-to-pi/SKILL.md` (loaded
  automatically when relevant) for how and when to use each one.
- `/pi-delegate:mode <mode>` — change the discipline mode later, any time.
- `/pi-delegate:probe` — get a one-time bypass in `strict` mode to make a single hand-edit
  (a probe), before writing the verified recipe into a task book for pi.
- `/pi-delegate:statusline` — add (or later remove) the live dispatch indicator in the status line.
- `/pi-delegate:doctor` — re-run this environment check any time something seems off (after
  a `pi` upgrade, after editing `~/.pi/agent/models.json` by hand, after switching
  providers).
