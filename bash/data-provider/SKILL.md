---
name: data-provider
category: simulation
tier: D
description: "Turn a question about the world into a table Parallax can accept, with every field typed observed or simulated at the moment it is written. You do the searching — WebSearch, WebFetch, whatever reaches the corpus — and this skill owns the parts that must be identical every time and checkable afterwards: recording a finding against the artifact it was read from, hashing that artifact, judging each column observed or simulated by a stated rule rather than by feel, and emitting the exact `parallax propose --kind business-data` invocation. Use it to supply the business-data ingress, which otherwise has no supplier and depends on a human typing a table list by hand. USE WHEN find companies, find leads, find prospects, find suppliers, research a market, build a table from search, prospect for clients, gather evidence into a table, supply business-data, data provider, feed parallax, observed vs simulated for search results. NOT FOR general web research you are going to read rather than model (just search); scraping a site you already know the URL of (fetch it); any workflow where the output is prose rather than rows; and anything that needs a calibrated recall or precision number, which this deliberately does not publish."
triggers:
  - find leads
  - find prospects
  - build a table from search
  - supply business-data
  - data provider
  - feed parallax
effort: medium
---

# data-provider

Parallax proposes an ontology from what is actually in a context, and refuses to
run until a human accepts it. That makes every answer a function of what reached
the proposer — and `business-data`, its richest ingress, has **no supplier**.
Today a person types the table list by hand. This is the layer that fills it.

The searching is yours. This skill owns the four things that must be the same
every time and checkable afterwards.

## The split, and why it is the point

| You do | This does |
|---|---|
| decide what to search for | — |
| run WebSearch / WebFetch | — |
| read what came back | `record` it against the artifact, and hash the bytes |
| — | `judge` each column observed or simulated, by rule |
| — | `emit` the exact `parallax propose` invocation |
| — | `status` in numbers that cannot report motion that did not happen |

A model that both gathers evidence and decides whether the evidence is good is
grading its own homework. A model that gathers, and a function that grades
against a stated rule, is not. That is the entire architecture.

## The flow

```bash
# 1. Search however you like. For each thing you read and intend to cite,
#    save what you actually read -- not just the URL.
#
# 2. Build a records file: one object per row, one key per column.
#    A field is EITHER read from an artifact OR inferred. Never neither.
cat > records.json <<'JSON'
[
  {
    "company": {"value": "Arepas del Valle",
                "evidence": {"url": "https://…/directory/1",
                             "sha256": "…", "snapshot": "evidence/….snapshot"}},
    "fit":     {"value": 0.82, "inferred_from": "category match against the brief"}
  }
]
JSON

# 3. Emit. By default this OPENS every cited artifact and checks its digest
#    before classifying anything observed -- an unchecked citation is not
#    evidence, and `--unverified` exists only so that skipping the check is a
#    decision someone typed rather than a silent fallback.
python3 scripts/provider.py emit --table leads --records records.json \
    --run <run-id> --root .
#   parallax propose --kind business-data --table leads#1:company:string:observed,fit:number:simulated
```

The row count is **counted**, never declared. The origins survive into the
proposal a human accepts, which is what makes this handoff type-preserving
rather than lossy.

## Where the guarantee ends, precisely

This is worth stating exactly, because the loose version of it is false.

**What is enforced:** *this provider* will not emit `observed` for a field whose
artifact it cannot open and re-hash. That is checked, in both the library and the
CLI, and it is what R1 and R2 buy.

**What is not, and cannot be:** Parallax's runtime cannot verify anything. It has
no access to your run directory and may not even be on the same machine — a
`ColumnSpec.origin` reaching it is a *supplier's assertion*, and any caller
hand-typing `--table leads#40:company:string:observed` is making one with nothing
behind it. The runtime says so rather than hiding it: the proposal reads
"supplier reports its values observed", not "observed".

So the chain is: this provider verifies, then asserts; the runtime records who
asserted; the **human accept gate** is where an assertion nobody can check gets
weighed. Claiming the runtime enforces it would be the same overclaim this whole
layer exists to refuse.

## The one rule you cannot work around

