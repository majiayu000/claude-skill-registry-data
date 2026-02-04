---
name: catz-challenge-evaluator
description: Evaluates Catz Android coding challenge submissions against SWORD Health requirements. Use when reviewing or assessing this coding challenge. Produces a structured markdown report with seniority level assessment (Junior/Mid/Senior/Staff) and confidence rating, covering requirements compliance, architecture, code quality, testing, and documentation.
---

# Catz Challenge Evaluator

Evaluate the Catz Android coding challenge submission and generate a comprehensive assessment report.

## Evaluation Workflow

Execute each phase sequentially, gathering evidence before making assessments.

### Phase 1: Requirements Checklist

Read `references/requirements.md` for the full requirements list.

**Functional Requirements** - Verify each:
1. List screen with cat image + breed name
2. Search bar filtering by breed name
3. Favorite button on breeds screen
4. Favorites screen with average lifespan
5. Detail screen (name, origin, temperament, description, favorite toggle)
6. Jetpack Navigation Component usage
7. Click navigation to detail view

**Technical Requirements** - Verify each:
- MVVM architecture (ViewModels, state management)
- Jetpack Compose (Material 3)
- Unit test coverage
- Offline functionality (Room database)

### Phase 2: Architecture Assessment

Examine module structure and dependencies:

```
Key files to examine:
- settings.gradle.kts (module structure)
- */build.gradle.kts (dependencies per module)
- **/di/*.kt (dependency injection setup)
- **/repository/*.kt (data layer patterns)
- **/viewmodel/*.kt (presentation patterns)
```

Evaluate:
- Module separation and boundaries
- Dependency direction (domain → data, not reverse)
- Repository pattern implementation
- Use case abstraction (if present)
- DI framework usage

### Phase 3: Code Quality Review

Examine implementation patterns:

```
Key areas:
- Error handling (Result types, try-catch usage)
- Null safety (nullable types, safe calls)
- Coroutine usage (scopes, dispatchers, cancellation)
- State management (StateFlow, immutability)
- Kotlin idioms (data classes, sealed classes, extension functions)
```

Check for:
- Consistent naming conventions
- Code organization within files
- Appropriate visibility modifiers
- Avoidance of code duplication

### Phase 4: Testing Analysis

Examine test coverage and quality:

```
Test locations:
- */src/test/ (unit tests)
- */src/androidTest/ (instrumented tests)
- */src/screenshotTest/ (screenshot tests)
```

Evaluate:
- Test coverage (repository, viewmodel, mapper, UI)
- Test quality (meaningful assertions, edge cases)
- Mocking strategy (appropriate use of mocks)
- Test organization and naming

### Phase 5: Bonus Features Check

| Bonus | What to look for |
|-------|------------------|
| Error handling | Result sealed class, graceful degradation, user feedback |
| Pagination | Paging 3 library or manual implementation |
| Modular design | 3+ modules with clear responsibilities |
| Integration/E2E | Instrumented tests, Espresso, or Compose UI tests on device |

### Phase 6: README Assessment

Examine `README.md` for:
- Architecture explanation
- Design decisions rationale
- Setup instructions
- Known limitations acknowledged

### Phase 7: Seniority Determination

Based on evidence gathered, determine seniority level:

| Level | Indicators |
|-------|------------|
| **Junior** | Basic MVVM, minimal tests, single module, copy-paste patterns, limited error handling |
| **Mid-Level** | Clean MVVM, decent test coverage, consistent style, basic error handling, 2+ modules |
| **Senior** | Multi-module Clean Architecture, comprehensive tests, Result types, offline-first, proper DI, thoughtful README |
| **Staff/Principal** | Exceptional patterns, beyond requirements, novel solutions, excellent documentation, teaching-quality code |

**Confidence Factors:**
- High (85%+): Consistent evidence across all dimensions
- Medium (60-85%): Mixed signals, some areas unclear
- Low (<60%): Limited evidence, significant gaps

### Phase 8: Interview Questions

Generate targeted interview questions based on findings. Include:

**Architecture Questions** - Probe understanding of design decisions:
- Why this module structure? What are the trade-offs?
- Why separate tables for favorites vs. a column?
- How would you change the architecture for X requirement?

**Technical Deep-Dives** - Validate implementation knowledge:
- Walk me through the data flow for [specific feature]
- How does [specific mechanism] work under the hood?
- What happens when [edge case scenario]?

**Pressure Points** - Challenge decisions and gaps:
- Questions about missing features (pagination, E2E tests)
- Alternative approaches they considered
- How they'd handle production issues

**Growth Questions** - Assess learning and scalability thinking:
- What would you do differently?
- How would this scale to 10x data?
- What's the weakest part of this codebase?

### Phase 9: Report Generation

Generate the report using this template:

---

## Report Template

