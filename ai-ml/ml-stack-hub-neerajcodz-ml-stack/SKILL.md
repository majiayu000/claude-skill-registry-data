---
name: ml-stack-hub
description: Manage Hugging Face or repository artifacts when a user asks to browse revisions, inspect cards, upload files, commit, open a PR, create a discussion, configure a webhook, or publish a model, dataset, Space, or trace; keep writes approval-gated and URLs revision-pinned.
---

# Hub and repository lifecycle

Require artifact type and ID, exact revision, intended operation, license and metadata, visibility, files, provenance, destination, and explicit approval for every write or external notification.

## Workflow

1. Resolve model, dataset, Space, or repository identity to an exact URL and revision; distinguish mutable main branches from immutable commits/tags.
2. Inspect cards, metadata, license, README, file manifest, and existing provenance before proposing changes.
3. Keep traces and sensitive artifacts private by default; redact secrets and personal data.
4. Treat uploads, commits, PRs, discussions, webhooks, publication, and visibility changes as separate approval-gated operations. If no matching runtime operation exists, return a bounded plan with exact API/CLI intent and expected response.
5. Hand immutable URLs, hashes, metadata, and approval evidence to `ml-stack-deployment` or `ml-stack-audit`.

## Outputs and abstention

Never claim a write, PR, discussion, webhook, or publication occurred without an observed result. Abstain when revision, license, destination, or approval is missing. Next owner: `ml-stack-deployment` for serving release, `ml-stack-tracking` for private traces, or `ml-stack-audit` for final artifact reconciliation.

See [Hub revisions](references/hub-revisions.md), [cards and metadata](references/cards-and-metadata.md), [repository and PR policy](references/repo-and-pr-policy.md), and [trace privacy](references/trace-privacy.md).
