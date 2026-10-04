---
name: ticket-ownership
description: Establish and verify exclusive ownership of a GitHub issue before refine or implementation work begins. Use from ticket-mode workflows that must claim an unassigned issue for the active GitHub CLI user without replacing existing assignees.
user-invocable: false
---

# Ticket Ownership

Apply this contract only in ticket mode, after `gh` authentication and repository
identity have been verified.

**Caller responsibility**: `## Inspect ownership (read-only)` below performs zero
GitHub writes and may run at any point before substantive work. `## Claim ownership
(mutating)` performs a real GitHub mutation (`gh issue edit --add-assignee`) — it
must **not** run before the calling workflow's own authorization gate (e.g. a
Confirm/Decline confirmation). Adding `Working` or doing substantive work must never
precede the claim.

## Inspect ownership (read-only)

### Resolve the current user

Run:

```bash
gh api user --jq .login
```

Trim the result and validate it against `^[A-Za-z0-9-]+$`. Stop if the command
fails or the login is empty or invalid. Never infer a GitHub login from Git
`user.name` or `user.email`.

### Check for a conflict

Use assignees from the caller's fresh ticket fetch when available; otherwise fetch:

```bash
gh issue view <number> --repo <owner>/<repo> --json assignees
```

Compare logins case-insensitively:

- Exactly one assignee matching the current login: continue — already owned by the
  caller, no claim needed.
- Exactly one different assignee: stop and report that ticket `#<number>` is owned
  by `@<login>` and cenci will not replace the existing assignee.
- Multiple assignees: stop, list them, and report that cenci requires one exclusive
  owner. Do not add or remove anyone.
- No assignees: no conflict — the caller's write phase may proceed to
  `## Claim ownership (mutating)` below, at the appropriate point in its own
  authorization boundary.

## Claim ownership (mutating)

Reached only once the calling workflow's own authorization gate has been passed.
Re-verify first — the assignees may have changed since the inspection above ran, so
re-fetch rather than trusting the earlier read:

```bash
gh issue view <number> --repo <owner>/<repo> --json assignees
```

Re-apply the same conflict comparison as above. If it is still unassigned, claim it:

```bash
gh issue edit <number> --repo <owner>/<repo> --add-assignee <current-login>
```

Then re-fetch `assignees`. Continue only when the current login is the sole
assignee. If the edit or fetch fails, or another assignee appeared concurrently,
stop and report the observed state. Do not remove or replace assignees to repair
a conflict automatically.

Ticket creation is not a claim. Split children remain
unassigned until a primary workflow is invoked for each one.
