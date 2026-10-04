---
name: summarize
description: "Summarize or extract key points from a URL, article, web page, or local file. Trigger on: summarize, fass zusammen, was steht da drin, give me a summary, tldr, key points, zusammenfassen, worum geht es."
user-invocable: true
---

# Summarize

## When to use
- User shares a URL and wants to know what it contains
- User asks to summarize a local file
- User says "tldr", "fass zusammen", "was steht da drin", "key points", "zusammenfassen"

## Steps
1. Determine whether the input is a URL or a local file path.
2. For a URL: use `web_fetch` to retrieve the content.
   If `web_fetch` fails or returns too little text, fall back to `browser` with `action=extract`.
3. For a local file: use `read` to load the content.
4. Produce a structured summary in the same language the user used.

## Output format

**Title** (if available)

**Summary**
2–4 sentences capturing the main idea.

**Key points**
- Point 1
- Point 2
- Point 3 (add more if needed)

**Source**: <url or file path>

## Notes
- If the content exceeds 10,000 characters, focus on the first 10,000.
- Always reply in the same language as the user's request.
- If neither `web_fetch` nor `browser` returns usable content, tell the user and suggest alternatives.
