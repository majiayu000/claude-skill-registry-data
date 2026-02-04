---
name: release-reports
description: |
  Generates weekly release cycle reports for the team.
  - preview: What's shipping (run Sunday after release train)
  - retro: What happened (run Tuesday after prod stabilizes)
---

# Release Reports Skill

Generate reports for weekly release cycles.

## Available Actions

| Action | Description |
|--------|-------------|
| `preview` | Release preview - what's shipping, risk flags |
| `retro` | Release retro - what happened, hotfixes, trends |

## Usage

```bash
python {baseDir}/skills/release-reports/scripts/release_reports.py --action <ACTION> [OPTIONS]
```

### Options

- `--action` (required): `preview` or `retro`
- `--days N`: Days to look back for release trains (default: 30)

### Examples

```bash
# Sunday evening after release train is merged
python {baseDir}/skills/release-reports/scripts/release_reports.py --action preview

# Tuesday morning after prod is stable
python {baseDir}/skills/release-reports/scripts/release_reports.py --action retro
```

## Report Details

### Preview Report

Run after the develop → staging PR is merged (Sunday).

Shows:
- Release train PR details
- All feature PRs in this release
- Risk flags: large PRs (500+ lines), quick approvals
- Hotfixes from previous cycle that need backmerge
- Monday QA focus areas
- Release notes data for AI generation

#### Release Notes Generation

The preview report outputs structured PR data in `<release-notes-data>` tags. When you see this data:

1. Generate polished, user-facing release notes
2. Rewrite each PR title as a clear one-line summary focusing on user impact
3. Group items into these categories (skip empty ones):
   - **What's New** - New features and capabilities
   - **Bug Fixes** - Problems that were resolved
   - **Improvements** - Enhancements to existing functionality
4. Do NOT include PR links (this is for external sharing)
5. Use professional, concise language

Example output:
```
## Release Notes

### What's New
- Users can now export reports in PDF format
- Added dark mode support across all pages

### Bug Fixes
- Fixed crash when loading large datasets
- Resolved timezone display issues in reports

### Improvements
- Improved search performance by 40%
- Streamlined onboarding flow
```

### Retro Report

Run after production is stable (Tuesday).

Shows:
- Release timeline (staging date, prod date)
- Outcome (clean release or hotfixes required)
- What shipped (PRs, contributors, lines)
- Hotfixes during QA with backmerge status
- Trend of last 4 releases

## Branch Model

| PR Type | Base | Head | Description |
|---------|------|------|-------------|
| Feature | develop | feature/* | Normal development |
| Release train | staging | develop | Weekly release |
| Hotfix | staging | fix/* | Direct fix during QA |
| Promotion | release | staging | Push to production |
| Backmerge | develop | staging | Sync hotfix back |

## Output

Reports include emoji indicators for quick scanning:
- ✅ Clean / Good
- ⚠️ Needs attention
- ❌ Action required
