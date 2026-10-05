---
name: ha:ha-docs-fetcher
description: "Fetch Home Assistant library docs with HTML-to-markdown conversion. Use when looking up docs on developers.home-assistant.io, home-assistant.io, PyPI, or GitHub home-assistant/core source — packages, APIs, guides, changelogs."
effort: low
---

# HA Docs Fetcher

Efficiently fetch Home Assistant documentation from developers.home-assistant.io,
home-assistant.io, PyPI project pages, and GitHub home-assistant/core source
using Claude Code's native `WebFetch` tool.

## Usage

When researching integrations or libraries, use `WebFetch`:

```
# Fetch developer docs section
WebFetch(
  url: "https://developers.home-assistant.io/docs/integration_fetching_data",
  prompt: "Extract the main documentation, including overview, patterns, and key examples. Format as clean markdown."
)

# Fetch a PyPI project page (JSON) for a library dependency
WebFetch(
  url: "https://pypi.org/pypi/aiohttp/json",
  prompt: "Extract the latest version, summary, project URLs, and requires_python."
)

# Fetch user-facing integration docs
WebFetch(
  url: "https://www.home-assistant.io/integrations/mqtt/",
  prompt: "Extract the complete configuration and usage guide content."
)
```

## Token Efficiency

WebFetch automatically converts HTML to markdown and extracts relevant content:

| Source | Raw HTML | With WebFetch | Benefit |
|--------|----------|---------------|---------|
| home-assistant.io integration page | ~80k tokens | ~15k tokens | **80% reduction** |
| Developer docs (developers.home-assistant.io) | ~120k tokens | ~25k tokens | **79% reduction** |
| README | ~20k tokens | ~8k tokens | **60% reduction** |

## Integration with pypi-library-researcher

When evaluating library dependencies, fetch docs efficiently:

```
# Get library overview with focused extraction
WebFetch(
  url: "https://pypi.org/pypi/aiohttp/json",
  prompt: "Extract: 1) Latest version and requires_python 2) Summary 3) Project/homepage URLs"
)
```

## Common Docs URLs

```
# PyPI project page (JSON) — canonical for library metadata
https://pypi.org/pypi/{package}/json
https://pypi.org/pypi/{package}/{version}/json

# PyPI project page (HTML)
https://pypi.org/project/{package}/

# Home Assistant developer docs
https://developers.home-assistant.io/docs/{section}

# Home Assistant user docs (integrations, config)
https://www.home-assistant.io/integrations/{domain}/

# home-assistant/core source lookup on GitHub
https://github.com/home-assistant/core/blob/dev/homeassistant/components/{domain}/{file}
https://raw.githubusercontent.com/home-assistant/core/dev/homeassistant/components/{domain}/{file}

# GitHub raw README — fallback when a library has no dedicated docs site
https://raw.githubusercontent.com/{org}/{repo}/main/README.md
https://raw.githubusercontent.com/{org}/{repo}/master/README.md
```

## Prompt Strategies

Use focused prompts for better extraction:

```
# For API docs
prompt: "Extract all public method/function signatures with types and examples"

# For guides
prompt: "Extract the complete guide content preserving code examples"

# For troubleshooting
prompt: "Extract any troubleshooting sections, common errors, and FAQs"

# For configuration
prompt: "Extract configuration options and their defaults"
```

## Caching

WebFetch includes automatic 15-minute caching. When fetching the same URL multiple times in a session, results are cached automatically.

For longer persistence, save to planning directory:

```
# After fetching, write the result to a file
Write(
  file_path: ".claude/plans/{slug}/research/docs/aiohttp.md",
  content: "{extracted content}"
)
```

## Local Source Alternative

If you have a home-assistant/core checkout or the library is already installed,
prefer reading it directly over fetching the web:

```
Read(file_path: "homeassistant/components/{domain}/manifest.json")
Read(file_path: "homeassistant/components/{domain}/__init__.py")
Read(file_path: ".venv/lib/python3.13/site-packages/{package}/__init__.py")
```

This matches the exact version pinned in your environment — faster, more
accurate, zero web tokens than a generic PyPI/docs-site fetch.

## Iron Laws

1. **NEVER fetch entire home-assistant.io or docs sites** — always target specific pages or sections
2. **Use focused prompts** — generic fetches waste tokens; specify what to extract
3. **Prefer local source when available** — exact version match beats generic web docs
