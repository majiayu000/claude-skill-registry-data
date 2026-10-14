---
name: craft-plugin-update
description: Release a plugin version. Bump plugin.json, then commit.
---

# Skill: Craft Plugin Update

> "Bump, commit, push. In that order."

## When

Run this when releasing a new version of a plugin.

## The Protocol

1. **Bump the version** in the plugin's own `plugin.json`
   - Patch: bug fixes, docs
   - Minor: new skills, features
   - Major: breaking changes

   One place. `marketplace.json` names plugins and where they live, and carries no version — the
   field is optional and Claude Code falls back to `plugin.json`. A second copy made one shared line
   every branch edits, so plugin work collided for packaging reasons.

2. **Update changelog** (if exists)
   - Date + version header
   - Brief summary of changes

3. **Commit with conventional format**
   ```
   chore({plugin-name}): bump to {version}
   ```

4. **Push and merge** to main

## The Versioning

| Change Type        | Bump  | Example       |
|--------------------|-------|---------------|
| Bug fix            | Patch | 1.0.0 → 1.0.1 |
| New skill          | Minor | 1.0.0 → 1.1.0 |
| Skill refinement   | Patch | 1.0.1 → 1.0.2 |
| Breaking change    | Major | 1.0.0 → 2.0.0 |
| Docs only          | Patch | 1.0.0 → 1.0.1 |

## The Anti-Patterns

- **Forgetting the bump**: Merge without version update
- **Wrong bump type**: Major for a typo fix
- **No commit message**: Generic "update" message

## The Output

State: "Bumped `{plugin}` to `{version}`. Pushed."
