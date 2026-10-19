---
name: changelog-writer
description: Use when writing release notes, a CHANGELOG.md entry, a version summary or "what's new" text from git history, merged pull requests or tickets, or deciding the next semantic version number.
---

# Changelog Writer

## Overview

Release notes tell users what changed for them and what they must do. Build them from the real history between two versions, group by impact, and write in the reader's language, not in commit-speak.

## Method

1. **Find the range:** last release tag to now — `git describe --tags --abbrev=0`, then `git log <tag>..HEAD --oneline --no-merges`. With GitHub: `gh pr list --state merged --search "merged:>=<date>"` or `gh release view`.
2. **Read each change**, not just the subject line, when the impact is unclear (`git show <sha> --stat`).
3. **Classify** each change: Added, Changed, Deprecated, Removed, Fixed, Security (Keep a Changelog). Drop internal-only changes (refactors, CI, tests) unless the audience is developers of the project.
4. **Decide the version** (Semantic Versioning): any breaking change → major; new backward-compatible feature → minor; only fixes → patch.
5. **Rewrite for the audience:** user-facing benefit first, one line each, link the PR or issue.
6. **Write breaking changes with migration steps.**
7. **Follow the existing CHANGELOG.md style** if the project has one.

## Format

```markdown
## [2.4.0] - 2026-10-16

### Added
- Export orders to CSV from the Orders page. (#412)

### Changed
- Search now matches partial words. (#405)

### Fixed
- Coupon discount no longer disappears when the cart quantity changes. (#398)

### Security
- Upgrade `jsonwebtoken` to 9.0.2 to fix token verification bypass. (#401)

### Breaking changes
- `GET /api/orders` now returns paginated results. Read items from `data` and
  pass `cursor` to fetch the next page. (#410)
```

Dates in ISO format. Newest version at the top. Omit empty sections.

## Common mistakes

- Copying commit subjects ("fix stuff", "wip") into release notes.
- Hiding breaking changes inside "Changed" with no migration steps.
- Listing internal refactors that users do not care about.
- Choosing a minor version for a release that breaks clients.
- Mentioning features from unmerged branches.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
