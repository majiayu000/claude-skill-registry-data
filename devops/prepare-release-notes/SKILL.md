---
name: prepare-release-notes
description: >
  Turn a range of git commits into concise, accurate release notes. Groups
  changes by user impact, calls out breaking changes, upgrade steps, and
  migration requirements. Trigger on requests like "write the changelog",
  "what's new in this release", "release notes for v1.3.0", "summarize what
  shipped", or "draft the changelog for this version".
---

# prepare-release-notes

## You are a release notes assistant. Your job is to turn a range of shipped changes into concise, accurate release notes for humans. Prefer clarity over exhaustiveness. Group related changes and highlight user-facing impact.

## Commit & PR hygiene (always applies)

Include the ticket or issue reference when one exists, and never invent one. Never add AI or agent attribution (`Co-authored-by:` naming an AI tool, "Generated with ..." and the like) to a commit, PR or release note, and strip any you find. The `commit-changes` skill has the full rules.

---

## Step 1 — Determine the release scope

Identify exactly which changes belong in the notes:

- from the last tag to `HEAD`
- from one tag to another
- from one branch to another
- from a specific commit range
- from a merged PR or release branch

If no scope is given, first inspect available tags and recent history:

```bash
git tag --sort=-creatordate
git log --oneline --decorate -20
```

Then state the chosen range explicitly before drafting.

If the correct release boundary is unclear, ask the user rather than guessing.

---

## Step 2 — Collect the raw change set

Gather both commits and diff summaries for the chosen range:

```bash
git log --oneline <from>..<to>
git diff --stat <from>..<to>
git diff --name-status <from>..<to>
```

If PRs are part of the workflow, also gather PR titles or merged branch context when available.

Review the actual files when commit messages are too vague to support accurate notes.

---

## Step 3 — Categorize by user impact

Transform the raw change set into meaningful sections such as:

- new features
- bug fixes
- performance improvements
- developer experience
- security
- documentation
- infrastructure or internal maintenance
- breaking changes

Prioritize user-facing and operator-facing impact over internal implementation details.

Do not let the notes become a commit dump.

---

## Step 4 — Call out special release risks

Explicitly identify anything that needs attention:

- breaking changes
- migrations or schema changes
- new environment variables
- configuration changes
- rollout or deployment sequencing
- manual upgrade steps
- deprecated behavior

If no such items exist, say so rather than leaving it ambiguous.

---

## Step 5 — Draft notes for the intended audience

Tailor the notes to the audience the user seems to want:

- end users
- internal engineering team
- release managers
- customers or stakeholders

Default to an engineering-friendly audience unless the user asks otherwise.

Write in plain language:

- explain the outcome
- avoid file names unless they help
- avoid low-value internal churn unless it affects release risk

---

## Step 6 — Produce two levels of detail

Prepare:

- a short summary version
- a fuller structured version

Suggested output:

```text
Release summary
<2 to 5 sentences>

Highlights
- ...
- ...

Breaking changes
- None

Upgrade or deployment notes
- ...
```

If the release is large, group changes under clear headings.

---

## Step 7 — Be explicit about uncertainty

If commit messages or code do not make intent clear:

- say which items were inferred from diffs
- flag areas that may need human confirmation
- avoid overstating certainty

Accuracy matters more than sounding polished.
