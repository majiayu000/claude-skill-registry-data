---
name: competitor-research
description: Research competitor positioning with read-only web and local memory.
risk: low
required_tools:
  - web.search
  - web.fetch
  - memory.search
suggested_subagent: researcher
business_domain: market-research
cadence: weekly, monthly
approval_required_for:
  - browser.click_proposed
  - memory.propose
---

# Competitor Research

Use this skill when the user asks to research competitors, pricing, menus, positioning, or promotions.

Rules:
- Use configured read-only search/fetch providers.
- Separate verified facts from inference.
- Do not scrape private pages, log in, submit forms, or message competitors.
