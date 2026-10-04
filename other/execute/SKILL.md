---
name: execute
description: "Execute an existing implementation plan or settled multi-step request through connected slices with targeted checks and controlled plan drift."
---

# Execute

Turn a settled plan into working code. Preserve momentum while maintaining evidence and scope control.

## Load and sanity-check

Read:

- Applicable repository instructions
- The plan or settled request
- The accepted specification when the plan derives from one
- Files and tests directly named by it
- Any referenced schema or contract

Perform one sanity check before editing:

- Does the plan conflict with the current repository?
- Is a dependency missing?
- Would it cause data loss, a security regression, or a public compatibility break?
- Has the requested behavior already been implemented differently?
- If the plan claims full-spec scope, does it still cover all accepted requirements? For a bounded tranche, are its applicable requirements and dependencies settled?
- Does the plan preserve the accepted programme order and trust model under the applicable current authority?
- What present consumer, current requirement, or explicit authorization justifies any generalized protocol or infrastructure it introduces?

Correct small stale details yourself. Surface a concern only when it changes the approach materially.

When an approved specification governs the work, it remains the scope and acceptance authority throughout execution. A tranche controls what is being worked on now; it does not remove later scope from the complete plan. Repair a partial plan that claims full-spec coverage before relying on that claim. An explicitly requested tranche can proceed from its applicable requirements and settled dependencies without first creating a whole-program plan. Record scope or order changes as explicit deltas, and report tranche completion separately from full-spec completion.

## Complete outcome is the default

When the user asks to build, implement, adapt, or borrow a clear feature, deliver the complete requested usable outcome and the integration required for it to work in the repository. `MVP`, prototype, scaffold, placeholder, or local-only happy path is valid only when the user or accepted specification chooses that scope.

Choose the simplest implementation that satisfies the whole contract. Do not turn caution into silent product narrowing, defer an obvious core path as “later,” stop after backend scaffolding when the requested outcome is end-to-end, or report a plan as implementation. If authority, missing inputs, or an external blocker prevents completion, finish every safe in-scope part, label the result partial, and name exactly what remains.

For reference-led work:

- Carry forward the material dispositions established during design, including remaining accepted scope and unresolved items. A selected first slice does not replace the whole request; if source material still needs synthesis to establish scope, use `design` before narrowing execution.
- Treat product descriptions and tutorials as inspiration unless the user makes named behavior normative.
- Treat screenshots and mockups as contracts for visible details only when the user or accepted specification makes them normative. Otherwise use them as reference material. They do not prove hidden data or interaction behavior.
- Let explicit written instructions, corrections, and accepted specifications override inferred reference details.
- Inspect the actual repository and adapt the reference to its architecture; do not clone unrelated features merely because they appear in the source.

## Close the reuse decision before introducing common machinery

For a new generic helper, dependency, adapter, integration, parser, validator, queue, or fallback, inspect the existing implementation and its current caller first. Then check installed dependencies and supported runtime or platform surfaces. Consult current official documentation or maintained external implementations only for gaps that can change the decision.

Close on reuse, extension, composition, or justified custom code. Compare behavior coverage, compatibility, maintenance and dependency cost, security and privacy boundaries, and the present consumer. Popularity alone does not settle fit. Adapting a mechanism need not import its whole framework.

Stop when evidence settles the decision. Do not browse registries for a domain-specific invariant with no useful package boundary. Distinguish searched, unavailable, and unnecessary channels; do not claim ecosystem absence from incomplete access. External queries must omit private code, credentials, and identifying context not needed for the search.

Use a short inline rationale or the existing design record for a consequential choice. Do not add a mandatory research artifact. Research does not authorize dependency installation, external side effects, or changes to accepted behavior.

## Spend complexity on current work

- Prefer one normal implementation path and one source of truth.
- Give every new file, abstraction, state, fallback, retry, compatibility path, dependency, and check a present job. If removing it would not change the requested outcome or protect an applicable boundary, do not add it.
- A second path needs a real caller or supported contract plus explicit precedence and failure behavior.
- Choose each additional search or check because its result can change the implementation or confidence. Stop when the settled request and risk-matched proof are complete.

## Execute connected slices

Use the accepted dependency order. For a cross-component outcome, make the earliest useful run traverse the real entry point and material boundary before expanding similar features around it. When the path is settled, implement it directly; use a bounded probe only for an assumption that could change the approach. Do not create a prototype phase or new infrastructure just to demonstrate this method.

For each coherent slice:

1. Identify the behavior being completed and inspect its current callers, state owner, selected delivery path, and relevant tests. Follow only relationships that can affect this change.
2. Make the simplest complete change, including required wiring, persistence, generated projections, or current consumers. When the accepted outcome depends on a selected caller, a helper with no selected caller is an integration checkpoint, not completion.
3. Add or update a check that distinguishes the relevant failure. Preserve strict red-green where bugs, state transitions, contracts, parsers, migrations, concurrency, or security make it useful; for cross-component work, exercise the entry path at the earliest useful point. A focused compiler or unit check remains enough when risk is genuinely local. Inspect the result and diff before multiplying the pattern.
4. Use the observation to choose the next action: continue a sound implementation; investigate a violated assumption; or revise only the dependent choices invalidated by new evidence. Keep independent safe work moving.

