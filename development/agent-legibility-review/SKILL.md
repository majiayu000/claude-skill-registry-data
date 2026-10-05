---
name: agent-legibility-review
description: Framework-agnostic repository review from the perspective of a future AI coding agent. Use when Codex needs to evaluate whether a repo is easy for agents to find, understand, modify, and safely evolve with minimal ambiguity; find discoverability problems, missing or duplicated authoritative locations, hidden conventions, cross-file invariants, ambiguous ownership, scattered change surfaces, unpredictable impact, and agent risk hotspots. This skill evaluates the agent interaction surface; use architecture-review to decide or redesign architectural ownership and boundaries. Do not use as an ordinary code-style, framework-specific, bug, performance, security, clean-code, maintainability, or generic architecture review unless the user explicitly asks for agent-legibility.
---

# Agent Legibility Review

Evaluate one question: can a future AI coding agent find, understand, modify, and safely evolve this repository with minimal ambiguity and minimal risk?

Do not modify code during the review unless the user explicitly asks for implementation. If the user asks for both review and fixes, complete the review first, then make only the requested or clearly justified changes.

## Core Principle

A repository is agent-legible when:

- relevant code can be found quickly
- business rules are explicit
- responsibilities are obvious
- changes are localized
- impact scope is predictable
- ambiguity is minimized
- Every finding is a hypothesis. Before reporting it, actively attempt to disprove it. A finding should only survive if the available repository evidence does not invalidate it.

This is not a code-style review, framework review, idiom review, performance review, security review, clean-code review, maintainability review, or generic architecture review. Discuss structure only when it directly affects finding code, discovering rules, identifying ownership, predicting impact, or making safe modifications.

## Relationship With Architecture Review

Keep the two review scopes distinct:

- Use `architecture-review` to decide where responsibility and authority should
  live, evaluate lifecycle and module boundaries, or design a structural
  refactor.
- Use `agent-legibility-review` to evaluate whether future agents can find the
  right edit point, recognize the authoritative source, discover hidden rules,
  select relevant context, and predict impact in the current repository.

An agent-legibility finding may reveal an architecture problem, but this skill
should report the future-agent failure mode rather than silently redesign the
architecture. When a recommendation requires new ownership or boundary
decisions, hand that decision to `architecture-review`. When both skills are
used, avoid duplicate findings: architecture owns the boundary decision;
legibility owns the navigation and modification consequence.

## Agent Legibility Criteria

Evaluate the repository as an interaction surface for a future coding agent:

1. **Discoverability:** Can an agent identify the likely edit point for a
   realistic task without an unnecessarily broad search?
2. **Authority visibility:** Can an agent distinguish the authoritative owner
   from callers, adapters, generated surfaces, compatibility layers, and
   duplicated representations?
3. **Context locality:** Can an agent load the rules, contracts, collaborators,
   and tests needed for one change without absorbing unrelated behavior?
4. **Impact predictability:** Can an agent discover direct consumers, side
   effects, generated outputs, and validation surfaces before editing?
5. **Intent signaling:** Do names, structure, tests, and nearby guidance expose
   concepts, lifecycle stages, policies, and safe modification boundaries?
6. **Hidden knowledge:** Are invariants and conventions visible where an agent
   will look, rather than existing only in call order, tribal knowledge,
   distant comments, or unrelated files?

These criteria describe whether an agent can perceive and use the current
repository safely. They do not decide where responsibility should live. Route
findings that require new authority, ownership, or boundary decisions to
`architecture-review`.

## Review Process

Follow this order. Use each step to collect evidence; assign each issue to exactly one output section later.

1. Map the repository.
   - Belongs: top-level structure, entrypoints, major modules, tests, generated/vendored areas, build/config files, and local guidance such as README, AGENTS, CONTRIBUTING, specs, ADRs, runbooks, domain docs, schema docs, and generated-code notices.
   - Does not: taste, idiom, or preferred architecture judgments. Output use: cite evidence and uncertainty; do not create findings from structure alone unless it affects navigation or modification safety.

2. Build an agent navigation map.
   - Belongs: where an agent would start for common changes, duplicated entrypoints, competing abstractions, misleading names, naming-based contracts, file/directory conventions, excessive indirection, and deep call chains that obscure the right edit point.
   - Does not: ordinary naming or organization comments when the correct edit point is obvious. Owner: Discoverability; if the issue is source of truth or ownership, use Duplicate Concepts or Ambiguous Ownership.

3. Identify concepts and authority.
   - Belongs: recurring domain nouns, identifiers, statuses, lifecycle states, permissions, validation rules, schema shapes, provider mappings, defaults, generated values, and their redefinitions/translations/validations/generation/persistence/interpretation sites.
   - Does not: unclear module naming unless it creates a source-of-truth problem. Owner: Duplicate Concepts for duplicated or missing authority; Ambiguous Ownership only when one implementation exists but ownership is unclear.

