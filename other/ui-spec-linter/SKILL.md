---
name: ui-spec-linter
description: Validate a complete spec package for completeness, vocabulary, consistency, and state coverage before code generation begins. Run this as the final quality gate after all spec files exist and before invoking ui-generate-code. It produces a lint report with severity-ranked issues and suggested fixes — it does not auto-fix.
status: stable
promotion_candidate: true
---

# UI Spec Linter

A skill for catching spec defects before they become implementation defects. It reads the full spec package — brief, blueprint, component specs, system spec — and produces a ranked issue report. A lint failure is cheaper to fix than a redline audit after code is written.

## When to use this skill

Use this skill when:
- A full spec package exists (brief + blueprint + at least one component spec + system spec) and the user is about to run `ui-generate-code`.
- A spec package has been revised after a redline cycle and you want to confirm the revisions are internally consistent.
- A new contributor is picking up an existing spec package and you want a quick health check before they proceed.

Do **not** use this skill when:
- No spec package exists yet. Run `ui-brief`, `ui-blueprint`, and `ui-component-spec` first.
- Only one spec file exists. Validate inline within that skill's own acceptance criteria — the linter is designed for cross-file consistency checks, which are meaningless with a single file.
- The user wants a redline of the implementation, not the spec. Use `ui-redline` for that.

## Core principle

**Bad specs produce bad code.** A vague spec is not a starting point — it is a decision deferred to the implementer, who will make it wrong half the time. The linter's job is to make every deferred decision visible before it becomes a line of code. A lint failure caught here costs a sentence to fix; the same failure caught in a redline costs hours.

## Lint rule categories

The linter checks four categories in order. Run all four every time — do not skip a category because you think it will pass.

---

### Category 1 — Completeness

Check that the minimum required files are present and that each file is fully populated.

**Required files (per `shared/references/spec-package-format.md`):**

| File | Required? |
|---|---|
| `00-index.md` | Required (must include **Run Manifest**) |
| `brief.md` | Required |
| `blueprint.md` | Required |
| `system.md` | Required |
| At least one file under `component-specs/` | Required |
| `acceptance.md` | Required before code generation |
| `microcopy.md` | Required if any user-visible copy exists |

**Run Manifest Check:**

The `00-index.md` MUST include the following sections to prevent stale report bugs:
- `## Run history`
- `## Active reports`
- `## Historical reports`
- `## Superseded reports`

If any report artifact exists in the package (e.g., `*-REPORT.md` or `*-SUMMARY.md`), it MUST be listed in one of the report sections (Active, Historical, or Superseded). An active report that has not been updated after a corresponding code or spec change is a **blocker**.

**Required sections per file type:**

- **brief.md** — all ten sections (§1 Goal through §10 Assumptions) must be present and non-empty.
- **blueprint.md** — must include: hierarchy ranking, wireframe layout, responsive behavior per breakpoint.
- **component spec** — must include: anatomy, states matrix, keyboard map, accessibility requirements, token usage.
- **system.md** — must include all required semantic token categories from `shared/references/token-schema.md`.
- **acceptance.md** — must include at least one criterion per section that applies to the scope.

**Placeholder text check:**

Flag any cell or paragraph containing exactly: `TBD`, `TODO`, `coming soon`, `placeholder`, `fill in`, `[add later]`, `pending`, or any empty section heading (heading with no content below it before the next heading).

---

### Category 2 — Vocabulary

Check for banned vague words and undefined token references.

**Banned vague words (per `shared/references/vague-language-translator.md`):**

The following words are a lint error when they appear in a spec without a concrete translation in the same sentence or the immediately following bullet:

`clean`, `modern`, `intuitive`, `user-friendly`, `sleek`, `beautiful`, `elegant`, `simple`, `professional`, `minimal`, `premium`, `polished`, `nice`, `good`, `better`, `seamless`

A concrete translation means: a token name, a pixel value, a named pattern, or a reference to a specific property. "Generous spacing" is vague. "Generous spacing (`space.8`, 32px)" is concrete.

**Undefined token references:**

For every token name referenced in any spec file (e.g. `color.brand.primary`, `space.6`, `radius.md`), check that the token is defined in `system.md`. Flag any token reference that does not have a matching definition.

Conversely, flag any token defined in `system.md` but never referenced in any other spec file — it may be dead weight or may indicate a component spec is missing.

