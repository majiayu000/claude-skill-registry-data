---
name: sf-code-analyzer-quality
description: Salesforce Code Analyzer v5 and the rest of the local quality gate - sf code-analyzer run/rules/config with --workspace, --target, --rule-selector, --severity-threshold, --view, --output-file and --config-file, the pmd, eslint, regex, retire-js, flow, cpd and sfge (Salesforce Graph Engine) engines, code-analyzer.yml schema with rule overrides, ignores and suppressions, custom PMD rulesets and XPath rules, ESLint flat config with @salesforce/eslint-config-lwc, Prettier with prettier-plugin-apex, the 1-5 severity taxonomy and the analyzerFailSeverity gate, baseline and ratchet strategies for legacy code, SARIF output and CI annotation. Use when configuring or running static analysis, triaging violations, authoring or suppressing rules, or when running vf-check static, vf-check lint, vf-check format, vf-check analyzer, or vf-check local.
---

# Code Analyzer and Quality Gates

## When to use

- Setting up or changing static analysis for a Salesforce project.
- Triaging a `vf-check analyzer` failure, deciding fix versus suppress, or writing a suppression with
  a reason and a cap.
- Authoring a custom PMD rule or a regex rule for a project convention.
- Wiring Prettier/ESLint so `vf-check format` and `vf-check lint` are deterministic.
- Introducing the gate to a legacy codebase without stopping delivery (baseline and ratchet).
- Wave 2 of the vibe-force workflow: `sf-quality-gate` runs `vf-check local` and reports.
- Org-wide debt rather than a diff: skill `sf-technical-debt-audit` (it turns recurring findings into regex rules authored here).

## Toolchain and prerequisites

| Tool | Install | Requirement |
| --- | --- | --- |
| Code Analyzer plugin | `sf plugins install code-analyzer` (it is also a JIT plugin: running a `code-analyzer` command installs it automatically) | Salesforce CLI; Node.js 20 or later if the CLI was installed via `npm` |
| `pmd`, `cpd`, `sfge` engines | bundled with the plugin | JDK 11 or later |
| `flow` engine (Flow Scanner) | bundled | Python 3.10.0 or later |
| `eslint`, `retire-js`, `regex` engines | bundled | Node, no extra runtime |
| Prettier + Apex plugin | `npm i -D prettier prettier-plugin-apex` | Node 22 or later; JRE 17 or later only on platforms without a prebuilt native parser |
| LWC ESLint | `npm i -D eslint @babel/core @babel/eslint-parser @salesforce/eslint-config-lwc @lwc/eslint-plugin-lwc @salesforce/eslint-plugin-lightning eslint-plugin-import eslint-plugin-jest` | ESLint 9 for `@salesforce/eslint-config-lwc` 4.x and `@lwc/eslint-plugin-lwc` 3.x |

If Java or Python are unavailable in an environment (a lean CI image, for example), disable those
engines in `code-analyzer.yml` rather than tolerating engine errors:

```yaml
engines:
  flow:
    disable_engine: true
  cpd:
    disable_engine: true
```

Config files live in the plugin and are referenced by the check runner; do not duplicate them per
project: `config/code-analyzer.yml`, `config/pmd/apex-ruleset.xml`, `config/eslint/eslint.config.mjs`,
`config/prettier/.prettierrc`.

## Engines

| Engine | Analyzes | Detects | Notes |
| --- | --- | --- | --- |
| `pmd` | Apex, Visualforce, HTML, JavaScript, XML | security, error-prone, performance, style, documentation | JDK required; default languages `apex` and `visualforce`; AppExchange ruleset available via `--rule-selector AppExchange` |
| `eslint` | JavaScript, TypeScript, LWC, Aura, CSS/SCSS (SLDS), JSX | LWC rule violations, JS correctness, SLDS 2 misuse, React/JSX when enabled | bundles `@salesforce/eslint-config-lwc/recommended` and `@lwc/lwc-platform/recommended`; supports ESLint 8 and 9 |
| `regex` | any text file | project conventions, banned strings, trailing whitespace | custom rules need a global-modifier regex (`/TODO/gi`) |
| `retire-js` | bundled JavaScript, static resources | known-vulnerable third-party libraries | |
| `flow` | Flows, subflows | unsafe Flow patterns, data passed into `without sharing` Apex | Python required |
| `cpd` | multiple languages | copy/paste duplication | JDK required; off by default in the vibe-force config |
| `sfge` | Apex | path-based CRUD/FLS, sharing, null-pointer, loop-database, mass-schema-lookup issues | Developer Preview; JDK required; slowest engine |

