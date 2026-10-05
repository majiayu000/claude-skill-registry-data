---
name: delegate-work
description: "Brief a background agent, confirm the brief arrived, and verify its report before acting on it. Use when writing the prompt for a subagent or parallel session, when several agents will run against one repository, when an instruction sent to a running agent goes unmentioned in its report, when a delegated fix has been rejected and another verification round is about to start, or before relaying a delegate's report onward. Also use when a delegate's final report arrives as a fragment or refers to a message that never reached you. Do NOT use to measure a run's cost (audit-agent), to prove a green check could go red (prove-checks), or to check a delegated claim (research-it)."
metadata:
  author: Serghei Iakovlev
  version: "1.0"
  category: meta
---

# Delegate Work and Verify What Comes Back

Your only view of delegated work is the delegate's own account of it. That account is written by the one party with an interest in it reading as complete, from a context you cannot inspect, and it is silent in exactly the places where it is wrong. A report that says nothing about instruction four is indistinguishable from a report whose author never received instruction four.

The defense is not skepticism, it is structure: make each instruction produce a named artifact, then check the artifacts instead of reading the prose.

`research-it` owns what a delegated *conclusion* is worth (a claim, not evidence). `prove-checks` owns whether a *check* could have gone red. This skill owns the orchestrator's side of the exchange: the brief, the delivery, and the report as a whole.

## Trigger

- A prompt for a subagent, a background agent, or a parallel session is about to be written.
- Two or more agents will run against the same repository or worktree.
- A correction, a scope change, or a new instruction was sent to an agent that is already running.
- A returned report is about to be relayed to a user, quoted, or used as the input to the next delegation.
- The delegated work is expensive enough that re-running it is not the cheap fix.

Not this skill: measuring what a run cost (`audit-agent`), proving a green check was capable of failing (`prove-checks`), or deciding whether a technical claim the delegate made is actually true (`research-it`).

## Procedure

### 1. Hoist the standing guardrail block out of the brief

Anything repeated into a second brief is written down once and referenced, never retyped. Four hand-copied blocks are four blocks that will drift, and the drift is invisible: each brief looks right on its own.

Keep one file (a shared brief fragment, a section of `AGENTS.md`, or a skill the brief names) covering the categories below. The instances are project-specific; the categories are not.

| Category | What it must settle |
|---|---|
| Isolation | The assigned checkout or directory, the files the agent may change, and where runtime tests run in isolation. A separate worktree is optional; a shared checkout requires preserving other sessions' changes. |
| Forbidden commands | The exact commands that would destroy a parallel session's uncommitted work. Name them; "be careful with git" is not an instruction. |
| Gate selection | How this project's checks choose the files they check, when that differs from "everything". |
| Evidence standard | Real command output pasted, not paraphrased. A summary of a gate run is not a gate run. |
| Negative control | Required before any green counts. Defer to `prove-checks` rather than restating it. |
| Report contract | What the report carries and what it must not: the answer that was asked for, and nothing appended the caller did not ask for. A delegate has no standing to propose changes to the caller's tooling and no one on its end to approve them. |
| Incremental findings | Findings written to a file as they accumulate. Defer to the working agreement's reporting rule rather than restating it. |

The gate-selection row is the one most often skipped and the most expensive to skip. In this repository every file-selecting `make` gate selects its inputs through `git ls-files`, so a new file that is not yet indexed is silently skipped and the gate can still exit 0. A brief that omits this gets a green report about a file nothing read.

### 2. Keep your own unchecked claims out of the brief

`research-it` tells the receiver that the brief which reached it is not a source. This is the same rule from the sending end: a number you computed, a count you eyeballed, a classification you inferred, or a statement about what the project's own tooling does becomes unfalsifiable the moment it enters a brief as a fact, because the agent will build on it rather than check it.

State provenance, and grant standing to refute:

- Not: *"Remove the 26 new violations and leave the 43 pre-existing ones."*
- But: *"I count 26 new and 43 pre-existing. That count is mine and unverified. Derive it yourself, and if it disagrees, report the disagreement and act on your number."*

The second form costs one sentence and converts a silent corruption into a finding. A brief that encodes a verifier's arithmetic as fact has laundered an unchecked claim through the authority of an instruction.

The class this misses most often is not arithmetic. A brief that names a gate ("`lint-markdown` runs over this too, check you did not break it") has asserted a pathspec, and the pathspec sits in the build file one `grep` away, which is why the sentence reads as background rather than as a claim. Read the selector before writing the sentence: step 1's gate-selection row is a fact about the repository, not a slot filled from memory. A named gate that does not cover the file sends the delegate to collect a green that was never about its work.

