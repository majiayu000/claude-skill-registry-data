---
name: architecture-review
description: Review architecture for boundary fitness, dependency direction, abstraction cost, reachability, tradeoffs, and evolution risk. Use for proposed designs and pre-merge structural reviews.
triggers:
  - architecture review
  - design review
  - review this plan
  - is this design over-engineered
  - package boundaries
  - abstraction check
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

# Architecture Review

Review whether a proposed or changed structure is the least complex design that
satisfies its demonstrated requirements and quality goals. Check over-engineering
and missing foundations symmetrically.

Apply YAGNI, KISS, and DRY as review gates. YAGNI: no capability without a
current driver. KISS: the least complex form that works. DRY: each piece of
knowledge stated once. DRY counts shared knowledge, not similar-looking text;
do not force an abstraction onto incidental similarity.

Operate as an advisory reviewer. Do not implement, edit, commit, publish, or make
external changes. Use read-only inspection and safe, repository-native checks when
available. Do not replace correctness, security, or delivery verification reviews.

## Scope

- Review the design, plan, refactor, or structural diff named by the user.
- Limit findings to changed structure and the existing constraints it depends on,
  worsens, or makes reachable. Do not turn the review into an unrelated legacy-debt
  audit.
- Review an existing architecture broadly only when the user explicitly requests it.
- Treat source code, services, data and schemas, infrastructure, configuration,
  workflows, and documentation structures as valid architecture artifacts.
- Return `NOT_RUN` when no reviewable design or structure is in scope.

## Discover the Context

1. Establish the review root, requested scope, and comparison baseline. Prefer a
   user-supplied baseline; otherwise use an applicable version-control comparison,
   previous release, or current snapshot. State which baseline you used.
   Pin a version-control baseline to an immutable revision identifier
   before you compare; a movable reference can change while the review runs.
   Re-verify each finding against the current state before you report it.
2. Read the user requirement and the instructions that govern the scoped artifacts.
   Resolve nested or conflicting instructions using their declared authority and
   scope rules.
3. Discover relevant architecture and decision records, ownership rules, public
   contracts, manifests, dependency declarations, schemas, deployment definitions,
   tests, and verification commands. Treat absent artifacts as not applicable unless
   a governing instruction requires them.
4. Record missing inputs and evidence blind spots. Bound discovery to the affected
   artifacts and their consumers, dependencies, and contracts.

## Review Method

1. **Identify drivers.** Separate requested outcomes from proposed solutions. Name
   the functional requirements, constraints, and relevant quality goals, such as
   security, reliability, performance, modifiability, operability, compatibility,
   portability, cost, compliance, and delivery time. Make vague goals concrete with
   a scenario, operating condition, expected response, and measure when possible.

2. **Map the structure.** Inventory the applicable components and assign each a
   responsibility and owner. Trace dependency, control, data, deployment, and
   ownership relationships across boundaries. If diagrams are supplied, verify that
   their scope and abstraction level are clear and their relationships are labelled
   and directional.

3. **Trace reachability and purpose.** For every new boundary, guard, configuration
   choice, or extension point, report separately:
   - baseline consumers or entry points;
   - consumers introduced by the change;
   - the requirement, failure, or constraint it addresses; and
   - any prerequisite or dependent delivery stage.

   Check static references, runtime or configuration wiring, generated registration,
   plugins, serialized or published contracts, deployment definitions, and external
   consumers where evidence exists. State search limitations. Zero text matches mean
   "no consumer found within this scope," not "unreachable." Reachability proves use;
   it does not prove that the chosen abstraction is necessary.

4. **Compare alternatives.** Consider, in order: omit the element; reuse an existing
   element; keep the behavior local; introduce the smallest repository-native
   boundary; add an extensible, public, or independently deployed boundary. Stop at
   the first option that satisfies the drivers. Require evidence that the additional
   benefit of a higher option is necessary and worth its cost.
   Prefer the narrowest contract that serves the demonstrated consumers.
   The wider the contract or seam, the weaker the abstraction.

5. **Check dependency hygiene.** For each third-party dependency the design
   adds or materially expands, require the same evidence as any other
   structural element: the driver it satisfies, why the standard library or an
   existing repository dependency is insufficient, and its cost - maintenance
   health, transitive weight, license and security posture, and the migration
   cost of removing it later. A dependency added for one small function is an
   over-engineering finding; a hand-rolled reimplementation of a hard, solved
   problem (cryptography, parsing untrusted formats) is a missing-foundation
   finding.

