---
description: CLI for YC Startup School, a16z Speedrun, SPC, and startup program discovery — weekly updates, dashboard, applications, accelerator deadlines
allowed-tools: Bash, Read, Write
name: yc
version: 0.3.1
metadata:
  openclaw:
    requires:
      bins:
        - yc
    install:
      - kind: node
        package: "@lucasygu/yc"
        bins: [yc]
    os: [macos]
    homepage: https://github.com/lucasygu/yc-cli
tags:
  - ycombinator
  - startup-school
  - a16z
  - speedrun
  - south-park-commons
  - spc
  - accelerator
  - fellowship
  - incubator
  - discover
  - productivity
---

# YC CLI — YC Startup School, a16z Speedrun, SPC & Startup Discovery

CLI tool for managing your YC Startup School journey, submitting a16z Speedrun and SPC applications, and discovering 24+ accelerators, fellowships, and incubators — all from the terminal.

## Prerequisites

- Node.js 22+
- For YC commands: Logged into [startupschool.org](https://www.startupschool.org/) in Chrome, macOS
- For Speedrun commands: No auth required (public API)
- For SPC commands: Chrome browser (for form auto-fill via Chrome automation)

## Quick Reference

```bash
# YC Startup School
yc whoami                    # Test connection, show user info
yc dashboard                 # Show streak, curriculum, weekly status
yc updates                   # List all weekly updates
yc show <id>                 # Show a single update in detail
yc new                       # Submit new weekly update (interactive)
yc new --metric 5 --morale 7 --talked-to 3   # Non-interactive

# a16z Speedrun
yc speedrun template         # Generate JSON template
yc speedrun apply            # Interactive application
yc speedrun apply --from-json app.json   # Submit from JSON file
yc speedrun apply --from-json app.json --dry-run  # Validate without submitting
yc speedrun upload-deck deck.pdf   # Upload pitch deck

# South Park Commons
yc spc info                  # Show form URLs and program details
yc spc template              # Generate JSON template (fellowship)
yc spc template --type membership  # Template for community membership
yc spc apply                 # Interactive application
yc spc apply --from-json app.json  # Fill from JSON file
yc spc apply --from-json app.json --dry-run --headed  # Preview
yc spc open                  # Open form in browser

# Discover Programs
yc discover                  # Overview — deadlines + rolling programs
yc discover list             # Browse all 24+ programs
yc discover list --type fellowship   # Filter by type
yc discover list --stage pre-seed    # Filter by stage
yc discover deadlines        # Upcoming deadlines sorted by date
yc discover show yc          # Full details for a program
yc discover search "deep tech"       # Search by name/focus/description
yc discover open yc          # Open application page in browser
```

## YC Startup School Commands

### `yc whoami`
Test your connection and display user info (name, track, slug).

### `yc dashboard`
Show your Startup School dashboard:
- Current streak (consecutive weeks of updates)
- Curriculum progress (completed/required)
- Next curriculum item
- Recent weekly update status (submitted/missing)

### `yc updates`
List all your weekly updates with metric values, morale scores, and highlights.

### `yc show <id>`
Display a single update in full detail including goals and their completion status.

### `yc new`
Submit a new weekly update. Runs in interactive mode by default (prompts for each field).

**Interactive mode:**
```bash
yc new
# Prompts for: metric value, morale, users talked to, changes, blockers, goals
```

**Flag mode (for automation):**
```bash
yc new \
  --metric 10 \
  --morale 8 \
  --talked-to 5 \
  --change "Shipped MVP to first 10 users" \
  --blocker "Payment integration delayed" \
  --learned "Users want simpler onboarding" \
  --goal "Launch public beta" \
  --goal "Set up analytics"
```

## a16z Speedrun Commands

### `yc speedrun template`
Generate a JSON template for a Speedrun application. Save it, fill in your details, then submit with `--from-json`.

### `yc speedrun apply`
Submit a Speedrun application. Two modes:

**Interactive mode** (prompts for all fields):
```bash
yc speedrun apply
```

**From JSON file** (for automation / repeat submissions):
```bash
# Generate template, edit it, submit
yc speedrun template > my-app.json
# ... edit my-app.json with your details ...
yc speedrun apply --from-json my-app.json

# Dry run first to validate
yc speedrun apply --from-json my-app.json --dry-run
```

### `yc speedrun upload-deck <file>`
Upload a pitch deck PDF and get the GCS URL to include in your application.

```bash
yc speedrun upload-deck pitch.pdf
```

### Speedrun Categories
```
B2B / Enterprise Applications
Consumer Applications
Deep Tech
Gaming / Entertainment Studio
Infrastructure / Dev Tools
Healthcare
GovTech
Web3
Other
```

## Global Options

YC Startup School commands support:
- `--cookie-source <browser>` — Browser to read cookies from (chrome, safari, firefox). Default: chrome
- `--chrome-profile <name>` — Specific Chrome profile directory name
- `--json` — Output raw JSON (for scripting)

## South Park Commons Commands

SPC uses Airtable Interface forms. The CLI fills and submits via Playwright (headless Chromium).

### `yc spc info`
Show available SPC programs and their Airtable form URLs.

### `yc spc template`
Generate a JSON template for an SPC application.

```bash
yc spc template                    # Founder Fellowship (default)
yc spc template --type membership  # Community Membership
```

### `yc spc apply`
Fill and submit an SPC application via Playwright (headless browser).

```bash
yc spc apply                                          # Interactive
yc spc apply --from-json my-app.json                  # From JSON file
yc spc apply --from-json my-app.json --dry-run        # Fill but don't submit
yc spc apply --from-json my-app.json --headed         # Show browser window
yc spc apply --from-json my-app.json --dry-run --headed  # Visual review
```

### `yc spc open`
Open the SPC application form in your default browser.

```bash
yc spc open                    # Founder Fellowship
yc spc open --type membership  # Community Membership
```

### SPC Programs

| Program | Funding | Duration |
|---------|---------|----------|
| Founder Fellowship | $400K for 7% + $600K follow-on | Cohort-based (Spring/Fall) |
| Community Membership | No funding | Up to 6 months |

## Discover Commands

Browse 24+ curated accelerators, fellowships, and incubators with deadlines, terms, and application links.

### `yc discover`
Overview of programs with open/upcoming deadlines plus rolling programs. Default command.

### `yc discover list`
Browse all programs in a table format. Filter with options:
- `--type <type>` — Filter: `accelerator`, `fellowship`, `incubator`, `community`
- `--stage <stage>` — Filter: `pre-idea`, `pre-seed`, `seed`
- `--focus <focus>` — Filter by focus area: `ai`, `deep-tech`, `fintech`, etc.
- `--tier <tier>` — Filter: `1` (elite), `2` (major), `3` (notable)
- `--json` — Output as JSON

### `yc discover deadlines`
All upcoming deadlines sorted by closing date.

### `yc discover show <slug>`
Full details for a specific program — investment terms, equity, deadlines, focus areas, application URL.

### `yc discover search <query>`
Search programs by name, focus area, or description.

### `yc discover open <slug>`
Open a program's application page in the default browser.

## Workflows

### Weekly Update Routine
```bash
yc dashboard            # Check status
yc new                  # Submit if needed
yc updates              # Verify
```

### Speedrun Application via Claude Code
When the user asks to apply to a16z Speedrun, generate a JSON template, fill it with their info, and submit:
```bash
yc speedrun template > /tmp/speedrun-app.json
# ... Claude fills in the JSON ...
yc speedrun apply --from-json /tmp/speedrun-app.json --dry-run  # Validate first
yc speedrun apply --from-json /tmp/speedrun-app.json            # Submit
```

### SPC Application via Claude Code
```bash
yc spc template > /tmp/spc-app.json                        # Generate template
# ... Claude fills in the JSON ...
yc spc apply --from-json /tmp/spc-app.json --dry-run --headed  # Preview in browser
yc spc apply --from-json /tmp/spc-app.json                     # Submit
```

### Program Discovery
```bash
yc discover                         # What's open right now?
yc discover list --type fellowship  # Browse fellowships
yc discover show yc                 # Deep dive on YC
yc discover open yc                 # Open YC application
```

## Authentication

- **YC Startup School**: Extracts session cookies from Chrome — log in at startupschool.org first.
- **a16z Speedrun**: No authentication needed. The API is public.
- **South Park Commons**: No auth needed. Uses Playwright (headless Chromium) to fill Airtable forms.
