---
description: Export design tokens from a Figma file to CSS, Tailwind, or JSON format
---

# Export Tokens

Export design tokens from the Figma design system to a code-ready format.

## Process

1. **Identify the Figma file.** The user should provide a Figma file key or URL. Extract the file key from the URL if needed (the key is the string between `/design/` or `/file/` and the next `/`).

2. **Fetch design tokens:**
   - Call `figma_get_variables` with the file key
   - If the user specified a format, pass `exportFormat` as "css", "tailwind", or "json"
   - Default to "css" if no format is specified

3. **Present the exported tokens** to the user.

4. **Optionally save to file.** If the user requests, write the output to a file:
   - CSS: `tokens.css`
   - Tailwind: `tailwind.tokens.json`
   - JSON: `tokens.json`

## Output

The exported tokens displayed to the user and optionally saved to a file.
