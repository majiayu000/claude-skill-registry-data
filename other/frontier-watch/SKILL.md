---
name: frontier-watch
description: Track and verify new research labs, teams, model releases, agent infrastructure, MCP servers, skill libraries, and emerging technical directions for PaperTrace. Use when building a watchlist or publishing a frontier update.
---

# Frontier Watch

Find early signals that may deserve a researcher's attention before they become established literature.

## What belongs

- a newly launched lab, institute, research startup, or cross-institution program;
- a major researcher move that changes a team's technical direction;
- a new model family, meaningful version, retirement, or migration deadline;
- research infrastructure such as an MCP server, agent harness, skill library, index, dataset, evaluation suite, or reproducibility system;
- a new research direction with multiple independent technical signals.

Routine marketing, minor UI updates, and unverified rumors do not belong.

## Verification

Resolve the entity before writing. Nicknames, transliterations, building names, and lab names are easy to confuse. Require at least one primary source and record the canonical name, URL, date, people, focus, and current status. If an example such as “N1 Lab” cannot be matched confidently, keep it in a clarification queue rather than publishing a guessed entity.

For model lifecycle news, distinguish ChatGPT/product availability from API availability. Include the exact model identifier and effective date when available.

## Frontier card

Produce a compact record:

```yaml
name:
type: lab | team | model | infrastructure | direction
domain:
announced_at:
canonical_url:
what_changed:
why_watch:
people_or_orgs: []
evidence: []
attention_budget: skim | read | deep_dive
next_check_at:
confidence: high | medium | low
```

Set `next_check_at` for early announcements that lack a paper, repository, product, or staffing page. Do not present a low-confidence record as published news.

## Source layering

Use official announcements, papers, repositories, and documentation as evidence. Use X, Xiaohongshu, newsletters, bloggers, and public accounts to detect attention and expert interpretation. Make the distinction visible in the published card.
