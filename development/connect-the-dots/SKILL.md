---
name: connect-the-dots
description: >-
  Given a problem or a new feature, find the modules this codebase already has
  that cover parts of it, before anything new is designed. Restates the problem
  as the capabilities it needs, searches the repo's own maps and any installed
  code graph, index or code RAG before grepping, reads the candidates, and
  returns a cited fit table plus the remainder that is new. Trigger on
  /connect-the-dots, and on "what do we already have for this", "what can we
  reuse for X", "are we reinventing something", "what existing pieces solve
  this", "I keep getting stuck on X, what am I missing in our own code", or
  when a design for a new subsystem has stalled across sessions. Strategic and
  read-only: it names candidates and stops. Do NOT fire when the module to
  change is already named (that is /recon), to audit paths that already
  duplicate each other (that is /dry), to shrink a solution already chosen
  (that is /ponytail), to choose between options already on the table (that is
  /better-options), or to decide whether the problem is worth solving (that is
  /sanity-check or /worth-it).
argument-hint: "<the problem or feature, in the operator's own words>"
---

# Connect the Dots

A module is named for what it is, not for the problem it could solve. Search for the problem's name and you find the documents about the problem. The parts that would solve it sit under other names, in other folders, and nobody proposes them.

The case this skill was written for (GH-1484): sessions spent on "get the flywheel outer loop going" kept returning to the flywheel documents and never weighed the repo's coordination kernel or its variation runner. In one recorded comparison, a fresh agent given that wording named neither; a second fresh agent asked for "a loop that claims tasks so two agents never collide and runs parameter variations" named both. One run each, so it is an observation, not a rate. It is why step 1 comes first, and why step 2 also sweeps the maps in reverse: a capability list only finds what it thought to ask for. This skill makes the candidates and the dismissals visible. It does not guarantee a particular module is chosen.

## When to run

- A problem or feature looks new, and the next move would be to design something.
- Work on one problem has stalled across sessions and keeps circling the same documents.
- The operator asks what already exists that could be reused.

## Skip when

- The module to change is already named. Trace it with `recon`.
- It is a local bug fix. Use `debug-mantra`.
- The repo is small enough to list in one glob. Read it.
- A fit table for this problem exists and no relevant commit has landed since. Re-read it.

## Which skill, by the open question

Phrases overlap ("is this already implemented somewhere" can mean two things). Pick by what is still unknown:

| Open question | Skill |
|---|---|
| Which existing modules could carry this problem? | `connect-the-dots` |
| How does the module I picked work, end to end? | `recon` |
| Which paths that already exist should be one? | `dry` |
| Which of these options survives? | `better-options` |
| How much evidence do I buy before shrinking a known change? | `triangulate` |
| What is the smallest version of this solution? | `ponytail` |
| Is this problem real and worth fixing now? | `sanity-check` |

## Step 1 — State the problem as capabilities

**Say it back first.** From the operator's words alone, before opening any file, write one to three sentences under each heading:

- **What this asks for.**
- **How it is handled today, per the operator.**
- **What it's not.**

This is a self-paraphrase adapted from the paraphrase-first lens (Elephant-Goldfish Model, GH-1414). The lens proper uses a reader with no session history; here the same agent says the operator's words back, and the independent form is the optional `consult` hand-off below. The rules are written once in [`start-task` Step 6](../../1-hourly/start-task/SKILL.md); follow them, do not restate them: ground each exclusion in something the operator said, label inference as inference, never invent a non-goal. A heading that cannot be filled from the operator's words is the first unknown: write `not stated` and carry it to step 4. The capability list below is built from this paraphrase, so a wrong reading of the problem is visible here, before it decides what gets searched.

Then write down, still before any search:

- **Outcome:** what is true when this is solved, in one sentence.
- **Constraints:** what must not change, and what the operator has already ruled out.
- **Capabilities:** three to seven verb phrases the outcome needs. Each names an action and the thing acted on, with no solution noun and no repo jargon.

"Outer loop for the flywheel" is a solution noun. Its capabilities are: wake on a schedule; claim a task so no second agent takes it; survive a restart without redoing finished work; run variations of an input unattended; record a receipt for each completion.

For each capability, list two or three synonyms and the state it would own (claim / lease / lock / token; fuzz / variation / mutate; receipt / ledger / journal). These are the search terms. The problem's own name is not one of them: if every search term appears in the operator's sentence, the breakdown is not done.

## Step 2 — Search by capability, then read

Use what the repo already paid to describe itself before any grep. Work down and stop at the first rung that yields named candidates for every capability:

