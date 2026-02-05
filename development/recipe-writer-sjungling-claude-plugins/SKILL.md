---
name: recipe-writer
description: Expert in test-first development of production-quality OpenRewrite recipes for automated code refactoring. Automatically activates when working with OpenRewrite recipe files, Java/YAML files in `src/main/java/**/rewrite/**` directories, writing tests implementing `RewriteTest`, or when users ask about recipe development, writing recipes, creating migrations, LST manipulation, JavaTemplate usage, visitor patterns, preconditions, scanning recipes, YAML recipes, GitHub Actions transformations, Kubernetes manifest updates, or code migration strategies. Guides recipe type selection (declarative/Refaster/imperative), visitor implementation, and test-driven development workflows.
---

# OpenRewrite Recipe Writing Expert

## Overview

Create production-quality OpenRewrite recipes using test-first development. This skill combines comprehensive coverage of all recipe types (declarative, Refaster, imperative) with deep domain expertise in Java and YAML transformations.

**Core Principle:** Write tests first (RED), implement minimally (GREEN), apply OpenRewrite idioms (REFACTOR).

## When to Use This Skill

Explicitly invoke this skill for:

- **Planning recipes** - Determining the best recipe type for a use case
- **Implementing recipes** - Writing recipe classes, visitors, and JavaTemplate code
- **Writing tests** - Creating comprehensive test coverage with RewriteTest
- **YAML transformations** - GitHub Actions, Kubernetes manifests, CI/CD configs
- **Java refactoring** - Code migrations, API updates, framework modernization
- **Debugging recipes** - Troubleshooting visitor behavior, type checking, or preconditions
- **Converting recipe types** - Analyzing if an imperative recipe can be declarative
- **Understanding OpenRewrite concepts** - Learning about LSTs, cursors, traits, or scanning patterns

## When NOT to Use This Skill

Do NOT invoke this skill for:

- **General Java programming questions** - Use standard Java knowledge unless specifically about OpenRewrite LST manipulation
  - ❌ "How do I parse JSON in Java?"
  - ✅ "How do I parse Java code into LSTs?"
- **General YAML editing** - Use standard Edit tools for direct file modifications
  - ❌ "Edit this YAML file to change the value"
  - ✅ "Create a recipe to update GitHub Actions across all repositories"
- **Running OpenRewrite recipes** - This skill is for authoring recipes, not executing them
  - ❌ "How do I run the Maven plugin?"
  - ✅ "How do I test my recipe runs correctly?"
- **Build tool configuration** - Unless directly related to recipe publishing/distribution
  - ❌ "How do I configure Gradle for my project?"
  - ✅ "How do I publish my recipe to Maven Central?"
- **General refactoring questions** - Only use for OpenRewrite recipe implementation
  - ❌ "What's the best way to refactor this code?"
  - ✅ "What recipe type should I use for this refactoring?"
- **Reading/understanding existing code** - Unless analyzing recipe implementation
  - ❌ "Explain what this Spring controller does"
  - ✅ "Explain what this JavaIsoVisitor is doing"

## Quick Examples

Here are example requests that activate this skill:

**Planning:**
- "I need to migrate from JUnit 4 to JUnit 5 - help me plan the recipe"
- "What's the best recipe type to replace all ArrayList with List?"
- "Should I use a declarative or imperative recipe for adding annotations?"
- "Help me create a recipe to update GitHub Actions to use Node 20"

**Java Implementation:**
- "Write a recipe that adds @Deprecated to classes in com.example.old package"
- "Show me how to use JavaTemplate to add a method to a class"
- "Create a recipe that changes method return types from Optional to nullable"

**YAML Implementation:**
- "Create a recipe to update all GitHub Actions checkout actions to v4"
- "Write a recipe to change Kubernetes image tags across all manifests"
- "Build a recipe to migrate Travis CI configs to GitHub Actions"

**Debugging:**
- "My recipe isn't matching the expected classes - help debug"
- "Why is my JavaTemplate throwing a parse error?"
- "The recipe runs but doesn't make any changes - what's wrong?"
- "My YAML recipe isn't preserving comments - how do I fix it?"

**Testing:**
- "Write tests for a ScanningRecipe that analyzes multiple files"
- "How do I test a recipe that requires external classpath dependencies?"
- "Show me how to test edge cases in my YAML recipe"

## Recipe Type Selection

Choose the appropriate recipe type based on your needs.

### Decision Tree