---

### Category 3 — Consistency

Check that claims made in one file do not contradict claims made in another.

**Checks to run:**

| Check | Source | Target | What to compare |
|---|---|---|---|
| Primary user match | `brief.md §2` | Component spec `§7 Accessibility` | Does the accessibility consideration reflect the primary user's stated constraints? |
| Platform match | `brief.md §7 Constraints > Platform` | Component spec `breakpoints` | Does the component spec define breakpoints that include the brief's declared platform? |
| Spacing token match | `blueprint.md` spacing claims | `system.md space.*` tokens | Every spacing value mentioned in the blueprint must resolve to a token in system.md. |
| Color token match | All component specs | `system.md color.*` tokens | Every color name or value used in a component spec must resolve to a token. |
| Non-goal compliance | `brief.md §8 Non-goals` | Blueprint and component specs | No spec downstream of the brief may spec a feature the brief explicitly listed as a non-goal. |
| Success criteria traceability | `brief.md §6 Success criteria` | `acceptance.md` | Every success criterion in the brief must have at least one corresponding acceptance criterion. |

---

### Category 4 — State coverage

For every interactive component in the `component-specs/` directory, check that the states matrix covers the required states.

**Required states per component type:**

All interactive components must have specs for:

| State | Required for |
|---|---|
| Default | All interactive components |
| Hover | All interactive components |
| Focus / Focus-visible | All interactive components |
| Active / Pressed | Buttons, links, toggles |
| Disabled | Buttons, inputs, selects, any component that can be inactive |
| Loading | Any component that triggers an async operation |
| Error | Inputs, forms, any component that receives or sends data |
| Empty | Lists, tables, feeds, any component that displays a collection |

Flag missing states as **major** issues. A missing loading state on an async trigger is a **blocker** because it indicates the spec will produce code that provides no feedback during network latency.

---

## Output template

Produce the lint report in this exact structure. Do not omit sections; if a section has zero issues, write "None."

```markdown
---
spec_type: lint-report
spec_id: <slug matching the brief>
based_on: <list of spec files linted>
created: <YYYY-MM-DD>
status: draft
spec_consistency: pass | fail
implementation_alignment: not_checked | partial | ready
---

# Spec Lint Report

**Package:** <spec package name>
**Date:** <YYYY-MM-DD>
**Result:** PASS / FAIL (<N> issues found)
**Spec Consistency:** pass (internal structure is coherent)
**Implementation Alignment:** not_checked (spec may require redline fixes after code generation)

## Issues

| Severity | Category | File | Issue | Suggested Fix |
|---|---|---|---|---|
| blocker | Completeness | brief.md | Section §8 Non-goals is empty | Add at least one explicit non-goal |
| blocker | State Coverage | component-specs/button.md | Loading state missing; button triggers async submit | Add loading state to states matrix with spinner and disabled-during-load behavior |
| major | Vocabulary | blueprint.md | "generous spacing" used without a token value | Replace with `space.8` (32px) or the relevant token name |
| major | Consistency | component-specs/form.md | Breakpoints defined for mobile/desktop only; brief §7 states "cross-platform including tablet" | Add tablet breakpoint (768px) to component spec |
| minor | Vocabulary | system.md | Token `color.border.subtle` defined but not referenced in any component spec | Remove token or add a reference note explaining its intended use |

## Summary

- **Blockers:** N (must fix before code generation)
- **Major:** N (should fix before code generation)
- **Minor:** N (fix before v1 release)
- **Passed checks:** N criteria passed without issue

## Next step

<If FAIL:> Resolve all blockers before running `ui-generate-code`. Address major issues in the same pass. Rerun the linter after fixes to confirm clean.
<If PASS:> Spec package is ready for `ui-generate-code`.
```

---

## Auto-fix policy

The linter **does not auto-fix**. It reports issues and suggested fixes. The user, another skill (`ui-component-spec`, `ui-brief`, etc.), or a human reviewer resolves each issue. This is intentional: auto-fixing vocabulary or consistency issues would require judgment calls that belong to the spec author.

---

## Workflow

### Step 1 — Inventory the package

List every file present in the spec package directory. Cross-reference against the required file list in Category 1. Record any missing files immediately as blockers before reading any content.

### Step 2 — Run completeness checks

