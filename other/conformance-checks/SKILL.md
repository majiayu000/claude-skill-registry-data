---
name: conformance-checks
description: "Picks the right tool for a convention no linter knows: helm-unittest for rendered Helm charts, conftest with Rego for YAML, JSON, HCL, TOML and Dockerfile, kubeconform for schemas, never a bespoke check script. Use when writing or reviewing a check for the repository's own rules."
---

# Conformance checks

Enforce a rule specific to this repository where no linter has an opinion.

## When to use

- A convention needs enforcing and no linter covers it.
- A `check-*.sh` script exists and should become a declarative check.
- Deciding where a new rule belongs.

## Rules

- Rendered Helm charts: `helm-unittest`. Declarative suites in `tests/*_test.yaml` next
  to the chart, with `equal`, `matchRegex`, `isKind` and snapshot assertions. Never render
  a chart in a script to grep the output.
- Structured data, meaning YAML, JSON, HCL, TOML or Dockerfile: `conftest` with Rego
  policies under `policy/`. The parser follows the file extension, `--parser` forces one.
- A rule spanning files, for example an item in one file must appear in another:
  `conftest --combine` puts every file into one input array for a single policy.
- Kubernetes manifest schema validity: `kubeconform`, not a hand written rule.
- Language style and correctness: the language's own linter, see `lint`.
- Something only a real validator can judge: invoke that validator directly. Wrapping
  it in assertions adds nothing.
- No bespoke check runner, no assertion library, no declarative format of our own. A
  search for an existing tool happens before any of that gets designed.
- One rule per policy or test case. The failure message names the offending element,
  not the rule text.
- Fixtures and inputs live in files, never inline in the check, so a diff shows whether
  an input or an expectation changed.
- Keep the policy next to what it guards: chart tests with the chart, repository
  policies under `policy/`.
- Call the check from the task runner so CI and a local run do the same thing.
- A check past roughly one screen means the wrong tool is in use, or the right one was
  never looked for.

## Guardrails

- An existing tool was searched for, and the result is named.
- Chart renders go to `helm-unittest`, structured data to `conftest`.
- Cross file rules use `--combine`, not a script reading both files.
- No new framework, no new assertion language, no check script past one screen.
- Failure messages name the offending element.
- Inputs in files, check called from the task runner.

## References

- helm-unittest: <https://github.com/helm-unittest/helm-unittest>
- conftest: <https://www.conftest.dev/>
- `lint` for linter owned rules.
