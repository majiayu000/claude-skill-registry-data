---
name: minecraft-permissions-admin
description: "Administer Minecraft server permissions for 1.21.x, centered on LuckPerms and common Vault-integrated stacks. Use for groups, tracks, inheritance, contexts, temporary grants, staff role design, user audits, permission exports, rollback-safe edits, and plugin permission triage across Java servers and crossplay environments."
---

# Minecraft Permissions Administration Skill

## Scope

Use this skill for permission policy and operational changes, especially on
LuckPerms-based Paper/Purpur/Velocity networks.

### Routing Boundaries
- `Use when`: the task involves groups, tracks, contexts, inheritance, temporary permissions, user access audits, Vault permission bridges, or staff permission safety.
- `Do not use when`: the task is EssentialsX command policy only (`minecraft-essentials-ops`), broad server hosting operations (`minecraft-server-admin`), plugin implementation (`minecraft-plugin-dev`), or Bedrock operator files without a Java permission manager (`minecraft-bedrock-server-admin`).

## Permission Change Workflow

1. Identify the exact plugin permission node and target scope.
2. Export or snapshot current permissions before editing.
3. Apply the smallest group or context change that satisfies the goal.
4. Test with a representative non-admin account.
5. Document the command and expected rollback.

Never grant wildcard permissions to normal players or temporary staff accounts.

## LuckPerms Command Patterns

Group assignment:

```mcfunction
/lp user Alex parent add member
/lp user Alex parent remove member
```

Temporary staff grant:

```mcfunction
/lp user Alex parent addtemp helper 7d
```

Permission node:

```mcfunction
/lp group helper permission set essentials.mute true
/lp group helper permission unset essentials.mute
```

Track promotion:

```mcfunction
/lp track staff append helper
/lp track staff append moderator
/lp user Alex promote staff
```

Contexted grant:

```mcfunction
/lp group builder permission set worldedit.region.set true server=creative
```

Use contexts to keep powerful permissions away from survival or production
servers.

## Role Design

Suggested split:

- `owner`: break-glass administrative access.
- `admin`: platform and player operations.
- `moderator`: chat, jail, mute, kick, tempban.
- `builder`: WorldEdit and creative build tools in build contexts only.
- `member`: normal gameplay features.
- `guest`: limited join and read-only access.

Prefer additive groups over per-user one-off permissions.

## Vault And Plugin Integrations

Vault is a bridge, not a permission source of truth. Keep permissions in
LuckPerms and use Vault so plugins can query groups, prefixes, suffixes, and
economy integrations.

When triaging plugin access:

1. Confirm the plugin exposes a documented permission node.
2. Check whether the plugin expects Vault or native LuckPerms hooks.
3. Run a permission check against the exact user and server context.
4. Apply the node at group level when multiple users need the feature.

## Audit And Rollback

Before risky changes:

```mcfunction
/lp export permissions-before-change
```

After validation:

```mcfunction
/lp user Alex info
/lp group moderator info
```

Rollback options:

- Unset the specific permission node.
- Remove the temporary parent.
- Restore from the exported permission snapshot if multiple changes interacted.

## Crossplay Notes

For Geyser/Floodgate servers:

- Confirm the username format visible to LuckPerms.
- Keep Bedrock test users in non-staff groups until authentication is verified.
- Use contexts when Bedrock access should differ from Java access.
