---
name: roots-reviewing
description: Use when asked to review or audit code in a Roots-stack WordPress project - "review my diff", "check before the MR", a pre-merge or convention audit of providers, hooks, Blade, blocks, post types, routes, Livewire, assets and security. Read-only, fixed report template. For understanding a project use roots-onboarding; for fixing a bug use roots-debugging.
---

# Roots reviewing: convention audit by profile

Reviews a diff or a folder against the conventions of the active profile and reports findings in one fixed template. It reads and reports; it does not edit, commit or push.

## When to use

- Before opening or merging a change request, or when the user asks for a review or a health check.
- After generating code (a block, a provider, a component) to confirm it follows the project's pattern.
- For a second, independent read: run the `acorn-reviewer` agent on the same scope.

## Inputs required

- Scope: files, a folder, or the diff against the default branch (`git diff <default branch>...HEAD --stat` to list it). Default: everything changed on the branch.
- Active profile and app path from the session context or the detector JSON (`scripts/detect-roots-project.mjs`).
- Project rules: `AGENTS.md`, `.ai/`, `.claude/rules/`. A project rule overrides any default below; cite it when it decides a finding.
- Runner placeholders for any command you suggest: `{{runner.test}}`, `{{runner.cache}}`, `{{runner.acorn}}`.

## Procedure

1. **Fix the scope and the profile.** List changed files; group them by area (providers, views, blocks, post types, routes, Livewire, assets, config, tests).
2. **Load the project rules** and note anything stricter than the defaults (language of code, commit rules, native-first gates).
3. **Apply the checks for each area that appears in the scope.** The full greppable checklist is in `references/checklists.md`; the profile decides which checks apply:

   | Area | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
   | --- | --- | --- | --- |
   | Theme provider | `ThemeServiceProvider` extends `Roots\Acorn\Sage\SageServiceProvider` | not applicable | not applicable |
   | Other providers | extend `Illuminate\Support\ServiceProvider`; registered in `config/app.php` or `functions.php` | registered where the boot code lists them (configurator, `config/app.php`, composer extra) | registered in `composer.json` `extra.acorn.providers` |
   | Post types | Poet config or the project's classes | classes or Poet, as the project does | `config/post-types.php` (`roots/acorn-post-types`) |
   | Blocks | ACF Composer class + Blade view | ACF Composer class + Blade view | native `block.json` + Blade render; ACF checks do not apply |
   | Livewire | only if installed | version 4 rules (see `acorn-livewire`) | only if installed |
   | Tests | project suite | project suite | Pest |

4. **Native-first check.** For every custom class or hook in the diff, ask which native WordPress / ACF / Acorn mechanism covers it and whether the diff says why not. Missing reason on a duplicate of a native mechanism is a finding.
5. **Security and escaping pass** on every view and endpoint touched (checklist section "Security").
6. **Run the tests the scope implies** (`{{runner.test}}`) when the user allows it; a failing test is a Critical finding with the output line.
7. **Report with the template below.** Every finding has file:line, the rule, and the skill that explains it. Count findings by severity. Acknowledge what is done well.
8. **Do not fix** unless the user asks afterwards; then hand each finding to the owning skill.

### Severity

| Severity | Meaning | Examples |
| --- | --- | --- |
| Critical | Breaks behaviour, security or data | unescaped output, missing `permission_callback`, double escape that corrupts a URL, provider never registered, raw SQL without `prepare` |
| Improvement | Convention or maintainability | hooks outside `boot()`, logic in a Blade view, custom code duplicating a native mechanism |
| Good practice | Worth keeping | tests added, native hook used with a verified reason |

### Report template (fixed)

```markdown
## Review: <scope>
Profile: <kind> at <path>   Rules read: <files>

### Critical
- **<file>:<line>** - <issue>. Rule: <rule>. See `<skill>`.

### Improvement
- **<file>:<line>** - <issue>. Rule: <rule>. See `<skill>`.

### Good practices
- <observation>

### Not checked
- <area and why, for example "Livewire: not installed">

### Summary
<X> critical, <Y> improvements, <Z> good practices. Verdict: <ready | ready after fixes | needs rework>.
```

## Verification

- Each finding points to a real line you read; no finding is inferred from a file name alone.
- Checks for packages the profile lacks (ACF on `radicle-app`, Livewire when not installed) are listed under "Not checked", not reported as violations.
- The report uses the template exactly and states the profile.
- Suggested commands use runner placeholders; none runs `wp`, `composer`, `php`, `yarn` or `npm` bare.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| ACF findings on a project without ACF | Applied the `sage-theme` checks to `radicle-app` | Re-read the profile; move them to "Not checked" |
| "Provider not registered" false alarm | Registration lives in `composer.json` extra or a configurator | Check the profile's registration place with `scripts/inventory-project.mjs --app <path>` |
| Review flags a project convention as wrong | Project rule stricter or different from the default | Follow the project rule; cite it |
| Findings without line numbers | Reviewed the summary, not the file | Open the file and cite the line |
| Verdict "ready" but tests were not run | Skipped step 6 silently | State that tests were not run |

## Escalation

- Disagreement between a project rule and a native mechanism: report both and ask the user which wins.
- A suspected security issue in code outside the scope: report it separately, do not widen the review silently.
- Large diffs (over about 40 files): ask whether to split the review by area and run `acorn-reviewer` per area.

<!-- verified: refs/roots-sage/app/Providers/ThemeServiceProvider.php:7 — extends SageServiceProvider; refs/roots-acorn/src/Roots/Acorn/Sage/SageServiceProvider.php:9 — SageServiceProvider extends Illuminate ServiceProvider; vendor/illuminate/view/Compilers/BladeCompiler.php:124 — echo format e(%s); vendor/illuminate/support/helpers.php:124 — e() double-encodes by default; vendor/log1x/acf-composer/src/Console/BlockMakeCommand.php:18 — acf:block; src/Console/stubs/block.localized.stub:146,156 — with() and fields(); upstream design-system checks (R-css-vars, R-component-reuse, R-nl2br) dropped as project-specific -->
