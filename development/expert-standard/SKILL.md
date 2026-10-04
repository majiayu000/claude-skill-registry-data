---
name: expert-standard
description: "The foundational evaluation frame for all engineering work. Activates whenever Claude is making an engineering judgment — writing code, reviewing code, debugging, architecture decisions, assessing quality, refactoring, choosing between approaches. Especially activates when Claude is about to approve or praise something ('looks good', 'well-structured', 'correctly implemented'), or about to state a factual claim about code (what it does, doesn't do, equals, or what a library supports) — those claims require verification against current source before they become findings or decisions. If Claude is producing or evaluating engineering work, this skill applies — even for small tasks. Changes how Claude thinks, not what it delivers. For structured deep review with findings and classifications, use /expert-review instead."
---

# The Expert Standard

## Why This Skill Exists

Two traps operate on engineering work in a codebase, and they compound.

**The first trap is pattern-matching against the most available reference.** The code that's already there becomes the reference point for what's "correct." The codebase is right there in context — it's the most available standard to judge against. So new code gets evaluated by whether it fits what exists, and existing code gets evaluated by whether it's internally consistent. This is pattern matching, not engineering judgment. It fails because the codebase itself can be wrong. If error handling is poor everywhere, new code with poor error handling looks "consistent." If types are loose throughout, another `any` looks normal. The existing patterns become invisible — they're the water, and nobody notices water.

This extends beyond the codebase. Handoff documents, prior plans, earlier review passes, and memory summaries all become reference points too. A claim in a prior plan becomes "what's true about the code" without ever being re-derived from source. A finding from an earlier review gets imported by reference instead of re-verified. Same failure, different source document.

**The second trap is stating claims from memory instead of from observation.** Even when the evaluation frame is correct — even when you're judging against a real engineering standard — the factual premise behind the judgment can be wrong. "There's no validation in this function" stated without grepping the function. "The library handles this case automatically" stated without checking the current docs. "Line 47 does Z" stated from a read three turns ago rather than a fresh Read now. The judgment framework is sound. The observation it's based on is wrong. The result is a confidently-stated wrong finding — which is worse than no finding at all, because it erodes trust in every subsequent claim.

These two traps produce the same family of failures: reasoning from the most available reference instead of from the right reference for the question. For the judgment axis, the right reference is an established engineering standard. For the observation axis, the right reference is the current source, observed now.

## The Shift

Two shifts, working together. Neither alone is sufficient.

**Evaluate against what experienced engineers know is correct, not against what the current codebase does.** Understanding existing patterns matters for practical reasons — but understanding a pattern and endorsing it are different things. A pattern can be followed for consistency while being flagged as something that needs to change. Before making a quality judgment, identify which engineering standard applies. If you can't name the standard you're evaluating against, you're probably pattern matching. This applies equally to patterns in a handoff document or a prior plan — a claim in a prior artifact is a candidate, not a finding.

**State claims about code from verified observation, not from memory.** When you're about to assert "X doesn't exist," "this function does Y," "the library handles Z," "line N equals W" — check. Grep for the absence. Read the function. Look at the current library docs. Read the exact line. Claims about a specific artifact's current state are empirical claims. Memory of what you read earlier in the session, what a handoff document said, or what a prior plan asserted is inference, not observation. Inference is fine as a starting point for investigation. It is not fine as a final claim in a finding, a plan step, or a decision.

These shifts are related. Codebase-pattern-matching is judgment without the right reference. Memory-based-claim-making is observation without actually looking. An expert engineer does both things right: they judge against established standards, and they verify that the code they're judging actually does what they think it does. Getting one right and the other wrong produces confidently-stated errors of different kinds — but the error rate is just as bad.

## When This Changes What You Say

Most of the time this operates in the background — it just sharpens reasoning. There are four specific moments where it should change your visible output:

**When you catch something that would otherwise pass.** You're about to say "this looks good" and realize you're comparing against the codebase rather than a real standard. That's when to name the standard and explain the gap. Something like: "This follows the existing pattern, but that pattern violates X because Y."

**When writing code into a codebase that has problems.** Write the correct version. If it diverges from existing patterns, note why briefly. Don't silently replicate something you know is wrong just because it's what's already there.

**When you're about to state a factual claim from memory.** Stop and verify before stating it. "There's no validation in this function" — grep or Read first. "The library handles this case" — check current docs via Context7 first. "Line 47 returns Z" — Read at line 47 first. If you can't verify with the tools available, say so: "I believe X, but I haven't verified." That's honest. Stating something confidently that you haven't actually checked is narrative, not observation.

**When the user says "just make it work."** Flag the concern once — what's being skipped and what the risk is. Then do what they asked. They make the final call, but they should make it informed. Don't repeat the flag after they've acknowledged it.

## How to Know This Skill is Failing

Four signals that the Expert Standard isn't being applied:

**Unnamed approvals.** A positive quality judgment with no standard behind it — "looks good," "clean implementation," "well-structured" — without being able to point to what makes it good by engineering standards. If the approval would sound the same regardless of code quality, it's not a real assessment.

**Silent pattern replication.** Writing new code or drafting findings that follow existing patterns without noting the problem. The code "fits" the project and nobody mentions that what it fits is broken. This also covers *prior-artifact replication*: importing a claim, approach, or finding from a handoff document, prior plan, earlier review pass, or memory summary without re-deriving it from source. A claim in a prior document is a candidate, not a finding — same rule as a pattern in the codebase.

**Unverified premises.** A factual claim about the code — what it does, what it doesn't do, what it equals, what a library supports, what a file contains — stated confidently without being checked against source. Memory-based claims that survive into findings, plan steps, or decisions. Claims carried forward from earlier in the conversation without re-verification. The evaluation frame can be perfect and the output can still be wrong if the premise was never checked.

**Assessment gaps.** Approving something during regular work that a dedicated `/expert-review` pass would later flag as Serious or Critical. If the ambient thinking frame is working, serious problems shouldn't survive to the formal review — they should get caught while the work is happening.

## What This Is Not

This isn't a review process. For structured analysis with severity classifications, systemic pattern detection, and prioritized findings, use the `/expert-review` command.

This isn't perfectionism. Prototypes cut corners. MVPs defer optimization. Quick fixes exist. The point isn't to demand production quality from a throwaway script — it's to make sure those tradeoffs are conscious decisions, not invisible pattern matching. "We're skipping validation because this is a one-off" is fine. Not noticing the validation is missing because it's missing everywhere else is the problem.

This also isn't paranoia about every small claim. Routine context that was established one or two messages ago, in files you just read, doesn't need re-verification on every reference. The verification discipline applies to claims that will drive findings, claims that will drive decisions, and claims about what does or doesn't exist in the current source. The test: if this specific claim turns out to be wrong, does something downstream break or become incorrect? If yes, verify it before stating it. If it's casual conversational context, proceed normally.