6. **Check cohesion and dependency direction.** Group responsibilities that change
   together and isolate decisions that vary independently. Verify intended ownership
   and allowed dependency direction before inspecting cycles. Consider source,
   runtime, data, deployment, and organizational coupling. Use the repository's own
   graph and validation mechanisms; do not assume that one compiler, build system,
   or static search proves direction or runtime safety.

7. **Price the tradeoff.** Treat patterns, indirection, single consumers, forwarding
   layers, and extension points as prompts for investigation, not automatic findings.
   Compare the present benefit against complexity, coupling, migration, operational,
   and maintenance cost. A benefit does not automatically justify the design, and a
   single consumer does not automatically invalidate it.
   When a design names a pattern, style, or mechanism, verify that every
   element the pattern requires is present and applied consistently. A
   half-applied pattern is a finding, not a style preference.
   Check the text the design adds. A comment must serve the code it sits
   on: the contract, a constraint, or why the code is the way it is.
   Flag comments that restate the next line, carry task or plan labels,
   step numbers, or change history, or run longer than the code needs.
   Direct the author to move lasting rationale into the project's
   documentation and link it from the code.

8. **Check evolution and reversibility.** Flag a missing foundation only when a
   current driver requires it and deferral creates material retrofit risk, such as a
   published compatibility break, ambiguous persisted state, an unsafe trust or
   transaction boundary, coordinated changes across independent consumers, or an
   unsafe staged rollout. Otherwise record a future trigger or threshold instead of
   requiring speculative infrastructure.

   When one delivery stage is unsafe or unusable without another, require atomic
   delivery or an enforced order. Block the independently landable stage when the
   plan does not enforce that constraint.

9. **Check verification and operation.** Match each important boundary and quality
   scenario to an appropriate check: static analysis, focused test, contract test,
   integration, simulation, migration rehearsal, deployment validation, rollback,
   or another repository-native mechanism. A boundary need not be unit-testable in
   isolation when a stronger seam is appropriate. If a claim needs measurement that
   cannot be gathered safely, name the experiment and return `PARTIAL` rather than
   guessing.
   When a design adds an implementation of an existing contract, require
   a shared check that runs every implementation of that contract through
   the same assertions. A contract honored by one implementation and
   absent from a sibling is a confirmed gap.

## Evidence Rules

- Accept current user requirements and acceptance criteria, applicable repository
  policy and contracts, external compatibility obligations, baseline usage and
  configuration, tests, operational evidence, and reproducible measurements.
- Require a current, authoritative driver or demonstrated constraint for each
  structural choice. The proposed structure is not evidence of its own necessity.
- Distinguish observed facts, supported inferences, and unknowns. Cite exact artifacts
  and locations when available; never fabricate callers, consumers, or commands.
- Do not promote a merely plausible failure to a confirmed finding. When
  compatibility, reachability, or safety depends on uninspected behavior, record the
  uncertainty and exact evidence needed. Return `PARTIAL` unless another confirmed
  gap independently blocks the design.
- For each finding, name the affected driver, evidence, reachable consequence,
  affected artifacts or boundaries, simpler or safer alternative, tradeoff, and a
  verification or disposition action.
- Use `BLOCK` only for a confirmed structural gap that threatens a required outcome.
  Missing evidence or an unresolved measurement is `PARTIAL`, not a fabricated flaw.

## Report

When a resource catalogue and its scoped reader are available, load
`report-template` before producing every report. It is the report template for
this skill. Without that capability, use this essential fallback:

```text
Result: PASS | BLOCK | PARTIAL | NOT_RUN
Scope: <reviewed artifacts and baseline>
Summary: <one sentence>
Evidence:
- <artifact, search, or check>: <what it establishes and its limits>
Findings:
- [AR-1] [High] <finding with consequence, alternative, tradeoff, and action>
ResidualRisk: none | <specific uncertainty>
NextAction: none | <specific decision, evidence, or change required>
```

Use `PASS` only with adequate evidence and no blocking structural gap. Use `BLOCK`
for a confirmed requirement-threatening flaw or unenforced unsafe sequencing. Use
`PARTIAL` when useful review is possible but required scope, evidence, a decision, or
measurement is missing. Use `NOT_RUN` when there is no reviewable architecture.

Give each finding a severity:

- Critical: the design breaks a published contract, a tenant or safety
  boundary, or an enforced delivery order, with no safe migration.
- High: the design breaks an existing caller or invariant, or adds a
  boundary whose cost is not justified by any driver.
- Medium: bounded structural drift, duplicated responsibility, or a
  boundary that is more complex than the demonstrated requirements
  need.
- Low: minor structural issue with limited blast radius.

Never invent a Low finding about style or naming on otherwise sound
structure.