4. Find hidden rules, hidden conventions, and cross-file invariants.
   - Belongs: magic strings/numbers, conditional status groups, undocumented transitions, implicit call order, filename contracts, prefix/suffix semantics, identifier formats, string-pattern routing, registration-by-name behavior, status synchronization, schema compatibility, caller/callee contracts, producer/consumer invariants, and generated-code/runtime alignment.
   - Does not: broad "coupling" claims without a concrete rule an agent could miss. Owner: Hidden Rules; mention locality impact in the recommendation instead of duplicating the finding.

5. Review responsibility clarity.
   - Belongs: modules, classes, functions, configs, or tests whose names/boundaries make it unclear where an agent should make or validate a change.
   - Does not: vague names, utility modules, or abstraction choices that do not affect agent behavior. Owner: Ambiguous Ownership; use Discoverability for navigation-only issues and Duplicate Concepts for source-of-truth issues.

6. Evaluate change locality and impact predictability.
   - Belongs: typical changes requiring edits across scattered files, hidden consumers, side effects, event flows, or integrations whose downstream impact is not discoverable from the changed area.
   - Does not: cross-file invariants already reported as Hidden Rules or duplicated concepts already reported as Duplicate Concepts. Owner: Recommended Improvements, or High-Risk Findings only for P0/P1 risks with no clearer owner.

7. Identify agent risk hotspots.
   - Belongs: code shapes likely to make agents misread local evidence, such as complex condition trees, defensive branches that imply undocumented rules, dynamic dispatch, generated code, reflection, metaprogramming, and weak test anchors.
   - Does not: duplicate concepts, missing authority, hidden rules, or ambiguous ownership. Owner: Agent Risk Hotspots only for risky interpretation surfaces without an earlier owner.

## Scoring The Criteria

Score each Agent Legibility Criterion from 1 to 5 using observable evidence:

- 5: inspected evidence shows one obvious edit path for major capabilities, explicit rules or documented conventions, clear owners, localized change paths, and discoverable consumers.
- 4: most major capabilities have clear edit paths and owners; remaining ambiguity is localized, documented, or covered by tests.
- 3: agents can complete changes, but must infer some rules from usage, naming, call order, or multiple files; authority is uneven.
- 2: several important changes require broad search or cross-file inference because ownership, rules, conventions, or consumers are not discoverable from one area.
- 1: inspected evidence shows agents are likely to edit the wrong place, miss an undocumented invariant, or change one location while leaving required coupled locations inconsistent.

## Finding Rules

Every finding must include:

- location: concrete file, module, function, class, config, doc, test, or "repo-wide" when structure-level
- issue: what is agent-illegible
- why it matters: how this materially affects discoverability, authority, explicitness, ownership clarity, change locality, or impact prediction
- agent failure mode: the likely mistake a future agent would make
- recommendation: the smallest practical improvement
- priority: P0, P1, P2, or P3

Use this priority scale:

- P0: Agent-legibility issue can plausibly cause severe correctness, data integrity, deployability, or operational failure.
- P1: High-risk ambiguity, missing or duplicated authority, hidden rule, or unpredictable impact likely to cause regressions.
- P2: Meaningful navigation, ownership, explicitness, or locality issue likely to slow or mislead agents during common changes.
- P3: Low-risk clarification worth reporting only when it removes a real future-agent trap.

Report only issues that materially affect future agent behavior, navigation, or modification safety. Do not report harmless duplication, cosmetic naming, preferred organization, generic clean-code advice, or documentation gaps without a concrete agent failure mode.

## Finding Disproof Pass

Generate candidate findings first, then challenge each one before reporting it.

For each candidate:

- Search for counter-evidence in docs, tests, names, nearby comments, repository instructions, generated-code notices, and common edit paths.
- Ask whether a future agent can actually find the correct edit point through existing docs, tests, names, or call paths.
- Check whether the alleged hidden rule is already explicit in a nearby authoritative location.
- Check whether the predicted agent failure mode is concrete, or merely speculative.
- Check whether tests already cover the behavior strongly enough to make the change safe to modify.
- Downgrade or reject findings when counter-evidence is strong; preserve uncertainty instead of overstating future-agent risk.
- Avoid letting the same reasoning path both create and validate the finding without challenge.

When useful, list rejected candidates under "Non-Issues / Intentionally Not Flagged" so future reviews do not repeat the same false positive.

## Output Format

Use this structure unless the user asks for a different format. Maximize unique information per section.

