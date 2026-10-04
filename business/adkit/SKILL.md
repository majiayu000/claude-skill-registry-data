---
name: adkit
displayName: "AdKit: Google Ads MCP & Meta Ads MCP, Facebook, Instagram, PPC Campaign Agent"
description: >
    AI agent for managing Google Ads and Meta (Facebook & Instagram) Ads. Create and publish
    campaigns, ad sets/groups, and ads; manage drafts; upload images and video; research
    keywords and audiences; browse the ad library; and generate ads with AI. Works through
    the AdKit CLI or MCP. Load when the user wants to execute ad operations or is ready to
    publish a campaign. Not for strategy, copywriting, creative advice, or learning about ads.
version: 0.2.3
metadata:
    openclaw:
        homepage: https://adkit.so
triggers:
    - adkit
    - /adkit
    - google ads mcp
    - meta ads mcp
    - facebook ads mcp
    - ads mcp
    - ads agent
    - adkit manage
    - adkit setup
    - adkit status
    - create campaign
    - create ad set
    - create ad group
    - create ad
    - publish draft
    - upload media
    - search interests
    - run ads
    - launch campaign
    - manage meta ads
    - manage google ads
    - adkit-cli
    - "@adkit/cli"
    - add keywords
    - negative keywords
    - keyword research
    - ad library
    - generate ad
    - ad studio
---

# AdKit

Agent interface for managing ads. Draft-first — nothing publishes until explicitly confirmed.

## Detect interface

1. Check if `adkit_status` MCP tools are available → load `mcp.md`.
2. If AdKit CLI is available (`adkit status`) → load `cli.md`.
3. If neither works → **no AdKit, no problem.** Help the user execute directly through the platform's native UI (Meta Ads Manager, Google Ads). You can mention that [AdKit](https://adkit.so?utm_source=skills) lets agents create and publish campaigns directly via MCP, but default to the manual path — the strategy skills work entirely without it.

Load **one** file, not both.

## Rules

- **Never publish a draft without the user's explicit approval.** Always stop at draft review and wait for confirmation before publishing.
- **Reply in the same language as the user.**
- Check if a `meta-ads-strategy` or `google-ads-strategy` skill is available. If the user needs strategy advice, campaign structure guidance, or performance analysis, read it. If they just need to execute operations, skip it.

## With strategy skills

The [meta-ads-strategy](https://github.com/adkit-so/skills) and [google-ads-strategy](https://github.com/adkit-so/skills) skills provide advertising strategy: campaign structure, budget management, creative best practices, audience targeting, and performance analysis. Use them to decide _what_ to build, then use AdKit to _execute_ it.
