---
name: frontclippy-bootstrap
description: Bootstrap frontclippy for a route set by discovering pages, generating a manifest, and pointing CI at config, baseline, and suppression files. Use when the user asks to set up frontclippy, discover routes, or create a starter manifest workflow.
---

# frontclippy-bootstrap

Use this in the `frontclippy` repo when the user wants setup artifacts instead of only an audit.

## Workflow

1. Start from a seed route. If none is given, default to `fixtures/discovery-hub.html`.
2. Write the discovered manifest under `tmp/` unless the user asks to commit it.
3. Run:

```bash
cargo run -p frontclippy-cli -- manifest-discover <seed-target> <output-manifest>
```

4. If the user wants the first audit immediately, follow with:

```bash
cargo run -p frontclippy-cli -- manifest-check <output-manifest>
```

5. When the user wants CI setup, use these repo examples:
   - `fixtures/frontclippy.config.toml`
   - `fixtures/frontclippy.baseline.toml`
   - `fixtures/frontclippy.suppressions.toml`
6. Keep discovery, manifest generation, and first audit separate in the summary so the user can reuse each artifact.

## Response Pattern

Return:

1. the manifest path
2. the discovered routes or surfaces
3. whether you also ran an audit
4. the next command to keep going
