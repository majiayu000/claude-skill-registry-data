---
name: intentumdiff-guardrails
description: >-
  IntentumDiff's protected-config guardrails — the project policy that flags semantically risky
  changes to protected settings (API keys, immutable fields, resource identities) in config/data
  files. Use this whenever you work on guardrail detection, the `intentumdiff.yaml` policy, the
  `GuardrailViolation` output, guardrail severity/strict-mode behavior, or how guardrails surface
  in the CLI and the VS Code extension. It covers what languages guardrails apply to and why
  (keyed/resource profiles, semantic keys not line numbers), the policy file shape, the
  important-vs-immutable severity model, and the CLI/extension wiring. Read intentumdiff-engine for
  where guardrails sit in the pipeline and intentumdiff-language-profiles for the keyed/resource
  identity model guardrails rely on; new authoritative logic belongs in the Rust core.
---

# IntentumDiff — Protected-config guardrails

Guardrails let a project declare **protected semantic paths** and get flagged when a diff changes
them — e.g. "`settings.api_key` must not change" or "this Databricks job's cluster is immutable."
They run after the final review diff is assembled (pipeline **stage 5e**), and their hits become
`SemanticDiff.guardrail_violations`.

Core module: `src/intentumdiff/analysis/guardrails.py` (test-oracle; the authoritative engine
destination is Rust — see `intentumdiff-architecture`). Deep doc: `docs/GUARDRAILS.md`.

## Why guardrails are key-based, not line-based

Guardrails are **restricted to keyed/resource-profile config languages** —
`GUARDRAIL_CONFIG_LANGUAGES = KEYED_DATA_LANGUAGES | RESOURCE_PROFILE_LANGUAGES` (json, yaml, adf,
databricks/databricks-workflow, hcl, dockerfile, puppet, …). This is deliberate: a protected path
like `resources.jobs.nightly.schedule` is matched against the file's **stable semantic key**
(`keyed_data_key` / `resource_profile_key`, see `intentumdiff-language-profiles`), not a line number
or a fuzzy AST path — so the policy keeps working when the file is reordered or reformatted. Code
languages have no stable semantic-path identity of this kind, so guardrails don't apply to them.

## The policy file (`intentumdiff.yaml`)

`GUARDRAIL_POLICY_FILENAME = "intentumdiff.yaml"` at the project root (or an explicit
`DiffConfig.guardrail_policy_path`). It declares `ProtectedRule`s:
`{ rule_id, severity, language, path, message, files? }` — `path` is the protected semantic path
(supports globbing), `files` optionally scopes the rule to matching file globs. **Edits to
`intentumdiff.yaml` itself are protected by default**, so the policy can't be silently weakened.

## Severity model (`GuardrailSeverity`)

- **`important`** — review-required; a call-out, not a hard stop.
- **`immutable`** — must not change; the strongest signal.

`GuardrailViolation` carries: `rule_id, severity, file, language, semantic_path, node_type,
old_node_id, new_node_id, old_value, new_value, message` — enough to explain *what* protected
value changed and *from → to*, which the intent explainer and release notes correlate by
`semantic_path`.

## Config knobs (`DiffConfig`)

- `guardrails_enabled: bool = True` — run project `intentumdiff.yaml` checks.
- `guardrails_strict: bool = False` — a direct CLI diff exits **non-zero** when any `immutable`
  violation is present (for CI gating).
- `guardrail_policy_path: Path | None` — explicit policy override.
When diagnostics are enabled, guardrail hits are also recorded as `guardrails` trace events.

## How guardrails surface

- **CLI:** `SemanticDiff.guardrail_violations`; strict mode → non-zero exit on immutable hits.
- **VS Code extension:** violations become `vscode.Diagnostic`s in the Problems panel, are
  **pinned at the top** of the Semantic Changes tree and review panel, and map to **critical**
  risk in intent/release-notes (see `intentumdiff-vscode` / `intentumdiff-release-notes`). They are
  the highest-severity review signal — never suppressed as noise.

## Working on guardrails

- Reproduce: put an `intentumdiff.yaml` beside a fixture, diff a protected-path change via the real
  engine, and assert on `diff.guardrail_violations` (rule_id, severity, semantic_path, old/new
  value). See `tests/unit/test_invariances.py` / guardrail-focused tests for the pattern.
- Adding coverage for a new config language means it must first have a keyed or resource profile
  (identity by semantic key) — guardrails build on that, so extend the profile first
  (`intentumdiff-language-profiles`).
- Pure-Python changes here need no maturin rebuild; the authoritative fix (per the boundary) is
  the Rust core's guardrail interpretation, with the Python module as the parity oracle.
