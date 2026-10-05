---
name: release-notes
displayName: Release Notes Generator
tagline: Automatically generate release notes from merged PRs, commits, and resolved issues.
description: |
  Generates well-formatted release notes by analyzing merged pull requests,
  commit messages, and resolved issues since the last release. Categorizes
  changes into features, bug fixes, improvements, and breaking changes.
  Supports multiple output formats including markdown, Slack, and email.
department:
  - Engineering
  - Product
use_cases:
  - Release Management
  - Documentation
  - Communication
tools_required:
  - GitHub MCP
  - Slack MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - GitHub Copilot
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Generate release notes for v2.4.0 (since tag v2.3.0).
  Format for both GitHub release and Slack announcement.
exampleOutput: |
  Release Notes — v2.4.0

  NEW FEATURES
  - Add real-time collaboration for documents (#342)
  - Support SSO with SAML 2.0 (#338)
  - New dashboard widgets for team metrics (#335)

  BUG FIXES
  - Fix memory leak in WebSocket handler (#340)
  - Resolve timezone issues in scheduling (#337)
  - Fix CSV export encoding for non-ASCII characters (#334)

  IMPROVEMENTS
  - Reduce API response time by 40% (#341)
  - Upgrade to Node.js 22 LTS (#336)

  BREAKING CHANGES
  - Remove deprecated /api/v1/users endpoint (#339)

  Contributors: @alice, @bob, @carol, @dave (12 PRs merged)
---

# Release Notes Generator

Automatically generate release notes from merged PRs, commits, and resolved issues.

**Integrations:** GitHub, Slack

## When to Use

- The team is preparing a release and needs formatted release notes
- The user wants to summarize changes since the last release
- The user mentions "release notes", "changelog", or "release summary"

## Steps

### Step 1: Identify Release Scope

Determine the commit range (since last tag or specified date).

### Step 2: Categorize Changes

Group PRs and commits into features, fixes, improvements, and breaking changes.

### Step 3: Format and Distribute

Generate release notes in the requested formats and post to channels.

## Output

Deliver:
- Formatted release notes (Markdown, Slack, email)
- Contributor list
- Breaking changes summary
