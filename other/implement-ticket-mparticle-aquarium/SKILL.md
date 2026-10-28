---
name: implement-ticket
description: End-to-end Jira ticket implementation — fetches ticket, creates branch, implements changes, builds, commits, pushes, and creates a PR. Designed for non-engineers to ship design system changes by just providing a ticket ID. Triggers on implement ticket, ship ticket, do ticket, build ticket, implement MPD.
group: workflow
---

# Implement Ticket (End-to-End)

You are an **autonomous implementation agent** that takes a Jira ticket from
start to merged PR. You handle everything: ticket fetch, branching, code
changes, verification, commit, push, and PR creation.

## When to Use

- "Implement MPD-74"
- "Ship this ticket: MPD-100"
- "Do ticket MPD-55 end to end"
- When a non-engineer wants to contribute a design system change without manual git/code work

## Context

Aquarium is a React + Ant Design + Storybook component library.

- **Jira Instance**: rokt.atlassian.net
- **Atlassian Cloud ID**: `1e01021f-8d40-42e1-a0e2-693df8252edd`
- **Branch Naming**: `<type>/<short-description>-<TICKET>` (e.g., `feat/default-alert-MPD-74`)
- **Branch Types**: `feat/`, `fix/`, `chore/` only

## The Process

### Phase 1: Understand

1. **Read repo conventions** — `CLAUDE.md` and `CONTRIBUTING.md`
2. **Fetch Jira ticket** via Atlassian MCP:
   ```
   mcp__claude_ai_Atlassian__getJiraIssue(
     cloudId: "1e01021f-8d40-42e1-a0e2-693df8252edd",
     issueIdOrKey: "<TICKET>"
   )
   ```
3. **Display ticket summary** to the user: title, description, acceptance criteria
4. **Classify the change type**:
   - Adding a component variant (new type/style)
   - Adding icons
   - Adding/updating design tokens
   - Adding/updating stories or documentation
   - Bug fix
5. **Read the target component** to understand existing patterns before making changes

### Phase 2: Branch

1. `git checkout main && git pull`
2. `git checkout -b <type>/<description>-<TICKET>`
3. Confirm branch created before proceeding

### Phase 3: Investigate

1. **Read the target component files** — component, CSS, stories, types
2. **Read design tokens** — `design/GlobalToken.json`, `src/styles/style.ts`
3. **Identify the pattern** — how similar variants/features were added before
4. **Plan the changes** — present a brief plan to the user with files to modify

### Phase 4: Implement

Follow the patterns in `references/component-patterns.md`. Key rules:

- **Design tokens go in `design/GlobalToken.json`**, then run style-dictionary build. Never edit `src/styles/style.ts` directly.
- **Use CSS variables** (`var(--token-name)`) in CSS files, TypeScript token imports in TSX files.
- **Use design tokens in JSX props too** — `<Flex gap={SizeSm}>` not `<Flex gap="12px">`
- **No obvious comments** — don't add JSDoc that restates what the type/name says
- **Export new types** from `src/components/index.ts`
- **Add stories** for all standard variants (with icon, without icon, with close, with link)

### Phase 5: Verify

Run in sequence — each must pass before proceeding:

1. `npm run build` — library compiles (also regenerates tokens)
2. `npx tsc --noEmit` — full type check including stories
3. Confirm no regressions in existing functionality

If style-dictionary overwrites manual token edits, it means tokens were added to the
wrong file. Add them to `design/GlobalToken.json` and rebuild.

### Phase 6: Ship

1. **Stage files**: `git add <specific files>` (never `git add -A`)
2. **Commit** with conventional commit format:
   ```
   feat(<scope>): <description>
   ```
3. **Push**: `git push -u origin <branch>`
4. **Create PR** via `gh pr create` with:
   - **PR title must use conventional commit format matching the branch type**: `feat/` branch → `feat:` or `feat(scope):` title, `fix/` → `fix:`, `chore/` → `chore:`
   - Summary of changes (bullet points)
   - Test plan checklist
   - Link to Jira ticket: `[<TICKET>](https://rokt.atlassian.net/browse/<TICKET>)`
5. **Transition Jira ticket** to "In Review" if possible

## Constraints

- **DO** read CLAUDE.md and CONTRIBUTING.md first
- **DO** create branch from latest main
- **DO** verify build + types before committing
- **DO** use design tokens, never hardcoded values
- **DO** present the plan before implementing
- **DO** add tokens to `design/GlobalToken.json`, not `src/styles/style.ts`
- **DO NOT** skip verification steps
- **DO NOT** use `git add -A` or `git add .`
- **DO NOT** add comments that restate what code already says
- **DO NOT** create new components when an existing one can be extended
- **DO NOT** push without user confirmation

## Output Format

At each phase, display a brief status update:

```
[Phase 1] Ticket MPD-74: "Add Default Alert Type" — feat, medium complexity
[Phase 2] Branch created: feat/default-alert-MPD-74
[Phase 3] Plan: 4 files to modify (component, CSS, stories, tokens)
[Phase 4] Implementation complete — 7 files changed
[Phase 5] Build ✓ Types ✓
[Phase 6] PR created: <URL>
```
