---
name: pr-review
description: Lightweight per-PR security gate that detects Critical and High severity OWASP/LLM issues in changed files only. Use when scanning a small git diff in CI for blocking findings. Single-pass; does not dispatch subagents and does not perform threat modeling or attack-chain analysis.
---

# Pull Request Security Gate (A01:2025–A10:2025 + LLM01:2025–LLM10:2025)

## What this checks

Fast single-pass review of the files in a pull request diff. Reports
only Critical and High severity findings. Designed for CI: completes
in seconds-to-minutes on `haiku`, well under the time a developer
expects to wait on a PR check. This is the per-PR gate. For nightly
or deep audits, reach for `security-review` or `contract-review`.

## Vulnerable patterns

Soundcheck's per-category skills (`injection`, `csrf`, `ssrf`,
`broken-access-control`, `authentication-failures`,
`hardcoded-secrets`, `path-traversal`, `prompt-injection`, …)
auto-invoke when their description matches code in the diff. Examples
this gate is expected to catch on a routine PR:

- SQL or shell string built from request data — `injection`
- Path opened from a URL parameter without normalization —
  `path-traversal`
- A new credential string-literal in a config file —
  `hardcoded-secrets`
- A new state-changing endpoint without `csrfProtection` —
  `csrf`
- A new fetch to a caller-supplied URL with no host allowlist —
  `ssrf`

## Procedure

This skill is the coordinator — it does the reading; per-category
skills supply the patterns. No subagents.

```
- [ ] Read every file in the supplied changed-file list once
- [ ] Apply soundcheck's per-category skills as their descriptions match
- [ ] Filter findings to severity Critical or High
- [ ] Emit findings table only (no chains, no design review)
- [ ] Append the machine-readable <soundcheck-findings>[...] block
```

For each finding, the table row contains:

| Severity | File:Line | Skill | Finding | Fix |

- *Severity* is Critical or High; drop Medium and Low.
- *File:Line* must be inside the supplied changed-file list.
- *Skill* names the auto-invoking soundcheck skill the pattern matched.
- *Finding* is one short sentence a non-security developer can act on.
- *Fix* is one short sentence; link or quote the secure pattern from
  the relevant skill's `Fix immediately` block.

If a pattern requires cross-file tracing or threat modeling to
classify, **do not emit it** — that's mode 2's job. Better a clean
miss in CI than a noisy false positive that trains developers to
ignore the gate.

Finish with one summary line: `N findings (M Critical/High)` or
`No Critical or High findings.` Suggest `/security-review` for a
deeper manual scan.

## Verification

- [ ] Every emitted finding is severity Critical or High
- [ ] Every emitted finding's file:line is inside the changed-file list
- [ ] No Agent tool invocations (single-pass, no subagent dispatch)
- [ ] Response ends with a one-line summary
- [ ] Machine-readable `<soundcheck-findings>` block appended

## References

- CWE-693 ([Protection Mechanism Failure](https://cwe.mitre.org/data/definitions/693.html))
- [OWASP Web Top 10:2025](https://owasp.org/www-project-top-ten/)
- [OWASP LLM Top 10:2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
