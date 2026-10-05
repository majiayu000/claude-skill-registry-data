---
name: java-cleanup
description: Remove dead code, update deprecated APIs, apply modern Java patterns, and clean up Java codebases. Use when cleaning up Java projects, removing unused.
---

# Java Code Cleanup

Systematically identify and remove dead code, update deprecated APIs, and apply modern Java patterns to maintain a clean, maintainable codebase.

## When to Use This Skill

Use this skill when you need to:

- Remove unused imports and dead code
- Update deprecated API usage
- Apply modern Java features (8+)
- Fix Checkstyle/PMD issues
- Clean up before code review

**Trigger phrases**: "cleanup Java", "remove dead code Java", "modernize Java", "fix Checkstyle", "Java refactor"

## What This Skill Does

### Cleanup Areas

1. **Dead Code Removal**
   - Unused imports
   - Unused private methods
   - Unreachable code
   - Redundant code

2. **Style Compliance**
   - Checkstyle rules
   - PMD/SpotBugs
   - Naming conventions

3. **Modernization**
   - Streams API
   - Optional
   - var keyword
   - Records (Java 14+)

## Instructions

### Step 1: Run Analysis Tools

```bash
# Run Checkstyle
mvn checkstyle:check

# Run PMD
mvn pmd:check

# Run SpotBugs
mvn spotbugs:check
```

### Step 2: Modernize Patterns

```java
// Traditional loop → Stream
// Before
List<String> names = new ArrayList<>();
for (User user : users) {
    if (user.isActive()) {
        names.add(user.getName());
    }
}
// After
List<String> names = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .collect(Collectors.toList());

// Null checks → Optional
// Before
String name = user != null ? user.getName() : "Unknown";
// After
String name = Optional.ofNullable(user)
    .map(User::getName)
    .orElse("Unknown");

// Anonymous class → Lambda
// Before
button.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        handleClick(e);
    }
});
// After
button.addActionListener(e -> handleClick(e));

// Data class → Record (Java 14+)
// Before
public class User {
    private final String name;
    private final String email;
    // constructor, getters, equals, hashCode, toString
}
// After
public record User(String name, String email) {}
```

## Tools

- **Checkstyle**: Style checking
- **PMD**: Static analysis
- **SpotBugs**: Bug detection
- **IntelliJ Inspections**: IDE analysis

## Quality Checklist

- [ ] Unused imports removed
- [ ] Deprecated APIs updated
- [ ] Modern patterns applied
- [ ] Checkstyle passes
- [ ] Tests still pass

## Related Skills

- `code-review-quality` - Code quality assessment

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates code_cleanup/java_cleanup.md


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
