---
name: gk-personal
description: Manage the user's GitKraken CLI workspaces across personal GitHub, Priceless, and Brown and Brown Azure DevOps, including bb-mac. Use for gk inventory, repo grouping, workspace renames, cloud synchronization, team sharing, and local clone mapping. Discover native gk state instead of maintaining a duplicate manifest.
---

# Personal GitKraken operations

Read [context.md](references/context.md) when choosing a business context. Read
[native-inventory.md](references/native-inventory.md) when discovering, syncing, or changing inventory.
These references describe policy and discovery, not a second repository database.

## Procedure

1. Identify the requested host and business context. Inspect `gk version` and relevant command `--help` on that host. Use `gk version`, not `gk --version`, which can invoke Git passthrough.
2. Discover existing workspaces with `gk workspace list --output json`. For current cloud membership use `--sync`. Load only the selected workspace with `gk workspace info "<name>" --output json`.
3. Preserve existing workspace IDs. Treat names as changeable labels. Do not create duplicates because another machine cannot see a cloud workspace. Check authentication and organization access first, using supported read-only commands. Never copy credential stores between machines.
4. Resolve repo identity by provider, owner/org, project, and repo ID or sanitized remote. Names alone are not unique. Empty local paths mean unmapped, not deleted. Local worktrees are not separate hosted repos.
5. State the intended membership delta before making changes. Execute changes the user authorized, but do not infer permission to invite people, buy licenses, change Git remotes, delete clones, push code, or enable AI services. Team sharing and repository grouping are separate decisions.
6. Update inventory through native `workspace update` commands. Prefer existing cloud workspaces. Convert a local workspace with `--cloud` only after verifying there is no existing cloud equivalent, the provider constraints, and the intended organization. Never edit internal gk JSON stores to simulate a successful cloud change.
7. Synchronize the listing again, inspect affected memberships, and compare workspace IDs, repo membership, and sharing. Verify both sides when moving membership. Report exact changes and blockers. Do not claim an authentication error proves a workspace is absent.

## Boundaries

- Cloud workspace definitions are shared metadata, not backups of code or working files.
- A session isolates gk auth/cache, not Git identity, SSH keys, or credential-manager accounts. Discover sessions rather than assuming they exist.
- Use explicit repo paths for mixed directory trees. Do not import every checkout under a home directory or a coordination hub.
- `workspace refresh` can clone/pull. It is not a metadata refresh. Do not run it for inventory discovery.
- Avoid logging tokens, raw credential stores, or credential-bearing remote URLs. Never place live employer inventory in this skill repo.
- Keep human grouping decisions separate from observations. Unknown teams, inaccessible providers, and unverified mappings stay unknown.

## Response

Report host/context, observed workspaces, proposed or applied delta, verification, and any remaining blockers. Use a compact table when comparing collections. Do not create a proprietary manifest or hardcode all current repositories into this skill.
