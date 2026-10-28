---
name: doc-hygiene
description: How to write and prune a document an agent reads — a root or package `CLAUDE.md`, a `SKILL.md`, or anything reached by a pointer. Use when adding to one, when deciding whether material belongs inline or behind a pointer, when a document has grown and needs cutting, or when drafting a plan — a `PLAN.md`, an `IDEAS/` roadmap, or a gameplan in chat.
---

# Doc hygiene

Every document here is read by an agent before it is read by a person, and the two want opposite things. This is the method for deciding what a document carries, where it sits, and what comes out of it. The vocabulary is adapted from Matt Pocock's `writing-for-agents` ([mattpocock/skills](https://github.com/mattpocock/skills)); the numbers were measured here.

## The two loads

Every document and every pointer spends one of two budgets, and naming which one is what makes the trade decidable.

**Context load is always-loaded material** — the root `CLAUDE.md`, a skill's `description`, anything in the window every turn — and it is spent whether or not it fires. **Cognitive load is the cost on a person**: which documents exist, and when to reach for each. That second one is not a cost to minimize. It is the price of human agency, so spend it where judgment matters and remove it where it does not.

Material behind a pointer escapes context load and pays the pointer's own line instead. **A skill is still a document**: `.claude/skills` is in `doc-audit`'s corpus, so a path, an id or an Invariant it cites is graded like one cited anywhere else, and `fli check`'s `skill-pointer` resolves every skill name the root `CLAUDE.md` gives to a `SKILL.md` whose frontmatter agrees. Material with no pointer at all rides entirely on cognitive load, which is how a document nobody remembers quietly stops being true.

**Measured: the root `CLAUDE.md` was 254 KB**, about 63k tokens on every turn of every session. § Live hazards and § Bridge index were 57% of it and neither is read by anything but a person; both are skills now. The file has grown again since (new drives, new packages) — check its current size rather than trust a number here.

