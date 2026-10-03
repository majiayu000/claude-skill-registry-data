---
name: agent-memory
description: Session memory management, browser-based QA testing, and multi-agent coordination skill. Use when the user wants to persist learnings across sessions, review what the agent has learned about their codebase, prune stale knowledge, run browser-based testing with real Chromium, coordinate multiple AI agents on the same task, or set up authenticated browser sessions for testing.
---

# Agent Memory — Unified Skill

This skill unifies three complementary capabilities into a single, coherent workflow:

1. **`/learn` — Session Memory Management** — Persist, search, prune, and export what the agent has learned about your codebase and project across sessions.
2. **`/browse` — Browser-Based QA Testing** — Drive real Chromium (headless or headed), click elements, take screenshots, import cookies, and assert page state for production-grade QA.
3. **`/pair-agent` — Multi-Agent Coordination** — Spawn parallel sub-agents on isolated scopes, aggregate results, and hand off context cleanly between agents.

---

## Part 1 — Memory Management (`/learn`)

### 1.1 Philosophy: Why Memory Matters

Every time the agent explores your codebase, it discovers implicit patterns that are expensive to rediscover:

- Which modules are load-bearing vs. experimental
- Naming conventions that are project-local (not language-default)
- Fragile integration points that have broken before
- Performance invariants the team cares about
- Domain-specific jargon used in comments and variable names

Without memory, the agent starts cold every session. With memory, compound knowledge accumulates — each session builds on prior sessions, reducing repeated archaeology and increasing the precision of every suggestion.

**Principle: Memory is a first-class engineering artifact. Treat it like documentation.**

---

### 1.2 Memory Scopes

There are two distinct scopes of memory. Always be explicit about which scope you are reading from or writing to.

#### Global Memory (`~/.agent-memory/global/`)

Stores patterns that apply across all projects on this machine:

- Preferred code style decisions (e.g., "always use early-return guards")
- Recurring architectural preferences (e.g., "prefer repository pattern over active record")
- User-level shortcuts and workflow preferences
- Learned tool behaviors (e.g., "this user's Makefile uses `make lint` not `make check`")

#### Project Memory (`<repo-root>/.agent-memory/`)

Stores patterns specific to the current repository:

- Module ownership and dependency graph insights
- Known flaky test files and their workarounds
- Environment setup quirks (e.g., "must source `.env.local` before running tests")
- API contracts with external services this codebase integrates with
- Domain concepts: entity names, lifecycle states, event vocabulary
- Historical bugs and their root causes (for future regression awareness)
- Architecture Decision Records (ADRs) that affect code shape

**Rule:** If a pattern applies only to one repo, it MUST be written to project memory, not global. Polluting global memory with project-specific facts degrades the signal-to-noise ratio for all projects.

---

### 1.3 Memory File Format

All memory entries are stored as structured Markdown files for human readability and diff-friendliness.

```
.agent-memory/
├── patterns/
│   ├── naming-conventions.md
│   ├── architecture.md
│   ├── testing-patterns.md
│   └── fragile-zones.md
├── domains/
│   ├── entities.md
│   └── events.md
├── history/
│   ├── bugs-resolved.md
│   └── refactors-completed.md
└── index.md          ← master index with dates and tags
```

Each entry in a memory file follows this schema:

```markdown
## [PATTERN_ID] Short Title

**Learned:** YYYY-MM-DD  
**Confidence:** high | medium | low  
**Scope:** global | project  
**Tags:** #architecture #naming #performance  
**Source:** session-id or description of how this was discovered  

### Observation
What was observed.

### Pattern
The generalizable rule extracted from the observation.

### Example
Concrete code or command example.

### Caveats
Conditions under which this pattern does NOT apply.
```

---

### 1.4 Writing New Memory

When you discover something worth remembering, write it immediately — not at the end of the session, because sessions can be interrupted.

**Trigger conditions for writing a new memory entry:**

