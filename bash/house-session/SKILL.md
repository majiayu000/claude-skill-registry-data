---
name: house-session
description: Runs a House Session on this host — a panel of pinned deciders from at least two model families, each seat a read-only command in its own lane, blind first round, counted, stopped and sealed by the HPP core.
---

> **Auto-Trigger:** When a decision is worth more than one model's opinion — a risky plan, a review before merge, a release gate, an incident with two diagnoses, a design with real options — and the answer must be checkable afterwards.
> **Keywords:** "house session", "deliberate", "panel", "second opinion", "several models", "cross-model review", "dissent", "judge", "steelman", "blind round"
> **Priority:** MEDIUM
> **Tools:** Bash, Read

## When NOT to Activate
- A question one test, one command or one file read answers — measure it; a panel is for judgement, not for lookup.
- The host has one model family (`house_session.py families` says `DEFERRED`) — do not run a one-family panel and call it a panel; record the deferral.
- A reversible change small enough to try and revert — the cost of a panel is several model runs.

## Contract

**INPUT:** a question with options (`hpp.decision/v1` question), the state being judged, and a panel file `hpp.panel/v1` naming each seat's role, provider, pinned model, family and lane.

**OUTPUT:** one `hpp.turn/v1` per seat per round (with its verbatim text beside it), then an `hpp.deliberation/v2` record sealed by `python -m hpp deliberate record`.

**EXIT CODES** (`scripts/house_session.py`):

| Exit | Meaning |
|---|---|
| 0 | `families`: two or more families available · `seat`: turn written |
| 1 | `families`: `DEFERRED` · `seat`: the seat failed or timed out — not judged, no turn |
| 2 | `families --require` deferred · `seat` refused: the seat WROTE to its worktree, a malformed answer, no git worktree, no HPP core |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| the seat's worktree | Reads (fingerprint before and after) | proves the seat did not write |
| `--out DIR` | Writes `<seat>-r<round>.turn.json` and `.txt` | the turn and the verbatim text its hash anchors |
| the seat's command | Runs it (argv, no shell) | the seat answers; the runner never calls a model itself |

## Process

1. **Check the host:** `python ${CLAUDE_PLUGIN_ROOT}/scripts/house_session.py families --maker claude`. `DEFERRED` stops here.
2. **Write the panel** (`hpp.panel/v1`) and check it: `python -m hpp deliberate plan panel.json --context context.json --out panel.json` — the context the seats receive becomes the evidence a `fact` may cite, and the panel file now carries it (its hash changed, so every later step reads this file).
3. **Give every seat its own lane** (its own git worktree, e.g. `git worktree add ../seat-a HEAD`), so a write is attributable.
4. **Round 1, blind, in parallel** — one runner per seat, each with its seat's CLI in read-only mode:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/house_session.py seat --panel panel.json --seat a --round 1 --out turns --root ../seat-a -- codex exec --sandbox read-only "$(cat prompt-a.md)"
   python ${CLAUDE_PLUGIN_ROOT}/scripts/house_session.py seat --panel panel.json --seat b --round 1 --out turns --root ../seat-b -- claude -p "$(cat prompt-b.md)" --allowedTools "Read,Grep,Glob"
   ```
   The prompt tells the seat its role and to print exactly one JSON object: `{"position", "confidence", "claims": [{"kind": "fact|inference|opinion", "refs": [...]}], "text"}`. A review-lens seat puts its `hpp.findings/v1` document in `text`; pass `--subject change.diff` so a review of another change is refused. The CLI lines are adapters: check that your CLI prints only the answer on stdout; a non-JSON answer is refused, never guessed.
5. **Count and decide the stop:** `python -m hpp deliberate stop --panel panel.json --turns turns.json` (a JSON list of the turn files). `continue` → the next round, each seat run with `--seen` and the hashes of the turns it read.
6. **Judge and seal:** the judge seat (another lane) answers with an `hpp.decision/v1`; over grounded dissent it also writes an `hpp.rationale/v1` (a steelman of each dissenting position and `would_change_if`). Then `python -m hpp deliberate record --panel panel.json --turns turns.json --judge judge.json [--rationale rationale.json] --out record.json` and `python -m hpp deliberate verify record.json`.

## Executed examples

```console
$ python scripts/house_session.py families --maker claude
{"status": "ready", "maker": "claude", "families": ["anthropic", "openai"], "providers": {"anthropic": ["claude"], "openai": ["codex"]}, "unknown_family": ["cursor"]}
```
<!-- executed: 2026-09-25 · exit=0 -->

```console
$ python scripts/house_session.py seat --panel ../panel.json --seat a --round 1 --out ../turns -- python ../pen.py
house_session: seat a wrote to its worktree; the turn is invalid. Paths now differing from HEAD: notes.md
```
<!-- executed: 2026-09-25 · exit=2 -->
(`pen.py` answered correctly and also wrote `notes.md`: the turn is refused and nothing is written to `--out`.)

```console
$ python scripts/house_session.py seat --panel ../panel.json --seat a --round 1 --out ../turns -- python ../clean.py
{"status": "turn", "turn": "../turns/a-r1.turn.json", "sha256": "65a05d923e6b46057ea96662d53908460d3018dcc9da8b4497edfec063ba4f3d"}
```
<!-- executed: 2026-09-25 · exit=0 -->
(the same seat without the write: the turn and its verbatim text are written, and the turn normalises against the panel.)

## Proof

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/house_session.py --self-test
```
