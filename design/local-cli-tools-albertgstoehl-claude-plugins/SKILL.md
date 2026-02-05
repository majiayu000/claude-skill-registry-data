---
name: local-cli-tools
description: Use when user mentions bookmarks, knowledge management, notes, saving URLs, or taking screenshots - provides quick reference for km (Zettelkasten notes), bookmark (URL manager), and shot-scraper (automated website screenshots) CLI tools installed on this system
---

# Local CLI Tools

## Overview

User has three CLI tools installed and ready to use: `km` for knowledge management, `bookmark` for URL management, and `shot-scraper` for automated website screenshots. Use these commands directly - they're in PATH.

**REQUIRED:** Always use the correct tool:
- `km new` for notes and knowledge management
- `bookmark add` for saving URLs to read/reference later (NOT for screenshots)
- `shot-scraper` for ANY screenshot, capture, or visual image of a website

**CRITICAL DISTINCTIONS:**
- User wants to READ/REFERENCE content later → `bookmark add`
- User wants SCREENSHOT/VISUAL/IMAGE of website → `shot-scraper`
- User says "screenshot", "capture", "take a picture", "grab an image" → `shot-scraper` (NEVER bookmark)

**Screenshots are NOT bookmarks. Bookmarks are NOT screenshots. These are different tools for different purposes.**

## Quick Reference

| Task | Command | Notes |
|------|---------|-------|
| Save bookmark | `bookmark add URL` | Auto-extracts title, generates summary |
| List bookmarks | `bookmark list` | Shows recent bookmarks |
| Search bookmarks | `bookmark search QUERY` | Semantic search via embeddings |
| Create note | `km new "Title"` | Opens editor for Zettelkasten note |
| Search notes | `km find QUERY` | Full-text search through notes |
| List notes | `km ls` | Shows recent notes |
| Browse notes | `km graph` | Interactive TUI browser |
| Screenshot webpage | `shot-scraper URL` | Automated website screenshot |
| Multiple screenshots | `shot-scraper multi shots.yaml` | Batch screenshot generation |
| Execute JavaScript | `shot-scraper javascript URL` | Scrape data via JS execution |
| Add documents | Copy to `/home/ags/paperless-ngx/consume/` | Auto-processed by Paperless-ngx |

## Bookmark Manager (`bookmark`)

**Location:** `/home/ags/.local/bin/bookmark`
**Backend:** API running on localhost:8000

```bash
# Add a bookmark (automatically fetches title and summary)
bookmark add https://example.com/article

# List recent bookmarks
bookmark list

# Search bookmarks (uses semantic search with embeddings)
bookmark search "docker security"

# Mark bookmark as read
bookmark mark BOOKMARK_ID read
```

**Features:**
- Automatic title extraction via Jina AI
- AI-generated 2-3 sentence summaries (Claude Haiku)
- Semantic search via embeddings
- Read/inbox status tracking

## Knowledge Management (`km`)

**Location:** `/home/ags/.cargo/bin/km`
**Storage:** Git-backed Zettelkasten notes

```bash
# Create new note (opens editor)
km new "Docker Security Best Practices"

# Create note with content via stdin
km new "Quick Note" << 'EOF'
# Quick Note
Content here
Tags: #docker #security
EOF

# Search notes by content
km find docker

# List recent notes
km ls

# Browse note graph interactively
km graph

# Show specific note
km show NOTE_ID

# Sync to remote
km sync
```

**Note Format:**
- Markdown files
- Use `#tags` for categorization
- Wikilinks `[[other-note]]` for connections
- Backed by git for version control

## Screenshot Automation (`shot-scraper`)

**THIS IS THE SCREENSHOT TOOL - Use this for ANY website screenshot request**

**Installation:** `pip install shot-scraper && shot-scraper install`
**Built on:** Playwright for reliable browser automation

**When to use:** User asks to screenshot/capture/grab image of ANY website - simple or complex

```bash
# Basic screenshot (auto-names file based on URL)
shot-scraper https://datasette.io/

# Screenshot with custom height
shot-scraper https://github.com/simonw/shot-scraper -h 900

# Screenshot specific element
shot-scraper https://example.com --selector ".main-content"

# Multiple screenshots from YAML config
shot-scraper multi screenshots.yaml

# Execute JavaScript and capture data
shot-scraper javascript https://example.com "
  return {
    title: document.title,
    links: Array.from(document.querySelectorAll('a')).length
  }
"

# Generate PDF instead of screenshot
shot-scraper pdf https://example.com -o output.pdf

# Wait for element before capturing
shot-scraper https://example.com --wait 2000

# Set viewport size
shot-scraper https://example.com --width 1280 --height 720

# Capture with authentication
shot-scraper auth https://app.example.com
shot-scraper https://app.example.com  # Uses saved auth
```

**Common YAML config (screenshots.yaml):**
```yaml
- url: https://example.com
  output: homepage.png
  height: 800

- url: https://example.com/about
  output: about.png
  selector: ".content"

- url: https://example.com/dashboard
  output: dashboard.png
  wait: 2000
```

**Features:**
- CSS selector-based element targeting
- JavaScript execution for data scraping
- Custom wait conditions and delays
- PDF generation from webpages
- Authentication workflow support
- Retina/high-DPI support
- GitHub Actions integration
- Transparent backgrounds
- Batch processing via YAML config

