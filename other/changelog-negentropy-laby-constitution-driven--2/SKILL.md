---
name: changelog
description: "Auto-generates a changelog from git commits, sprint data, and design documents. Game: player-facing content, gameplay, balance. Product: API changes, migrations, dependency updates."
argument-hint: "[version|sprint-number]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write
context: |
  !git log --oneline -30 2>/dev/null
  !git tag --list --sort=-v:refname 2>/dev/null | head -5
model: haiku
---

## User Guide

- When to use: Auto-generates a changelog from git commits, sprint data, and design documents. Game: player-facing content, gameplay, balance. Product: API changes, migrations, dependency updates.
- Inputs: Command arguments: `/changelog [version|sprint-number]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Detection

Read `CLAUDE.md`, `standards/technical-preferences.md`, existing scoped domain
decisions, and the substantive bodies of any `design/cdd/game-concept.md` or
`design/cdd/product-concept.md` before selecting domain-dependent paths. Filenames,
placeholders and shared file extensions do not establish the domain.

Populated legacy `Language & Framework`, `Platform & Deployment`, and
`Agent Routing` / `File Extension Routing` sections remain valid Product
configuration alongside `Product Stack`. Read their actual values; a missing new
section or concept does not erase configured TypeScript/Bun API/CLI facts.

- **Game**: consistent substantive Game concept/decision or actual engine/domain
  and Game behavior evidence supports `[Game]` paths.
- **Product**: consistent substantive Product concept/decision or actual Product
  configuration supports `[Product]` paths, including legacy projects without a concept.
- **Unknown**: insufficient, conflicting or mixed evidence leaves the affected
  domain branch unresolved. Use an existing scoped decision or clarify with the
  user/configured project lead. Neutral changelog analysis may continue:
  gather confirmed commit/version/sprint facts and affected paths in conversation,
  with unresolved scope listed. Until the domain is resolved, stop before Phase 3
  Game/Product categorization, domain-specific changelog templates or file output;
  do not choose Game categories as a fallback.

Record the supporting sections and values. Never silently default to Game.
Missing or inaccessible required branch inputs leaves the affected check Incomplete;
domain selection alone does not establish readiness or completion.

---

## Phase 1: Parse Arguments

Read the argument for the target version or sprint number. If a version is given, use the corresponding git tag. If a sprint number is given, use the sprint date range.

Verify the repository is initialized: run `git rev-parse --is-inside-work-tree` to confirm git is available. If not a git repo, inform the user and abort gracefully.

---

## Phase 2: Gather Change Data

Read the git log since the last tag or release:

```
git log --oneline [last-tag]..HEAD
```

If no tags exist, read the full log or a reasonable recent range (last 100 commits).

Read sprint reports from `production/sprints/` for the relevant period to understand planned work and context behind changes.

Read completed design documents from `design/cdd/` for any new features implemented during this period.

---

## Phase 3: Categorize Changes

### [Game] Game Categories

Categorize every change into one of these categories:

- **New Features**: Entirely new gameplay systems, modes, or content
- **Improvements**: Enhancements to existing features, UX improvements, performance gains
- **Bug Fixes**: Corrections to broken behavior
- **Balance Changes**: Tuning of gameplay values, difficulty, economy
- **Known Issues**: Issues the team is aware of but have not yet resolved
- **Miscellaneous**: Changes that do not fit the above categories, or commits whose messages are too vague to classify confidently

### [Product] Product Categories

Categorize every change into one of these categories:

- **New Features**: New endpoints, CLI commands, SDK methods, capabilities
- **Improvements**: Performance gains, error handling improvements, documentation, accessibility
- **Bug Fixes**: Corrections to broken behavior
- **Breaking Changes**: API contract changes, removed endpoints, changed behaviour requiring consumer action
- **Deprecations**: Features scheduled for removal with sunset dates
- **Dependency Updates**: Notable library/framework version changes
- **Security**: Security fixes and vulnerability patches
- **Migrations / Data Changes**: Database schema changes, data transforms
- **Known Issues**: Issues the team is aware of but have not yet resolved
- **Miscellaneous**: Changes that do not fit the above categories

For each commit, check whether the message contains a task ID or story reference
(e.g. `[STORY-123]`, `TR-`, `#NNN`, or similar). Count commits that lack any task reference
and include this count in the Phase 4 Metrics section as: `Commits without task reference: [N]`.

---

## Phase 4: Generate Internal Changelog

### [Game] Game Internal Changelog

```markdown
# Internal Changelog: [Version]
Date: [Date]
Sprint(s): [Sprint numbers covered]
Commits: [Count] ([first-hash]..[last-hash])

## New Features
- [Feature Name] -- [Technical description, affected systems]
  - Commits: [hash1], [hash2]
  - Owner: [who implemented it]
  - Design doc: [link if applicable]

## Improvements
- [Improvement] -- [What changed technically and why]
  - Commits: [hashes]
  - Owner: [who]

## Bug Fixes
- [BUG-ID] [Description of bug and root cause]
  - Fix: [What was changed]
  - Commits: [hashes]
  - Owner: [who]

## Balance Changes
- [What was tuned] -- [Old value -> New value] -- [Design intent]
  - Owner: [who]

## Technical Debt / Refactoring
- [What was cleaned up and why]
  - Commits: [hashes]

## Miscellaneous
- [Change that didn't fit other categories, or vague commit message]
  - Commits: [hashes]

## Known Issues
- [Issue description] -- [Severity] -- [ETA for fix if known]

## Metrics
- Total commits: [N]
- Files changed: [N]
- Lines added: [N]
- Lines removed: [N]
- Commits without task reference: [N]
```

