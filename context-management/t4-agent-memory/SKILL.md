---
name: t4-agent-memory
description: Use when working as the primary coding agent in a T4-team repo (T4 Labs / Slow-Inc) and you need durable memory across sessions and context-compaction — at session start (what's the open work, what did past sessions decide), after shipping or learning something worth persisting, or when open work is scattered across issues, ADRs, and MD files. Covers the team memory vault, the open-work ledger, the ship log, the survey-provenance cache, and Serena code memories. Triggers include "where did we leave off", "record what I shipped", "read the project memory", "what's still open".
---

# T4 Agent Memory

## Overview

In a T4 repo the **agent is the primary coder**, and an agent's binding constraint is its context window — it loses everything on compaction and between sessions. So the repo's memory files are not team paperwork; they are the agent's **durable working memory**. This skill is how to read and write that memory efficiently.

**Core principle: retrieval-first.** Store memory so a future agent can pull the *one relevant slice* into a fresh context — never so it must load a giant file to find one fact. An index you skim + linked detail you open on demand beats one append-only wall of text every time. The whole-file scan is the failure mode; the index-then-open is the pattern.

## The memory layers

Each layer exists because it answers a different question, and each is structured so you retrieve a slice, not the whole.

| Layer | Answers | Retrieval unit | Read it when |
|---|---|---|---|
| **Team memory vault** — `Obsidian-<Repo>/` (committed), `Home.md` is the Map-of-Content index | "What durable facts/decisions/feedback does the team hold?" | one note per memory, opened via `Home.md` links | **Every session start** — read `Home.md`, then only the linked notes the task touches |
| **Personal memory** — `~/.claude/projects/<slug>/memory/` + `MEMORY.md` index | "What did *I* learn across my own sessions?" (same note format) | one file per memory, via `MEMORY.md` | Loaded by the runtime each session; keep in sync with the vault |
| **Open-work ledger** — `docs/OPEN-WORK-LEDGER.md` | "What is still open, tracked *and* untracked?" | one row per work item | **Every session start** — the consolidated *discovery index* (GitHub issues stay the source of truth for tracked work; the ledger also catches untracked MD-only items and reconciles to issues) |
| **Ship log** — `DONE.md` | "What did past sessions actually ship, and how was it validated?" | one dated entry (newest on top) | When you need the history of a change; append after each shipped unit |
| **Skill-usage feedback** — `skill-feedback` issues on `xenodeve/xeno-skills`; `Obsidian-xeno-skills/skill-usage/` as the local copy while developing the library | "Which rules actually held in real work, and how often did each fail?" | one issue per rule, one comment per session | **Before changing a skill** — read its issue instead of designing a benchmark; report at session end from any repo |
| **Survey-provenance cache** — `docs/reports/survey-manifest/` | "What did a prior scan already read, at which commit?" | one entry per file/issue/PR | Before a broad codebase/issue survey — skip or diff unchanged sources |
| **Serena code memories** — `mem:` graph | "How is the *code* structured?" | one memory per topic, reached via `mem:core` | When exploring unfamiliar code |

## Session-start read protocol

Do this at the start of every session in a T4 repo, in order, and **stop pulling detail once you have enough for the task** — don't preload the whole graph.

1. **`Home.md`** (team vault MoC) — skim the one-line descriptions; open only the notes the current task touches. Unresolved `[[wikilinks]]` = memories worth writing.
2. **`docs/OPEN-WORK-LEDGER.md`** — the current open work. The 🔴 UNTRACKED rows (MD-only, no issue) are the highest miss-risk; they don't show up in `gh issue list`.
3. **The relevant GitHub issue(s)** — `gh issue view <n> --comments` for the item you're picking up.
4. **`DONE.md` / survey-manifest / Serena `mem:core`** — only if the task needs history, prior scan provenance, or code-structure context. Not by default.

## Retrieval-first rules (this is the discipline)

- **Index-then-open, never whole-file scan.** `Home.md`, the ledger table, and the survey-manifest index exist so you load a pointer and open one slice. If you catch yourself reading a 1000-line log end-to-end to find one fact, the file is mis-structured — fix the structure (add an index / split it), don't normalize the scan.
- **One source of truth per fact.** Open work lives in the ledger (mirrored to a GitHub issue); a decision lives in one ADR; a shipped change is logged once in `DONE.md`. Duplicating the same fact across `Todo.md` + `Roadmap.md` + ledger + log is how an agent ends up trusting a stale copy. When you find a duplicate, collapse it: keep the canonical one, replace the others with a one-line redirect marker.
- **Bound the append-only logs.** `DONE.md` and the impact register grow forever. Keep them retrievable: newest entry on top, one dated `##` heading per unit so an agent can jump; when a log crosses ~a few hundred lines or a phase closes, archive the old part to `DONE-archive-<period>.md` and leave a redirect. A log you can't load isn't memory.
- **Freshness over authority.** A memory or doc that cites `file:line` looks authoritative but silently rots when code moves. Before you rely on a cited location, verify it still exists. A wrong fact that looks confident is worse than a missing one — for a human, far worse for an agent that can't easily sanity-check.
- **Write memory a future agent can act on, not a diary.** Dense, durable, generalizable. Not "today I fixed X" — instead the invariant/decision that stops the next agent repeating the mistake.

## Writing memory

- **One note = one memory.** Filename = hyphen-kebab slug matching the note's `name:` frontmatter so `[[wikilinks]]` resolve. Frontmatter carries `type` (`feedback` / `project` / `reference` / `user`) + a one-line `description` (this is what a future agent skims in `Home.md` to decide relevance). Add a line to `Home.md` when you create one.
- **Add/update threshold — be strict.** Persist only stable, non-obvious conventions/decisions/feedback that save a future agent from costly rediscovery. Do NOT persist: quick-read facts, generic framework knowledge, one-off task notes, volatile line-level details, or anything likely to change soon. If asked to "remember" something the repo already records (code structure, git history, a past fix), persist instead *what was non-obvious about it*.
- **Link liberally.** A `[[name]]` that doesn't exist yet marks a memory worth writing later — it's a to-do, not an error. Reference related memories so the graph, not any single note, holds the structure.
- **Update, don't duplicate.** Before writing, check `Home.md` for a note that already covers it; edit that one. Delete memories that turn out to be wrong.

## The skill-usage log

Every skill in this family was improved the same way: a session went wrong, somebody noticed afterwards, and the finding was reconstructed from a transcript. That needs a person to remember something felt off, and it only catches failures large enough to survive to the end of a session. The alternative — handing a skill to an agent on an invented task and grading the output — buys one synthetic session at full price, with no control run and nobody needing the work.

Real sessions already produce this data and throw it away. The log keeps it.

### The GitHub issue is the record

Report to **`xenodeve/xeno-skills`**, from whichever repo the session ran in. A file was the first design and was refuted: a directory inside a git checkout vanishes on `git switch`, and a session that ends by crashing or cancellation never reaches "session end" at all, so a file written there is written never. An issue has neither property.

**One issue per rule, not per session.** A rule that fails in five sessions is one issue with five comments, and the comment count is the frequency. A new issue per session buries the signal it exists to surface.

At session end, for each rule that did not hold:

1. **Search, `--state all`.** `gh issue list --repo xenodeve/xeno-skills --state all --search "<skill> <rule>"`. `gh issue list` defaults to `--state open`, and the closed ones are the expensive misses — one may already contain the analysis you are about to redo, or record that the behaviour you are calling a bug is deliberate.
2. **Found one → add a comment.** Do not open a second.
3. **None → open one**, labelled **`skill-feedback`**, titled `feedback(<skill>): <the rule that did not hold>`.
4. **Pass `--repo xenodeve/xeno-skills` on every call.** `gh` defaults to the repo you are standing in; without the flag the feedback lands in whatever project you happened to be working on.

Each report names the **skill file**, the rule **in the words the skill uses**, and **what was actually written or done, quoted** — plus whether the rule was skipped outright or followed and still produced the wrong thing.

### What an absence in the log means, and where the denominator starts

**An absence is `unknown`, not `no`, until you have checked that the hook existed.** `t4-skill-log` is a **tracked file**, so a checkout can remove it: a branch cut from a base that predates it runs with no logger and no registration, and the log it does not write is indistinguishable from a session that loaded nothing.

**Measured, on this repository.** Of 52 `Skill` invocations in one session's transcript, the log holds 11. Everything before the hook's install commit is missing for the obvious reason — and **three more are missing from a single contiguous window**, bracketed exactly by two commands:

```
28843  git switch -c chore/255-plan-tracking-issues main   <- a base without the hook
28886  simplify        not logged
28931  code-review     not logged
28983  scrutinize      not logged
29219  git switch feat/185-turn-end-wiring                  <- the hook returns
29784  security-review logged
```

**Two plausible explanations were offered before this one and both were wrong** — that the logger filtered non-library skills (`security-review` is not in `skills/` and is logged twice), and that the ~32 KB argv cap ate them (every `tool_result` in that window is 110–124 bytes). A gap in a measurement invites a mechanism; check the observer was present before proposing one.

**So before reading a rate out of this file:**

1. `git log --diff-filter=A -- .claude/hooks/t4-skill-log` — the denominator starts there, and nothing earlier counts.
2. Any window spent on a branch cut from an older base is a hole. **An AFK batch cuts branches constantly**, which is exactly when it opens.

**This is #241's class from the other side** — there, the enforcing copy of a hook was not the tested one; here it was simply absent, and the artifact cannot say so about itself.

### The Obsidian note

Keep writing `skill-usage/<YYYY-MM-DD>-<slug>.md` in the library's own vault (skeleton in `references/memory-artifacts.md`) **only when the session ran inside `xeno-skills` itself**. There it is the working database you read while changing a skill, next to the code. A session in any other repo files the issue and writes no note — the note would live in a checkout that repo does not have.

**This is deliberately not a vault note**, and the strict add/update threshold above does not apply to it. That threshold rejects one-off task notes, which is right for the vault and exactly wrong here: a feedback database needs the unremarkable entries, because the rate is the signal. A log of only the memorable sessions is a failure-selected sample, and no rate can be computed from one.

Three rules:

- **A session that skipped a rule must record the skip** — including the embarrassing case, especially the embarrassing case. An empty section is written out as "none observed" rather than dropped, because silence is indistinguishable from compliance in the only record anybody reads. This is the principle `check-gate-ledger` is built on.
- **Only what happened in this session.** A reconstructed retrospective is a hypothesis wearing a log's clothing.
- **Name the skill file and quote what was actually written or done.** A finding without its artifact cannot be acted on by whoever reads it next.

**Writing the entry is agent discipline.** No hook produces the *findings*, and none can — a hook enforces checkable actions, not judgement (`docs/adr/0001-hook-based-workflow-enforcement.md`). Treat a missing entry as a missing entry, not as a session in which nothing went wrong.

**Only the judgement half is beyond mechanism, and the sentence above used to claim the whole obligation was.** The *denominator* — which skills a session actually invoked — is a checkable action and `hooks/t4-skill-log` performs it, wired on `PostToolUse`. Read the distinction the way it is: nothing can decide **whether a rule held**; something already records **what was loaded**. Two sessions stood behind the overstated version.

**`/handoff` is not the end of the session, and it is where the report keeps dying.** It produces a document, it feels terminal, and the report is not part of it — so the agent reaches it, writes a good handoff, and stops. **Reaching `/handoff` does not discharge the session-end report**, the same way `using-t4` says a parent skill does not discharge its leaves.

**Measured across three consecutive sessions**, which is this file's own threshold for *a design problem in the rule rather than a bad session*:

| session | tracker issues | local note |
|---|---|---|
| 2026-08-14 | none | none — the handoff *named the debt* and did not pay it |
| 2026-08-17 | written | owed |
| 2026-08-19 | written | written — **only because the session ran on past `/handoff`** |

The third row is not a success. The report was produced because something external kept the session going, not because reaching the end produced it.

## Dev notifications (agent → developer)

The agent runs long/AFK; surface reaching-a-decision or done to the developer's phone. Prefer the repo's real-toast script (e.g. `scripts/notify.ps1`) over the built-in push tool when the latter doesn't surface a toast on the dev's setup. Notify on: a TDD cycle / long task complete, needing a confirm (before closing issues / merging), or an AFK batch done — not routine sub-progress.

## Skeletons

See `references/memory-artifacts.md` for drop-in skeletons: `Home.md` (MoC index), a memory note, `OPEN-WORK-LEDGER.md`, `DONE.md`, the survey-manifest schema, and the Serena `mem:` conventions.

## Common mistakes

- **Loading the whole vault / whole log every session.** Defeats the point. Skim the index, open the few notes that matter.
- **A ledger that only lists GitHub-tracked work.** The MD-only 🔴 items are exactly the ones that vanish — the ledger's job is to catch them.
- **Letting `DONE.md` grow to thousands of lines unindexed.** It stops being loadable. Archive by period; keep it skimmable.
- **Trusting a `file:line` citation without checking it.** Verify before relying.
- **Writing a diary entry as "memory."** If it isn't a durable, act-on-able invariant, it's noise in the graph.
