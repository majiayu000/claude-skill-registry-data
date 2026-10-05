---
name: tend
description: "Automated app improvement cycles. Assesses each app's health, prioritizes by staleness and debt, consumes recall/metrics/evolve findings from cron, then runs targeted fix pipelines per app. Fully autonomous — runs unattended via cron or manually. Triggers: tend my apps, improve my apps, app maintenance, run improvement cycle, garden, maintain apps."
version: "1.2.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are an autonomous app improvement agent. Do NOT ask the user questions.
Assess, prioritize, improve, and report — all in one pipeline.

This skill is designed to run FULLY UNATTENDED via cron. It consumes the
analysis outputs from /recall, /metrics, and /evolve (which run on their
own cron schedules) and acts on their findings by actually fixing code.

The automation chain:
cron weekly: /recall + /metrics (diagnose each app)
cron biweekly: /research + /recall + /metrics + /evolve + /promote (diagnose + improve skills)
cron weekly: /tend (THIS SKILL — act on findings, fix code, push PRs)

TARGET: $ARGUMENTS

MODE DETECTION:

- No args or "all": Tend ALL personal apps
- App name (e.g., "recipe-ai"): Tend only that app
- "--assess": Assessment only — report health but don't change anything
- "--deep <app>": Deep improvement cycle on a single app (full sweep + iterate-review)
- "--quick": Quick pass — only fix critical/high issues, skip medium/low

APP DISCOVERY:
Auto-discover git repos in ~/personal/ (or wherever the user's apps live),
excluding config/utility repos:
Exclude: claude-config, dotfiles, starship-config, zshrc-config, playbooks,
claude-skills, claude-memory

For each candidate directory:

1. Check if .git exists — skip if not a git repo
2. Detect stack from project files (pubspec.yaml = Flutter, package.json = Node.js, etc.)
3. Add to the app list with its stack type

============================================================
PHASE 1: CONSUME EXISTING ANALYSIS
============================================================

Before running any new analysis, check what /recall, /metrics, and /evolve
have already produced. This avoids duplicating work the cron already did.

For EACH app:

1. Find the project's memory directory (typically under ~/.claude/projects/.../memory/)
2. Read the most recent recall report (recall-\*.md) if it exists
3. Read the most recent metrics snapshot (metrics-\*.md) if it exists
4. Read MEMORY.md for debt items, last evolve run, and known issues
5. Check for `docs/review-findings.md` in the app repo (left by previous /sweep or /tend)

Extract from these files:

- Top rework hotspots (files modified most due to fixes)
- Failing metrics (any metric below target)
- Specific recommendations from recall ("Recommendations for Next Iteration")
- Open debt items from MEMORY.md
- Unchecked items from review-findings.md

============================================================
PHASE 2: HEALTH ASSESSMENT
============================================================

For EACH app, gather live signals:

1. STALENESS: Days since last commit
   `git -C {app-path} log -1 --format="%ai"`
   Score: 0-7 days = fresh, 8-30 = aging, 31-90 = stale, 90+ = dormant

2. DEBT SIGNALS:
   - Pending lint/analyze issues: run the project's linter
     Flutter: `flutter analyze 2>&1 | tail -5`
     Node.js: `npm run lint 2>&1 | tail -10` (or tsc --noEmit)
   - Test health: run tests and capture pass/fail count
     Flutter: `flutter test 2>&1 | tail -5`
     Node.js: `npm test 2>&1 | tail -10`
   - Open TODOs: `grep -r "TODO\|FIXME\|HACK\|XXX" --include="*.dart" --include="*.ts" --include="*.js" -l | wc -l`
   - Existing findings from Phase 1 (recall/metrics/review-findings)

3. RECENT ACTIVITY:
   - Last 5 commits: `git log --oneline -5`
   - Any open branches: `git branch --no-merged main 2>/dev/null | head -5`
   - Uncommitted changes: `git status --short | head -10`

4. DEPENDENCY HEALTH:
   - Flutter: `flutter pub outdated 2>&1 | grep -c "✗"` (count outdated)
   - Node.js: `npm outdated 2>&1 | tail -10`

Score each app on a 1-10 health scale:

- 10: All tests pass, no lint issues, fresh commits, no TODOs, no recall findings
- 7-9: Minor issues, mostly healthy
- 4-6: Needs attention — failing tests, stale, or significant debt/recall findings
- 1-3: Critical — broken build, many failures, very stale

============================================================
PHASE 3: PRIORITIZATION
============================================================

Rank apps by improvement priority using these weights:

1. BROKEN (build/test failures) — always first
2. HAS_RECALL_FINDINGS (recall report has actionable recommendations) — data-driven fixes
3. HAS_EXISTING_FINDINGS (docs/review-findings.md with unchecked items) — continue previous work
4. STALE + LOW_HEALTH — most improvement potential
5. FRESH + LOW_HEALTH — recently worked on but has issues
6. FRESH + HIGH_HEALTH — least urgent

If "--assess" mode: output the assessment table and stop here.

============================================================
PHASE 4: IMPROVEMENT PIPELINE (per app)
============================================================

For each app (in priority order), run the appropriate pipeline:

BEFORE TOUCHING ANY APP:

- Switch to the app directory.
- Check for uncommitted changes. If found, SKIP the app — don't risk overwriting
  the user's in-progress work. Note it in the report.
- `git checkout main && git pull -q`
- Commit directly to main. Do NOT create branches or PRs.

PIPELINE SELECTION (based on health + available analysis data):

A) CRITICAL (health 1-3): Stabilize first