### [Product] Product Internal Changelog

```markdown
# Internal Changelog: [Version]
Date: [Date]
Sprint(s): [Sprint numbers covered]
Commits: [Count] ([first-hash]..[last-hash])

## New Features
- [Feature Name] -- [Technical description, affected modules]
  - Commits: [hash1], [hash2]
  - Owner: [who implemented it]
  - Design doc: [link if applicable]

## Improvements
- [Improvement] -- [What changed technically and why]
  - Commits: [hashes]
  - Owner: [who]

## Bug Fixes
- [BUG-ID] [Description of bug and root cause]
  - Fix: [What was changed]
  - Commits: [hashes]
  - Owner: [who]

## Breaking Changes
- [Change description] -- [Why it was necessary]
  - Migration: [link to migration guide or steps]
  - Affected consumers: [who needs to update]
  - Owner: [who]

## Deprecations
- [Deprecated feature/API] -- Will be removed in [version/date]
  - Replacement: [what to use instead]
  - Owner: [who]

## Dependency Updates
| Dependency | Old | New | Reason |
| ---------- | --- | --- | ------ |
| [name] | [old] | [new] | [why] |

## Security
- [Fix description] -- [CVE or internal reference]
  - Severity: [Critical/High/Medium/Low]
  - Owner: [who]

## Migrations / Data Changes
- [Migration name] -- [What changed in the schema or data]
  - Forward: [tested?]
  - Reverse: [tested?]
  - Owner: [who]

## Miscellaneous
- [Change that didn't fit other categories]
  - Commits: [hashes]

## Known Issues
- [Issue description] -- [Severity] -- [ETA for fix if known]

## Metrics
- Total commits: [N]
- Files changed: [N]
- Lines added: [N]
- Lines removed: [N]
- Commits without task reference: [N]
```

---

## Phase 5: Generate Public-Facing Changelog

### [Game] Player-Facing Changelog

```markdown
# What's New in [Version]

## New Features
- **[Feature Name]**: [Player-friendly description of what they can now do
  and why it is exciting. Focus on the experience, not the implementation.]

## Improvements
- **[What improved]**: [How this makes the game better for the player.
  Be specific but avoid jargon.]

## Bug Fixes
- Fixed an issue where [describe what the player experienced, not what was
  wrong in the code]
- Fixed [player-visible symptom]

## Balance Changes
- [What changed in player-understandable terms and the design intent.
  Example: "Healing potions now restore 50 HP (up from 30) -- we felt
  players needed more recovery options in late-game encounters."]

## Known Issues
- We are aware of [issue description in player terms] and are working on a
  fix. [Workaround if one exists.]

---
Thank you for playing! Your feedback helps us make the game better.
Report issues at [link].
```

### [Product] Developer-Facing Changelog

```markdown
# Changelog: [Version]
*[Date]*

## Breaking Changes
- **[Change]**: [What changed and why]. See [migration guide link] for upgrade steps.

## New Features
- **[Feature Name]**: [What it does, how to use it, link to docs]

## Improvements
- **[What improved]**: [How this benefits users/developers. Be specific.]

## Bug Fixes
- Fixed an issue where [describe the observable symptom]
- Fixed [observable symptom]

## Deprecations
- **[Deprecated feature]**: Will be removed in [version]. Use [replacement] instead.

## Security
- **[Fix]**: [What was fixed, impact]. [CVE reference if applicable].

## Dependency Updates
- [dependency]: [old] → [new]

## Known Issues
- We are aware of [issue description] and are working on a fix.
  [Workaround if one exists.]

---
[Footer with links to docs, migration guide, issue tracker]
```

---

## Phase 6: Output

Output both changelogs to the user. The internal changelog is the primary working document. The public-facing changelog is ready for review and publication.

---

## Phase 7: Offer File Write

After presenting the changelogs, ask the user:

> "May I write this changelog to `docs/CHANGELOG.md`?
> [A] Yes, append this entry (recommended if the file already exists)
> [B] Yes, overwrite the file entirely
> [C] No — I'll copy it manually"

- Check whether `docs/CHANGELOG.md` exists before asking. If it does, default the
  recommendation to **[A] append**.
- If the user selects [A]: append the new internal changelog entry to the top of
  the existing file (newest entries first).
- If the user selects [B]: overwrite the file with the new changelog.
- If the user selects [C]: stop here without writing.

After a successful write: Verdict: **CHANGELOG WRITTEN** — changelog saved to `docs/CHANGELOG.md`.
If the user declines: Verdict: **COMPLETE** — changelog generated.

---

## Phase 8: Next Steps

- Use `/patch-notes [version]` to generate a styled, saved version for public release.
- Use `/release-checklist` before publishing the changelog externally.

### Guidelines

- Never expose internal code references, file paths, or developer names in the public-facing changelog
- Group related changes together rather than listing individual commits
- If a commit message is unclear, check the associated files and sprint data for context
- **[Game]** Balance changes should always include the design reasoning, not just the numbers
- **[Product]** Breaking changes must always include migration steps
- Known issues should be honest — transparency builds trust
- If the git history is messy (merge commits, reverts, fixup commits), clean up the narrative rather than listing every commit literally
