---
name: uw-code-review
description: Pre-commit code quality review for Unity C# code. Checks against Rules, CODING_STANDARDS.md, NAMING_CONVENTIONS.md, and GDD Gherkin test coverage. Use when code has been written and tests are passing but before committing. Runs automatically at Step 8.5 of /uw-cmd-implement-feature. Triggers on "review this code", "check my implementation", "pre-commit review", "code review", "check before commit", "is this ready to commit", "review my changes", or any request to validate code quality before committing.
---

# Code Review

Pre-commit quality gate. Read the target files, then run this checklist. Output one structured report per review. Fix all issues before committing.

## Before You Start

1. Read `docs/CODING_STANDARDS.md` for formatting, class structure, serialization, null safety, and async rules.
2. Read `docs/NAMING_CONVENTIONS.md` for naming rules (private fields, properties, files, asmdefs).
3. Read `docs/GDD.md` for Gherkin scenarios — every scenario should have a corresponding test.
4. Read the files being reviewed in full before assessing.

## Checklist

### 1. Rules Compliance
- [ ] All Inspector fields use `[SerializeField] private` — no `public` fields on MonoBehaviours
- [ ] All component references cached in `Awake()` or `Start()` — never in `Update/FixedUpdate/LateUpdate`
- [ ] `GameDebug` used instead of `Debug.Log` / `Debug.LogError` / `Debug.LogWarning`
- [ ] New Input System only — no `Input.GetKey*` / `Input.GetAxis*`
- [ ] `TryGetComponent<T>()` preferred over `GetComponent<T>()` where component may be absent
- [ ] No Unity API calls from background threads
- [ ] No `.meta` file modifications

### 2. Naming Conventions
- [ ] Private fields: `_camelCase`
- [ ] Public properties & methods: `PascalCase`
- [ ] Parameters & local variables: `camelCase`
- [ ] Booleans: `is/has/can/should` prefix (e.g. `_isGrounded`, `CanJump`)
- [ ] Events: `On` prefix (e.g. `OnDeath`)
- [ ] Static fields: `s_camelCase`
- [ ] Class name matches file name

### 3. Code Quality
- [ ] No magic numbers or hardcoded strings — use constants, ScriptableObjects, or serialized fields
- [ ] No `FindObjectOfType<T>()` or `GameObject.Find()` (except in editor-only code)
- [ ] No cross-assembly references that violate the TDD's asmdef dependency graph
- [ ] K&R braces (opening brace on same line)
- [ ] 4-space indentation (no tabs)

### 4. Performance
- [ ] No `new` allocations inside `Update/FixedUpdate/LateUpdate` (no GC pressure in hot paths)
- [ ] Particles are pooled or have Stop Action set to `Destroy` with pool backing
- [ ] DOTween/PrimeTween tweens are killed in `OnDestroy` or `OnDisable`
- [ ] No `string` concatenation in hot paths — use `GameDebug` with conditional compilation

### 5. Test Coverage
- [ ] Every GDD Gherkin `Given/When/Then` scenario for this feature has a corresponding NUnit test
- [ ] EditMode tests for pure logic; PlayMode tests for MonoBehaviour lifecycle
- [ ] All tests currently passing

### 6. Game Feel
- [ ] If "later" was chosen in `/uw-cmd-implement-feature` Step 3: `// TODO(gamefeel): [feature] — pending` comment exists in the main script
- [ ] If "later" was chosen: a pending row exists in `docs/GFD.md` Feedback Matrix
- [ ] If "now" was chosen: Rule of Three satisfied (visual + audio + kinesthetic minimum)

## Output Format

```
## Code Review — {FeatureName}

### Rules          [Pass | Issues]
### Naming         [Pass | Issues]
### Code Quality   [Pass | Issues]
### Performance    [Pass | Issues]
### Test Coverage  [X/Y scenarios | Missing]
### Game Feel      [Integrated | TODO filed | Missing]

Issues to fix before commit:
- [list each issue with file and line, or "None"]
```

Do not commit until **Issues to fix** is "None".

## After Review

- **Fix issues:** Address all flagged items, then re-run this review.
- **Debug failures:** Use `uw-unity-debugging` for systematic diagnosis of any issues found.
- **Missing tests:** Use `uw-unity-test-runner` to generate tests for uncovered Gherkin scenarios.
- **Missing game feel:** Use `uw-game-feel-integrator` if Rule of Three is not satisfied and "now" was chosen.
