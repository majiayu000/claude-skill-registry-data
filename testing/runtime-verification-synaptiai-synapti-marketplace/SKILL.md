---
name: runtime-verification
description: Verifies implementation works at runtime by discovering and executing dev server startup, API smoke tests, E2E tests, and browser checks. Use after quality checks pass (lint, test, typecheck) to confirm the code actually runs. Use when validating acceptance criteria, running Playwright or Cypress suites, or smoke-testing endpoints before PR creation.
allowed-tools: Bash, Read, Glob, Grep, WebFetch
context: fork
agent: Explore
---

# Runtime Verification

This skill verifies that an implementation actually works at runtime, not just that it compiles and passes lint/tests.

## Purpose

Quality checks (lint, test, typecheck) answer "does it compile?" This skill answers "does it work?" by:
- Starting dev servers and verifying they respond
- Running smoke tests against new/modified endpoints
- Executing E2E test suites if available
- Visually verifying UI changes in the browser
- Verifying acceptance criteria programmatically

## Read Timeout Settings

Before running verifications, read timeout configuration (local > project > user > defaults):

```bash
DEV_STARTUP_TIMEOUT=$(jq -r '.timeouts.devServerStartup // empty' .claude/settings.gh-workflow.local.json 2>/dev/null)
[ -z "$DEV_STARTUP_TIMEOUT" ] && DEV_STARTUP_TIMEOUT=$(jq -r '.timeouts.devServerStartup // empty' .claude/settings.gh-workflow.json 2>/dev/null)
[ -z "$DEV_STARTUP_TIMEOUT" ] && DEV_STARTUP_TIMEOUT=$(jq -r '.timeouts.devServerStartup // empty' "$HOME/.claude/settings.gh-workflow.json" 2>/dev/null)
[ -z "$DEV_STARTUP_TIMEOUT" ] && DEV_STARTUP_TIMEOUT="30"

E2E_TIMEOUT=$(jq -r '.timeouts.e2eTest // empty' .claude/settings.gh-workflow.local.json 2>/dev/null)
[ -z "$E2E_TIMEOUT" ] && E2E_TIMEOUT=$(jq -r '.timeouts.e2eTest // empty' .claude/settings.gh-workflow.json 2>/dev/null)
[ -z "$E2E_TIMEOUT" ] && E2E_TIMEOUT=$(jq -r '.timeouts.e2eTest // empty' "$HOME/.claude/settings.gh-workflow.json" 2>/dev/null)
[ -z "$E2E_TIMEOUT" ] && E2E_TIMEOUT="120"

VERIFICATION_TIMEOUT=$(jq -r '.timeouts.verificationScript // empty' .claude/settings.gh-workflow.local.json 2>/dev/null)
[ -z "$VERIFICATION_TIMEOUT" ] && VERIFICATION_TIMEOUT=$(jq -r '.timeouts.verificationScript // empty' .claude/settings.gh-workflow.json 2>/dev/null)
[ -z "$VERIFICATION_TIMEOUT" ] && VERIFICATION_TIMEOUT=$(jq -r '.timeouts.verificationScript // empty' "$HOME/.claude/settings.gh-workflow.json" 2>/dev/null)
[ -z "$VERIFICATION_TIMEOUT" ] && VERIFICATION_TIMEOUT="180"
```

## Quick Verification Fast Path

Before running the full discovery process, check for an existing verification script. Many mature projects already wire everything up in one command — if one exists, run it and skip the rest.

```bash
# Check for dedicated verification scripts
ls verify.sh test-e2e.sh smoke-test.sh scripts/verify* 2>/dev/null

# Check Makefile for verify/e2e/smoke targets
grep -E "^(verify|e2e|smoke|integration-test):" Makefile 2>/dev/null
```

If found, run it with a timeout:
```bash
timeout $VERIFICATION_TIMEOUT ./verify.sh 2>&1  # or make verify, etc.
```

If it passes, skip to Output Format. If it fails or no script exists, continue with full discovery.

## Discovery Process

### Step 1: Check CLAUDE.md for Dev/Test Commands

Search project instructions for any development or verification commands:

```bash
grep -iE "(dev server|npm run|yarn |pnpm |python.*run|go run|cargo run|docker.compose|make\s+\w+|uvicorn|gunicorn|flask run)" .claude/CLAUDE.md CLAUDE.md 2>/dev/null
grep -iE "(verify|e2e|smoke|integration|acceptance)" .claude/CLAUDE.md CLAUDE.md 2>/dev/null
```

