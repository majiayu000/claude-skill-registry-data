---
name: coding-guardrails
description: Enforce ThemeGPT complexity budgets and prevent over-engineering. Activates automatically when writing, reviewing, or refactoring code. Validates against 6 anti-patterns from SynthAI archaeology (Specification Inflation, Enterprise Pattern Obsession, Premature Abstraction, Configuration Explosion, Framework Absorption, Test Suite Inflation). Use when creating features, adding abstractions, writing tests, or configuring projects.
---

# Coding Guardrails

Enforce simplicity-first development and prevent complexity accumulation. This skill activates automatically during coding tasks to validate decisions against ThemeGPT's development philosophy.

## Required Reading

Before any coding task, mentally reference:
- **CONSTITUTION.md**: Philosophical principles (Simplicity > Privacy > Accessibility)
- **DIRECTIVES.md**: Enforcement rules with specific limits
- **doc/guard/SYNTHAI_PROJECT_ARCHAEOLOGY.md**: Historical lessons on over-engineering

## Complexity Budget Enforcement

### Hard Limits (Block if Exceeded)

| Metric | Limit | Action |
|--------|-------|--------|
| Single file | 200 lines | Pause and reassess |
| Feature total | 500 lines | Require architectural review |
| Configuration files | 50 lines total | Justify why hard-coding fails |
| Abstract classes | 0 | Require 3+ concrete implementations first |
| Test files | < 50% of implementation | Review necessity |

### Pre-Implementation Checklist

Before writing any code, answer:

1. **Scale Check:** Does this complexity match the problem scale?
2. **Abstraction Check:** Is there proven duplication (3+ occurrences)?
3. **Pattern Check:** Would this pattern be appropriate for a browser extension?
4. **Configuration Check:** Can this value be hard-coded instead?

If any answer suggests simpler alternatives, use them.

## Anti-Pattern Recognition

Actively flag and prevent these patterns from SynthAI archaeology:

### Pattern 1: Specification Inflation

**Warning Signs:**
- Specs describe implementation details, not outcomes
- Specification longer than estimated implementation
- Bulleted requirements spawn multiple files

**Response:** Rewrite to focus on outcomes only. Ask "What problem does this solve?" not "How should it be built?"

### Pattern 2: Enterprise Pattern Obsession

**Warning Signs:**
- Circuit breakers for local tools
- Service registries for < 5 items
- Rollback managers for single-user applications
- Audit logging beyond console output

**Response:** Remove or justify with concrete scale requirements. Browser extensions don't need enterprise infrastructure.

### Pattern 3: Premature Abstraction

**Warning Signs:**
- Abstract class with 1 implementation
- Interface before concrete use case
- Adapter pattern for single provider
- Factory pattern for single object type

**Response:** Delete abstraction. Write concrete implementation. Add abstraction only when 3+ duplications exist.

**Example:**
```typescript
// BAD: Premature abstraction
abstract class BaseProvider {
  abstract call(input: string): Promise<string>;
}
class OpenAIProvider extends BaseProvider { ... }
// Only one provider exists!

// GOOD: Direct implementation
async function callOpenAI(input: string): Promise<string> {
  return await openai.complete(input);
}
```

### Pattern 4: Configuration Explosion

**Warning Signs:**

- Config file growing beyond 50 lines
- Environment variables for internal values
- YAML/JSON for hard-codeable constants
- Configuration for "flexibility"

**Response:** Hard-code by default. Make configurable only when users demonstrably need to change values.

**Example:**

```typescript
// BAD: Configuration for hard-codeable value
const config = loadConfig();
const MAX_TOKENS = config.maxTokens ?? 4096;

// GOOD: Hard-coded default
const MAX_TOKENS = 4096;
```

### Pattern 5: Framework Absorption

**Warning Signs:**

- Domain-specific types in utility modules
- Framework concepts leaking into generic code
- Every module imports domain-specific types

**Response:** Keep domain frameworks separate. Utilities should have no domain dependencies.

### Pattern 6: Test Suite Inflation

**Warning Signs:**

- Tests approaching implementation size
- Tests per function instead of per behavior
- High coverage on trivial code

**Response:** Tests < 50% of implementation lines. Test behavior, not implementation. Skip tests for trivial code (getters, simple mappings).

## Decision Framework

When principles conflict, apply this priority:

1. **Simplicity** — Never add complexity beyond what the problem requires
2. **Privacy** — Never compromise user data protection
3. **Accessibility** — Never exclude users
4. **Brand Integrity** — Maintain visual consistency
5. **Completeness** — No placeholders or incomplete features
6. **Performance** — Fast, responsive extension

## Verification Commands

Run these checks before committing:

```bash
# Check for files over 200 lines (warning threshold)
find apps packages -name "*.ts" -o -name "*.tsx" | xargs wc -l | awk '$1 > 200 {print "WARNING:", $0}'

# Check for placeholder content
grep -rE "TODO|FIXME|TBD|XXX|lorem ipsum" --include="*.ts" --include="*.tsx" apps/ packages/

# Check for premature abstractions
grep -rE "abstract class|interface.*Adapter|Registry|Factory" --include="*.ts" apps/ packages/

# Check config file sizes
find . -name "*.json" -o -name "*.yaml" | xargs wc -l | awk '{sum+=$1} END {print "Total config lines:", sum}'

# Check test-to-implementation ratio
echo "Test lines:" && find apps packages -name "*.test.ts" | xargs wc -l 2>/dev/null | tail -1
echo "Impl lines:" && find apps packages -name "*.ts" ! -name "*.test.ts" | xargs wc -l 2>/dev/null | tail -1
```

## Response Protocol

When this skill activates during a coding task:

1. **Before Implementation:** Run pre-implementation checklist mentally
2. **During Implementation:** Flag any anti-pattern warning signs immediately
3. **Before Committing:** Run verification commands
4. **If Limits Exceeded:** Stop, explain the concern, propose simpler alternative

## Key Phrase Triggers

Activate heightened scrutiny when you hear:

- "We might need..."
- "For flexibility..."
- "In case of..."
- "Best practice says..."
- "Enterprise-grade..."
- "Future-proof..."

These phrases often precede unnecessary complexity.

## Simplicity Mantra

> "Sometimes the best code is the code you don't write."
> — SynthAI Project Archaeology

When in doubt, implement the minimal solution. Complexity can be added later; removing it is much harder.
