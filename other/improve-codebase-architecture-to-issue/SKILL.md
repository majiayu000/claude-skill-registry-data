---
name: improve-codebase-architecture-to-issue
description: Run improve-codebase-architecture and land the whole audit as one tracker issue instead of an HTML report.
disable-model-invocation: true
---

# Improve codebase architecture → issue

Wraps `improve-codebase-architecture`, swapping the report's form: one audit run produces **one** `architecture-review`-labeled issue holding all candidates, the same way the base skill produces one HTML report. The issue is then consumed by the **Ship Arch** workflow, which triages, implements, and closes it.

The base skill is user-invoked, so it cannot be reached through the Skill tool. Read `~/.claude/skills/improve-codebase-architecture/SKILL.md` directly and follow it, with these overrides:

- Run its **step 1 (Explore)** in full, exactly as written — after the ledger check below.
- Replace its **step 2 (HTML report)** with the issue filing below. Skip `HTML-REPORT.md` entirely.
- Skip its **step 3 (grilling loop)**: the issue is the deliverable; design decisions happen when the workflow addresses it.

## Check the ledger

Before exploring, detect the host from `git remote get-url origin` (github.com → `gh`, gitlab domain → `glab`), then list open audit issues:

- GitHub: `gh issue list --label architecture-review --state open --json number,title,body`
- GitLab: `glab issue list --label architecture-review`

Open issues fence off territory: any module, feature, or code area their candidates cover is already spoken for — steer the Explore step away from those areas entirely rather than re-deriving or duplicating their candidates. Tell the user which areas were fenced off and by which issue.

If the CLI is missing or unauthenticated, tell the user and stop — without a tracker this workflow has no output; point them at the base skill for the report-only run.

## File the audit issue

One issue for the whole run. Keep each candidate's content and vocabulary intact — files, problem, solution, benefits in terms of locality and leverage, recommendation strength, and any ADR-conflict callout.

1. Ensure the label exists (ignore "already exists"):
   - GitHub: `gh label create architecture-review --description "Deepening candidates from an architecture review, shallow modules worth refactoring into deep ones" --color 1D76DB`
   - GitLab: `glab label create --name architecture-review --description "Deepening candidates from an architecture review, shallow modules worth refactoring into deep ones" --color "#1D76DB"`
2. File it — title `Architecture review: <scope> — <YYYY-MM-DD>` (scope = the module/area explored, or the repo name for a full sweep). Body, in order:
   - **Checklist** at the very top, one task-list item per candidate, all pending, each linking to its section: `- [ ] [C1: <name>](#c1-name) — pending`. The filing skill writes it; the workflow owns it afterwards (ticking landed, striking rejected, marking blocked).
   - **Top recommendation** callout: which candidate to tackle first and why.
   - One `## C<n>: <name>` section per candidate: files, problem, solution, benefits, recommendation strength badge (`Strong` / `Worth exploring` / `Speculative`), and the before/after diagrams as ```mermaid fenced blocks (GitHub and GitLab render them natively — use mermaid or plain text in place of the report's CSS/SVG visuals).
   - GitHub: `gh issue create --label architecture-review --title "..." --body "..."`
   - GitLab: `glab issue create --label architecture-review --title "..." --description "..."`
3. Report the issue URL back to the user, and suggest the next step: run the **Ship Arch** workflow on it.

Done when the audit issue exists with checklist, top recommendation, and every candidate section — or the user was told why filing was skipped.

## When this skill is the wrong fit

- Interactive session ending in a visual report and a grilling loop → `improve-codebase-architecture`
