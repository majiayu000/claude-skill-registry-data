---
name: update-docs
description: Repo-wide documentation sweep for updating project docs, context, ADRs, diagrams, README files, agent instructions, and documentation sites after feature work, decisions, or direction changes. Use this skill whenever the user asks to update docs, refresh documentation, prepare for PR, finish a branch, merge, ship, close out work, record what changed, or align docs with code. It first discovers the repo's key Markdown documentation and docs sites, ignores historical archives by default, presents the proposed docs plan for approval, then updates only the approved docs surgically.
---

# Update Docs

## Purpose

Run this when docs need to reflect current code, decisions, project context, or branch state. The goal is to leave future humans and agents with the current state, decisions, and next steps, without rewriting unrelated docs or repeating setup instructions that belong in README.

Use the `documentation-and-adrs` skill for deeper guidance when decisions, public APIs, architecture, or feature behavior changed. If that skill is available, read it before writing ADRs or decision-heavy docs.

## Documentation discovery

Start by discovering the repo's documentation shape. .md, .mdx, and .html are the default file types, but include docs-site content when the repo has one.

Check these locations first when they exist:

- Docs maps or indexes: `docs/docs-map.md`, `docs/index.md`, `docs/map.md`, `index.md`, `map.md`.
- Agent and assistant context: `AGENTS.md`, `CLAUDE.md`.
- Project overview and commands: `README.md`, package or app README files when relevant.
- Changelog: `CHANGELOG.md`, `Changelog.md`, `changelog.md`, or repo-specific changelog files when user-visible changes need release notes.
- Project context: `CONTEXT.md`, `docs/CONTEXT.md`.
- ADRs: `docs/adr/`.
- Diagrams: `docs/diagrams/`.
- Documentation sites: `apps/online-docs/`, Mintlify docs directories, or similar docs-app content.
- Specs, plans, roadmaps, and milestone docs under `docs/`.

Useful discovery commands:

```bash
find . -path '*/_archive/*' -prune -o -path '*/_done/*' -prune -o -type f \( -name '*.md' -o -name '*.mdx' \) -print
find . -maxdepth 4 -type f \( -name 'docs-map.md' -o -name 'index.md' -o -name 'map.md' -o -name 'AGENTS.md' -o -name 'CLAUDE.md' -o -name 'README.md' -o -name 'CHANGELOG.md' -o -name 'Changelog.md' -o -name 'changelog.md' -o -name 'CONTEXT.md' \) -print
find apps/online-docs -type f \( -name '*.md' -o -name '*.mdx' \) -print 2>/dev/null
```

Ignore historical artifacts by default unless the user explicitly asks to update them:

- `_archive/*` and nested `*/_archive/*`.
- `_done/*` and nested `*/_done/*`.
- Generated build output, vendored dependencies, and package-manager directories.

After discovery, present the docs plan and wait for user approval before editing. Include:

- Docs proposed for update, with the reason each may need an edit.
- Docs reviewed but likely left unchanged.
- Docs intentionally ignored, including archives and done folders.
- Any uncertainty about source-of-truth docs or conflicting docs.

## Workflow

1. Inspect the branch state.

```bash
git status --short --branch
git diff --stat main...HEAD 2>/dev/null || git diff --stat
git diff --name-status main...HEAD 2>/dev/null || git diff --name-status
```

2. Identify what changed.

Look for:

- Product behavior changes.
- Architecture or dependency decisions.
- Public API, IPC, preload, transport, storage, or data-shape changes.
- Milestone, spike, or plan status changes.
- New gotchas future agents should know.
- Commands or setup changes that belong in README.
- Diagrams that no longer match the code or decision.
- Prototype code or dependencies that should not survive a no-go spike.

3. Decide which docs need edits.

Use this routing:

- `README.md`: setup, run, test, release, troubleshooting commands.
- `CHANGELOG.md`, `Changelog.md`, `changelog.md`, or equivalent: user-visible changes, release notes, migration notes, breaking changes when the repo maintains a changelog.
- `AGENTS.md` and `CLAUDE.md`: durable project context, current direction, repo map, agent-relevant rules.
- `CONTEXT.md`: domain language, product context, current architecture, project constraints.
- Docs maps and indexes: navigation, source-of-truth pointers, status summaries.
- `docs/adr/`: accepted or rejected architectural decisions, dependency decisions, expensive-to-reverse choices.
- `docs/diagrams/`: system flows, architecture diagrams, state/session diagrams.
- `apps/online-docs/` and similar docs sites: public or internal user-facing documentation, Mintlify pages, navigation metadata.
- Specs, plans, roadmaps, and milestone docs under `docs/`: specs, spike outcomes, roadmap status, milestone scope.

4. Present the docs plan for approval.

Do not edit documentation until the user approves the proposed list. Use this concise format:

```markdown
Proposed docs updates:
- `path`: why it should change

Likely unchanged:
- `path`: why no edit seems needed

Ignored by default:
- `path`: historical/generated/vendor reason

Questions:
- [Only include blockers or source-of-truth uncertainty]
```

5. Update approved docs surgically.

- Record why a decision was made, not just what changed.
- Keep roadmap status aligned with ADRs and spike specs.
- Link related docs instead of duplicating long explanations.
- Keep README as the home for commands. Do not repeat command lists in AGENTS.md or specs.
- Remove stale open questions when the question has been answered.
- Preserve spike outcomes in specs or ADRs. Do not keep dead prototype code or dependencies unless explicitly adopted.
- Do not rewrite unrelated prose or reformat whole files.

6. ADR guidance.

Write or update an ADR when the branch includes:

- A selected or rejected library/framework.
- A session, storage, IPC, transport, auth, or data-model decision.
- A durable workflow or milestone direction change.
- A no-go spike result that affects future implementation.

Use this concise ADR shape:

```markdown
# ADR 000N: [Decision title]

## Status

Accepted

## Context

[Why this decision came up, constraints, and relevant alternatives.]

## Decision

[The choice in direct language.]

## Consequences

- [Impact on implementation.]
- [Future revisit trigger, if any.]
```

7. Verify docs.

For docs-only changes, run targeted checks:

```bash
git diff --check
rg -n "TBD|TODO|broken-link-placeholder" AGENTS.md CLAUDE.md README.md CHANGELOG.md Changelog.md changelog.md CONTEXT.md docs apps/online-docs 2>/dev/null || true
```

Also verify referenced files exist:

```bash
for f in <paths-you-linked>; do test -e "$f" || echo "missing: $f"; done
```

For code plus docs changes, also run the smallest deterministic code checks that prove the changed behavior. Prefer the repo `check` command for final verification when practical.

8. Report the result.

Use this concise format:

```markdown
Docs updated:
- `path`: what changed

Decision records:
- `path`: decision captured, or "none needed"

Verification:
- `command`: result
```

## Stop and ask

Ask before proceeding when:

- The branch has competing possible decisions and the user has not chosen one.
- A stale doc conflicts with code and you cannot tell which is authoritative.
- The discovered docs plan has not been approved yet.
- Updating docs would require inventing roadmap scope or acceptance criteria.
- The only evidence for a claim is a prototype that the user wants discarded.

## Common misses

- Updating a spike spec but not the roadmap.
- Recording a decision in prose but not an ADR.
- Leaving an answered question in Open Questions.
- Keeping no-go prototype dependencies in `package.json`.
- Adding setup commands to AGENTS.md instead of README.
- Forgetting diagrams after changing architecture or data flow.
