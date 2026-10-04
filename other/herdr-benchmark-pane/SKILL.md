---
name: herdr-benchmark-pane
description: Run Skill Heaven benchmark probes and side-by-side posture comparisons in visible Herdr panes. Use whenever comparing postures (floor, product-floor, curated, native), doors (claude-zero, pi-zero, codex-zero), or harnesses, and the operator must be able to watch every arm run.
---

# Herdr Benchmark Pane — side-by-side posture comparison

Benchmarking is only useful if the operator can see every arm running. This skill covers
laying out comparison arms in visible panes and collecting their output.

For **dispatching coding workers**, use the `herdr-dispatch` skill instead. This one is for
**measurement**.

---

## Hard rules

1. **Every arm is visible.** One pane per arm, all on screen together. An arm that ran
   off-screen is not evidence anyone can check.
2. **Explicit `--cwd` on every split.** Prevents state leaking between arms.
3. **Never take over the controlling pane.** The orchestrator's pane stays the orchestrator's.
4. **Arms are priced separately, never averaged.** The doorless benchmark floor and the
   doorful product floor are different objects (founder ruling V5-5) — do not fold one
   into the other, and do not report a single blended "floor" number.
5. **Never report a measurement you did not take.** If an arm did not run, say it did not run.

---

## 0. Verify the environment

```bash
herdr status
```

Proceed only if `server.status: running`.

---

## 1. Paths

The checkout is at `/Users/marcotiongson/gaia-skill-heaven`. Door entrypoints:

```
packages/claude-zero/bin/claude-zero.mjs
packages/pi-zero/bin/pi-zero.mjs
packages/core/bin/skill-zero.mjs
```

Resolve these relative to the repo root rather than hardcoding an absolute path — the
checkout location has moved before and stale absolute paths silently break this skill.

```bash
REPO="$(git -C . rev-parse --show-toplevel)"
```

---

## 2. Lay out the arms

Orchestrator on the left, arms stacked on the right:

```bash
# arm A
ARM_A=$(herdr pane split --current --direction right --ratio 0.5 --cwd "$REPO" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['pane']['pane_id'])")

# arm B, stacked under A
ARM_B=$(herdr pane split "$ARM_A" --direction down --ratio 0.5 --cwd "$REPO" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['pane']['pane_id'])")
```

---

## 3. Non-interactive probes

For a probe that runs and exits, you do not need to start an agent in the pane.

**`pane run` takes argv as separate tokens and does NOT preserve shell quoting.** It is fine for
a command with no quoted arguments:

```bash
herdr pane run "$ARM_A" node packages/claude-zero/bin/claude-zero.mjs --print
herdr pane run "$ARM_B" node packages/claude-zero/bin/claude-zero.mjs --posture product-floor --print
```

**The moment your command contains a quoted prompt, use `pane send-text`** with a trailing
newline inside the quotes. `pane run` will split the prompt into separate arguments, and a shell
glob character in it (`(`, `*`, `?`) will fail outright:

```bash
herdr pane send-text "$ARM_A" 'pi --model openai-codex/gpt-5.6-luna:low -p --no-session "List every skill you can see."
'
herdr pane read "$ARM_A"
```

This has silently corrupted probes before — a split prompt still returns a plausible-looking
answer to a question you did not ask.

Read the results:

```bash
herdr pane read "$ARM_A"
herdr pane read "$ARM_B"
```

`--print` emits the compiled plan (argv, env, fsPlan, doseSummary) **without spawning the
harness**. This is the cheapest way to compare compositions and it costs no model tokens.

---

## 4. Interactive arms — `agent start`

When the arm must be a live session:

```bash
herdr agent start arm-native --kind claude --pane "$ARM_A" --timeout 120000 \
  -- --model sonnet

herdr agent start arm-zero --kind claude --pane "$ARM_B" --timeout 120000 \
  -- --model sonnet
```

For a door-launched arm, start a plain shell pane and `pane run` the door binary — the door
execs the harness itself, so let it do that rather than starting the harness first.

Send the same probe to every arm so the comparison is fair:

```bash
PROBE="List every skill you have available, by name. If none, say NONE."
herdr agent prompt arm-native "$PROBE" --wait --until idle --timeout 300000
herdr agent prompt arm-zero "$PROBE" --wait --until idle --timeout 300000
```

Collect:

```bash
herdr agent read arm-native
herdr agent read arm-zero
```

---

## 5. Standard comparison matrix

| Arm | Command | What it prices |
|---|---|---|
| native | `claude-zero --posture native --print` | the unmodified harness |
| benchmark floor | `skill-zero --posture floor --print` | doorless absolute zero — placebo-of-record |
| product floor | `claude-zero --posture product-floor --print` | the nearest launchable zero, door open |
| curated | `claude-zero --posture curated --skill <dir> --print` | a chosen skill set and nothing else |

The gap between benchmark floor and product floor **is** the door's cost. Report it as its
own number; never let either floor stand in for the other.

---

## 6. Cross-harness arms

Same probe, different harness, one pane each:

```bash
herdr pane run "$ARM_A" node packages/claude-zero/bin/claude-zero.mjs --posture curated --skill "$SKILL" --print
herdr pane run "$ARM_B" node packages/pi-zero/bin/pi-zero.mjs --posture curated --skill "$SKILL" --print
```

Harness versions must be recorded with any result — a dose measured on one version does not
carry to another. Capture them:

```bash
claude --version; pi --version; codex --version; hermes --version; grok --version
```

---

## 7. Recording a result

`packages/core/src/record.ts` assembles an `hh-ledger/v1` record via `--record`. Use it rather
than hand-writing numbers into a document.

Any recorded result must carry: harness name **and version**, date, posture, the exact argv,
and the observed dose. A result missing its harness version is not admissible.

---

## 8. Teardown

```bash
herdr pane close "$ARM_A"
herdr pane close "$ARM_B"
```

Leave panes open while their output is still evidence the operator has not reviewed.
