---
name: app-store-preflight
description: Audits an iOS, iPadOS, macOS, watchOS, tvOS or visionOS app against every App Store Review Guideline and App Store Connect submission requirement before it is sent to App Review. It checks the code, optionally drives App Store Connect in the browser (Claude in Chrome or Playwright MCP) to compare the listing with the app, marks every check pass or fail with evidence, verifies each failure, then fixes what can be fixed in code and documents the rest. Use when the user wants to submit an app to the App Store, asks whether an app will be rejected, wants an App Review or App Store Connect checklist, received an App Review rejection, or mentions App Store guidelines, privacy manifests, purpose strings, account deletion, Sign in with Apple, or in-app purchase review.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Workflow
  - Workflow(app-store-preflight:preflight)
  - Agent
  - Bash(python3 -I *)
  - Bash(git *)
  - Bash(mkdir -p *)
  - Bash(date *)
  - Bash(ls *)
  - Bash(xcodebuild *)
  - Bash(xcrun *)
---

# App Store Preflight

Run a pre-submission review of an Apple app the way App Review would: every guideline, every App Store Connect requirement, a pass or fail for each with evidence, then fixes.

The knowledge base is in `references/`. Every check in it quotes Apple's text word for word (App Review Guidelines, App Store Connect Help, App Review Help, developer documentation). Do not add requirements from memory. If a situation isn't covered by a check, say so instead of guessing.

`<skill>` below means this skill's base directory.

## 1. Find the project and confirm scope

1. The project root is the argument if one was given, otherwise the current working directory. It must contain an `.xcodeproj`, `.xcworkspace`, `Package.swift`, or an iOS folder of a React Native, Expo, Flutter or Capacitor app. If none is found, ask for the path.
2. Check the guidelines are current: `python3 -I <skill>/scripts/check_guidelines_version.py <skill>/source/app-review-guidelines.md`. If Apple's page has a newer "Last Updated" date, tell the user once (the bundled checks may lag behind) and continue.

## 2. Ask the setup questions (one AskUserQuestion call)

Skip any question the user already answered in their request.

