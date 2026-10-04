---
name: synapse.news
description: "Fetch the latest news headlines from Reuters RSS and present them with source attribution."
version: "1.0.0"
author: "synapse-core"
triggers: ["news about", "latest news", "what's happening", "headlines"]
model_hint: "casual"
permissions: ["network:fetch"]
cloud_safe: false
enabled: true
entry_point: "scripts/news.py:get_news_context"
---

# News Skill

You have been given the latest headlines fetched from the Reuters RSS feed. Present them clearly.

## When invoked

The user wants to know what's in the news. The `context_block` contains the top headlines with
their URLs.

## How to respond

1. **List the headlines** — present them as a numbered list for easy reading.
2. **Add brief context** — if you can infer a one-sentence summary from the title, include it.
3. **Attribute the source** — mention "Reuters" as the source.
4. **If the user asked about a specific topic**, highlight any relevant headlines first, then
   present the rest.
5. **If context_block is empty or shows an error**, apologise and suggest the user check
   Reuters or another news site directly.

## Format example

Here are the latest headlines from Reuters:

1. **[Headline title]** — [brief context if inferable] ([link])
2. **[Headline title]** ...

*Source: Reuters (https://reuters.com)*

## Notes

- Do not editorialize or add political commentary beyond what the headline states.
- Headlines are fetched live — they may cover breaking news. Present them factually.