**Use cases:**
- Documentation screenshots
- Dashboard archiving
- Visual regression testing
- Web scraping with JS
- Automated report generation

**HANDLES COMPLEX CASES:** shot-scraper supports multiple pages, custom selectors, wait conditions, viewports - everything you need. Don't write custom Playwright/Puppeteer scripts.

## Paperless-ngx Document Management

**Location:** `/home/ags/paperless-ngx`
**URL:** https://n8n.gstoehl.dev

### Adding Documents

```bash
# Copy files to consume directory for automatic processing
cp ~/Downloads/invoice.pdf /home/ags/paperless-ngx/consume/

# Or use docker exec for management commands
cd /home/ags/paperless-ngx
docker compose exec webserver python manage.py COMMAND
```

### Common Management Commands

```bash
# Export all documents
docker compose exec webserver python manage.py document_exporter /usr/src/paperless/export

# Query documents via Python shell
docker compose exec webserver python manage.py shell_plus --plain -c "
from documents.models import Document
print('Total documents:', Document.objects.count())
"

# Create superuser account
docker compose exec webserver python manage.py createsuperuser
```

## When User Says...

| User Request | Execute This | Never |
|--------------|--------------|-------|
| "Save/add bookmark" | `bookmark add URL` | Not curl, not API |
| "Search bookmarks" | `bookmark search "X"` | Not grep |
| "Create/make/write a note" | `km new "Title"` | Not echo >, not touch |
| "Find/search notes" | `km find X` | Not grep |
| "Screenshot/capture website" | `shot-scraper URL` | Not manual browser, not puppeteer script |
| "Take screenshots of pages" | `shot-scraper multi config.yaml` | Not custom script |
| "Add PDF to paperless" | `cp FILE /home/ags/paperless-ngx/consume/` | Not docker cp |

**User says "note" → You run `km new`**
**User says "bookmark" → You run `bookmark add`**
**User says "screenshot" → You run `shot-scraper URL`**

## Red Flags - STOP and Use Correct Tool

If you find yourself doing ANY of these, STOP immediately and use the correct tool:

- About to suggest `bookmark add` when user asked for screenshot → Use `shot-scraper`
- Thinking "maybe they don't really need a screenshot" → User knows what they want, use `shot-scraper`
- Writing Puppeteer/Playwright code → Use `shot-scraper`
- Creating YAML config but then suggesting custom script → Use `shot-scraper multi config.yaml`
- Asking user to clarify screenshot vs bookmark → User said screenshot, use `shot-scraper`
- Suggesting manual browser screenshot → Use `shot-scraper`

**All of these mean: Execute `shot-scraper` immediately**

## Don't - No Exceptions

- ❌ Use curl to call the bookmark API directly (use `bookmark` CLI)
- ❌ Use Python script paths like `/home/ags/bookmark-manager/cli/bookmark_cli.py` (use `bookmark` command)
- ❌ Create standalone .md files (use `km new`)
- ❌ Download HTML files (use `bookmark add`)
- ❌ Write custom Puppeteer/Playwright scripts (use `shot-scraper`)
- ❌ Manual browser screenshots (use `shot-scraper`)
- ❌ "Complex requirements justify custom script" (shot-scraper handles it)
- ❌ Use `bookmark add` when user asks for screenshots (bookmark ≠ screenshot)
- ❌ Suggest "better alternatives" to screenshot requests (user knows what they want)
- ❌ "Time pressure justifies skipping tools" (tools are faster)
- ❌ Navigate to tool directories to run scripts (tools are in PATH)
- ❌ Provide multiple alternatives (use the proper tool)
- ❌ Ask which approach to use (execute the command)
- ❌ Explore directories to find tools (use commands directly)

**No matter how urgent:** Use `bookmark add` for URLs, `km new` for notes, and `shot-scraper` for screenshots. These commands take 2 seconds.

## Commands Are Installed

All three commands are installed in PATH:
- `bookmark` → `/home/ags/.local/bin/bookmark`
- `km` → `/home/ags/.cargo/bin/km`
- `shot-scraper` → Installed via pip

**Always use the command name directly. Never use full paths or Python scripts.**

## Common Mistakes

| Mistake | Why Wrong | Correct Approach |
|---------|-----------|------------------|
| Create ~/note.md directly | Bypasses km's git tracking, search index, graph | Use `km new "Title"` |
| Use Python script path | Not the installed command | Use `bookmark` command |
| curl to localhost:8000 | Bypasses CLI features | Use `bookmark` command |
| Write Puppeteer script | Reinvents shot-scraper, slower setup | Use `shot-scraper URL` |
| Manual browser screenshots | Not automatable, not repeatable | Use `shot-scraper` |
| User asks for screenshot, you use `bookmark add` | Screenshots and bookmarks are different things | Use `shot-scraper` for screenshots |
| "Complex case needs custom code" | shot-scraper handles selectors, waits, batches | Use `shot-scraper multi` with YAML |
| "Quick note, skip km" | Loses searchability, git history | Always use `km new` |
| Provide alternatives | Decision paralysis | Execute the proper command |
