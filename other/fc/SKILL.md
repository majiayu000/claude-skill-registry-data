---
name: fc
description: Perform web search then firecrawl scrape each result and combine.
category: web-workflow
---

**Description**: Perform a web search for a given query, then scrape each result URL using Firecrawl, and combine the extracted content into a single response.

**Trigger**: Slash command `/fc <query>` where `<query>` is the search term.

**Prerequisites**:
- Firecrawl API key in `~/.hermes/.env` as `FIRECRAWL_API_KEY`.
- Firecrawl SDK installed in the venv: `uv pip install firecrawl-py --python venv/bin/python`.

**Steps**:\n1. **Parse Input**: Check if input is a URL (starts with `http`) or a search query.\n2. **URL Mode** (if input is a URL like `/fc https://x.com/...`):\n   - **Try 1**: `npx -y firecrawl@latest scrape "<url>"` (CLI approach)\n   - **Try 2**: Python SDK `FirecrawlApp(api_key).scrape(url, formats=['markdown'])`\n   - **Fallback** (for X/Twitter or blocked sites): Browser automation workflow:\n     a. `mcp_chrome_devtools_new_page(url=<url>)`\n     b. `mcp_chrome_devtools_take_screenshot(fullPage=true, filePath=/tmp/page.png)`\n     c. `vision_analyze(image_url=/tmp/page.png, question="Extract all text content")`\n     d. Alternative: `mcp_chrome_devtools_evaluate_script` to extract DOM text\n3. **Search Mode** (if input is a query):\n   - Call `web_search` with the query, requesting up to 5 results.\n   - Extract the `url` field from each result.\n4. **Firecrawl Scrape** (for each URL in Search Mode):\n   - Use the Firecrawl SDK to scrape the content.
   - Use the Firecrawl SDK to scrape the content.
   - **Python Implementation Pattern**:
     ```python
     from firecrawl import FirecrawlApp
     import os

     # Load API key from .env
     api_key = None
     with open(os.path.expanduser('~/.hermes/.env')) as f:
         for line in f:
             if line.startswith('FIRECRAWL_API_KEY='):
                 api_key = line.split('=', 1)[1].strip()
                 break

     app = FirecrawlApp(api_key=api_key)
     doc = app.scrape(url=target_url, formats=['markdown'])
     content = doc.markdown
     ```
   - **Fallback**: If the SDK returns `InternalServerError` (common on X.com/Twitter), use the CLI:
     `npx firecrawl-cli@latest scrape <url>`
4. **Combine Results**:
   - Concatenate all scraped markdown sections, separating each with a heading indicating the source URL (e.g., `## Source: <url>`).
   - If any URL fails to scrape, note the error and continue.
5. **Output**:
   - Return the combined markdown to the user.
   - Include the original web search URLs as references (per user preference).

**Pitfalls**:
- **SDK v2 API**: Remember that `app.scrape_url` is deprecated; use `app.scrape(url=..., formats=['markdown'])`.
- **Pydantic Objects**: The SDK returns a `Document` object; use `result.markdown`, not `result['markdown']`.
- **Auth**: The SDK does NOT auto-read `FIRECRAWL_API_KEY` from env; it must be passed explicitly.
- **Anti-Bot Protection**: Some sites block the SDK's playwright backend. The `npx firecrawl-cli` is the recommended workaround for these cases.
- **X/Twitter**: Often blocks Firecrawl entirely (returns `InternalServerError`). Use browser automation fallback:
  1. Open URL via `mcp_chrome_devtools_new_page`
  2. Take full-page screenshot with `mcp_chrome_devtools_take_screenshot(fullPage=true)`
  3. Extract text using `vision_analyze` on the screenshot
  4. Alternatively, use `mcp_chrome_devtools_evaluate_script` to extract DOM text directly
- **Government / Weather Sites** (e.g., CWA/中央氣象署 for 台灣天氣):
  - Web search for real-time weather may return only climate averages or outdated summary pages instead of current forecasts.
  - Target government sites (cwa.gov.tw, etc.) often block both `web_extract` and Firecrawl SDK.
  - Workaround: use browser automation (`mcp_chrome_devtools_take_snapshot`) on the official forecast page for structured, parseable text — prefer `take_snapshot` over `vision_analyze` when the page has well-structured tables/lists.

**Verification**:
- After running `/fc test query`, verify that:
  - The response contains sections for each successfully scraped URL.
  - Each section starts with `## Source: <url>`.
  - The combined content is in markdown format.

**Example**:
```
/fc latest AI advancements 2024
```
Will search the web, scrape the top result pages via Firecrawl, and return a consolidated markdown summary.
