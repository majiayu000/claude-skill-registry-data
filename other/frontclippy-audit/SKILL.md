---
name: frontclippy-audit
description: Run frontclippy against a local HTML file, live URL, snapshot JSON, suite, or manifest and summarize the findings. Use when the user asks to audit a UI, inspect frontclippy output, emit SARIF, or run capture plus analysis.
---

# frontclippy-audit

Use this in the `frontclippy` repo when the user wants a real audit run instead of a theoretical explanation.

## Workflow

1. Work from the repo root.
2. Choose the narrowest command for the artifact the user provided:
   - Local HTML file or live URL:

```bash
cargo run -p frontclippy-cli -- check <target>
```

   - Behavioral or keyboard-flow audit:

```bash
cargo run -p frontclippy-cli -- trace-check <target>
```

   - Stress or matrix audit:

```bash
cargo run -p frontclippy-cli -- matrix-check <target>
```

   - Snapshot JSON:

```bash
cargo run -p frontclippy-cli -- analyze <snapshot.json>
```

   - Related snapshots:

```bash
cargo run -p frontclippy-cli -- suite-analyze <snapshot-a.json> <snapshot-b.json> [...]
```

   - Manifest:

```bash
cargo run -p frontclippy-cli -- manifest-check <manifest.toml>
```

3. Add `--format sarif` when the user wants CI or code-scanning output.
4. Add `--config`, `--baseline`, `--suppressions`, or `--write-baseline` when review state matters.
5. If no target is provided, use `fixtures/frontclippy.manifest.toml` for a broad demo or `fixtures/checkout-chaos.html` for a single-surface demo.

## Response Pattern

Return:

1. the exact command that ran
2. the finding count and highest severity
3. whether findings were configured, suppressed, or baselined
4. the most relevant next step
