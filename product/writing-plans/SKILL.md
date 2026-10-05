---
name: writing-plans
description: "Convert a technical specification, tracker reference, or feature request into a rigorous, atomic, dependency-ordered implementation plan the coder agent executes step-by-step. Use whenever the output is a Markdown plan file under `.plans/`, or when asked to plan, break down work, sequence implementation phases, turn a spec into actionable tasks, write a roadmap, decompose a feature into phases, or convert a `Spec-*.md` into a `Plan-*.md` artifact. Defines phase structure, output-style rules (WHAT not HOW, signatures only, no language-tagged code fences, symbol references over file paths), step anatomy (atomic, file-explicit, verify-gated), per-phase constraint checks, the philosophy-checklist self-gate, and a validation script. Do NOT use for writing the specification itself, writing implementation code, writing tests, code review, or evaluating an existing plan."
metadata:
  author: Serghei Iakovlev
  version: "1.1"
  category: planning
---

# Writing Implementation Plans

Transform a Technical Specification (or equivalent input) into an atomic, dependency-ordered Implementation Plan. The plan is the contract between architect and implementer: it removes ambiguity about WHAT changes, WHERE it changes, in WHAT ORDER, and HOW each step is verified. The coder agent executes the plan verbatim; ambiguous or oversized steps each produce a class of implementation defect.

This skill is stack-agnostic and project-agnostic. Concrete phase catalogs, layering rules, banned patterns, and verification commands come from the project's architecture document and agent-instruction files, not from this skill. Read those documents first; design within them; flag every deviation explicitly.

## Running scripts bundled with this skill

Script paths in this document (e.g. `scripts/`) are resolved relative to **this** SKILL.md file, not to your current working directory. If a relative command fails to resolve, prefix it with the path your platform loaded this SKILL.md from.

**Fallback.** If `python3` cannot be located, analyze the script's purpose and logic and execute its intent with available tools, but warn the user that python is not available and the logic was executed with a fallback approach that may not be perfect.

## Project context: reading order

These documents are the authority every plan must conform to. Read in this order; skip tiers the project does not ship; do not load files that do not exist.

1. **Agent-instruction files**: `AGENTS.md`. Boundary rules (often "Always / Ask First / Never"). Quote the rules that constrain this feature.
2. **Documentation index**: if `docs/` exists, read `docs/README.md` (or the closest equivalent: `docs/index.md`, `docs/SUMMARY.md`, `docs/DIGEST.md`). Use it as a map.
3. **Architecture and product docs** named by the index: `architecture.md`, `ARCHITECTURE.md`, `design.md`, `PRD.md`, `product.md`, or whatever name the project uses.
4. **Decision records**: `docs/decisions/`, `docs/adr/`, `adr/`, `ADR/`. Read the index first; read individual records only when they constrain this feature. Accepted decisions are architectural law.
5. **Language and style rules**: `.agents/rules/`, `.github/instructions/`, `.copilot/instructions/`, `.claude/rules/`. Plan-prose requirements (RFC 2119 keywords, banned vocabulary, comment style, naming).
6. **Codebase structure**: list the relevant package or module directories. Identify entry points, existing abstractions to reuse, and where new code belongs.

When the project documents none of the above, say so explicitly in the plan's Summary section and propose what context the project should add. Do not invent constraints the project did not document.

## Input types

The planning input is one of:

- **Spec file**: `.specs/Spec-*.md` or whichever path the project uses. The common case.
- **Tracker reference**: a Jira ID/URL, GitHub issue, Linear/Asana/Notion link. Fetch before planning: title, description, acceptance criteria, labels, components, linked design pages. Use whichever MCP server, CLI, or web fetch is available.
- **Feature request**: natural-language description when no spec exists. Flag the missing spec and consider invoking `writing-specs` before planning.

If the input is missing, one-line, or so ambiguous the plan would be a guess, stop and ask. Planning from guesses produces plans that drift from architecture on first contact with the code.

## Workflow

Five phases, executed sequentially. Do not skip a phase, do not reorder phases, do not collapse two phases. Each phase has an exit gate; do not advance until the gate passes.

Copy this checklist into the reasoning trace and mark items as you complete them:

- [ ] Phase 1: Read project context
- [ ] Phase 2: Read the input
- [ ] Phase 3: Order the phases by dependency direction
- [ ] Phase 4: Draft atomic steps using the template
- [ ] Phase 5: Validate against the philosophy checklist and validator script

### Phase 1: Read project context

Apply the reading order in § Project context. Extract concrete, named constraints, not impressions. Quote the rules that constrain this feature so the plan can cite them.

**Exit gate.** You can answer: which agent-instruction rules apply, which architecture sections constrain the work, which ADRs touch this feature, and which language/style rules govern plan prose.

### Phase 2: Read the input

Read the spec or tracker in full. Identify every behavior the input requires, every interface it names, every acceptance criterion, every constraint it carries. If the input contradicts the architecture document, surface the contradiction; do not silently resolve it.

**Exit gate.** You can list: exact files that will change, layers/modules touched, acceptance criteria the plan must satisfy.

### Phase 3: Order the phases by dependency direction

