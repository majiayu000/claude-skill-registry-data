---
name: encoding-fix-script-first
description: Enforce script-only text encoding fixes in any repository. Use when files contain mojibake, broken Cyrillic/UTF-8 text, or UTF-8 BOM issues, and require Codex to run the bundled `scripts/fix_mojibake.py` instead of manual or ad-hoc encoding edits.
---

# Encoding Fix Policy

Use this skill only for encoding/BOM correction tasks.
Do not use this skill for layout, SEO, routing, or feature implementation.

## Workflow

1. Identify target files or directories with suspected encoding issues.
2. Run only the bundled script for fixes:
   - `python scripts/fix_mojibake.py <paths...>`
   - On Windows fallback: `py -3 scripts/fix_mojibake.py <paths...>`
   - Script behavior: if `ftfy` is missing, it installs `ftfy` automatically and continues.
3. If preview mode is needed first, run:
   - `python scripts/fix_mojibake.py --dry-run <paths...>`
4. Limit extensions when needed:
   - `python scripts/fix_mojibake.py <paths...> --extensions .php .html .js .css .md .xml .yaml`
5. Re-run the script after edits if new mojibake appears.

## Output Format

In the final response:
- List processed paths.
- Include the exact `fix_mojibake.py` command used.
- Report whether files changed.

## Hard Rules

- Do not manually rewrite mojibake text as a primary fix.
- Do not use ad-hoc recoding via editors/scripts when `scripts/fix_mojibake.py` can handle the case.
- If script output is insufficient, report remaining files and ask for explicit permission before custom recovery steps.
