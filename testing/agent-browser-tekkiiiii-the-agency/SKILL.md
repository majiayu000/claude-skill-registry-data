---
name: agent-browser
description: >
  Native Rust headless browser CLI for AI agents. Automates web UIs, scrapes pages, runs QA tests, and performs structured regression testing with health scores and fix loops. Triggers on: "automate browser", "scrape webpage", "QA test this site", "run browser tests", "find bugs on this page", "automate login", "take screenshot", "click this button". Also triggers on: "open this URL", "navigate to", "browser automation", "headless test", "web scraping", "test the web UI". Key capabilities: ~100ms per command, QA workflows with 8-category health scores, diff-aware regression on changed files/routes, multi-session isolation with named profiles, authenticated session persistence, tabs and iframe support, cloud provider integration (Browserless, Browserbase, Browser Use), content boundaries to prevent prompt injection, and command chaining with `&&`. Ideal for QA engineers, developers running regression suites, and agents needing reliable browser automation. Also for: visual bug reports, form filling, cookie session management, endpoint smoke testing, and comparing staging vs production environments.
---

# agent-browser

A fast native Rust CLI for headless browser automation, designed specifically for AI agents. No Playwright or Node.js required for the daemon.

## Installation
```bash
npm install -g agent-browser
agent-browser install   # Downloads Chrome for Testing (first time only)
```

On Linux, add `--with-deps` to install system dependencies.

## Core AI Workflow (Always Use This Pattern)
```bash
# 1. Open page
agent-browser open <url>

# 2. Get interactive elements with refs
agent-browser snapshot -i --json

# 3. Interact using refs from snapshot
agent-browser click @e2
agent-browser fill @e3 "input text"

# 4. Re-snapshot after page changes
agent-browser snapshot -i --json
```

**Refs are the preferred selector method for AI.** They come from `snapshot` output like:
```
- button "Submit" [ref=e2]
- textbox "Email" [ref=e3]
```
Then use `@e2`, `@e3` in subsequent commands.

## Essential Commands

### Navigation & Interaction
```bash
agent-browser open <url>              # Navigate (aliases: goto, navigate)
agent-browser click <sel>             # Click element
agent-browser fill <sel> <text>       # Clear and fill input
agent-browser type <sel> <text>       # Type into element
agent-browser press <key>             # Press key (Enter, Tab, Control+a)
agent-browser hover <sel>             # Hover element
agent-browser select <sel> <val>      # Select dropdown option
agent-browser check/uncheck <sel>     # Toggle checkbox
agent-browser scroll <dir> [px]       # Scroll up/down/left/right
agent-browser drag <src> <tgt>        # Drag and drop
agent-browser upload <sel> <files>    # Upload files
```

### Snapshot & Screenshots
```bash
agent-browser snapshot                 # Full accessibility tree with refs
agent-browser snapshot -i              # Interactive elements only (best for AI)
agent-browser snapshot -i -c -d 5     # Compact, depth-limited
agent-browser screenshot [path]       # Screenshot (saves to /tmp if no path)
agent-browser screenshot --annotate   # Numbered labels matching @eN refs
agent-browser screenshot --full        # Full page
```

### Get Info
```bash
agent-browser get text <sel>           # Get text content
agent-browser get url                  # Current URL
agent-browser get title                # Page title
agent-browser get value <sel>          # Input value
agent-browser get attr <sel> <attr>   # Element attribute
```

### Wait
```bash
agent-browser wait <selector>          # Wait for element visible
agent-browser wait <ms>                # Wait milliseconds
agent-browser wait --text "Welcome"   # Wait for text
agent-browser wait --url "**/dash"     # Wait for URL pattern
agent-browser wait --load networkidle  # Wait for network idle
agent-browser wait --fn "window.ready === true"  # Wait for JS condition
```

### Selectors

Use refs `@eN` from snapshot (preferred). Also supported:
- CSS: `"#id"`, `".class"`, `"div > button"`
- Text: `"text=Submit"`
- XPath: `"xpath=//button"`
- Semantic: `agent-browser find role button click --name "Submit"`

