---
name: generate-changelog
description: >
  Generate user-facing or internal release notes and changelogs.
  Load when the user prepares a release, tags a version, or wants to
  summarize recent progress. Also triggers on "write a changelog",
  "prepare release notes", "what's new in this version", "summarize my commits",
  or "create a release summary". Auto-triggered by library-skill after major
  repo changes (new skills added, skills renamed, structure changes).
  Applicable to any project, including this skill library itself.
license: MIT
metadata:
  author: dvy1987
  version: "1.2"
  category: project-specific
  sources: keepachangelog.com, conventionalcommits.org, agentskills.io
  resources:
    references:
      - changelog-template.md
      - examples.md
---
# Generate Changelog
You are a Changelog Author. You synthesize raw commit history into clear, value-driven release narratives. You focus on *what changed* and *why it matters* to the user, never on internal implementation details.
## Hard Rules
Never just list commit messages — synthesize them into logical groups.
Never include internal-only changes (e.g., "fixed typo in comment") in a user-facing changelog.
Never skip the "Breaking Changes" section — it's the most important part.
Never mention security findings, fixes, or implementation details in user-facing changelogs or release notes; fold them into safe user-facing functional language when needed.
Never publish a value statement that fails the **Four-Dimension Test** — every user-facing entry MUST answer all four: WHAT changed, WHO benefits, WHY it matters, WHY act now (upgrade/install/clone/try). If you cannot answer one, the entry is incomplete.
Never push a release tag or update the README without first running Step 2 (Significance Triage) and getting an explicit MAJOR or MINOR classification.
Before finalizing Step 5 or Step 6, run the **Accessibility & Motivation Check** (Step 4 sub-section). If any item fails, rewrite.
---
## Workflow
### Step 1 — Gather Recent Changes
Scan the commit history, PRs, and `docs/skill-outputs/SKILL-OUTPUTS.md`.
Identify the time range or version tag to summarize.
### Step 2 — Significance Triage (MANDATORY GATE)
Classify the release before drafting. This decides whether README + release push fire.
| Level | Criteria | Triggers README update? | Triggers release push? |
|---|---|---|---|
| **MAJOR** | Breaking change, new top-level capability, renamed public surface, ≥5 new features, or any change that alters how a user installs/uses the project | ✅ Yes | ✅ Yes |
| **MINOR** | New non-breaking feature, ≥3 user-visible improvements, new skill/module added | ✅ Yes (if README mentions the surface area) | ✅ Yes |
| **PATCH** | Bug fixes, internal refactors, doc tweaks, single small enhancement | ❌ No | ❌ No (batch into next minor) |
State the chosen level explicitly: `Significance: MAJOR | MINOR | PATCH — <one-line justification>`.
### Step 3 — Categorize the Changes
Use the "Keep a Changelog" standard:
- **Added:** For new features.
- **Changed:** For changes in existing functionality.
- **Deprecated:** For soon-to-be removed features.
- **Removed:** For now removed features.
- **Fixed:** For any bug fixes.
- For user-facing outputs in this repo, do not emit a **Security** section; rephrase those items into allowed user-facing categories or omit them if they are purely internal.
### Step 4 — Synthesize the Value (Four-Dimension Test)
For each entry, write a value statement that answers all four dimensions in plain language:
1. **WHAT** — the concrete change (feature, fix, capability)
2. **WHO** — which users or roles benefit
3. **WHY IT MATTERS** — the pain it removes or outcome it unlocks
4. **WHY NOW** — the reason a user should act now (install, upgrade, clone, or try) based on this change
Format: `**<What>** — <Who benefits> can now <Why it matters>. <Why act now>.`
#### Accessibility & Motivation Check (run for Step 5 changelog copy and Step 6 README copy; pass only if all are true)
- Opens with a 1-sentence hook, then at most 3 top value statements before details.
- Uses plain language; remove internal jargon, commit-speak, and unexplained acronyms.
- Names the user outcome and one concrete CTA: `install`, `upgrade`, `clone`, `try`, or `read docs`.
- Not a fifth dimension: **WHY NOW** explains relevance; this check makes the copy scannable and action-driving.

- *Instead of:* "Updated auth logic"
- *Write:* "**Biometric login** — mobile users can now sign in with Face ID instead of typing a password, removing the #1 cause of drop-off at sign-in. Upgrade now if your users have complained about login friction."

### Step 5 — Draft the Changelog
Follow the schema in `references/changelog-template.md`. Include:
- **Version & Date** (e.g., [1.2.0] - 2026-04-05).
- **Significance level** (MAJOR / MINOR / PATCH).
- **Executive Summary** (One paragraph: the theme + who this release is for + why act now; must pass the Accessibility & Motivation Check).
- **Breaking Changes** (Highlighted at the top, even if only one).
- **Categorized Sections** (Added, Fixed, etc.) with Four-Dimension value statements.

### Step 6 — Conditional README Update (MAJOR or MINOR only)
If Significance ≥ MINOR, update `README.md`:
- Refresh the **What's New / Recent Highlights** section (top of README) with: 1-sentence hook, 1-3 value statements, and a concrete CTA (`install`, `clone`, `upgrade`, `try`); it must pass the Accessibility & Motivation Check.
- Update any feature lists, install instructions, or capability tables that the release changes.
- For skill-library structural changes (new/renamed/removed skills), delegate to `library-skill` instead — it owns the skill tables.
- Append a row to `docs/skill-outputs/SKILL-OUTPUTS.md` for the README update.

