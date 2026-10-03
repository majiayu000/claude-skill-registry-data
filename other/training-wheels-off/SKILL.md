---
name: training-wheels-off
description: >
  Audits a project for mock data, placeholder content, hardcoded shortcuts, and
  anything else that's "not the real thing" — then helps you replace each one
  with a real implementation. Use this skill when the user says "training wheels
  off", "remove mock data", "are we using any fake data", "production ready",
  "find placeholders", "real data check", "audit for shortcuts", "is anything
  hardcoded", or any variation of wanting to make sure everything in the project
  is genuinely wired up and not faked. Also trigger when someone asks "is this
  ready for production", "what's still stubbed out", or "what's not real yet".
---

# Training Wheels Off

You're doing a thorough audit of a project to find every place where someone
took a shortcut that needs to be replaced before this thing is real. Mock data,
hardcoded values, stubbed functions, placeholder text, TODO hacks, commented-out
"real" implementations with a simpler fake sitting in their place — all of it.

The goal isn't to shame anyone for taking shortcuts. Shortcuts are how projects
get built. The goal is to find them all so nothing slips through when it matters.

## How This Works

1. **Scan** — Systematically search the project for shortcuts
2. **Classify** — Categorize what you find by severity and type
3. **Report** — Present findings with specific file locations and what "real"
   looks like for each one
4. **Fix** — Offer to replace shortcuts with real implementations one by one

---

## Phase 1: Scan

**IMPORTANT: Use parallel subagents for speed.** Launch 2-3 Task tool calls
with `subagent_type: "Explore"` simultaneously, each focused on a different
scan category. For example:

- **Agent 1: Textual signals** — Grep for all the keyword patterns (mock, fake,
  TODO, placeholder, hardcoded, etc.) across the codebase
- **Agent 2: Structural signals** — Read key files (API routes, config files,
  env files, entry points) looking for stubbed logic, swallowed errors, and
  bypassed systems
- **Agent 3: File & dependency signals** — Check for mock-named files, fixture
  dirs used in production, mock libraries in non-dev deps, and credential
  exposure

Launch all agents in a single message so they run concurrently. Then synthesize
their findings together before moving to Phase 2.

Search the entire project methodically. Don't just grep for "mock" and call it
a day — shortcuts hide in lots of places and go by lots of names.

### What to Search For

**Textual signals** — Search for these patterns across all files:

- `mock`, `Mock`, `MOCK`, `mocked`
- `fake`, `Fake`, `FAKE`
- `dummy`, `Dummy`, `DUMMY`
- `placeholder`, `PLACEHOLDER`
- `sample`, `sample_data`, `sampleData`
- `example`, `example.com`, `example.org`
- `test_data`, `testData`, `test_` (in non-test files)
- `hardcode`, `hardcoded`, `hard-coded`, `hard_coded`
- `stub`, `stubbed`
- `fixme`, `FIXME`, `hack`, `HACK`, `xxx`, `XXX`
- `TODO` (especially ones about replacing temporary implementations)
- `lorem ipsum`, `foo`, `bar`, `baz`, `asdf`, `qwerty`
- `temp`, `tmp` (as variable/function names, not OS temp dirs)
- `changeme`, `replace_me`, `update_this`
- `your_`, `my_`, `insert_` (as in `your_api_key`, `my_password`)
- `0000`, `1234`, `abcd`, `password`, `secret` (hardcoded credentials)
- `localhost`, `127.0.0.1` (outside of dev config files where it belongs)
- `sleep` with round numbers (often a hack for timing issues)

**Structural signals** — Look for these patterns in the code:

- Functions that return static data instead of fetching it
- API calls commented out with a hardcoded response below them
- `if true` / `if false` blocks that bypass real logic
- Feature flags permanently set to one value
- Environment variables with default fallbacks that *are* the real value
  (e.g., `os.getenv("API_KEY", "sk-actual-key-here")`)
- Try/catch blocks that swallow errors and return fake success
- Commented-out imports with a local reimplementation below
- Seed data files that are actually being used in production paths
- Configuration files with obviously non-production values
- Timeout values set to unrealistically high or low numbers
- Retry logic set to 0 or 1 attempts
- Pagination hardcoded to page 1 or a small limit
- Date/time values hardcoded to a specific date instead of computed
- User IDs, email addresses, or names that look like test data

**File-level signals** — Check for:

- Files named `mock_*.py`, `fake_*.js`, `*_stub.go`, etc.
- `fixtures/` or `seeds/` directories imported outside of tests
- `.env.example` that's actually the `.env` being used
- Config files with `development` or `debug` settings that shouldn't be
  shipping

**Dependency signals** — Check for:

- Mock libraries (faker, factory_boy, miragejs, msw, json-server, etc.)
  imported outside of test/dev dependencies