**What Claude Code loads, and when** ([memory docs](https://code.claude.com/docs/en/memory)):

- **A package `CLAUDE.md` is context load for its package.** It loads the first time a file in that directory is READ, then stays. So the root owes nothing a package file already carries.
- **The target is under 200 lines per file**, because a longer one lowers adherence as well as costing tokens.
- **Instructions earlier in a file are followed better** (IFScale, arXiv 2507.11538). Put the rules and commands first and the routing table last.
- **A block-level HTML comment is stripped before injection**, and a comment inside a code fence is kept. That is where a section only a PARSER reads goes: it stays at its path for the reader and costs the agent nothing. `packages/litestone/CLAUDE.md`'s layout is the example — `fli done`'s `layout-named` reads it raw. Keep `--` and code fences out of the comment.
- **An overview does not help an agent find files, and an instruction is obeyed whether or not it is still true** (Gloaguen et al., arXiv 2602.11988). A layout map earns visible space only where it names an owner. A rule earns its line by naming the test that pins it, because a stale rule gets followed too.

## The ladder

Three rungs, ranked by how immediately the agent needs the material.

1. **In-file step** — what to do, in order.
2. **In-file reference** — consulted on demand. A flat peer set of rules is a fine arrangement, not a smell.
3. **Disclosed reference** — its own file behind a pointer, loaded only when the pointer fires.

**A path-scoped rule is the third rung with a mechanical trigger.** `.claude/rules/*.md` with `paths:` globs loads when a matching file is READ, so it fires without a pointer being worded well — and does not fire while a new file is being written, which is why `code-style.md` keeps its first-write half in the root `CLAUDE.md`. An import line in a `CLAUDE.md` is not a rung at all: it loads at launch.

**A skill loads WHOLE when it fires, so a catalog skill is an index with `references/` beside it.** `SKILL.md` carries one line per entry — the rule, or the seam with its owner — and the section's reference file carries the mechanism, the measurement and the ruling, so a turn needing one hazard reads the index and one file. Measured: the three hazard skills and `bridge-index` loaded 185 KB per firing as prose and 29 KB as indexes. A new entry is a line in the index AND a paragraph in its reference file. Whether the files are reached is `bun run skills:reach`, which reads the session transcripts Claude Code already keeps: per skill, the sessions that loaded it and the reference files opened.

**What decides the rung is branching, not size.** Inline what every branch needs; disclose what only some branches reach. A `@@softDelete` trap costs nothing on a turn spent in sierra and everything on the turn it is needed, which is why the hazards split by realm rather than by weight.

**The pointer's wording decides whether the material is reached; its target does not.** A must-have document behind a weakly worded pointer is a variance bug — sharpen the wording first, and inline the material only if sharpening fails. Front-load the word that does the triggering, give one trigger per genuinely distinct branch, and cut the identity the body already carries.

Where the ladder decides how far down a piece sits, **co-location decides what sits beside it** once there: a term's definition, its rules and its caveats under one heading, so reading one part brings its neighbors with it.

## What cannot move

**A section a program parses is a source of truth and moves only with its parser.** Modules read the root `CLAUDE.md` by path — `invariants.js` the numbered list, `repo-map.js` and `repo-atlas.js` the package table, `doc-audit.js` the invariant count — and `DRIVES.md` by the path `proofs.js` owns, for both of its tables. Moving a table without its reader is a green build over a table nothing reads any more; moving it WITH the reader is the ladder's third rung applied to parsed material, which is how the drive tables left the always-loaded file (60% of it, and branch-only: a turn that proves nothing never needs them).

That is also the case the cache rule below gets wrong on first look. The drives table restates every `verify:*` script that is already in `example/package.json`, so it reads as a copy of the environment. It is not one: `preflight.js` parses the column beside them, and there is nowhere else that column lives.

## The four cuts

- **The delete test**, which `PHILOSOPHY.md` § VII states for a document sentence and House style states again for a code comment: if it vanished, could someone acting on this file make a mistake it would have prevented? For a document an agent reads there is a sharper form of the same question — does this change behavior against the model's default? A line the model already obeys pays load to say nothing. That form is model-relative rather than reader-relative, so two people disagreeing about it disagree about the default and settle it by running the document rather than by arguing. When a sentence fails, delete the whole sentence rather than trim words out of it.
- **Cache.** The environment is a source of truth too — `package.json` scripts, a config file, `--help` output — and a document that restates a one-command lookup is a copy that goes stale with nothing failing. Cache what cannot be found by looking: the unwritten convention, the reason behind a choice, the gotcha no config confesses.
- **Negation.** Steering by prohibition drags the forbidden behavior into context and makes it more available, not less; the ban half-reads as an instruction to do the thing. State the target behavior instead, so the banned one is never spoken. A prohibition earns its place only as a guardrail that cannot be phrased positively, and then it is paired with the positive.
- **Sprawl.** A document simply too long, with every line live and unique. Attention thins across the excess, and every extra line is one more to keep true. The cure is the ladder rather than the blue pencil.

**A restatement made at three sites is a word waiting to be coined.** This repo already does that well — *drive*, *realm*, *seam*, *pivot*, *residue*, *ladder* each carry a paragraph in one token — so the work is hunting the passages that have not collapsed yet, not adding vocabulary. A word too weak to beat the default is itself a no-op, and the fix is a stronger word rather than a different technique.

## A plan's shape

**A plan is Phases of Steps** (`FJS-D927`). This applies to a `PLAN.md`, to a roadmap in `IDEAS/`, and to a gameplan drafted in chat.

```md
### Phase 2 — Writes to pixels

Goal: one line, the outcome.
Done when: the command, drive or measurement that proves it.

- [x] 2.1 Crop with handles and aspect
- [ ] 2.2 Rotate and flip
  - What the step found goes indented under it.
- [~] 2.3 Touch drags — dropped: the reason
```

- **Phases count from 0.** Phase 0 is the groundwork: scaffolding, measuring the original, reading the source. Every phase ends in something checkable, and that check is its `Done when:` line.
- **A step is about one commit of work and is cited `phase.step`**, so `2.3` means the same thing in a memory, a commit and a chat. Its box is `[ ]` open, `[x]` done or `[~]` dropped, and a dropped step says why. A phase with one piece of work has one step.
- **A number is a citation key, issued once.** A step inserted later becomes `2.3a`, new work is added at the end, and a dropped step keeps its number. Open questions follow the same rule as `Q1`, `Q2` and so on, and a ruling cites a question by its `Q` number.
- **The next step is the first open box.** Frontmatter `status:` holds § VII's lifecycle word, and the position is read off the boxes. A finished phase gets one paragraph after its steps, starting **Done <date>.**, that says what it found.
- **A plan is read on every turn of a session, so it stays under 32 KB** (`plan-size`, `FJS-1562`). A finished phase keeps its heading, steps and **Done** paragraph; its found-record, answered questions and ticked detail move verbatim to `docs/plan-done.md` with a one-line stub under the heading, so `Q` and step numbers still resolve. A reader takes one section with `fli outline PLAN.md '<heading>'`.
- **Order is spelled Phase and Step.** *Tier* is priority: Tier 1 comes first, and the order inside a tier is free. *Wave* is a batch of independent items run in parallel. Outside its plan, a phase is named with the plan it belongs to, as in *darkroom Phase 2* (`FJS-D395`).
