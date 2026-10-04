---
name: vibe-changelog
description: >
  Generates and maintains two changelog files from git tags, TASKS.md,
  DECISIONS.md, and feature folders. CHANGELOG.md at repo root is
  developer-facing in Keep a Changelog format with task IDs and decisions.
  CHANGELOG_CLIENT.md is plain English, grouped by "what you can now do",
  written like a product update — no task IDs or framework names. Version
  detection reads git tags first, then package.json or pyproject.toml.
  Appending uses git log [last-tag]..HEAD — never date-based. Groups
  completed tasks into higher-level entries rather than one line per task.
  If no git tags exist, generates as [Unreleased] and prompts to tag.
  Triggers: "changelog:" to generate or update both files,
  "changelog: since v1.0" to generate entries since a specific tag.
---

# Vibe Changelog Skill

Generates two changelog files from actual project history —
git tags, completed tasks, decisions, and feature specs.
Never one line per task. Always grouped into meaningful entries.
Always two audiences: developers and clients.

---

## Two files, always generated together

| File | Audience | Format | Location |
|---|---|---|---|
| `CHANGELOG.md` | Developers | Keep a Changelog, task IDs, decisions | repo root |
| `CHANGELOG_CLIENT.md` | Client stakeholders | Plain English, product-update style | repo root |

---

## Triggers

| Trigger | What it does |
|---|---|
| `changelog:` | Generate or update both files for current version |
| `changelog: since v1.0` | Generate entries only for changes since a specific tag |

---

## Step 0 — Read all sources

Read everything needed before generating a single line.

```bash
# Git history and tags
git tag --sort=-version:refname 2>/dev/null
git log --oneline --no-merges 2>/dev/null
git log --format="%H|%ai|%s|%an" --no-merges 2>/dev/null

# Version from project files
cat package.json 2>/dev/null
cat pyproject.toml 2>/dev/null
cat setup.py 2>/dev/null

# vibe context
cat vibe/TASKS.md 2>/dev/null
cat vibe/DECISIONS.md 2>/dev/null
ls vibe/features/ 2>/dev/null
ls vibe/bugs/ 2>/dev/null

# Read each feature and bug spec
cat vibe/features/*/FEATURE_SPEC.md 2>/dev/null
cat vibe/bugs/*/BUG_SPEC.md 2>/dev/null

# Existing changelogs — read before writing
cat CHANGELOG.md 2>/dev/null
cat CHANGELOG_CLIENT.md 2>/dev/null
```

---

## Step 1 — Detect version and scope

### Version detection (in order)

**1. Git tags (primary):**
```bash
git tag --sort=-version:refname | head -5
```
Most recent tag = current released version.
If tags exist: `git log [last-tag]..HEAD --oneline` = unreleased commits.
If HEAD is itself tagged: this is a release — generate entries for that tag.

**2. package.json (fallback):**
```json
{ "version": "2.1.0" }
```

**3. pyproject.toml (fallback):**
```toml
[tool.poetry]
version = "2.1.0"
```

**4. No version found — use [Unreleased]:**
Generate changelog as `[Unreleased]` and append this warning at the top:
```
⚠️  No git tags found. Changelog generated as [Unreleased].
    Tag your release to enable version-based changelogs:
      git tag -a v1.0.0 -m "Initial release"
      git push origin v1.0.0
```

### Scope detection

**If appending to existing CHANGELOG.md:**
1. Read the most recent version header from the file e.g. `## [1.0.0]`
2. Find that tag in git: `git rev-parse v1.0.0`
3. Scope = `git log v1.0.0..HEAD` — only commits after that tag
4. Cross-reference TASKS.md: completed items whose phase/feature aligns
   with the date range between the last tag and HEAD
5. Cross-reference DECISIONS.md: entries after the last tag date

**If no existing CHANGELOG.md:**
Generate the full history — all tags, all versions, back to initial commit.

**`changelog: since v1.0` trigger:**
Override scope to `git log v1.0..HEAD` regardless of existing file state.

---

## Step 2 — Group and summarise commits

This is the core of the skill. Raw commits and tasks must be grouped
into meaningful higher-level entries — not listed one per line.

### Grouping rules

**By feature folder:**
Tasks in the same `vibe/features/[name]/` folder → one changelog entry.
Use the feature name from FEATURE_SPEC.md, not the folder name or task IDs.

```
vibe/features/2026-04-12-web-connect/
  FEATURE_SPEC.md → "Web Connect — wire frontend to live API"

Tasks: WC-01, WC-02, WC-03 ... WC-18

Changelog entry:
  Added: Web frontend fully connected to live API — all 18 screens
         wired to real data with WebSocket chat and DM support
```

**By phase:**
Tasks in the same phase with no feature folder → grouped by theme.
Identify the theme from the task names and phase label in TASKS.md.

