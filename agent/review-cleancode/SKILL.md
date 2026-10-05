---
name: review-cleancode
description: Review code for clean-code principles — SOLID, DRY, YAGNI, KISS, code smells. Triggers "review clean code", "check DRY/SOLID", "code smells".
argument-hint: '[--staged | --unpushed | --changed | --all | --multi]'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Review Clean Code

Language-agnostic clean code review covering SOLID, DRY, YAGNI, KISS, design principles, and code smells.

## Usage

```
/review-cleancode                  # Review context-related code
/review-cleancode --staged         # Review staged changes
/review-cleancode --unpushed       # Review files changed across all unpushed commits
/review-cleancode --changed        # Review unstaged changes
/review-cleancode --all            # Full codebase audit (parallel agents)
/review-cleancode --multi          # Also get external advisor opinions
```

## Scope

| Flag | Scope | Method |
|------|-------|--------|
| (none) | Context-related code | Files from the current conversation context. If no context, ask the user to specify files or use `--staged`/`--changed`/`--all`. |
| `--staged` | Staged changes | `git diff --cached --name-only` |
| `--unpushed` | Files changed across unpushed commits | `git diff --name-only $(git rev-list HEAD --not --remotes \| tail -1)^..HEAD` |
| `--changed` | Unstaged changes | `git diff --name-only` |
| `--all` | Full codebase | Glob source files, parallel agents |
| `--multi` | Add external opinions | Combines with any scope above; invokes `second-opinion --quick` |