- You found a non-obvious architectural invariant (e.g., "all writes go through the event bus, never direct DB calls")
- You discovered a project-specific naming rule not in any README
- You debugged a recurring error class and want to short-circuit future debugging
- You learned how the build system behaves in an undocumented edge case
- The user explicitly says "remember this" or "add this to memory"

**Writing procedure:**

```bash
# 1. Determine scope
SCOPE="project"  # or "global"

# 2. Determine the correct category file
CATEGORY="patterns/architecture"  # or naming-conventions, testing-patterns, etc.

# 3. Generate a unique pattern ID
PATTERN_ID="ARCH-$(date +%Y%m%d)-001"

# 4. Write the entry (append to the category file)
# Use the schema defined in section 1.3 above.

# 5. Update the index
echo "- [$PATTERN_ID] Short title — $CATEGORY — $(date +%Y-%m-%d)" >> .agent-memory/index.md
```

---

### 1.5 Reading and Reviewing Memory

At the START of every session on a known project, load the memory index and the relevant category files before making any code suggestions.

```bash
# Load the project memory index
cat .agent-memory/index.md 2>/dev/null || echo "No project memory yet."

# Load global memory index
cat ~/.agent-memory/global/index.md 2>/dev/null || echo "No global memory yet."
```

When the user asks to **review** memory:

1. Print the full index with IDs, titles, dates, and tags.
2. Group entries by category (patterns, domains, history).
3. Flag entries older than 90 days as "⚠️ Stale — review for pruning."
4. Flag entries with `Confidence: low` as "🔍 Uncertain — verify before relying on."

---

### 1.6 Searching Memory

When the user asks to **search** memory for a topic:

```bash
# Search all memory files for a keyword
grep -r "KEYWORD" .agent-memory/ --include="*.md" -l

# Search with context lines
grep -r "KEYWORD" .agent-memory/ --include="*.md" -n -B 2 -A 4
```

Search is case-insensitive by default. Present results grouped by file, with the pattern ID and title prominently displayed.

---

### 1.7 Pruning Memory

Memory must be pruned to stay useful. Stale or wrong memory is worse than no memory — it misleads future sessions.

**Prune when:**
- A refactor changed the architectural pattern the entry described
- A dependency was removed (its patterns are now irrelevant)
- An entry is >180 days old and hasn't been referenced or validated
- The user explicitly says "this is no longer true"
- The confidence level was `low` and it never got validated

**Prune procedure:**

```bash
# 1. List entries older than 90 days
find .agent-memory/ -name "*.md" -mtime +90

# 2. For each candidate, present to user for confirm/keep/update
# 3. Delete confirmed-stale entries
# 4. Remove from index.md
# 5. Commit the pruning as a standalone commit with message:
#    "chore(memory): prune stale entries — YYYY-MM-DD"
```

**Never silently delete memory.** Always show the user what will be removed and get confirmation (or use `--force` flag only if user explicitly requests unattended pruning).

---

### 1.8 Exporting Memory

When the user wants to export memory (e.g., to share with a new team member, or to seed a new project):

```bash
# Export as a single consolidated Markdown document
cat .agent-memory/**/*.md > memory-export-$(date +%Y%m%d).md

# Export as JSON for programmatic use
python3 -c "
import os, json, re
from pathlib import Path

entries = []
for f in Path('.agent-memory').rglob('*.md'):
    content = f.read_text()
    entries.append({'file': str(f), 'content': content})

print(json.dumps(entries, indent=2))
" > memory-export-$(date +%Y%m%d).json
```

---

### 1.9 How Learnings Compound Across Sessions

The compounding effect works as follows:

| Session | What Happens |
|---------|--------------|
| 1 | Agent discovers project structure, writes 3–5 foundational entries |
| 2 | Agent loads index, skips re-exploration, writes 2–3 deeper entries |
| 3 | Agent cross-references existing patterns, catches inconsistencies |
| 5+ | Agent predicts issues before the user encounters them |
| 10+ | Agent functions like a senior team member who knows the codebase |

**Key behaviors that enable compounding:**
- Always load memory at session start (not on demand)
- Cross-reference new discoveries against existing entries before writing duplicates
- Upgrade confidence levels when an entry is validated a second time
- Link related entries using `[PATTERN_ID]` references within entries

