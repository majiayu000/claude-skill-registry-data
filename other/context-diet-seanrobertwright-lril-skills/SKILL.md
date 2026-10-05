---
name: context-diet
description: Audit and prune CLAUDE.md and other instruction files using progressive disclosure — move situational content out of every-session context into path-scoped rules, skills, nested CLAUDE.md files, or referenced docs, and delete what the codebase already tells Claude. Use when a CLAUDE.md is long or bloated, when startup context is too full, when instructions are being ignored, when asked to prune, trim, slim, shrink, audit, or restructure CLAUDE.md / project instructions / memory files, or when the user says "context diet", "my CLAUDE.md is too big", or asks to reorganize instructions into .claude/rules or .claude/references.
---

# context-diet

Shrink what loads into **every** session down to what is genuinely needed in
every session. Everything else moves to a mechanism that loads only when it is
relevant — or gets deleted because the codebase already says it.

The unit of value is not "CLAUDE.md got shorter." It is **eager tokens
removed** while the instruction remains reachable at the moment it matters.

## Non-negotiables

1. **Never emit `@path` imports.** Imported files are expanded into context at
   launch. An `@import` shortens the file on screen and saves nothing. If the
   target already has them, report them as false economy and offer to convert.
2. **Never apply without approval.** Write the plan, wait, then apply.
3. **Back up before writing.** Always, even inside a clean git repo.
4. **Safety-critical rules stay in root CLAUDE.md**, however situational they
   are. Only root CLAUDE.md is re-injected after `/compact`.
5. **Never delete silently.** Every deletion is an itemized line in the plan.
6. **Report in eager tokens, not lines.** Lines are not the cost.

## Pipeline

Run the phases in order. Do not skip Phase 2 — unverified pruning is guessing.

### Phase 0 — Discover and measure

```
python <skill>/scripts/discover.py --root <project-dir> [--json-out .claude/.context-diet]
```

Finds every file that can enter context: root and ancestor `CLAUDE.md` /
`CLAUDE.local.md` / `.claude/CLAUDE.md`, nested subdirectory `CLAUDE.md`,
`~/.claude/CLAUDE.md`, `~/.claude/rules/`, `.claude/rules/`, the managed-policy
file, resolved `@imports`, auto-memory `MEMORY.md`, and the names/descriptions
of installed skills. It classifies each as **eager** (every session) or **lazy**,
segments the eager markdown into offset-addressed blocks, and writes
`inventory.json` + `blocks.json`.

Report the eager total up front. That number is the thing being reduced.

### Phase 1 — Read the landscape

Read the eager files in full. Read `.claude/rules/` and `~/.claude/rules/` to
spot content duplicated between a rule and CLAUDE.md. Read the skill
descriptions from the inventory — do **not** extract a procedure into a new
reference when an installed skill already covers it; that is a delete, not a
move. Read `MEMORY.md` to find facts Claude already learned on its own that
CLAUDE.md is redundantly restating.

### Phase 2 — Gather evidence

For every block, verify its claims against the actual repo before judging it.
See `references/taxonomy.md` for the check-per-claim table. Minimum:

- **Commands** — does that script exist in `package.json` / `pyproject.toml` /
  `Makefile`? Does the binary resolve?
- **Paths** — does the directory or file still exist?
- **Libraries / frameworks** — present in the manifest, and actually imported?
- **Scope and frequency** — how many files would this rule apply to? Count
  them. A rule matching 12 of 900 files is a path-scoped rule; a rule matching
  most of the repo stays put.

A block whose claims fail verification is **stale**, which is a deletion
candidate, not a relocation candidate. Say so explicitly.

### Phase 3 — Judge

Apply the routing tree in `references/mechanisms.md`, in order. Every block
gets exactly one verdict: `KEEP`, `RULE`, `REFERENCE`, `SKILL`, `NESTED`,
`DELETE`, `ARCHIVE`, or `ASK`.

Use `ASK` freely. "As small as defensible" means each removal must be
defensible — when the evidence is ambiguous, ask rather than guess.

The criticality gate runs **first** and overrides everything: see
`references/mechanisms.md#criticality-gate`.

### Phase 4 — Write the plan

Write `.claude/context-diet-plan.md` in the exact format in
`references/plan-format.md`. It is machine-parsed on apply, so the syntax is
not optional.

Then give a short chat digest: eager tokens before → projected after, block
counts per verdict, and every `ASK` stated as a real question.

Stop. Wait for approval. The user may edit verdicts in the plan file first.

### Phase 5 — Apply

```
python <skill>/scripts/apply.py --root <project-dir>
```

Block offsets are only valid against the exact bytes Phase 0 read. If any
source file changed since — you edited it, or a plan was already applied —
`apply.py` refuses and tells you to re-run `discover.py`. Do that and rebuild
the plan; do not work around it. Applying stale offsets cuts the wrong bytes
and can silently remove a safety-critical rule.

Backs up every file it will touch to `.claude/.context-diet/backups/<stamp>/`,
performs all writes transactionally (restores on any failure), rewrites the
managed pointer index inside CLAUDE.md between its HTML-comment markers, and
writes `manifest.json` recording every block's origin and destination.

### Phase 6 — Verify

```
python <skill>/scripts/verify.py --root <project-dir>
```

Checks that no block vanished (offset accounting against `blocks.json`), that
every pointer path resolves, that every `paths:` glob **matches at least one
real file** — a typo'd glob silently matches nothing and the rule never loads —
that every generated skill has a description, and that no `@import` was
introduced. Report measured before/after eager tokens.

Fix anything it flags before declaring done.

## Writing pointers

A reference is only worth extracting if Claude reliably fetches it later. That
depends entirely on the pointer sentence. State the **trigger**, not the topic:

- Bad — `See .claude/references/deploy.md for deployment info.`
- Good — `` Before deploying, running any `vercel` or `gh workflow` command, or editing CI config, read `.claude/references/deploy.md`. ``

Formula: *`Before/when <observable trigger>, read <path>.`* If you cannot name
a concrete trigger, the content probably belongs in a path-scoped rule (which
needs no pointer) or should be deleted.

## Re-running

Treat existing state as input, not as settled. Start with:

```
python <skill>/scripts/reaudit.py --root <project-dir>
```

It reports what is checkable from disk: extracted content that has **drifted**
back into eager context, **dangling** pointers, **orphaned** references nothing
points at, rules whose globs **match nothing** (so they never load),
**regrowth** against the token count recorded at the last apply, and pointers
with **no concrete trigger**.

Then run the normal pipeline from Phase 0, treating existing rules, skills, and
references as part of the landscape.

**On "should this come back into CLAUDE.md?"** — how often Claude actually
reads a given reference is *not observable from disk*, and neither this skill
nor its tooling can measure it. `reaudit.py` flags pointers whose trigger is
broad enough to fire most sessions, which is a proxy and nothing more. Present
those to the user as a judgement call and say why you are unsure. Do not assert
a frequency you cannot know.

## Reference files

- `references/mechanisms.md` — how each loading mechanism actually behaves, the
  routing decision tree, the criticality gate, and the `/compact` caveat.
- `references/taxonomy.md` — content categories, the default verdict for each,
  and the evidence check that settles it.
- `references/plan-format.md` — the exact plan file syntax that `apply.py` parses.