A field is `observed` **only** if you hold the artifact it was read from and can
produce it. Everything else — concluded, matched, guessed, averaged — is
`simulated`, and must say what it was inferred from.

A field with neither is **refused** (`UNCLASSIFIED_FIELD`). Not defaulted to
`simulated`: that reads as caution and is a fabrication, because it asserts you
know the value was produced when you know nothing about it. And it is
unrecoverable — Parallax types values at birth and has no operator that adds
provenance afterwards, so a field that gets past this point untagged has thrown
the distinction away permanently.

Contamination flows one way. **A column with nine cited values and one guess is a
simulated column.** Reporting it as observed because most of it was read is the
overclaim the type exists to prevent, and it is the version a dashboard prefers.

## Seven rules, and where they came from

Each was derived from a specific observed failure in a prospecting service, not
from taste. `references/rules.md` carries the full statement of each.

| | Rule | The failure it answers |
|---|---|---|
| R1 | Classify at the moment of writing, never after | — (this is Parallax's constraint, not a defect) |
| R2 | A record cites its artifact or it is not evidence | a citation nobody can resolve is indistinguishable from an inference |
| R3 | Progress is work completed, never stage index | read 22% at t+2s and 22% at t+67s while its own counter said 0 of 11; a completion count that went **backwards**, 6 → 2 |
| R4 | Finding nothing is terminal and visibly distinct from still-running | no run was ever observed leaving `orchestrating` |
| R5 | A started run can be stopped by whoever started it | no cancel endpoint existed |
| R6 | Credentials are required, not optional | an uncredentialed server-side POST started real work |
| R7 | A page that renders is not a run that carried | the status shell returned HTTP 200 with identical bytes whether the backend was alive or dead |

**R5 and R6 are answered by shape rather than by code here, and that is stated
rather than hidden.** They exist because that thing was a long-running remote
service. This is a script you run inside your own turn: there is no endpoint to
authenticate and nothing that keeps running after the turn ends. `cancel` is
implemented anyway, because a run's directory outlives the turn. Implementing an
API-key check on a local function to tick R6 would be theatre.

## Reading a refusal

Every failure is a typed value, exit code 2, `{code, reason, detail?}` on stderr —
the same shape Parallax uses, so one branch handles both.

| Code | What to do |
|---|---|
| `UNCLASSIFIED_FIELD` | Add `evidence` or `inferred_from`. Do not pick `simulated` to get past it. |
| `EVIDENCE_INCOMPLETE` | Evidence needs a url, a **64-hex** sha256, and a snapshot path. A short or absent digest is a citation that cannot be checked wearing the word that means it was. |
| `EVIDENCE_UNVERIFIED` | Either a cited artifact is missing / no longer hashes to its digest, or observed records reached `emit_table_arg` without having been verified at all. Not downgraded to `simulated` — that would hide a broken pipeline behind a plausible table. |
| `EVIDENCE_ESCAPES_RUN` | A snapshot path is absolute or climbs with `..`. It must stay inside the run directory — Python's `/` discards the left operand on an absolute right-hand side, so such a path would let verification be satisfied by any file on the disk. |
| `RESERVED_CHARACTER` | A name contains `,` `:` or `#`. Those are `--table` delimiters, so such a name **injects extra columns** rather than producing a bad one. |
| `RECORDS_MALFORMED` / `RECORDS_UNREADABLE` | The records file is not readable, or not a JSON list of objects. |
| `AMBIGUOUS_ORIGIN` | The field has both. It is one or the other. |
| `NO_RECORDS` | You found nothing. That is a complete run, not a table — report it, do not emit. |
| `PROGRESS_WENT_BACKWARDS` | Your loop restarted rather than resumed. Fix the loop; do not lower the number. |
| `RUN_NOT_FOUND` | The run does not exist. This is deliberately not reported as a run at 0%. |
| `RUN_TERMINAL` | Already complete, failed or cancelled. Terminal means terminal. |

## Tests

```bash
cd skills/simulation/data-provider
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q     # 60 tests
```

`PYTHONDONTWRITEBYTECODE` because a same-size edit inside one second reuses stale
bytecode, which reports a mutant as survived without ever running it.
