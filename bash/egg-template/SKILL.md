---
name: egg-template
description: |
  Create or update egg templates. Use when user wants to: (1) create a new template from scratch, (2) add/modify/remove macros, (3) update template files or lifecycle hooks, (4) convert files to Stencil format. For fetching/pinning/syncing existing templates from a repo (egg template install, eggs.yml manifests, egg template sync/update), use egg-cli-guide instead.
---

# egg Template

## Operation Detection

| User Intent | Operation |
|-------------|-----------|
| "create template", "new template" | Create |
| "add macro", "modify", "rename", "remove" | Update |
| Template name/path + changes | Update |
| "install this template repo", "add/pin/sync templates from a repo", "keep templates up to date across machines" | Not this skill — use `egg-cli-guide`'s `egg template install` (one-shot fetch) or `eggs.yml` manifest + `egg template sync`/`update` (declarative, reproducible) |

## Create Workflow

1. **Ask setup questions** (AskUserQuestion - all at once):
   - Template name
   - Location: Project (`./.eggs/`) | Global (`~/.eggs/`) | Repository
   - Mode: config.yml only | Full scaffolding

2. **Define macros** → See [references/config-spec.md](references/config-spec.md)

3. **Configure lifecycle hooks** (optional) → See [references/lifecycle.md](references/lifecycle.md).
   When writing `run:` commands, read its "Shell Quoting in `run:`" section first — wrapping `___MACRO___` or `${{ ... }}` in your own quotes silently corrupts the value.

4. **Configure hatch**: output, excludes

5. **Generate config.yml**

6. **Scaffolding** (if full mode) → See [references/template-files.md](references/template-files.md)

7. **Validate**: `egg template validate <path>`

## Update Workflow

1. **Locate template**:
   - By name: `egg template detail <name>`
   - By path: Verify `config.yml` exists

2. **Analyze**: Read config.yml, list files

3. **Check dependencies** → See [references/update.md](references/update.md)

4. **Apply changes**

5. **Validate**: `egg template validate <path>`

## Key Commands

```bash
egg template detail <name>    # Show info
egg template open <name>      # Open in Finder
egg template validate <path>  # Validate
egg hatch preview <name> --macro-name value ...   # Test as a transaction (no writes yet)
egg hatch apply <applyToken>                      # Commit the test run
```

## References

- [references/config-spec.md](references/config-spec.md) - config.yml syntax, macro types
- [references/lifecycle.md](references/lifecycle.md) - pre_hatch/post_hatch hooks, step outputs
- [references/template-files.md](references/template-files.md) - Native vs Stencil syntax
- [references/create.md](references/create.md) - initial questions, location, scaffolding, repository structure
- [references/update.md](references/update.md) - dependency checks before modifying an existing template
- [references/update.md](references/update.md) - dependency checking, rename/remove operations
