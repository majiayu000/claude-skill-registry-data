---
name: seo
description: Search engine optimization audits — on-page, technical, content, and link analysis with prioritized recommendations.
category: web
aliases:
- search-engine-optimization
- site-audit
triggers:
- SEO audit
- check this page for SEO
- improve SEO
- meta tags
- search rankings
keywords:
- seo
- search
- ranking
- meta
- keyword
- on-page
- technical
- audit
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- meta
- ranking
- search
- seo
- web
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# SEO

## Purpose

Audit a site or page for SEO: on-page elements, technical issues, content quality, and
links. Produce a prioritized list of recommendations.

## When to Use

- User wants to improve search rankings
- User has launched a new page / site
- User asks for an SEO audit

## When NOT to Use

- The user wants paid ads / SEM (route to general marketing)

## Capabilities

- On-page checks (titles, meta, headings, content quality)
- Technical checks (sitemap, robots, canonical, structured data, performance)
- Content audits
- Internal / external link suggestions

## Safety

- Don't recommend black-hat SEO
- Don't promise rankings

## Source

Custom skill, written for this library.

## Notes

Pairs with `accessibility-testing` (related technical audit).

## Inputs

- The user's goal and desired output.
- Relevant source material, constraints, and environment details.
- Acceptance criteria when available.

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "SEO audit"; "check this page for SEO"; "improve SEO".
