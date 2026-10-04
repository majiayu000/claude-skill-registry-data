---
name: kanso-nuclear
description: Use when the user asks for a nuclear review, a thermonuclear audit, a deep maintainability sweep, a structural audit of the whole codebase, or a "harsh" pass on a branch. Stricter and more structural than /kanso-audit.
argument-hint: "[scope: all|diff|branch|path] [--fresh]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(gh *) Bash(rg *) Bash(find *) Bash(wc *)
---

# kanso-nuclear

A structural review that refuses to approve code on the grounds that it works. Where `/kanso-audit` checks correctness, clarity, consistency, and architecture, this skill is single-minded about *structure*: whether the change makes the codebase harder to scan a year from now.

The principles from `kanso-principles` apply, and the standing rule of this skill sharpens them: **delete complexity before you move it**. A refactor that rearranges the same difficulty is not a refactor — it's relocation.

## Always run inline

Findings, the approval gate, refactor handoffs, and the verify result all stay in the calling chat so the user can see them and act on them.

### Exception: `--fresh` for Phase A only

Append `--fresh` to push the investigation into a read-only subagent (prefer the `Explore` agent type — read-only by construction). If the harness has no read-only subagent, say so in one line and run Phase A inline; `--fresh` degrades gracefully. The findings come back as Phase A's output; Phases B (proposal), C (apply), and D (verify) continue inline. Whole-skill `context: fork` is deliberately not used — only Phase A benefits from fresh context. Use this when the current session has already touched the code — fresh context cuts the anchoring on prior decisions in the transcript. On `all`-mode runs over large repos, `--fresh` is usually the right default to keep the main chat readable.

## Resolve the scope

`$ARGUMENTS` selects:

- *(empty)* or `all` → the whole codebase. The marquee invocation.
- `diff` or `branch` → commits on the current branch vs upstream or `main`.
- a path like `src/billing/` → everything under that path.

If `diff` mode finds nothing staged or committed, fall back to the last commit and tell the user.

Before any review:

- Shape of the repo: `!git ls-files | wc -l`
- Largest files first (they are the most likely Phase B targets): `!git ls-files | xargs wc -l 2>/dev/null | sort -rn | head -20`
- Voice calibration: `!git log -n 20 --oneline`
- Existing conventions: read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, linter configs

A finding that contradicts established repo style is noise, not signal.

## What this skill looks for

Five structural smells, in priority order. Each is its own category in the findings list.

### 1. Missed simplification ("judo")

The whole change can be reframed so entire branches, helpers, modes, or layers disappear — not just shrink. Ask: is there a path that uses the existing architecture more directly and makes the change feel inevitable in hindsight? Push for that path rather than polishing what's there.

Bias hard toward deletion of complexity. Rearrangement is a consolation prize.

### 2. File sprawl

A file growing past a healthy size — kanso's rule of thumb is ~600 lines for tight modules, ~1,000 for established ones — earns a question, not a pass. The question is: should this be decomposed before the new code lands? Waive only when the resulting file is genuinely cohesive and the alternative split would be artificial.

The threshold matters less than the *crossing*. A file that was 980 lines and is now 1,400 deserves the question even if the absolute count was already large.

### 3. Spaghetti growth

New conditionals scattered into unrelated flows. One-off branches threaded through code that doesn't otherwise care about the feature. Booleans and nullable modes added to functions whose contracts they muddy. These are design failures, not stylistic nits — the logic belongs in its own abstraction, state machine, policy object, or module.

Phrase findings as "this change makes the surrounding code harder to reason about", because that is the harm.

### 4. Abstraction theatre

Thin wrappers, identity helpers, single-implementation factories, pass-through layers, generic mechanisms hiding simple data shapes, casts and optionality papering over unclear invariants. Indirection is only worth its keep if it makes the caller clearer. When it doesn't, it's overhead pretending to be architecture.

Silent fallbacks (`try/catch` returning `null`, default values that mask missing data) get flagged as **boundary problems** when the invariant should be explicit. Tightening such a boundary is a behaviour change — tag accordingly.

### 5. Wrong-layer logic

Feature-specific code leaking into shared modules. Implementation details bleeding through APIs. Bespoke helpers where the codebase already has a canonical one. The fix is rarely "make it better here" — it's "move it to where it belongs". Push for the canonical home.

## The questions to ask of every change

- Is there a judo move that deletes whole branches instead of moving them?
- Did the diff add concepts the reader has to hold in their head, or remove them?
- Did a previously cohesive module become more coupled or more stateful?
- Are repeated conditionals signalling a missing model?
- Is this abstraction earning its keep, or just adding a layer?
- Did this change introduce optionality, casts, or `any` that obscure the real contract?
- Is the logic in the canonical layer, or has it leaked across a boundary?

If the answer to any of these is "yes, and it's avoidable", the finding belongs in the report.

## Report format

One tight markdown document. No preamble, no apology.