### 3. Give every instruction a named artifact

A brief that says "do X" can only be verified by reading a report about X. A brief that says "do X, which leaves artifact Y" can be verified against the filesystem, without the report and without trusting it.

Generalize the pattern this repository already uses in its own pipelines: gate on a literal token that a tool prints, not on prose that can be reworded. `composer` requires the string `VALIDATION_RESULT=PASS` pasted verbatim and treats "the validator was clean" as a failed gate. Apply the same shape to every instruction that matters:

| Instruction shape | Artifact to name in the brief |
|---|---|
| Run a gate | The gate's own final line, pasted verbatim |
| Add a target, rule, or config key | The file and the exact key, greppable |
| Fix N occurrences | The count command, and its output before and after |
| Write findings | The path written to |

Instructions with no artifact are the ones that vanish without trace. Sort your brief by that test before sending it.

### 4. Confirm the message arrived, in both directions

A message to an already-running agent can fail to deliver in silence. The send returns without error, the agent never sees it, and its final report describes everything it *did* receive as complete. Nothing in the report marks the hole.

Confirm against the artifact from step 3, never against an acknowledgment:

1. For each mid-flight instruction, name the one artifact it must leave.
2. When the agent reports, grep for that artifact directly. Do not search the report for a mention of it.
3. If the artifact is absent while the rest of the report reads as complete, treat the message as undelivered, not as disobeyed. Resend the instruction alone, with its artifact restated.
4. Record the resend. An instruction delivered on the second attempt was executed with different surrounding context than the first batch.

This check is cheap and it is the only one that catches a dropped message. It costs one grep per mid-flight instruction.

The return leg fails the same way and reads worse. A final report can reach you as a fragment, an appendix, a closing section, one of several messages, while the delegate's own record shows it sent the whole thing. The fragment is well-formed and confident, so it presents as a short report rather than as the tail of a long one. Two markers give it away: a reference to a message you never received, and a step-3 artifact missing from a fragment that never claims to have skipped it.

A fragment is a transport failure, not a thin report and not work left undone. Ask for the missing part to be resent, and settle the substance from the artifacts while you wait, because the tree already holds what the missing prose would have told you. Do not re-run the work and do not re-brief the agent; both spend a full run to recover text that already exists.

### 5. Verify the report in cost order

Run these against the artifacts, in this order. Each is cheaper than the one below it and catches a different class.

1. **Omission.** For every instruction in the brief, check its named artifact exists. This is the class the report structurally cannot fake, and the only one that surfaces an undelivered message. Do it first and do it from the brief, not from the report's own section list: a report organized around what it did will not have a section for what it did not.
2. **Unsourced numbers.** Any figure not accompanied by the command that produced it is unsourced, including figures that agree with your own. Re-run the command.
3. **Quotes.** Grep each quoted string in the file it is attributed to. A quote that matches nothing is fabricated, and a plausible fabricated quote is the single most damaging thing a report can carry downstream.
4. **Propagated premises.** Any claim the report inherited from your brief is still your claim wearing the delegate's authority. It has been through no check at all. Mark these before relaying anything.

A second agent is a purchase, and the price is judged against what a wrong result costs to recover from, not against how much the work mattered. Recovery usually means redoing the work, so a result you can rebuild in a minute is cheaper to re-derive than to get a second opinion on: one check is the whole budget. Reserve the rounds below for work where redoing is not recovery, because it is slow or unrepeatable, or because a wrong result reaches something you cannot take back.

**When the work is expensive or unrepeatable, verify with a second agent, and do not hand it the first report, unless the orchestrator's own protocol caps its delegations.** An agent given the first report reads it, agrees with it, and returns a confirmation; anchoring is the failure mode, not laziness. Give the second agent the brief and the tree, and ask it to rebuild the checks independently. Two roles that pay for themselves: one reading the run's own transcript for whether cited sources were actually fetched and whether gates ran in the claimed order, and one reconstructing the negative controls from scratch. The second routinely finds defects the first report's own self-check reported clean.

### 6. When the verdict is reject, run the next round

A rejected fix starts a loop, and the loop has its own failure mode: each round re-tests the last round's defect and finds nothing new. Round N is worth running only if its verifier could catch something round N-1 structurally could not.