---

## Part 2 — Browser QA Testing (`/browse`)

### 2.1 Philosophy

Real QA requires a real browser. Mocks and unit tests cannot catch:
- Layout regressions caused by CSS specificity conflicts
- Race conditions in JavaScript initialization
- Server-side rendering hydration mismatches
- Authentication flows that depend on session cookies
- Third-party widget interactions (analytics, chat widgets, payment iframes)

This skill drives **real Chromium** via Playwright, giving you pixel-accurate, JS-executing, network-real browser automation.

---

### 2.2 Prerequisites and Setup

```bash
# Install Playwright with Chromium
pip install playwright
playwright install chromium

# Or via npm
npm install -D playwright
npx playwright install chromium

# Verify installation
python3 -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"
```

---

### 2.3 Basic Navigation and Screenshot

```python
from playwright.sync_api import sync_playwright
import os

def browse_and_screenshot(url: str, output_path: str = "screenshot.png"):
    """
    Navigate to a URL and capture a full-page screenshot.
    Uses stealth settings to avoid bot detection.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-accelerated-2d-canvas",
                "--no-first-run",
                "--no-zygote",
                "--disable-gpu",
            ]
        )

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            timezone_id="America/New_York",
        )

        # Anti-bot: remove webdriver property
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.screenshot(path=output_path, full_page=True)
        browser.close()
        print(f"Screenshot saved to {output_path}")

browse_and_screenshot("https://localhost:3000", "qa-screenshot.png")
```

---

### 2.4 Real Clicks and Form Interactions

```python
def test_login_flow(base_url: str, email: str, password: str):
    """
    Test a real login flow with form filling and navigation assertions.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"{base_url}/login")

        # Fill form fields
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)

        # Screenshot before submit (for debugging)
        page.screenshot(path="before-login.png")

        # Click submit and wait for navigation
        with page.expect_navigation(wait_until="networkidle"):
            page.click('button[type="submit"]')

        # Assert post-login destination
        assert "/dashboard" in page.url, f"Expected redirect to /dashboard, got {page.url}"

        # Assert key element is present
        page.wait_for_selector('[data-testid="welcome-message"]', timeout=5000)

        # Screenshot after login
        page.screenshot(path="after-login.png")
        browser.close()
        print("Login flow: PASS")
```

---

### 2.5 Anti-Bot Stealth Configuration

For sites with advanced bot detection (Cloudflare, Akamai, DataDome):

```python
def stealth_context(playwright_instance):
    """
    Create a maximum-stealth browser context.
    Mimics a real macOS Chrome user as closely as possible.
    """
    browser = playwright_instance.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-features=IsolateOrigins,site-per-process",
        ]
    )

    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        screen={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        locale="en-US",
        timezone_id="America/Los_Angeles",
        color_scheme="light",
        device_scale_factor=2.0,  # Retina display
        has_touch=False,
        java_script_enabled=True,
        accept_downloads=True,
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }
    )

    # Remove all automation fingerprints
    context.add_init_script("""
        // Hide webdriver
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

        // Fake plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });

        // Fake languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });

        // Hide Chrome automation
        window.chrome = { runtime: {} };

        // Fake permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications'
                ? Promise.resolve({ state: Notification.permission })
                : originalQuery(parameters)
        );
    """)

    return browser, context
```

---

### 2.6 Cookie Import from Real Browser

To test authenticated sessions without re-logging in via automation (which often triggers 2FA):

#### Step 1: Export cookies from your real browser

Use the browser extension **"Cookie-Editor"** (Chrome/Firefox) to export cookies as JSON, or use the EditThisCookie extension.

Alternatively, export from Chrome's profile directly:

```bash
# macOS — copy Chrome's cookies database (requires Chrome to be closed)
cp ~/Library/Application\ Support/Google/Chrome/Default/Cookies /tmp/chrome-cookies.db

# Extract cookies for a specific domain using sqlite3
sqlite3 /tmp/chrome-cookies.db \
  "SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly
   FROM cookies WHERE host_key LIKE '%yourdomain.com%';"
```

