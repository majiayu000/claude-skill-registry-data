---
name: keyword-research
description: Pull keyword data from GSC, Ahrefs Webmaster, and DataForSEO. Returns a clustered keyword brief.
---

# /keyword-research

Usage: `/keyword-research <domain | topic | competitor-domain>` `[--for=<product-slug>]`

Examples:
- `/keyword-research linkedup.io --for=linkedup` — pull GSC + AWT data for own site
- `/keyword-research "form builder for indie hackers" --for=formpad` — topic search via DataForSEO
- `/keyword-research typeform.com --for=formpad` — competitor's ranking keywords via DataForSEO

## What this does
Invokes `agents/launch/keyword-researcher/SKILL.md`. Output saved to `products/<slug>/launch/keyword-briefs/YYYY-MM-DD-<topic>.md`.

## What you do as the assistant
1. Resolve `<for>` to a product slug. If omitted and unambiguous from context, infer; else ask.
2. Determine which API surface to call based on the input:
   - Looks like the product's own domain → GSC API + Ahrefs Webmaster
   - Looks like a competitor → DataForSEO domain queries
   - Looks like a topic (with quotes / spaces) → DataForSEO keyword suggestions
3. If API credentials aren't set yet (check `.env.local` for `DATAFORSEO_LOGIN`, GSC OAuth, etc.), tell the user what's missing and provide the setup link. Don't fail silently.
4. Execute the agent's protocol.
5. Save output, print location, summarize top 3 clusters in chat.

## Cost discipline
Per brief, target < $0.50 in DataForSEO API costs. If a query batch would exceed $2, confirm with user before running.
