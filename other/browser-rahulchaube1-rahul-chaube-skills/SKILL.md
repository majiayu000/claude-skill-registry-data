---
name: browser
description: Browser control, navigation loops, elements locating, and scraping.
---

# Browser

Browser control, navigation loops, elements locating, and scraping.

## Core Guidelines

- **Wait States**: Implement wait loops for dynamic JavaScript elements. Do not guess sleep durations.
- **Selectors**: Use stable IDs or data attributes instead of brittle CSS structural paths.
- **Rate Limits**: Respect targets by throttling crawler pipelines.