Decompose work into ordered phases. Imports and dependencies flow downward only: data shapes -> services/business logic -> composition -> boundary/UI. The project's documented layering, if any, overrides this default. Each phase has an entry condition, a step pattern, and an exit gate.

See [references/phase-structure.md](references/phase-structure.md) for the dependency-graph principle, the universal phase template, common partial-scope shapes, and the constraint-check pattern.

Only include phases that are actually touched. A two-layer change produces a two-phase plan; a feature that threads through every layer produces a full plan. Do not pad with empty phases.

**Exit gate.** You can list the phases in execution order and explicitly state which canonical phases are omitted and why.

### Phase 4: Draft atomic steps using the template

Use [assets/plan-template.md](assets/plan-template.md) as the structural skeleton. Every section of the template appears in the final plan. Empty sections include a note explaining why ("No persistence changes required.").

Group steps into the selected phases. Each step is a Markdown checkbox: `- [ ] **N.M** {step title}`. See § Step anatomy below and [references/output-style-rules.md](references/output-style-rules.md) for the detailed rules with examples.

### Phase 5: Validate

Run the validator as a feedback loop:

```bash
python3 .agents/skills/writing-plans/scripts/validate_plan.py .plans/Plan-{slug}.md
```

If the script is unavailable, walk through [references/philosophy-checklist.md](references/philosophy-checklist.md) manually. Fix every error and re-run until the validator reports `Validation passed`. Fix warnings where the plan can reasonably be improved; warnings do not block delivery but they signal under-specified or untraced work.

## Output style rules

These rules are the core of the plan protocol. A plan that violates any of them is not a valid plan. They exist because the coder agent executes the plan verbatim: ambiguity or leaked implementation costs real engineering time.

1. **Location.** Write to `.plans/Plan-{slug}.md`. Derive `{slug}` from: (a) the spec filename, stripping the `Spec-` prefix; (b) the tracker ID if present; (c) otherwise a kebab-case slug of the feature title. Reuse the same slug across spec, plan, and review for traceability.
2. **Summary first.** Open the plan with a one-sentence Summary section immediately after the title and before Phase coverage. Format: "Builds X by Y; touches Z layer(s)." The Summary primes the coder agent's reading of the steps; it is not a TL;DR for human skimming, so it stays short.
3. **WHAT, not HOW.** Define file paths, function and method signatures, type or schema shapes, package or module boundaries, ordered steps, verify gates. Do NOT write function bodies, full implementations, exact SQL strings, exact algorithms, test bodies, or full component code. Do NOT use fenced code blocks tagged with a language identifier (`go`, `ts`, `tsx`, `python`, `sql`, `rust`, `java`, etc.); the tag signals runnable code and lets implementation creep into the plan. Inline signatures in prose are correct. Untagged pseudo-code is acceptable for non-trivial logic when prose alone is unclear.
4. **Reference symbols, not just files.** When a step reuses, extends, or interacts with existing code, name the concrete symbol (function, method, type, constant, package, module path) so the implementer can grep for it.
5. **One step, one file, one outcome.** Every step modifies or creates one file (or one tightly-coupled set), describes the intended change in signature or prose form, and ends with a verify gate. A step that touches more than approximately 3 files or ~300 lines of code MUST be decomposed.
6. **Verify gates are specific.** Every productive step terminates with a `Verify:` line carrying a specific, runnable command with the actual target (package path, test name, file path, named check). Bad: `Verify: tests pass`. Good: `Verify: run the project's test command targeting the modified package; confirm the new test for X passes`. Discover the actual commands from the project (Makefile, Taskfile.yml, package.json scripts, `scripts/`, CI configuration); do not hardcode `make test` or `go test ./...` unless the project documents them.
7. **Dependencies flow downward; annotate the non-trivial ones.** Phase ordering matches dependency direction; a step in phase N must not depend on artifacts produced in phase N+M (M > 0). Within a phase, when a step depends on a specific earlier step beyond the previous one, append a parenthesized annotation to the step title: `(depends on step N)`. When two steps in the same phase share no file and no data dependency, annotate both: `(parallel with step N)`.
8. **Atomicity.** Each step has a single outcome the reviewer can confirm. "Implement and test" is two steps (coder + tester). "Add validation and refactor the parser" is two steps.
9. **Cite project sources.** Every design decision that traces to the spec, an ADR, an architecture-document section, or an agent-instruction rule MUST cite the source: anchor link, filename, ADR number, or rule name. Decisions that do not trace MUST be flagged in the plan as plan extensions requiring review.
10. **Tests are separate steps assigned to the tester agent.** Do not bundle "and add tests" into an implementation step. The plan names test additions (test names, intent, coverage area) without writing the test bodies.
11. **No banned patterns.** Where the project's agent-instruction files or ADRs list banned libraries, banned patterns, or deprecated APIs, do not propose them. If a banned pattern appears to be the only feasible solution, halt and ask for clarification.
12. **No em-dashes.** Use commas, parentheses, periods, semicolons, or colons.
13. **One term per concept.** Pick one name; use it everywhere; do not alternate synonyms.
14. **The reader is a machine.** The coder and tester agents open this file, execute the steps they own, and close it. No orienting prose, no recap of a previous phase, no closing summary. A step is File, Change, Symbols, Signature, Logic, Verify; prose that fits none of those fields is either a Decision or it does not belong in the plan.
15. **Point at the spec, do not restate it.** The header names the source spec. Do not re-derive its business rationale, re-list its risks, or re-explain its data shapes. What the plan adds is what the spec does not carry: order, atomicity, file targets, and verify gates. A step that restates a spec section instead of acting on it is the most common way a plan doubles in size without gaining executable content.
16. **"none" is a complete answer.** Under Decisions, Plan extensions, and Further considerations, write the word and stop. Do not explain what you considered or why nothing qualified. Unlike a specification, this document keeps these sections when empty: an explicit "none" records that the planner looked, which a deleted heading cannot distinguish from a planner that forgot.

