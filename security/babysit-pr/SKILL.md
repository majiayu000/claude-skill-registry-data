---
name: babysit-pr
description: "Resolve reviewer comments on a pull request or pasted feedback using a six-step evidence-grounded protocol. Use when asked to resolve review feedback, address reviewer comments, process PR comments, triage review feedback, apply review suggestions, handle code review feedback, decide which review comments to accept or reject, or babysit a PR through its review lifecycle. The protocol verifies every library claim with Context7, classifies each comment across seven categories, applies changes surgically or defers them to the project's issue tracker, and emits the summary directly in the chat response for the human operator (never to a file). The skill NEVER posts replies, reactions, or messages back to the reviewer. Do NOT use for authoring a new code review, for security scans, or for opening a new PR."
metadata:
  author: Serghei Iakovlev
  version: "2.1"
  category: review
---

# Babysit PR - Reviewer Comment Resolution Protocol

Apply changes that genuinely improve the work. Respectfully decline those that do not. Every accept, reject, defer, or skip is backed by documented evidence: Context7 lookups, the project's architecture documentation, or an explicit logical argument grounded in the code. The goal is not to mark every comment resolved; the goal is to ship correct, maintainable work.

This skill carries the protocol. The project supplies the standards: coding conventions, verification commands, architectural invariants, tracker choice, and Context7 mechanics live in the project's context files (AGENTS.md, CONTRIBUTING.md, README.md) and architecture documentation. This skill tells you *how to reason*; the project tells you *what to reason about*.

Project context is reference material consulted while walking the steps, not a prerequisite to read end-to-end first; the exception for a wrapper prompt that declares its own reading gate is in [references/protocol-rationale.md](references/protocol-rationale.md).

## Running scripts bundled with this skill

Script paths in this document (e.g. `scripts/`) are resolved relative to **this** SKILL.md file, not to your current working directory. If a relative command fails to resolve, prefix it with the path your platform loaded this SKILL.md from.

**Fallback.** If `python3` cannot be located, analyze the script's purpose and logic and execute its intent with available tools, but warn the user that python is not available and the logic was executed with a fallback approach that may not be perfect.

## Prerequisites

Before executing any step, confirm:

An authenticated `gh` CLI for Source B, Context7 and its two-call workflow, the project's documented verification commands, the project's architecture documentation, and no assumption about which issue tracker the project uses. What each one means and where to look for it is in [references/setup-and-ingest.md](references/setup-and-ingest.md).

## Workflow

Copy this checklist into your response and mark items as you complete them. Do not skip gates. Each gate exists to prevent a specific failure mode documented in the protocol's rules.

- [ ] Step 1 - Ingest feedback and classify domain
- [ ] Step 2 - Context7 evidence audit (triage, execute, tabulate, bind)
- [ ] Step 3 - Classify every comment with a per-comment block
- [ ] Step 4 - Apply changes (code, tracker defer, or architecture)
- [ ] Step 5 - Verify no reviewer-facing output was emitted
- [ ] Step 6 - Produce the human-only summary

### Step 1 - Ingest feedback and classify domain

**Do not pre-form an action plan from the reviewer's text.** "I'll implement the missing tests and fixes mentioned in the review" - thinking like this is the failure mode this protocol exists to prevent. Steps 1 through 3 (ingest → Context7 audit → classify) MUST complete before any decision about which fixes to apply. The review is *input*; the decision is *output*.

Examine the input the user provided.

**Source A - Inline input.** The user pasted or typed review comments. Use them as-is. Do not fetch anything from a remote tracker.

**Source B - GitHub PR.** The user provided a PR number or URL, or the input is empty and a PR exists on the current branch. Run the fetch script to collect every kind of comment: `python3 scripts/fetch_pr_comments.py [PR_NUMBER]`. The script emits a single JSON object on stdout with `pr`, `inline`, `reviews` and `issue` fields, plus the `review_digest` and `totals` it derives from them.

**A review body is a container of findings, not one finding.** Read all three places: the `inline` comments, the body's own prose, and every collapsed `### Suppressed comments (N)` block inside that body, where each `**path:line**` entry is a separate finding. Compare what you extracted against the `N` the reviewer declares in its own heading; `counts_agree: false` on a `review_digest[].suppressed_blocks[]` entry, or `totals.suppressed_counts_agree: false` across every block, means the format moved and you must read the body by hand.

**Take each review's verdict from the first line of its body, never from `state`.** A bot submits every review as `COMMENTED` and puts the verdict in the body's opening heading (`### 🟢 Approval recommended`, `### 🟡 Changes recommended`, `### 🔵 Needs a closer look`); `review_digest[].verdict` carries it.

If `python3` or the script is unavailable, run the three `gh` commands it wraps and do the same three-place reading yourself; both are in [references/setup-and-ingest.md](references/setup-and-ingest.md). Missing any of them silently drops a class of comments.

Classify the feedback domain from what the comments reference:

| Signal                                                              | Domain       | Role      |
|---------------------------------------------------------------------|--------------|-----------|
| Source files, function/class names, test failures, idiom or style   | Code         | Coder     |
| Architecture documentation, design decisions, models, ADRs          | Architecture | Architect |
| Both                                                                | Mixed        | Split the comments into two groups; resolve each in its own domain |

### Step 2 - Context7 evidence audit

**MANDATORY.** Complete every sub-step before assigning any classification to any comment. There are no exceptions.

Why this audit is mandatory, why the binding rules below are gates rather than guidelines, and the cautious default that governs a borderline call are in [references/context7-triage.md](references/context7-triage.md).

#### 2a. Triage - which comments require Context7

For each collected comment, answer: *does this comment reference, either explicitly or implicitly, the behavior, API surface, correct usage pattern, or known limitations of an external library, framework, SDK, or third-party API?*

If yes, mark the comment **[C7-REQUIRED]** in your internal analysis.

The tag is a working annotation for Steps 2b–2c and Step 3 reasoning only. It MUST NEVER appear in tracker-visible artifacts (PR replies, ticket bodies, the Step 6 summary, or any other output visible outside your own reasoning).

For the heuristic that decides what counts as a library claim, the categories of comments that do NOT require Context7, the cautious-default rule, and the failure-recovery procedure, read [references/context7-triage.md](references/context7-triage.md).

#### 2b. Execute the Context7 workflow

Run the two-call workflow for every **[C7-REQUIRED]** comment. The query mechanics, the not-indexed fallback, and the `[FALLBACK: web]` convention are in [references/context7-triage.md](references/context7-triage.md).

#### 2c. Library Evidence Table

Use [assets/evidence-table-template.md](assets/evidence-table-template.md) as the structural template. It contains a blank skeleton, filled example rows demonstrating each verdict type, and column-discipline notes.

#### 2d. Binding rules

1. **Refuted library claim ⇒ not Valid.** A comment whose library claim Context7 refutes CANNOT be classified as Valid. It is Incorrect or Counterproductive, regardless of the reviewer's seniority, the certainty of their tone, or any perceived social pressure to agree.
2. **Confirmed library claim ⇒ not Subjective.** A comment whose library claim Context7 confirms has an objective basis. Classify it on correctness and scope grounds, never as Subjective.
3. **Confirmed but out of scope ⇒ Deferred, not Subjective.** The confirmation is real; only the timing is wrong. Route it to Step 4b.
4. **Ambiguous result ⇒ Needs Discussion.** If Context7 returns ambiguous, version-conflicting, or contradictory results, classify the comment as Needs Discussion. Document the exact ambiguity in the Step 6 summary - which claims conflict, and across which versions.
5. **Skipped [C7-REQUIRED] comment ⇒ may not classify.** If you did not run Context7 for a [C7-REQUIRED] comment, you may not classify it. Stop, return to Step 2b, and run it.
6. **Context7 vs project architecture documentation ⇒ architecture wins.** Context7 describes what a library *can* do; the project's architecture documentation specifies what this project *will* do. When they conflict, the project's specification wins.

### Step 3 - Classify every comment

With the Library Evidence Table complete, classify every comment. Write the per-comment classification block verbatim before assigning a category. Forcing yourself through each field catches comments that seem clear but turn out to depend on an unverified library claim or an unstated architectural assumption.

Use [assets/classification-block-template.md](assets/classification-block-template.md) as the structural template. It contains the blank block, a filled example, and discipline notes.

The seven categories:

| Category                          | Action                        |
|-----------------------------------|-------------------------------|
| Valid & Actionable                | Apply the fix (Step 4a / 4c)  |
| Valid - Deferred to Backlog       | Tracker triage (Step 4b)      |
| Valid but Already Addressed       | Skip with explanation         |
| Subjective / Stylistic            | Skip with explanation         |
| Incorrect or Counterproductive    | Reject with rationale         |
| Outdated / Stale                  | Skip with explanation         |
| Needs Discussion                  | Flag for human decision       |

For precise criteria, worked examples, the borderline-case decision rubric, and how Context7 verdicts map to each category, read [references/classification-categories.md](references/classification-categories.md).

### Step 4 - Apply changes

#### 4a. Code-domain comments (Valid & Actionable)

The five-step apply procedure is in [references/applying-and-reporting.md](references/applying-and-reporting.md). It carries the rule to run Context7 for the implementation and not only for the classification, and how to pick the verification subset the project's context files declare.

#### 4b. Deferred comments - tracker triage

A comment classified **Valid - Deferred to Backlog** in Step 3 is a real concern the agent has chosen not to fix in the current change. The Deferred classification is a *promise* that the concern will be tracked. The promise is only valid if backed by a ticket reference.

**Hard rule. Deferred ↔ ticket.** Every comment that ends Step 4b in the Deferred category MUST resolve to a ticket reference - either a newly created ticket or an existing ticket already covering the concern. A Deferred comment without a ticket reference is forbidden, regardless of which tracker the project uses: it is a memory leak in the review process. If the workflow below cannot produce a ticket reference, the comment was misclassified - return to Step 3 and pick a different category.