## Severity taxonomy and the gate

| Severity | Name | vibe-force policy |
| --- | --- | --- |
| 1 | Critical | blocks; fix before the PR leaves wave 2 |
| 2 | High | blocks |
| 3 | Moderate | blocks (`gates.analyzerFailSeverity` default `3`) |
| 4 | Low | reported, does not block |
| 5 | Info | reported, does not block |

`--severity-threshold` makes the command exit non-zero when a violation meets or exceeds the given
level; it accepts a number or its name (`2` or `"High"`). `vf-check analyzer` passes
`gates.analyzerFailSeverity` from `.vibeforce/config.json`.

## Core patterns

### 1. List the rules before running them

```bash
# recommended rules for every available engine (the default selector is Recommended)
sf code-analyzer rules

# everything the pmd engine offers, with full detail
sf code-analyzer rules --rule-selector pmd --view detail

# scope to what actually applies to this codebase
sf code-analyzer rules --rule-selector all --workspace . --target force-app/**/*.cls
```

`--rule-selector eslint` is equivalent to `eslint:all`; append `:Recommended` to stay inside the
recommended set. Criteria combine with `:` as AND and `,` as OR, and parentheses group; a selector
containing parentheses must be double-quoted.

### 2. Run the same selectors

```bash
sf code-analyzer run --workspace . --rule-selector Recommended --severity-threshold 3 --view detail

# Apex-only path analysis, whole project as context, targeted files as entry points
sf code-analyzer run --workspace . --rule-selector sfge --target force-app/main/default/classes

# machine-readable plus human-readable in one pass
sf code-analyzer run --workspace . \
  --output-file .vibeforce/reports/analyzer.json \
  --output-file .vibeforce/reports/analyzer.html
```

`--workspace` is the analysis context (default `.`); `--target` narrows which files produce
violations while keeping the workspace available to engines that need the whole project - Graph
Engine compiles the workspace to build its call graph.

### 3. Generate and evolve the configuration

```bash
# write the current effective configuration, comments included, to a file
sf code-analyzer config --config-file ./code-analyzer.yml --output-file ./code-analyzer.yml

# just the recommended rules, including their unmodified default values
sf code-analyzer config --rule-selector Recommended --include-unmodified-rules

# what is configured for one rule
sf code-analyzer config --rule-selector pmd:ApexCRUDViolation
```

Every `code-analyzer` command auto-discovers `code-analyzer.yml` or `code-analyzer.yaml` in the
current folder; `--config-file` overrides the location. Schema details:
`references/code-analyzer-cli.md` and `references/config-templates.md`.

### 4. Override severity and tags instead of deleting rules

```yaml
rules:
  pmd:
    ApexCRUDViolation:
      severity: "Critical"
      tags: ["Recommended", "Security", "VibeForceBlocking"]
    ApexDoc:
      disabled: true
  eslint:
    "@lwc/lwc/no-inner-html":
      severity: 1
  regex:
    NoTrailingWhiteSpace:
      tags: ["Suggestion"]
```

`rules.<engine>.<rule>.severity` accepts `1`-`5` or `Critical|High|Moderate|Low|Info`; `tags`
replaces the rule's tags; `disabled: true` switches the rule off for every file.

### 5. Add a project convention as a regex rule

```yaml
engines:
  regex:
    custom_rules:
      NoSeeAllData:
        regex: /@IsTest\s*\(\s*seeAllData\s*=\s*true\s*\)/gi
        file_extensions: [".cls"]
        description: "Tests must not use seeAllData=true."
        violation_message: "Replace seeAllData=true with @TestSetup-created data."
        severity: 2
        tags: ["Recommended", "VibeForce"]
```

The regex must carry a global modifier (`/.../g` or `/.../gi`); without it the engine errors.
`[unverified]` The exact property names under `custom_rules` beyond `regex` and `file_extensions`
were not enumerated on the fetched configuration pages; generate a skeleton with
`sf code-analyzer config --rule-selector regex --include-unmodified-rules` and copy the shape it
prints.

### 6. Add a custom PMD rule