1. **Purpose-written maps.** `ROUTER.md` routing hints, `ARCHITECTURE.md`, `README.md`, a skills index, ADRs. These describe modules by what they are for, which is what a capability search needs. A code graph indexes symbols, not purpose, so maps come first here.
2. **An installed code graph, index or code RAG.** The rungs, their order and their freshness rules are already written; follow them, do not restate them: [`swe-diagram` Step 1](../../4-occasional/swe-diagram/SKILL.md) (graphify output, the codebase-memory graph, `ask_self`, written docs, source last) and [`recon` Step 2](../../1-hourly/recon/SKILL.md) (check the indexed revision; "the graph is a lead, not a citation"). Query by capability and synonym. Search the graph by capability verbs and their synonyms (`schedule tick heartbeat`, `retry park attempt`), not by module names; tracing callers and callees from a candidate is optional.
3. **Grep, last.** Only for capabilities the rungs above left empty.

State the mode in the output: which maps, which index and at what revision, or `grep-only`. A missing or stale index is said in one line, not worked around silently.

**Then sweep the maps in the other direction.** Searching by capability only finds what the capability list thought to ask for. Walk the purpose-written map once, top to bottom, and for every subsystem it names ask the reverse question: what does this do, and could any part of the problem use it? A subsystem the capability list never mentioned is the dot this skill exists to connect. List each subsystem considered with a one-line verdict (`candidate` or `set aside: <reason>`), so a reader can see what was looked at and dismissed. Bound it to the maps; this is not a walk of the source tree.

A `set aside` reason says what the subsystem is not, and where that comes from: the map line or source line read, or the word `inferred`. A reason taken from the subsystem's name or from one phrase in a map is `inferred`. Before an `inferred` dismissal stands for a subsystem that shares a verb with any capability in step 1, open its source; then it is either a candidate or a dismissal with a line behind it. Silence in a map is not an exclusion. Close the sweep with a count: how many subsystems the map names, and how many got a verdict. If the numbers differ, say which were skipped.

Then **read every shortlisted candidate's source.** A map line or an index hit is a lead. A candidate enters the fit table only after its source was opened, and the row cites the lines read. That holds for every column: a line cited for an owner or a constraint also comes from a file that was opened. A search hit that was not opened is written as a search hit, not as a citation.

If a shortlisted candidate fails the constraint check in step 3, continue for that capability from the rung below the one that produced it, and do not reconsider a candidate already rejected. The stop rule above holds only for candidates that pass. Grep is the last rung: when its candidates fail too, the row reads `not found in these searches` and lists the rejected candidates with the constraint each failed. Do not repeat the searches.

## Step 3 — Fit table

One row per capability:

| Capability | Existing module | `file:line` | Owner of the state or lock | Fit | Limiting constraint | Cost or risk to adapt |
|---|---|---|---|---|---|---|

**Fit** is one of:

- `use as is` — covers the capability under this problem's constraints.
- `adapt` — covers it after a named change.
- `pattern only` — the approach transfers, the code does not.
- `not found in these searches` — nothing surfaced. List the searches.

A shared verb is not a fit. Before writing `use as is`, name one constraint of the module that could break the fit and check it against the problem: scope (one clone, one machine), ownership (who else writes this state), side effects (does it reset or mutate its target), and what supervises it. A claim mechanism that is local to one clone, or a variation runner that resets its target repo, is `adapt` or `pattern only` for a problem that crosses that line.

The **owner** column is there to stop a second authority: if an existing lock, ledger or queue already owns the responsibility, the row names it, and the composition extends that owner.

## Step 4 — Connect the dots

Close with four short parts:

- **Composition:** which existing owner carries which capability, and how they join.
- **New remainder:** what no existing module covers. This is the only part that needs designing.
- **Unknowns:** what was not read or could not be confirmed, any `not stated` heading from step 1, and what would settle each.
- **One next action:** a single hand-off, not a menu.

End with **Files opened**: the paths actually read, as distinct from searched. It lets a reader check any citation against what was opened. In two recorded runs each table carried one citation to a file that was searched but not opened, so check before relying on a row.

Absence is always worded as "not found in these searches", with the searches listed, in the opening line and the summary as well as in the table. "This repo has nothing that does X" is the same claim without its bound; do not write it. A bounded search is not proof that nothing exists. If no capability has a candidate, say so plainly and stop; do not stretch a weak match into a fit.

## Hand off, do not build

This skill writes no code, no plan document and no ledger row. Output goes to chat, or to an issue comment when the operator asks. Name one next step:

- `recon` — trace the chosen owner before changing it.
- `ponytail` — shrink the new remainder.
- `sanity-check` — when the search shows the problem itself is in doubt.
- `dry` — when the search turned up paths that already duplicate each other.
- `consult` — when the table will drive a build decision: a reader with no session history says the table back under the same three headings as step 1. A mismatch is a signal to investigate, not a verdict.
- `/idea` or `start-task` — to file or start the work.

Do not run the neighbours automatically.

## Rules

- Say the problem back, then capabilities, then searches. No search runs on the problem's own name alone.
- Both directions: capabilities to modules, then the map's subsystems back to the problem.
- Every dismissal names its source line or says `inferred`.
- Maps, then index, then grep; state the mode.
- No unread candidate in the table; every row cites `file:line`, and every cited file was opened.
- Every `use as is` names the constraint that was checked.
- "Not found in these searches", never "does not exist".
- Read-only.