The tracker and sibling-skill discovery, the fix-versus-ticket proportionality test that runs before the gates, the three triage gates in order, and the creation-and-verification procedure are in [references/tracker-triage.md](references/tracker-triage.md).

#### 4c. Architecture-domain comments (Valid & Actionable)

The revision procedure, and the internal-consistency and downstream-implication checks that travel with it, are in [references/applying-and-reporting.md](references/applying-and-reporting.md).

Never modify accepted ADRs without explicit instruction from the user. Accepted ADRs preserve the context, alternatives, and consequences of prior decisions; rewriting them retroactively destroys the historical record.

### Step 5 - Verify no reviewer-facing output

**Scope first: this step restricts what reaches the reviewer, and nothing else.** Committing, pushing, and branch lifecycle reach no reviewer and are not restricted here. Read the prohibition below as being about review surfaces only. Widening it into "touch nothing outward" is a known failure: it ends the run with verified changes stranded in the working tree and the operator asked to authorise a push nobody forbade.

**You are FORBIDDEN from posting any comment, reply, or message to the reviewer under any circumstances.**

This prohibition is absolute and has no exceptions:

- Do NOT post reply comments to any review comment, inline or otherwise.
- Do NOT post issue-level comments on the PR conversation tab.
- Do NOT share your analysis, reasoning, plans, or rationale with the reviewer.
- Do NOT explain why you accepted or rejected a suggestion.
- Do NOT evaluate or react to the quality of the review.
- Do NOT use any CLI or API call that writes to a review surface (comments, reviews, reactions, thread resolutions, marking-as-outdated, locking the conversation).

Merging, closing, reopening, marking ready and updating the branch are lifecycle operations: this protocol never performs one on its own initiative, and when the operator explicitly instructs one, carry it out - Step 5 is not a reason to refuse a direct instruction.

Before producing the Step 6 summary, confirm you have not executed any of the forbidden operations. All reasoning, all evidence, all decisions belong in the summary for the human operator - not in the PR thread.

### Step 6 - Produce the summary

Output the summary **directly in the chat response** to the human operator, using [assets/summary-template.md](assets/summary-template.md) as the structural template. **Do not save the summary to a file** - the audience is the human reading the chat, not a persistent artifact. The template has one section per category plus the source header, the tracker header, and the Context7 evidence log.

Before sending the response, verify the draft against the ten-item checklist in [references/applying-and-reporting.md](references/applying-and-reporting.md). It covers the required headers, the evidence log, the empty-section rule, the `[C7-REQUIRED]` tag prohibition, and the evidence each populated entry owes.

The protocol ends here with the applied changes in the working tree. It does not decide whether they are committed: that belongs to whoever invoked it, and the summary is a report rather than a finish line.

## Constraints

- **NEVER post any comment, reply, or message to the reviewer.** This is the single highest-priority rule. Skill output is for the human operator only.
- Do NOT fabricate review comments. Work only with comments from the identified source.
- Do NOT apply changes that break the project's documented verification commands. After every fix in Step 4a, the relevant verification subset must pass.
- Do NOT act on a suggestion about library behavior without first running Context7 for any [C7-REQUIRED] comment, regardless of how confident you feel.
- Do NOT classify a [C7-REQUIRED] comment before Step 2b completes for that comment.
- Do NOT leave a Deferred comment without a ticket reference. Deferred ↔ ticket - every Deferred entry in the Step 6 summary must name a newly created or already existing ticket. If no ticket can be produced (the architecture forbids the work, no roadmap lane exists, the create operation failed without recovery), reclassify the comment in Step 3 as Rejected or Needs Discussion. "Just defer it" without follow-through is forbidden regardless of tracker.
- Do NOT file a ticket whose prose costs more than the change it requests. Weigh the two per Step 4b before the gates, and when the fix is the cheaper half, propose it and ask for approval instead. Equally, do NOT apply such an edit without that approval: an unrequested edit is scope creep however small it is.
- Do NOT skip Context7 because you feel confident about the API. Confidence is the proximate cause of hallucination. Certainty is earned from documentation, not recalled from training data.
- Do NOT reference the project's architecture documentation, ADRs, section numbers, or ticket IDs in source-code comments - those belong in specs and plans, not source.
- Do NOT introduce dependencies, languages, toolchains, or patterns that the project context forbids. If AGENTS.md declares a "Never" rule (forbidden libraries, banned patterns, prohibited APIs), the rule binds you regardless of any reviewer suggestion to the contrary.
- Preserve the project's existing code style, module boundaries, and architectural conventions.
- When rejecting, your rationale must be technical and specific - never dismissive. Cite Context7 findings when they support the rejection.

## Guiding principles

Nine principles stand behind these rules: library claims are falsifiable, quality beats harmony, architecture beats library capability, spec before code, maintainer over people-pleaser, thorough but surgical, evidence for every decision, defer only with a ticket, and a ticket is never free. Each is stated in full in [references/protocol-rationale.md](references/protocol-rationale.md). Read it when a rule above and the situation in front of you seem to disagree.