1. Write an XPath rule (or a Java rule packaged in a JAR) in a PMD ruleset XML file; use
   `sf code-analyzer ast-dump` to see the AST you are matching against.
2. Register the ruleset:

```yaml
engines:
  pmd:
    custom_rulesets:
      - "config/pmd/apex-ruleset.xml"
    java_classpath_entries: []
```

3. Confirm registration, then run it:

```bash
sf code-analyzer rules --rule-selector pmd:Custom --view detail
sf code-analyzer run --rule-selector pmd:CheckForBadVariableNames --view detail
```

Code Analyzer tags every custom rule `Custom` and also adds a tag matching the `<ruleset>` `name`
attribute with spaces removed. Custom PMD severities derive from PMD priority: 1 -> 2 (High),
2 -> 3 (Moderate), 3 -> 3 (Moderate), 4 -> 4 (Low), 5 -> 4 (Low).

### 7. Suppress narrowly, with a reason

In-source markers (processed by Code Analyzer v5 for any text file):

```javascript
// code-analyzer-suppress-next-line eslint:no-console -- deliberate build-time diagnostic
console.log('bundle built');
```

Configuration-level bulk suppression:

```yaml
suppressions:
  disable_suppressions: false
  "force-app/legacy/classes/":
    - rule_selector: "pmd:ApexCRUDViolation,pmd:ApexSharingViolations"
      max_suppressed_violations: 40
      reason: "Legacy module; tracked by VF-214, migrating to user mode per quarter."
```

Marker forms: `code-analyzer-suppress`, `code-analyzer-suppress-line`,
`code-analyzer-suppress-next-line`, and `code-analyzer-unsuppress` to restore checking. A bare
`code-analyzer-suppress` applies from that line to end of file or until an unsuppress marker, so
prefer the line-scoped forms. Folder paths in `suppressions` must end with `/`. `--no-suppressions`
ignores both marker and config suppressions, except that a `suppressions.disable_suppressions`
setting in the config file takes precedence over the flag. PMD's own `@SuppressWarnings('PMD.RuleName')`
annotation and `// NOPMD` comment still work for the PMD engine; vibe-force prefers the
Code Analyzer markers because they work across every engine and are greppable.

### 8. Formatting and linting around the analyzer

```bash
# format check (what vf-check format runs)
npx prettier --check --config config/prettier/.prettierrc --ignore-path config/prettier/.prettierignore "force-app/**/*.{cls,trigger,js,html,css,xml,json}"

# lint LWC/Aura JS (what vf-check lint runs)
npx eslint --config config/eslint/eslint.config.mjs "force-app/**/lwc/**/*.js" "force-app/**/aura/**/*.js"
```

Prettier owns whitespace, ESLint owns JavaScript semantics, Code Analyzer owns Apex, metadata, and
cross-language rules. Never encode formatting preferences as analyzer rules.

### 9. Composition of the vibe-force checks

| `vf-check` | Composed of |
| --- | --- |
| `format` | `prettier --check` over changed Apex, LWC, Aura, XML, JS (`--fix` runs `prettier --write`) |
| `lint` | `eslint` over changed LWC/Aura JS |
| `analyzer` | `sf code-analyzer run --config-file config/code-analyzer.yml --severity-threshold <gates.analyzerFailSeverity>` over the changed files as `--target` with the package directories as `--workspace` |
| `static` | `format` + `lint` + `analyzer` |
| `local` | `static` + `jest` - the full no-org gate |

Reports land in `<project>/.vibeforce/reports/<check>-<ISO>.json` with `{check, startedAt,
durationMs, status, gates, findings[], raw}`. Exit codes: `0` pass, `1` gate failed, `2`
misconfiguration or missing tool, `3` org/network error.

## Anti-patterns