## Sessions & Authentication
```bash
# Multiple isolated sessions
agent-browser --session agent1 open site-a.com
agent-browser --session agent2 open site-b.com

# Persist login across restarts
agent-browser --profile ~/.myapp-profile open myapp.com

# Auto-save/restore session state
agent-browser --session-name myapp open myapp.com

# Import auth from running Chrome
agent-browser --auto-connect state save ./auth.json
agent-browser --state ./auth.json open https://app.example.com
```

## Command Chaining
```bash
agent-browser open example.com && agent-browser wait --load networkidle && agent-browser snapshot -i
agent-browser fill @e1 "user@example.com" && agent-browser fill @e2 "pass" && agent-browser click @e3
```

Chain with `&&` when you don't need intermediate output. Run separately when you need to parse output first.

## JSON Output (for programmatic use)
```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
agent-browser is visible @e2 --json
```

## Security Options
```bash
--content-boundaries           # Wrap output in delimiters (prevents prompt injection)
--allowed-domains "example.com,*.example.com"   # Restrict navigation
--max-output 50000             # Prevent context flooding
--action-policy ./policy.json   # Gate destructive actions
```

## Diff & Debug
```bash
agent-browser diff snapshot                      # Compare vs last snapshot
agent-browser diff url https://v1.com https://v2.com  # Compare two pages
agent-browser console                            # View console messages
agent-browser errors                            # View page JS errors
agent-browser trace start / stop [path]         # Record trace
```

## Cloud Browser Providers

When a local browser isn't available (serverless, CI/CD):
```bash
# Browserless
export BROWSERLESS_API_KEY="..."
agent-browser -p browserless open https://example.com

# Browserbase
export BROWSERBASE_API_KEY="..."
agent-browser -p browserbase open https://example.com

# Browser Use
export BROWSER_USE_API_KEY="..."
agent-browser -p browseruse open https://example.com
```

## Tabs & Frames
```bash
agent-browser tab new [url]    # New tab
agent-browser tab <n>          # Switch tab
agent-browser frame <sel>      # Switch to iframe
agent-browser frame main       # Back to main frame
```

## Configuration File

Create `agent-browser.json` in project root:
```json
{
  "headed": true,
  "profile": "./browser-data",
  "userAgent": "my-agent/1.0"
}
```

Priority: CLI flags > env vars > project `agent-browser.json` > `~/.agent-browser/config.json`

## Default Timeout

Default is 25 seconds. Override:
```bash
export AGENT_BROWSER_DEFAULT_TIMEOUT=45000
```
Keep below 30000ms to avoid EAGAIN errors.

---

## Structured QA Workflow (for browser-based testing)

When the user asks to "QA test", "find bugs", "run browser tests", or "test this site", follow this workflow.

### QA Modes

| Mode | Scope | When to use |
|------|-------|-------------|
| **Diff-aware** | Changed files/routes | Default on feature branch — auto-detect from `git diff` |
| **Full** | All pages | Systematic page-by-page |
| **Quick** | Homepage + top 5 | 30-second smoke test |
| **Regression** | Compare to baseline | Compare against prior `baseline.json` |

### Diff-Aware Setup

```bash
# Detect changed files/routes from git
git fetch origin main --quiet 2>/dev/null || true
git diff origin/main --name-only | grep -E '\.(tsx|jsx|vue|svelte|html)$' | head -20

# Detect local app port
ss -tlnp 2>/dev/null | grep -E '3000|4000|8080|5173|5000' || netstat -tlnp 2>/dev/null | grep -E '3000|4000|8080|5173|5000' || echo "No dev server detected"
```

### QA Tiers

| Tier | Scope | Fixes |
|------|-------|-------|
| **Quick** | Critical + High | 30-second smoke test |
| **Standard** | + Medium | Systematic exploration |
| **Exhaustive** | + Low/Cosmetic | Full depth |

### QA Phases

**Phase 1 — Initialize:**
```bash
mkdir -p .claude/qa-reports/screenshots
TIMER=$(date +%s)
```