**Steer by defect class, never by findings.** Step 5 forbids handing over the previous report. It does not forbid saying what went wrong in the abstract. Pass the category ("the fix over-blocks legitimate input") and withhold the corpus, the examples and the verdict. The category is one clause and constrains nothing; a worked example silently becomes the next verifier's test plan.

**Make the verifier derive its corpus from the pattern's grammar, not from the conversation.** Cases assembled from what has already been discussed can only rediscover what has already been found. Put the provenance of the corpus in the brief as an instruction: enumerate the forms the pattern itself admits, then test those.

**Spawn the verifier fresh; resume the author.** A verifier that already returned a verdict holds its own corpus and will re-run it, so resuming it buys a second opinion on the first opinion. The author is the party that needs the defect and the party whose context is worth keeping.

**Stop on what the round found, not on a count.** The loop ends on an accept from an independently generated corpus. It is thrashing rather than converging when a round rejects on something the previous round's corpus could already have caught, which means the rounds are re-testing each other instead of widening. A round budget fixed in advance measures neither.

### 7. Decide and record the scope

Close with **accept**, **resend**, or **re-verify**, and record what was checked against artifacts versus what was taken on the report's word. "Steps 1 to 3 verified against the tree; step 4 is the delegate's account" is worth more downstream than "the agent completed the task".

## Boundary with fixed pipelines

An orchestrator that has no terminal, such as this repository's `composer` and `conductor`, is told to verify artifacts through delegation rather than by opening a shell. That is correct for them: they cannot run the check, and re-reading costs them a context round trip they were built to avoid. It is not a general rule. When the orchestrator does hold the tools, one grep against the tree beats any amount of parsing the report, and step 4 exists because a report parsed carefully still passed.

## Validation

A delegated result is accepted only when all of these hold:

- [ ] The brief's repeated guardrails came from one file, not from retyping.
- [ ] Every number and classification the brief asserted was labeled as unverified, with standing to refute.
- [ ] Every gate the brief named was checked against its selector in the build file rather than recalled.
- [ ] Every instruction that matters named an artifact, and the artifact is a token or a path, not a claim.
- [ ] Each named artifact was checked against the filesystem, working from the brief rather than from the report's contents.
- [ ] Every quoted string was found in the file it was attributed to.
- [ ] Every number was reproduced by re-running its command.
- [ ] Any mid-flight instruction whose artifact is missing was resent rather than assumed refused.
- [ ] A report that referred to a message that never arrived was treated as truncated and resent, not read as complete.
- [ ] The final report distinguishes what was verified from what was taken on the delegate's word.
- [ ] In a multi-round loop, each round's verifier received the defect class rather than the previous findings, and generated its own corpus.

Any unticked box makes the result unverified, not wrong. Say which.

## Anti-patterns

- **Reading the report for plausibility.** A coherent, well-structured, confident report is the expected output of a delegate that went wrong, not a signal that it did not. Coherence is the one property the delegate optimizes for and the one property that carries no information.
- **Checking completion from the report's own outline.** The report enumerates what it did. The brief enumerates what was asked. Only the second finds the missing item.
- **Treating an acknowledgment as delivery.** A send that returns without error and an agent that received the message are different facts, and only one of them is observable from the tree.
- **Reading a fragment as the report.** A tail section that arrives alone is coherent on its own terms and carries no marker of what preceded it. A dangling reference to an earlier message is the report telling you it is incomplete; the artifacts, not the prose, settle what was actually done.
- **Accepting a self-audit.** "I verified X" inside a report is part of the report, written by the party under audit, and inherits none of the independence the word "verified" implies.
- **Anchoring the second opinion.** Handing the re-verifier the first report converts an independent check into a review of someone else's conclusions, which is a different and much weaker thing.
- **Retyping the guardrails.** Four copies of a block are four different blocks within a week, and no copy announces that it is the stale one.
- **Welding your own arithmetic into the brief.** The delegate will build on it, and the error becomes structural rather than local. Give it provenance and standing to disagree.
- **Re-asking the same agent.** A delegate confirming its own report is the writing path verifying itself. Verify through the tree.
- **Buying a verifier the work does not need.** When redoing the work is cheaper than a second opinion about it, the second opinion buys nothing, and the rounds past that point re-test each other instead of the work.
- **Fixing the round count in advance.** Three rounds is not a budget, it is what convergence cost once. A loop that stops on a number stops mid-defect, or runs past the point where the rounds began re-testing each other.