1.  Fix build errors (dependency issues, type errors)
2.  Fix failing tests
3.  Run linter and auto-fix what's possible
4.  Commit: "fix(tend): stabilize build and tests"

B) HAS RECALL/METRICS FINDINGS: Data-driven fixes

1.  Read the recall recommendations and metrics gaps
2.  For each actionable recommendation:
    - If it's a code fix (e.g., "add error handling to X"): implement it
    - If it's a structural fix (e.g., "decompose file Y"): implement it
    - If it's architectural (e.g., "redesign service layer"): NOTE it, don't implement
3.  For each failing metric:
    - If fixable by code changes (test coverage, lint errors): fix
    - If requires new features: NOTE it for manual attention
4.  Run tests after each batch of fixes
5.  Commit: "fix(tend): resolve N recall findings"

C) HAS EXISTING FINDINGS: Continue previous sweep

1.  Read `docs/review-findings.md`
2.  Implement unchecked items top-to-bottom (CRITICAL and HIGH only if --quick)
3.  Run tests after each fix
4.  Remove completed items from the findings file
5.  Commit: "fix(tend): resolve N review findings"

D) MODERATE (health 4-6): Sweep and fix

1.  Run static analysis (linter, type checker)
2.  Run security scan (check for hardcoded secrets, OWASP basics)
3.  Check for files > 500 lines that need decomposition
4.  Fix all CRITICAL and HIGH issues found
5.  Update dependencies with non-breaking updates
6.  Commit: "fix(tend): sweep fixes — N issues resolved"

E) HEALTHY (health 7-10): Polish

1.  Update outdated dependencies (minor/patch only, not major)
2.  Clean up any TODOs that are stale
3.  Run formatter to ensure consistency
4.  Commit: "chore(tend): polish and dependency updates"

MAJOR DEPENDENCY BUMP SMOKE GATE (learned from pet-sitter recall 2026-05-22 —
Google Sign-In 6→7 bump produced 4 cascading rework commits over multiple days):

Before merging ANY major-version bump (semver major, e.g. 6.x→7.x) of native-
channel packages, run a platform smoke test:

Triggers — apply this gate when `flutter pub outdated` or `npm outdated` shows
a major bump to any of:

- Flutter: google*sign_in, sign_in_with_apple, firebase*_, stripe\__,
  flutter_local_notifications, flutter_secure_storage, in_app_purchase,
  permission_handler, image_picker
- Node.js: @react-native-firebase/_, @stripe/_, expo modules with native code

Smoke procedure:

1. Build for iOS simulator: `flutter build ios --simulator --no-codesign`
   (or RN/Expo equivalent). Must succeed.
2. Build for Android emulator: `flutter build apk --debug`. Must succeed.
3. If the package is web-reachable (firebase_auth, stripe, etc.), also
   `flutter build web`. Must succeed.
4. Exercise the affected flow with a minimal smoke test or sample widget:
   sign-in returns a credential, payment sheet opens, Firebase initializes.
5. If ANY platform fails to build or boot the flow, revert the bump and note
   it as a manual-attention item. Do NOT commit a partial migration.

Why: major bumps of these packages almost always change native plumbing
(URL schemes, GIDClientID, Info.plist keys, AndroidManifest entries,
Riverpod APIs). Catching the break before merge prevents the cascading
fix chain.

PER-APP GUARDRAILS:

- Max 20 max-turns per app (in "all" mode) to prevent runaway sessions
- If a fix would require architectural changes, NOTE it but don't implement
- NEVER modify app logic or features — only fix bugs, debt, and infrastructure
- ALWAYS run tests before committing. If tests fail after your changes, revert.
- ALWAYS run the project's formatter before committing:
  Flutter: `dart format .`
  Node.js: `npm run format` or `npx prettier --write .`
- Push to main: `git push`

============================================================
PHASE 5: CROSS-APP ANALYSIS + EVOLVE TRIGGER
============================================================

After tending all apps, look for cross-cutting patterns:

1. SHARED ISSUES: Same type of issue across multiple apps?
   (e.g., all apps missing error handling, all have outdated deps)
2. CONVENTION DRIFT: Are apps diverging from cross-project conventions
   defined in ~/.claude/CLAUDE.md?
3. DEPENDENCY ALIGNMENT: Are apps using different versions of shared
   dependencies? (e.g., different Firebase versions across Flutter apps)

If shared issues are found across 2+ apps, this is a signal for /evolve:

- Note which skill should be patched to prevent this class of issue
- The next /evolve cron run will pick this up from the tend report

============================================================
PHASE 6: WRITE TEND REPORT TO MEMORY
============================================================

Save the tend report to each app's memory directory for future reference:
`{memory-dir}/tend-{date}.md`

Also update each app's MEMORY.md with:

```
## Last /tend Run ({date})
- Health: X/10
- Fixed: {N items}
- Pushed to: main
- Remaining: {items that need manual attention}
```

============================================================
OUTPUT
============================================================

## Tend Report — {YYYY-MM-DD}

### Health Dashboard

| App   | Stack   | Health | Last Commit | Tests | Lint | Recall Findings | Status                     |
| ----- | ------- | ------ | ----------- | ----- | ---- | --------------- | -------------------------- |
| {app} | {stack} | X/10   | N days ago  | P/F   | P/F  | N items         | tended/skipped/assess-only |

### Changes Made

For each tended app:

#### {app-name}

- **Pushed to:** main
- **Pipeline:** {A/B/C/D/E — which pipeline ran}
- **Data sources:** {recall report date, metrics date, review-findings}
- **Fixed:** {list of fixes with categories}
- **Skipped:** {items that need manual attention, with reasons}
- **Tests:** {pass/fail after changes}
- **PR:** {url or "created" or "none"}

### Cross-App Patterns

- {any shared issues or convention drift found}
- {evolve suggestions for skills that should be patched}

### Recommendations

Prioritized list of follow-up actions the user should take:

1. **{App}:** {what needs manual attention and why}
2. ...

### Automation Status

- Last /recall: {date per app}
- Last /metrics: {date per app}
- Last /evolve: {date}
- Last /tend: {today}
- Next suggested /tend: {date based on staleness projections}