See [references/output-style-rules.md](references/output-style-rules.md) for each rule expanded with Good/Bad examples.

## Step anatomy

Each step MUST be atomic and independently verifiable, sized for a single coder-agent session. A well-formed step names:

- **What** to create, modify, or delete (file path + verb)
- **Symbols** it touches (function, type, method, constant, module path)
- **Signature or shape** of the change, inline in prose or as an untagged block
- **Logic** as a numbered prose list when branching matters; omit otherwise
- **Constraint check** for the layer boundary the step honors
- **Verify** as a specific runnable command with a named target

Example of a well-formed step (universal):

```
- [ ] 2.1 Add the listing operation to the contact service.
  - File: src/services/contact-service.{ext}
  - Change: MOD (extend existing module)
  - Symbols: existing `ContactService`; new `listContacts` exported function
  - Signature: `listContacts(userId, cursor?, limit?) -> Promise<ContactPage>`
  - Logic:
    1. Validate `userId` against the existing scope guard.
    2. Query the contact store filtered by `userId` and `relationshipTag`.
    3. Paginate with cursor-based navigation per architecture Section 5.3.
  - Constraint check: no UI imports, no transport-layer imports.
  - Verify: run the project's typecheck command targeting `src/services/`; confirm no new errors.
```

**Step granularity.** Optimal step count follows a U-shape: under-specified plans (under ~3 steps per phase) cause hallucinated sub-tasks; over-specified plans (monolithic steps that span multiple files) fail atomicity. Aim for 3 to 15 steps per phase; split whenever a step names more than one file.

**Forbidden step shapes:**

- "Refactor everything related to X" - not atomic
- "Clean up the module" - not verifiable
- "Implement the feature end-to-end" - collapses the phase structure

See [references/output-style-rules.md](references/output-style-rules.md) § Anti-patterns to reject on self-review for the full catalogue.

## Plan file structure

Every plan follows this top-level structure (see [assets/plan-template.md](assets/plan-template.md) for the verbatim template):

1. **Header** - title, created-at, tracker ref, source spec, one-sentence feature summary
2. **Summary** - one sentence (per Output Rule 2)
3. **Phase coverage** - one-paragraph statement of phases that apply (in execution order) and canonical phases that are omitted with a one-clause reason each. Phase ordering is already visible in the H2 headings of the phase sections themselves; this section adds the omissions context
4. **Phase sections** - one `## Phase N: <Name>` per applicable phase with checkbox steps inside and a constraint-check bullet at the end
5. **Files Affected** - table listing every new or modified file with change type and purpose
6. **Decisions** - design choices the planner committed to (with assumptions and scope boundary)
7. **Plan extensions** - decisions that do not trace to a project source (with reasoning and review needed)
8. **Further considerations** - open questions with named alternatives and the planner's recommendation

The philosophy checklist is the planner's internal pre-delivery self-check (Phase 5 of the workflow). It runs in the planner's reasoning trace; it does NOT belong in the artifact. The artifact is read by the coder and tester agents, neither of which extracts value from the checklist content; the structural conditions the checklist verifies are independently enforced by `scripts/validate_plan.py`.

This rule went unenforced long enough to leak: in a measured corpus of 153 plans, 30 shipped a `## Philosophy Checklist` section. `scripts/validate_plan.py` now treats that heading as a structural error, so the rule can fail rather than merely being stated.

After writing, report the absolute plan-file path to the caller.

## References

| File | When to read |
|------|--------------|
| [references/phase-structure.md](references/phase-structure.md) | Phase 3 of the workflow. Dependency-graph principle, universal phase template, partial-scope shapes, constraint-check pattern |
| [references/output-style-rules.md](references/output-style-rules.md) | Phase 4. Each output rule expanded with Good/Bad examples plus the anti-patterns catalogue |
| [references/philosophy-checklist.md](references/philosophy-checklist.md) | Phase 5. Self-check organized by concern (Traceability, Layering, Atomicity, Sequencing, Security, Style, Simplicity, Delivery) |
| [assets/plan-template.md](assets/plan-template.md) | Phase 4. Structural skeleton for the plan file |
| [scripts/validate_plan.py](scripts/validate_plan.py) | Phase 5. Automated validator for the structural and style rules |
