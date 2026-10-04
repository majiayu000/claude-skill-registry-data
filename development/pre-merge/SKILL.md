---
name: pre-merge
description: "Primary pipeline review step after verified implementation. Use to create a PR with lineage and run architectural review before merge. Not for QA intake, planning, or implementation work."
sources:
  secondary:
    - "Software Requirements — Karl Wiegers & Joy Beatty"
    - "The Checklist Manifesto — Atul Gawande"
    - "Continuous Delivery — Jez Humble & David Farley"
    - "The Twelve-Factor App — Adam Wiggins"
    - "Release It! — Michael Nygard"
    - "Growing Object-Oriented Software, Guided by Tests — Freeman & Pryce"
    - "Domain Modeling Made Functional — Scott Wlaschin"
    - "Noise: A Flaw in Human Judgment — Daniel Kahneman, Olivier Sibony & Cass Sunstein"
    - "Best Kept Secrets of Peer Code Review — Jason Cohen"
    - "Engineering a Safer World — Nancy Leveson"
---

# Pre-Merge

Create a GitHub PR linking back to the PRD and slice issues, then review the full diff against the project's architectural principles. Produces advisory findings — does not block merge, auto-fix code, or file issues.

## Invocation Position

This is a primary pipeline skill used after implementation has been verified and before merging to main, *or* when picking up someone else's PR for review.

Use `/pre-merge` when the branch is ready for PR creation, architectural review, and final plan-to-code reconciliation. Use `/pre-merge --pr <number>` when you are reviewing a PR you did not author.

Do not use it as a substitute for implementation verification, QA intake, or refactor planning. It assumes the work is already built and ready to review.

## Modes

`/pre-merge` runs in one of three modes. All three reuse the architectural review dimensions defined in `review-checklist.md`; they differ in what they consume and what they produce.

- **Author-mode (default)** — invoked on your own branch with no `--pr` argument. The skill creates the PR (Phase 2) and prints findings to the terminal as advisories (Phase 4), then hands back there — **it makes no fix commits of its own and opens no second pass.** This is the mode auto-invoked by `/execute` Step 6 on the HITL path. **What it reads is decided by branch state, not by a flag:** a first review reads the whole branch; a re-run against a PR that already carries a review-currency stamp, whose head has since moved, takes the post-stamp delta — the commits after the stamped SHA — as the review's *subject*, and does not re-read what the earlier review covered. Phase 1 step 4 makes that decision and prints it. The delta is the subject, not the limit of what a reviewer may read: `review-checklist.md` settles what a reviewer reads, and that includes the tree around the delta.
- **Reviewer-mode** — invoked as `/pre-merge --pr <number>` against a PR you did not author. The skill skips PR creation (the PR already exists) and produces *draft comment text* (Phase 4) for you to review and post, structured per `references/comment-craft.md` (5P gate, Triple-R, Comment Signals, MMG Exchange).
- **Loop-mode** — invoked as `/pre-merge --loop`, or entered automatically when `/execute` hands off on an AFK run. Runs Phases 1–4 as author-mode does, except Phase 1 step 4's scope decision: loop-mode always reads the whole branch and never takes the post-stamp delta, then continues into **Phase 5**: it records every finding in a durable ledger on the PR, attaches the evidence that supports or refutes each one, and hands back to the operator. Findings stop being terminal output in this mode; they become durable rows with owners. **Loop-mode does not fix anything and makes no commits** — the operator decides what happens to each finding (see Phase 5 § Why the loop does not fix).

**Loop-mode's exit condition is that every finding has an owner — never that the review came back clean.** "Zero findings" is a *forbidden* termination signal, consistent with Phase 4's existing minimum-findings guard, which was written because a near-empty review on a non-trivial diff means the review stopped early rather than that the code is flawless. A loop that terminates on clean reviews will reliably produce clean reviews and nothing else (Meadows, *Seeking the Wrong Goal*; Leveson: never reward low incident counts — reward reporting itself).

If you are running on a branch other than the user's working branch and `--pr` was not provided, ask once whether the user means reviewer-mode against a specific PR number rather than guessing — auto-detection saves a keystroke but misclassifying mode produces draft comments that would have been local advisories or vice versa.

## When to Use

- **Author-mode:** after QA passes and before merging a feature branch to main; after Ralph finishes AFK execution and you've verified behavior; or for any branch you want reviewed before merge, even without a full pipeline run.
- **Reviewer-mode:** when a teammate or external contributor opens a PR and you want to apply the full architectural review in `review-checklist.md` to their diff and produce constructive comment text.
- **Loop-mode:** when findings must survive the session that produced them — the AFK handoff from `/execute`, or any branch you will review over several sittings and do not want to re-derive each time. Use it when the cost you are paying is *losing track of findings*, not *making the fixes*.

## Execution Flow

### Phase 1: Gather Context

**Author-mode:**

1. **Ask for the PRD issue number.** Accept "none" if this change didn't go through the full pipeline. **In loop-mode entered from an AFK `/execute` handoff, do not ask** — take the issue number from the handoff (`/execute` Step 6 passes it) and treat its absence as "none". There is nobody to answer, so an unconditional question here would hang the run at its first step.

2. **If a PRD was given:**
   ```bash
   gh issue view <number>
   gh issue list --search "in:body #<prd-number>" --state all --json number,title,state,body --limit 100
   ```
   Parse boundary maps (Produces/Consumes sections) from each slice issue body.

3. **Detect the base branch and assess the diff:**
   ```bash
   BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null | sed 's@^origin/@@')
   if [ -z "$BASE_BRANCH" ]; then
     for candidate in main master prod develop trunk; do
       if git rev-parse --verify "$candidate" >/dev/null 2>&1; then BASE_BRANCH=$candidate; break; fi
     done
   fi
   # A name is not a ref. $BASE_BRANCH names the branch (for `--base`, `git switch`);
   # $BASE_REF points at it, and is the only thing safe as a range endpoint.
   if git rev-parse --verify "origin/$BASE_BRANCH" >/dev/null 2>&1; then
     BASE_REF="origin/$BASE_BRANCH"
   else
     BASE_REF="$BASE_BRANCH"
     echo "note: origin/$BASE_BRANCH does not resolve — measuring against the local branch, which may be stale" >&2
   fi
   git diff "$BASE_REF...HEAD" --stat
   git log --oneline "$BASE_REF..HEAD"
   ```
   For a stacked-PR slice, override `$BASE_BRANCH` with the sibling slice's branch name (the upstream the PR will target) and re-derive `$BASE_REF` from it. If no diff from the base, tell the user there's nothing to review and stop. Do not hardcode `main` — Skill Kit's own repo uses `prod`, and many others use `develop`, `trunk`, or a team-specific name.

   **Residual:** `$BASE_REF` is only as fresh as the last `git fetch`, and on a triangular fork (or a remote not named `origin`) `origin/$BASE_BRANCH` may be absent or track your fork rather than upstream — the `else` branch then falls back to the local branch, which is the stale-ref behavior this guard exists to avoid. It says so on stderr rather than falling back silently, because a plausible wrong answer with no signal is what let this defect live for five months. If the counts look wrong, `git fetch` and re-run, or set `BASE_REF` by hand.