### Step 2: Check for E2E Test Frameworks

```bash
# Playwright
ls playwright.config.* 2>/dev/null
grep -l "playwright" package.json 2>/dev/null

# Cypress
ls cypress.config.* cypress/ 2>/dev/null

# Selenium
grep -l "selenium" requirements.txt pyproject.toml 2>/dev/null
```

### Step 3: Discover Dev Server Commands

```bash
# Node.js
grep -E '"(dev|start|serve)"' package.json 2>/dev/null

# Makefile
grep -E "^(dev|serve|run|start|up):" Makefile 2>/dev/null

# Docker
ls docker-compose.yml docker-compose.yaml compose.yml compose.yaml 2>/dev/null

# Python
ls manage.py 2>/dev/null && echo "django: python manage.py runserver"
grep -E "(uvicorn|gunicorn|flask)" pyproject.toml requirements.txt 2>/dev/null

# Go
ls main.go cmd/*/main.go 2>/dev/null && echo "go: go run ."

# Monorepo
ls turbo.json 2>/dev/null && echo "turbo: check turbo.json for dev pipeline"
```

### Step 4: Discover Port Configuration

```bash
# Check for port configuration
grep -rE "PORT|:3000|:8080|:5173|:4000|:8000|:3001" package.json .env .env.local .env.development 2>/dev/null | head -10

# Common framework defaults:
# Vite/SvelteKit=5173, Next.js/Rails=3000, CRA=3000
# Django=8000, Flask=5000, Go=8080, Spring=8080
```

### Step 5: Check for Health/Readiness Endpoints

```bash
grep -rn "health\|healthz\|ready\|alive\|ping" --include="*.ts" --include="*.py" --include="*.go" --include="*.java" . 2>/dev/null | head -10
```

## Runtime Verification Protocol

### Step 1: Service Startup (if applicable)

If a dev server command is discovered:

1. Start server in background with PID tracking:
   ```bash
   {dev_cmd} &
   DEV_PID=$!
   ```

2. Wait for ready signal — try common health paths, fall back to port check:
   ```bash
   PORT={detected_port:-3000}
   for i in $(seq 1 $DEV_STARTUP_TIMEOUT); do
     curl -sf http://localhost:$PORT/ > /dev/null 2>&1 && break
     curl -sf http://localhost:$PORT/health > /dev/null 2>&1 && break
     curl -sf http://localhost:$PORT/healthz > /dev/null 2>&1 && break
     curl -sf http://localhost:$PORT/api/health > /dev/null 2>&1 && break
     nc -z localhost $PORT 2>/dev/null && break
     sleep 1
   done
   ```

3. If server doesn't start within ${DEV_STARTUP_TIMEOUT}s (default: 30s, configurable via `.timeouts.devServerStartup`), report as verification failure with the last few lines of output

### Step 2: Smoke Tests

For each new/modified API endpoint in the diff:

**Detecting endpoints from the diff:**
```bash
# Find route definitions in changed files
git diff origin/$DEFAULT_BRANCH..HEAD --name-only | xargs grep -nE \
  "@(app|router)\.(get|post|put|patch|delete)|app\.(get|post|put|use)|router\.(get|post)|@(Get|Post|Put|Delete|Patch)Mapping|@api_view|path\(" \
  2>/dev/null
```

For each discovered endpoint:
1. Send a basic request and verify non-error response
2. Verify response structure matches expected schema
3. Test with invalid input and verify error handling

### Step 3: E2E Tests (if framework detected)

Run discovered E2E test command with a timeout to prevent hanging:
```bash
timeout $E2E_TIMEOUT npx playwright test 2>&1  # or
timeout $E2E_TIMEOUT npx cypress run 2>&1       # or
timeout $E2E_TIMEOUT pytest tests/e2e/ 2>&1     # etc.
```

If the full suite is too large, run only tests related to changed files:
```bash
# Playwright: run specific test file
timeout $E2E_TIMEOUT npx playwright test tests/e2e/changed-feature.spec.ts 2>&1

# Pytest: run tests matching changed module names
timeout $E2E_TIMEOUT pytest tests/e2e/ -k "changed_module" 2>&1
```

### Step 4: Visual Verification (if UI changes detected)

When the diff includes frontend changes (templates, components, styles, layouts), visually verify the running application in a browser. This catches rendering issues, broken layouts, and visual regressions that automated tests often miss.

