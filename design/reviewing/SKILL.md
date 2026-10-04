---
name: superpowers-sage:reviewing
description: >
  Convention audit and pre-PR code review for Sage/Acorn projects — checks PHP Blade JS CSS
  against Sage/Acorn/Tailwind v4 conventions; audits ACF Composer field patterns,
  Livewire component structure, Eloquent models, Acorn routes, Blade components;
  verifies design alignment; dispatches sage-reviewer agent; prepares code for PR merge.
  Invoke for: "review before PR", "run sage-reviewer", "convention audit",
  "/reviewing", "check my block for issues", "pre-merge review", "review this code".
  Skip when: you just need to read or understand a file — that is not a review session.
user-invocable: true
argument-hint: "[file path or scope]"
---

# Reviewing — Convention Audit + Design Alignment

Review code against Sage/Acorn conventions and verify alignment with design reference.

## Inputs

$ARGUMENTS

If no scope specified, review all changed files (`git diff` against base branch).

## Procedure

### 0) Determine scope

- If file path provided, review that file and related files
- If "all" or no argument, scan full project
- If active plan exists, focus on plan components

### 1) Convention checklist

#### Service Providers
- [ ] `ThemeServiceProvider` extends `Roots\Acorn\Sage\SageServiceProvider`; other feature providers extend `Illuminate\Support\ServiceProvider`
- [ ] `register()` only contains bindings (no hooks, no side effects)
- [ ] `boot()` contains hooks and initialization
- [ ] Dependencies injected via constructor

#### ACF Blocks & Fields
- [ ] Blocks created via `acf:block` generator
- [ ] `with()` returns only data the view needs
- [ ] `fields()` uses Builder API
- [ ] Block views use `$variable` not `get_field()`
- [ ] Reusable fields extracted to Partials

#### Blade Templates
- [ ] Composers for data injection, Components for reusable UI
- [ ] No business logic in Blade views
- [ ] Proper layout inheritance (`@extends`, `@section`, `@yield`)

#### Block Views
- [ ] **R-css-vars**: No `match($tone)` → Tailwind class strings; no `tone="*"` props driving color; no hardcoded color utilities on `h2`/`p`/`span` → G10 violation (CRITICAL)
- [ ] **R-component-reuse**: No inline `<x-eyebrow>` + `<h2>` when `<x-section-header>` exists; no raw `<a>` with button utilities when `<x-button>` exists → G9 violation
- [ ] **R-nl2br**: `nl2br()` only on `addTextarea()`/`addWysiwyg()` fields, not `addText()` → G11 violation
- [ ] **R-arbitrary-btn**: No `text-[*px]` or `tracking-[*px]` in block/component views → CRITICAL

#### Routes & Controllers
- [ ] Clean route declarations (no logic in closures)
- [ ] Thin controllers (delegate to services)
- [ ] Prefer Acorn Routes over `register_rest_route()`

#### Frontend
- [ ] Tailwind v4 CSS-first approach
- [ ] Assets referenced via `@vite()` or `Vite::asset()`
- [ ] Editor styles included

#### Hooks Placement
- [ ] `add_action`/`add_filter` in ServiceProvider `boot()`
- [ ] `setup.php` only for `after_setup_theme` essentials
- [ ] No hooks scattered in random files

#### Content Architecture
- [ ] Content that grows over time uses CPTs (not hardcoded arrays)
- [ ] CPTs defined in `config/poet.php` (not `register_post_type()`)
- [ ] Shared content uses Options Pages (not duplicated across blocks)

### 2) Design alignment (if plan exists)

If active plan has assets:
1. Read design reference from `assets/`
2. Compare implemented components with design
3. Flag visual drift

### 3) Report findings

```markdown
## Review: {scope}

### Critical (must fix)
- **{file}:{line}** — {issue}. See `{skill}`.

### Improvement (should fix)
- **{file}:{line}** — {issue}. See `{skill}`.

### Good Practices Found
- {positive observation}

### Design Alignment
- {component}: {MATCH/DRIFT} — {details}

### Summary
{X} critical, {Y} improvements, {Z} good practices.
```

### 4) Visual verification — all components

After sage-reviewer completes:

1. Glob for all spec files: `docs/plans/<active-plan>/assets/section-*-spec.md`
2. For each spec file found:
   a. Read the `### Verification Inputs` block — extract `url`, `selector`, `ref`
   b. Dispatch `visual-verifier` agent with:
      - `url`: from spec Verification Inputs
      - `selector`: from spec Verification Inputs
      - `spec`: this spec file path
      - `ref`: from spec Verification Inputs
   c. Collect report: MATCH | DRIFT | MISSING | FAIL_ARBITRARY_VALUES
3. Present consolidated report:
   - List all components with their verification status
   - If any DRIFT or FAIL: list fixes needed before merge
   - If all MATCH: proceed to `finishing-a-development-branch`

### 5) After review

- Offer `finishing-a-development-branch` for merge/PR workflow
- Use base skills: `requesting-code-review`, `receiving-code-review`

## Key Principles
- **Reference the relevant skill** for every issue
- **Be specific** — file path and line number for every issue
- **Acknowledge good code** — don't just report problems
- **Check content architecture** — hardcoded dynamic content is a critical finding
