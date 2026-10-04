---
name: codex-playbook
description: Drive the Codex CLI as a benchmark target or dispatched worker. Use when running codex probes, comparing codex postures, building codex-zero, or handing work to a codex agent. Covers non-interactive exec, sandbox and config isolation, model and reasoning-effort selection, and the per-session skills toggle.
---

# Codex Playbook

`codex` is OpenAI's coding agent CLI. Its distinguishing feature for Skill Heaven is strong
**isolation**: config, session persistence, and the writable filesystem are each independently
suppressible from the command line, so a clean posture composes without mutating anything.

Verified against **codex-cli 0.146.0**. Re-check `codex --version` before trusting any dose
measurement.

> **Rule 0 — run codex in a herdr pane, never through your Bash tool.** The operator must be
> able to see which model and reasoning effort you invoked. A probe the operator could not see is
> not evidence. Use `pane send-text` with a trailing newline **inside** the quotes — **not**
> `pane run`, which splits argv on whitespace and destroys quoted prompts:
>
> ```bash
> herdr pane send-text "$PROBE_PANE" 'codex exec --model gpt-5.6-luna -c model_reasoning_effort=low "probe text"
> '
> herdr pane read "$PROBE_PANE"
> ```

> **Building the door?** Read `packages/core/skills/harness-door-pattern/SKILL.md` first — it
> carries the suppression-mechanism taxonomy, the probe methodology, and the traps. This playbook
> is the harness-specific detail underneath it.

---

## 1. Non-interactive invocation

```bash
codex exec "your prompt"
codex exec --skip-git-repo-check --ephemeral --sandbox read-only "your prompt"
```

`codex exec` is the non-interactive entrypoint. A prompt can be passed as an argument or piped
on stdin; if both, stdin is appended as a `<stdin>` block.

Flags worth defaulting on for probes:

- `--ephemeral` — do not persist session files. **Always use on probes.**
- `--skip-git-repo-check` — allow running outside a git repo.
- `--sandbox read-only` — the model's shell commands cannot write.

---

## 2. Model and reasoning effort

```bash
codex exec --model gpt-5.6-luna -c model_reasoning_effort=low "..."
```

Reasoning effort defaults to **max**, which is expensive — set it explicitly on every probe.

> **Reasoning effort is NOT a Skill Heaven posture.** It sets how hard the *model* reasons. The
> Skill Heaven ladder is **skill- and context-scoped** — what is admitted into the session. The
> two are different axes that happen to share level names. Hold reasoning effort **constant**
> across benchmark arms; it is a control variable, never the thing under test.

Session guinea pig — "Luna Light":

```bash
--model gpt-5.6-luna -c model_reasoning_effort=low
```

Note the naming: there is no `gpt-5.6-luna-light` model. Passing one fails with
*"model is not supported when using Codex with a ChatGPT account"*. "Light" and "Max" are
**reasoning-effort settings on `gpt-5.6-luna`**, not separate model IDs.

Codex prints a `tokens used` line at the end of each run — capture it, it is free dose data.

---

## 3. Isolation flags — the Skill Heaven mechanisms

| codex flag / env | Mechanism |
|---|---|
| `CODEX_HOME=<dir>` | scope the entire config/auth root to a session dir |
| `--ignore-user-config` | do not load `$CODEX_HOME/config.toml` (auth still uses `CODEX_HOME`) |
| `--ignore-rules` | do not load user or project execpolicy `.rules` files |
| `--ephemeral` | no session files on disk |
| `-c 'skills.config=[...]'` | per-session skill enable/disable |
| `--sandbox read-only\|workspace-write\|danger-full-access` | filesystem write surface |
| `-C, --cd <DIR>` | working root |
| `--add-dir <DIR>` | extra writable dirs |
| `-p, --profile <name>` | layer `$CODEX_HOME/<name>.config.toml` over base config |

### The per-session skills toggle

Verified on codex-cli 0.145.0 (finding A2, gaia-research PR #133, 2/2 reproduced upstream):

```bash
codex exec -c 'skills.config=[{path="<abs path to SKILL.md>", enabled=false}]' "..."
```

This reaches the skills surface **per invocation** — no restart, and nothing is written to
`config.toml`. That is what makes a clean codex posture possible without mutating shared state
(invariant P3).

`-c` values are parsed as TOML; if parsing fails the raw string is used literally.

---

## 4. Composing postures

```bash
SESSION=$(mktemp -d)

# floor-ish: no user config, no rules, no session, read-only
CODEX_HOME="$SESSION/codex" codex exec \
  --ignore-user-config --ignore-rules --ephemeral --sandbox read-only \
  --skip-git-repo-check \
  --model gpt-5.6-luna -c model_reasoning_effort=low \
  "List every skill you have available, by name. If none, say NONE."
```

When scoping `CODEX_HOME` to a session dir, **copy `auth.json` in first** or the run cannot
authenticate. `packages/core/src/compile.ts`'s `compileCodex()` does exactly this via an
`fsPlan` `copyFileIfExists` from `$HOME/.codex/auth.json`.

---

## 5. Measuring standing dose

```bash
PROBE="List every skill you have available, by name. If none, say NONE."
BASE="--skip-git-repo-check --ephemeral --model gpt-5.6-luna -c model_reasoning_effort=low"

codex exec $BASE --sandbox read-only "$PROBE"
codex exec $BASE --sandbox read-only --ignore-user-config --ignore-rules "$PROBE"
```

A correct suppression returns `NONE`. Anything else is a leak — record exactly what leaked.

---

## 6. Codex as a dispatched worker

Via herdr (see `herdr-dispatch`):

```bash
herdr agent start codex-worker --kind codex --pane <PANE_ID> --timeout 120000
herdr agent prompt codex-worker "Read /abs/path/brief.md in full and execute it. Begin now."
```

Direct, non-interactive, with write access to the working tree:

```bash
codex exec --sandbox workspace-write -C /path/to/repo \
  --model gpt-5.6-luna -c model_reasoning_effort=low \
  "$(cat brief.md)"
```

Sandbox choice for a worker that must commit: `workspace-write`. Reserve
`danger-full-access` and `--dangerously-bypass-approvals-and-sandbox` for environments that
are already externally sandboxed — they skip every confirmation.

Structured output:

```bash
codex exec --output-schema schema.json "..."
```

Resume a prior session:

```bash
codex exec resume --last "follow-up instruction"
```

---

## 7. codex-zero status

`packages/codex-zero/` ships as of 2026-08-07, with its probe recorded in
`packages/codex-zero/PROBE.md` on codex-cli 0.146.0.

The discipline that got it there still applies to any route change: `execSupport` moves on the
strength of **a probe you ran**, on a pinned version, recorded before the route changes — never
on the strength of this document.

---

## 8. Anti-patterns

- **Leaving reasoning effort at the `max` default on probes.** Expensive and slow.
- **Passing `gpt-5.6-luna-light` as a model.** Not a model — use effort settings.
- **Scoping `CODEX_HOME` without copying `auth.json`.** The run cannot authenticate.
- **Omitting `--ephemeral` on probes.** Session files accumulate and pollute later runs.
- **Recording a dose without recording `codex --version`.** Inadmissible.
