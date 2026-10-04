---
name: Cloud Storage
slug: cloud-storage
version: 1.0.1
description: Manage files across cloud providers with authentication, cost awareness, and multi-provider operations.
changelog: Added When to Use section for consistency
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

User needs to upload, download, sync, or manage files across cloud storage providers. Agent handles multi-provider operations with cost awareness.

## Quick Reference

| Topic | File |
|-------|------|
| Provider-specific patterns | `providers.md` |
| Authentication setup | `auth.md` |
| Cost calculation | `costs.md` |

## Scope

This skill covers operational cloud storage tasks across providers:
- S3, GCS, Azure Blob, Backblaze B2, Cloudflare R2
- Google Drive, Dropbox, OneDrive, iCloud

For storage architecture decisions, see `storage` skill.
For S3-specific deep patterns, see `s3` skill.

## Critical Rules

1. **Verify operations completed** — API 200 ≠ success; check file exists with correct size/checksum
2. **Calculate ALL costs before large transfers** — egress fees often exceed storage costs; check `costs.md`
3. **Never delete without backup verification** — confirm backup exists AND is restorable before removing source
4. **Handle partial failures** — long operations fail mid-way; implement checkpoints and resume logic
5. **Rate limits vary wildly** — Google 750GB/day upload, Dropbox batch limits, S3 3500 PUT/s per prefix

## Authentication Traps

- **OAuth tokens expire** — refresh before long operations, not during
- **Service account ≠ user account** — different quotas, permissions, audit trails
- **Wrong region/endpoint** — S3 bucket in `eu-west-1` won't work with `s3.amazonaws.com`
- **MFA required** — some operations need session tokens, plan for interactive auth

## Multi-Provider Gotchas

| Concept | Translates differently |
|---------|----------------------|
| Shared folder | Drive "Shared with me" ≠ Dropbox "Team Folders" ≠ OneDrive "SharePoint" |
| File ID | Drive uses IDs; Dropbox uses paths; S3 uses keys |
| Versioning | S3 explicit enable; Drive automatic; Dropbox 180 days |
| Permissions | S3 ACLs + policies; Drive roles; Dropbox link-based |

## Before Any Bulk Operation

- [ ] Estimated time calculated (size ÷ bandwidth)
- [ ] Rate limits checked for both source AND destination
- [ ] Cost estimate including egress + API calls
- [ ] Checkpoint/resume strategy for failures
- [ ] Verification method defined (checksum, count, spot-check)
