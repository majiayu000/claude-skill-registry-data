---
name: patch-notes
description: "Generate release notes from git history, sprint data, and internal changelogs. Game: player-facing patch notes. Product: developer-facing release notes with API/CLI/UI categories."
argument-hint: "[version] [--style brief|detailed|full] [--audience players|developers|all]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash
model: haiku
agent: community-manager
---

## User Guide

- When to use: Generate release notes from git history, sprint data, and internal changelogs. Game: player-facing patch notes. Product: developer-facing release notes with API/CLI/UI categories.
- Inputs: Command arguments: `/patch-notes [version] [--style brief|detailed|full] [--audience players|developers|all]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Detection

**Required Read before domain-dependent routing:** read `CLAUDE.md` and
`standards/technical-preferences.md`, the existing explicit domain decision for
the current scope, and any existing `design/cdd/game-concept.md` or
`design/cdd/product-concept.md` bodies. Read actual configuration before deciding
what the absence of a concept means. Filenames, copied templates, placeholders
and shared file extensions do not establish a domain.

In technical preferences, read populated legacy Product sections as valid aliases:
`Language & Framework` supplies language/framework/runtime choices;
`Platform & Deployment` supplies targets/deployment; `Agent Routing`, including
its `File Extension Routing`, supplies specialist routing in its owning domain.
Compare their actual values with `Product Stack` and applicable concept/decision
evidence. A missing parallel section does not erase valid configured facts or
require relocating them. Conflicting values block the affected route.

Classify the current scope after these reads:

- **Game**: consistent substantive Game concept/decision evidence, or actual
  configured engine/domain plus Game behavior evidence, supports `[Game]` paths.
- **Product**: consistent substantive Product concept/decision evidence or actual
  configured Product facts supports `[Product]` paths. Populated legacy
  TypeScript/Bun API/CLI targets and Product specialist routing, for example,
  remain Product without a concept or a new `Product Stack` section.
- **Unknown**: evidence is insufficient, conflicting or mixed without a concrete
  governing scope. Resolve Game or Product using an existing scoped decision or
  confirmation from the user/configured project lead before dependent branches.
  Both concept filenames do not select a branch; independent neutral reporting
  continues while the affected domain-specific work waits.

Record the chosen domain and the actual source sections/values supporting it.
Never silently default to Game. Missing/inaccessible required configuration or
branch inputs leaves the affected check Incomplete; domain selection alone does
not prove runtime availability, test execution, readiness or completion.

---

## Phase 1: Parse Arguments

- `version`: the release version to generate notes for (e.g., `1.2.0`)
- `--style`: output style — `brief` (bullet points), `detailed` (with context), `full` (with developer commentary). Default: `detailed`.
- `--audience`: **[Game]** `players` (default). **[Product]** `developers` (for API/CLI users), `users` (for end-user features), `all` (both). Default: `developers` for product, `players` for game.

If no version is provided, ask the user before proceeding.

---

## Phase 2: Gather Change Data

- Read the internal changelog at `production/releases/[version]/changelog.md` if it exists
- Also check `docs/CHANGELOG.md` for the relevant version entry
- Run `git log` between the previous release tag and current tag/HEAD as a fallback
- Read sprint retrospectives in `production/sprints/` for context
- **[Game]** Read any balance change documents in `design/balance/`
- **[Game]** Read bug fix records from QA if available
- **[Product]** Read migration files and API spec diffs if available

**If no changelog data is available** (neither `production/releases/[version]/changelog.md`
nor a `docs/CHANGELOG.md` entry for this version exists, and git log is empty or unavailable):

> "No changelog data found for [version]. Run `/changelog [version]` first to generate the
> internal changelog, then re-run `/patch-notes [version]`."

Verdict: **BLOCKED** — stop here without generating notes.

---

## Phase 2b: Detect Tone Guide and Template

**Tone guide detection** — before drafting notes, check for writing style guidance:

1. Check `standards/technical-preferences.md` for any "tone", "voice", or "style"
   fields or sections.
2. Check `docs/PATCH-NOTES-STYLE.md` if it exists.
3. **[Game]** Check `design/community/tone-guide.md` if it exists.
4. If any source contains tone/voice/style instructions, extract them and apply
   them to the language and framing of the generated notes.
5. If no tone guidance is found anywhere, default to domain-appropriate tone:
   - **[Game]** Player-friendly, non-technical language; enthusiastic but not hyperbolic;
     focus on what the player experiences, not what the developer changed.
   - **[Product]** Developer-friendly, precise language; include breaking changes
     prominently; include migration steps; focus on what changed and why.

**Template detection** — check whether a release notes template exists:

1. Glob for `docs/patch-notes-template.md` and `templates/patch-notes-template.md`.
2. If found at either location, read it and use it as the output structure for Phase 4.
3. If not found, use the built-in style templates as defined in Phase 4.

---

## Phase 3: Categorize and Translate

### [Game] Player-Facing Categories

Categorize all changes into player-facing categories:

- **New Content**: new features, maps, characters, items, modes
- **Gameplay Changes**: balance adjustments, mechanic changes, progression changes
- **Quality of Life**: UI improvements, convenience features, accessibility
- **Bug Fixes**: grouped by system (combat, UI, networking, etc.)
- **Performance**: optimization improvements players might notice
- **Known Issues**: transparency about unresolved problems

Translate developer language to player language:

- "Refactored damage calculation pipeline" → "Improved hit detection accuracy"
- "Fixed null reference in inventory manager" → "Fixed a crash when opening inventory"
- "Reduced GC allocations in combat loop" → "Improved combat performance"
- Remove purely internal changes that don't affect players
- Preserve specific numbers for balance changes (damage: 50 → 45)

### [Product] Developer-Facing Categories

Categorize all changes into developer/user-facing categories:

- **Breaking Changes**: API changes that require consumer updates, removed endpoints, changed behaviour
- **New Features**: new endpoints, new CLI commands, new SDK methods, new capabilities
- **Improvements**: performance gains, error message improvements, documentation updates
- **Bug Fixes**: grouped by component (API, CLI, SDK, UI)
- **Deprecations**: features/endpoints that will be removed in a future version (with timeline)
- **Security**: security fixes (include CVE references if applicable)
- **Dependency Updates**: notable dependency changes (major versions, security patches)
- **Migration Guide**: step-by-step instructions for upgrading (if breaking changes exist)
- **Known Issues**: transparency about unresolved problems

Translate developer-internal language to release note language:

- Internal refactoring that doesn't affect the API surface → omit
- "Changed the auth middleware" → "Authentication now requires `X-API-Key` header (see migration guide)"
- Include specific error code changes, response shape changes, CLI flag renames
- Always state upgrade impact: "No action required" / "Action required: [what to do]"

---

## Phase 4: Generate Release Notes

### [Game] Game Patch Notes Templates

#### Brief Style
```markdown
# Patch [Version] — [Title]