**Detecting UI changes in the diff:**
```bash
git diff origin/$DEFAULT_BRANCH..HEAD --name-only | grep -iE "\.(tsx|jsx|vue|svelte|html|css|scss|sass|less|ejs|hbs|pug)$"
```

If UI files changed and the dev server is running:

#### Option A: Browser tool (preferred)

If a browser MCP tool is available (e.g., Puppeteer, Playwright MCP), use it to:

1. Navigate to the affected pages/routes
2. Take screenshots for evidence
3. Check for console errors
4. Verify interactive elements respond to clicks

```
Navigate to http://localhost:{PORT}{route}
Take a screenshot
Check the browser console for errors
```

#### Option B: Playwright screenshot script

If no browser MCP but Playwright is installed, take automated screenshots:

```bash
# Quick screenshot of affected pages
npx playwright test --project=chromium -g "screenshot" 2>&1 || \
npx playwright screenshot http://localhost:$PORT{route} screenshot-{route-name}.png 2>&1
```

#### Option C: WebFetch + curl fallback

If no browser automation is available, fetch the page HTML and verify structure:

```bash
# Fetch rendered HTML and check for expected elements
curl -s http://localhost:$PORT{route} | grep -E "<(main|section|div|h1)" | head -20
```

Use the **WebFetch tool** for richer inspection — it renders JavaScript and returns the page content, which is useful for SPAs where curl only sees a shell `<div id="root">`.

#### What to verify visually

| Check | How | Evidence |
|-------|-----|----------|
| Page loads without errors | Browser console or curl status | Screenshot or 200 OK |
| Layout isn't broken | Screenshot or HTML structure check | Screenshot file path |
| New UI elements are present | Look for expected elements in DOM | Element found / not found |
| No console errors or warnings | Browser console output | Clean console or error list |
| Interactive elements work | Click/interact via browser tool | Before/after screenshots |

Record results in the Visual Verification section of the output.

### Step 5: Acceptance Criteria Verification

For each acceptance criterion from the linked issue:
1. Identify how to verify it (API call, UI check, CLI command)
2. Execute the verification
3. Record pass/fail with evidence

### Step 6: Cleanup

Kill any background services started in Step 1:
```bash
kill $DEV_PID 2>/dev/null
# For Docker Compose
docker compose down 2>/dev/null
```

## Output Format

```markdown
## Runtime Verification Results

### Service Status
| Service | Command | Status | Notes |
|---------|---------|--------|-------|
| Dev server | npm run dev | Started on :3000 | Healthy after 3s |

### Smoke Tests
| Endpoint/Feature | Test | Status | Evidence |
|-----------------|------|--------|----------|
| POST /api/users | Create user with valid data | Pass | 201 Created |
| POST /api/users | Create user with invalid email | Pass | 400 Bad Request |

### E2E Tests
| Suite | Status | Passed | Failed |
|-------|--------|--------|--------|
| Playwright | Pass | 12 | 0 |

### Visual Verification
| Page/Route | Check | Status | Evidence |
|------------|-------|--------|----------|
| /dashboard | Page loads | Pass | Screenshot: screenshot-dashboard.png |
| /dashboard | No console errors | Pass | Clean console |
| /users/new | Form renders correctly | Pass | All fields present |

### Acceptance Criteria
| Criterion | Verification Method | Status | Evidence |
|-----------|-------------------|--------|----------|
| Users can filter by date | GET /api/users?date=2024-01-01 | Pass | Returns filtered results |

### Not Verified (Requires Manual Check)
| Item | Reason |
|------|--------|
| Visual styling matches mockup | No browser automation available |
```

## Graceful Degradation

| Missing Capability | Fallback |
|-------------------|----------|
| No dev server command | Skip service startup, run only static checks |
| No E2E framework | Skip E2E, note as unverified |
| No health endpoint | Poll port availability with `nc -z` instead |
| No verification commands in CLAUDE.md | Infer from tech stack, ask user if ambiguous |
| Server won't start | Report failure with logs, don't block workflow |
| E2E tests timeout | Report timeout, suggest running a subset |
| No browser tool | Use Playwright screenshots, then WebFetch, then curl HTML check |
| No UI changes in diff | Skip visual verification entirely |

## Integration Points

This skill is invoked by:
- `gh-start` — Phase 7 (after quality checks, before code review)
- `gh-pr` — Step 3.6 (pre-PR runtime verification)

**IMPORTANT**: Runtime verification is additive, not blocking. If a project has no dev server or E2E framework, this skill completes with "skipped" status and the workflow continues.
