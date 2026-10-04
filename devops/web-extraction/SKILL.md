---
name: web-extraction
description: Extract specific information from a URL — main content, article text, structured fields — without full scraping infrastructure.
category: web
aliases:
- extract-from-url
- article-extraction
- main-content
triggers:
- extract the main content from this page
- pull the article text
- get the text from this URL
keywords:
- extract
- article
- main
- content
- page
- readability
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- article
- content
- extract
- extraction
- main
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

# Web Extraction

## Purpose

Pull the main textual content (or specific fields) from a single URL quickly. Lightweight
alternative to full scraping for one-off needs.

## When to Use

- User shares a URL and wants the content
- User wants a clean reading view of a page
- User wants specific fields from a known page structure

## Source

Custom skill, written for this library.

## Notes

Lighter than `web-scraping`. For multi-page or large-scale extraction, use scraping instead.

## When NOT to Use

Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.

## Capabilities

- Apply the web-extraction workflow consistently.
- Produce a clear, reviewable result.
- Surface assumptions, constraints, and unresolved risks.

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

Requests that should activate this skill include: "extract the main content from this page"; "pull the article text"; "get the text from this URL".

## Safety

- Preserve user data and existing work.
- Confirm before destructive or externally visible actions.
- Do not expose credentials or claim unverified results.
