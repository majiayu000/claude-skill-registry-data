---
name: construct-ai-workflow
description: Recurring workflow patterns from 904+ Construct-AI development sessions. Covers git operations, debugging, code review, UI component work, and documentation procedures.
---

# Construct-AI Workflow Skill

Derived from analysis of 904+ task sessions in the Construct-AI project history.

## When to Use

Apply this skill when working on the Construct-AI / paperclip-render project. It encodes the most common patterns and best practices discovered through extensive development history.

## Workflow Patterns (by frequency)

### 1. Git Operations (534 occurrences)

**Standard commit flow:**
1. `git status` — always check state first
2. `git add <specific files>` — scope changes carefully
3. `git commit -m "<scope>: <action-oriented message>"` — use conventional commits
4. `git push` — push when ready

**Branch management:**
- Always check `git branch -v` before switching
- Use `git pull --rebase origin main` before pushing to shared branches
- When merging: `git checkout main && git merge <branch> && git push`
- Never discard other agents' work during rebase

**Common pitfalls from history:**
- Port mismatches between client/server (3006 vs 3060) — always verify
- Duplicate files with same names in different directories
- Incomplete commits (missing related files) — check all touched files
- `gitHead` in package.json causing false version counters

### 2. Debugging & Fixing (1063 occurrences)

**Systematic debugging approach:**
1. **Reproduce** — understand the exact error message and context
2. **Locate** — find the source file and line number
3. **Analyze** — read surrounding code, check imports, verify types
4. **Fix** — make minimal targeted change
5. **Verify** — test the fix doesn't break related functionality

**Common error patterns from history:**
- "undefined function" errors → check import paths and function names
- CSS syntax errors → often from duplicated content blocks
- Scoping bugs → variables declared inside blocks but used outside
- Port configuration drift → check both client and server configs
- Modal show/hide state → ensure state synchronization between parent/child

### 3. Code Creation (1307 occurrences)

**Component creation pattern:**
1. Analyze existing similar components for patterns
2. Create file with proper imports and exports
3. Implement core functionality
4. Add error handling
5. Test integration with existing code

**Procedure/documentation creation:**
1. Review existing procedures for format and style
2. Identify all required sections
3. Write content matching existing conventions
4. Cross-reference related procedures
5. Verify numbering and naming conventions

### 4. Review & Analysis (1565 occurrences)

**Code review checklist:**
- [ ] Check git status and recent commits
- [ ] Verify all related files are consistent
- [ ] Look for duplicate code or files
- [ ] Check port/config consistency
- [ ] Verify imports and exports
- [ ] Test the change doesn't break existing functionality

**Architecture review:**
- Read existing accordion procedures and schemas
- Analyze current structure before proposing changes
- Design changes that fit existing patterns
- Verify integration points

## Project-Specific Knowledge

### Key Directories
- `server/` — Express API and orchestration
- `ui/` — React + Vite frontend
- `packages/db/` — Drizzle schema and migrations
- `packages/shared/` — Shared types and constants
- `docs-construct-ai/` — Extensive documentation and procedures
- `docs-paperclip/` — Paperclip framework docs

### Common Configuration
- Server ports: 3060 (client), verify server port in config
- Database: PostgreSQL with Drizzle ORM
- Frontend: React with Vite
- Docs: Mintlify

### Recurring Issues to Watch
1. **Port mismatches** — client and server must agree on ports
2. **Duplicate files** — same functionality in multiple locations
3. **State synchronization** — modals, tabs, and shared state
4. **CSS duplication** — check for doubled content blocks
5. **Import paths** — verify relative paths are correct
6. **Git counter** — `gitHead` in package.json can cause false version bumps

## Quick Reference Commands

```bash
# Git workflow
git status
git log --oneline -5
git add <files>
git commit -m "scope: action"
git push

# Debugging
grep -rn "function_name" --include="*.js" --include="*.jsx"
grep -rn "port" --include="*.js" --include="*.json" | grep -E "3006|3060"

# File discovery
find . -name "*.js" -path "*/agents/*" | head -20
find . -name "duplicate_name.*" 2>/dev/null