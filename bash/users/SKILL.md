---
name: users
description: List the users in your Frontline account from the CLI. Use when you need to resolve a user's ID — for example to fill a user-relation field, assign a task or record, or look up who is on the account. Read this when you need a user ID and only have a name or email.
allowed-tools: Bash(frontline:*)
---

# Users

List the human users on your account. This is a read-only lookup, mainly used to resolve
**user IDs** that other commands need (user-relation fields, task assignees, record owners).

Requires a USER API key (the same key used for conversations and playbooks).

```bash
frontline users list --table
frontline users list            # JSON (default)
```

**Output:** `results[]` of users with `id`, `full_name`, `first_name`, `last_name`, `email`,
`avatar`, `role`, `status`. Deleted users are excluded.

## Typical use

You usually run this to turn a name/email into the numeric `id` other commands expect:

```bash
# Find a user, then use their id elsewhere (e.g. as a task assignee)
frontline users list --table
# → note the id, then pass it where a user id is required
```

## See also

- Authentication and profiles: the `auth-and-profiles` skill.
- Full reference: <https://docs.getfrontline.ai/cli>.
