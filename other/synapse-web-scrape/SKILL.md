---
name: synapse.web-scrape
description: "Fetch and extract readable text content from a URL, then summarise or present key information."
version: "1.0.0"
author: "synapse-core"
triggers: ["scrape", "fetch this page", "read this url", "get content from"]
model_hint: "analysis"
permissions: ["network:fetch"]
cloud_safe: false
enabled: true
entry_point: "scripts/scrape.py:scrape_url_context"
---

# Web Scrape Skill

You have been given the text content scraped from a web page. Use it to answer the user's question.

## When invoked

The user has provided a URL and wants you to read, summarise, or extract information from it.
The `context_block` in your context contains up to 8000 characters of plain text extracted from
the page.

## How to respond

1. **Answer the user's actual question first** — if they asked a specific question about the page,
   address it directly before summarising.
2. **Summarise key information** — extract the most relevant content: main topic, key facts,
   important quotes, tables, or lists.
3. **Cite the source** — mention the URL in your response so the user can verify.
4. **Be concise** — do not reproduce the entire scraped text verbatim. Synthesise it.
5. **If context_block is empty or shows an error**, explain that the page could not be fetched
   and suggest the user try a different URL or check if it requires authentication.

## Notes

- Some pages require JavaScript rendering or authentication — plain HTTP fetch may not capture
  all content. Mention this caveat if the extracted content seems incomplete.
- Do not fabricate content not present in the scraped text.
