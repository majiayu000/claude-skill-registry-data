---
name: requirement-ledger
description: Track a project's long-lived requirements and recall what earlier deliveries decided. Use before clarifying a new request in an evolving project, and when a run starts, finishes or is archived.
---

# Requirement Ledger

A **requirement** is one long-lived business capability of a project, named `REQ-<n>`. It outlives any single delivery: the product evolves and the same requirement gains new runs. The ledger keeps one Markdown record per requirement — its current summary, plus *references* to the runs, specs, ADRs, deliveries and code behind it. It holds pointers, never copies.

Two boundaries hold throughout this skill:

- **Workloop is the only coding orchestration centre.** It owns runs, tickets, attempts, verdicts, delivery state and the run state machine; the ledger owns none of that, and reads a run's `state.json` without writing it.
- **The ledger executes nothing.** It runs no code, starts no agents, creates no tickets and pushes nothing. It answers two questions: which requirement is this, and where is that requirement's history.

## Look up before you clarify

Before a request becomes a spec, a ticket or a change, run the lookup on the user's own words:

```
node <this skill's directory>/scripts/req.mjs lookup "<the request>"
```

It scores every requirement of the current project on title, aliases, summary and refs, and returns up to five candidates with `score`, `matched_terms` and a `decision`: `strong`, `ambiguous` or `none`.

The lookup is evidence; Main decides, from the whole conversation. `strong` means the leading candidate clearly outscores the rest, not that the request belongs to it: check it against what the user said. On `none` or `ambiguous` the words did not settle it, and the reply lists every requirement of the project — id, status, title, aliases and the start of its summary. Judge which one the request belongs to, or that none does and it is new. Ask the user only when you cannot tell, naming at most three.

When the user confirms a requirement the words missed, add the term they used to its `aliases`, so the next lookup finds it. Don't add one on your own judgement: a wrong guess would come back next time as a strong match. [Lookup](reference/lookup.md) gives the scoring rule and what each decision promises.

## Keep the record current

| Moment | Command |
|---|---|
| A request belongs to a new requirement | `new "<title>" --alias <term>` |
| The user restates what a requirement covers | Edit the prose; `note` to record the change |
| A run starts | `link <project>/<feature> <REQ>` |
| The run finishes | `sync <project>/<feature>` |
| The run is archived | `sync <project>/<feature>` again |
| A Quick change, with no run | `note <REQ> --outcome …` |

`link`, `sync` and `note` are the whole Workloop integration: each writes only the ledger, and `link` and `sync` take their facts from the run's `state.json`. [Authorization](reference/authorization.md) covers their rules, including the one controlled way to correct a wrong association.

## Read the context before designing

Before designing a change to an existing requirement, run `context <REQ>`. It returns the requirement's summary and, in a fixed order, pointers to the specs, tickets, acceptance results, ADRs, delivery SHAs, evidence directories and CodeGraph hints behind it — enough to start from what was already learned instead of from nothing. [Context](reference/context.md) explains the order and the three delivery states that look alike and mean different things.

## Commands

| Command | Purpose |
|---|---|
| `new <title> [--alias …]` | Create a requirement, allocating `REQ-<n>` |
| `list` | List this project's requirements |
| `show <REQ>` | Read one requirement in full |
| `lookup "<text>" [--json]` | Find candidate requirements for a request |
| `context <REQ> [--json]` | Assemble the references for design work |
| `link <project>/<feature> <REQ> [--correct --reason]` | Record, or correct, which requirement a run delivers |
| `sync <project>/<feature>` | Copy the run's authoritative delivery into the ledger |
| `note <REQ> [--outcome …]` | Record Quick work, or a note |
| `retire <REQ>` | Mark a requirement retired; file and number stay |
| `doctor [--repair-log]` | Report inconsistencies, and fill recoverable audit gaps |

The CLI is `scripts/req.mjs`, beside this file. Run it from the project whose requirements you are reading.

## Reference

- [Domain](reference/domain.md) — what a requirement is, how it is identified, and how it relates to runs.
- [Storage](reference/storage.md) — the `.requirements/` layout, the record's fields, identity allocation, locking and the audit log.
- [Lookup](reference/lookup.md) — how candidates are scored and where that advice stops.
- [Context](reference/context.md) — what `context` returns, in what order, and the states a delivery passes through.
- [Authorization](reference/authorization.md) — the Workloop boundary, and what the ledger must never do.
