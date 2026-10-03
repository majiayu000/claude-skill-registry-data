---
name: threads-comment-scraper
description: Extract content from heavily-commented Threads (and similar social media) posts using infinite scroll browser automation.
created: 2025-05-06
---

# Scraping Heavily Commented Posts (Threads/Social Media)

Use this skill when extracting content from social media posts that use **infinite scroll** (e.g., Threads comment threads, Twitter/X threads, Instagram posts) where not all content is visible at once.

## Problem

Social media platforms like Threads heavily lazy-load comments. An initial snapshot only shows the first batch of comments, and standard scroll-by on container elements often fails (returns "Scroll element not found") because the DOM structure doesn't expose a single scrollable ancestor.

## Approach

### 1. Navigate and Snapshot
- Use `browser_navigate` (or `mcp_chrome_devtools_navigate_page`) to load the URL.
- Use `browser_snapshot` to verify the page loaded.

### 2. Handle Login if Needed
- If the page shows a login prompt/wall, wait for the user to log in or handle auth as appropriate.
- Verify the main post content + initial comments are visible after login.

### 3. Scroll to Load More Content
**Key step: try multiple scrolling strategies in order.**

```python
# Strategy A: Try scrollable container (most common)
mcp_chrome_devtools_evaluate_script('''
() => {
  const el = document.querySelector('[role="feed"]')
    || document.querySelector('[data-testid="commentListView"]')
    || document.querySelector('[role="scrollbar"]')
    || document.querySelector('main');
  if (el) { el.scrollTop = el.scrollHeight; return 'Container scrolled'; }
  return 'Container not found';
}
''')
```

```python
# Strategy B (fallback): Scroll the window directly
mcp_chrome_devtools_evaluate_script('''
() => {
  window.scrollBy({ top: 2000 });
  return 'Window scrolled, scrollY: ' + window.scrollY;
}
''')
```

### 4. Repeat Scroll-Snapshot Cycle
- After each scroll, take a snapshot and check for new comments/elements.
- Repeat until no new content appears (pagination exhaustion).
- Each scroll loads approximately 5-10 new comments on Threads.

### 5. Extract Content
- Use `take_snapshot` or `evaluate_script` to grab all visible text content.
- Parse author names, post text, linked URLs, and engagement metrics.
- De-duplicate brand/product mentions.

## Threads-Specific Tips

- **Comment count indicator**: Look for `返信 N` (reply count) to gauge thread depth.
- **Like counts**: `「いいね！」 N` — useful for prioritizing popular comments.
- **URLs are wrapped**: Threads uses `https://l.threads.com/?u=ENCODED_URL&e=...` — decode the `u` parameter to get the actual destination.
- **Images with text**: Some comments have product photos with text overlays; use `vision_analyze` or `take_screenshot` for these.
- **Reply chains**: Some brands reply to other replies; snapshot will show nested threads.

## Edge Cases

| Issue | Solution |
|-------|------|
| Page loads a different tab (OAuth redirect) | Close extra tabs, return to main tab |
| Snapshot truncates at 8000 chars | Use `evaluate_script` to pull `textContent` directly |
| Too many comments to fit in one snapshot | Scroll in batches of 2000px, collect per batch |
| Comments are images not text | Use `take_screenshot` + `vision_analyze` |
