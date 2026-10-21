---
name: proposal-review
description: Review technical proposals, design docs, RFCs, architecture decision records, and PRDs against industry evaluation standards (ATAM risk/non-risk triage, reversibility, Google design-doc structure). Triages every gap by whether it can flip the decision rather than by how important it feels, separates "decide now" from "state honestly now", and drafts review comments at the right severity. Use this whenever the user is reviewing, critiquing, approving, or blocking someone else's proposal or design doc, when they are self-reviewing their own before publishing, when they ask whether an objection is fair or whether "we can decide that later" is an acceptable answer, or when they paste a PR review thread on a docs/ or proposals/ file. Also use for any request phrased as "is this proposal any good", "what am I missing here", "should I block this", or "help me push back on this design".
---

# Proposal Review

## The frame

A technical proposal is a request for a decision, not a description of a system. Everything in this skill follows from that.

The reviewer's job is not to find everything wrong. It is to answer one question: **does this document contain enough, and enough that is true, for the reader to make the decision it is asking for?**

That reframing matters because the most common reviewer failure is not missing a flaw. It is filing an objection at the wrong severity, which trains the author to route around the reviewer. The second most common is accepting "we'll decide that later" for something that cannot be deferred, or refusing it for something that can.

## Step 1: Establish the ask and the gate

Before reading for content, answer three questions. If the document does not answer them, that is finding number one.

- **What decision is being requested?** Approve a direction, approve a build, approve a spend, ratify something already built. The bar differs enormously.
- **What happens after approval?** If a detailed design phase follows, "later" is a real place and deferral is legitimate. If this document is the last gate before implementation, "later" means never and every deferral becomes a build-time surprise. Ask explicitly if the process is unclear. Most disputes about deferral are really disputes about whether a later gate exists.
- **Who is the audience?** A proposal for a peer group can assume shared context. One going to a cohort review or a funding decision cannot.

## Step 2: Inventory the claims

Read the document once and extract every load-bearing statement into one of three buckets. Do this before forming opinions.

| Bucket | Definition | Treatment |
|---|---|---|
| **Asserted** | The doc claims something is true or handled | Verify it. This is where the real findings live. |
| **Deferred** | The doc explicitly marks something open | Triage it in step 3. Deferral is often fine. |
| **Silent** | Something a system of this shape must handle, that the doc never mentions | Surface it. Silence is the most expensive category because nobody can review what is not there. |

Pay special attention to removals. When a proposal deletes an existing component, the "what replaces it" column is an assertion, and an unsupported one is the highest-yield finding in any review. A proposal that removes something and does not say what covers its job is taking credit for a simplification while leaving the cost off the ledger, which distorts the exact comparison the proposal exists to support.

## Step 3: Triage every gap

Run each gap from step 2 through these tests in order. Stop at the first one that produces a severity.

### Test A: Honesty (blocking, always)

Does the document assert that something is handled when it is not? Is a mechanism named that does not do the job attributed to it?

This is the only unconditional block, and it is the cheapest to fix, because the remedy is a sentence rewrite rather than a design decision. A doc may say "open". A doc may not say "solved by X" where X does not solve it. Never let a schedule argument ("we'll decide later") answer an accuracy objection: they are different claims. Separate them explicitly in the comment.

### Test B: Flip (blocking if yes)

If this unknown resolves in the worst plausible way, does the recommendation change?

This is ATAM's risk versus non-risk distinction, and it is the single most useful discipline in the skill. Risks threaten a business driver and stem from ambitious quality goals, novel technology, or genuine uncertainty. Non-risks are well-understood areas with known solutions. Sensitivity points, where a small change produces a large effect on a quality attribute, are candidate risks until classified.

Applied concretely:

- **Selection risk**: several known solutions exist, one must be picked. Deferrable. Examples: which lock primitive, which queue, which serialization format, which cloud region.
- **Feasibility risk**: it is not established that any solution exists at the required cost. Not deferrable. Examples: an accuracy target nobody has hit, a latency budget the chosen substrate cannot meet, a component whose behavior the proposal assumes but has never been observed.

A feasibility risk is decision-flipping by construction. A selection risk almost never is. Reviewers who treat selection risks as feasibility risks get dismissed, correctly, and then get ignored on the feasibility risks that follow.

### Test C: Door (raises severity)