```markdown
# Nuclear audit: <short scope description>

**Scope:** <all | diff | path> · **Files:** <n> · **Findings:** <n> judo, <n> sprawl, <n> spaghetti, <n> theatre, <n> wrong-layer

<Two lines. Lead with the highest-leverage structural issue in plain language. Name the judo move if one exists.>

## Findings

[1] `src/billing/charge.ts:55-188` — new validator block tangled into the canonical charge flow; lives more naturally as a separate policy (spaghetti, refactor)
[2] `src/auth/session.ts:120` — silent fallback to anonymous when `verify()` throws hides a real invariant (theatre, behaviour-change)
[3] `src/api/user.ts:14` — `UserDataResultWrapper` wraps one field and adds no clarity (theatre, refactor)
[4] `src/foo/bar.ts:1-1420` — file grew from 870 to 1,420 lines on this PR; the new sync logic extracts cleanly (sprawl, refactor)
```

One line per finding. Format: `[N] \`path:line\` — <what's wrong>, <one-line remedy> (<category>, <shape>)`. Use the category names above (`judo`, `sprawl`, `spaghetti`, `theatre`, `wrong-layer`).

Order findings by category in the priority order listed under "What this skill looks for". Don't pad the report with cosmetic nits while structural issues exist. Density beats coverage.

**Shapes** (same vocabulary as `/kanso-audit`):

- `refactor` — fix preserves behaviour for every input the code already handles. Routes to `/kanso-refactor`.
- `behaviour-change` — fix alters output under some input (e.g. removing a silent fallback, tightening a contract). Applies inline only after explicit opt-in.

When in doubt, tag `behaviour-change`.

### When there are behaviour changes

After the findings list, add a short paragraph per behaviour-change finding so the user knows what would actually shift:

```markdown
## Behaviour changes — your call

[2] `src/auth/session.ts:120`: today, a failed `verify()` returns the anonymous user. Removing the fallback means callers see the real auth failure — almost certainly the right call, but it is a real shift and may break callers that depended on the implicit anonymous path.
```

One paragraph each. Plain language. Numbered to match the findings list. Skip the section entirely when no behaviour-change findings exist.

### When the diff is clean

```markdown
# Nuclear audit: <scope>

**Findings:** none

The diff holds up under the nuclear rubric. <One sentence on the most ambitious thing the author got right.>
```

No approval gate. End of turn.

## The approval gate

If there is at least one finding, end the report with:

```
Apply fixes? (<r> refactor, <b> behaviour-change)

  y                — run /kanso-refactor on the refactor findings
  y + behaviour    — run /kanso-refactor, then apply behaviour changes inline
  behaviour-only   — apply behaviour changes inline; skip refactor
  pick 1,3         — apply only those (routed by shape)
  edit             — amend the proposal
  n                — stop, leave the report in the transcript
```

Adapt the list to what's actually present. A bare "yes" never silently applies behaviour changes — it routes to refactor only when both shapes exist.

Routing on apply follows `kanso-audit`'s approval-gate rules (`../kanso-audit/SKILL.md`) exactly: refactor-shaped fixes go to `/kanso-refactor audit-report` inline, behaviour-change fixes apply inline one at a time with a re-read before each edit, and the two never share a commit.

## Phase D — Verify

After fixes land, run the project's verification command and paste the exit code. Command discovery order and the pass/fail/no-command report blocks are defined once, in `kanso-refactor`'s Verify section (`../kanso-refactor/SKILL.md`) — follow them exactly, and also check CI config for a verification job worth mirroring locally.

Narrowest command that covers the touched files. On fail, roll back or escalate — don't iterate silently. If no command exists, say so explicitly and list what was checked. Never silent-skip.

## Tone

Direct. Demanding about structure. Not rude.

If the code is making the codebase messier, say so plainly. If the author missed a dramatic simplification, say that too. Softening a major maintainability issue into a polite suggestion is its own failure mode. The user invoked this skill expecting friction — give them friction worth the invocation.

Critique the code, not the author. "This pushes a coherent module into incoherence" is fair. "You wrote spaghetti" is not.

## What this skill never does

- Run via Agent or Task tool, or dispatch any part of itself to a subagent — except Phase A under `--fresh`, which dispatches the investigation only.
- Edit files before the user has approved the proposal block.
- Skip the approval gate when there is at least one finding.
- Apply refactor-shaped fixes directly. That's `/kanso-refactor`.
- Apply behaviour-change fixes on a bare "yes". Behaviour changes need explicit opt-in.
- Mix refactors and behaviour changes in one commit.
- Run tests during Phase A. Verification happens in Phase D.
- Claim a fix is complete without a Phase D result — pass, fail, or explicit "no command found".
- Pad the report with cosmetic nits while structural findings exist.
- Approve code on the basis that the tests pass and the behaviour looks correct.

## Failure modes to avoid

- Producing 40 findings, half of them nits, when the PR has two real structural problems. Density beats coverage.
- Tagging a behaviour change as a refactor to slip it past the gate. When in doubt, tag `behaviour-change`.
- Recommending a rearrangement when a deletion is possible. Judo first.
- Soft-pedalling the file-size question because "the file was already large". The smell is the crossing, not the absolute count.
- Running on `all` mode without first sampling the largest files — the report misses its highest-leverage findings.
- Flagging style preferences that aren't in any style guide. The rubric is about harm, not taste.
- Letting the tone slip into rudeness. Critique the code; the author is not the target.

## Lineage

The general idea — an uncompromising structural review distinct from a normal code audit — is one Cursor's team has also written a skill for. This isn't a port. The rubric, voice, priority order, scope defaults, and apply path are kanso's own; the convergence is on the problem, not the implementation.