#### Step 2: Load cookies into Playwright context

```python
import json

def load_cookies_from_file(context, cookie_file: str):
    """
    Load cookies exported from a real browser into a Playwright context.
    Supports the Cookie-Editor JSON export format.
    """
    with open(cookie_file) as f:
        raw_cookies = json.load(f)

    playwright_cookies = []
    for c in raw_cookies:
        cookie = {
            "name": c["name"],
            "value": c["value"],
            "domain": c.get("domain", ""),
            "path": c.get("path", "/"),
            "secure": c.get("secure", False),
            "httpOnly": c.get("httpOnly", False),
        }
        # Handle expiry
        if "expirationDate" in c:
            cookie["expires"] = int(c["expirationDate"])

        playwright_cookies.append(cookie)

    context.add_cookies(playwright_cookies)
    print(f"Loaded {len(playwright_cookies)} cookies.")


# Usage
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    load_cookies_from_file(context, "exported-cookies.json")

    page = context.new_page()
    page.goto("https://app.yourdomain.com/dashboard")

    # If cookies loaded correctly, you should be authenticated
    page.screenshot(path="authenticated-session.png")
    browser.close()
```

---

### 2.7 Responsive Layout Testing

```python
VIEWPORTS = {
    "mobile": {"width": 375, "height": 812},    # iPhone 13
    "tablet": {"width": 768, "height": 1024},   # iPad
    "desktop": {"width": 1440, "height": 900},  # Standard desktop
    "4k": {"width": 3840, "height": 2160},      # 4K
}

def test_responsive(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for name, viewport in VIEWPORTS.items():
            context = browser.new_context(viewport=viewport)
            page = context.new_page()
            page.goto(url)
            page.screenshot(path=f"responsive-{name}.png", full_page=True)
            print(f"  {name} ({viewport['width']}x{viewport['height']}): captured")
            context.close()
        browser.close()
```

---

### 2.8 Asserting Element State

```python
def assert_page_elements(page, assertions: list[dict]):
    """
    Run a list of element assertions on a page.

    assertion format:
      {"selector": "...", "type": "visible" | "text" | "count" | "attribute",
       "expected": <value>}
    """
    results = []
    for a in assertions:
        sel = a["selector"]
        kind = a["type"]
        expected = a.get("expected")

        try:
            if kind == "visible":
                page.wait_for_selector(sel, state="visible", timeout=5000)
                results.append({"selector": sel, "status": "PASS", "check": "visible"})

            elif kind == "text":
                el = page.locator(sel).first
                actual = el.inner_text()
                passed = expected in actual
                results.append({"selector": sel, "status": "PASS" if passed else "FAIL",
                                 "expected": expected, "actual": actual})

            elif kind == "count":
                actual = page.locator(sel).count()
                passed = actual == expected
                results.append({"selector": sel, "status": "PASS" if passed else "FAIL",
                                 "expected": expected, "actual": actual})

            elif kind == "attribute":
                attr_name = a["attribute"]
                actual = page.locator(sel).first.get_attribute(attr_name)
                passed = actual == expected
                results.append({"selector": sel, "status": "PASS" if passed else "FAIL",
                                 "expected": expected, "actual": actual})

        except Exception as e:
            results.append({"selector": sel, "status": "ERROR", "error": str(e)})

    return results
```

---

### 2.9 Before/After Diff Screenshots

```python
from PIL import Image, ImageChops
import numpy as np

def diff_screenshots(before_path: str, after_path: str, diff_path: str):
    """
    Produce a pixel diff between two screenshots.
    Highlights changed regions in red.
    """
    before = Image.open(before_path).convert("RGB")
    after = Image.open(after_path).convert("RGB")

    # Resize to same dimensions if needed
    if before.size != after.size:
        after = after.resize(before.size)

    diff = ImageChops.difference(before, after)
    arr = np.array(diff)

    # Amplify differences
    arr_amplified = (arr * 10).clip(0, 255).astype(np.uint8)

    # Overlay red channel on changed pixels
    mask = arr.sum(axis=2) > 10
    overlay = np.array(before)
    overlay[mask] = [255, 0, 0]

    Image.fromarray(overlay.astype(np.uint8)).save(diff_path)
    changed_pixels = int(mask.sum())
    print(f"Diff complete. {changed_pixels} pixels changed. Saved to {diff_path}")
    return changed_pixels
```

