---
name: orbit-release-gate
description: Day-of-release sequence for a WordPress plugin. Runs 4 sequential gates — preflight (gauntlet-dry-run), release metadata check (header/readme.txt/version parity), full release-mode gauntlet, and evidence-pack generation. Outputs one HTML report bundle = the proof you actually shipped quality. Use when the user says "release this", "ship v2.0", "release gate", "WP.org submission", or has a `git tag` ready to go.
argument-hint: --version v2.3.0 (or detect from git tag)
---

# 🪐 orbit-release-gate — Day-of-release sequence

Four gates. One exit code. One evidence pack. Run this **before** `git tag`, **before** the WP.org submit, **before** the email goes out.

---

## The 4 gates (run in order — fail fast)

```bash
cd ~/plugins/my-plugin

# Gate 1 — Preflight (5 sec) — catches "command not found" before wasting 60 min
bash ~/Claude/orbit/scripts/gauntlet-dry-run.sh

# Gate 2 — Release metadata (30 sec) — header, readme, version parity, license
bash ~/Claude/orbit/scripts/check-plugin-header.sh .
bash ~/Claude/orbit/scripts/check-readme-txt.sh .
bash ~/Claude/orbit/scripts/check-version-parity.sh . v2.3.0
bash ~/Claude/orbit/scripts/check-license.sh .

# Gate 3 — Full release-mode gauntlet (45-60 min)
bash ~/Claude/orbit/scripts/gauntlet.sh --plugin . --mode release

# Gate 4 — Evidence pack
python3 ~/Claude/orbit/scripts/generate-reports-index.py \
  --title "Release v2.3.0 — $(date +%Y-%m-%d)"
open reports/index.html
```

---

## What "release mode" adds over "full"

| Check | Why it matters at release |
|---|---|
| **WP.org plugin-check** | The official plugin-team submission tool. Catches anything that would get auto-flagged at upload. |
| **Live CVE correlation** | Cross-references the plugin's PHP signatures against this week's WP CVE feed. Flags emergency patches. |
| **Ownership-transfer detection** | Checks for the April 2026 attack pattern — sudden wp.org slug owner change + obfuscated payload. |
| **Stable-tag check** | `Stable tag:` in readme.txt must match the version you're tagging. WP.org rejects on mismatch. |
| **POT freshness** | Translation file is up-to-date with current strings. Stale POT = bad UX for non-English users. |
| **Zip hygiene strict** | No `.git/`, `.cursor/`, `.github/`, source maps, or composer dev deps in the release zip. |

---

## Decision rules

| Outcome | Action |
|---|---|
| All 4 gates exit 0 | ✅ Tag + push + WP.org submit. |
| Gate 1 fails | Tool missing → `/orbit-install`, retry. |
| Gate 2 fails | Metadata problem — fix and re-run from Gate 2. Don't run Gate 3 yet. |
| Gate 3 has Critical/High | Block release. Drill into the failing skill. |
| Gate 3 only Medium/Low | Document in release notes ("known issues"), proceed at your discretion. |
| Gate 4 evidence pack opens cleanly | You have proof. Save the HTML for support / customer asks. |

---

## What goes in the evidence pack

`reports/index.html` after Gate 4:

- ✅ Top severity bar — Critical/High count for the whole release
- ✅ Tab per audit (Security, Perf, DB, A11y, Standards, Code Quality)
- ✅ Playwright HTML report — pass/fail per test, screenshots of failures
- ✅ Lighthouse score
- ✅ DB profile (query counts on every URL)
- ✅ Bundle weight diff vs previous release
- ✅ Competitor comparison
- ✅ PM UX report (typos, guided-UX score, label findings)

This is the file you send when a customer or your manager asks *"prove the release was QA'd."*

---

## Common failures and fixes

### `Stable tag mismatch — readme.txt says 2.2.0, you're tagging v2.3.0`
Edit `readme.txt`:
```
Stable tag: 2.3.0
```
Re-run Gate 2.

### `POT file out of date — 14 new strings since last regen`
```bash
wp i18n make-pot . languages/my-plugin.pot --slug=my-plugin
git add languages/my-plugin.pot && git commit -m "chore: regen POT for v2.3.0"
```

### `Plugin-check failure: no Tested up to`
Plugin header missing `Tested up to: 6.5`. Add it and bump on every WP minor release.

### `Live CVE match — pattern: WP CVE-2026-XXXX`
Run `/orbit-cve-check` on the specific pattern. If exploitable in your code → emergency patch. If not → document the analysis in release notes.

### `Ownership-transfer flag`
Check the wordpress.org/plugins/<your-slug>/ owner field and your last commit author. If both match → false positive (rare). If mismatch → security review.

### `Gate 3 hangs on AI skill audits`
The gauntlet's Step 11 spawns 6 Claude Code processes in parallel. If your machine is slow, that's the bottleneck. Check `reports/skill-audits/*.md` — any with content but no closing `# Summary` section is still running. Wait or kill + re-run that single skill.

---

## Auto-detect version from git

```bash
VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0-dev")
bash ~/Claude/orbit/scripts/check-version-parity.sh . "$VERSION"
```

The plugin header `Version:`, `readme.txt` `Stable tag:`, and the git tag must all be the same string. The script enforces this.

---

## Post-release checklist (after Gate 4 passes)

1. `git tag v2.3.0 && git push --tags`
2. Build the zip: `bash scripts/check-zip-hygiene.sh .` then `wp dist-archive .`
3. Upload to WP.org via SVN (or use the GitHub Action if configured)
4. Update changelog, release notes, blog post
5. Save `reports/index.html` to your release archive
6. Schedule `/orbit-cve-check` weekly via cron (`docs/24-use-cases.md` R3)

---

## CI version of the same gate

`.github/workflows/release.yml`:
```yaml
on:
  push:
    tags: [v*]
jobs:
  release-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bash ~/Claude/orbit/install.sh --skills-only
      - run: bash ~/Claude/orbit/scripts/gauntlet.sh --plugin . --mode release
      - if: always()
        uses: actions/upload-artifact@v4
        with: { name: release-evidence, path: reports/ }
```

Full template: `docs/15-ci-cd.md`.

---

## Hard rule

**Never tag a release with any unaddressed Critical or High finding.** Either fix it, document a conscious dev sign-off in the report, or roll back the version bump. Shipping with knowingly-broken code is how plugins get 1-star bombs and WP.org suspensions.