**New**
- [Feature 1]
- [Feature 2]

**Changes**
- [Balance/mechanic change with before → after values]

**Fixes**
- [Bug fix 1]
- [Bug fix 2]

**Known Issues**
- [Issue 1]
```

#### Detailed Style
```markdown
# Patch [Version] — [Title]
*[Date]*

## Highlights
[1-2 sentence summary of the most exciting changes]

## New Content
### [Feature Name]
[2-3 sentences describing the feature and why players should be excited]

## Gameplay Changes
### Balance
| Change | Before | After | Reason |
| ---- | ---- | ---- | ---- |
| [Item/ability] | [old value] | [new value] | [brief rationale] |

### Mechanics
- **[Change]**: [explanation of what changed and why]

## Quality of Life
- [Improvement with context]

## Bug Fixes
### Combat
- Fixed [description of what players experienced]

### UI
- Fixed [description]

### Networking
- Fixed [description]

## Performance
- [Improvement players will notice]

## Known Issues
- [Issue and workaround if available]
```

#### Full Style
Includes everything from Detailed, plus:
```markdown
## Developer Commentary
### [Topic]
> [Developer insight into a major change — why it was made, what was considered,
> what the team learned. Written in first-person team voice.]
```

### [Product] Product Release Notes Templates

#### Brief Style
```markdown
# Release [Version] — [Title]

**Breaking Changes**
- [Change requiring consumer action — with migration link]

**New**
- [Feature 1]
- [Feature 2]

**Fixes**
- [Bug fix 1]

**Deprecations**
- [Deprecated feature] — will be removed in [version/date]
```

#### Detailed Style
```markdown
# Release [Version] — [Title]
*[Date]*

## Highlights
[1-2 sentence summary of the most significant changes]

## Breaking Changes
| Change | Before | After | Migration |
| ------ | ------ | ----- | --------- |
| [API/CLI change] | [old behavior] | [new behavior] | [link to migration guide or steps] |

## New Features
### [Feature Name]
[What it does, how to use it, link to docs]

## Improvements
- [Improvement with measurable impact if applicable]

## Bug Fixes
### API
- Fixed [description of observable symptom]

### CLI
- Fixed [description]

### UI
- Fixed [description]

## Deprecations
| Feature | Deprecated In | Will Be Removed In | Replacement |
| ------- | ------------ | ------------------ | ----------- |
| [feature] | [this version] | [target version] | [what to use instead] |

## Security
- [Fix description — include CVE if applicable]

## Dependency Updates
| Dependency | Old | New | Notes |
| ---------- | --- | --- | ----- |
| [name] | [old] | [new] | [why upgraded] |

## Known Issues
- [Issue and workaround if available]
```

#### Full Style
Includes everything from Detailed, plus:
```markdown
## Developer Commentary
### [Topic]
> [Developer insight into a major change — why it was made, trade-offs considered.
> Written in first-person team voice.]

## Migration Guide
### Upgrading from [old version] to [new version]
1. [Step-by-step migration steps]
2. [Configuration changes needed]
3. [Verify migration with these commands/checks]
```

---

## Phase 5: Review Output

**[Game]** Check the generated notes for:
- No internal jargon (replace technical terms with player-friendly language)
- No references to internal systems, tickets, or sprint numbers
- Balance changes include before/after values
- Bug fixes describe the player experience, not the technical cause
- Tone matches the game's voice (adjust formality based on game style)

**[Product]** Check the generated notes for:
- Breaking changes are prominently flagged with migration steps
- Deprecations include timeline and replacement
- Bug fixes describe the observable symptom, not the root cause
- Links to docs/migration guides are functional
- No exposed internal paths, credentials, or infrastructure details
- Upgrade impact is clearly stated for each change

---

## Phase 6: Save Release Notes

Present the completed release notes to the user along with: a count of changes by category, and any internal changes that were excluded (for review).

Ask: "May I write these release notes to `docs/patch-notes/[version].md`?"

If yes, write the file to `docs/patch-notes/[version].md`, creating the directory
if needed. Also write to `production/releases/[version]/patch-notes.md` as the
internal archive copy.

---

## Phase 7: Next Steps

Verdict: **COMPLETE** — release notes generated and saved.

- Run `/release-checklist` to verify all other release gates are met before publishing.
- **[Game]** Share the patch notes draft with the community-manager for tone review before posting publicly.
- **[Product]** Share the release notes draft with the product owner and developer relations for review before publishing.