```
Phase 2 tasks: P2-rides-BE, P2-routes-BE, P2-tribe-BE,
               P2-admin-BE, P2-chat-BE, P2-notifications-BE,
               P2-rides-FE, P2-routes-FE ...

Grouped entry:
  Added: Complete core platform — rides, routes, tribe, admin,
         real-time chat, and push notifications
```

**By bug category:**
Multiple small bug fixes in the same area → one entry.

```
RFX-PA-001: OAuth callback timing fix
RFX-PA-002: Auth redirect guard on slow connections
RFX-PA-003: Token hydration race condition

Grouped entry:
  Fixed: OAuth login reliability on slow connections
```

**Standalone significant items:**
Large features, security changes, architectural decisions → own entry.

```
DECISION: Chat upgraded from polling to WebSocket
→ Changed: Real-time chat — upgraded from polling to WebSocket
           for instant message delivery
```

### Category mapping

Map grouped items to Keep a Changelog categories:

| Category | When to use |
|---|---|
| `Added` | New features, new screens, new API endpoints |
| `Changed` | Modified behaviour, upgrades, architectural changes |
| `Deprecated` | Features that still work but are scheduled for removal |
| `Removed` | Features removed in this version |
| `Fixed` | Bug fixes, crash fixes, reliability improvements |
| `Security` | Auth changes, CORS fixes, token handling, permissions |

### Writing the entries

**Dev changelog entries — technical but grouped:**
- Include task IDs in parentheses after the description
- Reference decisions with `(DECISION: [date])`
- Note which phase it came from if relevant
- One sentence per entry, precise

**Client changelog entries — plain English, no tech:**
- Never mention task IDs, framework names, file paths
- Write in second person: "You can now...", "Messages now..."
- Group related features into short paragraphs with a bold lead
- Tone: confident product announcement, not release notes

---

## Step 3 — Write CHANGELOG.md

Keep a Changelog format. Prepend new version above previous entries.
Never modify or rewrite existing version blocks — append only.

```markdown
# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] — 2026-04-16

### Added
- Complete web app with full feature parity — Next.js frontend deployed
  on Railway, all mobile features accessible in the browser (Web Connect,
  WC-01–WC-18)
- WebSocket-based real-time chat replacing HTTP polling — instant message
  delivery on mobile and web (PA-01, PA-02)
- Google and Apple OAuth login — one-tap sign-in on mobile and web (PA-04)
- Ratings and badges system — joiners rate posters after completed rides,
  milestone badges awarded automatically (PB-01–PB-03)
- Direct messages between tribe members — 1:1 WebSocket messaging with
  auto-reconnect (PB-05, PB-06)
- Vibe Match weather integration — 5-day forecast on web discover page,
  powered by OpenWeatherMap 2.5 (V2-C02)
- Admin route scraper — scheduled Gemini-powered extraction from
  configured source URLs, saves as unpublished drafts (V2-C03)

### Changed
- Chat architecture upgraded from polling (5–10s interval) to WebSocket
  for sub-second delivery (DECISION: 2026-04-12)
- Vibe match scoring moved to client-side — reduces server load at current
  scale, scores computed from loaded page (DECISION: 2026-04-12)
- Weather API uses OpenWeatherMap 2.5 over 3.0 — fully free tier,
  no credit card required (DECISION: 2026-04-13)

### Fixed
- OAuth callback timing on slow connections — replaced fixed 500ms delay
  with event-based redirect on auth store hydration (RFX-PA-001)
- ridesStore fully restored after Phase B review — was stubbed during
  parallel development, causing empty ride lists (RFX-PB-P0-001)
- WebSocket reconnect after app backgrounded — DM and chat stores now
  reconnect on app foreground event (RFX-PB-002)

### Security
- CORS origin locked to FRONTEND_URL env var — replaces wildcard
  that was used during development
- JWT secret and cron secret moved to Railway environment variables —
  never committed to repository

## [1.0.0] — 2026-03-28

### Added
- Initial platform launch — ride posting, discovery (75km radius),
  join request flow, per-ride group chat (Phase 1 + Phase 2)
- Tribe system — mutual follow, direct ride invites (Phase 2)
- Route discovery — 20+ seeded Pune routes, filterable by distance,
  vibe, and season (Phase 2)
- Admin route card tool — paste URL, Gemini extracts structured draft,
  admin publishes (Phase 2)
- Push notifications for 5 events — join request, approved, declined,
  tribe invite, DM received (Phase 2)
- Automated ride status transitions via Railway cron (Phase 3)
- 80%+ backend test coverage (Phase 3)

### Fixed
- Multiple Phase 2 review fixes — auth token edge cases, route filter
  pagination, chat message ordering (RFX-001–RFX-005)
```

---

