---
name: linkedin
description: Use when automating LinkedIn from the command line - fetching profiles, searching people and companies, sending messages and connection requests, posting, reacting, commenting, and extracting people/company/post data via the linkedin CLI.
---

# LinkedIn Automation

## Overview

Drive LinkedIn from the command line with the `linkedin` CLI, powered by Linked API cloud browsers. Fetch and search profiles and companies, send messages and connection requests, publish posts, react and comment, run Sales Navigator searches, and extract structured data about people, companies, and posts.

## When to Use

Use this skill when an agent needs to interact with LinkedIn programmatically: outreach at scale, lead research, network management, content publishing, or data extraction.

## Capabilities

- Fetch and search: profiles, companies, people search, Sales Navigator search
- Engage: send messages, connection requests, reactions, comments
- Publish: create posts
- Extract: structured data about people, companies, and posts

## Do not use

Do not use this skill to:
- Bypass LinkedIn access controls, rate limits, or account security
- Store or expose LinkedIn credentials, session cookies, or access tokens
- Send messages, connection requests, reactions, comments, or posts without the user's explicit approval

## Instructions

1. Confirm the LinkedIn action, target, and intended audience before any write operation.
2. Keep Linked API credentials in the user's secure environment; use placeholders in examples.
3. Prefer read-only profile, company, search, and extraction operations until the user approves a write.
4. Summarize the target and content and obtain confirmation immediately before sending, posting, or changing data.
5. Respect LinkedIn policies, consent, privacy, and rate limits; stop when authentication or access is unavailable.

## Notes

Each command runs a real cloud browser through Linked API, so operations take seconds to minutes rather than being instant. Requires a Linked API account and tokens. Docs: https://linkedapi.io
