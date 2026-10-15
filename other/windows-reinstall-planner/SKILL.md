---
name: windows-reinstall-planner
description: Prepare a metadata-only Windows software inventory and evidence-linked reinstall checklist without changing installed software. Use before replacing a computer or reinstalling Windows, or when organizing registered applications and unconfirmed shortcuts into a private review plan.
---

# Windows Reinstall Planner

Separate software evidence from reinstall decisions. An inventory is not a backup and does not authorize destructive maintenance.

## Workflow

1. Confirm the machine and private output location. Explain the limited collection scope before running it.
2. Read [collection and reporting boundaries](references/inventory-contract.md).
3. In Windows PowerShell 5.1, collect only the requested metadata:

       powershell.exe -NoProfile -File scripts/collect_software.ps1 -OutputPath inventory.json

   Use a new local filename in an existing directory. No elevation is required. From PowerShell 7, invoke Windows PowerShell as shown; unavailable adapters produce a partial-coverage report.
4. Build reports with Python 3.11 or newer:

       python scripts/build_reinstall_plan.py --input inventory.json --output-dir private-report

5. Review groups and uncertain duplicates. Keep unknown versions blank. Do not claim registrations prove an app still runs or reveal who originally installed it.
6. Let the user select Yes, No, Later, or Undecided in the generated CSV. Verify official publisher download links only for selected software, without downloading or installing anything.
7. Return the report locations, evidence counts, coverage gaps, and remaining decisions.

## Boundaries

The collector reads names, versions, publishers, package identifiers, and evidence types from uninstall registry entries, current-user Store packages, and Start-menu app listings. It excludes account access data, activation values, shortcut arguments, configuration contents, browser profiles, and broad drive scans.

Do not query `Win32_Product`, which can initiate installer repair checks. Do not install, uninstall, erase, format, restore, or export application settings. No background task or remote inventory is created.

Keep real inventories private, even when they contain no access data: software choices can identify a person or organization. Public examples must be fictional. Checklists and CSV choices are independent, not silently synchronized.

## Deliverables

- One evidence row per source record, with unique IDs.
- A conservatively grouped checklist linked to those IDs.
- A coverage report distinguishing records, display groups, and unknown runtime state.
- A reminder to verify separate file/settings backups before any later maintenance.

The report builder writes only new named reports and refuses to overwrite existing ones. It needs no third-party Python package.
