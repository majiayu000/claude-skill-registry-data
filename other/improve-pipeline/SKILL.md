---
name: improve-pipeline
description: "Optional meta-skill for improving `chrislacey89/skills` from real-world friction or breakdowns discovered while using the pipeline in another repo. Use when the main lesson is about the pipeline itself, not the downstream project. Grounds proposals in established software-engineering guidance from `/library`. Produces a GitHub issue in `chrislacey89/skills` and only moves to implementation after review."
sources:
  primary:
    - "Thinking in Systems — Donella Meadows"
  secondary:
    - "Thinking in Bets — Annie Duke"
    - "The Fifth Discipline — Peter Senge"
    - "Release It! — Michael Nygard"
    - "The Design of Everyday Things — Don Norman"
    - "Encouraging Divergent Thinking in LLMs through Multi-Agent Debate — Liang et al. (EMNLP 2024)"
    - "Improving Factuality and Reasoning in Language Models through Multiagent Debate — Du et al. (2023)"
---

# Improve Pipeline

Use this skill when real-world usage of the pipeline reveals a weakness in the pipeline itself. The triggering incident may happen in another repository, but the improvement target is always `chrislacey89/skills`: the skills, docs, checklists, and workflow guidance that shape future agentic development.

This is not automatic self-modification. Default output is a GitHub issue in `chrislacey89/skills`. The issue should explain what happened, why it is a pipeline problem rather than only a project problem, what change is recommended, what repo-wide effects the change could have, and which files in `chrislacey89/skills` would need to change if the recommendation is approved.

If the user asks for implementation after reviewing the proposal, implementation can follow as a separate step. Do not skip the proposal.

> **One question per turn.** If key facts are missing, ask one question at a time and wait for the user's answer before asking the next. Never turn incident intake or review into a questionnaire.
>
> **Prefer single-select.** Use single-select multiple choice when the user is choosing one direction, one priority, or one next step.
>
> **Use multi-select rarely.** Reserve it for compatible sets — goals, constraints, non-goals, success criteria — that can all coexist. If prioritization matters, follow up asking which selected item is primary.
>
> **Use the platform's question tool when available.** In Claude Code, use `AskUserQuestion`; in Codex, `request_user_input`; in Gemini, `ask_user`. Otherwise, present numbered options in chat and wait for the user's reply before proceeding.

## Invocation Position

This is an optional meta-skill, not a default pipeline stage.

Use `/improve-pipeline` when the main lesson is about the pipeline itself:

- a skill boundary was unclear enough to cause rework
- a handoff artifact was missing, weak, or misleading
- a guardrail or checklist should have prevented an avoidable failure
- a repeated failure mode suggests the pipeline is under-specified
- a prompt, workflow, or repo convention encouraged overfitting or shallow review
- `/compound` or `/pre-merge` surfaced a lesson that belongs in the pipeline repo rather than in the downstream app repo

Do not use it when the lesson is primarily about the downstream repository:

- project-specific architecture decisions
- app-specific bug fixes
- library integration quirks that do not reveal a pipeline weakness
- reusable product or domain knowledge that belongs in that repo's `docs/solutions/`

`/compound` and `/pre-merge` may recommend `/improve-pipeline`, but only if the skill is present and the main lesson is clearly pipeline-level. Do not auto-invoke it.

## Why This Exists

A delivery pipeline that never learns from field use eventually optimizes for the imagined environment in its prompts rather than the real environment in which it operates. The most dangerous pipeline failures are not always obvious syntax mistakes — they are shallow boundaries, missing feedback loops, duplicated guidance, and workflow steps that look coherent in isolation but break down when run end-to-end.

This skill exists to close that loop deliberately. It converts a field incident into a repo-wide proposal rather than a local patch. Its job is not to defend the current pipeline or to change it impulsively. Its job is to understand what happened, test whether the proposed change generalizes, and produce the smallest coherent improvement that strengthens the whole repository.

## Execution Flow

### Phase 0: Confirm Target Repo and Load Canonical Context

The GitHub issue target is always `chrislacey89/skills`. Never infer a different target from the current workspace, the downstream project's git remote, or whichever repository the incident happened in.

