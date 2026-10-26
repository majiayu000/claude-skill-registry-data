---
name: write-conventions
description: "Use when a project's conventions need to be written down or extended: starting a codebase from scratch, settling how one tier uses its framework, capturing a design decision that was just made, or turning unwritten patterns in an existing repo into rules. Produces or grows an AGENTS.md / CLAUDE.md. Any language or stack."
---

# Project conventions

**A convention document is the set of decisions a fresh agent would otherwise guess differently every time**, as short checkable rules in the repo's `AGENTS.md` (or `CLAUDE.md`, whichever the repo uses; `AGENTS.md` if neither).

## What earns a rule

**All five hold, or the candidate is dropped, naming the one that fails.**

1. **Contested**: a competent developer could defensibly do it the other way.
2. **Recurring**: a one-off belongs in a code comment.
3. **Consequential**: breaking it costs rework or silent drift.
4. **Checkable**: a reviewer can point at a line and say yes or no.
5. **Not tool-enforceable**: what a linter, formatter or type checker can enforce is configured there.

**Never a rule**: formatting, casing, import order, line length; a restated general principle; an aspiration with no test; code that does not exist yet.

## Rule shape

```
N. **MUST <imperative>.** <the cost of not doing it, or where it lives.> <optional: one path or symbol.>
```

- **Two or three sentences, under 50 words.** MUST for invariants, SHOULD for strong defaults.
- **The real symbol, path or command**, never a paraphrase of the idea.
- **Every rule states its cost**: a rule whose reason is invisible gets rationalised away.

<Good>
`2. **MUST derive DB-row types from Drizzle, never hand-write them.** Use `typeof <table>.$inferSelect`, or the aliases exported from the project's db package. Hand-written copies drift from the schema silently.`
</Good>

## Modes

- **bootstrap**, a new codebase. Read the stack first: the foundation reference when the project has a roadmap, its boards in aiview, any conventions file present. Ask only what none answers, through the `interview` skill, on the decision points that stack forces (`decision-points.md`). Write an `## Architecture (context you must not break)` section and the rules the answers produce. Stop at 5 to 8: rules written before the code are guesses.
- **harvest**, an existing codebase. Read the source and recent history for patterns followed but unwritten, and for places the codebase contradicts itself. Propose each with its evidence: the files that comply and the ones that do not. A pattern with no counter-example may not need writing down. A pattern broken in three places is a rule or a mistake: say which.
- **capture**, a decision just made. Run the five filters, write it in the shape, place it in its section.

## The vendor's own docs

**Before rules for a stack not yet codified, read its makers' guidance, official domain only, and note the major version read.**

- **The docs yield candidates**, which still face the five filters.
- **Cite the URL in the rule.** A rule that departs from official guidance says so and why.
- **Where the docs are silent, say so and decide on the merits.**
- **A framework with a catalogue at `references/framework-<name>.md`** (`references/framework-angular.md` today): read it after the stack catalogue, when that tier is about to get real. A framework without one gets a catalogue first: per fork, the official URL, the major version read, and two lines that let someone who does not know the framework judge it.

## Placement and numbering

- **Numbering is append-only**: `AGENTS EXCEPTION (rule 11)` markers in the code point at numbers.
- **Run `node scripts/rules.mjs` before writing a rule and before saying a marker holds**: it prints the rules, the next free number and every marker with the rule it cites, exit 1 on a marker citing no rule or on a duplicate number.
- **Group under the headings the document already uses**; a new heading waits for its third rule.
- **Two clauses near the top of every document, once.** The escape hatch: a rule may be deviated from at a specific site with a comment beginning `AGENTS EXCEPTION (rule N):` and the reason; without one, deviation is a review finding, and so is a marker whose reason does not hold. The capture clause: a decision made during a session that would pass the five filters is said in chat before the session ends, and written only on the person's yes.

## Output

**Show the exact markdown block and where it goes; apply on confirmation.** A proposal that contradicts an existing rule names its number, and superseding is the person's decision.
