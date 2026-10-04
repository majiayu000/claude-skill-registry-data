---
name: design-audit
description: Audit code architecture and maintainability for unnecessary complexity, premature or missing abstractions, duplication, unclear boundaries, and refactoring opportunities. Not for bug, security, or readability-only reviews.
---

# Design audit

Review the scope in the user's request or actual invocation arguments for architectural quality. Use `$ARGUMENTS` only when the active runtime expands it, never as a literal path. Look for structure that imposes concrete maintenance costs; do not assume the code is correct merely because this audit focuses on design.

This is a review skill first. Edit only when the user explicitly asks for refactoring, including in plain language, or supplies `--accept` as an actual invocation option. Examples and quoted text are not activation flags.

When refactoring is authorized, audit first, then implement high-confidence, behavior-preserving **high-impact** findings within scope without redundant confirmation. A specifically requested smaller refactor remains in scope; general acceptance does not authorize speculative medium- or low-impact cleanup. Broad redesigns, risky migrations or product choices require direction when the request does not already settle them. Preserve public interfaces, serialized data, ordering, error/cancellation behavior and side effects unless changes are explicitly authorized.

Use subagents to explore independent areas of the codebase in parallel where appropriate. Read actual code and call sites; don't guess from file names.

## Workflow

1. Identify explicit files, directories, diff/PR or subsystem first; default to the current project only without a supplied scope. Read project instructions and inspect the working tree and index. Record the reviewed revision and re-check affected code before applying recommendations. Preserve unrelated edits and staged work.
2. Map the relevant structure: entry points, module boundaries, data flow, shared helpers, and repeated implementation patterns.
3. Read representative code and enough callers, tests and history to verify candidate issues. Consider language idioms and documented compatibility/ownership constraints. Route incidental bugs or readability-only observations separately without silently starting another audit or mixing them into design findings.
4. Prioritize by demonstrated maintenance impact and confidence. Explain a concrete change that is harder today and how the proposed structure reduces that cost. Compare the smallest refactor with leaving the code alone; include migration risk and coupling introduced by consolidation. The checklist below supplies investigation prompts, not automatic findings.
5. For review-only requests, report paths without source/snapshot edits or external actions. When authorized in plain language or by `--accept`, implement selected in-scope refactors in logical increments. Establish relevant behavior before changes, then check the same observable contracts afterward with focused characterization/regression checks and the project's actual build/test commands. Byte-compilation is relevant for Elisp, not a universal requirement. Inspect test commands for live writes, installs and other side effects before running them.
6. Inspect the final diff for semantic changes and check analogous affected callers/modes. Commit each logical owned change according to project policy, preserving unrelated staging. Compiler/linter success alone does not demonstrate behavior preservation; report material untested boundaries, partial outcomes and unresolved decisions. Do not push or publish as an implicit refactoring step.

## What to look for

### Abstraction problems

- **Premature abstraction**: indirection whose cost exceeds its demonstrated purpose. A single use case may still justify compatibility, ownership, security or testing boundaries.
- **Missing abstraction**: genuinely shared logic that repeatedly changes together. Three occurrences is a clue, not a threshold; similar operations with different reasons to change may belong separately.
- **Wrong level of abstraction**: functions that mix high-level orchestration with low-level details, or modules that bundle unrelated responsibilities
- **Leaky abstraction**: callers that need to know internal details of a function or module to use it correctly (e.g., relying on side effects, required call order, internal state)

### Complexity

- **Unnecessary indirection**: wrapper functions that add nothing, delegation chains that pass through unchanged, adapter layers with no adaptation
- **Overengineering**: layers or configuration with removal-safe redundancy and demonstrated maintenance cost. Do not invent future usage or infer uselessness from one implementation; rollout, emergency-disable and public extension contracts may justify them.
- **God functions/modules**: single units that do too many things and would benefit from decomposition
- **Deep nesting**: tangled responsibilities with structural maintenance cost. Flattening for readability alone belongs in an interpretability audit.

### Structural issues

- **Circular dependencies**: modules that import each other, creating coupling that makes both harder to change
- **Shotgun surgery**: a single logical change requires touching many unrelated files because related logic is scattered
- **Feature envy**: code that primarily operates on another module's data rather than its own — suggests the logic belongs elsewhere
- **Dead code**: confirm no supported use before removal, including public exports, callbacks, reflection, dynamic registration, CLI/config entry points, platform variants and external consumers. A local text search alone cannot prove a public interface unused.
- **Inconsistent patterns**: the same kind of task (e.g., error handling, data transformation, API calls) done differently in different places without justification

### Interface design

- **Unclear contracts**: functions whose behavior depends on implicit assumptions rather than explicit parameters (e.g., relying on global state, environment variables, or call order)
- **Boolean blindness**: flag combinations that obscure distinct responsibilities or multiply invalid interface states. Unreadable call-site spelling alone is a readability concern.
- **Primitive obsession**: repeated invariant/representation maintenance that a named type would materially simplify. Preserve wire-format and public API contracts; a primitive value alone does not warrant a wrapper.
- **Kitchen-sink parameters**: functions with many optional parameters that serve different use cases — suggests the function should be split

### Duplication

- **Copy-paste code**: identical or near-identical logic in multiple places (not just similar-looking code — it must be genuinely the same operation)
- **Parallel hierarchies**: separately maintained copies of the same policy that drift or multiply work. Generated files, runtime/deployment mirrors and deliberately independent validators may require synchronization, not unification; edit their canonical source.
- **Reimplemented stdlib**: a standard operation can replace local logic with matching supported-version semantics, errors and ordering. Verify equivalence before recommending replacement.

## What NOT to flag

- Bugs, security issues, or error handling gaps (use `/code-audit` for that)
- Naming, comments, or readability issues (use `/interpretability-audit` for that)
- Style or formatting issues (that's what linters are for)
- Performance optimizations (unless the structure itself prevents reasonable performance)
- Missing features or tests
- Simple code that works — don't suggest abstractions for straightforward, non-duplicated logic
- Patterns that are idiomatic for the language/framework even if they seem verbose

## Output format

Use the required host/project review schema when present. Otherwise keep the report proportional to inspected scope, omit empty categories, and use:

1. **Overall assessment**: a brief, evidence-backed assessment of the inspected scope, not unreviewed codebase-wide health
2. **High impact**: structural problems that actively make the codebase harder to maintain or extend, with clear refactoring paths
3. **Medium impact**: issues worth addressing when working in the area, but not urgent
4. **Low impact**: evidenced structural costs too small to justify a dedicated refactoring effort, not style or speculative cleanup
5. **Good design**, only when useful: specific existing patterns worth preserving during the proposed changes, not obligatory praise

For each finding, include:

- File path and line number(s)
- What the structural problem is (be specific — "this 200-line function has three distinct phases that should be separate functions", not "this function is too long")
- A concrete refactoring approach, with compatibility constraints and change risk
- What the improvement buys you (e.g., "makes it possible to test the validation logic independently")

If there are no meaningful design issues, say so clearly and mention any residual uncertainty from areas you did not inspect.

For review-only requests, end with high-impact recommendations. For authorized refactoring, whether requested in plain language or with `--accept`, report changes, relevant verification, commit hash and unresolved issues. Never describe sampled coverage as exhaustive.
