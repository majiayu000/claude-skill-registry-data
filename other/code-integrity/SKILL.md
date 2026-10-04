---
name: code-integrity
description: Cross-language read-only audit engine for production hardcode and leaked mocks/fake data in frontend, backend, mobile, templates, and shared code. Use when Codex must scan TS/JS, Python, Go, Java/Kotlin, C#, PHP, Ruby, Rust, Vue/Svelte/HTML, or mixed repositories and produce evidence-based file:line findings while separating tests, fixtures, stories, seeds, examples, generated files, and vendored code.
---

# Code Integrity

Run a deterministic inventory before interpreting findings:

```bash
node "$SKILL_DIR/scripts/code-integrity-scan.mjs" <path> --mode all --format text
node "$SKILL_DIR/scripts/code-integrity-scan.mjs" <path> --mode hardcode --format json
node "$SKILL_DIR/scripts/code-integrity-scan.mjs" <path> --mode mocks --format text
```

Resolve `$SKILL_DIR` to this skill directory. Keep the audit read-only. Do not install dependencies or execute target-project code.

## Workflow

1. Detect repository languages, frontend/backend boundaries, i18n infrastructure, test roots, generated files, and vendor directories.
2. Run the scanner in the requested mode. Add `--include-test` only when the user asks to inventory legitimate test doubles too.
3. Inspect every candidate in source context. A regex hit is evidence to review, not automatically a defect.
4. Apply `$hardcode-detection` to hardcode candidates and `$mock-data-detection` to mock/fake-data candidates.
5. Report only confirmed production-path findings. Keep uncertain candidates in a separate `review` section.
6. For significant findings, create Task Master tasks with scope, severity, `file:line`, rule, evidence, remediation, and an appropriate implementation owner.

Read [references/language-routing.md](references/language-routing.md) when the repository is not primarily TypeScript/JavaScript or has mixed server/client languages.

## Evidence contract

For each finding include:

```text
[severity] [Frontend|Backend|Mobile|Shared] file:line
Rule: <stable rule id>
Evidence: <short source excerpt>
Why production: <entry point/import/build-path evidence>
Root cause: <why a real boundary was replaced or bypassed>
Remediation: <specific production integration or localization change>
Confidence: high|medium|low
```

Never claim completeness from text matching alone. State scanned roots, excluded roots, languages observed, scanner mode, and limitations.
