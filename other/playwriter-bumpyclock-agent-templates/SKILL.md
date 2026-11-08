---
name: playwriter
description: "Chrome automation via Playwriter/Playwright for JS-heavy sites; run `playwriter skill`."
---

# Playwriter

**REQUIRED: Read full docs first:**

```bash
playwriter skill # IMPORTANT! do not use | head. read in full!
```

Outputs complete docs: session management, timeout config, selector strategies (which to AVOID), timeout/failure prevention rules, slow pages, SPAs, context variables, utility functions.

Read ENTIRE output. Do NOT pipe through `head`, `tail`, or truncation. Critical rules about timeouts, selectors, pitfalls are spread throughout, not just at top.

## Minimal Example (after reading full docs)

```bash
playwriter session new
playwriter -s 1 -e 'await page.goto("https://example.com")'
```

Always use single quotes for `-e`. Prevents bash interpreting `$`, backticks, backslashes in JS. Use double quotes or backtick template literals for JS strings.

If `playwriter` not found: `npx playwriter@latest` or `bunx playwriter@latest`.
