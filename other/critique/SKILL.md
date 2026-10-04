---
description: Dispatch to pi behind a critic gate — a second, independent pi session judges the work against a contract written up front, and rejections go back for a bounded number of rounds
disable-model-invocation: true
---

The user wants this built behind a critic gate: $ARGUMENTS

This is a normal dispatch with one thing added: **the work does not count as done because pi
said it was done**. A second pi session — a different session, with no memory of the first —
reads the diff against a contract and returns ACCEPT or REJECT, and a REJECT goes back to the
generator to fix.

The reason to separate the sessions is the whole point. A model asked to review its own output
has already committed to it: it has the reasoning that produced the code sitting in context,
and it will defend that reasoning rather than read what actually got written. A session that
has never seen the generator's thinking has only the diff to go on, which is the same thing a
human reviewer has.

You are neither of them. You write the contract, and at the end you judge — because two models
agreeing with each other is not verification.

## 1. Write the contract first — before anything is dispatched

The contract is the critic's rubric, and it is **written before the generator runs**. This
ordering is not a formality:

- A critic with no rubric free-associates. It will report style preferences and taste, because
  those are what is available to say about code when nobody has said what the code is for.
- A rubric written *after* seeing pi's output gets bent toward that output. You read what was
  built, and the criteria quietly become a description of it. Then ACCEPT means nothing, because
  it was never possible to fail.

Write it to a temp file, in numbered items, each one **decidable by reading the diff**:

```bash
DIR=$(mktemp -d)
cat > "$DIR/CONTRACT.md" <<'EOF'
# 驗收契約

1. <a condition someone can check by reading the code, and answer yes or no to>
2. ...
EOF
echo "$DIR"
```

"Handles errors appropriately" is not an item — nobody can fail it. "A malformed payload
returns 400 and does not reach the parser" is: you can point at the line that decides it.

If you cannot write four or five items this way, stop and say so. That is not a contract
problem; it means the task is not specified well enough to be gated, and gating it will burn
three rounds discovering that.

## 2. Dispatch the generator

Write the task book to `$DIR/TASK.md` — the real task, with the contract quoted into it. The
generator gets the contract too: gating work against criteria it was never shown is a trick,
not a test, and it fails the honest cases along with the sloppy ones.

Dispatch with `pi_dispatch`: `task_file="$DIR/TASK.md"`, `cwd` = the repo root, `mode="sync"`.
Leave `tools` at its default (`read,write,edit`) and leave `provider` / `model` unset.

**Keep the returned `session_id`.** Every fix round resumes it.

Then capture the diff:

```bash
git diff HEAD > "$DIR/DIFF-1.patch" && wc -l < "$DIR/DIFF-1.patch"
```

## 3. Dispatch the critic — a new session, every round

```bash
cat > "$DIR/CRITIC-1.md" <<EOF
You are reviewing a change against a fixed contract. You did not write it and you have not
seen the reasoning behind it. Judge only what is in the diff.

Write your verdict to $DIR/VERDICT-1.md and nothing else. Do not modify any source file.

Format:

判定: ACCEPT | REJECT

Then, for each blocking finding, most serious first:

### <relative/path.ts>:<line>
違反: 契約第 <n> 項
理由: <what input, what happens, why that fails the item>
信心: 高 / 中 / 低

Then, optionally:

## 額外觀察
<anything real you noticed that no contract item covers — one line each>

Rules:
- REJECT **only** for a finding that names a contract item it violates. Everything else is
  an observation and does not block.
- A finding needs a concrete failure. "Could be clearer" is not one.
- 信心: 低 is useful — say it rather than dropping the finding or overselling it.
- If every item holds, write ACCEPT with no findings. An honest ACCEPT is a real result.

--- 契約 ---
$(cat "$DIR/CONTRACT.md")

--- THE CHANGE ---
$(cat "$DIR/DIFF-1.patch")
EOF
```