## Step 4 — Write CHANGELOG_CLIENT.md

Plain English. Product update style. No task IDs, no framework names.
Written as if sending a product update email to the client.
Prepend new version above previous entries — never overwrite history.

```markdown
# What's New in [Project Name]

---

## Version 2.0 — April 2026

**[Project] is now on the web.**
Everything you can do in the app is now available in any browser.
The full experience works on desktop and tablet too.

**Chat is now instant.**
Messages appear the moment they're sent, on both the app and the website.
No more pulling down to refresh.

**Sign in with Google or Apple.**
No need to remember another password. Tap "Sign in with Google" or
"Sign in with Apple" on the login screen and you're in.

**Rate your rides.**
After every ride, you can rate the person who organised it.
Ratings build reputation over time and help others find great ride leaders.
Riders also earn badges as they hit milestones.

**Message anyone in your Tribe directly.**
Send a direct message to any Tribe member — not just through a ride chat.

**Weather on the discover page.**
The web app now shows a weather forecast for your upcoming rides at a glance.
Covers the next 5 days.

**Routes now auto-update.**
New routes are pulled in automatically from motorcycle blogs and travel sites
overnight. They come in as drafts — you review and publish with one click.

---

## Version 1.0 — March 2026

**[Project] launched.**

Post a ride in under a minute — destination, date, time, and how many
riders you want. Set a vibe filter so only riders who match your style
can request to join.

Discover upcoming rides near you, filter by vibe or date, and send
a join request. The poster gets a notification within 30 seconds.
Once approved, everyone gets a group chat for that ride.

Build your Tribe — a personal network of trusted riders. Invite them
directly to rides without going through the public feed.

Explore curated routes — distance, difficulty, key stops, chai stops,
and stay options. Tap "Plan a Ride" on any route to pre-fill the post form.

Rides move automatically from upcoming to active to completed
on the right day — no manual updates needed.
```

---

## Step 5 — Confirm to user

Present a summary before writing files:

```
CHANGELOG — [Project Name]
Version: [detected version or Unreleased]
Scope: [last-tag]..HEAD ([N] commits · [date range])
──────────────────────────────────────────────────

Entries grouped:

  ADDED ([N] groups from [N] tasks)
  · [group description (task IDs)]
  · [group description (task IDs)]

  CHANGED ([N] decisions from DECISIONS.md)
  · [decision summary]

  FIXED ([N] fixes from [N] bug folders + reviews)
  · [fix summary]

  SECURITY ([N] items)
  · [security item]

Files to write:
  ✅ CHANGELOG.md — prepend [version] above existing [last-version] entry
  ✅ CHANGELOG_CLIENT.md — prepend "Version [N]" above existing entry

Writing now...
```

Write both files immediately after summary — no confirmation needed
unless the version number looks wrong or scope seems clearly off.

---

## Step 6 — Update vibe docs

Append to `vibe/DECISIONS.md`:
```markdown
## [date] — Changelog updated
- **Version**: [version]
- **Scope**: [last-tag]..HEAD
- **Files**: CHANGELOG.md, CHANGELOG_CLIENT.md
- **Entries**: [N] added · [N] changed · [N] fixed · [N] security
```

---

## Absolute rules

**Never overwrite existing version blocks.**
CHANGELOG.md is append-only. Find the most recent version header
and prepend the new block above it. Never touch anything below.
Existing history is immutable.

**Version scope always from git tags — never dates.**
`git log v1.0.0..HEAD` is the only reliable way to scope a release.
Date-based scoping produces wrong results due to rebases, cherry-picks,
and timezone differences. If no tags exist, use `[Unreleased]`.

**Group first — never one line per task.**
A changelog entry that says "Added P2-rides-BE" is useless to anyone.
Always group related tasks and write one meaningful sentence.
The minimum grouping unit is a feature area or phase theme.

**Client file — zero technical terms.**
CHANGELOG_CLIENT.md must be readable by a non-technical client.
If a sentence contains a framework name, file path, task ID,
HTTP method, or acronym without explanation — rewrite it.
Test: would a business owner understand every word?

**Decisions from DECISIONS.md always make it in.**
Any entry in DECISIONS.md that falls within the version scope
must appear in the dev changelog under `Changed` or `Security`.
These are the most important architectural changes — never omit them.

**No version invented without evidence.**
If the version cannot be determined from git tags or project files,
always use `[Unreleased]`. Never invent a version number.

**If no commits since last tag — say so and stop.**
```
Nothing to changelog — no commits since v1.0.0 (2026-03-28).
Commit and tag a new version when ready:
  git tag -a v1.1.0 -m "Version 1.1.0"
  git push origin v1.1.0
```

**Always prompt to tag if no tags exist.**
Include the exact tagging commands in the output so the user
can establish proper versioning immediately after first run.
