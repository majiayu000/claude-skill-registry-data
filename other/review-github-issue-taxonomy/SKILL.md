---
name: review-github-issue-taxonomy
description: Audit labels, milestones, projects, and path-label ownership.
---

# Review GitHub issue taxonomy

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/review-github-issue-taxonomy/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use when the taxonomy itself needs review. Stay read-only unless the caller explicitly authorizes
local configuration edits or a live taxonomy mutation. Read local `AGENTS.md` first.

1. Confirm repository identity. Fetch live labels, descriptions, colors, usage, milestones, open and
   closed projects, and their current scope.
2. Identify automation-owned labels. Inspect local label automation before recommending a rename,
   deletion, or rule change.
3. Audit aliases, ambiguity, unused labels, missing descriptions, color consistency, milestone
   overlap, delivery gaps, and path-label coverage. Audit projects against
   [github-issue](../github-issue/SKILL.md):
   - A milestone theme duplicated across repositories is a candidate project.
   - A project that holds only routine, non-initiative work is a candidate milestone. Repository
     count is not the signal.
   - Flag a project with no description, an empty or stale project, a closed project with open
     items, and an issue that belongs to more than one project.
   - Flag auto-add of a parent issue's sub-issues where the at-most-one-project rule applies. It
     can put an item in a second project.
4. Return exact recommendations with migration impact. Separate safe cleanup from decisions that
   need product or scheduling judgment. Applying an existing label is not taxonomy creation and
   needs no separate approval from the authorized issue operation.
5. Before creating a label, stop for explicit approval of its exact repository, name, description,
   and color. Re-fetch current state and apply the taxonomy-definition gate from
   [github-issue](../github-issue/SKILL.md): require `WRITE`, `MAINTAIN`, or `ADMIN` and the
   label-specific API capability immediately before the approved mutation. `viewerCanCreateIssues`
   applies only to issue creation. Approval for an issue or another label does not transfer.

Do not create or change labels, milestones, projects, issues, or local files for a
recommendation-only request.

Consumer wrapper owns: the repository taxonomy and the local automation file locations.
