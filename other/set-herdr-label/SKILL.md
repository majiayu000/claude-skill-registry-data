---
name: set-herdr-label
description: Internal helper that labels the herdr agent pane this session is running in, so a workspace full of agents can be told apart at a glance. Takes the desired label as its only argument and renames the current pane to a normalised form of it; an empty argument clears the label instead. Use when the work in flight has a name worth surfacing in the herdr sidebar — starting a feature, picking up a bug, switching to a materially different task — or when a previously set label no longer describes what this session is doing. Runs only inside a herdr-managed terminal (HERDR_ENV=1) and does nothing at all anywhere else, silently, so it is always safe to call. Writes no files, asks no questions, and never reports success in chat. Not user-invocable.
user-invocable: false
allowed-tools: Bash(herdr *), Bash(printf *)
---

# set-herdr-label — name the current herdr pane

Sets the agent name of the **herdr pane this session is running in**, so the user scanning a workspace of parallel agents can see what each one is doing.

**You are running inline, inside the calling turn.** The `Skill` tool loads these instructions into the same context that was already working — nothing is delegated, and nothing "returns" to a waiting caller. This skill is a side effect on the way past, not a destination.

Everything below is quiet by design. This skill produces **no chat output at all** — not on success, not on a skip, not on failure. A label is workspace furniture, not a result worth a sentence, and a label that failed to apply is worth even less than that: the user is mid-task, and the worst outcome here is derailing their attention to report that a cosmetic rename did not take.

## Input

The desired label, as the only argument — free-form text, e.g. `Fix login redirect loop`. You normalise it in Step 3; the caller is not expected to pre-slugify.

**An empty or whitespace-only argument means "clear the label"**, which is a legitimate call, not a missing input. Never ask the user what label to use, and never invent one from conversation context when the argument is empty — empty is an instruction.

## Step 1 — Gate on the herdr environment

Read the environment in one command:

```sh
printf '%s|%s\n' "${HERDR_ENV:-}" "${HERDR_PANE_ID:-}"
```

The output is `<HERDR_ENV>|<HERDR_PANE_ID>`.

**Skip silently unless `HERDR_ENV` is exactly `1`.** If `HERDR_ENV != "1"`, or `HERDR_PANE_ID` is empty, there is no herdr pane to label: stop this skill, say nothing about it, and **do not end your turn** — carry straight on with whatever you were doing when this skill was invoked. A skip is the normal outcome outside a herdr terminal and is never worth a remark.

`HERDR_PANE_ID` (e.g. `w9:p1`) is the target. It is the pane *this* session occupies, which is the only pane this skill may ever touch. Do **not** discover the target any other way — in particular, never call `herdr agent list` and match on `cwd`, because two sessions in the same repo collide and you would rename someone else's agent.

## Step 2 — Recognise the clear case

If the argument is empty or whitespace-only, skip Step 3 and go to Step 4 with the **clear** form.

## Step 3 — Normalise the label

herdr validates names server-side and rejects anything that does not match `^[a-z][a-z0-9_-]{0,31}$` — *lowercase letter first, then only lowercase letters, digits, `-` or `_`, 1 to 32 characters*. A raw label like `Fix login bug` is rejected outright, so normalise before calling.

Apply these rules in order, exactly:

1. Lowercase every character.
2. Replace every run of one or more characters outside `[a-z0-9_-]` with a single `-`.
3. Delete leading characters up to the first `a`–`z`.
4. Truncate to 32 characters.
5. Delete any trailing `-` or `_`.

Worked examples:

| Argument | Normalised |
| --- | --- |
| `Fix login bug` | `fix-login-bug` |
| `  spaced  out  ` | `spaced-out` |
| `UPPER_CASE` | `upper_case` |
| `feature/auth-v2` | `feature-auth-v2` |
| `123abc` | `abc` |
| `a-very-long-label-that-definitely-exceeds-the-limit` | `a-very-long-label-that-definitel` |
| `9` | *(empty — treat as clear)* |

If the result is empty (the label held nothing usable, as with `9` or `---`), treat it as the **clear** form rather than failing. A label that normalises to nothing carries no information, so removing the stale one is the useful outcome.

## Step 4 — Rename

Run exactly one of these, substituting the pane id from Step 1:

```sh
herdr agent rename "<HERDR_PANE_ID>" "<normalised-label>"
```

```sh
herdr agent rename "<HERDR_PANE_ID>" --clear
```

`--clear` is the **only** way to unset a name. herdr rejects both `""` and `"-"` with `invalid_agent_name`, so never try to clear by passing an empty string or a placeholder dash.

Exit code `0` means done. On a non-zero exit the command prints a JSON error such as `{"error":{"code":"invalid_agent_name",...}}`:

- **`invalid_agent_name`** — Step 3 was applied wrongly. Re-normalise once and retry. If the retry also fails, drop it silently; a missing label is not worth interrupting the user's work over.
- **Any other error** (socket unavailable, unknown target) — drop it silently. herdr not answering is the user's workspace state, not a problem with the task in hand.

Say nothing in chat on success — no confirmation, no "labelled the pane as …". The user can see the label in their own sidebar.

## When you are done

**Do not end your turn.** This skill is a side effect invoked mid-task; the moment the rename lands (or is skipped), continue with the work you were doing before it was invoked, exactly where you left off.

## Notes on scope

- **No Step 0 confirmation gate**, deliberately. The other proactively-invoked skills in this plugin gate because they spend the user's tokens or write artefacts; this one runs two commands and changes a label the user can see and override in their own UI. A confirmation round-trip would cost more than the action.
- **Writes no files.** It holds neither `Write` nor `Edit`, so it cannot.
- **Does not call `lessons-capture`.** It holds no `Skill` tool, so it cannot invoke any other skill — the `feature-mockup` precedent. There is no run to reflect on: the skill either renamed a pane or did not.
- **Touches only the current pane.** It never renames another agent, never stops or focuses one, and never changes anything else about the workspace.