```markdown
# Catz Challenge Evaluation Report

**Date:** [Current Date]
**Repository:** [Repository URL if available]

---

## Verdict

**Seniority Level: [Junior/Mid-Level/Senior/Staff]**
**Confidence: [High/Medium/Low] ([percentage]%)**

[2-3 sentence summary of overall assessment]

---

## Requirements Compliance

### Functional Requirements (7 items)

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | List screen (image + name) | [Pass/Fail] | [File path or note] |
| 2 | Search bar filtering | [Pass/Fail] | [Implementation details] |
| 3 | Favorite button | [Pass/Fail] | [File path or note] |
| 4 | Favorites screen + avg lifespan | [Pass/Fail] | [Implementation details] |
| 5 | Detail screen (all fields + favorite) | [Pass/Fail] | [File path or note] |
| 6 | Jetpack Navigation | [Pass/Fail] | [Navigation setup location] |
| 7 | Click → detail navigation | [Pass/Fail] | [Implementation details] |

**Functional Score: [X]/7**

### Technical Requirements (4 items)

| Requirement | Status | Evidence |
|-------------|--------|----------|
| MVVM architecture | [Pass/Fail] | [ViewModel locations, state management approach] |
| Jetpack Compose | [Pass/Fail] | [Compose usage, Material version] |
| Unit test coverage | [Pass/Fail] | [Test locations, coverage areas] |
| Offline functionality | [Pass/Fail] | [Room setup, caching strategy] |

**Technical Score: [X]/4**

---

## Architecture Analysis

### Module Structure
[Describe the module organization]

### Dependency Graph
[Describe how modules depend on each other]

### Strengths
- [Strength 1]
- [Strength 2]

### Areas for Improvement
- [Improvement 1]
- [Improvement 2]

---

## Code Quality Assessment

### Kotlin Usage
[Assess idiomatic Kotlin usage]

### Error Handling
[Describe error handling approach]

### State Management
[Describe state management patterns]

### Rating: [Excellent/Good/Adequate/Needs Improvement]

---

## Testing Coverage

### Unit Tests
[Describe unit test coverage]

### UI Tests
[Describe UI/screenshot tests if present]

### Integration/E2E Tests
[Describe or note absence]

### Rating: [Excellent/Good/Adequate/Needs Improvement]

---

## README Quality

### Content Assessment
[Evaluate README completeness]

### Rating: [Excellent/Good/Adequate/Needs Improvement]

---

## Bonus Points

| Bonus | Status | Notes |
|-------|--------|-------|
| Error handling | [Achieved/Partial/Missing] | [Details] |
| Pagination | [Achieved/Partial/Missing] | [Details] |
| Modular design | [Achieved/Partial/Missing] | [Details] |
| Integration/E2E tests | [Achieved/Partial/Missing] | [Details] |

**Bonus Score: [X]/4**

---

## Summary

### Key Strengths
1. [Top strength]
2. [Second strength]
3. [Third strength]

### Areas for Growth
1. [Primary improvement area]
2. [Secondary improvement area]

### Final Assessment
[1-2 paragraph synthesis of the evaluation, justifying the seniority level and confidence rating]

---

## Interview Questions

### Architecture Questions
[2-3 questions probing architectural understanding]

### Technical Deep-Dives
[2-3 questions requiring detailed implementation knowledge]

### Pressure Points
[2-3 challenging questions about gaps or controversial decisions]

### Growth Questions
[2-3 questions about improvements and scaling]

---

## Interview Flow Guide

### 15-Minute Screen
[3 essential questions]

### 30-Minute Technical
[5-6 questions with flow]

### 45-Minute Deep Dive
[8-10 questions covering all areas]

---

## AI-Generated Code Detection

### Code Ownership Probes
[Questions requiring personal experience and specific reasoning]

### Code Navigation Tests
[Questions about method names, file locations, constants]

---

## Scoring Rubric

| Score | Description |
|-------|-------------|
| 5 | Exceptional - exceeds expectations |
| 4 | Strong - fully meets expectations |
| 3 | Adequate - meets basic expectations |
| 2 | Weak - below expectations |
| 1 | Poor - does not meet |
| 0 | Red flag - disqualifying |

---

## Quick Reference Card

[Printable summary with verdict, key probes, gaps, and thresholds]
```

---

## Key Files Reference

For quick evaluation, these are the critical files in this codebase:

**Architecture:**
- `settings.gradle.kts` - Module definitions
- `app/build.gradle.kts` - App dependencies
- `CLAUDE.md` - Architecture documentation

**Data Layer:**
- `cat_breeds_data/src/main/java/.../data/repository/BreedRepositoryImpl.kt`
- `cat_breeds_data/src/main/java/.../data/local/CatBreedsDatabase.kt`
- `cat_breeds_data/src/main/java/.../data/api/CatApiService.kt`

**Domain Layer:**
- `cat_breeds_api/src/main/java/.../domain/model/Breed.kt`
- `cat_breeds_api/src/main/java/.../domain/repository/BreedRepository.kt`
- `cat_breeds_api/src/main/java/.../domain/result/Result.kt`

**Presentation Layer:**
- `cat_breeds/src/main/java/.../presentation/viewmodel/*.kt`
- `cat_breeds/src/main/java/.../presentation/ui/*.kt`
- `cat_breeds/src/main/java/.../presentation/navigation/CatBreedsRoute.kt`

**Testing:**
- `cat_breeds_data/src/test/` - Data layer tests
- `cat_breeds/src/test/` - UI and use case tests
- `cat_breeds/src/screenshotTest/` - Screenshot tests

**Documentation:**
- `README.md` - Project documentation