- In-memory database drivers used where a real database should be
- SQLite standing in for Postgres/MySQL in non-dev configs

### How to Search

Use a combination of grep/search tools and file reading. Start broad with the
textual signals, then narrow in on suspicious files. When you find something
that looks like a shortcut, read enough surrounding context to understand
whether it's actually a problem or intentional.

Not everything that matches is a real issue. Be thoughtful about what you flag:

- `mock` in a test file? Expected and fine.
- `example.com` in documentation? That's correct usage.
- `localhost` in a `.env.development`? Probably intentional.
- `TODO: replace with real auth` in production code? That's a finding.

The distinction is: **is this shortcut in a path that matters for the real
thing?** Test files, documentation, dev-only configs, and example scripts get
a pass. Everything else gets flagged.

---

## Phase 2: Classify

Group findings by type and severity. This helps the person prioritize what to
fix first.

### Severity Levels

**Critical** — Will break or compromise the project in production:
- Hardcoded credentials or API keys
- Mock auth that bypasses real authentication
- Fake payment/billing logic
- Test database being used for real data
- Security checks that are stubbed to always pass

**High** — Functional but wrong, users will notice:
- Mock data being displayed to real users
- Placeholder text visible in the UI ("Lorem ipsum", "TODO", etc.)
- Stubbed API integrations that return canned responses
- Hardcoded values that should come from config or database
- Email sending that's disabled or goes to a test address

**Medium** — Works for now but will cause problems as the project grows:
- Pagination hardcoded to small limits
- Error handling that swallows errors silently
- Retry logic that doesn't actually retry
- Caching disabled or set to absurd durations
- Feature flags stuck in one position

**Low** — Cosmetic or minor, but still not "the real thing":
- Placeholder images or icons
- Generic/template meta tags, page titles, favicon
- Default framework boilerplate that was never customized
- Sample data in seed files that's obviously fake

### Categorization

Also group by *type* of shortcut, since the person might want to tackle one
category at a time:

- **Mock Data** — Fake data standing in for real data
- **Stubbed Logic** — Functions that skip the real implementation
- **Hardcoded Values** — Things that should be configurable
- **Placeholder Content** — Text, images, or assets that aren't final
- **Bypassed Systems** — Auth, payments, email, etc. that are faked
- **Dev-Only Leftovers** — Debug code, dev tools, test configs in prod paths
- **Incomplete Features** — Half-built things gated behind always-off flags

---

## Phase 3: Report

Present findings clearly. For each finding:

1. **File and line** — Exact location
2. **What it is** — One sentence describing the shortcut
3. **Severity** — Critical / High / Medium / Low
4. **What "real" looks like** — Brief description of what should replace it
5. **Snippet** — Show the relevant code so the person can see it in context

Start the report with a quick summary: "I found N shortcuts across M files.
X critical, Y high, Z medium, W low." Give the person the lay of the land
before diving into details.

Present findings grouped by severity (critical first), then by type within each
severity level.

If the project is clean — few or no findings — say so clearly. That's a good
result and worth celebrating.

---

## Phase 4: Fix

After presenting findings, offer to fix them. Go one at a time or in batches,
depending on what the person prefers.

For each fix:

- **Explain what you're changing and why** before making the change
- **Ask if you need information** — some shortcuts exist because the real
  value wasn't known yet (API keys, real endpoints, production URLs). Don't
  guess at these; ask.
- **Don't over-engineer** — Replace the shortcut with the simplest real
  implementation that works. The person can refine later.
- **Preserve the intent** — If a mock function returns data in a specific
  shape, the real implementation should return the same shape.
- **Handle credentials carefully** — Never hardcode real credentials. Replace
  hardcoded fake credentials with proper environment variable lookups, and
  remind the person to set the actual values.

---

## Edge Cases

- **Monorepos** — Scan all packages/services, not just the root.
- **Generated files** — Skip `node_modules`, `dist`, `build`, `.git`,
  `__pycache__`, `vendor`, etc. If in doubt, check `.gitignore` for hints
  about what's generated vs. authored.
- **Intentional mocks** — Some projects use mock services in production on
  purpose (e.g., a feature that's gated, A/B tested, or in canary). If
  something looks intentional, flag it but note that it might be deliberate.
  Let the person decide.
- **Non-code projects** — For documents, check for placeholder text, template
  sections that were never filled in, stock photos, "[INSERT X HERE]" markers,
  and similar patterns.

## Tone

Be matter-of-fact. You're doing an audit, not a performance review. Present
what you found, where it is, and what the fix looks like. No judgment about
why the shortcuts are there — everyone takes shortcuts while building, that's
just how it works. The point is to catch them before they matter.
