---
name: caveman-help
description: "Manual one-shot reference card for Caveman levels and companion skills. Use only when explicitly invoked as $caveman-help, /caveman-help, 'Caveman help', or an unambiguous question about Caveman commands or levels. Never activate for generic help requests; do not activate a mode or change files. Turkish triggers: Caveman yardım, mağara modu seviyeleri ve komutları."
license: MIT
---

# Caveman Help

Return a compact reference card. Do not activate a mode, create state, or
promise environment-variable, hook, status-line, or config-file behavior.

Safety-adapted from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman), MIT licensed. Preserve the included `LICENSE` when redistributing.

## Modes

| Request | Result |
|---|---|
| `$caveman lite` | Tight, complete sentences. |
| `$caveman` or `$caveman full` | Clear fragments; all facts retained. |
| `$caveman ultra` | Minimum unambiguous wording. |
| `$caveman wenyan-lite` | Light classical-Chinese register. |
| `$caveman wenyan-full` | Compact classical-Chinese register. |
| `$caveman wenyan-ultra` | Maximum safe classical compression. |
| `$caveman off`, `/caveman off`, `normal mode`, `stop caveman`, or “mağara modunu kapat” | Return to normal prose. |

## Companion skills

| Skill | Invocation | Purpose |
|---|---|---|
| `caveman-commit` | `$caveman-commit` | Draft a terse Conventional Commit message. |
| `caveman-review` | `$caveman-review` | Produce concise, evidence-backed review findings. |
| `caveman-compress` | `$caveman-compress` | Build and validate a preview before changing a text file. |
| `caveman-help` | `$caveman-help` | Show this one-shot card. |

Only `caveman` may be inferred from explicit Caveman wording. Companion skills
are manual to prevent collisions with general commit, review, and compression
skills.
