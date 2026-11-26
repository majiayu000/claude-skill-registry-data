---
name: lint
description: "Detects the repository's formatters and linters from mise.toml, the task runner and config files, runs them and fixes the findings without disabling a rule to pass. Use when code needs linting or formatting, a lint job fails, or someone asks to run the linters."
---

# Lint

Run the repository's own formatters and linters and fix what they report.

## When to use

- Before committing or opening a pull request.
- When a lint or format job fails in CI.

## Steps

1. Detect the tooling from `mise.toml` first, then the task runner, then config files.
   Prefer the `lint:<tool>` task targets over calling a tool directly when they exist.
2. Match the tool to the file type: `golangci-lint fmt` (`gofumpt`), `go vet`, `golangci-lint`
   for Go; `ruff check`, `ruff format` for Python; `eslint` or `oxlint` for JavaScript and
   TypeScript; `shellcheck`, `shfmt` for shell; `yamllint` for YAML; `markdownlint` for
   Markdown; `actionlint` for GitHub Actions; `tofu fmt`, `tflint`, `trivy config` for
   OpenTofu; `ansible-lint` for Ansible; `helm lint` for Helm charts; `hadolint` for container
   images.
3. Run the formatter before the linter. Formatting noise mixed into a lint fix makes the
   diff unreadable.
4. Fix findings at the cause. Never disable a rule repository wide to silence one finding.
5. A justified exception is inline, narrow and names the rule and the reason. No blanket
   ignore file.
6. Keep configuration changes in a commit separate from the fixes they enable.
7. If a tool is missing locally, name it and the install command. Never skip the check
   silently.
8. Report what ran, what was fixed and what remains, with the reason.

A linter enforces a community default and gets configured, never reimplemented. A rule that
only this repository cares about belongs to `conformance-checks`, not a new linter config.

## Guardrails

- Tooling detected from the repository. No new tool introduced without asking.
- Formatter and linter both run. Formatting committed separately from fixes.
- Findings fixed at the cause. Exceptions narrow, inline and justified.
- Missing tools reported, never skipped silently.
- Final result reported honestly, including what still fails.

## References

- `conformance-checks` for rules no linter knows.