Before analyzing the incident or filing anything, load the minimum canonical context for `chrislacey89/skills`. When working inside the skills repo, read the repo-root originals; when invoked from a downstream project, read the bundled copies beside this skill:
- `README.md` — quick orientation to what Skill Kit is (repo-only; not bundled)
- `references/SYSTEM-OVERVIEW.md` (or repo-root `SYSTEM-OVERVIEW.md`) — pipeline philosophy, state model, and handoffs
- `CLAUDE.md` — rules for editing this repo itself (repo-only; not bundled)
- `references/skill-anatomy.md` (or repo-root `docs/skill-anatomy.md`) — the quality bar for skill changes
- `references/writing-for-humans.md` (or repo-root `docs/writing-for-humans.md`) — the plain-language walkthrough shape and revision bar for the issue body

Then read:
- the skill most closely related to the incident
- adjacent skills with overlapping boundaries
- any shared checklist, template, or repo doc that encodes the same guidance

Build a short context snapshot before proceeding:
- what this repo is for
- where state lives in this workflow
- which repo areas are most likely affected by the proposed change
- what should remain stable if the change lands

Use explicit GitHub commands that pin the target repository:
```bash
gh repo view chrislacey89/skills
gh issue list -R chrislacey89/skills --limit 1
```

If you cannot confirm GitHub access to `chrislacey89/skills`, or cannot load enough of the canonical context to reason about the repository as a whole, stop and ask. Do not file against the downstream repo as a fallback.

### Phase 1: Capture the Field Incident

Start from the real incident, not from a preferred fix.

Capture:

1. **Where the incident happened** — repository, branch, feature, or phase of work
2. **Which pipeline path ran** — for example `/shape` → `/research` → `/write-a-prd` → `/execute` → `/pre-merge` → `/compound`
3. **What was expected** — what the pipeline should have enabled or prevented
4. **What actually happened** — confusion, rework, misclassification, missing artifact, weak review, contradictory guidance, etc.
5. **What downstream evidence exists** — PRs, issues, failed runs, repeated questions, or concrete examples

Build a concise run breakdown:

- which step introduced the problem
- which step failed to catch it
- which step amplified it
- what the real cost was: rework, bad guidance, scope drift, false confidence, missed edge case, or user confusion

