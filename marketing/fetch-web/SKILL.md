---
name: fetch-web
description: Fetch web pages, scrape content, fill forms, take screenshots.
compatibility: Requires Node.js 18+, Chrome/Chromium. Run `npm install` in {baseDir}/scripts first.
---

# Fetch Web

Chrome-based web browsing. Extracts content as markdown. [Phoenix LiveView](https://github.com/phoenixframework/phoenix_live_view) auto-detected.

## Usage

```bash
{baseDir}/scripts/web.js <url> [options]
```

## Examples

```bash
# Fetch page as markdown
{baseDir}/scripts/web.js https://example.com

# Wait for DOM content to load
{baseDir}/scripts/web.js https://example.com --wait ".content-loaded"

# Screenshot
{baseDir}/scripts/web.js https://example.com --screenshot page.png

# Execute JS before extraction
{baseDir}/scripts/web.js https://example.com --js "document.querySelector('a').click()" --wait-ms 1000

# Persist session across calls
{baseDir}/scripts/web.js https://example.com --profile mysite

# Fill form and submit
{baseDir}/scripts/web.js https://example.com --profile mysite --js "
  document.querySelector('#email').value = 'user@example.com';
  document.querySelector('#password').value = 'secret';
  document.querySelector('form').submit();
" --wait-ms 2000

# Interactive element picker (user clicks in visible browser)
{baseDir}/scripts/web.js https://example.com --pick "Select the login button"

# View cookies
{baseDir}/scripts/web.js https://example.com --cookies

# Raw HTML instead of markdown
{baseDir}/scripts/web.js https://example.com --raw

# Visible browser for debugging
{baseDir}/scripts/web.js https://example.com --no-headless
```

See [references/examples.md](references/examples.md) for more (scraping patterns, table extraction, etc).
