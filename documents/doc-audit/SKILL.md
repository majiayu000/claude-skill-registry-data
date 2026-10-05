---
name: doc-audit
description: "Trigger when auditing documentation, checking markdown link integrity, formatting tables, checking headers, or verifying absolute/relative paths."
---

# Documentation Audit Skill

The markdown audit prose rules (link integrity, header hierarchy, linting standards) now live in [documentation §13](../documentation/SKILL.md). This skill retains the link-integrity check script.

## Utility Script Usage

Run automated link checks with the script at `scripts/check_docs.py`:

```bash
python3 skills/doc-audit/scripts/check_docs.py .
```

It scans markdown files for broken local and external links.