---

## Part 3 — Multi-Agent Coordination (`/pair-agent`)

### 3.1 Philosophy

Some tasks are too large or too parallel for a single agent context window. Multi-agent coordination enables:

- **Parallel exploration**: Split a large codebase across multiple sub-agents, each responsible for one module
- **Adversarial review**: One agent proposes, a second agent reviews independently
- **Specialization**: One agent focuses on security, another on performance, another on correctness
- **Fail-safe redundancy**: If one agent goes off-track, others continue independently

**Principle: Sub-agents must be given bounded, non-overlapping scopes. Ambiguous boundaries cause duplicate work and contradictory results.**

---

### 3.2 Spawning Sub-Agents

When spawning a sub-agent, always provide:

1. **Scope** — Exactly which files, directories, or concerns the agent is responsible for
2. **Deliverable** — Exactly what it should produce (code, analysis report, test cases, etc.)
3. **Constraints** — What it must NOT do (e.g., "do not modify files outside `src/auth/`")
4. **Output format** — How results should be structured for aggregation

```
Sub-Agent Spawn Template:
─────────────────────────
SCOPE:       src/auth/ — authentication and session management only
TASK:        Audit all session token generation and validation logic
DELIVERABLE: A Markdown report with: (1) findings, (2) severity ratings, (3) fix recommendations
CONSTRAINTS: Read-only. Do not modify any files. Do not follow imports outside src/auth/.
OUTPUT:      Save report to /tmp/audit-auth.md
```

---

### 3.3 Scope Isolation Patterns

#### Pattern A: Directory Isolation
```
Agent 1: src/api/          → API layer audit
Agent 2: src/services/     → Business logic audit
Agent 3: src/data/         → Data access layer audit
Agent 4: src/ui/           → Frontend component audit
```

#### Pattern B: Concern Isolation
```
Agent 1: Security — all files, only security concerns (input validation, auth, crypto)
Agent 2: Performance — all files, only performance concerns (N+1 queries, memory leaks)
Agent 3: Correctness — all files, only logic errors and edge cases
```

#### Pattern C: Test / Implementation Split
```
Agent 1: Write the implementation
Agent 2: Write the tests (without reading Agent 1's implementation)
→ Merge: tests should pass against Agent 1's code; gaps reveal spec ambiguity
```

---

### 3.4 Aggregating Results

After sub-agents complete their work, the coordinator agent must:

1. **Collect** all output files or structured responses
2. **Deduplicate** findings (multiple agents may flag the same issue)
3. **Resolve conflicts** (if two agents recommend contradictory approaches)
4. **Rank** findings by severity/impact
5. **Produce** a unified deliverable

```python
import json
from pathlib import Path

def aggregate_agent_reports(report_dir: str) -> dict:
    """
    Aggregate multiple agent report files into a unified finding set.
    Expects each report to be a JSON file with a "findings" array.
    """
    all_findings = []
    for report_file in Path(report_dir).glob("*.json"):
        data = json.loads(report_file.read_text())
        agent_name = report_file.stem
        for finding in data.get("findings", []):
            finding["source_agent"] = agent_name
            all_findings.append(finding)

    # Deduplicate by (file, line, type)
    seen = set()
    unique_findings = []
    for f in all_findings:
        key = (f.get("file"), f.get("line"), f.get("type"))
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    # Sort by severity
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    unique_findings.sort(key=lambda x: severity_order.get(x.get("severity", "info"), 5))

    return {
        "total_findings": len(unique_findings),
        "deduplicated_from": len(all_findings),
        "findings": unique_findings,
    }
```

