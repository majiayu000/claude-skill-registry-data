---
name: rewrite-yaml
description: Expert in test-first development of production-quality OpenRewrite recipes for YAML manipulation using LST structure, visitor patterns, and JsonPath matching. Automatically activates when working with OpenRewrite recipe files or Java files in `src/main/java/**/rewrite/**` directories.
---

# Writing OpenRewrite YAML Recipes

## Overview

Create production-quality OpenRewrite recipes for YAML manipulation using test-first development.

**Core principle:** Write tests first (RED), implement minimally (GREEN), apply OpenRewrite idioms (REFACTOR).

## When to Use

- User asks to create/modify OpenRewrite recipes for YAML
- Need to manipulate YAML files (GitHub Actions, K8s manifests, CI configs, generic YAML)
- Building search or transformation recipes for YAML structures

## When NOT to Use This Skill

Do not use this skill for:

- General YAML editing (use standard Edit tools)
- Non-OpenRewrite transformation tools
- Java versions above 8 (skill specializes in Java 8 compatibility)
- Generic code refactoring outside OpenRewrite ecosystem

## Critical Constraints

**JAVA 8 COMPATIBILITY ONLY**: Use traditional if-else, switch statements, explicit casting. NO switch expressions, pattern matching, `var`, text blocks, or Java 9+ features.

**LICENSE HEADERS**: Always check for `{repository_root}/gradle/licenseHeader.txt` when creating new recipe files. If this file exists, include its contents as the license header at the top of the generated Java recipe file. Remember to substitute `${year}` with the current year (2025 or later as appropriate).

## The Workflow

### Phase 1: RED - Write Failing Tests

Write test cases with before/after YAML examples using OpenRewrite's testing framework.

### Phase 2: Architecture Decision

Choose declarative (YAML composition) vs imperative (Java Visitor) approach.

### Phase 3: GREEN - Minimal Implementation

Implement just enough to make tests pass.

### Phase 4: REFACTOR - Apply OpenRewrite Idioms

Improve recipe using traits, composition, and conventions.

### Phase 5: Documentation

Add displayName, description (with markdown), and usage examples.

## Phase 1: RED - Write Failing Tests

### Test Structure

Use OpenRewrite's testing framework with before/after YAML. For detailed test patterns and examples, see `./references/testing-patterns.md`.

### Checklist

