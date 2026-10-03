---
description: >
  Run (or re-run) Stage 1 only — the Problem Investigator: citation graph,
  elite pool, deep reading, and the grounded Research Brief. Operates on the
  active run, or scaffolds a new one if a topic is given.
argument-hint: "[\"<topic>\" --task digits ...] | [--run <run-id>]"
disable-model-invocation: true
---

# /investigate — Stage 1: Problem Investigator

Arguments: `$ARGUMENTS`

Current state: !`python3 .claude/scripts/ledger.py status`

1. Resolve the run:
   - `--run <id>` given → use `workspace/runs/<id>`.
   - A topic string given → scaffold a fresh run first:
     `python3 .claude/scripts/new_run.py $ARGUMENTS`.
   - Neither → use the ACTIVE_RUN shown above; if none, ask for a topic.
2. Launch the `problem-investigator` subagent with the run directory, topic,
   and offline flag from `run-config.json`. It follows its own three-round
   protocol and the relevance gate.
3. On `ok: false` (gate abort): relay the reason; suggest better seeds in
   `workspace/seeds/` or a broader topic.
4. On success: run `python3 .claude/scripts/bib_validate.py <run>` (must
   pass), append ledger event
   `{"event":"stage_investigate","detail":"complete"}`, and show the user the
   brief's section headers plus the source count.

Next stage: `/discover`.
