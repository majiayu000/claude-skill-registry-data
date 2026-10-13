---
name: skill-improve
description: "Improve a skill using a test-fix-retest loop. Runs static checks, proposes targeted fixes, rewrites the skill, re-tests, and evaluates actual semantic/check regressions before a scoped keep or guarded revert."
argument-hint: "[skill-name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash
---
Read and apply `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`,
`standards/evidence-lifecycle.md` and `standards/notes-adr-sync.md` for scoped
authority, exact evidence and decision ownership. Existing named authority
continues; analysis is read-only and report-only excludes input/index/state writes.


## User Guide

- When to use: Improve a skill using a test-fix-retest loop. Runs static checks, proposes targeted fixes, rewrites the skill, re-tests, and evaluates actual semantic/check regressions before a scoped keep or guarded revert.
- Inputs: Command arguments: `/skill-improve [skill-name]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Proposed skill patch, before/after test comparison, and optional improvement evidence written only after user approval.
- Memory-bank writes: Only when Memory Bank is initialized and each named write effect is covered: `memory_bank/t3_archive/skill_testing/improvements/skill-improve-[name]-[YYYY-MM-DD].md`. Retest coverage is updated by `/skill-test`.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Determine the target skill's advertised domain capability before improving it.
`[Both]` below describes an artifact supporting both domains, not a project-domain
enum. Project routing uses concrete Game or Product scope, or unresolved Unknown,
under `standards/technical-preferences.md`.
- **[Game]** when the skill primarily supports game workflows, preserve game examples, player/gameplay/engine terminology, playtest references, and game CDD templates.
- **[Product]** when the skill is expected to support general projects, add product branches for API/CLI/web/data workflows, technology stack terms, user value, and product evidence.
- **[Both]** prefer dual-domain sections over replacing one domain with another.

Never delete game examples while improving a skill. Move them to `[Game]` / `[游戏专用]` sections if they no longer fit the shared path.
# Skill Improve

Runs an improvement loop on a single skill:
test → fix → retest → keep or revert.

---

## Phase 1: Parse Argument

Read the skill name from the first argument. If missing, output usage and stop:

```
Usage: /skill-improve [skill-name]
Example: /skill-improve tech-debt
```

Verify `skills/[name]/SKILL.md` exists. If not, stop with:
"Skill '[name]' not found."

---

## Phase 2: Baseline Test

Run `/skill-test static [name]` and record the baseline score:
- Count of FAILs
- Count of WARNs
- Which current checks failed or warned (Check 1–8)

Display to the user:
```
Static baseline:   [N] failures, [M] warnings
Failing: Check 4 (no ask-before-write), Check 5 (no handoff)
```

If baseline is 0 FAILs and 0 WARNs, note it and proceed to Phase 2b.

### Phase 2b: Category Baseline

Look up the skill's `category:` field in
`skill_testing/catalog.yaml`.

If no `category:` field is found, display:
"Category: not yet assigned — skipping category checks."
and skip to Phase 3.

If category is found, run `/skill-test category [name]` and record the category baseline:
- Count of FAILs
- Count of WARNs
- Which specific category rubric metrics failed

Read the current category metrics in `skill_testing/quality-rubric.md`; match the
reported baseline to those actual metric owners before diagnosing a fix.

Display to the user:
```
Category baseline: [N] failures, [M] warnings  ([category] rubric)
```

If static/category have no findings, verify applicable existing spec assertions
and affected semantics before saying NO CHANGE. Structural scores alone do not
prove behavioral correctness; disclose unexecuted runtime cases and unavailable
required checks. Do not manufacture improvements or call a skill perfect.

---

## Phase 3: Diagnose

Read the full canonical skill file at `skills/[name]/SKILL.md`.

For each failing or warning **static** check, identify the exact gap:

- **Check 1 fail** → which frontmatter field is missing
- **Check 2 fail** → how many phases found vs. minimum required
- **Check 3 fail** → no verdict keywords anywhere in the skill body
- **Check 4 fail** → actual scoped-authority behavior is missing/contradictory;
  keyword absence alone is not a failure of a valid shared-contract implementation.
- **Check 5 warn** → no follow-up or next-step section at the end
- **Check 6 warn** → `context: fork` set but fewer than 5 phases found
- **Check 7 warn** → argument-hint is empty or doesn't match documented modes
- **Check 8 fail/warn** → actual required dual-domain behavior is missing/ambiguous.

For each failing or warning **category** check (if category was assigned in Phase 2b),
identify the exact gap in the skill's text. For example:
- If G2 fails (gate mode, full directors not spawned): skill body never references all 4
  PHASE-GATE director prompts
- If A2 fails: the authoring skill writes effects outside named authority or
  ignores actual unresolved choices/explicit per-section preferences. A valid
  named multi-section approval must not be failed for avoiding repeated questions.
- If T3 fails (team, BLOCKED not surfaced): skill doesn't halt dependent work on blocked agent

### Phase 3b: Dual-Domain Parity Diagnosis

Read the full skill, actual advertised scope and applicable owner bodies, using
`standards/technical-preferences.md` domain/capability evidence. Markers help
locate material but cannot establish parity or trigger invented feature scope.
Evaluate actual context, actions/output and handoff for Game and Product where
supported. Valid substantive behavior before line 50 is sufficient; preserve all
Game examples. Record real gaps and inaccessible/omitted required inputs rather
than treating keywords/line counts/last-line quotes as full-reading proof.

Record the diagnosis:

```markdown
Dual-domain parity:
- Game branch preserved: [PASS / FAIL]
- Product routing only: [YES / NO]
- Product context reads: [PASS / MISSING]
- Product steps/checks: [PASS / MISSING]
- Product output/next steps: [PASS / MISSING]
- Recommended fix: [add Product branch / expand Product output / update docs only]
```

Show the full combined diagnosis to the user before proposing any changes.

---

## Phase 4: Propose Fix

Write a targeted fix for each failure and warning. Show the proposed changes
as clearly marked before/after blocks. Only change what is failing — do not
rewrite sections that are passing.

For dual-domain parity fixes:
- Add Product sections beside existing Game content.
- Do not delete, shorten, or genericize game examples.
- Do not create a separate product-only slash command.
- Reuse existing Product paths: `design/cdd/`, `design/ux/`, `docs/architecture/`, `production/qa/`, `production/releases/`, `tests/`, and `docs/reference/<stack>/`.
- Prefer a focused additive patch over a broad rewrite.

Before writing, reuse the exact authority for canonical changes, corresponding
platform projections and rollback, or ask once after presenting the concrete
patch and full effect list. Review every actually changed output and ownership
conflict. Unexpected or other-owner files stop the affected update until their
exact treatment is separately authorized. Preserve unrelated content and never
independently author derived platform files. Never invent a per-skill generator
flag, command or API; verify a proposed interface and its complete effect scope
against the actual authoritative Source before using it. If the required Source,
comparison or write coverage is unavailable, retain the candidate and request only the
missing scope. Declined writes mean NO CHANGE.

---

## Phase 5: Write and Retest

Retain recoverable snapshots of the exact invocation baseline bytes/full hashes
for the canonical skill, every potentially changed platform projection and
necessary owner inputs.
Capture expected after identities for this writer's effects. Before applying,
confirm live inputs still equal the bound baseline; stop on other-author drift.

Write only covered canonical effects and their reviewed deterministic platform
projections. Apply the approved delivery only after all changed-path and ownership
checks above pass. Recheck all current eight static checks and assigned category
metrics against the same scope, plus affected existing spec/semantics.
Retests are writer checks, not independent review. Required independent review
uses a fresh exact baseline after edits; unavailable review remains pending.

Display the comparison:
```
Static:   Before [N] failures, [M] warnings  →  After [N'] failures, [M'] warnings
Category: Before [N] failures, [M] warnings  →  After [N'] failures, [M'] warnings  (if applicable)
Combined change: improved / no change / worse
```

---

## Phase 6: Verdict

Compare individual current checks and actual behavior, not only aggregate counts.
A lower FAIL/WARN count cannot hide any new required failure, lost Game/Product
behavior, authority gap or unresolved significant decision. Apply the six
`standards/notes-adr-sync.md` dispositions; Accepted decisions/scoped exceptions
are required before affected implementation. Continue independent work.

**IMPROVED:** verified intended gaps fixed with no new required regression and
selected workflow's required independent review satisfied. Disclose runtime
execution limits; a score gain alone does not establish IMPROVED.
**NO CHANGE:** no approved change, no verified improvement, or affected verification
still pending (state the retained candidate/live outcome precisely).

For a permitted rollback, first verify each live touched canonical/adapter equals
this invocation's exact after identity and actual owner-input identities,
projection rules and complete output scope still match. Other-author changes
stop affected restore; never overwrite them or use
`git checkout`. Reuse scoped rollback authority or ask only when absent. Restore
the exact retained invocation before bytes, and restore only covered deterministic
platform effects after a fresh complete-output plan with no unrelated drift.
Verify restored identities.
**REVERTED** means the exact covered restore actually succeeded. Preserve failed
candidate/evidence; rollback does not grant independent approval or completion.

---

## Phase 6b: Optional Improvement Evidence

After the keep/revert decision, reuse exact improvement-record authority; ask only
for missing/new report effects after displaying the record:

"May I write the improvement record to
`memory_bank/t3_archive/skill_testing/improvements/skill-improve-[name]-[YYYY-MM-DD].md`?"

Write only the covered record (or established fallback when Memory Bank is absent).
The record must include:
- Skill name and path
- Baseline static/category result
- Diagnosis summary
- Patch summary
- Retest static/category result
- Keep/revert decision
- Follow-up recommendation

Do not update `memory_bank/t3_archive/skill_testing/coverage-index.yaml` here.
That index is maintained by `/skill-test` when retest evidence is approved.

---

## Phase 7: Next Steps

- Run `/skill-test static all` to find the next skill with failures.
- Run `/skill-improve [next-name]` to continue the loop on another skill.
- Run `/skill-test audit` to see overall coverage progress in `memory_bank/t3_archive/skill_testing/coverage-index.yaml`.

Improvement evidence uses separately named report authority and exact before/
after dependencies; report-only/review-only never fixes inputs or updates coverage.
Memory Bank absence uses the established fallback without activation. `/skill-test`
owns separately authorized coverage updates; include no implicit index/state effect.
