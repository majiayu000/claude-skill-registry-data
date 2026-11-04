---
name: agent-defaults
description: Improve codebases so coding agents reliably do the right thing by default. Use for architecture, type/invariant, static-analysis, verification, agent-guidance, and review-process improvements; prioritize deterministic enforcement over prose and manual review.
---

# Engineer Agent-Friendly Defaults

Design the development environment so the easiest path is also the correct path. Prefer eliminating whole classes of mistakes over reminding agents to avoid them. Treat the controls as an inverse pyramid: spend most effort on deterministic codebase improvements, then automated verification, then concise prose, and reserve human review for the highest-leverage decisions.

## Priority order

1. **Codebase design — primary investment.** Make invalid states unrepresentable where practical. Strengthen types, schemas, contracts, invariants, module boundaries, APIs, and safe defaults. Remove ambiguous or duplicate paths that invite agents to imitate a weak precedent. Centralize policy and make the preferred implementation the simplest one. Fix causes categorically rather than adding case-specific patches or instructions.
2. **Static, executable verification.** Add or improve lint rules, type checks, tests, CI gates, property/model-based checks, and formal methods (including TLA+ where concurrency or protocol state warrants it). Make checks deterministic, fast, actionable, and hard to bypass accidentally. Verify both the intended behavior and the invariant that prevents recurrence. Prefer a cheap automatic check to repeated token-heavy inspection.
3. **Prose for irreducible judgment.** Use comments, repository rules, AGENTS.md, and skills only for choices that cannot reasonably be encoded or checked. Keep guidance concise, local, specific, and actionable; avoid duplicating enforced rules or maintaining broad generic checklists. Use `/create-verification-skill` when available to turn a recurring judgment-dependent verification procedure into a reusable skill. If unavailable, use the repository's existing skill format and state that limitation when relevant.
4. **Human review — scarce, high leverage.** Focus review on architecture, trust boundaries, threat models, consequential tradeoffs, and gaps automation cannot resolve. Do not use exhaustive manual review as a substitute for missing types, invariants, tests, or gates. Independent review should target the highest-risk residual uncertainty.

## Workflow

1. **Find the failure class, not just the symptom.** Inspect the implementation, callers, nearby conventions, existing checks, and known failure examples. Identify how an agent could plausibly copy the wrong pattern or take a shortcut. For recurring corrections, cite actual examples and group the shared cause rather than adding one rule per incident.
2. **Choose the highest layer that can prevent recurrence.** Ask in order: Can the architecture/API make this impossible? Can types/schema/invariants reject it? Can a deterministic check catch it? Is concise guidance genuinely still needed? Does a residual risk merit human review? Do not reach for prose or review before evaluating stronger layers.
3. **Make the safe path easy.** Minimize special cases and duplicated policy. Prefer a clear canonical abstraction and executable examples over warnings. Ensure migration or compatibility boundaries are explicit where needed.
4. **Test the invariant.** Demonstrate the new guard rejecting a representative past mistake in an isolated fixture or historical reproducer, then accepting the corrected case. A rule listed in AGENTS.md is not enforcement. Run the narrow check, then the repository gate when available. Report checks that could not run without implying success.
5. **Review residual risk.** For substantial architectural, security-sensitive, public-API, or cross-subsystem changes, obtain independent review if available. Ask reviewers to challenge the invariant, missed callers, bypasses, and unintended consequences—not just style. Keep review bounded to what automation cannot prove.
6. **Report the leverage.** Summarize the failure class eliminated, the layer that now enforces the behavior, verification evidence, and any remaining judgment-dependent risk. Do not claim a class of bugs is eliminated unless the invariant and its bypass surface support that claim.

## Design checks

- Is there one obvious, canonical way to do this, and is it the easiest way?
- Can callers construct invalid or contradictory states? Can types or constructors prevent that?
- Is the invariant enforced at the boundary where bad data or behavior enters?
- Can alternate entry points, escape hatches, test-only behavior, or legacy paths bypass the control?
- Does the test fail if the old bug returns? Is the check deterministic and cheap enough to run routinely?
- Is prose duplicating something the compiler, linter, or CI already enforces?
- What uncertainty remains that genuinely needs a human decision or review?

## Avoid

- Adding more instructions as the first response to a repeated agent mistake.
- Broad refactors unrelated to the failure class or task scope.
- Tests that only mirror implementation details or pass without proving the invariant.
- Formal methods as decoration; use them when the state space, concurrency, or protocol justifies their cost.
- Treating an agent-generated review, a green test suite, or prose compliance as proof beyond the evidence each supplies.