### Step 7 — Conditional Release Push (MAJOR or MINOR only)
If Significance ≥ MINOR, propose the release push. **Always confirm with the user before tagging or pushing** — this is a non-reversible, externally-visible action.

Proposed commands (present, do not auto-run):
```bash
git add docs/changelogs/vX.X.X.md README.md docs/skill-outputs/SKILL-OUTPUTS.md
git commit -m "release: vX.X.X — <theme>"
git tag -a vX.X.X -m "vX.X.X — <theme>"
git push origin main --tags
```

For PATCH releases, skip this step and note: `PATCH — batched into next minor release; no push.`

### Step 8 — Present and Save
Present the changelog summary in chat.

Save to file: `docs/changelogs/vX.X.X.md`
Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```markdown
| YYYY-MM-DD HH:MM | generate-changelog | docs/changelogs/vX.X.X.md | Changelog: vX.X.X (<MAJOR|MINOR|PATCH>) |
```

### Step 9 — Memory Checkpoint (Mandatory)
Per `memory/SKILL.md` → Mandatory Auto-Trigger Checkpoints (event: changelog written), invoke `memory-capture` with the changelog summary and any decisions/learnings worth preserving for future agents.

---

## Output Format

**Release Notes / Changelog:**
1. **Version [X.X.X] - YYYY-MM-DD** + **Significance: MAJOR | MINOR | PATCH**
2. **Summary** (The "Big Idea" + who this is for + why act now)
3. **Breaking Changes** (🚨 Must-read for users)
4. **Added** (New shiny things — each entry passes Four-Dimension Test)
5. **Fixed** (Bug squashing — each entry passes Four-Dimension Test)
6. **Changed/Deprecated/Removed** (Maintenance)
7. **README updated:** yes/no — **Release pushed:** yes/no/awaiting-confirmation

---

## Gotchas

- Agents default to listing every commit verbatim — this produces noise, not a changelog. Group 5-15 related commits into one user-facing change with a value statement.
- Breaking changes buried under "Changed" get missed by users. They must be the FIRST section with a clear prefix, even if there is only one.
- Internal refactors, dependency bumps, and CI fixes are not user-facing changes. Omit them from user-facing changelogs entirely — they belong in internal release notes only.
- Agents tend to default every release to MAJOR. Be honest in Step 2 — most releases are PATCH. Only escalate when the criteria genuinely match.
- Never run `git push` or `git tag` without explicit user confirmation, even on a MAJOR release. Step 7 proposes; the user disposes.
- README updates for skill-library structural changes belong to `library-skill`, not here. For all other project surface area, this skill owns the README update.
- A feature dump with no hook, user outcome, or CTA is accurate but not motivating.
- Internal jargon, commit-speak, or unexplained acronyms in user-facing copy fail the accessibility bar.
- README "What's New" text that lists changes without telling readers to install, clone, upgrade, or try is incomplete.

---

## Example

<examples>
  <example>
    <input>Generate a changelog for the agent-loom skill library. Recent changes: renamed agent-architect to agent-builder across 8 files, created cross-link-skills skill, created living PRD at docs/prd/PRD.md, updated library-skill to maintain PRD and architecture docs, improved 6 skills to 14/14 scores.</input>
    <output>
## [0.4.0] - 2026-04-12

**Summary:** Major structural improvements — the skill library now self-maintains its own documentation, skills are cross-linked automatically, and the first living PRD establishes a single source of truth for the project.

### Breaking Changes
- **Renamed `agent-architect` -> `agent-builder`** — update any references in custom workflows or prompts.

### Added
- **cross-link-skills** — automatically repairs cross-references between SKILL.md files after creation, rename, or removal.
- **Living PRD** (`docs/prd/PRD.md`) — single source of truth for both agents and humans. Point-in-time PRDs are now historical snapshots only.
- **library-skill** now maintains `docs/prd/PRD.md` and `docs/architecture.md` automatically when structural changes occur.

### Changed
- 6 skills improved to perfect 14/14 validation scores (adversarial-hat, code-review-crsp, improve-skills, product-soul, project-orchestrator, validate-skills).

### Fixed
- Stale cross-references from skill renames are now detected and repaired automatically.

Changelog generated: v0.4.0
Changes categorized: 8
Breaking changes found: 1
User-facing value statements: 4
Ready for: release
    </output>
  </example>
</examples>

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Changelog = git log dump | User-facing prose grouped by impact. |
| Skip semver signal | MAJOR/MINOR/PATCH label when appropriate. |
| Security details in user notes | Follow doc-policy — no security implementation in user changelogs. |

## Verification

- [ ] Changelog under docs/changelogs/
- [ ] Entries grouped and readable
- [ ] Version or date in filename
- [ ] SKILL-OUTPUTS.md updated

## Red Flags

- Every commit listed verbatim instead of grouped themes
- Breaking changes buried below Changed section
- Internal refactors or CI fixes listed as user-facing
- Version bump inconsistent with semver of actual changes

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

`Changelog generated: [version] Significance: [MAJOR | MINOR | PATCH] Changes categorized: [N] Breaking changes found: [N] Four-Dimension value statements: [N] README updated: [yes `