Is the decision reversible? Irreversible or nearly irreversible choices, one-way doors, warrant methodical and deliberate scrutiny; reversible ones can be made fast and reopened later if suboptimal. Organizations that apply one-way-door process to two-way-door decisions get slowness and unthoughtful risk aversion, so calibrate hard in both directions.

Practical markers of a one-way door in software: public API or wire-format commitments, data migrations that lose information, schema changes that are expensive to reverse once customer data lands, vendor lock-in, anything that ships to customers as a billing or compliance artifact, and org-shaped choices that become team boundaries.

### Test D: Ledger (raises severity)

Does the proposal claim a benefit whose cost is unspecified? Removed components, absorbed responsibilities, and "the framework handles it" all belong here. The finding is not that the design is wrong. It is that the comparison is inflated, which corrupts the decision even if every individual statement is defensible.

### Test E: Cross-cutting coverage

Check the standard concerns explicitly, because these are the ones teams reliably forget and the reason design-doc templates carry dedicated sections for them. Not every concern applies to every proposal; note the ones that do and are missing.

- Failure modes and partial failure. What happens on crash, retry, duplicate delivery, concurrent execution.
- Correctness and data integrity. Lineage, idempotence, reconciliation, what a wrong output costs downstream.
- Security and privacy, including anything that changes a trust boundary.
- Observability. Can you tell whether it is working, and can you attribute cost.
- Migration and rollback. How the system gets from here to there, and what happens if it must go back.
- Operability. Who is paged, what they do, what the manual override is.
- Testing strategy, especially for anything nondeterministic.

### Test F: Alternatives

A proposal without an alternatives section is not yet a proposal, it is an advocacy document. The section exists to force the author to consider what else could achieve the goals, including using an existing system, buying something, or doing nothing. Check that the alternatives are real rather than strawmen, and that "do nothing" is among them when the status quo is functional.

Everything that survives all six tests without triggering is a nit. File nits separately or not at all.

## Step 4: Check yourself before filing

Run this pass every time. It is what separates a review that changes the document from one that gets resolved-as-wontfix.

- **Is this a correctness objection or a taste objection?** Both are legitimate to raise; only the first is legitimate to block on. Label which one you are making.
- **Would I accept this gap if I had written the doc?** If yes, downgrade.
- **Am I asking the author to design inside a proposal?** Proposals establish shape. Demanding a full mechanism inside one is scope creep by review, and it is the fastest way to lose the argument even when the underlying concern is real.
- **Is my analogy proportional?** Comparing a solved engineering problem to something physically unavailable is rhetorically satisfying and strategically fatal. The author dismisses the analogy and dismisses the finding with it. Analogies in reviews should undersell, not oversell.
- **Am I spending capital on a two-way door?** Count how many blocking comments you have filed. If everything is required, nothing is.

## Step 5: Write the findings

Order by severity, not by document order. Use this structure.

```
## Summary
[One paragraph: what decision is being asked for, and whether the doc currently supports it.
State the recommendation up front: approve, approve with required edits, or not ready.]

## Blocking
[Findings that fail Test A or Test B. For each:
- What the doc says, quoted or cited by line
- Why it is wrong or decision-flipping
- The smallest change that resolves it]

## Required before build
[Real gaps that do not flip the decision but must not be lost. Each one should name an owner
or a follow-up artifact, otherwise it evaporates.]

## Open questions to record
[Things that are legitimately deferred. The ask is not to answer them, it is to list them in
the doc so the deferral is visible to whoever approves.]

## Nits
[Everything else, explicitly non-blocking.]
```

## Comment craft

The wording of an individual comment decides whether it lands.

**Ask for the smallest change that fixes the actual problem.** If the problem is an inaccurate sentence, ask for a sentence edit, not a design. An ask the author cannot refuse without defending a false statement gets accepted. An ask that requires a week of design gets deferred, and your accurate observation gets deferred along with it.

**Separate the two asks when a comment contains both.** Timing is negotiable; accuracy is not. Concede the timing explicitly and hold the accuracy. This costs you nothing and removes the author's easiest exit.

**Example.**

Weak (conflates accuracy with design, invites deferral):
> [Required] The checkpointer does not do this. If the lock goes, something has to replace it. Name that mechanism here.

Strong (concedes the deferral, holds the falsehood, asks for an edit):
> The checkpointer persists state, it doesn't arbitrate two sessions racing on the same output prefix. So this cell is wrong as written. Fine to defer the mechanism, but change it to "Open: concurrency control undesigned" and list it under Open Questions.