```
Start here
    ├─ Can I compose existing recipes? ───────────────────┐
    │   YES → Use Declarative YAML                         │
    │   NO ↓                                                │
    ├─ Is it a simple expression/statement replacement? ───┤
    │   YES → Use Refaster Template                        │
    │   NO ↓                                                │
    └─ Do I need custom logic or conditional changes? ─────┤
        YES → Use Imperative Java Recipe                   │
                                                            │
Still unsure? → Start with declarative, fall back to ─────┘
               imperative only when necessary
```

### Recipe Type Comparison

| Type | Speed | Complexity | Use Cases | Examples |
|------|-------|------------|-----------|----------|
| **Declarative YAML** | Fastest | Lowest | Composing existing recipes | Framework migrations, standard refactorings |
| **Refaster Template** | Fast | Low-Medium | Expression/statement replacements | API updates, method call changes |
| **Imperative Java** | Slower | High | Complex transformations, conditional logic | Custom analysis, YAML LST manipulation |

### Declarative YAML Recipes (Preferred)

**Use when:** Composing existing recipes with configuration

**Advantages:**
- No code required
- Simple and maintainable
- Fast execution
- Easy to understand

**Example use case:** Combining framework migration steps

```yaml
type: specs.openrewrite.org/v1beta/recipe
name: com.yourorg.MyMigration
displayName: Migrate to Framework X
recipeList:
  - org.openrewrite.java.ChangeType:
      oldFullyQualifiedTypeName: old.Type
      newFullyQualifiedTypeName: new.Type
  - com.yourorg.OtherRecipe
```

**Common declarative recipes:**
- Java: `ChangeType`, `ChangeMethodName`, `AddDependency`, `UpgradeDependencyVersion`
- YAML: `FindKey`, `FindValue`, `ChangeKey`, `ChangeValue`, `DeleteKey`, `MergeYaml`, `CopyValue`

### Refaster Template Recipes

**Use when:** Simple expression/statement replacements with type awareness

**Advantages:**
- Faster than imperative recipes
- Type-aware matching
- Concise syntax
- Good for API migrations

**Example use case:** Replace `StringUtils.equals()` with `Objects.equals()`

```java
public class StringUtilsToObjects {
    @BeforeTemplate
    boolean before(String s1, String s2) {
        return StringUtils.equals(s1, s2);
    }

    @AfterTemplate
    boolean after(String s1, String s2) {
        return Objects.equals(s1, s2);
    }
}
```

### Imperative Java Recipes

**Use when:** Complex logic, conditional transformations, custom analysis, or YAML/LST manipulation

**Advantages:**
- Full control over transformation logic
- Complex transformations possible
- Access to full LST structure
- Can implement custom matching

**Example use case:**
- Add modifiers only to variables that aren't reassigned
- Transform YAML based on complex conditions
- Generate new files based on analysis
- Multi-file coordination with ScanningRecipe

**Decision Rule:** If it can be declarative, make it declarative. Use Refaster for simple replacements. Use imperative only when necessary.

## Test-First Development Workflow

Follow the RED-GREEN-REFACTOR cycle for recipe development:

```
Phase 1: RED (Write Failing Tests)
    ↓
Phase 2: DECIDE (Select Recipe Type)
    ↓
Phase 3: GREEN (Minimal Implementation)
    ↓
Phase 4: REFACTOR (Apply OpenRewrite Idioms)
    ↓
Phase 5: DOCUMENT (Add Metadata & Examples)
    ↓
Phase 6: VALIDATE (Production Readiness)
```

### Phase 1: RED - Write Failing Tests

Start with tests before writing any recipe code. This ensures you understand the transformation and can verify correctness.

**For Java recipes:**

```java
class YourRecipeTest implements RewriteTest {

    @Override
    public void defaults(RecipeSpec spec) {
        spec.recipe(new YourRecipe("parameter-value"));
    }

    @Test
    void makesExpectedChange() {
        rewriteRun(
            //language=java
            java(
                // Before
                """
                  package com.example;
                  class Before { }
                  """,
                // After
                """
                  package com.example;
                  class After { }
                  """
            )
        );
    }

    @Test
    void doesNotChangeWhenNotNeeded() {
        rewriteRun(
            //language=java
            java(
                """
                  package com.example;
                  class AlreadyCorrect { }
                  """
                // No second argument = no change expected
            )
        );
    }
}
```

**For YAML recipes:**

