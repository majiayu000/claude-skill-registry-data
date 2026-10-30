---
name: thatch-refine-oss-contribution
description: Type-specific requirements for refining a plan for a contribution to an open source repository the user does not maintain. Loaded by thatch-refine after classification; assumes the core loop in thatch-plan-refinement. The maintainer's design authority and house style govern, and the diff stays minimal.
---

You are refining a plan for an **oss-contribution**: a change to a
repository the user does not maintain. The governing value is the
maintainer's design authority. It is their codebase; the contribution
that gets merged is the one that fits their intent, not the one that
would be best by your lights. Load `thatch-plan-refinement` for the core
loop and apply the deltas below; where they disagree, these win.

## What this type owes

- **Conform to house style, even when it is worse.** A foreign codebase's
  conventions are not up for improvement in this change. Do not import
  patterns from other projects; do not refactor what the maintainer
  wrote.
- **Minimal diff.** No drive-by refactors, no reformatting of untouched
  lines, no new dependencies, no new abstractions beyond what the change
  strictly needs.
- **The discussion comes first.** Significant design work waits until the
  approach has a maintainer's nod: check CONTRIBUTING.md, search open
  and closed issues and PRs for the same idea, and file or comment on
  the proposal before investing in the implementation. A plan that
  assumes acceptance is building on an unverified premise.

## How this changes the loop

- **Add a premise class: upstream status.** Every plan premise about the
  maintainer's intent (is this wanted, is the approach acceptable, is
  the issue still open) needs evidence: an issue thread, a maintainer
  comment, a CONTRIBUTING instruction. No evidence means "unknown -
  ask upstream," and the plan gates on that question, not on a guess.
- **Consensus adds one test.** Alongside the core skill's consensus
  criteria, the reviewer answers: "would a maintainer accept this
  scope?" Scope findings are blockers. A contribution that solves the
  issue plus three adjacent problems will sit unmerged.
- **Round cap unchanged.** But a plan blocked on upstream discussion
  pauses for the user to have that conversation; it does not loop.

## Lens weights

- **Pattern and reuse inverts.** In team code, existing patterns are a
  strong default; here they are the requirement. A "better" pattern than
  the house style is a finding against the plan, not for it.
- **Hidden problems shrinks.** Consumers of internal state are the
  maintainer's concern. Focus on the change's own footprint and its
  interaction with in-flight upstream work (search open PRs for overlap).
- **Alternatives mostly skips.** The maintainer chose the architecture.
  The plan's job is fitting into it, and where the plan needs a
  maintainer decision, that is an upstream question, not an alternatives
  survey.

## Extra plan sections

- **Upstream discussion.** The issue or thread this change responds to,
  and the maintainer signals (or absence of them) the plan relies on.
- **House-style conformance.** The specific conventions the change will
  follow, read from the project's own CONTRIBUTING and recent merged
  PRs, not assumed.

## Docs bar

Match the project's own documentation conventions for any user-facing
text (changelog entries, docs pages) and the house code-comment style.
The writing skills still govern clarity, but the structure and tone
follow the project's.
