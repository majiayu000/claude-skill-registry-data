---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
tags: [meta, workflow, planning]
applies-to: [antigravity, cursor, copilot, gemini]
level: project
---

## Overview
Write comprehensive implementation plans assuming the engineer has zero context for the codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. Frequent commits.

Assume they are a skilled developer, but know almost nothing about the toolset or problem domain.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## Scope Check
If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure
Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure — but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

### Flutter File Structure Reference
A typical Flutter feature touches these files:

```
lib/features/<feature>/
├── data/
│   ├── datasources/<feature>_remote_data_source.dart
│   ├── models/<feature>_model.dart          (freezed + json_serializable)
│   └── repositories/<feature>_repository_impl.dart
├── domain/
│   ├── entities/<feature>_entity.dart
│   └── repositories/<feature>_repository.dart (abstract)
├── presentation/
│   ├── cubit/<feature>_cubit.dart
│   ├── cubit/<feature>_state.dart           (freezed with ApiStatus)
│   └── pages/<feature>_page.dart
└── <feature>_route_provider.dart             (GoRouter route definition)
```

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Bite-Sized Task Granularity
**Each step is one action (2-5 minutes):**
- "Write the data model with freezed annotations" — step
- "Run build_runner to generate code" — step
- "Create the Retrofit API interface" — step
- "Implement the repository" — step
- "Create the Cubit with states" — step
- "Build the UI page" — step
- "Register dependencies in DI" — step
- "Run `flutter test` and verify" — step
- "Commit" — step

## Plan Document Header
**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Use the executing-plans skill to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure
````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.dart`
- Modify: `exact/path/to/existing.dart`
- Test: `test/exact/path/to/file_test.dart`

- [ ] **Step 1: Create the data model**

```dart
@freezed
class FeatureModel with _$FeatureModel {
  const factory FeatureModel({
    required String id,
    required String name,
  }) = _FeatureModel;

  factory FeatureModel.fromJson(Map<String, dynamic> json) =>
      _$FeatureModelFromJson(json);
}
```

- [ ] **Step 2: Run code generation**

Run: `dart run build_runner build --delete-conflicting-outputs`
Expected: Generated `.freezed.dart` and `.g.dart` files

- [ ] **Step 3: Create the API interface**

```dart
@RestApi()
abstract class FeatureApi {
  factory FeatureApi(Dio dio) = _FeatureApi;

  @GET('/api/v1/features')
  Future<List<FeatureModel>> getFeatures();
}
```

- [ ] **Step 4: Run code generation again**

Run: `dart run build_runner build --delete-conflicting-outputs`
Expected: Generated Retrofit implementation

- [ ] **Step 5: Commit**

```bash
git add .
git commit -m "feat: add Feature data layer (model + API)"
```
````

## No Placeholders
Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Flutter-Specific Reminders
- Always include `build_runner` steps after creating/modifying `freezed` or `json_serializable` models
- Include DI registration steps (`@injectable`, `@lazySingleton`) when creating new services/repositories
- Include route registration when adding new pages
- Include `flutter analyze` as a verification step
- Remember to add asset references if new assets are introduced

## Remember
- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, frequent commits

## Self-Review
After writing the complete plan, look at the spec with fresh eyes and check the plan against it:

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `getWallet()` in Task 3 but `fetchWallet()` in Task 7 is a bug.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

## Execution Handoff
After saving the plan, offer execution:

**"Plan complete and saved to `docs/plans/<filename>.md`. Ready to execute using the executing-plans skill. Shall I proceed?"**
