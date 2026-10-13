---
name: new-project
description: Turn a fresh copy of this template into the user's own product - rename the owner, repository, product, bundle id and every boilerplate identifier, then walk docs/new-project.md's checklist. Use when the user has just created a repository from this template and wants to make it theirs.
argument-hint: <name> --owner <github owner> [--product "<Product>"] [--bundle-id <id>]
disable-model-invocation: true
---

# Make a new project from the template

`docs/new-project.md` is the checklist; this is the order to work through it in.

1. **Ask for the identity** if the arguments don't give it: the project name (lowercase,
   dashes allowed: it names Kubernetes resources and the compose project), the GitHub
   owner, the product name people see, and the mobile bundle id. The bundle id is fixed
   once the app is in a store, so confirm it.
2. **Rename, on a clean tree:** `bun run rename <name> --owner <owner> --product
   "<Product>" --bundle-id <id>`. It rewrites every tracked text file and fails if any
   old identifier is left, naming each line: change those by hand, then run it again
   until it passes. Then `bun install` (the lockfile's root name changed),
   `bun run gen`, `bun run lint`, `bun run check-types` and `bun run test`.
3. **Show the user the diff** before committing, and commit only with their approval.
4. **The domains** (`deploy/environments/*/`, `EMAIL_FROM`): the rename can't know them.
   Ask, or leave the `example.com` placeholders and say so.
5. **Features they don't need:** point at the remove-feature skill; don't remove any
   unasked.
6. **The rest of `docs/new-project.md`** (GitHub settings, secrets, infrastructure, the
   first deploy) needs the user's accounts: list the remaining steps with their
   commands, and run none that reach GitHub, a cloud or a cluster without approval.

The default branch stays `master`. Renaming it touches GitHub's settings, the ruleset and
every workflow's branch filters, so it's a separate change the user asks for.
