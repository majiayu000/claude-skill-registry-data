---
name: specify
description: Specify one bounded feature, bug fix, refactor, or other change with intended behavior, scope, acceptance criteria, and explicit TDD policy. Use whenever intended behavior, scope, or acceptance needs clarification or revision; use investigate to establish an unknown cause.
---

# Specify

Apply the [core](../../README.md#loading-rules); read linked procedures only when their operation applies.
Read the relevant product context if available and any existing spec, issue, or ticket for this change.
Persona: change analyst, focused on one verifiable outcome. Use the capability map for mapped
capabilities; a bug fix or direct bounded request does not require product definition first.

- Establish the user, problem, scope boundaries, constraints, and observable acceptance
  criteria. Include relevant failure or boundary behavior without enumerating speculative cases.
  Give saved criteria stable IDs such as AC1 and AC2; preserve existing IDs when reordering
  or refining them. Existing criteria without IDs can be referenced exactly without a rewrite.
- For a bug fix, distinguish expected behavior from observed behavior. Record reproduction
  steps and environment when known, impact, and evidence; label reported behavior separately
  from a reproduced failure. Keep suspected causes as hypotheses. If an unknown cause or
  reproduction gap blocks a useful plan, route that question to [investigate](../investigate/SKILL.md)
  without making diagnosis a prerequisite for recording the bug. A confirmed cause needs no
  repeated investigation. Acceptance criteria describe corrected behavior and relevant regressions.
- For a refactor, specify the structural outcome and observable behavior to preserve; do not
  invent a behavior change to fit the template.
- Recommend the smallest useful scope. Ask about consequential ambiguity; resolve routine
  details from the request and existing constraints, labeling assumptions that matter.
- For visual work, capture supplied references and concrete required or excluded visual patterns
  in the agreement. Clarify missing preferences only when they materially affect the outcome;
  a clear visual request does not require a design interview.
- When visual options or diagrams clarify a decision, apply [visuals](../../references/visuals.md).
- Create or update `docs/lusona/specs/<change-id>.md` from
  [the spec template](../../templates/spec.md) using the helper and
  [naming rules](../../references/naming.md); every definition produces a spec regardless of
  size, reusing existing specs or legacy feature documents under
  [retention](../../references/retention.md). An already clear request can proceed directly to
  authorized implementation. Link an external issue or ticket when provided; do not create one
  or copy a full ticket into a second maintained specification by default.
- Propose `none`, `targeted`, or `strict` under the [TDD rules](../../references/tdd.md).
  Record the user's choice or standing preference if supplied; otherwise leave it unset and ask.
- Define observable outcomes, not a proposed implementation. Preserve user-required or established
  technical constraints with their source; do not turn a design proposal into an acceptance
  criterion. Include technical detail only when it clarifies scope or resolves uncertainty.
  Continue into architecture or planning when useful and authorized.
- Keep the spec concise: link existing product context, constraints, architecture, and legacy
  execution records instead of repeating them. Keep agreement, optional execution, evidence, and
  current handoff in one change record; preserve existing execution details and separate plans.
- Before handing off the definition, make one inline check for contradictions, ambiguous
  requirements, and unresolved decisions that block the selected work. Fix routine omissions
  from known evidence; preserve unknowns as explicit questions rather than inventing answers.
  This check does not add a review cycle or another approval gate.
- Reconcile the spec's row under the [queue rules](../../references/queue.md).
  Agree what completion means, including human acceptance or delivery when required. Report remaining
  decisions together; do not force a separate approval round for each field.

## Next action

Return the spec path and any unresolved decisions together. Ask a blocking behavior, scope,
or TDD question; otherwise name the next action from unmet criteria or uncertainty: an
experiment, a consequential design decision, or an authorized increment.