```java
class YourYamlRecipeTest implements RewriteTest {

    @Override
    public void defaults(RecipeSpec spec) {
        spec.recipe(new YourYamlRecipe());
    }

    @Test
    void updatesGitHubActionsCheckout() {
        rewriteRun(
            //language=yaml
            yaml(
                """
                  jobs:
                    build:
                      steps:
                        - uses: actions/checkout@v2
                  """,
                """
                  jobs:
                    build:
                      steps:
                        - uses: actions/checkout@v4
                  """
            )
        );
    }
}
```

**Test Checklist:**
- [ ] Write happy path test (simplest transformation)
- [ ] Include edge cases (nulls, empty files, missing elements)
- [ ] Test no-op scenarios (recipe shouldn't change unrelated code)
- [ ] Test multi-document YAML if relevant
- [ ] Include real-world examples if domain is known
- [ ] Run tests to confirm RED state - tests must fail initially

**Key Principle:** Start with simplest possible before/after. Add complexity incrementally.

### Phase 2: DECIDE - Select Recipe Type

Use the decision tree above to choose between declarative, Refaster, or imperative.

**Ask yourself:**
1. Can this be done by composing existing recipes? → Declarative
2. Is it a simple expression/statement replacement? → Refaster
3. Does it need custom logic or LST manipulation? → Imperative

**For YAML-specific decisions:**
- Simple value changes, key renames → Declarative (use `ChangeValue`, `ChangeKey`)
- Complex JsonPath matching with conditions → Imperative
- Multi-step YAML transformations → Declarative (compose multiple recipes)
- Dynamic YAML generation → Imperative

### Phase 3: GREEN - Minimal Implementation

Implement just enough to make tests pass. Don't optimize or refactor yet.

**For declarative recipes:**

1. Create YAML file in `src/main/resources/META-INF/rewrite/`
2. Compose existing recipes
3. Run tests to verify GREEN state

**For imperative Java recipes:**

Use templates from `./templates/` directory:
- `template-imperative-recipe.java` - Complete recipe structure
- `template-recipe-test.java` - Test structure

**Automation:** Use `./scripts/init_recipe.py <RecipeName>` to generate boilerplate.

**For YAML recipes, extend YamlIsoVisitor:**

```java
public class YourYamlRecipe extends Recipe {

    @Override
    public String getDisplayName() {
        return "Your recipe display name";
    }

    @Override
    public String getDescription() {
        return "Description of transformation.";
    }

    @Override
    public TreeVisitor<?, ExecutionContext> getVisitor() {
        return new YamlIsoVisitor<ExecutionContext>() {
            @Override
            public Yaml.Mapping.Entry visitMappingEntry(Yaml.Mapping.Entry entry, ExecutionContext ctx) {
                entry = super.visitMappingEntry(entry, ctx);

                // Match specific key
                if ("targetKey".equals(entry.getKey().getValue())) {
                    // Safe value access
                    if (entry.getValue() instanceof Yaml.Scalar) {
                        Yaml.Scalar scalar = (Yaml.Scalar) entry.getValue();
                        if ("oldValue".equals(scalar.getValue())) {
                            return entry.withValue(
                                scalar.withValue("newValue")
                            );
                        }
                    }
                }

                return entry;
            }
        };
    }
}
```

**Verification:** Run tests to achieve GREEN state - all tests must pass.

### Phase 4: REFACTOR - Apply OpenRewrite Idioms

Now improve the recipe using OpenRewrite best practices. Don't skip GREEN to do this - refactoring comes AFTER tests pass.

**Refactoring Checklist:**

**1. Trait Usage** (Advanced)
- [ ] Can this recipe implement an existing trait?
- [ ] Should a new trait be created for reusable matching logic?
- [ ] Separate "what to find" (trait) from "what to do" (recipe)

See `./references/trait-implementation-guide.md` for details.

**2. Recipe Composition**
- [ ] Can parts be extracted into smaller, composable recipes?
- [ ] Are there opportunities for configurability (parameters)?
- [ ] Could this be split into search recipe + modification recipe?

**3. OpenRewrite Conventions**
- [ ] Recipe has clear `displayName` and `description` (both support markdown)
- [ ] Parameters use `@Option` annotations with descriptions and examples
- [ ] Properly handles `null` values and missing elements
- [ ] Preserves formatting and comments where possible
- [ ] Uses `@Value` and `@EqualsAndHashCode(callSuper = false)` for immutability
- [ ] `getVisitor()` returns NEW instance (never cached)

**4. Performance Considerations**
- [ ] Minimize LST traversals (don't visit more than necessary)
- [ ] Use preconditions to skip files that won't match
- [ ] Return original object if no changes made (identity check)

**5. YAML-Specific Refactoring**
- [ ] Use JsonPath matching for complex patterns
- [ ] Handle multi-document YAML if relevant
- [ ] Preserve YAML anchors and aliases
- [ ] Test with real-world files (GitHub Actions, K8s, etc.)

**Verification:**
- [ ] All tests still pass after refactoring
- [ ] Recipe follows OpenRewrite naming conventions
- [ ] Code is cleaner and more maintainable

### Phase 5: DOCUMENT - Add Metadata & Examples

Add comprehensive documentation to make the recipe discoverable and understandable.

**Recipe Metadata (supports markdown):**

```java
@Override
public String getDisplayName() {
    return "Update GitHub Actions to `actions/checkout@v4`.";
}

@Override
public String getDescription() {
    return "Updates all uses of `actions/checkout@v2` and `actions/checkout@v3` to `actions/checkout@v4`.\n\n" +
           "**Before:**\n```yaml\n- uses: actions/checkout@v2\n```\n\n" +
           "**After:**\n```yaml\n- uses: actions/checkout@v4\n```";
}
```

**Option Documentation:**

```java
@Option(
    displayName = "Old action reference",
    description = "The old action reference to replace (e.g., `actions/checkout@v2`).",
    example = "actions/checkout@v2"
)
String oldActionRef;
```

**Javadoc:**
- Add class-level Javadoc with use cases
- Show before/after transformations
- Document parameter effects
- Link to related recipes

**Naming Conventions:**
- Display names: Sentence case, code in backticks, end with period
- Recipe names: `com.yourorg.VerbNoun` (e.g., `com.yourorg.UpdateGitHubActions`)

### Phase 6: VALIDATE - Production Readiness

Use the comprehensive checklist to ensure production quality.

**Quick Validation:**
- [ ] All tests pass (GREEN state maintained)
- [ ] Recipe handles edge cases gracefully (no NPEs)
- [ ] Formatting/comments preserved in output
- [ ] Documentation is clear and includes examples
- [ ] Recipe is idempotent (same result on repeated runs)

**Full Validation:**
See `./references/checklist-recipe-development.md` for 200+ validation items.

**License Headers:**
Check for `{repository_root}/gradle/licenseHeader.txt`. If exists, use `./scripts/add_license_header.sh` to add headers.

## Implementation Patterns

Quick reference for common implementation patterns.

### Java Recipes

**Set Up Recipe Class:**

```java
@Value
@EqualsAndHashCode(callSuper = false)
public class YourRecipe extends Recipe {

    @Option(displayName = "Parameter Name",
            description = "Clear description.",
            example = "com.example.Type")
    String parameterName;

    @Override
    public String getDisplayName() {
        return "Your recipe display name.";
    }

    @Override
    public String getDescription() {
        return "What this recipe does.";
    }

    @Override
    public TreeVisitor<?, ExecutionContext> getVisitor() {
        return new YourVisitor();
    }
}
```

**Implement Visitor:**

```java
public class YourVisitor extends JavaIsoVisitor<ExecutionContext> {

    @Override
    public J.ClassDeclaration visitClassDeclaration(J.ClassDeclaration classDecl, ExecutionContext ctx) {
        // ALWAYS call super to traverse the tree
        J.ClassDeclaration cd = super.visitClassDeclaration(classDecl, ctx);

        // Check if change is needed (do no harm)
        if (!shouldChange(cd)) {
            return cd;
        }

        // Make changes using JavaTemplate or LST methods
        cd = makeChanges(cd);

        return cd;
    }
}
```

**Use JavaTemplate:**

```java
private final JavaTemplate template = JavaTemplate
    .builder("public String hello() { return \"Hello from #{}!\"; }")
    .build();

// In visitor method:
classDecl = template.apply(
    new Cursor(getCursor(), classDecl.getBody()),
    classDecl.getBody().getCoordinates().lastStatement(),
    fullyQualifiedClassName
);
```

**Add Preconditions:**

```java
@Override
public TreeVisitor<?, ExecutionContext> getVisitor() {
    return Preconditions.check(
        Preconditions.and(
            new UsesType<>("com.example.Type", true),
            new UsesJavaVersion<>(17)
        ),
        new YourVisitor()
    );
}
```

### YAML Recipes

**Basic YAML Visitor:**

```java
public class YourYamlRecipe extends Recipe {

    @Override
    public TreeVisitor<?, ExecutionContext> getVisitor() {
        return new YamlIsoVisitor<ExecutionContext>() {
            @Override
            public Yaml.Mapping.Entry visitMappingEntry(Yaml.Mapping.Entry entry, ExecutionContext ctx) {
                entry = super.visitMappingEntry(entry, ctx);

                // Match key
                if ("targetKey".equals(entry.getKey().getValue())) {
                    // Safe value access
                    String value = entry.getValue() instanceof Yaml.Scalar ?
                        ((Yaml.Scalar) entry.getValue()).getValue() : null;

                    if ("oldValue".equals(value)) {
                        return entry.withValue(
                            ((Yaml.Scalar) entry.getValue()).withValue("newValue")
                        );
                    }
                }

                return entry;
            }
        };
    }
}
```

**JsonPath Matching:**

```java
public class GitHubActionsRecipe extends Recipe {

    @Override
    public TreeVisitor<?, ExecutionContext> getVisitor() {
        return new YamlIsoVisitor<ExecutionContext>() {

            private final JsonPathMatcher matcher =
                new JsonPathMatcher("$.jobs.*.steps[*].uses");

            @Override
            public Yaml.Scalar visitScalar(Yaml.Scalar scalar, ExecutionContext ctx) {
                scalar = super.visitScalar(scalar, ctx);

                if (matcher.matches(getCursor())) {
                    String value = scalar.getValue();
                    if (value != null && value.startsWith("actions/checkout@v2")) {
                        return scalar.withValue(value.replace("@v2", "@v4"));
                    }
                }

                return scalar;
            }
        };
    }
}
```

**Common JsonPath Patterns:**

See `./references/jsonpath-patterns.md` for comprehensive patterns including:
- GitHub Actions: `$.jobs.*.steps[*].uses`, `$.on.push.branches`
- Kubernetes: `$.spec.template.spec.containers[*].image`, `$.metadata.labels`
- Generic YAML: `$.databases.*.connection.host`, `$[?(@.enabled == true)]`

### ScanningRecipe Pattern

Use when you need to see all files before making changes, generate new files, or share data across files.

```java
@Value
@EqualsAndHashCode(callSuper = false)
public class YourScanningRecipe extends ScanningRecipe<YourAccumulator> {

    public static class YourAccumulator {
        Map<SourceFile, Boolean> fileData = new HashMap<>();
    }

    @Override
    public YourAccumulator getInitialValue(ExecutionContext ctx) {
        return new YourAccumulator();
    }

    @Override
    public TreeVisitor<?, ExecutionContext> getScanner(YourAccumulator acc) {
        return new TreeVisitor<Tree, ExecutionContext>() {
            @Override
            public Tree visit(@Nullable Tree tree, ExecutionContext ctx) {
                // Collect data into accumulator
                return tree;
            }
        };
    }

    @Override
    public TreeVisitor<?, ExecutionContext> getVisitor(YourAccumulator acc) {
        return new TreeVisitor<Tree, ExecutionContext>() {
            @Override
            public Tree visit(@Nullable Tree tree, ExecutionContext ctx) {
                // Use data from accumulator to make changes
                return tree;
            }
        };
    }
}
```

For complete example, see `./examples/example-scanning-recipe.java`.

## Testing Recipes

### Test Structure

Use the RewriteTest interface for all recipe tests.

```java
class YourRecipeTest implements RewriteTest {

    @Override
    public void defaults(RecipeSpec spec) {
        spec.recipe(new YourRecipe("parameter-value"));
    }

    @Test
    void makesExpectedChange() {
        rewriteRun(
            //language=java
            java(
                // Before
                """
                  package com.example;
                  class Before { }
                  """,
                // After
                """
                  package com.example;
                  class After { }
                  """
            )
        );
    }

    @Test
    void doesNotChangeWhenNotNeeded() {
        rewriteRun(
            //language=java
            java(
                """
                  package com.example;
                  class AlreadyCorrect { }
                  """
                // No second argument = no change expected
            )
        );
    }
}
```

### Testing Best Practices

- **Test both changes AND no-changes cases** - Ensure recipe doesn't modify unrelated code
- **Test edge cases** - Nulls, empty files, missing elements, multi-document YAML
- **Test harness runs multiple cycles** - Ensures idempotence automatically
- **Add `//language=XXX` comments** - Helps IDE syntax highlight test code
- **Use text blocks properly** - End `"""` delimiter one indent to right of open delimiter

### YAML-Specific Testing

**Multi-document YAML:**

```java
@Test
void handlesMultiDocumentYaml() {
    rewriteRun(
        //language=yaml
        yaml(
            """
              ---
              first: document
              ---
              second: document
              """,
            """
              ---
              first: updated
              ---
              second: updated
              """
        )
    );
}
```

**Null value handling:**

```java
@Test
void handlesNullValues() {
    rewriteRun(
        //language=yaml
        yaml(
            """
              key: null
              another:
              """
            // Should not crash or change
        )
    );
}
```

**Comment preservation:**

```java
@Test
void preservesComments() {
    rewriteRun(
        //language=yaml
        yaml(
            """
              # Important comment
              key: oldValue
              """,
            """
              # Important comment
              key: newValue
              """
        )
    );
}
```

For more testing patterns, see `./references/testing-patterns.md`.

## Advanced Features

### OpenRewrite Traits

Traits provide semantic abstractions over LST elements, wrapping them with domain-specific logic.

**When to use traits:**
- You need reusable matching logic across multiple recipes
- You want to separate "what to find" from "what to do"
- You're working with complex LST patterns repeatedly

**Basic trait structure:**

```java
@Value
public class YourTrait implements Trait<J.ClassDeclaration> {
    Cursor cursor;

    // Domain-specific accessor
    public String getClassName() {
        return getTree().getSimpleName();
    }

    // Nested Matcher class
    public static class Matcher extends SimpleTraitMatcher<J.ClassDeclaration> {
        @Override
        protected @Nullable YourTrait test(Cursor cursor) {
            J.ClassDeclaration cd = cursor.getValue();
            // Custom matching logic
            if (matchesCondition(cd)) {
                return new YourTrait(cursor);
            }
            return null;
        }
    }
}
```

**Using traits in recipes:**

```java
@Override
public TreeVisitor<?, ExecutionContext> getVisitor() {
    return new YourTrait.Matcher().asVisitor((trait, ctx) -> {
        String className = trait.getClassName();
        // Use semantic API instead of raw LST navigation
        return trait.getTree();
    });
}
```

**IMPORTANT:** Never use deprecated `Traits` utility classes. Always instantiate matchers directly:

```java
// ❌ Old (deprecated):
Traits.literal()

// ✅ New (preferred):
new Literal.Matcher()
```

For complete trait implementation guide, see `./references/trait-implementation-guide.md`.

### Preconditions (Performance Optimization)

Preconditions filter files before running the recipe, improving performance.

**Common preconditions:**

```java
// Only run on files using specific type
new UsesType<>("com.example.Type", true)

// Only run on files with specific method
new UsesMethod<>("com.example.Type methodName(..)")

// Only run on specific Java version
new UsesJavaVersion<>(17)

// Only run on YAML files
new FindSourceFiles("**/*.yml", "**/*.yaml")
```

**Combining preconditions:**

```java
@Override
public TreeVisitor<?, ExecutionContext> getVisitor() {
    return Preconditions.check(
        Preconditions.and(
            new UsesType<>("com.example.Type", true),
            new UsesJavaVersion<>(11)
        ),
        new YourVisitor()
    );
}
```

### JavaTemplate Deep Dive

JavaTemplate compiles code snippets once and applies them to LST elements.

**When to use:**
- Adding new code structures (methods, statements, expressions)
- Complex code generation that's tedious with LST methods

**When NOT to use:**
- Modifying existing elements (use `.withX()` methods)
- Simple changes (reordering, renaming, removing)

**Template syntax:**

```java
// Untyped substitution (strings)
JavaTemplate.builder("System.out.println(#{})")
    .build();

// Typed substitution (LST elements)
JavaTemplate.builder("return #{any(java.lang.String)}")
    .build();

// With imports
JavaTemplate.builder("List<String> list = new ArrayList<>()")
    .imports("java.util.List", "java.util.ArrayList")
    .build();

// With classpath
JavaTemplate.builder("@Deprecated(since = \"2.0\")")
    .javaParser(JavaParser.fromJavaVersion().classpath("library-name"))
    .build();

// Context-sensitive (references local scope)
JavaTemplate.builder("localVariable.method()")
    .contextSensitive()
    .build();
```

**Applying templates:**

```java
// Apply to statement position
method.withBody(
    template.apply(
        new Cursor(getCursor(), method.getBody()),
        method.getBody().getCoordinates().lastStatement(),
        args
    )
);
```

**Tips:**
- Context-free templates (default) are faster
- Use `.contextSensitive()` only when referencing local variables/methods
- Declare all imports explicitly
- Escape special characters in template strings

### State Management

**Within visitor (intra-visitor state):**

```java
// Store state
getCursor().putMessage("key", value);

// Retrieve state from cursor hierarchy
Object value = getCursor().getNearestMessage("key");
```

**Between visitors (ScanningRecipe):**

Use accumulator pattern - see ScanningRecipe section above.

**Never:**
- Use ExecutionContext for visitor state
- Mutate recipe instance fields
- Use static variables

### Multi-Module Projects

Track data per-project, not globally:

```java
public static class Accumulator {
    // ✅ Per-project tracking
    Map<SourceFile, Boolean> fileData = new HashMap<>();

    // ❌ Don't assume single project
    // boolean globalFlag;
}
```

## Troubleshooting

Common issues and solutions when developing recipes.

### Recipe Not Running on Expected Files

**Symptoms:** Recipe doesn't execute on files you expect to change

**Solutions:**
1. Check preconditions - might be too restrictive
2. Verify file matches visitor type (JavaIsoVisitor for Java, YamlIsoVisitor for YAML)
3. Add debug logging to visitor methods
4. Ensure the file contains the patterns you're looking for
5. For YAML: Check file extension (`.yml` vs `.yaml`)

### JavaTemplate Parse Errors

**Symptoms:** Template fails to compile or apply

**Solutions:**
1. Check imports are declared with `.imports()`
2. Verify classpath includes all referenced types with `.javaParser()`
3. Use `.contextSensitive()` if referencing local scope
4. Escape special characters in template strings
5. Ensure placeholder syntax is correct:
   - `#{}` for strings
   - `#{any(Type)}` for LST elements

### Tests Passing But Recipe Doesn't Work in Real Code

**Symptoms:** RewriteTest passes but recipe fails on actual projects

**Solutions:**
1. Add more realistic test cases with complex code
2. Test with external dependencies via parser configuration
3. Verify preconditions match real-world usage
4. Check for edge cases not covered in tests
5. Test with different Java versions if version-specific

### Recipe Makes Changes But Not Idempotent

**Symptoms:** Running recipe multiple times produces different results each time

**Solutions:**
1. Ensure all checks use referential equality (return unchanged LST if no change needed)
2. Verify visitor doesn't accumulate state between invocations
3. Check that `getVisitor()` returns a NEW instance each time
4. Ensure recipe class is immutable (uses `@Value`)
5. Test with `rewriteRun()` which automatically runs multiple cycles

### Type Information Not Available

**Symptoms:** `TypeUtils.isOfClassType()` returns false when it should be true

**Solutions:**
1. Ensure test configures classpath with required dependencies
2. Check that imports are present in the source file
3. Verify the type binding resolved correctly (check for `null` types)
4. Add explicit type attribution if working with dynamic code

### YAML Recipe Not Matching Expected Elements

**Symptoms:** YAML recipe doesn't find or transform expected YAML elements

**Solutions:**
1. Check JsonPath pattern is correct - test with online JsonPath evaluator
2. Verify you're using correct LST visitor method (visitScalar vs visitMappingEntry)
3. Handle null values safely - YAML allows `key: null` and `key:`
4. Check for multi-document YAML (starts with `---`)
5. Verify you're calling `super.visitX()` to traverse tree

### YAML Comments or Formatting Not Preserved

**Symptoms:** Recipe changes YAML but loses comments or formatting

**Solutions:**
1. Never create new LST elements - always use `.withX()` methods
2. Use `ListUtils` for list operations, never mutate directly
3. Return original element if no change needed (identity check)
4. Check you're not replacing entire nodes unnecessarily

For more troubleshooting guidance, see `./references/troubleshooting-guide.md`.

## Critical Best Practices

### Do No Harm
- If unsure whether a change is safe, DON'T make it
- Make minimal, least invasive changes
- Respect existing formatting and comments
- Return unchanged LST if no change needed

### Immutability & Idempotence
- Recipes must be immutable (no mutable state)
- Same input → same output, always
- Use `@Value` and `@EqualsAndHashCode(callSuper = false)`
- `getVisitor()` must return NEW instance each time

### Never Mutate LSTs
```java
// WRONG
method.getArguments().remove(0);

// CORRECT
method.withArguments(ListUtils.map(method.getArguments(), (i, arg) ->
    i == 0 ? null : arg
));
```

### Naming Conventions
- Display names: Sentence case, code in backticks, end with period
- Example: "Change type from `OldType` to `NewType`."
- Recipe names: `com.yourorg.VerbNoun` (e.g., `com.yourorg.ChangePackage`)

## Accessing Bundled Resources

This skill uses progressive disclosure to minimize token usage. Load resources on demand:

### Templates (for boilerplate code)
- `templates/template-imperative-recipe.java` - Complete recipe class structure
- `templates/template-declarative-recipe.yml` - YAML recipe format
- `templates/template-refaster-template.java` - Refaster template structure
- `templates/template-recipe-test.java` - Test class using RewriteTest
- `templates/license-header.txt` - Standard license header

### Examples (for working patterns)
- `examples/example-say-hello-recipe.java` - Simple recipe with JavaTemplate
- `examples/example-scanning-recipe.java` - Multi-file analysis pattern
- `examples/example-yaml-github-actions.java` - YAML domain example
- `examples/example-declarative-migration.yml` - Framework migration

### References (for detailed guidance)
- `references/java-lst-reference.md` - Java LST structure and hierarchy
- `references/yaml-lst-reference.md` - YAML LST structure and hierarchy
- `references/jsonpath-patterns.md` - Domain-specific JsonPath patterns
- `references/trait-implementation-guide.md` - Advanced trait patterns
- `references/checklist-recipe-development.md` - 200+ validation items
- `references/common-patterns.md` - Copy-paste code snippets
- `references/testing-patterns.md` - Test patterns and edge cases
- `references/troubleshooting-guide.md` - Issue diagnosis and solutions

### When to Load Resources

| Resource Type | Typical Size | When to Load |
|--------------|-------------|--------------|
| SKILL.md | ~3,500 tokens | Always (auto) |
| Templates | ~500 tokens each | On demand (Read tool) |
| Examples | ~1,000 tokens each | On demand (Read tool) |
| References | ~1,500-3,000 tokens each | On demand (Read tool) |

**Best practice:** Only read templates/examples when actively working on implementation. The SKILL.md content provides sufficient guidance for planning and decision-making.

## Quick Reference

### Key Classes

| Class | Purpose |
|-------|---------|
| `Recipe` | Base class for all recipes |
| `JavaIsoVisitor<ExecutionContext>` | Most common Java visitor type |
| `YamlIsoVisitor<ExecutionContext>` | Most common YAML visitor type |
| `JavaTemplate` | Generate Java code snippets |
| `RewriteTest` | Testing interface |
| `ScanningRecipe<T>` | Multi-file analysis pattern |
| `JsonPathMatcher` | Match YAML/JSON paths |

### Key Methods

| Method | Purpose |
|--------|---------|
| `getVisitor()` | Returns visitor instance (must be NEW) |
| `super.visitX()` | Traverse subtree |
| `.withX()` | Create modified LST copy (immutable) |
| `ListUtils.map()` | Transform lists without mutation |
| `doAfterVisit()` | Chain additional visitors |
| `maybeAddImport()` | Add import if not present |
| `maybeRemoveImport()` | Remove import if unused |
| `getCursor().putMessage()` | Store intra-visitor state |

### Common Patterns

For quick reference on frequently used patterns, see:
- `references/common-patterns.md` - Import management, visitor chaining, type checking
- `references/jsonpath-patterns.md` - GitHub Actions, Kubernetes, CI/CD patterns

## Automation Scripts

Use helper scripts for common tasks:

- **`./scripts/init_recipe.py <RecipeName>`** - Generate recipe boilerplate (class, test file, optional YAML)
- **`./scripts/validate_recipe.py [path]`** - Validate recipe structure, naming, Java compatibility
- **`./scripts/add_license_header.sh [file]`** - Add license headers from `gradle/licenseHeader.txt`

## Token Budget Awareness

This skill is optimized for token efficiency:

- **SKILL.md**: ~3,500 tokens (loaded when skill activates)
- **Templates**: Load only when creating new recipes
- **Examples**: Load only when learning specific patterns
- **References**: Load only when you need deep dives or validation

**Strategy:** Start with SKILL.md guidance. Load templates for boilerplate. Load references for troubleshooting or advanced features.

## Remember

- **Always start with tests (RED)**
- **Try declarative before Refaster before imperative**
- **Apply idioms during REFACTOR, not GREEN**
- **Document with markdown for clarity**
- **Validate production-readiness before completion**
- **Preserve formatting and comments**
- **Do no harm - when in doubt, don't change**
