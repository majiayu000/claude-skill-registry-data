---
name: qa-test-cases
section: interactive
description: "Executes human-written test cases the user wrote in the AUDITED REPO (project-local test_cases.md, auto-detected at audit start). Falls back to the plugin's shipped test-cases/{appName}.md."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
selfSkip: "if no project-local test_cases.md is found in the audited repo AND no {plugin-root}/test-cases/{appName}.md exists"
---
## Two roots — read project-local FIRST

The plugin's CODE lives in the cache; the user's DATA (config, test cases, output) lives in the repo being audited. Resolve both:

- `{audit-root}` = the repository being audited = the current working directory (`process.cwd()` for scripts / the "Primary working directory" the orchestrator is given). This is where the app's own `.claude/automation.config.json`, `.tmp/`, and **test cases** live. It is NOT the plugin cache.
- `{plugin-root}` = the cached plugin install (skills + scripts only).

🚨 The same anchor the plugin WRITES `.tmp/` and `.claude/` to (`{audit-root}`) is the anchor it READS test cases from. If the plugin can write there, it can read there.

## Where test cases come from (first found wins)

1. `{audit-root}/test_cases.md`              ← project-local, repo root (PRIMARY — the user writes this before auditing)
2. `{audit-root}/.claude/qa-tests/*.md`      ← project-local, tidy multi-file variant
3. `{plugin-root}/test-cases/{appName}.md`   ← shipped fallback (legacy)

**Auto-detect:** glob the three locations above at audit start.
**Self-skip:** if NONE exist → record `skipped` (reason: "no test_cases.md in audited repo") and continue. Missing file is normal, never an error.

## Parse
- Split the file on headings: `/\n(?=#{2,3}\s)/`. Each `##` / `###` section = one test case. Title = heading text.
- `route:` line anywhere in the section → the page this case runs on. If `route` does not match `cell.route`, skip this case for this cell.
- `app:` line (optional) → if present and != `resolvedConfig.app.name`, skip the case.
- Steps = lines starting with `\d+\.` / `-` / `*`.

## Execute (up to 10 steps per case, try/catch each)
- `navigate|go to|visit {dest}` → `browser_navigate(dest or baseUrl+dest)`
- `click "{target}"` → click the element matching text/selector `{target}`
- `type "{text}" in {selector}` → fill `{selector}` with `{text}`
- `verify {selector} is visible` → fail if not visible
- `verify text "{expected}" (is visible)` / `verify {selector} (contains|has text) "{expected}"` → fail if `innerText` does not include `{expected}`
- Wait 300ms between steps

If a step fails → `testCaseFailed` (high): `"Custom test case \"{title}\" failed at step: \"{failedStep}\""`
If all steps pass → record the case as passed (no finding).

## Issues
| issueType | severity | description |
|---|---|---|
| testCaseFailed | high | "Custom test case \"{title}\" failed at step: \"{failedStep}\"" |