Open each file in turn. For each file, verify all required sections are present and non-empty. Scan for placeholder text strings. Record every failure with the exact file and section name.

### Step 3 — Run vocabulary checks

For each spec file, scan all prose content for banned vague words. For each occurrence, check whether a concrete translation appears in the same sentence or the immediately following item. Also extract every token reference and cross-check against `system.md`. Record failures with the exact file name and line context.

### Step 4 — Run consistency checks

Execute each check in the consistency table above in order. For each check, quote the source claim and the target claim side by side. If they conflict or one is missing, record the issue.

### Step 5 — Run state coverage checks

For each component spec in `component-specs/`, identify the component's type (button, input, list, etc.) and check the states matrix against the required state list for that type. Record any missing states with the component file name.

---

## Anti-pattern rules

1. **Do not flag style preferences as lint errors.** If the brief says "use a muted palette" and the system spec defines a muted palette, that is not a consistency error. Only flag missing or contradictory information, not aesthetic choices.
2. **Do not invent requirements not in the upstream brief.** If the brief does not mention internationalization, do not add an i18n lint check. Flag only what can be traced to an existing spec claim.
3. **Do not conflate "unused" with "wrong."** A token defined but unused is a minor flag. It is not a blocker. Do not inflate severity.
4. **Do not report the same issue twice.** If a token is undefined, report it once — not once per file that references it.
5. **Do not emit a PASS when blockers exist.** The result line must read FAIL if any blocker or major issue is present. Reserve PASS for a clean run.

---

## Acceptance criteria for this skill's output

A lint report produced by this skill is acceptable only if every one of these is true:

- [ ] The report covers all four lint categories — Completeness, Vocabulary, Consistency, State Coverage — and explicitly states "None" for any category with zero issues.
- [ ] Every issue row includes all five columns: Severity, Category, File, Issue, Suggested Fix.
- [ ] Severity values are drawn exclusively from: `blocker`, `major`, `minor`. No invented severities.
- [ ] The Summary block totals match the count of rows in the Issues table.
- [ ] The Result line correctly reads FAIL if any blocker or major issue is present, and PASS only if zero blockers and zero major issues exist.
- [ ] No issue was flagged as a result of a style preference — every issue traces back to a missing piece of information, a contradictory claim, or a banned word without translation.
- [ ] The report does not suggest auto-fixes that would resolve a contradiction — it suggests where to look and what to decide, leaving the decision to the author.
- [ ] The Next step section gives a concrete instruction matching the PASS or FAIL result.

If any check fails, revise before delivering.

---

## Promotion checklist

Complete every item before changing `status: draft` to `status: stable`.

### Evidence on the failing-spec-package fixture

- [ ] Running this skill against `examples/failing-spec-package/` produces a FAIL report that catches all 9 known defects listed in `examples/failing-spec-package/00-index.md`.
- [ ] FD-01 (missing §8 Non-goals) is reported as Blocker.
- [ ] FD-05 (missing `space.*` tokens) is reported as Blocker.
- [ ] FD-06 (missing `loading` state on async button) is reported as Blocker.
- [ ] FD-03 and FD-04 ("clean layout", "modern feel") are reported as Warnings.
- [ ] FD-09 (success criterion with no corresponding acceptance test) is reported as Blocker.
- [ ] No issues beyond the known 9 are invented (false positives count against promotion).

### Evidence on the settings-page fixture

- [ ] Running this skill against `examples/settings-page/` produces a PASS report (the settings-page package is a correct, complete example).
- [ ] The PASS report correctly shows zero blockers and zero major issues.

### Evidence on the spec-recovery-create fixture

- [ ] Running this skill against `examples/spec-recovery-create/` produces output consistent with `examples/spec-recovery-create/spec-linter-report.md`.
- [ ] The output is FAIL. B-01, B-02, and B-03 blockers are all reported.

### Regression: no style opinions

- [ ] Given a spec with non-standard but internally consistent vocabulary (e.g., custom state names), the linter does not flag it as an issue — only structural and completeness rules apply.

### Skill integration

- [ ] `validate-skill.py` passes for this skill with `status: stable` (no missing sections).
- [ ] `skills.json` entry for `ui-spec-linter` has been updated to `"status": "stable"`.
- [ ] README Skill Map table has been updated to show `stable`.
