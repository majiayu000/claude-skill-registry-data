---
name: ticket
description: Assemble a Jira/Linear/GitHub-Issue body from recent commits, diff, and branch context
triggers:
  - ticket
  - issue body
  - changelog
  - what did we ship
  - ticket summary
---

# Ticket

Generate an audit-friendly issue description from branch context, recent commits, and staged changes.

## Usage

```bash
ticket
```

Outputs markdown suitable for pasting into Jira, Linear, or GitHub Issues. Useful for "what did this engineer ship" reporting.

## Sections Generated

- **Summary**: Branch name, author, current directory
- **Changes**: File diff summary (counts per type: added, modified, deleted)
- **Commits**: Last 5 commit messages with timestamps
- **Testing**: Checklist template for test coverage
- **Risk**: Brief assessment of scope and breaking changes

## Safety

- Redacts secrets: `sk-*`, `ghp_*`, `AKIA*` patterns stripped from diff and messages
- No credential leakage into output
- Safe for shared channels, documentation, compliance reviews

## Exit Conditions

- **Success**: Markdown printed to stdout, ready to copy
- **No git repo**: Warns "not a git repo", exits gracefully
- **Merge commit**: Detects merge commits and flags in Risk section
- **Empty diff**: Builds ticket from commits and branch only
- **User abort**: Ctrl+C exits without output

## Examples

<!-- Replace with your actual author email. -->
```
## Summary
Branch: feat/auth-provider-refresh
Author: your.email@example.com
CWD: ai-dev-toolkit/packages/core/

## Changes
- Modified: 3 files (lib/auth/*.ts, tests/auth/*.test.ts)
- Added: 1 file (docs/oauth-flow.md)
- Lines: +287, -142

## Recent Commits
- c8a9d1f: Add token refresh retry logic with exponential backoff
- a3b7f2e: Refactor OAuth provider factory
- ...

## Testing
- [ ] Unit: auth middleware
- [ ] E2E: OAuth callback flow
- [ ] Secrets: env redaction test

## Risk
- **Scope**: Medium (auth layer only, no DB changes)
- **Breaking**: No breaking changes
- **Dependencies**: Adds `jose@^9.0.0` (peer-optional)
```
