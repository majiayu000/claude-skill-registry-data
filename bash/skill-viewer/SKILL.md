---
name: skill-viewer
description: List every skill in this repo with its name and one-line description, read live from skills/*/SKILL.md frontmatter. Use when the user asks "what skills are here", "list skills", "what can I run", or wants a quick catalog of the repo's skills. Read-only.
---

# skill-viewer

Show what is in the box. Run the bundled script from anywhere inside the repo:

```bash
python3 "$(git rev-parse --show-toplevel)/skills/skill-viewer/scripts/list_skills.py"
```

It prints one line per skill (name, description) and ends with `N skills`. The count is whatever
is on disk under `skills/*/SKILL.md`; nothing is hardcoded, so a skill you add appears on the next run.

Options: `--json` for machine-readable output, `--root DIR` to point at another checkout.

If a `SKILL.md` has missing or malformed frontmatter the script names it on stderr and exits 1,
so a broken skill never silently disappears from the list.
