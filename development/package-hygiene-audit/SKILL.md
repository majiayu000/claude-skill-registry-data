---
name: package-hygiene-audit
description: Audit a local release folder for app bundles, packaged archives, release notes, and screenshots before you ship from the Mac. Use when Codex needs a deterministic packaging check instead of a manual Finder scavenger hunt.
---

# Package Hygiene Audit

Use this skill when the user wants a deterministic local audit of a release folder before shipping from macOS.

Default product shapes:

- a local helper that scans a release folder and emits a ship-readiness report in markdown, prompt, or JSON
- a menu-bar audit panel that shows the current build artifact, notes, screenshot status, and the next packaging fix to make

## Quick Start

1. Point the skill at the release folder you actually plan to ship from.
2. Run `python3 scripts/package_hygiene_audit.py doctor --release-dir /path/to/release`.
3. Run `python3 scripts/package_hygiene_audit.py audit --release-dir /path/to/release --format markdown`.
4. Add `--notes-path /path/to/notes` when release notes live outside the release folder.
5. Add `--screenshot-dir /path/to/screenshots` when screenshots live elsewhere.
6. Set `--expect-app-name "My App"` when artifact naming needs to match a product name.
7. Use `--minimum-screenshots N` to match the current ship lane.
8. Add `--require-packaged-archive` when `.dmg`, `.zip`, or `.pkg` output is non-negotiable.
9. Return one of:
   - `release-audit`
   - `ship-readiness-summary`
   - `blocking-issues-list`

## Accepted Inputs

- a release folder with `.app`, `.dmg`, `.zip`, `.pkg`, `.tar.gz`, or `.tgz` outputs
- release note files inside the release folder or at an explicit `--notes-path`
- screenshots inside the release folder or at an explicit `--screenshot-dir`
- an expected product name when packaging labels matter
- the screenshot count required for this ship lane

## Output Artifact

Primary artifacts:

- `release-audit`
- `ship-readiness-summary`
- `blocking-issues-list`

Default `release-audit` sections:

- summary
- checks
- blocking issues
- warnings
- discovered artifacts
- next actions

## Workflow

### Audit The Real Folder

- Work from the release folder the user will actually ship from.
- Keep the check local-first and deterministic.
- Report exactly what is present or missing. Do not imply notes, screenshots, or archives exist when the folder does not contain them.

### Use The Helper First

- Start with `doctor` to confirm the release folder and search roots are correct.
- Use `audit` when the user needs a shareable report or prompt-sized summary.
- Prefer explicit `--notes-path` and `--screenshot-dir` inputs over guessing when the release structure is split across folders.
- Use `--expect-app-name` when naming hygiene matters for a product launch or handoff.

### Keep The Packaging Boundary Honest

- This skill audits local packaging inputs only.
- Do not invent notarization, App Store Connect, or release-hosting state.
- If the user needs signing or store-upload help, say that this audit only covers the local folder and the visible files inside it.

### Menu Bar Product Shape

- Prefer a compact status-item or menu-bar popover.
- Show one summary line first, then blocking items.
- Keep the main surface small:
  - current release folder
  - artifact counts
  - blocking issues
  - warnings
  - next action row for reveal, copy summary, or export

### Guardrails

- Do not pretend missing packaging files are optional unless the user explicitly relaxes that rule.
- Keep screenshots, notes, and artifact paths visible in the output so the user can verify them quickly.
- Stay within local file, folder, and naming checks. No invented cloud release APIs.

## Example Prompts

- `Use $package-hygiene-audit to audit this release folder and tell me if the DMG, notes, and screenshots are ready to ship.`
- `Use $package-hygiene-audit to scan my local release folder, require a packaged archive, and return a markdown report I can paste into the release thread.`
- `Use $package-hygiene-audit to build a compact Mac menu-bar utility that checks release bundles, screenshots, and notes before publish.`

## Resources

- `scripts/package_hygiene_audit.py`: deterministic local release-folder audit helper
- `references/audit-contract.md`: audit inputs, checks, and output contract
- `prototype/`: SwiftUI starter files for a compact menu-bar audit surface
