---
name: gmail-operations
version: 1.0.0
category: email
description: "Class-level Gmail and email operations: multi-account setup, OAuth, triage, extraction, archiving, attachments, unsubscribe, and touchbase workflows."
tags: [gmail, email, triage, extraction]
---

# Gmail Operations

## When to Use
Use for Gmail/himalaya setup and recurring inbox operations: triage, extraction to repositories, archive hygiene, attachment/document parsing, unsubscribe sweeps, and relationship touchbase.

## Class-Level Workflow
1. Confirm account context and OAuth/token health first.
2. Classify mail by action class: triage, extract/archive, attachment processing, unsubscribe, contact/touchbase.
3. Preserve source message identifiers in extracted artifacts.
4. Keep destructive mail actions batched and reviewable.

## Consolidated Session Learnings

The `references/` directory contains archived narrow skills absorbed during the 2026-04-29 umbrella consolidation pass. Use the subsections below as the class-level index, then open the named reference when a case-specific recipe is needed.
## Absorbed Narrow Skills (2026-04-29)

### `gmail-attachment-to-document`

- Former skill demoted to `references/gmail-attachment-to-document.md`.
- Preserved insight: Download attachments from Gmail threads, parse their content (Excel, PDF), extract structured data, and save to target repos with proper legal scanning.

### `gmail-data-extraction`

- Former skill demoted to `references/gmail-data-extraction.md`.
- Preserved insight: Extract structured data from Gmail emails using REST API (no pip dependencies). Covers inbox scanning, subject line regex extraction, email text parsing, thread-aware drafting, and legal-scan-before-commit workflow.

### `gmail-email-to-repo-extraction`

- Former skill demoted to `references/gmail-email-to-repo-extraction.md`.
- Preserved insight: Extract structured data from Gmail inbox emails, enrich with domain-specific classification, legal-scan against deny list, commit to appropriate repo, then optionally delete originals.

### `gmail-extract-and-clean`

- Former skill demoted to `references/gmail-extract-and-clean.md`.
- Preserved insight: Extract emails from Gmail to /mnt/ace/<repo>/, archive to appropriate workspace-hub external repos, commit, then delete from inbox. Uses email-routing.yaml for sender→repo routing.

### `gmail-extract-archive`

- Former skill demoted to `references/gmail-extract-archive.md`.
- Preserved insight: Extract Gmail data into a structured archive repo, parse attachments, legal scan, then delete from inbox. Single source of truth for all email data across 3 accounts.

### `gmail-headless-oauth`

- Former skill demoted to `references/gmail-headless-oauth.md`.
- Preserved insight: Manual OAuth2 token exchange for Gmail on headless servers. Bypass gmail-mcp-multiauth browser requirement. Generate auth URLs, exchange codes, manage multi-account credentials with auto-refresh.

### `gmail-multi-account`

- Former skill demoted to `references/gmail-multi-account.md`.
- Preserved insight: Multi-account Gmail management via himalaya CLI. Three accounts (aceengineer, achantav, skestates) with distinct triage rules, contact DBs, and tone profiles. Foundation skill for email automation.

### `gmail-touchbase`

- Former skill demoted to `references/gmail-touchbase.md`.
- Preserved insight: Periodic relationship maintenance via email — identify contacts due for outreach, draft personalized check-ins, queue for user approval. Supports per-account tone and cadence.

### `gmail-triage`

- Former skill demoted to `references/gmail-triage.md`.
- Preserved insight: Daily multi-account Gmail inbox triage — scan unread, classify by urgency, cross-reference contacts, generate actionable digest. Supports ace/personal/skestates accounts.

### `gmail-unsubscribe`

- Former skill demoted to `references/gmail-unsubscribe.md`.
- Preserved insight: Identify and batch-unsubscribe from newsletters and marketing emails across Gmail accounts. Scans List-Unsubscribe headers, generates candidates, executes with user approval.

### `contact-manager`

- Former skill demoted to `references/contact-manager.md`.
- Preserved insight: Normalize, classify, and manage contact databases across 3 Gmail accounts. Clean CSV exports, deduplicate, tag categories, flag touchbase/unsubscribe candidates.