- **Mode**: "Audit + fix (Recommended)": audit, then fix confirmed failures on a new git branch. "Audit only": report only, no changes.
- **App Store Connect**: "Claude in Chrome (Recommended)" / "Playwright MCP" / "Skip": the browser pass reads App Store Connect without changing anything and compares it with the app. Only offer the options whose tools are present (`mcp__claude-in-chrome__*`, `mcp__playwright__*`).
- **Simulator run**: "Static only (Recommended, faster)" / "Build and run in Simulator": builds the app, launches it, and walks the permission prompts, sign-in, settings and paywall. Walking those flows needs a UI driver: the [AXe](https://github.com/cameroncooke/AXe) CLI (`command -v axe`) or an Xcode/simulator MCP. Without one, it only launches the app and takes screenshots. If neither is installed, say so in the option description; don't install anything without asking. A walk from a fresh install uninstalls the app from the chosen Simulator first, which erases that copy's data. If `xcrun simctl listapps booted` shows the bundle ID installed, ask before allowing it and pass `allowReinstall` accordingly. Another session may be using that Simulator.
- **Thoroughness**: "Standard (Recommended)": one skeptic per failure. "Thorough": three skeptics per failure, kept only if a majority uphold it.

If App Store Connect was chosen, ask the user to make sure they are signed in to https://appstoreconnect.apple.com in that browser and to name the app as it appears there (needed when the account has several apps).

## 3. Prepare the run

```bash
RUN="<project>/.preflight/$(date +%Y%m%d-%H%M)"; mkdir -p "$RUN/verdicts" "$RUN/fixes" "$RUN/runtime"
python3 -I <skill>/scripts/scan_project.py "<project>" "$RUN/facts.json"
python3 -I <skill>/scripts/build_checks.py <skill>/references "$RUN/checks.json"
```

- If `.preflight/` is not in the project's `.gitignore`, offer to add it.
- Audit + fix mode in a git repo: if the working tree is clean, create the branch `app-store-preflight/fixes-<date>`. If it has uncommitted changes, ask whether to continue on the current branch or stop so they can commit first. Never commit or push without being asked.

## 4. Launch the workflow

Call Workflow with `name: "app-store-preflight:preflight"` (the plugin install). If that name is not found, use `scriptPath: "<skill>/workflow/preflight.js"` (the standalone install). Args:

```json
{ "projectRoot": "<abs project>", "runDir": "<abs RUN>", "skillDir": "<abs skill>",
  "mode": "fix" | "audit", "asc": "chrome" | "playwright" | "none", "ascApp": "<name or null>",
  "runtime": true | false, "allowReinstall": true | false, "verifyVotes": 1 | 3,
  "only": ["guidelines/", "asc/privacy-manifests.md"] }
```

`only` is optional: leave it out to cover everything, or pass reference-file path prefixes (as a JSON array, not a string) when the user asks for a narrower check, e.g. only privacy. After profiling, the workflow's planner (`scripts/plan_checks.py`) skips the checks whose Apple-stated scope (`**Requires:**` in the references) needs a feature the profile has ruled out. Each skipped check is recorded as ➖ NA with the reason, and only the rest go to agents. Tell the user it runs in the background, and that `/workflows` shows live progress.

What the workflow does: profiles the app (which features exist, so irrelevant guidelines become N/A) → audits every check batch against the code, with a skeptic trying to refute each failure as soon as its batch finishes → reads App Store Connect in parallel (read-only) and compares it with the app → optionally runs the app in the Simulator → in fix mode, applies fixes one fixer at a time, rebuilds, and has an independent agent re-verify every fix.

If the Workflow tool isn't available (another agent harness), run the same phases yourself with subagents or sequentially, following the prompts in `workflow/preflight.js`, and write the same files to `$RUN`.

## 5. When it finishes

1. If the App Store Connect pass returned `needsLogin`, ask the user to sign in, then relaunch with the same args and `resumeFromRunId`. Finished agents are reused from cache.
2. Render the report: `python3 -I <skill>/scripts/render_report.py "$RUN" "$RUN/checks.json" <skill>/source/app-review-guidelines.md`
3. Open `$RUN/PREFLIGHT_REPORT.md` and give the user: the status line; the count of each verdict; every remaining ❌ with a one-line fix; what was 🔧 fixed and on which branch; the ✋ questions only they can answer. Link the report path.
4. **App Store Connect fixes**: for each confirmed App Store Connect failure whose `fixPlan` names an exact field and value, list the proposed changes and ask for approval (AskUserQuestion, multi-select). Apply only the approved ones in the browser, one field at a time, and re-read the page to confirm. Never click "Add for Review", "Submit for Review" or "Submit to App Review", never change prices, agreements, tax or banking, and never delete anything. Submitting stays with the user.
5. Point the user to the "Draft notes for App Review" section of the report. Clear review notes and a working demo account prevent many guideline 2.1 rejections.

## Verdicts

| | Verdict | Meaning |
|---|---|---|
| ✅ | PASS | Requirement met; evidence cited |
| ❌ | FAIL | Requirement violated or a required item is missing: likely rejection |
| ⚠️ | WARN | Probable problem, or "should" advice not followed |
| 🌐 | ASC | Only App Store Connect can settle it (run with the browser pass, or check by hand) |
| ✋ | MANUAL | Only the developer can confirm (legal, business, content facts) |
| 🔧 | FIXED | Fixed by preflight and independently re-verified |
| ➖ | NA | Does not apply to this app |

## References

- `references/guidelines/*.md`: every App Review Guideline (sections 1 to 5, plus Introduction, Before You Submit and After You Submit), verbatim, each turned into pass/fail checks.
- `references/asc/*.md`: App Store Connect and platform requirements: privacy manifests and required-reason APIs, App Privacy details and App Tracking Transparency, product page metadata and screenshot specifications, submission, age rating, export compliance and DSA, in-app purchases and subscriptions, accounts, permissions and technical requirements, App Review Help.
- `references/asc-browser-audit.md`: page map and read-only procedure for the App Store Connect browser pass.
- `references/data/*.json`: machine-readable lists (required-reason API symbols, SDKs that need privacy manifests, purpose-string keys) used by the scanner.
- `source/`: the raw scraped Apple texts that every quote is checked against.

## Limits

- This skill lowers rejection risk; it does not guarantee approval. App Review decides.
- Checks marked ✋ need the developer's honest answer. Do not mark them PASS on their behalf.
- Guidelines change. `scripts/check_guidelines_version.py` warns when Apple's page is newer than the bundled copy, and `scripts/update_sources.sh` re-scrapes it.