**Do not mark selection risks as required.** Save the required label for Test A and Test B findings. A review where three comments are marked required and one of them is genuinely blocking is worse than a review with one.

**When the author refuses to record a deferral**, escalate on process rather than on the technical point. Refusing to list a known gap in an Open Questions section is a documentation-quality position, not a design position, and it is much harder to defend in front of a wider review group than the underlying technical disagreement would be.

## Self-review mode

When the user is the author rather than the reviewer, run the same six tests against their own draft and report the findings they would receive. Add two checks:

- Every removal in the proposal has a named replacement or an explicit open question.
- Every "handled by X" phrase has been verified against what X actually does, particularly for framework and library capabilities. Attributing behavior to a dependency that it does not have is the single most common falsifiable error in design docs.

## Voice

Review output lands on two different surfaces, and they need different voices. Route by surface, not by preference.

### Written surfaces: PR comments, review docs

Write these in a terse, fragmented, command-style register. Short declaratives. Fragments are fine. No narrative build-up, no spoken filler, no mid-sentence restarts, no check-ins like "does that make sense?". If a personal voice skill is installed (for example `voice-of-er`), consult it for additional speech-fingerprint detail, but this section stands alone and does not require it.

**Length is a hard rule, not a preference.** Three sentences maximum per comment. Blocking findings get four. If a finding needs more than that, it is not sharp enough yet, or it belongs in the review doc rather than an inline comment. Nobody reads a paragraph in a PR thread. An essay-length comment gets skimmed and resolved.

**Shape: what is wrong, why, the ask.** One line each, in that order. Delete any sentence that is not one of those three.

Rules:

- **No preamble.** Not "Great writeup, one thought", not "I might be missing something here, but". Open with the finding.
- **One qualifier or none.** "I think we should maybe consider possibly" is four. Pick zero.
- **Name the thing.** File, line, mechanism, number. Never "there may be concurrency issues"; write "two sessions on the same output prefix will race".
- **Technical terms naked.** No parenthetical definitions, no "also known as".
- **Do not sanitize.** If the doc is wrong, write that the doc is wrong. Correctness objections do not get softened into suggestions.
- **Never-says list applies fully.** No em dashes. No "stakeholders", "leverage", "end-to-end", "comprehensive", "robust", "seamless", "that said", "nuanced", "deep dive", "it's important to note", "this is where it gets interesting". No rule-of-three constructions.

**Final scrub before posting.** Strip these AI tells directly:

- Em dashes. Use commas, periods, or split the sentence.
- Rule-of-three lists ("faster, cleaner, and more maintainable"). Cut to one or two.
- Negative parallelism ("not just X, but Y"). Rewrite as a plain statement.
- Promotional adjectives: comprehensive, robust, seamless, powerful, elegant, significant.
- Vague attribution: "industry best practice", "it is widely understood", "experts recommend". Name the source or drop the claim.
- Superficial -ing analysis: "highlighting the importance of", "underscoring the need for", "reflecting a broader shift toward".
- Conjunctive padding: "furthermore", "moreover", "additionally", "that said", "it's important to note".
- Symmetrical sentence lengths. Three consecutive sentences of similar length is the strongest tell. Break the pattern.

If a `humanizer` skill is available, run it as a second pass. The list above is the floor and applies whether or not it exists.

**Examples.**

Blocking accuracy finding.

Wrong (essay, hedged, buried ask):
> Thanks for putting this together. I may be misreading the table, but I wanted to raise a concern regarding the concurrency story. My understanding is that the LangGraph checkpointer is primarily a state persistence mechanism, and I'm not sure it provides the mutual exclusion guarantees that the RunCoordinator lock was previously responsible for. It's possible I'm missing context here, but I think it might be worth considering whether we should clarify this in the document or perhaps defer it to a follow-up.

Right:
> The checkpointer persists state, it doesn't arbitrate two sessions racing on the same output prefix. So this cell is wrong as written. Fine to defer the mechanism, but change it to "Open: concurrency control undesigned" and list it under Open Questions.

Silent gap.

Wrong:
> One thing that occurred to me while reading through the proposal is that there doesn't appear to be any discussion of what happens in a partial failure scenario, which I think could be worth exploring further at some point.

Right:
> Nothing here covers partial failure. What happens if the agent dies mid-run with half the outputs written? Needs an answer before build, not before merge.

Nit.

Wrong:
> Very minor point and feel free to ignore, but I noticed the terminology seems to shift slightly between sections and I wondered if it might be clearer to standardize.

