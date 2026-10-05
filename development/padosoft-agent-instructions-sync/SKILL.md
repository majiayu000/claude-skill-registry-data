---
name: padosoft-agent-instructions-sync
description: >-
  Use this skill whenever a file that instructs a coding agent is created, changed or deleted — CLAUDE.md,
  AGENTS.md, a rule or skill folder, a Copilot instructions file, a Gemini or Cursor or Codex configuration
  — in a repository where more than one agent is used. Also when the user says one agent follows a rule the
  others ignore, that a convention was applied by one tool and not another, that an instructions file was
  truncated, or asks how to keep the instruction files aligned. It gives the one-source-many-targets
  contract, the per-target limits that force a transformation, and the checks that catch a target left
  behind. Do not use it to write the content of a rule, nor to build a skill for publication
  (padosoft-skill-creator covers that).
license: MIT
compatibility: >-
  Any repository with instruction files for more than one coding agent. The target-specific constraints are
  stated as classes rather than product names, because they change faster than the rule does.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: A rule one agent knows and the others do not is worse than no rule.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: claude.md, agents.md, copilot, gemini, cursor, instructions, rules, sync, multi-agent
---

# Agent instructions sync

A repository used with more than one coding agent has the same rules written in several places, in formats
that are not interchangeable. Change one and the others keep instructing the old behaviour — silently,
because nothing in a repository fails when two instruction files disagree.

**The rule: one authoritative source, every other file derived from it in the same change. A rule one agent
knows and the others do not is worse than no rule, because the disagreement gets attributed to the code.**

---

## 1. Declare the source and the targets, once

Write the mapping down in the repository, next to the source. It is the contract, and it is the thing that
tells the next person what they are about to leave behind.

| Source (authoritative) | Target A | Target B |
|---|---|---|
| the per-topic rule files | one instruction file each, path-scoped | one section each, appended to a single file |
| the top-level project instructions | the tool's own top-level instructions file | a section in the same single file |
| skills, packaged workflows | not supported — inline the critical part | not supported — inline the critical part |
| subagent definitions | not supported — record the gap | not supported — record the gap |

Two things this table is for: telling you which targets exist at all, and **making the unsupported cells
visible**. A capability that one agent has and another does not is a gap you accept on purpose, not one you
discover when the second agent does the wrong thing.

## 2. The targets are not copies. They are transformations

Each target imposes constraints that change the text, and the constraints are the reason a copy-paste
approach quietly fails.

- **A size limit that truncates.** Some review tools read only the first few thousand characters of an
  instruction file and silently ignore the rest — so the rule at the bottom does not exist. Check the size
  as part of the change, and condense rather than letting it be cut.
- **Path scoping, or none.** One tool applies a file only to matching paths; another applies everything to
  everything. When the target has no scoping, the instruction has to carry its own applicability in the
  text, or it fires where it does not belong.
- **Language.** Pick one language for all instruction files and keep it. Mixed-language instructions are
  read worse by every tool, and they make a diff between source and target unreadable for a human.
- **Condensation is allowed. Contradiction is not.** A target may drop examples, merge sections and lose
  detail. It must never state a different rule from the source — that is how two agents end up enforcing
  opposite conventions on the same file.

## 3. Deletion propagates too

The failure nobody plans for: a rule is removed from the source and left in the targets. An agent then
enforces a convention the team has abandoned, and the person arguing with it has nothing to point at
because the source no longer mentions it.

Create, change, **delete** — all three cross the whole mapping.

## 4. Make the gap detectable

A mapping table maintained by hand rots like any other document. Add whichever of these fits the repository:

- **A check that every source file has its declared targets**, and that no target exists without a source —
  the second half catches the orphan left by a deletion.
- **A size check per target**, failing before the truncating tool silently drops half the file.
- **A marker linking each target back to its source** — a stable identifier in both — so a reader of the
  target can find the authority in one search.

None of this needs a framework. It needs the mapping to exist in a form a script can read: see
**`padosoft-ci-workflow-gates`** for why a manifest that does not enumerate itself stays green while half
the contract is deleted.

## 5. The same discipline for what the instructions quote

An instruction file that names a helper, a path, a command or a flag is documentation, and it rots exactly
like documentation — with the difference that the agent follows the stale instruction **confidently**, which
is worse than having no instruction. See **`padosoft-docs-match-code`**, and treat a rename as a change to
every file that mentions the old name — **`padosoft-contract-changes`** is the same procedure at a different
altitude.

---

## Gotchas

- **Nothing fails when two instruction files disagree.** There is no test, no build, no runtime. The only
  symptom is two agents behaving differently, which gets blamed on the models.
- **The truncated file is the dangerous one**, because it looks present and complete in the editor.
- **"I will sync the others later" means the others are now wrong**, and the person who next reads them has
  no way to know which one is current.
- **A target with no path scoping applies your backend rule to the frontend.** Either say so in the text, or
  accept that the rule fires out of place.
- **Do not let the derived file become the one people edit.** If a target is easier to open than the source,
  it will be edited there, and the next sync silently reverts it. Say in the target that it is generated.

## Checklist

- [ ] The mapping between source and every target is written down in the repository
- [ ] Unsupported capabilities are listed as gaps, not left implicit
- [ ] Every create, change **and** delete crossed the whole mapping in the same change
- [ ] Each target respects its size limit, checked rather than assumed
- [ ] Applicability is carried in the text wherever the target has no path scoping
- [ ] One language across all instruction files
- [ ] No target contradicts the source; condensation only
- [ ] Targets say they are generated, and name their source
- [ ] A check exists for missing targets and for orphaned ones

## Final report

```
Change: <what was created / modified / deleted, in the source>
Targets updated: <file> (<size> / <limit>) · <file> · …
Unsupported: <capability> → <how it was handled, or the accepted gap>
Deletions propagated: yes | no | not applicable
Contradictions checked: <which rules were compared>
Detection: <the check that will catch the next missed target>
```
