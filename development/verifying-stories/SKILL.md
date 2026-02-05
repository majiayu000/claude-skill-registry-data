---
name: verifying-stories
description: Guides developer verification before handoff. Use when completing implementation, preparing for acceptance testing, or self-reviewing work before commit or PR.
---

# Verifying Implementation

Execute the verification approach defined in the story log.

## Checklist

```
Developer Verification:
- [ ] Acceptance criteria verified (per defined approach)
- [ ] Error cases verified
- [ ] Existing functionality not broken
- [ ] All automated tests pass
- [ ] Linting passes
- [ ] No debug prints left behind
- [ ] No TODO without context
- [ ] Story log updated
```

## Run Tests

```bash
npm test        # or
deno task test  # or
pytest
```

## Code Quality

Check for:
- No `console.log`, `print()`, or debug statements
- No uncontextualized `TODO` comments

## Update Story Log

```markdown
### Acceptance Checks

**Status: Pending Product Owner Review**

Developer verification completed:
- [How each criterion was verified]
- [Observations or limitations]
```

## Important

- **Do NOT check acceptance criteria checkboxes** — PO responsibility
- If verification approach wasn't defined or situation has changed, ask PO
- Use available MCP tools or skills for testing if present
- If verification is limited, explain what wasn't verifiable
