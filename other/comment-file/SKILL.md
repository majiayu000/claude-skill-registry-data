---
name: comment-file
description: Add TSDoc/JSDoc comment blocks to every exported function, route, hook, and component in a single file, following the project's Source/Consumer convention. Use when the user asks to "comment this file", "document file X", or as a sub-step of /comment-batch.
---

# comment-file

Add high-quality TSDoc to one file. The convention is at `Aqarkom_Knowledge/Engineering/Comment Style.md` — **read it first** if you haven't this session.

## Inputs

- **File path** (required) — absolute path or repo-relative
- **Mode** (optional) — `update` (default, only adds blocks for missing exports) or `rewrite` (replaces existing blocks; use with care)

## Steps

1. **Read** `Aqarkom_Knowledge/Engineering/Comment Style.md` if you haven't already this session — the convention is non-trivial.
2. **Read the target file** end-to-end. Don't skim. You can't write good `Source:` / `Consumer:` lines without understanding the full call flow.
3. **For each exported symbol** (functions, classes, components, hooks, route handlers, zod schemas, types):
   - Check if it already has a TSDoc block
   - In `update` mode, skip if a block exists; in `rewrite` mode, replace it
4. **For each new block, fill in**:
   - **Purpose** — one imperative line
   - **`@param`** for every input. **Source:** must point to a real call site you can name.
     - For Express handlers, parameters are usually `req.body.X`, `req.params.X`, `req.query.X`, or `req.user.X` (from JWT).
     - For React components, parameters are props from a parent.
     - For hooks, parameters are arguments from a calling component.
   - **`@returns`** with **Consumer:** pointing to a real downstream usage.
     - For API routes: name the React Query hook(s) that consume the response.
     - For React state setters: name the components that subscribe.
     - For lib functions: name the routes/components that import them.
   - **`@throws`** for any explicit error path
   - **`@sideEffect`** for DB writes, external API calls, file I/O, shared-state mutation
   - **`@route` + `@auth`** for Express handlers
5. **Use `/find-callers`** when you need to discover real callers — don't guess.
6. **Verify**:
   - Run `/typecheck` (comments shouldn't break anything)
   - Read 2-3 of the blocks you wrote and ask: "could a stranger understand the data flow from this alone?"
7. **Don't commit** — leave that to the caller (usually `/comment-batch`).

## Quality bar

A good block:
- Names specific files (`leads/index.tsx`, not "the frontend")
- Cites the exact React Query key (`['/api/leads']`)
- Mentions side effects you'd want to know about before refactoring
- Stays under 30 lines

A bad block:
- Restates the function signature in prose
- Says "Used by other parts of the application"
- Documents trivial getters
- Includes types (TypeScript already has them)

## Anti-patterns

- ❌ Don't invent call sites — if you can't find a real one, write `Source: not yet wired` and flag it
- ❌ Don't add line-level comments unless the code is genuinely non-obvious
- ❌ Don't change code while commenting — split into separate edits
- ❌ Don't comment generated files (Prisma client, GraphQL codegen)
- ❌ Don't blindly run on shadcn primitive re-exports

## Verification

- [ ] Convention guide read this session
- [ ] File read fully before commenting
- [ ] Every exported symbol has a block (or is intentionally skipped — explain why)
- [ ] At least one Source: traced via `/find-callers`
- [ ] `/typecheck` clean
- [ ] No invented call sites
