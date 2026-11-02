---
name: research-reports
description: Gather cited evidence from authorized sources and create reproducible reports.
priority: P0
category: productivity
status: builtin-guidance
---

# Research & Reports

**Scope:** Browser Operator + existing file tools. **Source:** https://github.com/microsoft/playwright-mcp

## Workflow

Define a precise research question, time window, and trustworthy sources. Read page text via existing authorized browser tools where possible; for bulk web automation opt-in to Browser Operator. Maintain source URLs and timestamps; separate fact from inference and avoid invented citations. Synthesize clear claims with a supporting evidence table, flag uncertainty and contradicting sources. Deliver Markdown, HTML or a requested artifact in a user-authorized workspace; verify paths, file content and citations. Never scrape sites in violation of user scope or access private pages without explicit authorization.

## Device and permission gates

Required authorization scopes: browser:read, computer:read, computer:write. Scripts, OS/desktop actions, external service side effects, media generation and paid API usage require independent user-approved execution permissions. This skill does not elevate Remote Arc Tool privileges or authorize use of hidden credentials.

## Preflight

Check the engines this skill names before relying on them, with tools you already have (for example `<engine> --version` through start_process, or list_directory on its install folder). Missing executors must be installed explicitly on the correct user device. A Skill being built-in is NOT evidence an engine is present.

## Evidence of completion

Report input constraints, executed tools and device, verified output path/result, permissions used, cost (if known) and failures. Do not imply successful execution from merely writing a plan.
