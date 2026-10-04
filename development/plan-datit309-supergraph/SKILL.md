---
name: plan
description: Create graph-informed implementation plans before writing code. Use before any non-trivial task. Skip for small changes (≤2 files, <20 lines, no hub/bridge).
mcp: codebase-memory-mcp
---

# /supergraph:plan

Scan codebase, map blast radius, create machine-readable plan.

Announce: "📐 /supergraph:plan — scanning codebase, creating plan..."

## Quick Gate
< 20 lines, ≤2 files, no hub/bridge, complexity <10 → skip to `/supergraph:tdd`.

## Steps

**0. Read CONTEXT.md (if exists):**
```bash
cat CONTEXT.md 2>/dev/null | head -60
```
Use domain vocabulary from CONTEXT.md in all plan task descriptions — never use raw file/class names where a domain term exists.

**1. Read the codebase (MANDATORY before planning):**
- Read config file → language, framework, versions
- Read 2-3 source files near target area → naming, imports, error handling
- Read 1-2 test files → test structure, assertion style

**2. Ensure graph:** Reuse `/supergraph:scan` context. If not done → run scan first. Requires `CBM_PROJECT` + healthy `index_status`; if stale/degraded → `index_repository` (absolute path).

**3. Graph analysis (parallel where independent):** See `references/codebase-memory-contract.md#Lifecycle`. Run `detect_changes`, `search_graph`, `trace_path` (inbound/outbound/data-flow), and `get_architecture` (overview/clusters/boundaries/hotspots) **in parallel** (no dependencies). After `get_graph_schema`, run recipes `hubs`, `bridges`, `test-gaps`, `cross-boundary` (requires schema). Derive risk from evidence; preserve escalation: >20 files STOP, hub/bridge needs approval. Respect `scan: TTL` — skip `index_repository` if fresh per scan logic.

**3b. Serena (optional):** See `serena/SKILL.md:Setup`. If scan not run, call `initial_instructions` first, then `find_referencing_symbols`/`find_implementations` for key symbols. Cross-check with graph blast radius; persist callers via `write_memory` only if >10 files or hub/bridge. Skip if Serena unavailable.

**4. Discuss approach (MANDATORY, user's language):** Present findings 1-3 (naming/patterns, graph risk, task summaries). Get approval before step 5; revise if needed.

**5. Create plan tasks** — each task 2-5 min. Use exact machine-readable format:

```markdown
## Task N: [Short description]
Wave: 1
Status: pending
Risk: low|medium|high
Dependencies: none | Task 1, Task 2
Model: flash|inherit|pro

Files:
- Create: path/to/new-file.ext
- Modify: path/to/existing-file.ext
- Test: path/to/test-file.ext

Blast radius:
- path/to/affected-file.ext

Acceptance:
- [observable behavior/result]
- [test/assertion that proves completion]

TDD:
- Behavior: single externally visible behavior
- Test file: exact test path
- Test name: behavior-focused test name
- 🔴 RED command: $FOCUSED_TEST_CMD
- Expected 🔴 RED failure: missing behavior, not setup/import/syntax error
- Minimal 🟢 GREEN change: smallest implementation idea
- Refactor candidates: optional, only after 🟢 GREEN
- Mocking: none | why unavoidable

Steps:
1. 🔴 RED: write exact failing test
   Command: $TEST_CMD
   Expected: FAIL
2. 🟢 GREEN: write minimal implementation
   Command: $TEST_CMD
   Expected: PASS
3. REFACTOR: safe cleanup or none
4. VERIFY:
   - $TEST_CMD
   - $LINT_CMD (skip if none)

Checkpoint:
- Files: path/to/test-file.ext path/to/source-file.ext
- Commit: type: short description
```

Task status values: `pending`, `in_progress`, `completed`, `stuck` (managed by executor)

### Architecture & Spec Contracts (Embedded or Referenced)

For complex multi-module or schema changes, embed key contracts, schemas, and design constraints directly in the `## Architecture & Contracts` section of this plan (or reference an approved SDD via `Spec: path/to/sdd.md` if one was explicitly created). Avoid creating separate SDD files unless specifically requested by the user.

### Wave Assignment Rules (DAG Parallelism):
- **Wave 1:** Foundational setup, data schemas, interface contracts, base types (`Dependencies: none`).
- **Wave 2:** Independent business features, service implementations, API endpoints (depend only on Wave 1). Executed **in parallel** by concurrent subagents.
- **Wave 3:** UI components, glue code, feature integration (depend on Wave 2).
- **Wave 4:** E2E / integration tests, migration scripts, documentation, cleanup.
- **Model Tiering Hint:**
  - `Model: flash` for low-risk boilerplate, test fixtures, types, docs (3x faster, 5x cheaper).
  - `Model: inherit` for standard feature logic and tests.
  - `Model: pro` for high-risk core algorithms, architecture refactoring, complex multi-file coupling.

**6. Validate:** All tasks have `## Task N:` + fields (Wave,Status,Risk,Dependencies,Files,Acceptance,TDD,Steps,Checkpoint), no TBD/TODO, real commands from .supergraph-env, no indentation under fields, no extra blank lines.

**7. Save plan:** `docs/supergraph/plans/YYYY-MM-DD-<slug>.md`

**8. Analysis Gate (if analyze used):** Verify plan aligns with `## Analysis Decisions`; if skipped → WARN "No analyze step".

**9. Environment Context (MANDATORY):** Include Language, TEST/LINT/FORMAT/BUILD cmds from .supergraph-env, Branch, commit style, codebase conventions, Graph Context (blast radius/hubs/bridges/communities).

**10. Auto-review:** Dispatch `plan-reviewer`; fix issues; require `Approved` before execute.
**11. User Gate (MANDATORY):** Present summary (plan path, Tasks N, blast radius, hubs, Review Approved); ask `[yes/modify/reject]` in user's language.
**12. Report:** `✅ /supergraph:plan complete — Plan: ... Tasks: N | Blast: M | Review: Approved | User: yes/modify/rejected | Next: execute/tdd`

## Rules
- Codebase first, plan second — never plan blindly
- Environment Context mandatory — executor depends on it
- Exact file paths, commands, code — no vagueness
- Task headings stay `## Task N:` for executor parsing
- No placeholders, no "TBD", no "similar to Task X"
- Never execute code — only create plans
