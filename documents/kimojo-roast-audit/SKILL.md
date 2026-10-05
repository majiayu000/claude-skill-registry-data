---
name: kimojo-roast-audit
description: Generate or refresh the Kimojo roast audit report; use when asked to audit doc vs code drift for the roast.
metadata:
  short-description: Roast audit report generator
---

# Kimojo Roast Audit Skill

Use this skill when asked to generate or update the roast audit report, or to check doc vs code drift for the roast.

## Quick start

1) Run the repo-local script from anywhere inside the repo:

```bash
./scripts/audit_roast.sh --out ai_docs/kimojo_roast_audit_report.generated.md
```

## Flags

- `--out <path>`
- `--config <path>` (default: `ai_docs/roast_audit_probes.tsv`)
- `--strict`
- `--quiet`

## Output

- Writes a markdown report to the output path.
- Includes summary counts and evidence lines from ripgrep.

## Notes

- Source of truth is the repo script (`scripts/audit_roast.sh`).
- Probes live in `ai_docs/roast_audit_probes.tsv`.