---

### 3.5 Agent Handoff Patterns

When one agent's output becomes another agent's input, the handoff must be explicit and structured.

#### Handoff Document Format

```markdown
# Agent Handoff — [FROM_AGENT] → [TO_AGENT]

**Date:** YYYY-MM-DD HH:MM  
**Session:** [session-id]  
**From Agent Role:** [e.g., Researcher]  
**To Agent Role:** [e.g., Implementer]  

## Work Completed
- [List of what FROM_AGENT finished]

## Key Decisions Made
- [Decision 1] — Rationale: [why]
- [Decision 2] — Rationale: [why]

## Open Questions
- [Question 1] — TO_AGENT must resolve this before proceeding
- [Question 2] — Can be deferred until [milestone]

## Artifacts Produced
- `path/to/file.py` — [description]
- `path/to/spec.md` — [description]

## Constraints for TO_AGENT
- [Must not change X]
- [Must maintain backwards-compat with Y]
- [Must pass tests in Z]

## Suggested Next Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

---

### 3.6 Conflict Resolution

When two agents produce contradictory recommendations:

1. **Surface the conflict explicitly** — never silently pick one
2. **Identify the root disagreement** — is it a different assumption, different data, or genuine ambiguity?
3. **Apply a resolution strategy:**

| Conflict Type | Resolution Strategy |
|---|---|
| Different assumptions about requirements | Escalate to user for clarification |
| Different data (one agent missed something) | Merge both datasets, prefer the more complete one |
| Genuine design tradeoff | Document both options with pros/cons; let user decide |
| One agent clearly wrong | Flag the error, explain why, discard the wrong output |
| Style/preference disagreement | Default to the project's existing convention |

---

### 3.7 Coordinator Agent Responsibilities

The coordinator agent (the one that spawns sub-agents) is responsible for:

- **Defining scope boundaries** before spawning (never let sub-agents self-define scope)
- **Preventing scope creep** — sub-agents that wander must be redirected
- **Maintaining the master todo list** — sub-agents should not modify the master plan
- **Aggregating and synthesizing** — the final user-facing output comes from the coordinator
- **Memory consolidation** — write the session's learned patterns to memory after sub-agents complete

---

## Part 4 — Memory Hygiene

### 4.1 When to Prune

| Condition | Action |
|---|---|
| Entry is >180 days old with no re-validation | Archive or delete |
| Entry describes a removed module or dependency | Delete immediately |
| Entry has `Confidence: low` and was never validated | Delete or downgrade to "hypothesis" |
| Refactor changed the described pattern | Update or delete |
| Two entries contradict each other | Resolve and merge |
| Entry is specific to a branch that was merged/closed | Delete |

### 4.2 When to Keep

| Condition | Action |
|---|---|
| Entry has been validated by multiple sessions | Upgrade confidence to `high` |
| Entry describes a bug class that recurs | Keep indefinitely; add "recurrence count" |
| Entry is referenced by other entries | Keep; it is foundational |
| Entry documents a non-obvious constraint from an external system | Keep until that system is replaced |
| Entry was written by a senior engineer's explicit instruction | Keep; flag with `authority: explicit` |

### 4.3 Memory Hygiene Cadence

| Frequency | Activity |
|---|---|
| Every session | Load index; check for contradictions with new discoveries |
| Weekly | Scan for entries with `Confidence: low` |
| Monthly | Full prune pass: delete stale, archive old-but-valid |
| On major refactor | Complete memory audit: every entry must be validated against new architecture |
| On team member offboarding | Export global memory for handoff |

---

## Part 5 — Cross-Session Context Preservation

### 5.1 Session Start Protocol

At the start of every session:

```bash
# 1. Load project memory index
cat .agent-memory/index.md

# 2. Load global memory index
cat ~/.agent-memory/global/index.md

# 3. Check git log for changes since last session
git log --oneline --since="7 days ago" 2>/dev/null | head -20

# 4. Check for new or modified files since last session
git diff --name-only HEAD~5 HEAD 2>/dev/null