- [ ] Write happy path test (simplest transformation)
- [ ] Include edge cases (empty files, missing keys, null values)
- [ ] Test no-op scenarios (recipe shouldn't change unrelated YAML)
- [ ] Consider multi-document YAML if relevant
- [ ] Include real-world examples if domain is known

### Verification

Run tests to confirm RED state - tests must fail initially.

**Key principle:** Start with simplest possible before/after. Add complexity incrementally.

## Phase 2: Architecture Decision - Declarative vs Imperative

### Decision Framework

**Start with:** Can this be done by composing existing recipes?

- **YES** → Use declarative YAML recipe
- **NO** → Need imperative Java recipe with Visitor

### Declarative Recipe (YAML Composition)

Create YAML file in `src/main/resources/META-INF/rewrite/`:

```yaml
---
type: specs.openrewrite.org/v1beta/recipe
name: com.example.MyComposedRecipe
displayName: My composed recipe
description: Composes existing recipes
recipeList:
  - org.openrewrite.yaml.search.FindKey:
      keyPath: $.some.path
  - org.openrewrite.yaml.ChangeValue:
      keyPath: $.some.path
      value: newValue
```

**When to use declarative:**

- Simple transformations using existing recipes
- Searching for patterns
- Standard modifications (change values, delete keys)
- Composing multiple existing recipes

**Common declarative recipes:**

- `org.openrewrite.yaml.search.FindKey`, `FindValue` - searching
- `org.openrewrite.yaml.ChangeKey`, `ChangeValue`, `DeleteKey` - modifications
- `org.openrewrite.yaml.MergeYaml`, `CopyValue` - additions

### Imperative Recipe (Java Visitor)

**When to use imperative:**

- Complex logic or conditional transformations
- Need to traverse YAML LST structure
- Creating new YAML structures dynamically
- Custom matching beyond JsonPath capabilities

**Key principle:** Always try declarative first. Only go imperative when you hit limitations.

## Phase 3: GREEN - Minimal Implementation

### For Declarative Recipes

1. Create YAML file in `src/main/resources/META-INF/rewrite/`
2. Compose existing `org.openrewrite.yaml.*` recipes
3. Run tests to verify GREEN state

For common recipe patterns, see `./references/recipe-patterns.md`.

### For Imperative Recipes (Java Visitor)

Extend `YamlIsoVisitor<ExecutionContext>` (when not changing tree structure) or `YamlVisitor<ExecutionContext>` (when structure may change).

For complete recipe templates and examples, see `./references/recipe-template.java`.

**Automation:** Use `./scripts/init_recipe.py <RecipeName>` to generate recipe boilerplate (class, test file, YAML declarative option).

### Verification

Run tests to achieve GREEN state - all tests must pass with formatting preserved.

## Phase 4: REFACTOR - Apply OpenRewrite Idioms

### Checklist for Idiomatic Recipes

**1. Trait Usage**

- [ ] Can this recipe implement an existing trait?
- [ ] Should a new trait be created for reusable matching logic?
- [ ] Separate "what to find" (trait) from "what to do" (recipe)

**2. Recipe Composition**

- [ ] Can parts be extracted into smaller, composable recipes?
- [ ] Are there opportunities for configurability (parameters)?
- [ ] Could this be split into search recipe + modification recipe?

**3. OpenRewrite Conventions**

- [ ] Recipe has clear `displayName` and `description` (both support **markdown**)
- [ ] Parameters use `@Option` annotations with descriptions
- [ ] Recipe class is Java 8 compatible (run `./scripts/validate_java8.py src/` to check)
- [ ] Properly handles `null` values and missing elements
- [ ] Preserves formatting and comments where possible

**4. Performance Considerations**

- [ ] Minimize LST traversals (don't visit more than necessary)
- [ ] Use preconditions to skip files that won't match
- [ ] Return original object if no changes made (identity check)

### Verification

- [ ] All tests still pass after refactoring
- [ ] Recipe follows OpenRewrite naming conventions
- [ ] Code is cleaner and more maintainable

## Phase 5: Documentation

### Documentation Requirements

**Recipe metadata (supports markdown):**

- `displayName`: User-friendly name with markdown formatting
- `description`: Detailed explanation with code examples, lists, links
- `@Option` descriptions: Clear explanations with inline code examples

**Example with markdown:**

````java
@Override
public String getDisplayName() {
    return "Update GitHub Actions to `actions/checkout@v4`";
}

@Override
public String getDescription() {
    return "Updates all uses of `actions/checkout@v2` and `actions/checkout@v3` to `actions/checkout@v4`.\n\n" +
           "**Before:**\n```yaml\n- uses: actions/checkout@v2\n```\n\n" +
           "**After:**\n```yaml\n- uses: actions/checkout@v4\n```";
}
````

**Usage examples:**

- Add Javadoc with common use cases
- Show before/after transformations
- Document parameter effects

## Technical Reference

### YAML LST Structure

Understanding the YAML LST hierarchy is essential. For detailed structure documentation, see `./references/yaml-lst-reference.md`.

Key concepts:
- **Yaml.Documents** → **Yaml.Document** → **Yaml.Mapping** → **Yaml.Mapping.Entry**
- **Yaml.Sequence** → **Yaml.Sequence.Entry**
- **Yaml.Scalar** (primitive values)

### Essential Patterns

For complete recipe templates and patterns, see:
- `./references/recipe-template.java` - Complete recipe structure with annotations
- `./references/recipe-patterns.md` - Search, replacement, and modification patterns
- `./references/jsonpath-patterns.md` - Common JsonPath patterns for GitHub Actions, K8s, and generic YAML

### Quick Reference

**Key matching:**
```java
if ("targetKey".equals(entry.getKey().getValue())) { /* match */ }
```

**Safe value access:**
```java
String value = entry.getValue() instanceof Yaml.Scalar ?
    ((Yaml.Scalar) entry.getValue()).getValue() : null;
```

**JsonPath matching:**
```java
JsonPathMatcher matcher = new JsonPathMatcher("$.jobs.*.steps[*].uses");
if (matcher.matches(getCursor())) { /* process */ }
```

For more JsonPath patterns, search `./references/jsonpath-patterns.md` for your use case.

### Recipe Development Rules

1. Always call super methods: `return super.visitMappingEntry(entry, ctx);`
2. Return modified copies - never mutate LST elements directly
3. Use `withX()` methods for all modifications
4. Handle null cases with conditional expressions
5. Preserve formatting - LST methods maintain it automatically
6. Java 8 only - no modern Java features

### OpenRewrite Traits (Advanced)

For complex recipes that benefit from higher-level semantic abstractions, OpenRewrite Traits provide domain-specific logic by wrapping LST elements.

**For detailed information about Traits**, refer to the companion guide: `./references/openrewrite-traits-guide.md`.

**Quick Traits Overview:**

- Traits implement `Trait<T extends Tree>` interface
- Include a nested `Matcher` class extending `SimpleTraitMatcher<T>`
- Use `matcher.asVisitor()` to convert to TreeVisitor in recipes
- Provide semantic methods like `getActionRef()` instead of raw LST navigation

**Example using Traits:**

```java
@Override
public TreeVisitor<?, ExecutionContext> getVisitor() {
    return new ActionStep.Matcher().asVisitor((step, ctx) -> {
        String ref = step.getActionRef();
        if (ref != null && ref.contains("@v2")) {
            return step.withActionRef(ref.replace("@v2", "@v3")).getTree();
        }
        return step.getTree();
    });
}
```

For complete trait implementation patterns, matcher API details, and advanced examples, consult `./references/openrewrite-traits-guide.md`.

## Final Validation

### Production-Ready Checklist

- [ ] All tests pass (GREEN state maintained)
- [ ] Recipe follows OpenRewrite naming conventions (`com.yourorg.RecipeName`)
- [ ] No hardcoded values that should be parameters
- [ ] Recipe handles edge cases gracefully (no NPEs)
- [ ] Code is Java 8 compatible (verify with `./scripts/validate_java8.py`)
- [ ] Formatting/comments preserved in YAML output
- [ ] Documentation is clear and includes examples
- [ ] Recipe could be contributed to OpenRewrite or org recipe library
- [ ] License header included if `gradle/licenseHeader.txt` exists (use `./scripts/add_license_header.sh`)

### Success Criteria

Recipe is production-ready when:

- Tests comprehensively cover happy path and edge cases
- Implementation follows OpenRewrite idioms (traits, composition)
- Documentation enables users to understand and use the recipe
- Code quality meets standards for upstream contribution

## Recommended Approach

Follow this workflow when creating OpenRewrite recipes:

1. **Phase 1 (RED)** - Write failing tests with before/after YAML
2. **Phase 2 (DECIDE)** - Choose declarative vs imperative approach
3. **Phase 3 (GREEN)** - Implement minimal working solution
4. **Phase 4 (REFACTOR)** - Apply OpenRewrite idioms (traits, composition)
5. **Phase 5 (DOCUMENT)** - Add markdown documentation and examples
6. **Validate** - Confirm production readiness with checklist

Always provide complete, working recipes with proper annotations, error handling, and clear comments explaining the logic.

## Remember

- **Always start with tests (RED)**
- **Try declarative before imperative**
- **Apply idioms during REFACTOR, not GREEN**
- **Document with markdown for clarity**
- **Validate production-readiness before completion**