A slice may span several files. Do not create one task per file or one subagent per checklist item. A working first path leaves the remaining accepted behavior due; continue through those requirements and final risk-matched verification. A surrogate, fixture, or source-only result closes only its named boundary, not an unavailable runtime or user surface.

## Plan drift

Use judgment when reality differs from the plan.

Proceed and note the adjustment when:

- A file moved,
- An existing abstraction already solves part of the problem,
- A test requires a nearby fixture update,
- A smaller implementation satisfies the same contract.

“Smaller” means less implementation complexity with equivalent specification coverage. It does not mean dropping accepted behavior, cardinality, migration, compatibility, or acceptance requirements.

Pause or explicitly flag the choice when:

- User-visible behavior changes,
- A public API or schema must differ,
- Data migration becomes necessary,
- Security or privacy assumptions change,
- The plan's central architecture is invalid.
- A derived artifact changes programme order or widens the trust model without applicable approval.
- Infrastructure displaces a narrower accepted path without applicable authorization, especially when it has no present consumer or current requirement.

When a safe reversible choice exists, take it and continue.

Do not treat already-written code as authority to cross these boundaries. Preserve it as `research-only` evidence when useful, return to the applicable authorized baseline, and continue only within the accepted goal.

## Testing

Use strict red-green where a failing test clarifies the contract, especially for bugs, domain logic, state transitions, parsers, migrations, concurrency, or security-sensitive behavior. Use characterization-first for unclear legacy behavior and test-alongside for styling, copy, simple configuration, or low-risk wiring. Existing valid code does not need to be deleted because the test came later.

At minimum:

- Reproduce bugs with a regression test when practical.
- Test domain logic, state transitions, parsers, and contracts.
- Use visual/manual checks for styling and interaction where unit tests add little value.
- Keep mocks at stable boundaries.

## Delegation

Choose responsibility before deep execution. Stay in the main agent for trivial or nearly completed work, work whose handoff and acceptance would largely repeat direct execution, or frequent unresolved cross-owner decisions. Delegate when a bounded lane creates material value through clean context, serial sequencing, parallel independence, or protected coordinator attention, and the task has already left the clear/direct path. The coupled parts or likely-common-cause symptoms of one responsibility stay together in whichever single lane owns them; coupling, reversibility, and a likely common cause do not force that lane to be the main agent.

Keep the main agent as coordinator and integration owner. Reuse an active worker or session that owns the lane instead of creating another, and do not implement the same work in the main agent while a worker owns it. If the user asks you to work solo, or subagent tools are unavailable, keep the same ownership boundaries and sequence the work locally instead of claiming a lane that did not run.

Give every worker an explicit outcome, scope, context, authority, and return contract; do not spawn a fresh implementer for every checklist item, duplicate reviewers, or competing writers. Workers do not delegate again.

Before the first dispatch, treat delegation as a genuine phase change and apply the `delegate` reference. Subagent-tool availability, a higher model/reasoning tier, or an idle slot is only host capability, not evidence that delegation is appropriate.

## Continue across methods

A domain method can contribute to this execution without starting a new commission. Carry forward settled choices, the existing plan, the current responsibility owner, useful evidence, and remaining scope. Reuse an already-owned worker lane and applicable checks; retain domain-specific acceptance. As a blocking question is settled, stop that investigation and continue the next useful action. Do not carry its ceremony into unrelated small work or discard a still-relevant check merely because the latest edit is small.

## Checkpoints

Give the user an update when:

- A meaningful slice is complete,
- A material issue changes the plan,
- A root cause or hidden constraint is discovered.

Do not ask “continue?” after routine milestones. Continue until completion, a real blocker, or the requested stopping point.

## Failure handling

If focused verification fails:

1. Read the full failure.
2. Decide whether it is caused by the current slice, an existing baseline issue, or the environment.
3. Fix current-slice regressions before proceeding.
4. When the cause is uncertain, stop speculative implementation and move to evidence-driven debugging: test one discriminating causal claim at a time, as in `debug`, without duplicating its full procedure here.
5. Do not stack speculative fixes.

Retain independently observed defects; one failed repair does not erase a defect that separate evidence still supports. Reset the diagnosis when repeated attempts based on the same idea stop adding discriminating evidence, rather than after a fixed number of tries.

## Completion

After all slices:

- Review the combined diff for scope and accidental changes.
- Run fresh verification at a scope justified by risk: focused checks for local changes, adjacent checks for shared code, and broad checks for migrations, security, public contracts, or integration readiness.
- Update documentation only when behavior, interfaces, setup, or durable decisions changed.
- Reconcile the final state against the requested scope. For full-spec work, use the complete coverage ledger. For a bounded tranche, report its outcomes and preserve the status of other accepted scope without creating a whole-program ledger; do not close the specification because one tranche finished.
- Do not commit, push, merge, or open a PR unless the user requests it or applicable repository/global instructions delegate it.

Report actual results, including checks not run.
