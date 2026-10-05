---
name: review-interfaces
description: Review interface design for functions, classes, modules, components — naming, params, encapsulation, YAGNI, usability. Triggers "review interfaces".
argument-hint: '[--staged | --unpushed | --changed | --all]'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Review Interfaces

Interface design review for functions, classes, modules, and components.

## Usage

```
/review-interfaces                  # Review context-related code
/review-interfaces --staged         # Review staged changes
/review-interfaces --unpushed       # Review files changed across all unpushed commits
/review-interfaces --changed        # Review unstaged changes
/review-interfaces --all            # Full codebase audit (parallel agents)
```

## Scope

| Flag | Scope | Method |
|------|-------|--------|
| (none) | Context-related code | Files from the current conversation context: any files the user has discussed, opened, or that you have read/edited in this session. If no conversation context exists, ask the user to specify files or use `--staged`/`--changed`/`--all`. |
| `--staged` | Staged changes | `git diff --cached --name-only` |
| `--unpushed` | Files changed across unpushed commits | `git diff --name-only $(git rev-list HEAD --not --remotes \| tail -1)^..HEAD` |
| `--changed` | Unstaged changes | `git diff --name-only` |
| `--all` | Full codebase | Glob source files, parallel agents |

`--unpushed` derives its range from `git rev-list HEAD --not --remotes` (oldest unpushed commit's parent → HEAD). If nothing is unpushed, or there is no remote/upstream (or the range walks back to the root commit) so it can't be determined reliably, stop and ask the user to pick another scope.

## Gotchas
- Default scope (no flag) uses conversation context, which may be stale from an earlier part of the session. The review silently targets the wrong files if context has shifted.
- Internal/private interfaces have different standards than public/exported ones. A helper function used in one file does not need the same rigor as an exported component consumed by many callers. Always check whether an interface is public before flagging encapsulation issues.

## Workflow

1. **Determine scope** based on flags (see Scope table above)
2. **Review each file** against all 6 categories in the Interface Checklist below
3. **Parallelize** if scope has >5 files: spawn one sub-agent per category, each scanning all files for that category. Merge results and deduplicate.

   Dispatch workers that return findings without editing files. Disable delegation tools where supported; read-only access alone does not prevent delegation. Any coordinating role needs explicit subtasks, a descendant limit, and a stopping condition in its brief.
4. **Classify severity** for each finding:
   - **Critical**: Interface that actively misleads callers into incorrect usage, allows invalid states, or has a naming/type mismatch that will cause bugs
   - **High**: Interface with significant usability problems — too many params, weak types where strong types exist, public members that leak implementation
   - **Medium**: Suboptimal design that increases cognitive load — inconsistent naming, boolean flags, mild YAGNI violations
   - **Suggestion**: Improvement opportunity with marginal current impact
5. **Report findings** grouped by severity using the Output Format below

## Interface Checklist

### Pit of Success

Does the interface guide callers toward correct usage?

- Multiple ways to achieve the same result (e.g., `label` prop AND `children` both accepting text content) — pick one
- Consecutive parameters of the same type that invite transposition (e.g., `copy(string, string)`) — use named params or wrapper types
- Ambiguous defaults that lead to silent wrong behavior
- Easy to call incorrectly without a type or runtime error

### Naming & Readability

- Names that do not describe what the function/class/component does
- Inconsistent vocabulary across related interfaces (`remove` vs `delete` vs `destroy`)
- Asymmetric pairs (`open`/`close`, `start`/`end`, `add`/`remove`) — both should exist if either does
- Name does not match actual behavior (principle of least astonishment)
- Generic names (`data`, `info`, `handle`, `process`, `manager`) that obscure purpose

### Signature Design

- More than 3-4 parameters — use an options/config object
- Boolean flag parameters (opaque at call site: `render(true)`) — use named options or separate functions
- Weak types where stronger types exist (`string` for a known set of values → use enum/union)
- Inconsistent parameter ordering across related functions
- Missing return type annotations on public functions
- Returning `null` where an empty collection would eliminate null checks for callers

### Surface Area & Encapsulation

- Public members that should be private/internal
- Internal types or implementation details exposed in the public interface
- Missing explicit exports (everything public by default)
- Transitive dependency types leaked through the public interface
- Mutable internal state exposed directly instead of via copies or accessors

### Flexibility & YAGNI

- Parameters, props, or configuration that no current caller uses
- Over-abstracted interfaces solving hypothetical future requirements
- Under-constrained types that allow invalid states (e.g., `status: string` instead of `status: 'active' | 'inactive'`)
- Premature abstraction — generic framework for a single use case
- Configuration surface area that exceeds what callers actually vary

### Composition & Extensibility

- Deep inheritance hierarchies where composition would be simpler
- God objects/components with too many responsibilities
- Violation of single responsibility — function/class needs "and" in its description
- Tight coupling — reaching through object chains (`a.getB().getC().doThing()`)
- Missing separation of logic and presentation (for UI components)

For annotated BAD/GOOD code examples for each category, see `references/interface-checklist.md`.

## Output Format

```markdown
## Interface Review: {scope}

### Critical (misleads callers / allows invalid states)
- {file}:{line} - {issue type}: {description}
  **Impact:** {why it matters}
  **Fix:** {solution with code example}

### High Priority
- {file}:{line} - {issue}
  **Fix:** {solution}

### Medium Priority
- {file} - {issue}

### Suggestions
- {improvement opportunity}
```

## Examples

**Staged changes introduce a component with overlapping props:**
> /review-interfaces --staged

Reviews staged files and catches a `<Button>` component that accepts both `label` (string) and `children` for button text. Reports it as Critical with the impact ("callers will disagree on which to use, leading to inconsistent behavior") and a fix to remove `label` in favor of `children`.

**Full audit finds god class with 15 public methods:**
> /review-interfaces --all

Parallel agents scan the full codebase by category. Finds a `UserService` class that handles authentication, profile updates, notification preferences, and billing — four distinct responsibilities. Suggests splitting into focused services.

## Troubleshooting

### False positive on an intentionally flexible interface
**Solution:** If the interface is intentionally generic (e.g., a utility library), note the design decision in a code comment (e.g., `// Intentionally flexible: used by 5+ consumers with different needs`). Re-run the review and the context will help distinguish intentional flexibility from accidental over-engineering.

### Disagreement on parameter count threshold
**Solution:** The 3-4 parameter guideline is a heuristic. Functions with 5 well-named, distinct-typed parameters may be fine. The real signal is: can a caller guess the correct argument order without checking the signature? If yes, the count is acceptable.

## Notes

- Focus on public/exported interfaces — internal helpers have lower standards
- Consider the number of callers: a function used once has different design pressure than one used everywhere
- Language idioms matter: what's good in Python may not apply in TypeScript
- For `--all`, use parallel agents per category
- Interface issues compound: a poorly named function with too many params and weak types is worse than the sum of its parts
