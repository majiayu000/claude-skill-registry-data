---
name: browser-domain-skills
description: >
  Shared domain knowledge convention for all browser automation tools. Stores per-host
  notes (login flows, selector quirks, anti-bot workarounds, form structures) that any
  browser skill can read before navigating and write after learning. Self-healing pattern:
  observe → capture → reuse across sessions. Not a tool — a shared memory protocol.
---

# Browser Domain Skills

Shared, cross-tool knowledge base for site-specific browser automation patterns.

## Directory Structure

```
~/.claude/skills/browser-domain-skills/
├── SKILL.md              (this file — convention definition)
└── {hostname}/
    └── notes.md          (domain knowledge for that host)
```

## Note Format

Each `{hostname}/notes.md` uses this structure:

```markdown
---
host: github.com
last_updated: 2026-05-16
source_tool: agent-browser | browse | browser-harness | playwright-mcp
confidence: high | medium | low
---

# {hostname} — Domain Notes

## Login Flow
(How auth works, selectors, MFA handling)

## Key Selectors
(Stable selectors that survive redesigns — data-testid preferred)

## Gotchas
(Anti-bot detection, rate limits, dynamic loading quirks, shadow DOM)

## Verified Workflows
(Step-by-step sequences that reliably work)
```

## Protocol

### Before Navigating to a Host

All browser tools SHOULD check:
```bash
ls ~/.claude/skills/browser-domain-skills/{hostname}/ 2>/dev/null
```
If `notes.md` exists, read it before interacting. This avoids re-learning known quirks.

### After Learning Something New

When a browser tool discovers something non-obvious about a site (a tricky selector, an anti-bot pattern, a reliable workflow), write or append to:
```
~/.claude/skills/browser-domain-skills/{hostname}/notes.md
```

Rules:
- Only write **non-obvious** knowledge — don't note that "google.com has a search box"
- Update `last_updated` and `source_tool` in frontmatter
- Append new sections; don't overwrite existing verified knowledge
- Set `confidence: low` for first-time observations, promote to `high` after 3+ successful reuses

### Cross-Tool Compatibility

| Tool | Reads shared notes | Writes shared notes |
|------|-------------------|-------------------|
| agent-browser | Yes (via Domain Knowledge section) | Yes |
| browse | Yes (also has its own `domain-skill` subcommand) | Via `domain-skill save` |
| browser-harness | Yes (check before `goto_url`) | Yes (alongside its own `agent-workspace/domain-skills/`) |
| Playwright MCP | Manual (caller reads before starting) | Manual |
| Lightpanda | N/A (data extraction only) | N/A |

## Examples

**Creating a note:**
```bash
mkdir -p ~/.claude/skills/browser-domain-skills/linkedin.com
cat > ~/.claude/skills/browser-domain-skills/linkedin.com/notes.md << 'EOF'
---
host: linkedin.com
last_updated: 2026-05-16
source_tool: browser-harness
confidence: medium
---

# linkedin.com — Domain Notes

## Gotchas
- Aggressive bot detection: need real Chrome profile with history
- Rate limits: max ~100 profile views/day before soft block
- Dynamic loading: wait for `div.scaffold-finite-scroll__content` not just networkidle

## Key Selectors
- Profile name: `h1.text-heading-xlarge`
- Experience section: `#experience ~ .pvs-list__container`
- Connect button: `button[aria-label*="Connect"]`
EOF
```
