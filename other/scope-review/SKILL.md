---
description: >-
  Five-step adversarial scoping for a contested fix, in-flight feature, or
  underspecified spec. Maps existing work, grounds the question in the
  codebase, runs first-principles critique, steelmans against own suggestions,
  then synthesizes outstanding product/engineering questions with multiple-
  choice product questions ready to forward to non-engineering stakeholders.
  Use when a PR has conflicting reviewer feedback, an "obvious" fix has
  hidden tradeoffs, a spec hasn't been pressure-tested, or a greenfield
  decision will become locked-in.
  <triggers>
    /scope-review, scope this work, scope the work, review this proposal,
    review the spec, first principles review, what's ambiguous, what could
    fail, steelman this, what questions should we answer, gray areas in this,
    pressure-test this proposal, what are we missing, scope before we build
  </triggers>
---

# Scope Review

Adversarial scoping for a proposed change. Use when a fix or feature has more uncertainty than initially obvious. Output is a structured report ending with forwardable product questions and locked-in engineering decisions.

## When to use

- PR with conflicting reviewer feedback or contested approach.
- "Simple fix" that touches load-bearing logic.
- Spec or proposal that hasn't been pressure-tested.
- Architectural decision being made under time pressure.
- Greenfield work where defaults will become locked-in semantics.

## When not to use

- Trivial change with no architectural surface (typo fix, single-line bug).
- Scope already locked and the user wants execution, not deliberation.
- User explicitly asked for implementation, not review.

## Process

The five steps are sequential. Each depends on the previous. Do not skip ahead.

### Step 1 — Map the work landscape

Before evaluating any proposal, understand what work already exists around this question. Categorize related work:

- **Complete** — already shipped (recent commits, recently-merged PRs in adjacent code).
- **Incomplete but ticketed** — in-flight work that affects the question (other PRs, JIRA tickets in same area, draft commits on related branches).
- **Unticketed** — behavior the question depends on that nobody has formalized.

Tools:

- `git log --oneline --all -- <path>` for history on the affected files.
- `gh pr list --search "<topic>"` for in-flight PRs.
- JIRA / ticket-tracker search for related tickets.
- `grep` for `TODO`, `FIXME`, `XXX`, deprecation notices in the affected area.
- Look for migrations affecting the same tables in the last ~6 months. Migrations signal architectural direction even when no ticket exists.

Then run `/audit` on the work landscape itself: are gaps and grey areas formally tracked, or invisible?

**Output:** list of related work items with status, plus one paragraph naming what is NOT formally tracked.

### Step 2 — Ground the question in the codebase

The proposal lives in code. Read it. Specifically:

- The exact file/function the proposal modifies (current state and proposed diff).
- The callers (read paths).
- The writers (write paths).
- The data the code produces or consumes (schema, migrations, seed data).
- Tests covering the affected code.
- Any feature flags gating the affected paths.

**Resist abstract evaluation.** The codebase usually contains evidence that invalidates abstract objections. Examples to watch for:

- A table being decoupled in a near-future migration → architectural direction already chosen.
- Missing writers → a "regression" can't manifest because the code path isn't live yet.
- Feature flag off in production → behavior change is gated and reversible.
- Greenfield models with no production data → migration cost is zero.

Check the data state. If the affected models have no production rows, "expensive backfill" objections collapse.

**Output:** 5-10 concrete findings, each citing file path and line. Flag any finding that materially changes how the proposal should be evaluated. Distinguish "speculative" from "verified" findings.

### Step 3 — First-principles review of the proposal

With the work landscape and codebase grounding in hand, critique the proposal:

- **Ambiguous** — what does this proposal mean exactly? Where would two readers disagree?
- **Underspecified** — what does it not say that it needs to say?
- **Failure modes** — what concrete scenarios break the proposal?
- **Unstated assumptions** — what is the proposal assuming that may not be true?
- **Premise check** — does the proposal solve the right problem, or a tangent?

Critique what's written, not what you imagine was meant. Cite specific lines of the proposal where ambiguity or failure lives. If the proposal is a PR, cite file:line. If it's a spec, cite section.

**Output:** numbered list of issues. Each issue cites the part of the proposal it applies to and includes a concrete failure scenario where applicable.

### Step 4 — Steelman against your own suggestions

Whatever fixes or alternatives surfaced in step 3 — argue against each one as strongly as a hostile reviewer would. Look for:

- **Hidden costs** — migration size, blast radius, team churn, ongoing maintenance.
- **False premises** — "this assumes X but X may not be true."
- **Latent regressions** — solves stated problem but reintroduces a different one.
- **Architectural debt** — works now, gets worse over time.
- **Scope creep** — suspiciously close to a different ticket, or balloons the PR.
- **Cosmetic fix** — appears principled but doesn't change behavior at the layer that matters.

Each steelman should be strong enough that you'd take it seriously coming from a reviewer.

**The point is to find the option you can't kill.** That is the strongest move. If every option dies, the proposal is broken at the premise — say so explicitly and return to step 3.

**Output:** per-option rebuttal. Mark any option that survives steelmanning as a candidate.

### Step 5 — Synthesize outstanding questions

The previous steps surfaced unknowns. Categorize them:

#### 5a. Product / compliance / legal questions

These require non-engineering input. Each must be:

- A plain-language scenario with named participants, dates, and concrete numbers.
- Multiple-choice — typically 2-4 options labeled (A), (B), (C), (D).
- Each option must have engineering implications spelled out so the answerer understands the cost of their choice.
- Forwardable as-is to a non-engineering stakeholder.

**Bad:** "What should the behavior be when configurations differ?"

**Good:** "Alice is a part-time employee. From Jul 2025 through Dec 2025 she worked 800 hours under config A. From Jan 2026 through Jun 2026 she worked 300 hours under config B. The eligibility rule (1000 hours / 12 months) is byte-identical across both configs. Should she be eligible? (A) Yes, hours additive. (B) No, reset on swap. (C) Depends on amendment type — needs new flag."

#### 5b. Engineering decisions

Internal decisions that don't require external input. List as decisions with:

- The choice space (numbered options).
- A recommended default with one-sentence justification.
- Tradeoffs per option.

#### 5c. Investigations needed

Concrete next actions that would resolve a remaining unknown without requiring product or major engineering deliberation. Each item names a file to read, a query to run, or a person to ask.

**Output:** three labeled lists. Anything urgent that blocks the current PR is flagged. Defaults are stated for everything that has one.

## Final report structure

When all five steps complete, deliver a single report:

1. **Work landscape** — 1 paragraph + list of related items.
2. **Codebase grounding** — 5-10 findings with file paths.
3. **Critique** — numbered issues.
4. **Steelmen** — per-option rebuttal, surviving option(s) called out.
5. **Outstanding questions** — three lists (product / engineering / investigation).

## Output files

When step 5 produces non-trivial product or engineering questions, write them to disk as raw markdown using the templates in `templates/`. Do not paste the questions into chat as the primary deliverable — they need to be forwardable as files.

### Product questions file

Use `templates/product-questions.md`. Replace `{{TOPIC_TITLE}}`, `{{ONE_PARAGRAPH_CONTEXT}}`, scenario fields, and per-option engineering implications. Output filename: `{{ticket-or-topic-slug}}-product-questions.md` at repo root (or a designated docs path if the project has one).

Each product question must be a self-contained scenario with named participants (Alice, Bob), concrete dates, concrete numbers, and 2-4 multiple-choice answers each annotated with engineering implications. The recipient must be able to answer without follow-up questions.

### Engineering questions file

Use `templates/engineering-questions.md`. Replace `{{TOPIC_TITLE}}`, the related-work links, the decisions table, and each decision's detail block. Output filename: `{{ticket-or-topic-slug}}-engineering-decisions.md` at repo root (or designated docs path).

Every code reference in the engineering file must be a **GitHub permalink with a fixed commit SHA**, not a branch-relative URL. To construct permalinks:

```bash
SHA=$(git rev-parse HEAD)
# https://github.com/{ORG}/{REPO}/blob/{SHA}/{path}#L{N}-L{M}
```

For PR-branch-only code, use the PR head SHA from `gh pr view {PR_NUM} --json headRefOid`. PR links use the form `https://github.com/{ORG}/{REPO}/pull/{NUM}` without `/files` suffixes (those lock to a specific patch chunk that moves on rebase).

Pair both files — a product-questions file without an engineering-decisions file is incomplete, and vice versa.

## Examples

The `examples/` directory pairs BAD vs GOOD outputs for each step using a real running scenario. Refer to these to calibrate the level of specificity, citation density, and structural rigor expected. Specifically:

- `examples/step-1-work-landscape.md` — citations vs vague summaries.
- `examples/step-2-codebase-grounding.md` — verified findings with paths vs plausible-sounding speculation.
- `examples/step-3-critique.md` — numbered issues with file:line citations and concrete failure scenarios vs unfalsifiable critiques.
- `examples/step-4-steelman.md` — per-option rebuttals reaching verdicts vs listing tradeoffs in the abstract.
- `examples/step-5-synthesis.md` — forwardable product questions and tabulated engineering decisions vs to-do lists.

## Anti-patterns

- **Skipping step 1.** Reviewing a proposal without understanding what's already in flight produces conflicting recommendations and duplicates work already underway elsewhere.
- **Skipping step 2.** Critique without codebase grounding generates objections that the code or migrations have already invalidated. Always check whether the regression you're worried about can actually occur given current data state.
- **Skipping step 4.** Producing options without steelmanning produces options that look principled but die on contact with a reviewer. The user (or a real reviewer) will steelman for you if you don't.
- **Vague product questions.** "What should the behavior be?" is unanswerable. Concrete scenarios with named participants, dates, hours, and consequences-per-answer are answerable.
- **Treating step 5 as a punt.** The synthesis is a deliverable. You must answer engineering questions that don't need product input, even if you'd rather defer. The output should reduce open questions, not catalogue them.
- **Re-evaluating the same option twice.** When step 4 kills an option, drop it. Don't reanimate it in step 5 unless new information surfaces.
- **Confusing "scoping" with "deciding".** This skill produces a structured decision matrix. The user makes the actual decision based on the matrix. Do not pre-empt their judgment by collapsing the multiple-choice answers into a single recommendation unless asked.

## Caveman mode

If caveman mode is active, the report body uses caveman compression. Product questions in step 5a stay in plain English regardless — they're forwardable to non-engineers and clarity wins over compression for that audience.