Do not assume the nearest visible failure is the true pipeline cause. Separate the event from the structure producing it. Frame the incident as a design failure, not a user failure (Norman's Blame Reversal Principle) — "I forgot to X" is not an incident; "the skill made it easy to forget X" is.

### Phase 2: Prove It Is a Pipeline Problem

Before proposing any repo change, test whether the incident truly belongs here.

Ask:

- Is this mainly a project-specific problem wearing pipeline clothes?
- Would improving the downstream repo alone solve it?
- Did the pipeline provide wrong guidance, missing guidance, weak sequencing, or no meaningful defense at all?
- Is this a one-off anomaly or part of a recurring pattern?

Classify the finding:

- **Local event** — belongs in the downstream repo, not here
- **Pipeline pattern** — this repo should change because the same class of issue is likely to recur
- **Pipeline structure** — the problem comes from a missing feedback loop, ambiguous ownership, overlapping skill boundaries, or contradictory repository guidance
- **Redundant or counter-productive guidance** — already-present text whose removal or consolidation would improve repo coherence. Subtraction is a legitimate finding, not only addition.
- **Discipline-shaped fix in disguise** — the proposed remedy requires the user to remember, notice, or do something. Reclassify as Pipeline structure and look for a knowledge-in-the-world equivalent (default behavior, forcing function, structural placement) before adding instruction text. (Norman, knowledge in the world vs. in the head.)

If the issue is only a Local event, stop and redirect to the downstream repo's normal documentation or `/compound` flow.

### Phase 3: Expand Scope to the Whole Repository

Never evaluate a proposed pipeline change in isolation.

Before recommending edits, inspect the full repository surface area that could be affected:

- `SYSTEM-OVERVIEW.md` (or `references/SYSTEM-OVERVIEW.md` when invoked outside the skills repo)
- the skill that appears closest to the incident
- adjacent skills with overlapping responsibilities
- any checklists, docs, or templates that encode the same guidance elsewhere
- the README or other discovery docs if the change alters how users should find or invoke the workflow

Explicitly search for:

- duplicated guidance that would become inconsistent
- adjacent skills whose boundaries would shift if this change lands
- prompts or templates that would need synchronized updates
- repo-level terminology that the change would affect
- downstream consequences of making the pipeline more prescriptive, more complex, or more opinionated

A proposal that only improves one file but weakens repository coherence is not ready.

### Phase 3.5: Consult the Library

Pipeline proposals should be grounded in established software-engineering guidance, not only in the agent's or the user's opinion. Before running the dialectic, consult `/library` — the user's local book index at `~/.claude/library/` — for books relevant to the incident.

Procedure:

1. **Survey the index.** Run `/library` with no args to see the catalog, or `/library --search <keywords>` when the incident has a clear topical handle (e.g. `testing`, `code review`, `debugging`, `systems`, `deep modules`, `feedback loops`, `refactoring`, `domain`).
2. **Select 1–3 relevant books.** Prefer books whose `description` or `tags` map directly to the incident type. Prefer books already cited in this skill's `sources:` frontmatter (Meadows, Duke, Senge, Nygard, Norman) when they are topically relevant so the skill's lineage and its live reasoning stay coherent.
3. **Load them.** Run `/library <name>` for each selected book and extract the concrete principle, checklist item, or failure mode that bears on the incident. Record these — they feed Phase 4 and the issue body.
4. **Do not over-consult.** Loading books has a context cost. Stop at three unless the incident is genuinely cross-cutting.
5. **Graceful degradation.** If `/library` is not installed or the index is empty, record "Library consultation: unavailable" and continue. Do not block filing.

Each book loaded should contribute something specific the dialectic can cite — a named principle ("shallow module smell"), a checklist item ("reviewer checks for X"), or a known failure mode ("policy resistance"). If a loaded book produces nothing citable, drop it from the record rather than name-dropping it.

### Phase 4: Run the Three-Agent Dialectic

Use a structured tension pattern before writing the proposal. Spawn the Advocate and the Skeptic as sub-agents **in a single message**, so each writes its opening case without the other's in context — two cases formed at the same moment cannot anchor on each other, and weighing them against each other only means something if they were formed apart. The Mediator runs after both return.

When sub-agents are unavailable, simulate the roles sequentially and name the run **degraded mode** in the issue body: the Skeptic reads the Advocate's case before writing, so its independence is gone and the verdict should be read accordingly. Degraded mode has no sub-agents to reply, so the reply round below does not run.

The Mediator may then call **one** reply round — see its gate below. Send both replies in a single message, so the independence that governs the opening cases governs the replies too. Each reply quotes the specific claim it answers, says what it concedes and what still stands, and stays under 250 words. The roles need not agree; the objective is the right answer rather than the win (Liang et al., *Multi-Agent Debate*).

Discard a reply that concedes without quoting a claim, and rule on the opening pair instead, noting the discard in the verdict. A reply that performs agreement is the failure this round is most likely to produce, and it reads exactly like a good one (Du et al. call it *sycophancy*: an agent names a peer's error, then adopts it anyway).

#### Agent 1: Advocate

The Advocate makes the strongest good-faith case for the change.

The Advocate should answer:

- What pipeline problem is being solved?
- Why does the current repository fail to address it?
- What improvement would reduce future failures?
- What instruction, section, or skill, if any, should be **removed or consolidated** to address this? Subtraction is a first-class option, not a fallback.
- Why is the proposed change better than leaving the pipeline alone?
- What exact files or skills likely need to change?

The Advocate must cite at least one loaded library source that supports the change — a named principle, checklist item, or design guideline. If no book in the surveyed set supports the proposal, say so explicitly; an unsupported advocacy case is a signal, not a thing to paper over.

#### Agent 2: Skeptic

The Skeptic makes the strongest good-faith case against the change.

The Skeptic should look for:

- overfitting the pipeline to one incident
- duplication of guidance that already exists elsewhere
- boundary erosion between skills
- accidental complexity or extra ceremony
- recommendations that would burden ordinary users who are not trying to improve the pipeline
- evidence that the issue was downstream and not structural here
- adds a feature whose cost is paid by every future user (Norman's featuritis, paired with Meadows policy resistance)

The Skeptic must cite at least one library source or established principle that warns against the change or names a known failure mode the change could create (for example, Nygard on accidental coupling, Meadows on policy resistance, Ousterhout on shallow modules, Fowler on premature abstraction).

#### Agent 3: Mediator

The Mediator synthesizes the two positions and decides what best serves the whole repository.

Before writing the verdict, attribute every decisive point to quoted text from one of the two cases. Call the reply round when a decisive point has no source in either case, or when the cases contradict each other on a checkable fact. Otherwise record **no reply round** and rule. Attribution is the gate because a Mediator that supplies its own arguments does not notice that it has.

The Mediator should produce one of four verdicts:

- **Reject** — not a pipeline problem or the proposed fix would harm coherence
- **Defer** — promising, but needs more evidence or wider repo review
- **Proceed narrowly** — make a small targeted change with limited blast radius
- **Proceed broadly** — a cross-repo update is warranted because multiple artifacts must stay in sync

The Mediator must name:

- the minimal coherent change set
- repo-wide risks
- what should explicitly remain unchanged
- what evidence would later justify revisiting the decision

The Mediator must reconcile the Advocate's and Skeptic's cited sources. If both roles cited the same book to opposite ends, surface that tension in the verdict narrative rather than resolving it silently — disagreement between principled readings of the same source is useful information for a future reviewer.

### Phase 5: Search for Related Issues, Then File the GitHub Issue

Search for related issues in `chrislacey89/skills` before filing anything new.

```bash
gh issue list -R chrislacey89/skills --search "<keywords>" --state all
```

- Search open and closed issues using the pipeline area, skill names, and the clearest failure-mode keywords from the incident.
- If an existing issue already covers the same problem, update or comment on it instead of filing a duplicate.
- If an existing issue is related but distinct, file the new issue and cross-link both.

Only after the overlap check, file the proposal as a GitHub issue in `chrislacey89/skills`.

```bash
gh issue create -R chrislacey89/skills
```

Use a concise issue title that names the pipeline area and the improvement opportunity.

Suggested title convention:

`[improve-pipeline] <short summary of pipeline change>`

Example:

`[improve-pipeline] Clarify execute skill boundary for behavior-heavy frontend work`

The `## Field Incident` and `## Why This Is a Pipeline Problem` sections carry the plain-language walkthrough for this artifact — a reader picking up the issue six months from now should be able to follow what happened and why it matters without opening the downstream repo. Meet the shape and revision bar in `references/writing-for-humans.md` (bundled alongside this skill): domain setup in the user's own words, a front-loaded lede, each recommended change motivated, and a `**Why it matters:**` signpost. The analytical sections (`## Advocate Case`, `## Skeptic Case`, `## Mediator Verdict`) sit beside the walkthrough and stay as tight bullets or short paragraphs — they are not another walkthrough.

**Before writing the Recommended Changes table.** For each row with a target file, open the file and confirm the proposed structure exists — a row that says "add a Quick Reference table entry" is only valid if the target file has a Quick Reference table. Substance and placement are decided in the same read, not in two passes. For proposals that add a new skill bundling a `docs/`-rooted reference, the table must include a `scripts/skill-references.manifest` row alongside the SKILL.md and discovery-doc rows; the bundled-references invariant in `CLAUDE.md` § Shared reference files requires it, and `scripts/sync-skill-references.sh --check` will fail at commit time otherwise.

Use this issue body template:

```markdown
**Target repo:** chrislacey89/skills
**Date:** YYYY-MM-DD
**Status:** proposed
**Triggering repo:** <repo-name>
**Triggering context:** <feature, issue, or branch>
**Pipeline area:** <skill, doc, checklist, or repo-wide>
**Change type:** prompt | workflow | checklist | artifact | terminology | boundary | other
**Confidence:** low | medium | high

## Field Incident

[What happened in the downstream repo. Keep this factual and concrete.]

## Pipeline Run Breakdown

- **Path run:** [/shape → /research → ...]
- **Expected behavior:** [What the pipeline should have enabled or prevented]
- **Actual behavior:** [What actually happened]
- **Introduced at:** [Where the weakness entered]
- **Missed by:** [Which step failed to catch it]
- **Cost:** [Rework, confusion, false confidence, missed edge case, etc.]

## Why This Is a Pipeline Problem

[Explain why this belongs in the pipeline repo rather than only in the downstream app repo.]

## Repo-Wide Context

[List the repository areas reviewed and what each implies for the proposal. Include the canonical docs plus the closest affected and adjacent skills.]

- `path/to/file` — [Why it matters]
- `path/to/other-file` — [Why it matters]

## Library Consultation

- **Books surveyed:** [brief notes from `/library` index or `/library --search <keywords>`, or "Library consultation: unavailable"]
- **Books loaded:** [names of books loaded via `/library <name>`]
- **Key principles applied:** [1–3 bullets, each tied to a specific book and the concrete idea borrowed]

## Suggested Further Reading

**From the library** (already available via `/library <name>`):

- `<book-name>` — [one line on why this book is worth loading before implementing or reviewing this proposal]

**Gap in the library** (not yet available; worth acquiring):

- `<Title> — <Author>` — [one line on why this book would have sharpened the analysis and what topic area it fills]

If no gap is identified, remove the Gap subsection rather than leaving a placeholder.

## Advocate Case

[The strongest argument for making the change.]

**Reply:** [The Advocate's answer to the Skeptic. Omit when no reply round ran, or when the reply was discarded.]

## Skeptic Case

[The strongest argument against making the change.]

**Reply:** [The Skeptic's answer to the Advocate. Omit when no reply round ran, or when the reply was discarded.]

## Mediator Verdict

**Verdict:** Reject / Defer / Proceed narrowly / Proceed broadly

[The synthesis. State the minimal coherent change set and the key repo-wide tradeoffs. When the dialectic ran in degraded mode, say so here and say what it cost: the Skeptic read the Advocate's case before writing, so the two positions are not independent and the verdict should be read accordingly.]

## Recommended Changes

| Target file | Change type | Change | Why | Risk if skipped |
|-------------|-------------|--------|-----|-----------------|
| `path/to/file` | add \| modify \| remove \| consolidate | [Specific recommendation] | [Rationale] | [Consequence] |

For any `remove` or `consolidate` row, add a `Text removed (with location):` line directly under the row quoting the exact text being cut and the section it lives in. This prevents Chesterton's-fence deletions and gives reviewers something concrete to evaluate.

## Non-Goals

[What this proposal intentionally does not change.]

## Follow-On Options

- **Proposal only:** stop here and review the issue
- **If approved:** implement the recommended file changes in a separate step in `chrislacey89/skills`

## Related Evidence

- [Link to issue, PR, transcript excerpt, or prior proposal]
```

Do not pad sections. If a section has no substance, tighten the proposal rather than writing filler.

If labels exist in the repository for maintenance or pipeline work, apply them. If they do not exist, do not block on label management.

When the proposal's "Gap in the library" subsection names one or more books the library should acquire, apply the `library-gap` label so these issues accumulate as a visible backlog rather than sitting buried in issue bodies. If the label does not yet exist in `chrislacey89/skills`, create it once with:

```bash
gh label create library-gap -R chrislacey89/skills \
  --description "Proposal surfaces a book the /library should acquire" \
  --color BFD4F2
```

Then apply it to this and future issues. If label creation fails (permissions, network), do not block filing — note in the issue body that the label should be applied later.

### Phase 6: Review Before Any Implementation

Present the proposal and review it with the user one question at a time.

Minimum review sequence:

1. Is the incident framing accurate?
2. Is the Mediator verdict the right one?
3. Does the recommended change set respect repo-wide coherence?
4. Should this remain an issue for later triage, or do you want approved follow-on implementation now?

Do not begin editing pipeline files until the user has reviewed the proposal and explicitly asked for implementation.

### Phase 7: Optional Follow-On Implementation

Implementation is optional and never the default.

If the user approves implementation:

- update the minimal coherent set of files named in the proposal
- search for overlapping guidance before editing any central skill
- keep terminology aligned across touched artifacts
- prefer the smallest repository change that fixes the structural problem
- if the proposal affects invocation boundaries, update every relevant skill that encodes those boundaries

After implementation, report:

- what files changed
- what intentionally did not change
- what future incidents would validate or falsify the improvement

## Verification

A run of `/improve-pipeline` is not complete until all of the following are true:

- the target repo was explicitly treated as `chrislacey89/skills`
- the canonical context was loaded from `README.md`, `SYSTEM-OVERVIEW.md` (or `references/SYSTEM-OVERVIEW.md`), `CLAUDE.md`, `docs/skill-anatomy.md` (or `references/skill-anatomy.md`), and `docs/writing-for-humans.md` (or `references/writing-for-humans.md`)
- the `## Field Incident` and `## Why This Is a Pipeline Problem` sections meet the walkthrough shape and revision bar in `references/writing-for-humans.md`
- the nearest affected skill and adjacent overlapping skills were reviewed
- the Advocate and Skeptic were spawned in one message and neither received the other's case, or the filed issue names the run as degraded mode
- the issue records the reply round's outcome as exactly one of: **replies kept** (they appear under the two case sections), **reply discarded**, **no reply round** (the gate did not fire), or **degraded mode** (there were no sub-agents to reply). Only *no reply round* counts as a gate non-fire when judging whether the round earns its place
- `/library` was surveyed (or its absence was recorded), and any loaded books are cited in the issue under Library Consultation and/or Suggested Further Reading
- related issues in `chrislacey89/skills` were searched before filing or updating
- an issue was filed or updated in `chrislacey89/skills`, or filing was intentionally deferred with a stated reason
- if the proposal recommends removal or consolidation, the issue cites the exact text being cut and the reason it is now redundant or counter-productive

## Repo-Wide Guardrails

- **Ground proposals in established guidance.** Before filing, consult `/library` for books relevant to the incident type and cite what they contribute in the issue. If `/library` is unavailable, record that explicitly rather than silently skipping the step.
- **Proposal first.** Do not jump from incident to repo edits.
- **Do not overfit.** One painful incident is evidence, not proof.
- **Protect ordinary users.** Most pipeline users are trying to ship work, not evolve the pipeline.
- **Search before editing.** If a recommendation touches one skill, inspect adjacent skills and shared docs before changing anything.
- **Name the blast radius.** Every proposal should say which files, skills, or conventions are affected.
- **Prefer the smallest coherent fix.** Resist sprawling “while we are here” pipeline rewrites.
- **Consider subtraction.** When the diagnosis is redundant, contradictory, or low-value guidance, the right fix is removal or consolidation, not another addition. Past invocations of this skill have skewed heavily toward additions; treat subtraction as a first-class outcome whenever the evidence supports it, and require equal evidence for it as for an addition.
- **Keep project knowledge in the project.** If the lesson belongs in the downstream app repo, use that repo’s normal documentation flow instead.
- **Capture findings in GitHub.** The default artifact is a GitHub issue in `chrislacey89/skills`, not a local proposal file.
- **Do not trust the current workspace remote.** A downstream repo may be where the incident happened, but it is never the issue target for `/improve-pipeline`.
- **Require canonical context.** Do not file a pipeline-improvement issue until the core repo docs and overlapping skills have been reviewed.
- **If canonical context or GitHub access is unavailable, stop and ask.** Do not guess, and do not file elsewhere as a fallback.

## What This Skill Is Not

- **Not `/compound`.** `/compound` captures durable knowledge for the downstream project. `/improve-pipeline` captures improvements for this pipeline repo.
- **Not automatic self-healing.** It recommends and optionally implements reviewed changes; it does not silently modify the pipeline.
- **Not a blame exercise.** It analyzes structural causes and repo-wide implications, not who made the mistake.
- **Not a local patch machine.** It should not “fix” one skill without checking the coherence of the repository around it.

## Handoff

- **Expected input:** a real incident or repeated friction encountered while using the pipeline, often discovered during `/compound` or `/pre-merge`
- **Produces:** a GitHub issue in `chrislacey89/skills` capturing the improvement proposal and supporting analysis
- **May follow with:** approved implementation of the proposal in `chrislacey89/skills`
- **Should be recommended by:** `/compound` or `/pre-merge` when present and when the main lesson is pipeline-level