# 5. Load domain entities (always relevant)
cat .agent-memory/domains/entities.md

# 6. Load fragile zones (always relevant)
cat .agent-memory/patterns/fragile-zones.md
```

### 5.2 Session End Protocol

At the end of every session (or before context window fills):

```bash
# 1. Write all new patterns discovered this session
# (use the writing procedure from section 1.4)

# 2. Update confidence levels for entries that were validated or invalidated

# 3. Write a session summary to history/
SESSION_DATE=$(date +%Y-%m-%d)
cat >> .agent-memory/history/session-log.md << EOF

## Session $SESSION_DATE

**Duration:** [estimate]
**Focus:** [what was worked on]
**Patterns learned:**
- [PATTERN_ID] [title]

**Patterns invalidated:**
- [PATTERN_ID] [title] — reason

**Open questions for next session:**
- [question]
EOF
```

### 5.3 Handoff Between Human Developers

When a human developer takes over from an agent-assisted session:

1. Export the session log from `.agent-memory/history/session-log.md`
2. Export the index: `cat .agent-memory/index.md`
3. Attach both to the PR or ticket description under a collapsible "Agent Session Notes" section
4. The next developer or agent session loads these before starting

---

## Part 6 — Definition of Done Checklist

Before closing any task that used this skill, confirm ALL of the following:

### Memory Checklist
- [ ] All new patterns discovered this session are written to the appropriate memory scope (project or global)
- [ ] Index is updated with new entries (IDs, titles, dates, tags)
- [ ] Stale entries encountered during the session have been flagged for pruning
- [ ] Confidence levels are accurate and reflect validation status
- [ ] No contradictory entries exist without a resolution note
- [ ] Session log entry is written to `history/session-log.md`

### Browser QA Checklist
- [ ] All critical user flows have been exercised with real Chromium
- [ ] Screenshots are captured for before/after states of any UI change
- [ ] Assertions are written as code (not manual visual inspection) where feasible
- [ ] Authenticated flows used real cookies (not mocked sessions)
- [ ] Responsive layouts tested at mobile, tablet, and desktop viewports
- [ ] Any failures are documented with screenshot evidence and console logs

### Multi-Agent Checklist
- [ ] Scope boundaries were defined BEFORE agents were spawned
- [ ] Each agent's deliverable format was specified upfront
- [ ] Results from all agents have been collected and aggregated
- [ ] Conflicts have been surfaced and resolved (or escalated to user)
- [ ] Final output comes from the coordinator, not raw sub-agent output
- [ ] Handoff document written if another session will continue this work
- [ ] Memory consolidation completed by coordinator after sub-agents finished

### General Checklist
- [ ] No sensitive data (credentials, tokens, PII) was written to memory files
- [ ] Memory files are committed to the repo if project-scoped (`.agent-memory/`)
- [ ] Global memory is backed up if significant entries were added
- [ ] User was notified of any unresolved open questions or blocked items

---

## Quick Reference

| Command | Description |
|---|---|
| `/learn review` | Print full memory index, flag stale entries |
| `/learn search <keyword>` | Search all memory files for a keyword |
| `/learn prune` | Interactive prune pass — review and remove stale entries |
| `/learn export` | Export memory as consolidated Markdown or JSON |
| `/learn write` | Manually add a new memory entry |
| `/browse <url>` | Navigate and screenshot a page with real Chromium |
| `/browse login <url>` | Test a login flow |
| `/browse diff <before> <after>` | Pixel-diff two screenshots |
| `/browse cookies <file>` | Import cookies from real browser for auth testing |
| `/browse responsive <url>` | Test at all viewport sizes |
| `/pair-agent spawn` | Define and spawn a sub-agent with bounded scope |
| `/pair-agent aggregate` | Collect and merge all sub-agent results |
| `/pair-agent handoff` | Write a handoff document for the next agent/human |
| `/pair-agent resolve` | Surface and resolve conflicts between agent outputs |

---

*Agent Memory Skill — version 1.0.0 — AI agent*