`--unpushed` derives its range from `git rev-list HEAD --not --remotes` (oldest unpushed commit's parent → HEAD). If nothing is unpushed, or there is no remote/upstream (or the range walks back to the root commit) so it can't be determined reliably, stop and ask the user to pick another scope. Like `--staged`, it reviews full file content, not just the diff.

## Gotchas
- Default scope (no flag) uses conversation context, which may be stale if context has shifted during the session.
- DRY violations across distant files are hard to detect without `--all` scope. Staged reviews only catch duplication within the diff.
- YAGNI is subjective — unused flexibility may be intentional (library/framework code). Check if the code is consumed externally before flagging.

## Workflow

1. **Determine scope** based on flags (see Scope table above)
2. **Read CLAUDE.md** in the repository root to understand project-specific conventions
3. **Review each file** against all 5 categories in the Clean Code Checklist below
4. **Parallelize** if scope has >5 files: spawn one sub-agent per category, each scanning all files for that category. Merge results and deduplicate.

   Dispatch workers that return findings without editing files. Disable delegation tools where supported; read-only access alone does not prevent delegation. Any coordinating role needs explicit subtasks, a descendant limit, and a stopping condition in its brief.
5. **External opinions** (if `--multi`): invoke `second-opinion --quick`, which queries every advisor it has configured, in parallel (the roster lives in the `second-opinion` skill), with this prompt:

```
Read-only clean code review. Review the code in this repository (use `git diff --cached` for `--staged`, `git diff` for `--changed`, or read the relevant files). Evaluate against clean code principles: SOLID, DRY, YAGNI, KISS, Law of Demeter, code smells (god classes, long methods, feature envy, primitive obsession, shotgun surgery). Provide a focused review in 300 words or less.
```

Wait for all external results before proceeding to step 6.

6. **Classify severity** for each finding:
   - **Critical**: Structural issue that will cause bugs or make changes dangerous (e.g., shotgun surgery, broken LSP, god class actively accumulating responsibility)
   - **High**: Significant maintainability problem (e.g., DRY violation across 3+ locations, deep inheritance instead of composition, feature envy)
   - **Medium**: Design issue that increases cognitive load (e.g., long method, primitive obsession, minor YAGNI)
   - **Suggestion**: Improvement opportunity with marginal current impact
7. **Report findings** grouped by severity using the Output Format below

## Clean Code Checklist

### 1. SOLID Principles

- **SRP**: Does the class/function have a single reason to change? Can you describe it without "and"?
- **OCP**: Can new behavior be added without modifying existing code? Watch for growing switch/if chains on type codes.
- **LSP**: Do subclasses honor the parent's contract? Watch for overrides that throw "not implemented" or change semantics.
- **ISP**: Are interfaces focused? Do implementors need to stub unused methods?
- **DIP**: Do high-level modules depend on abstractions or concrete implementations?

### 2. Foundational Principles

- **DRY**: Is the same logic repeated in multiple places? Would a change require edits in multiple files?
- **YAGNI**: Is there code, parameters, or abstraction for hypothetical future needs that nothing currently uses?
- **Reuse-first (anti-reinvention)**: Before accepting hand-written code, walk the ladder — could it be replaced by (1) a helper/util/pattern already in this codebase, (2) the standard library, (3) a native platform feature (`<input type="date">` over a date-picker lib, CSS over JS, a DB constraint over app code), or (4) an already-installed dependency? Hand-rolling what one of these already ships is the most common avoidable bloat; a new dependency added for what a few lines or a present dep covers is its inverse. When flagging, name the specific replacement, not just "this is complex."
- **KISS**: Could a simpler approach achieve the same result? Are there clever tricks that obscure intent?
- **Fail Fast**: Are inputs validated early, before expensive work?

### 3. Design Principles

- **Law of Demeter**: Long chains like `a.getB().getC().getValue()`?
- **Separation of Concerns**: Business logic mixed with infrastructure, UI, or persistence?
- **Composition over Inheritance**: Deep hierarchies (>2 levels) used for code reuse rather than polymorphism?
- **Principle of Least Astonishment**: Does the function do what its name suggests? Hidden side effects?
- **Tell Don't Ask**: Querying object state then acting on it externally instead of telling the object?
- **Command-Query Separation**: Methods that both mutate state and return data?
- **Encapsulation**: Internal state exposed directly? Getters returning mutable references?
- **Cohesion/Coupling**: Unrelated methods in one class? Excessive dependencies between modules?

### 4. Code Smells

- **God Class**: Class with too many responsibilities (>~300 lines, multiple unrelated method groups)
- **Long Method**: Method doing multiple phases (>~20 lines, multiple levels of nesting)
- **Feature Envy**: Method uses another class's data more than its own
- **Data Class**: Fields + getters/setters only, no behavior
- **Duplicate Code**: Identical or near-identical blocks in multiple locations
- **Message Chains**: Long chains through intermediate objects
- **Primitive Obsession**: Strings/ints for concepts that deserve value types
- **Long Parameter List**: 4+ parameters that should be grouped
- **Dead Code**: Unused functions, unreachable branches, unused imports
- **Speculative Generality**: Abstractions, configs, or flexibility for nonexistent use cases
- **Shotgun Surgery**: One logical change requires edits across many files
- **Divergent Change**: One class modified for multiple unrelated reasons
- **Data Clumps**: Same group of parameters passed together repeatedly

### 5. Readability & Structure

- **Guard Clauses**: Deep nesting that could use early returns
- **Meaningful Names**: Cryptic abbreviations, generic names (`data`, `info`, `process`)
- **Small Functions**: Functions with section comments (signal they do too much)
- **Comments**: "What" comments that should be "why" comments, or could be replaced by better naming
- **Declarative Style**: Imperative loops where filter/map/reduce would be clearer (but not dogmatically)

For annotated BAD/GOOD code examples for each category, see `references/cleancode-checklist.md`.

## Output Format

```markdown
## Clean Code Review: {scope}

### Critical (structural issues, bug risk)
- {file}:{line} - {category}: {description}
  **Impact:** {why it matters}
  **Fix:** {solution with code example}

### High Priority (maintainability)
- {file}:{line} - {category}: {description}
  **Fix:** {solution}

### Medium Priority (cognitive load)
- {file} - {category}: {description}

### Suggestions
- {improvement opportunity}

**Net:** ~{N} lines removable across the findings above (omit if nothing is cuttable).
```

If `--multi` was used, append:

```markdown
### External Opinions

Add one subsection per advisor that responded, titled with the advisor's name as reported by `second-opinion`:

#### {advisor name}
{that advisor's review}

#### Cross-Model Agreement
{areas where the external advisors agree/disagree with the Claude review — consensus issues (flagged by multiple models) get higher confidence}
```

## Examples

**Staged changes with DRY violation:**
> /review-cleancode --staged

Reviews staged files and catches the same email validation logic duplicated in `createUser` and `updateUser`. Reports as High with fix to extract a shared `validateEmail` function.

**Full codebase audit finds god class:**
> /review-cleancode --all

Parallel agents scan by category. Finds `AppService` handling auth, payments, notifications, and reporting — four distinct responsibilities. Reports as Critical with a split plan.

**Get external opinions on clean code quality:**
> /review-cleancode --multi --staged

Runs the 5-category review plus the external advisors. Cross-model agreement highlights a SOLID violation multiple reviewers independently flagged.

## Troubleshooting

### Too many false positives on YAGNI
**Solution:** Check whether the code is a library or framework consumed by external callers. Flexibility is expected in public APIs. Add context in a code comment (e.g., `// Public API: consumers use these options`) and re-run.

### DRY violations not caught across distant files
**Solution:** Use `--all` scope. The default, `--staged`, and `--changed` scopes only see a subset of the codebase, so cross-file duplication requires the full scan.

### Disagreement on class/method size thresholds
**Solution:** The ~300 line / ~20 line guidelines are heuristics, not rules. A 25-line method that does one clear thing is fine. The real signal: can you describe what it does in one sentence without "and"?

## Notes

- Apply judgment, not dogma — these are principles, not laws
- Consider context: a startup prototype has different standards than a banking system
- Language idioms matter: what's idiomatic in Python may not apply in Go
- For `--all`, use parallel agents per category (5 agents)
- Multiple violations compound: a god class with long methods and feature envy is worse than the sum of its parts
