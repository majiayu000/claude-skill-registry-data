---
name: pi-playbook
description: Drive the pi CLI as a benchmark target or dispatched worker. Use when running pi probes, comparing pi postures, launching pi-zero, or handing work to a pi agent. Covers the flag surface that maps onto Skill Heaven mechanisms, model selection, and non-interactive invocation.
---

# pi Playbook

`pi` is a coding agent CLI with a flag surface that maps unusually cleanly onto Skill Heaven's
mechanisms — it can evict and readmit skills natively, so postures compose without any
config-directory tricks.

Verified against **pi 0.83.0**. Re-check `pi --version` before trusting any dose measurement;
a flag's behaviour has changed across versions before (see §5).

> **Rule 0 — run pi in a herdr pane, never through your Bash tool.** The operator must be able to
> see which model you invoked. A probe the operator could not see is not evidence. Use
> `pane send-text` with a trailing newline **inside** the quotes — **not** `pane run`, which
> splits argv on whitespace and destroys quoted prompts:
>
> ```bash
> herdr pane send-text "$PROBE_PANE" 'pi --model openai-codex/gpt-5.6-luna:low -p --no-session "probe text"
> '
> herdr pane read "$PROBE_PANE"
> ```

> **Building the door?** Read `packages/core/skills/harness-door-pattern/SKILL.md` first — it
> carries the suppression-mechanism taxonomy, the probe methodology, and the traps. This playbook
> is the harness-specific detail underneath it.

---

## 1. Model selection

```bash
pi --list-models                 # all models
pi --list-models luna            # fuzzy search
```

Models are addressed as `provider/id`, with an optional `:thinking` suffix:

```bash
pi --model openai-codex/gpt-5.6-luna:low   "..."
pi --model openai-codex/gpt-5.6-luna:max   "..."
```

Session guinea pig: **`openai-codex/gpt-5.6-luna:low`** ("Luna Light") — use it for probes and
high-volume runs. `:max` ("Luna Max") is the heavier tier for coding work.

Thinking levels: `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max` — settable inline as
`:level` or via `--thinking <level>`.

---

## 2. Non-interactive invocation

```bash
pi -p --no-session "your prompt"
```

- `-p` / `--print` — process the prompt and exit.
- `--no-session` — do not persist a session file. **Always use this for probes**, otherwise
  probe runs accumulate as session state and pollute later comparisons.
- `--mode json` — structured output for machine consumption.

Read-only run (safe for evaluating a repo without edits):

```bash
pi --tools read,grep,find,ls -p "Review the code in src/"
```

---

## 3. Flags that map onto Skill Heaven mechanisms

| pi flag | Mechanism |
|---|---|
| `--no-skills` | evict all skills |
| `--skill <path>` (repeatable) | readmit exactly these — the curated posture |
| `--no-extensions` / `--extension <path>` | the extension (door) surface |
| `--no-context-files` | suppress `AGENTS.md` / `CLAUDE.md` discovery |
| `--no-prompt-templates` | suppress prompt templates |
| `--no-tools` / `--tools <list>` / `--exclude-tools <list>` | tool surface |

> **`--thinking` is NOT a Skill Heaven mechanism.** It sets how hard the *model* reasons. The
> Skill Heaven ladder is **skill- and context-scoped** — what is admitted into the session — and
> is a different axis entirely. The two share level names (`off`, `low`, `medium`, `high`,
> `xhigh`, `max`) purely by coincidence of vocabulary, and conflating them will produce
> meaningless benchmark arms. Hold `--thinking` **constant** across arms; it is a control
> variable, never the thing under test.

The curated posture is `--no-skills` followed by one `--skill <dir>` per admitted skill.
This is a native primitive, not a workaround — it is why pi is the cleanest door to build after
Claude Code.

---

## 4. Measuring standing dose

Ask the session what it can see, with and without suppression:

```bash
PROBE="List every skill you have available, by name. If none, say NONE."

pi --model openai-codex/gpt-5.6-luna:low -p --no-session "$PROBE"
pi --model openai-codex/gpt-5.6-luna:low -p --no-session --no-skills "$PROBE"
```

A correct suppression returns `NONE`. Anything else is a leak — record exactly what leaked.

Run every arm on the **same model at the same thinking level**, or the comparison is
meaningless.

---

## 5. Known version-sensitive behaviour

`packages/core/src/compile.ts` carries a note pinned to **pi 0.80.10**: `--no-skills`
immediately followed by `-p` silently lost the suppression, so the launcher emits tail args
first. Whether this still reproduces on 0.83.0 is recorded in
`packages/pi-zero/PROBE.md` — read that file rather than assuming either way.

The general rule: **argv ordering is load-bearing on pi**. When a probe gives an unexpected
result, try reordering before concluding a flag does not work.

---

## 6. pi as a dispatched worker

Via herdr (see `herdr-dispatch`):

```bash
herdr agent start pi-worker --kind pi --pane <PANE_ID> --timeout 120000 \
  -- --model openai-codex/gpt-5.6-luna:low

herdr agent prompt pi-worker "Read /abs/path/brief.md in full and execute it. Begin now."
```

Direct, non-interactive:

```bash
pi --model openai-codex/gpt-5.6-luna:low -p "$(cat brief.md)"
```

pi has read, bash, edit, and write tools by default. Constrain with `--tools` when the worker
should not be able to modify files.

---

## 7. Extensions

```bash
pi install <source>     # install an extension and add to settings
pi list                 # list installed
pi remove <source>
pi config               # TUI to enable/disable package resources
pi --extension <path>   # load an extension for one run, without installing
```

`--extension` is the right flag for testing a door surface without mutating the user's
settings — it keeps the P3 "never mutate shared state" guarantee intact.

---

## 8. Anti-patterns

- **Omitting `--no-session` on probes.** Session state leaks into later runs.
- **Comparing arms across different models or thinking levels.** Not a comparison.
- **Assuming a flag works because it is in `--help`.** Probe it, on the version in front of you.
- **Recording a dose without recording `pi --version`.** Inadmissible.
