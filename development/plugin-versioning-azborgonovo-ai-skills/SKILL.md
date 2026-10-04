---
name: plugin-versioning
description: How to bump a plugin's SemVer version in .claude-plugin/plugin.json before committing changes under skills/<plugin>/. Use before every commit that touches a plugin's skill files (drafts under skills/drafts/ are exempt), and when a commit spans multiple plugins that need different bump levels.
---

Each plugin under `skills/<plugin>/` pins an explicit `version` in its `.claude-plugin/plugin.json`. Claude Code treats that string as the update key. So the version of a plugin **must** increase whenever any of its skills change. Otherwise installed users never receive the change.

Versions follow [SemVer](https://semver.org), taken from the same Conventional Commit type that you write on the commit. A breaking change gives MAJOR. A `feat` gives MINOR. Everything else gives PATCH, which covers `fix`, `docs`, `refactor`, `chore`, and the rest.

**Before every commit**, check `git status` for changed files under any `skills/<plugin>/` path. Drafts under `skills/drafts/` are not plugins, and they are never versioned. When the skill files of a plugin changed, run the bundled `scripts/upgrade-plugin-versions.py`, relative to this SKILL.md. Pass the exact Conventional Commit message that you are about to commit, and include the edits of the script in that same commit:

```
python .claude/skills/plugin-versioning/scripts/upgrade-plugin-versions.py --message "feat(bdd): add scenario linter"
```

The script bumps only the plugins whose skill files changed, and it updates the `version` in each `plugin.json`. It is idempotent, so a second run before the commit lands does not double-bump. **Why the message**: the commit does not exist yet, so the script reads the bump level from the message that you pass. Use `--major`, `--minor`, or `--patch` to override the level when the message type does not capture the intent.

**When a commit touches more than one plugin**, the level of that single message applies to every changed plugin. That is correct when the plugins share one intent, such as a repo-wide `docs:` fix or a `refactor:` that bumps them all the same. When the plugins need *different* levels, prefer splitting the work into one commit per plugin, because a Conventional Commit describes one logical change. When they genuinely belong together, bump each plugin on its own with `--plugin`:

```
python .claude/skills/plugin-versioning/scripts/upgrade-plugin-versions.py --plugin bdd --minor
python .claude/skills/plugin-versioning/scripts/upgrade-plugin-versions.py --plugin decisions --patch
```

The marketplace-wide `version` in `.claude-plugin/marketplace.json` is separate. Bump it by hand only for a marketplace-structure change, which is a plugin added, removed, or renamed.

**Working across several commits on an unmerged branch**: the script bumps relative to HEAD, so one call per commit compounds. The HEAD of each new commit already includes the previous bump. A branch with three `feat`-sized commits then ends up three versions higher than it needs to be. None of those intermediate versions were ever released, because `main` never saw them. Only the version present when the branch finally merges is real.

Bump once for the whole branch instead, sized to the highest-order Conventional Commit type across all of its commits. A single `feat` anywhere means MINOR for the branch as a whole, even when the other commits on it are `fix`, `docs`, or `chore`. When you already bumped per commit before you noticed, collapse it. Reset `version` back to the value it held before the branch started, then bump once at that level.