Dispatch with `pi_dispatch`: `task_file="$DIR/CRITIC-1.md"`, `cwd` = the repo root,
`tools="read,write"`, `mode="sync"`, **no `resume_session_id`**.

`read,write` and not `edit`: the critic creates one file and reads surrounding code the diff
does not show. Nothing in a review justifies changing a line of source, and withholding the
tool is cheaper than trusting it not to.

**Two asymmetries, and they are deliberate:**

- **The generator resumes; the critic never does.** A critic that carries its own previous
  verdict anchors on it — round 2 becomes a check that round 1's complaints were addressed,
  not a fresh read of the code that now exists. Every round pays to re-read the whole diff.
  That cost *is* the independence; it is not overhead to optimize away.
- **Only contract-bound findings block.** A fresh critic each round can always produce new
  opinions, so without this rule the loop cannot converge — every round ends in REJECT for a
  reason that was never in scope. Observations get carried to the user at the end, not back
  to the generator.

## 4. The loop — at most 3 rounds

Read `$DIR/VERDICT-1.md`.

**ACCEPT** → go to step 5. Do not skip step 5 because the critic accepted.

**REJECT** → resume the generator with the findings, and nothing else:

```bash
cat > "$DIR/FIX-2.md" <<EOF
A reviewer rejected the change. Fix exactly these, and change nothing else:

$(cat "$DIR/VERDICT-1.md")
EOF
```

```
pi_dispatch(task_file="$DIR/FIX-2.md", cwd=<repo root>, mode="sync",
            resume_session_id="<the generator's session_id>")
```

Resuming is why the fix task book is three lines: pi still has the code it wrote and the
reasoning behind it, so restating the task would only give it a second, slightly different
version of the same instruction to reconcile.

Then re-capture the diff as `DIFF-2.patch`, write `CRITIC-2.md` from the **same contract**, and
dispatch a **new** critic session. Repeat at most three times.

**If round 3 still returns REJECT, stop.** Do not run a fourth. Three rounds against a fixed,
decidable contract without convergence almost never means the code is stubborn — it means the
contract item is not actually decidable, or it is asking for two incompatible things, or the
task needed splitting before it was ever dispatched. Report which item survived all three
rounds and say that. That diagnosis is worth more to the user than a fourth round would be.

## 5. Judge — the critic's verdict is evidence, not the gate

An ACCEPT from the critic means one model read the diff and did not object. Check it yourself
before it counts:

- Walk the contract item by item against the real code. Read the files. Trace the path.
- For any REJECT that was fixed along the way, confirm the fix does what the finding asked and
  did not quietly do something else.

Report as three groups, keeping all three:

- **確認** — you verified it, with the clause saying what you checked
- **誤判** — the critic was wrong; one line on why, so the user need not re-check your re-check
- **待確認** — needs context neither of you has; name what would settle it

Then the critic's 額外觀察, unfiltered and marked as unadjudicated. They did not block, they
were not checked, and the user should get to decide about them with that label attached.

## 6. Say what it cost

Close with: rounds used, the `duration_s` and token counts of every dispatch summed, and how
many findings were raised versus confirmed by you.

That last ratio is the number that matters over time. A critic confirming near 100% is doing
work; one confirming near 20% is generating text you then pay to refute, and the user is
entitled to find that out from their own runs rather than from this file's opinion.

## When this is worth running

Roughly 3-10× a plain dispatch, and on a **local endpoint the rounds are serial wall-clock** —
one pi at a time, so three rounds is three full runs end to end.

Worth it when a mistake is expensive to discover later: anything touching auth, money, data
migration, a public interface, or a failure mode that is silent. Not worth it for internal
tooling, scripts, or anything where the feedback loop is "run it and see" — there, the
ordinary dispatch plus `/pi-delegate:review` when something feels off is the better trade.

Not worth it either when the contract cannot be made decidable (step 1). The gate is only as
good as the thing it checks against, and an unfalsifiable contract turns three rounds of real
compute into a ceremony that always ends in ACCEPT.