| Anti-pattern | Consequence | Instead |
| --- | --- | --- |
| `--rule-selector eslint` when you meant the recommended set | runs every ESLint rule, floods the report | `eslint:Recommended` |
| `--target` without `--workspace` on Graph Engine runs | Graph Engine cannot build the call graph and misses or misreports paths | pass the whole project as `--workspace` |
| Deleting a rule from the ruleset to silence it | loses the signal everywhere, silently | `rules.<engine>.<rule>.disabled` with a comment, or a scoped suppression |
| Bare `code-analyzer-suppress` at the top of a file | suppresses to end of file | `code-analyzer-suppress-next-line <selector> -- reason` |
| Suppression without `max_suppressed_violations` | debt grows invisibly | set a cap; new violations beyond it are reported normally |
| Running `--rule-selector all` in the PR gate | noisy, slow, unstable across plugin upgrades | `Recommended` plus explicitly added rules |
| Turning off the whole `sfge` engine because it is slow | loses path-based CRUD/FLS detection | keep it in the nightly or pre-deploy run, raise `java_thread_count`, `java_max_heap_size` |
| `auto_discover_eslint_config: true` plus a conflicting local config | plugin-version conflicts and engine errors | pin `eslint_config_file` to `config/eslint/eslint.config.mjs` |
| Formatting rules enabled in both Prettier and ESLint | fight each other on every save | Prettier formats, ESLint lints |
| Using v4 syntax (`sf scanner run --category Security`) | removed command surface | see the migration table in `references/code-analyzer-cli.md` |

## Verification

```bash
# does the configuration resolve and are the intended rules selected?
sf code-analyzer config --config-file config/code-analyzer.yml --rule-selector Recommended
sf code-analyzer rules --config-file config/code-analyzer.yml --workspace . --view table

# the gate itself, on changed files only
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" analyzer --changed

# the full local gate before any deploy
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local

# CI: SARIF for code scanning upload
sf code-analyzer run --workspace . --rule-selector Recommended \
  --severity-threshold 3 --output-file analyzer.sarif
```

A configuration change is proven by a before/after `sf code-analyzer rules --rule-selector <rule>`
pair showing the new severity or tags, plus a `run` that exits `0` on clean code and `1` on a
deliberately seeded violation.

## References

- `references/code-analyzer-cli.md` - command, flag, and engine tables; output file formats; v4 to v5 migration.
- `references/rule-catalogue.md` - highest-value PMD Apex, ESLint LWC, Graph Engine, regex, and retire-js rules with fixes.
- `references/config-templates.md` - the content expected in `config/code-analyzer.yml`, `config/pmd/apex-ruleset.xml`, `config/eslint/eslint.config.mjs`, `config/prettier/.prettierrc`, `.prettierignore`.
- `references/quality-gates-and-baselines.md` - gate policy, legacy baselines, ratchets, CI integration, suppression review.
- Code Analyzer: [Use CLI Commands](https://developer.salesforce.com/docs/platform/salesforce-code-analyzer/guide/analyze.html), [Customize the Configuration](https://developer.salesforce.com/docs/platform/salesforce-code-analyzer/guide/config-custom.html), [Top-Level Customization Reference](https://developer.salesforce.com/docs/platform/salesforce-code-analyzer/guide/config-toplevel.html), [PMD engine](https://developer.salesforce.com/docs/platform/salesforce-code-analyzer/guide/engine-pmd.html), [ESLint engine](https://developer.salesforce.com/docs/platform/salesforce-code-analyzer/guide/engine-eslint.html), [Graph Engine](https://developer.salesforce.com/docs/platform/salesforce-code-analyzer/guide/engine-sfge.html), [Graph Engine rules](https://developer.salesforce.com/docs/platform/salesforce-code-analyzer/guide/rules-sfge.html), [Suppress Violations](https://developer.salesforce.com/docs/platform/salesforce-code-analyzer/guide/suppress-violations.html), [Output Schemas](https://developer.salesforce.com/docs/platform/salesforce-code-analyzer/guide/output-schemas.html)
- CLI reference: [code-analyzer commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_code-analyzer_commands_unified.htm)
- [PMD Apex rules](https://pmd.github.io/pmd/pmd_rules_apex.html), [PMD rulesets](https://docs.pmd-code.org/latest/pmd_userdocs_making_rulesets.html)
- [@lwc/eslint-plugin-lwc](https://github.com/salesforce/eslint-plugin-lwc), [@salesforce/eslint-config-lwc](https://github.com/salesforce/eslint-config-lwc), [prettier-plugin-apex](https://github.com/dangmai/prettier-plugin-apex)
- Sibling skills: `sf-apex-development`, `sf-apex-testing`, `sf-lwc-development`, `sf-lwc-jest-testing`, `sf-security-model`, `sf-debugging-logs`, `sf-deployment-strategies`, `sf-post-deploy-verification`.