Right:
> Nit: "skill bundle" in section 3, "vertical" in section 5. Pick one.

### Spoken surfaces: standup, cohort review, defending a blocked finding live

Spoken output is the opposite register from the comments. Verbose, chronological, narrative. Lead with the problem and walk forward to the conclusion, never conclusion-first. Casual connectors ("so", "basically", "and then", "the thing is", "right?"). Concrete numbers and tool names dropped without preamble or definitions. At least one unfiltered take per answer. Vary sentence length hard, long then short then medium. End on a blunt line or a question back, not a summary.

If a personal voice skill is installed (for example `Skill("voice-of-er")`), invoke it and let it own this transformation. If not, the paragraph above is enough to work from.

When the user asks for talking points, a verbal response to pushback, or anything they will say rather than post, transform the findings into this register before returning them.

If it is ambiguous which surface the output is for, ask. Posting spoken-voice text into a PR thread is a worse failure than asking one question.

## Grounding

These references exist so findings can be framed as standard practice rather than personal preference. Cite them when an author pushes back on the process itself.

- **ATAM** (Kazman, Klein, Clements, SEI/CMU): scenario-driven architecture evaluation producing risks, non-risks, sensitivity points, and tradeoff points, synthesized into risk themes showing how each threatens a business driver. Source of the flip test. https://www.sei.cmu.edu/documents/629/2000_005_001_13706.pdf
- **Design Docs at Google** (Malte Ubl, Industrial Empathy): the alternatives-considered section as a fixed structural requirement, and dedicated cross-cutting-concern chapters so privacy, security, scalability, and monitoring are never left implicit. https://www.industrialempathy.com/posts/design-docs-at-google/
- **One-way and two-way doors** (Bezos, 2015 Amazon shareholder letter): scrutiny scaled to reversibility, and the explicit warning against heavyweight process on reversible decisions.
- **Architecture Decision Records** (Michael Nygard): decision records carry context, decision, and consequences. If a proposal states a decision without its consequences, the record is incomplete.
- **RFC 2119**: when a proposal uses must/should/may, hold it to those meanings. Vague modal verbs in a spec are a finding.

---

## Changelog

### v1.3
- Removed all hard dependencies on external skills. `voice-of-er` and `humanizer` are now optional enhancements; the skill is self-contained without them.
- Inlined the typing-register definition for written comments (terse, fragmented, command-style, no spoken filler).
- Inlined the AI-tell scrub as an explicit eight-item checklist (em dashes, rule of three, negative parallelism, promotional adjectives, vague attribution, superficial -ing analysis, conjunctive padding, symmetrical sentence lengths).
- Inlined the spoken register for verbal surfaces (chronological, casual connectors, one unfiltered take, varied sentence length, no summary ending).
- No changes to Steps 1 through 5, the triage tests, comment craft, the length rule, self-review mode, or the grounding references.

### v1.2
- Written comments now use the author's personal typing register directly instead of a neutral written register. Reversed the v1.1 decision to hold `voice-of-er` back from written output.
- Added a hard length rule: three sentences max per comment, four for blocking findings. Longer means the finding is not sharp enough or belongs in the review doc.
- Added a fixed comment shape: what is wrong, why, the ask. One line each, delete anything else.
- Added rules against preamble and stacked qualifiers, plus three wrong/right example pairs (blocking finding, silent gap, nit).
- Shortened the example in `## Comment craft` so it obeys the new length rule.
- No changes to Steps 1 through 5, the triage tests, self-review mode, or the grounding references.

### v1.1
- Added a `## Voice` section that routes output by surface instead of applying one voice everywhere.
- Written surfaces (PR comments, review docs, one-pagers): explicitly do NOT apply the full `voice-of-er` skill. Apply only the four transferable traits (concrete specifics, naked technical terms, unsanitized directness, terseness proportional to the finding) plus the full never-says list, then pass the output through the `humanizer` skill.
- Spoken surfaces (standup, cohort review, live pushback): invoke `voice-of-er` in full.
- Added an ambiguity rule: ask which surface the output is for rather than guessing.
- No changes to Steps 1 through 5, the triage tests, comment craft, self-review mode, or the grounding references.

### v1.0
- Initial skill: decision-frame, claim inventory, six-test gap triage (honesty, flip, door, ledger, cross-cutting, alternatives), reviewer self-check, findings output format, comment craft rules, self-review mode, grounded in ATAM, Google design docs, one-way/two-way doors, ADRs, RFC 2119.
