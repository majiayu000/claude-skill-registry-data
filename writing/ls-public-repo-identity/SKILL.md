---
name: ls-public-repo-identity
description: "Public repo identity - use in README and published repos. For real identity details, use a local-only identity file that is not committed. Use when editing README*, CONTRIBUTING*."
metadata:
  version: "1.2"
---

# Public repo identity

Use a **local identity file** and this committed stub so the framework repo stays generic (no PII).

- **Canonical committed source:** This skill is the committed public identity stub for LocalSetup. Keep it generic so README, CONTRIBUTING, and published repo files do not inherit maintainer-specific names, contact details, or organization data.
- **Canonical local source:** Put real identity details in a local-only file loaded by your agent platform, such as `.cursor/rules/local-identity.mdc` for Cursor-style rules or the equivalent local rules/instructions path for another platform. If that path is not already ignored by the repo, add it to `.git/info/exclude` or another local-only ignore file before writing personal details.
- **Template guidance:** LocalSetup does not ship a separate public identity template. To create a local identity file, copy the fields you need from this stub and fill them in only in the local-only file.

Do not put real names, contact info, or org details in this file; they belong in local-identity.mdc (not committed).

## Rule ownership

This skill owns public identity behavior for README, CONTRIBUTING, SUPPORT, SECURITY, package metadata, and other publishable surfaces.

- Keep committed identity generic unless the user explicitly provides public identity text for the repo.
- Keep private identity files local-only and ignored.
- When publishing, combine this skill with `ls-github-publishing-workflow` so identity, license, contact, and repository links are checked together.