4. **Decide the scope — the whole branch, or the post-stamp delta.** This decision is author-mode only. Loop-mode skips it and sets `SCOPE_FROM="$BASE_REF"` unconditionally, reading the whole branch on every invocation, per Phase 3's loop-mode bullet. A first review reads the whole branch. A re-run against a PR this skill already stamped, whose head has since moved — a `/fix-findings` round, or a hand fix after a deliberate lock deletion — takes the post-stamp delta as its subject. Read the stamp with the same expression `/closeout` Step 2 uses; `scripts/test-review-currency-marker.sh` pins the two byte-identical, and `scripts/test-delta-review-scope.sh` runs this block against a fixture for every branch state it names:
   ```bash
   REVIEWED_SHA=$(gh pr list --head "$(git branch --show-current)" --json body -q '.[0].body // ""' \
     | sed -n 's/.*<!-- reviewed-at: \([0-9a-f]\{40\}\) -->.*/\1/p' | tail -1)
   SCOPE_FROM="$BASE_REF"
   if [ -n "$REVIEWED_SHA" ] \
     && git merge-base --is-ancestor "$REVIEWED_SHA" HEAD 2>/dev/null \
     && [ "$REVIEWED_SHA" != "$(git rev-parse HEAD)" ] \
     && [ -z "$(git log --merges --format=%H "$REVIEWED_SHA..HEAD")" ]; then
     SCOPE_FROM="$REVIEWED_SHA"
   fi
   if [ "$SCOPE_FROM" = "$BASE_REF" ]; then
     echo "review scope: whole branch, from $BASE_REF"
   else
     echo "review scope: post-stamp delta, from $SCOPE_FROM"
   fi
   git diff "$SCOPE_FROM...HEAD" --stat
   git log --oneline "$SCOPE_FROM..HEAD"
   ```
   Four states fall back to the whole branch, each on purpose: no stamp (a first review, or a hand-authored PR); a stamp that is not an ancestor of `HEAD` (the branch was force-pushed and the reviewed commit rewritten away — `/closeout` calls this the *stronger* divergence signal, and it is not a smaller review); a stamp equal to `HEAD` (nothing new to scope to); and a merge commit after the stamp (the post-stamp diff would carry the base branch's own changes, which nobody on this branch wrote). The decision is printed so the terminal readout and the PR say the same thing about what was read.

   **On a delta re-run, the delta is the subject and the tree is still readable.** Brief each Phase 3 reviewer with the findings the post-stamp commits claim to close — the earlier readout in this session, the PR's ledger if loop-mode wrote one, or the commit messages themselves — and with the `/fix-findings` breaker verdicts when there are any. The first question per commit is whether the fix closes its finding at every site the finding named, which is the Fix Completeness dimension; the second is what the new text contradicts nearby, which is the census in `references/restated-claims.md`. Both need the surrounding tree, and the checklist's context contract already grants it; the scope narrows what the review is *about*, never what the reviewer may open.

**Reviewer-mode (`--pr <number>`):**

1. **Fetch the PR and its diff:**
   ```bash
   gh pr view <pr-number> --json number,title,headRefName,baseRefName,body,author,url,state
   gh pr diff <pr-number>
   ```
   If the PR is already merged or closed, tell the user and stop — review comments on a closed PR are surfaced separately and rarely useful.

2. **Identify the PRD issue from the PR body.** Look for `Closes #<n>`, `Refs #<n>`, or a `## PRD` section pointing at an issue. If found, run the same `gh issue view` + slice-issue search as author-mode step 2 to load PRD context and boundary maps. If the PR has no PRD lineage, treat it as the "no PRD" branch — the PRD-gated dimensions skip themselves, each in the phase its `**Runs in:**` marker assigns it to.

3. **Note the diff size and base branch from the PR JSON.** No local branch math — `gh pr diff` returns the merged-base-to-head diff directly. Do not try to check the PR out locally; you are reviewing the diff, not running it.

### Phase 2: Create the PR

**Skip this phase entirely in reviewer-mode** — the PR already exists, you did not author it, and rewriting someone else's PR body is out of scope. Proceed to Phase 3.

1. **Check for an existing PR:**
   ```bash
   gh pr list --head $(git branch --show-current) --json number,url
   ```

2. **Create or update the PR.** Use `gh pr create --base "$BASE_BRANCH"` (override `--base` for stacked-PR slices to the sibling slice's branch) or `gh pr edit`.

**PR body template (when PRD exists):**

```markdown
## Summary

[For trivial PRs — typo fixes, dep bumps, formatting-only, single-line reverts — 1–2 sentences derived from the PRD's Problem and Solution sections.

For non-trivial PRs — behavior changes, new surface area, bug fixes with non-obvious root causes, refactors crossing module boundaries — write a plain-language walkthrough: one paragraph of domain setup, what changed and why each piece was the right move, and why it matters. Aim for a reader who doesn't have the codebase in their head. See `references/writing-for-humans.md` for the shape and revision bar.]

## PRD

Closes #<prd-issue-number>

## Slices

- [x] #N — Title (for closed slices)
- [ ] #N — Title (for still-open slices)

## Key Decisions

[Bullet list of notable implementation decisions that refined or diverged from the PRD. Derived from commit messages and slice issue comments. Omit this section if nothing diverged.]
```

**PR body template (no PRD):**

```markdown
## Summary

[For trivial PRs — typo fixes, dep bumps, formatting-only, single-line reverts — 1–2 sentences derived from the diff and commit messages.

For non-trivial PRs, write a plain-language walkthrough: one paragraph of domain setup, what changed and why each piece was the right move, and why it matters. See `references/writing-for-humans.md`.]
```

3. **Write the `## Review Notes` block, when `/execute` handed one over.** Both the author-mode and loop-mode handoffs pass a block of re-runnable verification claims — which commands ran and their exit status, which tiers were skipped and why, scope absorbed under the Consumes gate, assumptions that shifted, known-weak spots. Emit it verbatim after `## Summary`; do not summarize or re-word it. Its whole value is that the reviewer can re-run the claims, and every summarization hop is a lossy transformation authored by the agent under review. See `/execute` Step 6 for the block's shape.

4. Print the PR URL.

5. **Note that the body gains one more section later.** Phase 4 appends a `## Review Currency` block recording the head SHA the review actually covered. It is written *after* Phase 3 runs, not here — a stamp written at PR-creation time would certify a review that had not happened yet.

### Phase 3: Architectural Review

Consult `review-checklist.md` for the review dimensions and their violation patterns. That file is the roster — its `## N.` headings are the only place the set of dimensions is defined, and nothing here restates it. The dimensions run identically in all three modes; only the `diff` they read differs:

- **Author-mode** — the local `git diff "$SCOPE_FROM...HEAD"`, where Phase 1 step 4 set `$SCOPE_FROM` to `$BASE_REF` (a first review: the whole branch) or to the stamped SHA (a re-run whose head moved: the post-stamp delta). On a delta re-run each reviewer is also briefed with the findings the post-stamp commits claim to close and any breaker verdicts, and reads the tree around the delta as the checklist's context contract allows — the delta is the subject, not the reading limit.
- **Reviewer-mode** — the `gh pr diff <pr-number>` output.
- **Loop-mode** — the local `git diff "$BASE_REF...HEAD"` — the whole branch on every invocation; loop-mode does not take the delta scope. Loop-mode makes no commits, so on a later invocation the diff has moved only if the *operator* pushed fixes; the ledger, not a narrowed diff, is what stops the pass re-reporting settled findings.

**Delegation exists for reviewer independence; parallelism on large diffs is a sub-case of it.** When `/pre-merge` is auto-invoked by `/execute` Step 6 it runs in the session that just wrote the code, holding every rationalization the implementing agent made while writing it. The dimensions are sound; the reviewer is not independent. Cohen's finding is that the author's job is to *annotate for* a reviewer, not to be one — so the sub-agent split below is first a way to put a clean context in front of the diff, and only second a way to halve wall-clock on a big one.

**So delegation is unconditional in all three modes** — the session that wrote the code never reviews its own diff inline. The one exception is drawn by *content*, not size: the four trivial classes Phase 2's two body templates already name — typo fixes, dep bumps, formatting-only changes, single-line reverts — review in-session, and that is the only trivial/non-trivial distinction Phase 3 draws. The exemption covers Phase 3 only; a trivial-class diff large enough to trip Phase 4's minimum-findings guard still delegates there.

Size then decides *how many* sub-agents, never *whether* the review leaves the authoring session:

- **Small diff** (< 200 changed lines, < 10 files): one sub-agent runs every dimension the checklist marks as sub-agent work and whose own gating condition is met — each dimension's section in the checklist states its own gate; the notes below elaborate on a few of them but are not the inventory.
- **Larger diff**: spawn two sub-agents in parallel, splitting that same set between them.

Either way the controller-owned dimensions are outside this choice entirely — diff size decides how many *sub-agents* run, never whether a dimension the checklist withholds from sub-agents gets delegated anyway.

**Why the trigger is content and not size.** Cohen's Cisco dataset retires the proxy on its own evidence: four reviews of 1–2 lines each ran past 15 minutes, because small physical changes carried architecture-sized ramifications. This repo has its own instance — a 34-line, 2-file diff, comfortably inside the old band, whose composition defect the authoring session's pass missed across eight findings and a clean context returned as its top Concern in one pass (`docs/solutions/architecture-decisions/self-review-blind-to-composition-2026-08-13.md`). Deleting the band retires the proxy; the four-class exemption keeps what the band was actually protecting, and is narrower.

**When sub-agents are unavailable**, run the dimensions in-session and name the run **degraded mode** in the findings output: the reviewer holds the authoring session's context, so its independence is gone and the findings should be read accordingly. This is the same declaration `/improve-pipeline` Phase 4 makes when its dialectic cannot be spawned. Degraded mode is a disclosure, not a second exemption — do not reach for it because delegation is inconvenient.

**The context contract is about provenance, not permission.** It has three parts, and the closed list is only the first of them.

**Handed over — the same in all three modes.** The diff, `review-checklist.md`, `references/writing-for-humans.md`, and — when one exists — the PR body's `## Review Notes` block. Nothing else is *given* to a sub-agent, in particular not the implementing session's context. An externally-authored PR reviewed in reviewer-mode has no `## Review Notes` block, because `/execute` never ran on it; that is an absent input, not a missing step.

**Reached for itself — durable state, read at the source.** A dimension's own procedure may send its sub-agent past that list: to the merged tree, the branch's commit history — `git log`, the commit messages, the per-commit diffs — `git show` on a deleted path, the slice or PRD issue body, the package registry, the research archive, an installed `.d.ts`, `docs/solutions/`, a scratch `tsc --noEmit`. The commit history is on that list because two dimensions cannot execute without it: Vertical Slice Integrity is defined entirely over commit structure, and Surgical Scope names the commit messages and branch name as its stated-task source of last resort. It is a separate artifact, not a summary of the diff, so reading it does not touch the rule below. **In reviewer-mode, `gh pr view <n> --json commits` reaches the commit messages and SHAs** without a local checkout; it returns no per-commit diffs, so a pattern that needs them cannot be checked there. That is not an exception to the contract; it is the contract working. Reading a durable artifact yourself is what *preserves* independence — what destroys it is receiving that artifact pre-digested by the session under review. One rule governs it: **read it at its source and cite it, never accept the controller's account of it.** The reviewer reading the diff rather than a summary of the diff is the same rule, applied to the one input that is always present.

**Withheld absolutely — the change's context.** That phrase means the authoring session's working state: its reasoning, the alternatives it discarded, the justifications it assembled while writing the diff, and any controller-authored narration, summary, or paraphrase standing in for something the sub-agent could have read directly. `## Review Notes` is handed over despite being author-written because it is a *checkable* record — `/execute` Step 6 requires commands and exit statuses the reviewer can re-run — and not a construal to inherit.

**What that makes decidable.** A sub-agent can substantiate a finding when the evidence is reachable by a procedure the dimension itself names, from the diff plus durable state of the kind above. It cannot when the finding needs a *view assembled across artifacts* that no single named procedure reconstructs — which is the ground the controller bucket stands on, stated per-dimension in each controller-owned `**Runs in:**` marker rather than as a blanket rule here.

**Loop-mode adds exactly one thing:** from pass 2 on, the *states and evidence* recorded in the ledger, so the pass does not re-report findings the operator already settled. It never adds the previous pass's severity judgments; Phase 5's ledger section gives the full forward/withheld split and the reason for it.

Both reference files are **rubrics** — what to look for, and the bar the resulting prose must meet. The independence contract withholds *the change's context*; it was never about withholding the standards the review is held to.

**The split is derived from the checklist, never restated here.** Every dimension in `review-checklist.md` carries a `**Runs in:**` marker directly under its heading naming exactly one of three owners — `sub-agent A`, `sub-agent B`, or `the controller, in Phase 4` (the checklist's legend defines each bucket's theme). Read the markers and hand each sub-agent the dimensions marked for it. Dimensions marked for the controller are **not** sub-agent work and are not delegated; Phase 4 runs them in-session, where the GitHub state they need is already loaded.

This is deliberately not a list. A hand-maintained copy of the roster sat here and shipped wrong from birth; `scripts/test-review-dimension-partition.sh` carries that incident in its header, and fails on any dimension the canon leaves unassigned.

Each sub-agent reads the full diff and its assigned dimensions from `review-checklist.md`, then returns findings in the three-tier severity format — **each Suggestion and Concern written to the shape and revision bar in `references/writing-for-humans.md`**, which is handed over as a rubric for the finding text even though the doc scopes itself to issue and PR bodies. Observations are exempt, per Phase 4's exemption — not the doc's own when-to-skip list, which exempts artifact classes and reaches no finding. Phase 4 states the bar and the reason for it.

**The reviewer always reads the actual diff, never a summary of it.** A summary is a lossy transformation authored by the controller under review; a fresh context buys independence from *rationalization* and buys nothing against *misreporting* (Leveson: no control system performs better than its measuring channel).

**Gates, thresholds, and per-dimension procedures are stated in the checklist and nowhere else.** Several dimensions fire only when the diff meets their own condition; several carry numeric bands, an exemption, or a named verification procedure. All of it lives under that dimension's heading — hand each sub-agent its assignment and let it read its own gate. A copy here would be a second operative site for the same claim, so changing a band in one file would ship a stale one in the other: the class [references/restated-claims.md](references/restated-claims.md) defines, and the one this skill's own Deep Modules bullet detects. `scripts/test-restated-review-operatives.sh` covers part of this; its header is the one place that states which part, and it is not restated here. Read it before treating a green run as the class being closed.

**TypeScript projects:** `/ts-audit` complements the architectural review with type-safety analysis on changed `.ts`/`.tsx`. Whether it runs depends on the mode:

- **Author-mode and reviewer-mode: mention it, do not invoke it.** For branches with significant `.ts` or `.tsx` changes, note it as an option — "For deeper TypeScript analysis, consider running `/ts-audit` on the changed files" — and leave the decision with the user. This is the deliberate HITL boundary; the scoping below does not move it. A soft "significant" is the right bar here, because the cost of misjudging it is one unnecessary sentence.
- **Loop-mode: auto-invoke it**, and record its findings in the Phase 5 ledger alongside the dimension findings. It is already the recommended next action at exactly this point for exactly these files; the only reason it was ever manual is that nothing drove the cycle. One constraint, because an *invoke* rule needs a decidable trigger where a *mention* rule does not:
  - **Trigger — more than 50 changed `.ts`/`.tsx` lines, or more than 2 changed `.ts`/`.tsx` files**, measured over the diff this pass reads. Below that, skip the audit and record the skip on the ledger's "Checks not run this pass" line rather than passing over it silently — the same rule Review-friendly Size already follows for suppressed size findings. "Significant changes" is a usable instruction for a human deciding whether to *mention* a tool and an unevaluable one for a loop deciding whether to *run* it.
  - Findings it repeats from an earlier pass are matched against the ledger and left as the rows they already have, rather than added twice.

**Verify, don't suspect — library callback semantics, subpath swaps, and provider schema constraints.** When a finding turns on how a library treats a value the application hands it (return from a callback, object passed to a hook, systemMessages/tools/middleware collection semantics), the sub-agent must cite the installed type definition — `node_modules/<library>/**/*.d.ts` file path and line — in the finding. If a research archive entry exists for this feature, prefer its `callback_contracts_snapshot` (see `research/SKILL.md` Phase 1.25). For findings that turn on which subpath of a package an import resolves through — runtime-affecting swaps disguised as type-only diffs across sibling subpaths of multi-runtime packages — prefer the `installed_versions_snapshot` (see `research/SKILL.md` Phase 5b); Boundary Map Contracts' spec-reality check item 2 is the gate that consumes it. For findings that turn on **provider schema constraints when an SDK wraps a provider** — the SDK's type signature accepts a shape (JSON Schema, Zod, tool definitions) that the underlying provider's actual contract rejects (e.g. Gemini's `response_schema` rejecting numeric enums, Anthropic's `tool.input_schema` honoring only a subset of JSON Schema, OpenAI Structured Outputs' schema-subset divergence from JSON Schema 2020-12) — the citation must include the provider's contract docs at the installed SDK version, not only the SDK's permissive `.d.ts`. Hedged language ("if the library replaces X rather than merges", "if this field is accepted", "the SDK lets you pass any schema") without a source citation is not acceptable for this class of finding — the proof is one grep or one provider-docs page away and the failure mode is runtime-invisible. Either cite the source and classify as Observation/Suggestion/Concern per the severity rules, or downgrade to a named follow-up with an explicit "verify before merge" action.

### Phase 4: Present Findings

**Run the controller-owned dimensions first, then combine findings from all dimensions (or sub-agents).**

**Controller-owned dimensions run here, in this session.** Every dimension in `review-checklist.md` whose `**Runs in:**` marker reads `the controller, in Phase 4` is yours to execute — Phase 3 did not delegate it, and no sub-agent could have. The marker is on those dimensions because their procedures need a cross-slice view — the PRD, every slice issue, and the set of merged slices held together at once. Phase 1 assembles exactly that, in this context, which is the whole reason the work lands here.

Read each such dimension's procedure from `review-checklist.md` and run it now. Its findings are ordinary findings: they carry the severity the checklist assigns them, they join the three tiers below, and in loop-mode they get ledger rows like any other. **In particular, a Concern from a controller-owned dimension is still a Concern, named escalation and all** — the relocation moved where the check runs, not what its verdict is worth. There is no tier above Concern; a dimension whose verdict should stop a merge says so by naming that action inside its Concern, which is what Coverage Matrix Reconciliation does for an unmapped Must.

Then run them through the same evidence discipline as everything else: a controller-owned dimension is not exempt from citing what supports it. What it *is* exempt from is the delegated-finding check immediately below, which exists to catch a sub-agent misreporting; there is no sub-agent here.

If a controller-owned dimension gates itself off — Coverage Matrix Reconciliation only fires when this PR closes the last slice of a multi-slice PRD — say so in the findings output rather than skipping silently, the same way Review-friendly Size declares a suppressed size finding. A dimension that reports nothing and a dimension that never ran read identically otherwise, and that ambiguity is exactly what let this dimension go missing for months.

**Check delegated findings against the tree before presenting them.** Delegation removes one failure mode and exposes another: a fresh context buys independence from *rationalization* and buys nothing against *misreporting* (Leveson — Phase 3 says this of summaries, and it holds equally for sub-agent output). Loop-mode already handles it, at Phase 5 Step 2, which records `refuted — <evidence>` when the tree contradicts a claim. Author-mode and reviewer-mode had no equivalent, so a sub-agent's misreport printed as an advisory with nothing between it and the reader. Now that every non-trivial review is delegated, that gap sits on the default path.

So for each delegated finding, run Phase 3's "Verify, don't suspect" rule from this context — the grep, file path, and line that support or refute it; the installed type definition when the finding turns on library semantics — and then:

- **Supported by the tree** — present it, with the evidence cited in the finding.
- **Refuted by the tree** — do not present it as a finding. Record it once as a factual note (`sub-agent B reported X; path:line contradicts it`), printed after the three tiers alongside the other reporting-only notes below, so the check is visible rather than a silent deletion. It is not gated on a PRD the way Scope Notes is; a refuted finding on a no-PRD review still gets its line.
- **Neither confirmable nor refutable from the tree** — the disposal depends on whether the finding is of the class "Verify, don't suspect" governs. If it turns on library callback semantics, subpath resolution, or provider schema constraints, **apply that rule's downgrade clause**: it does not print at Observation, Suggestion, or Concern, but as a named follow-up with an explicit "verify before merge" action. That rule already denies an uncited finding of this class a tier, and a controller that could not cite it either has not changed the citation state. Every other finding is presented at the tier the sub-agent assigned, with the unverified basis named — the downgrade clause does not reach it, and does not license the tier either.

Checking is not re-judging. The parent verifies claims; it does not re-rank a sub-agent's severity, and it does not reconcile one sub-agent's findings against the other's.

**This rule governs terminal presentation only, and loop-mode runs Phase 4.** A refuted finding still gets its ledger row, `open`, with the refutation attached — Phase 5 Step 1 takes *every* finding from Phase 3 with no filtering, and Step 2 keeps refuted ones on the explicit ground that dropping one is a decision the operator makes. Suppressing a refuted finding from the terminal is presentation; suppressing it from the ledger would be the unacknowledged report the ledger exists to prevent. Where the two rules would disagree, the ledger wins.

**Minimum-findings guard.** Before presenting, count the total findings — all three tiers, plus any downgraded verify-before-merge follow-ups, which are findings whose print location moved, not findings that stopped existing. If the total is fewer than 4 on the diff Phase 3 read — the whole branch on a first review, the post-stamp delta on a re-run, so a two-commit fix does not trip this — and that diff is of any meaningful size (more than ~50 changed lines or more than 2 files), do one more focused pass explicitly looking for what you might be missing — scope drift, silent assumption changes, shallow modules, tests that only cover the happy path, or new state files that slipped past State Discipline. **That second pass runs in a fresh sub-agent, on the same context Phase 3 specifies — not as a re-read in this context.** It is spawned from Phase 4, so say so explicitly, and read that context off Phase 3 rather than off a list here — including the one thing loop-mode adds to it, the ledger's recorded states and evidence. An enumeration at this distance from the contract is how this sentence previously dropped the ledger and sent the second pass to re-report findings the operator had already settled. Its findings are held to the same reader bar as any other. **Brief it to skip the controller-owned dimensions.** It is handed the whole checklist, and those dimensions were already disposed of above — run, or declared self-gated-off. Phase 3's sub-agents get the checklist *with an assignment* — the dimensions marked for them — so nothing controller-owned is ever offered; Phase 4's second pass gets the file with no assignment, so it must be told what to skip. Without it the pass either silently drops them or re-runs them from a context that cannot support the verdict. The guard fires precisely when the first pass came back thin, and the bias blind spot means hygiene cannot be self-administered (Kahneman, Sibony & Sunstein, *Noise*) — a re-read holding the first pass's context reproduces the review that was thin, and launders it as an independent second look. Its findings go through the evidence check above like any other delegated finding. A count of zero or one on a non-trivial diff is a signal that the review stopped too early, not that the code is flawless. If after the second pass the count is still low, present what you have — do not fabricate findings to hit a quota.

**Hold each finding to the same reader bar as the PR body.** Phase 2 already requires a plain-language walkthrough for the bodies it writes on non-trivial PRs. The findings had no equivalent bar, and they are this skill's primary product — the body is scaffolding around them. A finding a reader cannot parse fails the same way a finding that was never raised fails, and it fails silently: the tier prints, the ledger row shows an owner, and nothing registers that the signal did not transmit. So write each Suggestion and Concern to the shape and revision bar in `references/writing-for-humans.md` — name the part of the system in domain terms, front-load the claim before qualifying it, close with what it prevents or unlocks, then strip the clutter.

Two limits. **Observations are exempt, as is any finding whose domain meaning is self-evident** — a one-line note about a naming pattern carries no domain setup. That exemption is stated here as this skill's own rule rather than borrowed from the doc's when-to-skip list, which exempts *artifact classes* (typo fixes, dep bumps, formatting-only PRs, single-line reverts, trivially-reproducible bugs) and reaches no finding. Four of those five are diffs Phase 3 never delegates, so the list a review sub-agent holds is inapplicable to it by construction; what does transfer is the closing rule beneath it — when in doubt, one sentence beats a padded walkthrough.

Second, the bar is on **clarity, not length** — a finding that got longer without getting clearer failed it. Read this alongside the minimum-findings guard above: that guard forbids inventing findings to hit a count, this one forbids padding the findings you have.

The bar governs the finding text itself, so it carries into all three modes — author-mode's terminal advisories, the reviewer-mode drafts built from the same findings, and the loop-mode ledger rows that outlive the session that produced them, where the reader is coldest.

**Findings arrive written to the bar; this phase does not reword them.** Phase 3 puts the obligation in the writer's brief — delegated or in-session — so the bar is met at authorship rather than retrofitted here. The prohibition is narrow and covers one act: rewriting a returned finding to fix its prose. In author-mode the parent is the session that wrote the code, so passing an independent reviewer's findings through it to be reworded would spend the independence delegation just bought. When findings arrive below the bar, the fix belongs in Phase 3's brief, not in a cleanup pass here.

Parent-authored text built *from* a finding is not covered by that prohibition and is governed by the bar directly — reviewer-mode's Triple-R Rationale and loop-mode's ledger `Finding` cell are both written by the parent, and both are held to it.

**Author-mode** prints terminal advisories (below). **Reviewer-mode** transforms those same findings into draft PR comment text (see "Reviewer-mode comment drafts" below) — same dimensions, same severity classification, different output shape.

Present in the terminal using three tiers (author-mode):

```
## Architectural Review

### Observations (for awareness — no action needed)

[Patterns noticed that aren't violations. Example: "The presence module
exports 6 functions — reasonable, but worth watching if it grows."]

### Suggestions (action optional — would improve quality)

[Grouped by dimension. Things that aren't violations but would make
the code better. Written to the reader bar above.]

### Concerns (action recommended — potential principle violation)

[Grouped by dimension. Each concern cites the principle, shows the
specific code, and explains why it matters — and reads cold to someone
who did not write the diff, per the reader bar above
(`references/writing-for-humans.md`).]

### Verify before merge (findings that hold no tier)

[Findings the "Verify, don't suspect" downgrade clause removed from the
tiers — library callback semantics, subpath resolution, or provider schema
constraints that nothing could cite. Each names the check that would settle
it. Omit the section when there are none.]

---
No action is required. These are advisory.
When ready, merge the PR at <PR-URL>.
```

**This block is the last review action author-mode takes.** Finish the rest of Phase 4 below, then hand back at the `## Handoff` next-step menu (`references/next-step-menu.md`) — that menu is where what-happens-to-a-finding gets decided, and the user picks, not this session.

**Scope Notes (only when a PRD with slice issues was provided):**

After the three-tier findings, note any significant scope drift between the planned decomposition and the actual diff:

- Work that appears in the diff but wasn't in any slice's Boundary Map (omitted scope discovered during implementation)
- Declared Produces that don't appear in the diff (planned work that was cut or deferred)
- Slices where the actual diff footprint was dramatically different from the boundary map's declared scope

These are factual notes, not review findings. They don't produce Observations, Suggestions, or Concerns — they record plan-vs-actual divergence so the user and `/compound` can decide whether a pattern is worth capturing. Omit this section entirely if the diff aligns closely with the planned boundary maps.

**Acceptance-criteria checkbox reconciliation (reporting only).** While the slice issues are loaded, compare each slice's `## Acceptance Criteria` checkbox state against what the merged diff and verification actually establish. Flag any mismatch as a factual note — a criterion that reads as met but whose box is still unchecked, or a checked box the diff doesn't support. A criterion written in EARS form (`When`/`While`/`If … then`, with a `shall` clause naming the behavior) carries its own search key: look for the clause in test names and assertions in the diff, and report a criterion whose clause appears nowhere as the same kind of factual note. A matching clause proves a test exists, not that it is correct — this is a reader aid for the comparison above, not a substitute for it. Report it; do not edit the issue. `/execute` is the single writer for these boxes (see its Step 5/6 writeback); `/pre-merge` stays advisory and never writes, so this is a merge-gate backstop that surfaces drift without creating a second editor.

**Closing-issue comment-thread reconciliation (reporting only).** Phase 1 loads slice issues without their comment threads, so a requirement living only in a comment is invisible to every check above. For each issue named in the PR body's `Closes #N` lines — those issues only, not every slice loaded in Phase 1 — fetch the thread and compare it against the body:

```bash
gh issue view <closing-issue-number> --comments
```

Report as a factual note any comment naming a concrete capability the body's acceptance criteria do not cover **and whose consumer you can name** (an issue, slice, PRD, or shipped code that would use it). Apply the same discriminator `/execute` Step 1 uses: an exploratory comment with no identified consumer does not qualify. Merging is what closes the issue, so this is the last moment the thread is still attached to open work. Report it; do not edit the issue and do not file the follow-up yourself — `/execute` remains the single writer, and this backstops the case where `/execute` never ran on the issue at all (hand-authored PRs, external contributions).

If the review reveals that the main lesson is about Skill Kit itself — for example unclear stage boundaries, missing handoff guidance, or a review checklist gap in `chrislacey89/skills` rather than a problem in the downstream codebase — note: "Consider running `/improve-pipeline` if that skill is present." Do not invoke it.

If a concern warrants deeper work, note: "Consider running `/request-refactor-plan` for this area." Do not invoke it.

If a finding looks like a behavioral bug, note: "Consider running `/qa` to verify." Do not file an issue.

If the person about to merge did not author the diff — or hasn't internalized it commit-by-commit — note: "Consider running `/walk-commits` for an interactive per-commit comprehension walkthrough before merge." Do not invoke it. This is a comprehension/sign-off pass, distinct from the defect review above; it does not replace these findings.

Omit any tier that has zero findings.

**When a single finding's disposition forks three or more ways, present the options as a comparison.** Most findings have an obvious disposition and need no ceremony. Occasionally one does not: the same Concern can be fixed on this branch, filed as an issue, accepted with a reason, or dropped as wrong — the four states the Phase 5 ledger already names — and each carries its own resulting state, cost, and "take it if." When that fork clears the threshold in `references/next-step-menu.md` § *Show the comparison before you take the choice* — three or more mutually exclusive options, each with three or more attributes, not orderable on one axis — present it as a table, attributes as rows and dispositions as columns, each cell cited to a `file:line` or marked asserted. Below the threshold, prose as usual.

This phase **presents**; it does not take the choice, and this paragraph does not change that. The comparison is a presentation device that makes the finding legible, exactly like the three-tier format around it. The operator disposes — at the Handoff menu below in author-mode, or by writing a state into the ledger in loop-mode — and the comparison is what they read before doing so. Do not add options to that menu on the strength of a comparison rendered here.

**Stamp the reviewed head SHA into the PR (author-mode and loop-mode).** The review above covers one specific commit. Record which one in the PR body, so a later — possibly fresh-session — `/closeout` can tell whether the diff it is about to merge is still the diff that was reviewed. Prospective memory fails silently (Norman), so the marker goes into durable GitHub state rather than into the operator's head; `/closeout` Step 2's review-currency precondition is its only reader.

Write it only after the findings above have been presented — the stamp asserts "a review completed at this SHA," so writing it earlier would certify a review that had not run.

```bash
REVIEWED_SHA=$(git rev-parse HEAD)
SHORT_SHA=${REVIEWED_SHA:0:7}   # pinned, not `git rev-parse --short` — see the width note below
BODY_FILE=$(mktemp)   # unique per run — parallel worktrees must not share a temp path

# Guard the read half. Check the fetch's exit status, not just the file's size:
# a 5xx makes `gh` fail, and the edit below would then replace the whole PR body
# with a stamp. `--json` parses the response, so a success exit means the body is
# whole; the emptiness check below is for a PR whose body is genuinely blank.
if ! gh pr view <pr-number> --json body -q .body > "$BODY_FILE"; then
  echo "stamp aborted: PR body fetch failed" >&2; rm -f "$BODY_FILE"; exit 1
fi
[ -s "$BODY_FILE" ] || { echo "stamp aborted: PR body came back empty" >&2; rm -f "$BODY_FILE"; exit 1; }
ORIG_BYTES=$(wc -c < "$BODY_FILE")

# In "$BODY_FILE": replace the existing "## Review Currency" section if one is
# present; otherwise append this block, substituting the real SHAs:
#
#   ## Review Currency
#
#   <!-- reviewed-at: <full-sha> -->
#   Reviewed by `/pre-merge` at `<short-sha>`. Commits pushed after this SHA have
#   not been through the review dimensions — `/closeout` surfaces the delta before merge.
#

# Guard the write half. With $SHORT_SHA pinned above, stamping only ever appends
# one block or swaps one fixed-width block for another, so the edited body is
# never shorter than what was read. Shorter means the edit dropped content.
[ "$(wc -c < "$BODY_FILE")" -ge "$ORIG_BYTES" ] || { echo "stamp aborted: edited body is shorter than the body read" >&2; rm -f "$BODY_FILE"; exit 1; }

# Guard the write half too. Everything below this line — including the local
# flag that locks the branch — runs only if the stamp actually landed in the PR.
# An unchecked `gh pr edit` would leave the PR body unstamped and the flag on
# disk, which locks the branch on the strength of a review nothing recorded.
if ! gh pr edit <pr-number> --body-file "$BODY_FILE"; then
  echo "stamp aborted: PR body write failed" >&2; rm -f "$BODY_FILE"; exit 1
fi
rm -f "$BODY_FILE"

# The stamp's local twin. `.claude/.review-stamped` is read by
# .claude/hooks/enforce-classification.sh, which refuses implementation writes
# while it exists and .claude/.fix-findings-active does not — so a post-review
# fix has to go through /fix-findings or through a visible hand deletion.
# /closeout removes it at merge. The guard on the `gh pr edit` above is what
# makes this line reachable only after the stamp write succeeded; without it the
# touch would run on an aborted stamp too.
# $CLAUDE_PROJECT_DIR is unset outside a Claude Code session, and an unguarded
# expansion would resolve to "/.claude" — a silent no-write that leaves the
# lock disengaged while everything above reports success.
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"
mkdir -p "$PROJECT_DIR/.claude" && touch "$PROJECT_DIR/.claude/.review-stamped"
```

- **All three guards refuse rather than repair, and an abort is not a failed review.** Retry the fetch **once**, and a failed write **once** — the write sets the body from a file rather than appending, so a retry cannot double-stamp; if the second attempt also aborts, report it and hand back with the findings you already presented standing. The bound matters — an unbudgeted retry loop against a flaking API was an untimed contributor to the incident this guard came from. Losing a stamp costs one `/closeout` prompt about review currency. Overwriting a PR body costs the lineage, the `Closes #N` lines, and the `## Review Notes` `/execute` wrote — the things nothing else holds a copy of.
- **`$SHORT_SHA` is pinned to 7 characters rather than taken from `git rev-parse --short`.** The abbreviation `--short` picks is variable-width and grows as a repo does, so a re-stamp could swap an 8-character short form for a 7-character one and leave the body one byte shorter than what was read — which the write guard would correctly refuse, on a write that was correct. Pinning the width is what makes the guard's "never shorter" premise true rather than nearly true.

- **The HTML comment carries the full 40-character SHA — never the short form.** The two placeholders sit on adjacent lines and are not interchangeable: `<full-sha>` is the untruncated `git rev-parse HEAD` output, `<short-sha>` is the abbreviated form and belongs *only* in the visible prose line. `/closeout` compares the extracted marker against `headRefOid`, which is always 40 characters, so a short SHA in the comment can never compare equal — the gate would then report divergence on a PR whose head never moved, and a gate that cries wolf is one that gets clicked through. `/closeout`'s parser requires exactly 40 hex characters, so a swapped placeholder does not degrade quietly into a prefix match; it fails to parse. In the Skill Kit repo, `scripts/test-review-currency-marker.sh` pins this contract by round-tripping this template through `/closeout`'s own extraction, so the two skills cannot drift apart silently.
- **Exactly one stamp per PR.** Re-running `/pre-merge` replaces the existing block rather than appending a second one. `/closeout` reads the stamp as a single value, and two stamps make "which SHA was reviewed" ambiguous — with the stale one being the more dangerous answer.
- **The stamp claims coverage over commits, not one whole-tree read.** Its own visible line says what it means: commits after the SHA have not been through the review dimensions. A re-run in delta scope (Phase 1 step 4) satisfies that claim for every commit up to the new head — the earlier review covered the commits up to the old stamp, this one covered the rest — so it re-stamps at `HEAD` with the same template. Nothing in the block records the scope, deliberately: the block is width-pinned by the never-shorter guard above, and a scope field that shrank on the next whole-branch re-stamp would abort it. The scope is printed to the terminal in Phase 1 instead.
- **Keep both halves.** The HTML comment is what `/closeout` greps for; the visible line is what tells a human skimming the PR why an unfamiliar SHA is sitting in the body.
- **Reviewer-mode does not stamp, and does not touch `.claude/.review-stamped`.** It never creates or rewrites the PR body (Phase 2 is skipped for the same reason), and its findings are drafts the user has not yet posted — nothing has been reviewed *into* that PR to certify. Locking a local checkout on the strength of comments nobody has posted would refuse edits on a branch the reviewer does not own.
- **Fixes made in response to these findings will move the head past the stamp.** That is the mechanism working, not a false alarm: those commits genuinely have not been reviewed. `/closeout` Step 2 makes that divergence *visible* at merge; the `.claude/.review-stamped` flag written above is what makes it *cost something* at the moment of the edit, by routing the fix to `/fix-findings` — a sub-agent that did not write the code — or forcing a deliberate hand deletion. The flag is local and transient; the stamp in the PR body remains the durable record, and this skill remains its only writer.
- **Loop-mode stamps exactly as author-mode does.** It makes no commits of its own, so the head does not move underneath it and none of the rules above need a loop-mode exception. Fixes the *operator* makes in response to the ledger move the head past the stamp, which is the bullet immediately above: real and unreviewed.

**At the very end of Phase 4 output, if — and only if — a durable lesson emerged from this work that future `/research` or `/write-a-prd` would benefit from, recommend capturing it in this PR before merge.** `/compound`'s default is to commit the `docs/solutions/` entry onto this still-open PR branch and hand back here for a re-run that reads that commit and re-stamps, so the lesson is reviewed before the same merge and merged atomically with the code — capture it now, before `/closeout`, rather than as a separate post-merge session. Print the runtime handoff line:

```
**Next session:** /compound
**Input:** PR #<pr-number>  (capture the lesson onto this PR branch, before /closeout merges)
```

**Do not print it on the re-run `/compound` itself handed back.** That run is in delta scope (Phase 1 step 4) and its subject is the `docs/solutions/` entry — the lesson it would recommend capturing is the commit under review. Recommending it again would hand back to `/compound`, which would hand back here, and neither step has a counter to stop on; the "if — and only if — a durable lesson emerged" condition is what forecloses it, because a captured lesson has not emerged uncaptured. The discriminator is the delta, not memory of the session: when the post-stamp delta consists only of `docs/solutions/` paths, this recommendation is already answered and the exit is `/closeout`. Read that off the delta the scope decision printed:

```bash
# This block runs in its own shell — $SCOPE_FROM was assigned in Phase 1 step
# 4's fenced block and does not survive here. Unset, the range below makes git
# diff HEAD against itself and print nothing, and the guard below would
# misread that empty diff as "delta is a /compound entry" on a delta that was
# never read. Same failure BASE_REF's guard at review-checklist.md:114 exists
# to catch.
: "${SCOPE_FROM:?resolve it with the Phase 1 step 4 scope-decision block before running this}"
# Capture and test for empty rather than asking `grep -qv` for the verdict.
# Two reasons, and the second is why this shape is not optional: `grep -q` exits
# at the first match and the producer dies of SIGPIPE, which `pipefail` reports
# as "no match" from a pipeline that matched (scripts/test-pipefail-safe-matchers.sh);
# and the `grep` on PATH in a Claude Code shell is a function wrapping ugrep,
# whose `-q -v` returns 1 on input that *does* contain a non-matching line —
# the exact inversion of the verdict, in the direction that suppresses the
# recommendation on a delta carrying code. `grep -v` without `-q` is correct
# under both.
outside=$(git diff --name-only "$SCOPE_FROM...HEAD" | grep -v '^docs/solutions/' || true)
if [ -z "$outside" ]; then
  echo "delta is a /compound entry — do not re-recommend /compound; the exit is /closeout"
fi
```

A delta carrying anything outside `docs/solutions/` is not that case, including a `docs: compound` commit that also staged Phase 4's mechanism — the subject line is not evidence of what the commit contains, which is `/closeout` Step 2's discriminator too.

Substitute `<pr-number>` with the PR created in Phase 2. Skip the line when the work was a clean execution of a pre-shaped plan with no surprises, rework, or non-obvious decisions — the issue body and PR description already carry that record, and a `docs/solutions/` entry with no reusable lesson trains future readers to skim. When in doubt, skip. Signals that a lesson is worth capturing: a tricky bug whose root cause was non-obvious, a Rabbit Hole from the PRD that actually bit, an architectural decision with significant tradeoffs, or a pattern that should be reused. See `/compound`'s "When NOT to Use" for the full skip list.

### Phase 5: Loop-Mode — Give Every Finding an Owner

**Loop-mode only.** Author-mode and reviewer-mode end at Phase 4; their findings stay advisory by design.

Phases 1–4 are a sensor. Without something that acknowledges, investigates, and resolves what the sensor reports, the reporting channel is functionally equivalent to having no sensor at all (Leveson, Ch. 12) — and Phase 4's own closing line is "No action is required. These are advisory." Phase 5 closes that loop by making findings *durable*: every finding gets a row in a ledger on the PR, and the ledger survives the session that produced it.

**Loop-mode does not fix anything.** It reviews, records, gathers evidence, and hands back. The operator decides what happens to each finding. That boundary is the design, not a limitation to be removed later — see "Why the loop does not fix" below.

**The loop is human-driven.** Loop-mode does not run autonomous passes: it makes no commits, so there is no delta for it to re-review on its own. A pass happens when the operator invokes `/pre-merge --loop` again after acting on the previous pass's findings. There is no pass bound, because there is no autonomous cycle to bound.

#### Step 1 — Record every finding in the ledger

Every finding from the review — every dimension in `review-checklist.md`, whichever bucket its `**Runs in:**` marker assigns it to, plus `/ts-audit` when its trigger fires — gets a row. That includes the controller-owned dimensions Phase 4 runs rather than Phase 3, which is the whole reason this sentence names the checklist instead of a count: a ledger row is an attestation, and the previous phrasing attested a number this skill never verified against the roster. No filtering, no severity cutoff, no "this one is obviously fine." A finding the loop drops silently is exactly the unacknowledged report Leveson's rule is about. This includes findings Phase 4's evidence check refuted and therefore did not print: the ledger's input is Phase 3's output, not Phase 4's.

Findings arrive **open**. `open` means "recorded, awaiting the operator's decision," and it is the only state loop-mode may assign.

#### Step 2 — Attach evidence, do not draw conclusions

A finding is a *claim about* the code, not the code. On the corpus that validated this design, one finding of fourteen asserted that a block "no-ops because the mutating step is a bash comment," and three independent classifiers all rated it high-confidence actionable. It was a false positive: the comment-carries-the-judgment-step shape is an established convention in this repo, used identically in `/execute` Step 5's acceptance-criteria writeback.

So loop-mode checks each finding against the tree and records **what it found**, not **what should happen**:

- The grep, file path, and line that support or refute the finding.
- The installed type definition, when the finding turns on library semantics (Phase 3's "Verify, don't suspect" rule).
- A plain `refuted — <evidence>` note when the tree contradicts the claim.

Gathering evidence is not deciding. A refuted finding still stays in the ledger as `open` with its refutation attached, because dropping it is a decision and the operator makes those. The value is that the operator reads a claim with proof beside it rather than a claim alone.

#### Step 3 — Write the ledger and hand back

Write the ledger block (below), then print what the operator is inheriting: the finding count, how many carry refuting evidence, and which dimensions produced them.

`/pre-merge` does not stamp differently in loop-mode. Loop-mode makes no commits, so the head does not move and Phase 4's ordinary stamp rules apply unchanged.

#### The disposition ledger

Each invocation runs in a fresh context, so without a durable artifact it re-derives the previous pass's findings (Cohen: N passes by a self-similar reviewer are not N independent reviews). The ledger is that artifact, and it is simultaneously the acknowledged / investigated / resolved record Leveson's closed-loop rule requires — one artifact, both jobs, GitHub-native.

It follows the `## Review Currency` conventions with **one deliberate divergence**: a marked block in the PR body, exactly one per PR, with a machine-readable marker and a visible human line — but where the stamp holds a single current value that each write supersedes, the ledger is a *cumulative* record.

**Rewriting the block must carry every prior pass's rows forward.** "Replace, don't append" governs the block, not its contents: pass 2 emits one block containing pass 1's rows plus its own. A literal replacement that drops pass 1's rows destroys exactly the record this section cites Leveson to justify — and it fails silently, because the surviving block looks complete.

```markdown
## Review Disposition Ledger

<!-- loop-pass: 2 -->
<!-- loop-judge: model=claude-opus-5 checklist=a1b2c3d prompt=loop-mode-v1 -->

Recorded by `/pre-merge` loop-mode. Every finding below has an owner. Rows marked `open` are waiting on a decision from you.

| Pass | Finding | Dimension | State | Evidence / outcome |
|---|---|---|---|---|
| 1 | Duplicate date formatter in pipeline | 1 — Deep Modules | fixed | `abc1234` — operator |
| 1 | Same pattern in `lib/export/` | 1 — Deep Modules | filed | #199 — operator |
| 1 | Stamp block "no-ops" | 7 — docs/solutions | open | refuted — `/execute` Step 5 uses the same shape ("Write verified status back to the issue") |
| 2 | Presence helper claimed as Effect Layer | 4 — Boundary Map | open | confirmed — `lib/presence.ts:12` exports a plain function |

**Checks not run this pass:** `/ts-audit` — delta is 12 changed `.ts` lines across 1 file, below the 50-line / 2-file trigger.
```

**No angle brackets inside the marker values.** The fields above carry literal values (a model ID, a short SHA, a prompt name), never `<placeholder>` syntax — a `>` inside an HTML comment terminates the naive `<!-- … -->` extraction that reads it, truncating the marker at the first placeholder and silently dropping every field after it. That is not hypothetical: `scripts/test-loop-ledger-markers.sh` was written against a template that had this bug and caught it on the first run. Substitute real values; if a value could ever contain `>`, quote or encode it.

The **Checks not run this pass** line is where a suppressed check is recorded. A skipped check is not a finding and has no state, so it does not belong in the table — but leaving it out entirely would let the ledger read as "everything ran," which is the silent-truncation failure the ledger exists to prevent. Omit the line when every check ran.

**The `Finding` cell is read cold, sittings later, by whoever picks the branch up.** It is the narrowest slot Phase 4's reader bar applies to and the one where it matters most: name the thing in domain terms and front-load the claim, so the row stands on its own without the terminal output that produced it — `Duplicate date formatter in pipeline`, not `Deep Modules issue`. Two cells are outside the bar. The `Evidence / outcome` cell carries a citation, not prose, and padding it into a sentence would bury the grep the operator is there to check. And Observation rows are exempt here as they are in Phase 4 — the ledger takes every finding, so Observations do get rows, but a naming-pattern note is not made to carry domain setup to sit in one.

**States in the `State` column.** Loop-mode writes only `open`. The operator writes the rest — `fixed` (with the commit), `filed` (with the issue number), `accepted` (won't fix, with the reason), or `dropped` (with why the finding was wrong). `/pre-merge` never overwrites an operator's state on a later pass; it appends new findings and leaves settled rows alone.

Write the block with the same `mktemp` → **check the fetch's exit status** → read body → **record its byte count** → edit the block → **refuse the write if the result is shorter** → `gh pr edit --body-file` shape Phase 4's stamp uses. The two guards are named here rather than left to "same shape," because they are the half of that shape a reader reconstructing it from the four visible steps would omit — and the ledger is the block this skill rewrites most often. `gh pr edit` creates no commits, so ledger and review-notes writes do not move the head and are **benign** writers in the review-currency interval — stated explicitly because "writes to the PR" reads as invalidating when left unclassified, and an unclassified writer is how a gate acquires its first false positive on the happy path.

**What passes forward to the next pass, and what is withheld.** Independence and efficiency pull opposite ways here, and the split resolves them:

- **Forward: the states and the evidence** — what was fixed, filed, accepted, or dropped, and the greps behind each. These are facts about the code's *current* state. Without them the next pass re-reports resolved findings.
- **Withheld: the previous pass's severity judgments.** That is the anchoring surface. A fresh reviewer independently re-raising something an earlier pass rated trivial is *signal*, and forwarding the earlier rating would suppress it.

This is deliberately **not** `/handoff`. That skill summarizes into a transient `mktemp` doc, and both properties are wrong here: the fix Leveson's rule demands is "hand over checkable claims," not "summarize better," and every summarization hop is a lossy transformation authored by the upstream controller. `/handoff`'s own Red Flags already forbid producing a doc at a pipeline-skill boundary; that fence stays where it is.

#### Pin the judge, or cross-pass comparison is meaningless

The delegated reviewer is an AI judge, and **a judge is a system — model + prompt + sampling parameters — not a model** (Huyen, Ch. 3). Comparing pass 1 against pass 3 — "is this the same finding I saw before, or a new one?" — silently assumes both measured the same way. So loop-mode records the reviewer's model, the `review-checklist.md` revision, and the prompt shape in the ledger's `loop-judge` marker. **A change to any of the three starts a new loop rather than continuing the current one** — cross-pass comparisons do not carry across a judge change.

#### Why the loop does not fix

The obvious next step is to let the loop act on its own findings: fix the local ones, escalate the rest. That step is deliberately **not** taken here, and the reasons are worth stating so the boundary does not read as an oversight.

- **The cheap half and the risky half are separable, and only the cheap half has evidence behind it.** Driving the cycle — re-running the review, remembering `/ts-audit`, keeping state across invocations — carries no risk of wrong action. Deciding what to do about a finding carries all of it. Automating the second while the first was the actual friction inverts the cost/benefit.
- **The available evidence measures agreement, not correctness.** The FEASIBILITY spike found 93% unanimity across three independent classifiers — but unanimity is not accuracy, and the same corpus contained a finding all three rated high-confidence actionable that was a false positive. Nothing yet measures whether an automated fix would have been *right*.
- **Compound error runs against it.** Roughly 40 decisions at 95% each gives about a 13% chance all are correct (Huyen). The usual mitigation is to bias errors toward escalation — but most real findings need judgment, so a correctly-biased loop escalates nearly everything and saves nothing.
- **The reversal is asymmetric.** Adding action to a loop that records is easy. Removing it after it has silently "fixed" things is not.
- **The pipeline's own rule says prove it HITL-first.** `/setup-ralph-loop` already defers the `ralph.sh` review phase on exactly this ground. Applying the same rule one level up is consistency, not timidity.

The ledger is what makes the later decision possible: it accumulates real findings with real outcomes, which is the corpus an automated disposition rubric would need before it could be trusted. Tracked as a follow-up rather than dropped — in the Skill Kit repo, issue #190, which states the evidence needed before it may start and names "close it unimplemented" as an acceptable outcome.

#### Health signals

**The loop's health signal is findings surfaced and given owners — never findings remaining.** If *findings surfaced per pass* trends down across runs over time, the loop is suppressing reports rather than improving code (Leveson: never reward low incident counts — reward reporting itself). Re-anchor the bar or return review to plain author-mode.

Watch one more: the share of ledger rows still `open` at merge. A ledger where everything sits `open` means the record is being written and ignored, which is the unclosed audit loop with extra steps.

#### Loop-safety coverage

The rules above are placed where they apply rather than collected in a list, so they are read at the moment they bind. That makes the set harder to audit, so here is the derivation. STPA Step 1 classifies inadequate control actions four ways, and **three of the four require nothing to fail** — which is why enumerating them catches hazards that listing plausible mistakes does not:

| Inadequate control action | The rule that covers it |
|---|---|
| Not provided | A finding never reaches the ledger → Step 1: every finding gets a row, no filtering, no severity cutoff |
| Provided unsafely | The loop acts on a finding it should have handed back → it never acts at all; `open` is the only state it may write, and it never overwrites an operator's state |
| Wrong timing or sequence | A pass reports on a half-applied state → the loop makes no commits, so no such state exists; operator-applied fixes land between invocations, not during one |
| Stopped too soon / applied too long | The loop reports clean while findings sit unrecorded → the health signal is findings *surfaced*, never findings *remaining*, and a falling per-pass count is read as suppression |

**Circuit breakers: loop-mode introduces none of its own.** It makes no commits and runs no autonomous passes, so `/execute`'s repeated-failure and plateau rules have nothing to trip on here. They apply to the operator's fix work between invocations, where they already did.

### Reviewer-mode comment drafts

In reviewer-mode, transform the dimension findings into PR comment text per `references/comment-craft.md`. Output drafts to the terminal (clearly grouped) for the user to review and post — do **not** post comments directly via `gh pr comment` or `gh api` from this skill. The user is the editor of last resort; auto-posting comments on someone else's PR is hard-to-reverse and skips the human empathy pass that comment-craft is built around.

For each finding, draft the comment using these rules. The full methodology is in `references/comment-craft.md`; this is the application:

1. **Run the 5P gate per finding.** If the concern is unjustifiable, *Pass* (drop it from the draft set). If it is valid but out of scope for this PR, *Postpone* (surface as a "Suggested follow-up issue" line, not a PR comment). Only Propose-class findings become PR comments.

2. **Map severity → Comment Signal.** Use `review-checklist.md`'s severity classification to pick the prefix:
   - `Concern` → `needs change:` (small fix), `needs rework:` (major refactor), or `align:` (convention violation)
   - `Suggestion` → `levelup:` (non-blocking improvement)
   - `Observation` → either drop entirely (no action implied) or post as `nitpick:` if it warrants noting

3. **Use Triple-R for action-requiring comments** (any blocking signal, plus most `levelup:`s). Request (transformation verb), Rationale (objective justification — cite the principle from `review-checklist.md`, the `.d.ts` line, the prior PR), Result (measurable end state). **The Rationale is where Phase 4's reader bar lands**: a citation is not an explanation, so the Rationale has to orient an author reconstructing context, not just name the rule that was broken. Request and Result stay terse — they are instructions, and the bar does not ask them to become prose.

4. **Apply tone discipline.** Replace sentence-initial "you" with "we." Ask, don't command. Target the artifact, not the author.

5. **Anchor each comment to a file path and line.** A PR comment without a code anchor is harder to act on than a terminal advisory; reuse the file/line citations the dimension findings already require (especially Surgical Scope's "cited hunks, not yes/no" rule).

Output shape in the terminal:

```
## Reviewer-Mode Draft Comments — PR #<pr-number>

### Per-line comments (paste at the cited code position)

#### `path/to/file.ts:42`
**`needs change:` Move helper into existing utility module**

**Rationale** — the new `formatBillDate` in `src/pipeline/format.ts:42` duplicates `lib/dates/format.ts`'s shape. `pre-merge/review-checklist.md`'s Deep Modules dimension flags this as information leakage between two modules holding the same protocol detail.

**Result** — `formatBillDate` lives in `lib/dates/format.ts` and `src/pipeline/format.ts:42` imports it.

---

[next per-line comment]

### Top-level review summary (paste as PR-level comment)

[2-3 sentence summary of the review posture, naming the dimensions that ran and the highest-severity finding. Frame as collaborative, not adversarial — Rigby's "shippable code, not a defect tally."]

### Suggested follow-up issues (5P-Postpone — do not post in this PR)

- [Title] — out of scope for this PR; file as `<repo>/issues/new` if the team wants to track it
- [Title] — same

### Held back at 5P-Pass (no comments posted)

- [One-line note per dropped concern with the reason — kept for the user's audit, not for the PR]
```

If after the 5P gate the per-line comment count is zero, the review may still produce a top-level approval comment — phrase it as collaborative ("ready to ship from a structural standpoint" rather than "LGTM"). Tacke notes that LGTM-only approvals are a code-review failure mode; if you ran every dimension in `review-checklist.md` and have nothing concrete to say, that result is meaningful and should at least name which dimensions were checked.

If a disagreement is anticipated (e.g., the finding overturns a deliberate choice the author made), draft a single comment opening the MMG Exchange offline ("Can we sync briefly on the X tradeoff before I leave detailed comments?") rather than posting an objection thread on the PR.

## What This Skill is NOT

- **Not a test runner.** Pre-commit hooks run tests, typecheck, and lint on every commit.
- **Not a bug finder.** `/qa` files behavioral bugs as GitHub issues.
- **Not a refactoring planner.** `/request-refactor-plan` produces RFC-style refactor proposals.
- **Not a CI gate.** Findings are advisory in every mode. Loop-mode makes them durable rather than binding — it ends at "every finding has an owner," never at "safe to merge," and `/closeout` remains HITL-confirmed.
- **Not an auto-fixer.** Loop-mode records findings and gathers evidence; it makes no commits and decides nothing. The operator disposes of each row. See Phase 5 § Why the loop does not fix.
- **Not an auto-poster.** Reviewer-mode produces draft comment text for the user to review and post; the skill does not call `gh pr comment` or `gh pr review` itself.
- **Not a learning organ.** The ledger records *what* was found and what happened to it. Diagnosing the process defect that let a flaw through is `/compound`'s job, and the ledger is its input.

## Handoff

- **Expected input:** verified implementation work that is ready for review and PR creation (author-mode), an existing PR number you want reviewed (reviewer-mode), or an AFK handoff from `/execute` — branch plus the `## Review Notes` it wrote into the PR body (loop-mode)
- **Produces:** a PR with lineage, stamped with the head SHA the review covered — plus, locally, the transient `.claude/.review-stamped` flag the classification hook reads to route post-review fixes through `/fix-findings` — and an architectural review readout (author-mode); draft PR comment text following `references/comment-craft.md` (reviewer-mode); or that same PR plus a `## Review Disposition Ledger` in which every finding has a row, an owner, and the evidence for or against it (loop-mode)
- **May redirect:** to `/qa` when a finding looks behavioral, or to `/request-refactor-plan` when deeper structural cleanup is warranted
- **May invoke:** `/ts-audit` on changed `.ts`/`.tsx` — in loop-mode only; author-mode and reviewer-mode mention it without invoking
- **Comes next by default:** when a durable lesson emerged, `/compound` first — captured onto this open PR, then handed back here for a re-run over its commit, so the entry is reviewed and merged with the code it explains rather than merged unreviewed (skip when the work was a clean execution of a pre-shaped plan); then `/closeout` — confirm, merge the reviewed PR, re-anchor off the worktree before removing it, prune the merged branch, pull base, and verify a clean end state. When no lesson is worth capturing, go straight to `/closeout`. Lessons that only surface during or after merge can still be compounded post-merge as the fallback. In reviewer-mode, the user reviews and posts the draft comments; the next step is the author's response, not `/closeout`. In loop-mode, the ledger hands back to the operator: settle the `open` rows — fix, file, accept, or drop each one — then either re-invoke `/pre-merge --loop` on the updated diff or continue to `/compound`, the `/pre-merge` re-run it hands back to, and `/closeout` as above

**Next-step menu.** This is a genuine branch point, so offer the next step as a menu rather than leaving the user to retype a command (see `references/next-step-menu.md`). It does not apply on AFK loop-mode runs — there is no user to ask, so print the exit readout and the handoff line instead. Present a single `AskUserQuestion` with the recommended step first, each option naming its outcome rather than just its skill. In author-mode, when a durable lesson emerged: **→ `/compound` in this PR (recommended — capture the lesson)**, **`/closeout` (merge and clean up — no lesson worth capturing)**, **Fix a finding on this branch first (`/fix-findings <numbers>` — fresh fixer, then a `/pre-merge` re-run reads the post-stamp delta and re-stamps)**, **Hand the findings off as issues, then capture the lesson**. When no lesson emerged, lead with **→ `/closeout` (recommended — merge and clean up)**, **Fix a finding on this branch first (`/fix-findings <numbers>` — fresh fixer, then a `/pre-merge` re-run reads the post-stamp delta and re-stamps)**, **Hand the findings off as issues, then merge**. Route those findings to `/qa` or `/request-refactor-plan` after the choice, rather than naming two skills in one label. Both menus carry the finding-disposition pair because it is a separate axis from the lesson: whether a finding can wait does not depend on whether a lesson emerged, and a reviewer holding both has to be able to say so. **On the re-run `/compound` handed back — the delta test above says the post-stamp delta is only `docs/solutions/` paths — take the no-lesson menu even though a lesson plainly emerged from the branch: it is already captured, in the commit this run just reviewed, so `/compound` is not an option to re-offer and `/closeout` leads.** Within that pair the discriminator is *now vs. later*, not severity — so each label leads with the act that distinguishes it (*fix* vs. *hand off*) and closes with the step it returns to, rather than leading with the step both options share. In reviewer-mode the options differ — **Post the draft comments**, **Talk it through offline first (MMG Exchange)**, **Revise a draft comment** — because the next move is the author's response, not `/closeout`. The platform's free-text "Other" option is the escape hatch — don't add one.
