---
name: reedom-gh:create-draft-pr
description: Prepare complete PR content ready for creation via reedom-gh:pr-maker agent.
allowed-tools: Read
---

Collect data, draft complete PR content, cleanup, return ready-to-use JSON.

## Arguments

| Arg | Default | Description |
|-----|---------|-------------|
| `--against` | origin/main | Target branch |
| `--lang` | system | PR content language |
| `--prefix` | "" | Prefix to prepend to title |

## Workflow

1. Run `${CLAUDE_PLUGIN_ROOT}/skills/create-draft-pr/scripts/collect-info.sh -a <target> --lang <lang>`
2. Check for errors
3. Read temp files (commits, diffs)
4. Draft PR title and body
5. Prepare preceding PR update (if exists)
6. Run `${CLAUDE_PLUGIN_ROOT}/skills/create-draft-pr/scripts/cleanup.sh <temp_dir>`
7. Return complete PR data

## Output JSON

```json
{
  "current_branch": "feature/x",
  "target_branch": "origin/main",
  "push_needed": true,
  "matched_spec": "auth",
  "pr": {
    "title": "feat(auth): add login module",
    "body": "## Summary\n..."
  },
  "existing_pr": {
    "exists": false,
    "number": null
  },
  "preceding_pr": {
    "exists": true,
    "number": 122,
    "updated_body": "## PR Order\n- this PR\n- #NEW\n\n<original body>"
  }
}
```

Agent replaces `#NEW` with actual PR number after creation.

---

## Title Format

`<prefix> type(scope): description`

- Prepend `--prefix` value if provided
- Type: feat/fix/refactor/chore/docs/test (from commits)
- Scope: matched_spec if single, omit if multiple/none
- Max 50 chars (excluding prefix), lowercase, imperative

---

## Body Format

Language: `lang.effective`

```markdown
## Summary
What and why (2-3 sentences)

## Changes
- Key changes

## Testing
How to verify

## Related Issues
closes #N
```

---

## Preceding PR Update

If preceding PR exists, prepare `updated_body`:

```markdown
## PR Order
- this PR
- #NEW

<original body>
```

Use `## PR順序` for Japanese.

---

## Large Diff Strategy

When split: read manifest.json, prioritize source files, skip generated.

## Error Handling

```json
{"error": "message", "error_code": "NOT_GIT_REPO"}
```
