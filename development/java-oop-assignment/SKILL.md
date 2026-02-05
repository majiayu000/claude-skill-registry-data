---
name: java-oop-assignment
description: Completes Java OOP university assignments from PDF specifications with minimal implementation. Use when user provides a PDF assignment file or mentions completing a Java/FOP/OOP homework exercise. Focuses on writing the least code necessary to satisfy requirements.
---

# Java OOP Assignment Solver

## Philosophy

**KISS + YAGNI**: Write the minimum code to pass. Less code = less to review = fewer bugs.

## Workflow

### Phase 1: Understand

1. **Read the PDF** - Extract all requirements, class diagrams, method signatures
2. **Explore codebase** - Find existing templates, enums, helper classes marked `@DoNotTouch`
3. **Identify tasks** - List each numbered requirement (H6.1, H6.2, etc.)

### Phase 2: Plan

Create a todo list with:
- Files to CREATE (interfaces, enums, classes)
- Files to MODIFY (implement methods, add `implements`)
- Implementation order (dependencies first)

### Phase 3: Implement

For each task:
1. **Interfaces/Enums first** - No dependencies
2. **Abstract classes** - Base functionality
3. **Concrete classes** - Extend/implement
4. **Modify existing** - Add interface implementations, fill in `TODO` methods
5. **Remove crash() calls** - Replace `crash("H6.X")` with actual implementation

### Phase 4: Verify

1. Build with Gradle: `./gradlew compileJava`
2. Run main if playground exists: `./gradlew run`
3. Check output matches PDF examples

## Implementation Rules

### Minimal Code

- No extra comments unless logic is unclear
- No extra validation unless specified
- No helper methods unless reused 3+ times
- Match exact signatures from PDF (visibility, types, names)

### PDF Reading Tips

- **Class diagrams**: Solid arrow = extends, dashed arrow = implements
- **"protected"**: Accessible to subclasses
- **"private final"**: Immutable, set in constructor
- **Mandatory requirements** in boxes: Must follow exactly

### Modern Java Idioms

Use the following for code conciseness, elegance and brevity.

- **Switch expressions** (`->`) - returns value, no break needed, fewer lines
- **Pattern matching instanceof** - cast + variable binding in one check
- **var** - type inference for locals, less redundancy
- **Ternary operator** - one-liner conditionals over if-else blocks
- **Math.min/max** - bounds checking without branching
- **Records** - immutable data classes in one line (if allowed)
- **Text blocks** (`"""`) - multi-line strings without concatenation

### Gradle Notes

- If build fails with version error, try: `JAVA_HOME=/path/to/jdk21 ./gradlew build`
- `@StudentImplementationRequired("H6.X")` marks methods to implement
- Remove `crash("H6.X")` calls when implementing

## Checklist

- [ ] All `TODO` comments addressed
- [ ] All `crash()` calls removed
- [ ] All interfaces/classes from diagram created
- [ ] Build succeeds
- [ ] Run output matches PDF examples (if playground provided)