Assign each finding to one primary home:

- High-Risk Findings: P0/P1 issues whose primary risk cuts across categories or does not fit sections 4-7. If a P0/P1 finding has a clearer home in sections 4-7, keep it there and mention it briefly in Executive Summary instead of duplicating it.
- Duplicate Concepts: duplicated authority or missing authority.
- Hidden Rules: implicit rules, hidden conventions, and cross-file/module invariants.
- Ambiguous Ownership: unclear module/concept ownership when authority is not duplicated or missing.
- Agent Risk Hotspots: risky interpretation surfaces not already owned by Duplicate Concepts, Hidden Rules, or Ambiguous Ownership.
- Recommended Improvements: ordered actions; summarize, do not restate full findings.

Pure discoverability issues without authority or ownership problems should be reported under Ambiguous Ownership if they obscure the edit owner, or under Recommended Improvements if they are low-risk navigation improvements.

### 1. Executive Summary

- overall agent-legibility health
- highest-leverage risk, not every category
- smallest improvement with the highest leverage

### 2. Agent Legibility Score

Use a table:

| Dimension | Score | Evidence |
|---|---:|---|
| Discoverability | 1-5 | observed navigation evidence |
| Authority Visibility | 1-5 | observed source-of-truth evidence |
| Context Locality | 1-5 | observed context-selection evidence |
| Impact Predictability | 1-5 | observed consumer/effect evidence |
| Intent Signaling | 1-5 | observed naming, structure, test, and guidance evidence |
| Hidden Knowledge | 1-5 | observed invariant and convention evidence |

### 3. High-Risk Findings

Use only for P0/P1 findings that do not have a clearer home in sections 4-7.

| Priority | Location | Issue | Why it matters | Agent failure mode | Recommendation |
|---|---|---|---|---|---|
| P0/P1 | file/module/function/doc or repo-wide | concrete issue | legibility impact | likely future agent mistake | smallest useful fix |

### 4. Duplicate Concepts

Owns duplicated or missing authority: duplicated business rules, validation logic, state transitions, status mappings, identifier generation, permission checks, schema assumptions, provider mappings, or concepts assembled from multiple callers without one source of truth.

Do not include mere repeated code, unclear names, or cross-file invariants unless they create duplicated or missing authority.

### 5. Hidden Rules

Owns rules that require inference: magic strings, magic numbers, undocumented transitions, implicit workflow order, conventions encoded in names or file paths, identifier formats, string-pattern routing, caller/callee contracts, producer/consumer invariants, and schema/status synchronization across files.

Do not duplicate these under Agent Risk Hotspots; use hotspots only when the risk is a confusing implementation surface rather than an implicit rule.

### 6. Ambiguous Ownership

Owns unclear responsibility: concepts, modules, classes, functions, configs, docs, or tests where an agent cannot tell who should own the change or validation.

Do not include duplicated authority, missing authority, or pure navigation friction; those belong to Duplicate Concepts or Discoverability/High-Risk Findings.

### 7. Agent Risk Hotspots

Owns risky interpretation surfaces: complex condition trees, dynamic dispatch, generated code, reflection, metaprogramming, defensive branches that imply undocumented rules, or weak test anchors that make local edits unsafe.

Do not include a hotspot if the same issue is already a duplicate concept, hidden rule, or ownership gap. Reference the primary finding instead.

### 8. Recommended Improvements

Order actions by leverage and safety. Prefer small changes that create authoritative locations, name hidden rules, reduce duplicate concepts, or improve navigation.

Do not repeat full findings. For each action, reference the owning section, expected blast radius, and validation needed when non-trivial.

### 9. Non-Issues / Intentionally Not Flagged

Use only when it adds signal. Briefly list candidate findings rejected by the disproof pass and the evidence that made them safe or intentional.

## Quality Bar

- Ground claims in inspected code, docs, tests, configs, generated artifacts, or runtime wiring.
- Each issue must have one primary output section.
- Findings must survive the Finding Disproof Pass and include a concrete agent failure mode.
- Separate agent-legibility risk from style, taste, maintainability, framework practice, and generic architecture preference.
- Do not use file length or folder count as a finding without a concrete discoverability, authority, context-selection, locality, or impact-prediction failure mode.
- Do not recommend new abstraction unless it reduces real ambiguity, duplicated authority, missing authority, or scattered change surface.
- Do not flag naming, structure, responsibility, or documentation concerns unless they affect findability, rule discovery, ownership clarity, change locality, or impact prediction.
- Treat tests as legibility anchors only when they expose or fail to expose rules an agent needs for safe modification.
- When reviewing large repositories, sample systematically and state the sampling boundary instead of pretending the review is exhaustive.