**Phase 2 — Authenticate:**
Handle login. Try cookie import first:
```bash
agent-browser --auto-connect state save /tmp/auth.json
agent-browser --state /tmp/auth.json open <app-url>
```
If 2FA or CAPTCHA: hand off to user, then resume.

**Phase 3 — Orient:**
```bash
agent-browser open <url>
agent-browser snapshot -i
agent-browser console errors
agent-browser errors
agent-browser screenshot /tmp/initial.png
```

Detect framework type (SPA/Next.js/Rails/WordPress) from snapshot patterns.

**Phase 4 — Explore:**
Per page:
```bash
agent-browser screenshot
agent-browser console errors
agent-browser errors
agent-browser snapshot -i
# Interact: fill forms, click buttons, test nav
# Check: visible, enabled, disabled, checked states
```

**Phase 5 — Document:**
For each issue found, document immediately with:
```bash
agent-browser screenshot /tmp/issue-001-step-1.png
agent-browser snapshot -i
agent-browser screenshot /tmp/issue-001-result.png
```

Report format:
```
ISSUE #001
Severity: HIGH
Category: Functional
Page: /login
Description: Login form shows "Invalid credentials" for valid users
Repro steps: 1. Fill email 2. Fill password 3. Click Submit
Expected: Dashboard loads
Actual: Error message displayed
Screenshot: screenshots/issue-001-result.png
```

**Phase 6 — Health Score:**

Compute health score across 8 weighted categories:

| Category | Weight | Scoring |
|----------|--------|---------|
| Console errors | 15% | 100 - (critical×25 + high×15 + medium×8 + low×3) |
| Functional | 20% | Based on broken flows |
| Accessibility | 15% | ARIA labels, keyboard nav, focus management |
| UX | 15% | Navigation clarity, error messaging, loading states |
| Visual | 10% | Layout issues, spacing, alignment |
| Links | 10% | Broken links, missing hrefs |
| Performance | 10% | Load times, network errors |
| Content | 5% | Missing text, broken images |

Overall: weighted average. Report as `N/100`.

**Phase 7 — Fix Loop:**

For each issue, in severity order:
1. **Locate** — `grep` for error messages, component names
2. **Fix** — minimal change only, no refactoring
3. **Commit** — one per fix:
   ```bash
   git add -p
   git commit -m "fix(qa): ISSUE-NNN — short description"
   ```
4. **Re-test** — before/after screenshots, `agent-browser diff snapshot`
5. **Classify** — verified / best-effort / reverted / deferred

Stop conditions:
- 30+ fixes reached
- Fix risk exceeds 20% (might break something else)
- All Critical + High resolved

**Phase 8 — Save Baseline:**
```bash
echo '{
  "date": "'$(date -I)'",
  "health_score": N,
  "issues": [...],
  "url": "...",
  "git_sha": "'$(git rev-parse HEAD)'"
}' > .claude/qa-reports/baseline.json
```

### Output Structure

```
.claude/qa-reports/
├── qa-report-{domain}-{YYYY-MM-DD}.md
├── screenshots/
│   ├── initial.png
│   ├── issue-001-step-1.png
│   ├── issue-001-result.png
│   └── ...
└── baseline.json
```

### QA Report Template

```markdown
# QA Report — {domain} — {YYYY-MM-DD}

URL tested: {url}
Health score: {N}/100
Tier: {Quick/Standard/Exhaustive}
Mode: {Diff-aware/Full/Regression}
Time: {N} minutes

## Issues Found

| # | Severity | Category | Page | Description | Status |
|---|----------|----------|------|-------------|--------|
| 001 | HIGH | Functional | /login | ... | FIXED |
| 002 | MEDIUM | UX | /home | ... | VERIFIED |

## Severity Breakdown
Critical: N  High: N  Medium: N  Low: N

## Health Score
Console: N/100  Functional: N/100  Accessibility: N/100
UX: N/100  Visual: N/100  Links: N/100
Performance: N/100  Content: N/100

## Fixes Applied
- [commit hash] fix(qa): ISSUE-001 — ...
```
