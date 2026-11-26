---
name: ecdsafail-oracle-loop
description: "Iterate on an ecdsa.fail route until a fresh official `ecdsafail run` says it is better, never on a self-reported number, and keep a route journal (tried, killed, next cut) that survives context compaction. Use for \"loop this route\", \"run it to a verified win\", \"what have I already tried\". Adapted from tanweai/pua (discipline only)."
license: MIT
---

# Chrischtallchugle (ecdsafail-oracle-loop)

*ecdsa.fail oracle loop and route journal*

Drive a route or lever change to a **harness-verified** result, and never lose route
state to compaction. Two mechanisms, both lifted from `tanweai/pua` and stripped to the
engineering:

1. **Oracle-gated loop**: "Claude saying done doesn't count; only the verify command
   counts." The verify command here is the official `ecdsafail` harness.
2. **Compaction-aware route journal**: dump tried/killed/next-hypothesis state to a file
   outside the context window so a reset doesn't cost you the search.

## Source and scope

Adapted from `https://github.com/tanweai/pua`: files `skills/pua-loop/SKILL.md`
(oracle loop, stall escalation) and `skills/pro/SKILL.md` (PreCompact state journal).

This integration imports the **loop and journal discipline only**. It deliberately does
NOT import: PUA/PIP rhetoric, plugin hooks, prompt routers, telemetry, feedback upload,
leaderboard/tier registration, email/phone intake, self-evolution baselines, or any
always-on behavior. Provenance is the repo + path above; this card was hand-written, not
byte-copied: treat the pua repo as inspiration, not a pinned dependency.

## Public boundary

For public `ecdsa.fail` coordination. Do not request or expose private endpoints, account
details, keys/tokens, raw logs, unreleased nonces, live candidate diffs, private mailbox
history, or submit authority. When a step needs private state, stop at a handoff boundary
and name the public evidence that justifies it. See `pip-discipline`.

## The oracle (what "done" means)

Score = `avg_executed_Toffoli x peak_qubits` (lower is better), validated on 9,024
SHAKE256-derived inputs reseeded by the free 96-gate identity tail (`DIALOG_TAIL_NONCE`).
A route is **done** only when ALL of these hold, never on a self-estimated count:

1. **Binary is fresh.** After any edit/`install`/`sync`: `(cd $CHALLENGE && ecdsafail run)`
   prints a score and it matches the leaderboard binary (stale-binary trap).
2. **Island is CLEAN.** Every config tightening reseeds the inputs, so the current
   `DIALOG_TAIL_NONCE` must still validate. Re-hunt via jieyilong's GPU island toolkit until the
   searcher prints `CLEAN`. A score on a dirty island is not a score.
3. **Score strictly beats the baseline** recorded in the journal (`prev_best`). Equal or
   worse is a rejection, not a win.

Concretely, the oracle command is:

```bash
cd $CHALLENGE && ecdsafail run    # exit 0 + printed score == the only success signal
```

If you cannot produce a fresh `ecdsafail run` number on a CLEAN island, you have NOT
finished. Say so and name the missing step as the blocker.

## Loop protocol

Run with the `/loop` skill self-paced (no fixed interval), or step manually. Each
iteration:

1. **Read the journal first** (see below). Do not re-try anything under `killed` or
   `do_not_retry`. Pick the highest-value untried structural cut.
2. **Make the smallest change that tests one hypothesis**: a structural cut, not a lever
   wiggle.
3. **Rebuild + re-hunt:** `install`/`sync` as needed, then re-hunt the island to `CLEAN`.
4. **Run the oracle:** `cd $CHALLENGE && ecdsafail run`.
5. **Judge against `prev_best`:**
   - strictly better -> accept; update `prev_best`, append to `wins`, journal the diff.
   - equal/worse, but island CLEAN -> reject; journal as `score-dead` under `killed`.
   - island won't go CLEAN after a fair hunt -> journal as `tail-sensitive`, park.
6. **Update the journal** before the next iteration (every iteration, not just on win).

### Stall escalation (from pua-loop, count-based)

- **3–4 consecutive rejections:** stop tweaking. Force a reassessment of the shared
  assumption behind the last attempts. Hand to `pip-discipline` and produce three
  *materially different* hypotheses, not three parameter tweaks.
- **5+ rejections:** re-examine the requirement itself: is the qubit shelf / lifetime /
  Toffoli move even on this route? Rebuild the route slate via `nasqret-playbook` off
  the current frontier diff. Do not keep looping the dead route.

Forbidden exits: "I can't solve this" with no evidence; declaring a win on a self-reported
count; looping the same idea past the escalation gates.

## The route journal (survives compaction)

State that must outlive a context reset lives in a file, not in the conversation:

```
~/.ecdsafail/route-journal.md
```

(Outside `$CHALLENGE` so it's never committed or reseeded.) Read it at the start of every
session and every loop iteration; rewrite the touched fields after every iteration and
**before any likely compaction**. Template:

```markdown
# ecdsafail route journal — updated <ISO date>
prev_best: <score>            # avg_Toffoli x peak_qubits on a CLEAN island
prev_best_nonce: <DIALOG_TAIL_NONCE that was CLEAN at prev_best>
active_route: <one line: the structural cut being tested>
next_hypothesis: <the next untried structural cut, most promising first>

## tried (this campaign)
- <route> -> <score or "dirty"> -> accept | reject

## killed / do_not_retry
- <route> — <reason: score-dead | tail-sensitive | structurally-dirty | validation-only>

## wins (chronological)
- <ISO date> <score> — <the diff that earned it> — nonce <...>

## key_context
- frontier target: <current SOTA Q.T> | levers in play | island box in use
```

Pair this with the stale-nonce gotcha: when you record a `prev_best`, record the
nonce that was CLEAN for it, because tightening anything reseeds the inputs.

**Optional auto-reinjection:** a Claude Code `SessionStart` hook with matcher `compact` can print
the journal back into the context after each compaction. Gate it on a flag file you create when the
loop starts and delete when the campaign is parked, or the journal leaks into unrelated sessions.
The journal on disk stays the source of truth either way.

## Invocation

- `/loop` then describe the route and point at this card: e.g.
  *"loop this route to a verified win: oracle is `cd $CHALLENGE && ecdsafail run`, gate on
  CLEAN island, beat prev_best in the journal."* Let it self-pace; it stops when the oracle
  reports a strict improvement or you `<loop-abort>`.
- Or run the protocol manually one iteration at a time. Either way, the journal is updated
  every iteration and the oracle is the only success signal.

## Completion gate

Do not call a route done, or prepare a submission, until you have a fresh `ecdsafail run`
score on a CLEAN island that strictly beats `prev_best`, and the journal records the diff +
the nonce. Submission itself goes through the official `ecdsafail` CLI (`ecdsafail submit`), not this
loop. This loop's job ends at a verified, journaled improvement.
