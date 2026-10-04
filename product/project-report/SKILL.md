---
name: project-report
description: Generate the project's complete status report — a read-only Keelokit page with every stage and its documents (context, gaps, PRD scope and metrics, stack, backlog by wave and by epic), bug bashes and security reviews with their findings, environments, decisions and history — to share with someone or export as a file. Use when the user says "reporte", "reporte completo", "informe de estado", "exportá el estado", "para compartir", "status report", "export", "share the project's status", or presses "Generate the full report" on the dashboard. For day-to-day work, use project-dashboard.
---

# Report — the whole project on one read-only page

The same script as the dashboard, in report mode: everything the repo says about the project, laid
out to read end to end. It has no buttons that prepare requests and no Ask Claude box — it is
for reading, sharing and keeping, not for working (that is `/keelokit:project-dashboard`).

## 1. Build

Project root and language as in `project-dashboard` (`[dashboard] lang` in `.keelokit/state.toml`).

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/project-dashboard/scripts/dashboard.py" --root <root> --report
```
writes `.keelokit/out/report.html` for the Artifact tool; add `--standalone` for a complete HTML
file that opens in any browser (`--out <file>` to choose where).

## 2. Hand it over

Ask once, in one line, what the user wants unless they said it:
- **A page to share** → publish `report.html` as its own Artifact (icon `report`, description
  "<product>'s status on <date>, from the repository.") with **no** `capabilities`, so the owner
  can share it from the page's Share menu, even by public link. Each report is a new Artifact —
  a snapshot of that day; the dashboard stays the live page. It contains the product's documents:
  remind the user of that before they share it outside their team.
- **A file** → generate it with `--standalone` and send the file (the chat's file tool, or its
  path). It opens offline; links to documents point to the repository on GitHub when there is a
  remote, otherwise to the files next to it.

Then say in two lines what it covers (the date, the stage, stories done of total, open decisions)
and that it doesn't update itself: generate a new one to share a later state.
