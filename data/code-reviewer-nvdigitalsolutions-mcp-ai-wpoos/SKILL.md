---
type: Skill
name: code-reviewer
description: Review code for quality, simplicity, and maintainability. Identifies unnecessary abstractions, duplicated logic, oversized functions, missing error handling, and naming issues — then fixes them automatically before presenting the result.
license: MIT
compatibility: Claude Code, Cursor, Gemini CLI, Codex CLI
---

# Code Reviewer

Run a structured quality review pass over any code you write or modify. Use this skill to ensure code is production-ready before presenting it.

## What This Skill Checks

- **Single responsibility**: functions doing too much (> ~30 lines is a signal)
- **Duplication**: logic repeated more than twice that should be extracted
- **Abstraction level**: unnecessary indirection or over-engineering
- **Error handling**: missing try/catch, unhandled promise rejections, no null checks
- **Performance**: N+1 queries, unnecessary re-renders, blocking operations
- **Dead code**: unused imports, unreachable branches, commented-out code
- **Naming**: identifiers that don't communicate intent
- **TypeScript/typing**: `any` usage, missing return types
- **Security**: unvalidated inputs, hardcoded secrets, SQL concatenation

## Review Workflow

After completing any implementation:

1. Review the changed files for the issues listed above
2. Fix what you find — don't just flag it
3. Present the improved code, not the first draft
4. Briefly note what was changed and why (one line per fix)

## Example: Before and After

**Before review:**

```typescript
const getUser = async (id: string) => {
  const res = await fetch(`/api/users/${id}`);
  const data = await res.json();
  return data;
};

const getPost = async (id: string) => {
  const res = await fetch(`/api/posts/${id}`);
  const data = await res.json();
  return data;
};
```

**After review (pattern extracted, error handling added):**

```typescript
const fetchResource = async <T>(path: string): Promise<T> => {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json() as Promise<T>;
};

const getUser = (id: string) => fetchResource<User>(`/api/users/${id}`);
const getPost = (id: string) => fetchResource<Post>(`/api/posts/${id}`);
```

## Project-Level Standards (configure in CLAUDE.md)

Add a section like this to `CLAUDE.md` to set project-specific thresholds:

```markdown
## Code Review Standards
After completing any implementation, review for:
- Functions longer than 30 lines (likely doing too much)
- Logic duplicated more than twice (extract to utility)
- `any` type usage in TypeScript (replace with real types)
- Components with more than 3 props that could be grouped
- Missing error handling on async operations
- Unvalidated user input before database/API use
```

## PHP-Specific Review Points

For WordPress / PHP code, additionally check:

- Missing `sanitize_*()` on input, missing `esc_*()` on output
- Nonces absent on state-changing requests
- Direct `$_POST`/`$_GET` access without sanitization
- `wpdb->prepare()` used for all dynamic queries
- `current_user_can()` checked before privileged operations
- `wp_safe_remote_*()` instead of raw `curl`

## Thresholds

| Signal | Action |
|--------|--------|
| Function > 30 lines | Consider splitting |
| File > 300 lines | Consider modularizing |
| Duplication × 3 | Extract to shared utility |
| > 5 function parameters | Group into object/array |
| Nested callbacks > 3 deep | Refactor to async/await |

## Tips

- Run this review automatically — treat it as a mandatory pre-flight before presenting code
- The goal is the **second draft**: clean, correct, and maintainable
- Don't over-engineer: only extract when duplication is actual, not theoretical
- When in doubt, favour **readability** over cleverness
