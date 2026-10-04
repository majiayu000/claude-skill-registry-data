---
name: plugins
description: "Claude Code plugin and marketplace engineering: `plugin.json` and `marketplace.json` manifests, component layout (skills, agents, hooks, MCP/LSP, monitors, themes, bin), plugin sources and hosting, team/enterprise rollout and lockdown, plugin dependencies, and versioning/release mechanics for a plugin and the skills and agents it ships. WHEN: \"plugin.json\", \"marketplace.json\", \"plugin marketplace\", \"claude plugin validate\", \"claude plugin install\", \"claude plugin init\", \"--plugin-dir\", \"/reload-plugins\", \"enabledPlugins\", \"extraKnownMarketplaces\", \"strictKnownMarketplaces\", \"pluginConfigs\", \"plugin version bump\", \"private marketplace\", \"CLAUDE_PLUGIN_ROOT\", \"plugin dependencies\", \"claude plugin tag\", \"renames\", \"@skills-dir\". Do NOT use for authoring the SKILL.md content inside a plugin (frontmatter, progressive disclosure, token budgeting) — that's the `agent-skills` skill; for general Claude Code harness configuration (settings.json scopes, permission rules, hook event semantics, subagent behavior, headless/CI, auth) — that's `claude-code`; for the Model Context Protocol itself (spec, transports, writing servers) — that's `mcp`."
license: MIT
---

# Claude Code plugins and marketplaces

A plugin is a directory of components (skills, agents, hooks, MCP/LSP servers, monitors, themes, executables) that installs as one unit. A marketplace is a `marketplace.json` catalog that distributes plugins with version tracking and updates. This skill covers packaging, distributing, versioning, and operating them.

Corpus fetched 2026-08-05 against `code.claude.com/docs`. Many behaviors are gated on a CLI version (`v2.1.x+`); check `claude --version` before debugging a "missing" feature.

## Answering rules

Always run `claude plugin validate` before claiming a manifest is correct — it catches required-field, JSON-syntax, path, and `renames`-chain errors that only surface as silent load failures at runtime. Add `--strict` in CI to turn warnings into failures.

Always determine the **version resolution source** before diagnosing "users aren't getting my update". `plugin.json` `version` beats the marketplace entry beats the git SHA — a stale `plugin.json` version silently masks a bumped marketplace entry.

Never put `skills/`, `agents/`, `commands/`, or `hooks/` inside `.claude-plugin/`. Only `plugin.json` goes there; everything else lives at the plugin root. This is the single most common reason components don't appear.

Never reference paths outside the plugin directory (`../shared-utils`). Install copies the plugin into `~/.claude/plugins/cache` — files outside it are not copied. Share within a marketplace via symlinks instead.

Always use `${CLAUDE_PLUGIN_ROOT}` for bundled scripts and configs, and never write state there — it changes on every update. Persistent state goes in `${CLAUDE_PLUGIN_DATA}`.

Never treat plugins as a sandbox. Plugins and marketplaces execute arbitrary code with the user's privileges; Anthropic does not verify third-party plugin contents. Install only from trusted sources, and restrict org-wide with `strictKnownMarketplaces`.

## Plugin or standalone `.claude/`?

| Use | When |
|---|---|
| Standalone `.claude/` (skill invoked as `/hello`) | Single project, personal config, experiments, you want short unnamespaced names |
| Plugin (skill invoked as `/plugin-name:hello`) | Sharing with a team or community, same components across projects, versioned releases, marketplace distribution |

Plugin skills are always namespaced by the plugin `name` — that is what prevents cross-plugin collisions. Migration mechanics (what moves where, and the agent-override trap) are in `references/quickstart-and-migration.md`.

## Layout

```text
my-plugin/
├── .claude-plugin/plugin.json   # manifest — the ONLY thing in this directory
├── skills/<name>/SKILL.md       # skills
├── commands/*.md                # flat-file skills (legacy shape; prefer skills/)
├── agents/*.md                  # subagents
├── hooks/hooks.json             # hook config
├── .mcp.json  .lsp.json         # MCP / LSP servers
├── monitors/monitors.json       # background monitors
├── themes/*.json  output-styles/*.md  workflows/
├── bin/                         # executables added to the Bash tool PATH
├── settings.json                # defaults on enable (`agent`, `subagentStatusLine` only)
└── scripts/  LICENSE  CHANGELOG.md
```

The manifest is **optional**: with no `plugin.json`, Claude Code auto-discovers the default directories and names the plugin after its directory. A plugin root `CLAUDE.md` is **not** loaded as context — ship instructions as a skill.

A plugin shipping exactly one skill may put `SKILL.md` at the plugin root; set frontmatter `name` explicitly, because the fallback is the install directory name (a version string that changes on every marketplace update).

Read `references/components.md` for every component's config format, plugin-agent frontmatter restrictions, the scoped names plugin hooks must use to target their own MCP server, and `@skills-dir` plugins.

## `plugin.json`

`name` is the only required field. It is the namespace (`/my-plugin:hello`, `my-plugin:code-reviewer`) and the stable identity used by `enabledPlugins`, `pluginConfigs`, and `/plugin install`.

```json
{
  "name": "deployment-tools",
  "displayName": "Deployment Tools",
  "version": "2.1.0",
  "description": "Deployment automation tools",
  "author": { "name": "Dev Team", "email": "dev@company.com" },
  "license": "MIT",
  "keywords": ["deployment", "ci-cd"],
  "skills": "./custom/skills/",
  "dependencies": [{ "name": "secrets-vault", "version": "~2.1.0" }]
}
```

Rules that bite:

- **Path fields**: `commands`, `agents`, `workflows`, `outputStyles`, `experimental.themes`, `experimental.monitors` **replace** their default directory. `skills` **adds** to the default `skills/` scan — except for a marketplace entry whose `source` is the marketplace root, where listed subdirectories become the complete set.
- All paths are relative to the plugin root and start with `./`; `skills` also accepts `"."`. No absolute paths, no `..`.
- **Unrecognized top-level fields are ignored** and reported as warnings, so a `package.json`/VS Code manifest can coexist. Wrong *types* are errors and fail the load — except `experimental` and `metadata`, where a non-object is only a warning.
- `defaultEnabled: false` ships a plugin installed-but-off (v2.1.154+). An existing `enabledPlugins` entry and a dependency requirement both override it.
- `userConfig` prompts the user for values at enable time; `${user_config.KEY}` substitutes into MCP/LSP configs and hook commands, but is **rejected** in shell-form hook commands, monitor commands, and MCP `headersHelper` (shell-injection guard) — read `CLAUDE_PLUGIN_OPTION_<KEY>` from the environment instead.
- `pluginConfigs` is read only from user settings, `--settings`, and managed settings. Project and local settings entries are **ignored** so a cloned repo cannot inject values into hook commands. `enabledPlugins` is unaffected by this restriction.

Path variables, resolved inline in skill/agent content, hook and monitor commands, and MCP/LSP server fields:

| Variable | Meaning |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin install directory — changes every update, treat as ephemeral |
| `${CLAUDE_PLUGIN_DATA}` | `~/.claude/plugins/data/{id}/`, survives updates, deleted on last-scope uninstall unless `--keep-data` |
| `${CLAUDE_PROJECT_DIR}` | Project root |

Read `references/plugin-manifest.md` for the complete field tables, `userConfig` schema and storage, `channels`, the cache/symlink rules, and the `SessionStart` dependency-reinstall pattern.

## `marketplace.json`

Required: `name`, `owner`, `plugins`. Put it at `.claude-plugin/marketplace.json` in the repository root.

```json
{
  "name": "company-tools",
  "owner": { "name": "DevTools Team", "email": "devtools@example.com" },
  "metadata": { "pluginRoot": "./plugins" },
  "plugins": [
    { "name": "code-formatter", "source": "./plugins/formatter", "version": "2.1.0" },
    { "name": "deployment-tools", "source": { "source": "github", "repo": "company/deploy-plugin" } }
  ]
}
```

A plugin entry accepts **any** `plugin.json` field plus `source`, `category`, `tags`, `strict`, `relevance`, `defaultEnabled`.

| `source` | Shape |
|---|---|
| Relative path | `"./plugins/my-plugin"` — must start with `./`, no `..`, resolved from the marketplace root |
| `github` | `{ "source": "github", "repo": "owner/repo", "ref?", "sha?" }` |
| `url` | `{ "source": "url", "url": "https://…", "ref?", "sha?" }` |
| `git-subdir` | `{ "source": "git-subdir", "url": …, "path": "tools/plugin", "ref?", "sha?" }` — sparse clone for monorepos |
| `npm` | `{ "source": "npm", "package": "@acme/plugin", "version?", "registry?" }` |

When both `ref` and `sha` are set, `sha` is the effective pin. Relative paths do **not** resolve when the marketplace was added by direct URL to `marketplace.json` — only that one file is downloaded.

`strict` defaults to `true` (the `plugin.json` is authority; the entry supplements). `strict: false` makes the entry the entire definition — and a `plugin.json` that also declares components then becomes a load-failing conflict.

Each user may register only **one** marketplace per name; adding a second with the same name replaces the first. Anthropic reserves a list of marketplace names, re-checked on every load, so a marketplace whose name later becomes reserved stops loading — see `references/marketplace-schema.md`.

Worked example in this repo: `.claude-plugin/marketplace.json` uses `metadata.pluginRoot: "./plugins"`, one relative-path entry per domain plugin, and a top-level `renames` map; each plugin pins its own `version` in `plugins/<domain>/.claude-plugin/plugin.json`.

Read `references/marketplace-schema.md` for the full field tables, shared-`skills/` entry patterns, and the organization-sync source restrictions on Team/Enterprise.

## Versioning and releases

Version is the **cache key**. If the resolved version equals the installed one, update is skipped. Resolution order, first set wins:

1. `version` in `plugin.json`
2. `version` in the marketplace entry
3. Git commit SHA of the plugin source (git-backed sources)
4. `unknown` (npm sources, non-git local dirs)

| Strategy | How | Update behavior | Fits |
|---|---|---|---|
| Explicit version | `"version": "2.1.0"` in `plugin.json` | Only on bump — pushing commits does nothing | Published plugins, stable releases |
| Commit-SHA | Omit `version` everywhere | Every new commit is an update | Internal, actively developed plugins |

Never set `version` in both `plugin.json` and the marketplace entry: `plugin.json` wins **silently**, so a stale manifest masks the version you bumped in the catalog. The docs state the semver convention directly (MAJOR breaking / MINOR features / PATCH fixes) and recommend a `CHANGELOG.md`.

**Bump on every release or existing users never receive it.** This is the failure mode behind almost every "my fix didn't reach anyone" report — it applies to the skills, agents, and hooks inside the plugin too, since they ship only as part of a resolved plugin version.

**Release channels**: two marketplaces pointing at different `ref`s of the same repo, assigned by group via managed `extraKnownMarketplaces`. Each channel must resolve to a *different* version string, or updates are skipped as identical.

**Renaming**: changing `name` breaks every install. Use `displayName` to relabel the UI. To really rename or remove, add a top-level `renames` entry (`"old": "new"` or `"old": null`, v2.1.193+); Claude Code rewrites `enabledPlugins`/`pluginConfigs` keys in writable scopes and shows a one-line notice. Treat `renames` as **append-only** — chains are followed hop by hop, and `claude plugin validate` rejects a chain that cycles or does not terminate at `null` or a listed plugin. Managed-settings entries are read-only, so the notice recurs each session until an admin updates them.

**Dependency tags**: version constraints resolve against git tags named `{plugin-name}--v{version}` on the marketplace repo. Create with `claude plugin tag --push`.

Read `references/hosting-and-versioning.md` for private-repo credentials, container seeding, auto-update behavior, and the full rename semantics.

## Dependencies

```json
{ "name": "deploy-kit", "version": "3.1.0",
  "dependencies": ["audit-logger", { "name": "secrets-vault", "version": "~2.1.0" }] }
```

Bare string = any version the marketplace provides; object adds a Node-`semver` range and an optional `marketplace`. Unconstrained dependencies track latest, so an upstream release can break every install on auto-update — constrain anything you test against.

Cross-marketplace dependencies are refused unless the **root** marketplace lists the target in `allowCrossMarketplaceDependenciesOn`; trust does not chain through intermediates.

A manifest of just `name` + `dependencies` is a **bundle plugin** — the cleanest way to ship "the standard set" to a team, then add tools by publishing a new bundle version.

Errors (`dependency-unsatisfied`, `range-conflict`, `dependency-version-unsatisfied`, `no-matching-tag`) disable the dependent plugin until resolved; find them in `/plugin` Errors or `claude plugin list --json`. Read `references/dependencies.md` for range intersection, tag resolution details, and per-error resolution steps.

## Team rollout

Project `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "company-tools": { "source": { "source": "github", "repo": "your-org/claude-plugins" } }
  },
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

Teammates are prompted to install when they trust the folder. As of v2.1.195 an externally sourced plugin enabled only by project settings does not load until the member runs the `claude plugin install` command Claude Code prints.

Marketplace state is per user in `~/.claude/plugins/known_marketplaces.json`, not per project; local `directory` sources resolve against the repo's main checkout, so worktrees share it.

Private repos: interactive commands use your normal git credential helpers, but the **background auto-update pull disables credential helpers**, so HTTPS private fetches fail there. Fix with an SSH remote plus `ssh-agent`, or a scoped global git URL rewrite. `GITHUB_TOKEN` alone does nothing.

Containers/CI: prebuild `~/.claude/plugins` and point `CLAUDE_CODE_PLUGIN_SEED_DIR` at it — read-only, precedence over user config, no runtime cloning.

## Enterprise lockdown

Managed-settings-only controls:

| Setting | Effect |
|---|---|
| `strictKnownMarketplaces` | Allowlist of addable marketplace sources. `[]` = total lockdown incl. the official marketplace. Exact matching; prefer `hostPattern`/`pathPattern` regex entries over literal URLs |
| `blockedMarketplaces` | Denylist, checked before any download |
| `disableSideloadFlags` | Rejects `--plugin-dir`, `--plugin-url`, `--agents`, `--mcp-config` (v2.1.193+) |
| `pluginSuggestionMarketplaces` | Which marketplaces may surface "suggested for this directory" plugins |

`strictKnownMarketplaces` restricts what can be *added*; it does not register anything. Pair it with `extraKnownMarketplaces` in the same managed settings, or users on locked-down machines end up with no marketplace at all. Enforcement runs on add **and** on every install/update/refresh, so a pre-existing marketplace that no longer matches stops updating.

Read `references/team-and-enterprise.md` for scope precedence, managed-settings delivery mechanisms, and the exact allowlist matching rules.

## Develop, test, validate

```bash
claude plugin init my-tool --with skills hooks   # scaffold into ~/.claude/skills/ as my-tool@skills-dir
claude --plugin-dir ./my-plugin                  # session-only; beats an installed plugin of the same name
claude --plugin-url https://ci/artifact.zip      # session-only from a hosted .zip
claude plugin validate ./my-plugin --strict      # CI gate
claude plugin details my-plugin                  # component inventory + projected token cost
```

`/reload-plugins` picks up changes without a restart (skills reload immediately from `SKILL.md` edits; other components need the reload). Its skill count only counts `commands/` directories, so `0 skills` after reloading a `skills/`-based skill is a display artifact, not a failure.

Validate before publishing anywhere — the community-marketplace review pipeline runs the same check plus safety screening.

**Practice recommendations** (advice, not documented behavior): keep `version` only in `plugin.json` so there is one source of truth; run `claude plugin validate . --strict` on every PR touching a manifest; pin `sha` rather than `ref` for third-party sources in regulated environments; keep a `CHANGELOG.md` entry per bump so `/plugin` users can tell what changed.

## Debugging

Start with `claude --debug` (shows plugin load, manifest errors, component registration, MCP init) and the `/plugin` **Errors** tab.

| Symptom | Cause | Fix |
|---|---|---|
| Plugin doesn't load | Invalid `plugin.json` | `claude plugin validate ./my-plugin` |
| Skills missing | Components inside `.claude-plugin/` | Move to plugin root |
| Hooks never fire | Script not executable, or wrong event case | `chmod +x`, `PostToolUse` not `postToolUse` |
| MCP server fails | Path not using `${CLAUDE_PLUGIN_ROOT}` | Use the variable everywhere |
| Path errors | Absolute path, or missing `./` | Make relative, prefix `./` |
| `conflicting manifests` | `strict: false` plus a component-declaring `plugin.json` | Drop one of the two definitions |
| Whole plugin gone after adding hooks | Malformed `hooks/hooks.json` | Fix JSON — it blocks the entire plugin |
| Old name reports `plugin-not-found` | Client below v2.1.193 ignores `renames` | Upgrade, or reinstall under the new name |

Read `references/cli-and-debugging.md` for every `claude plugin` subcommand and flag, the `/plugin` UI behavior, and the full validation error/warning catalog.

## Unverified

The exact JSON **shape** of `enabledPlugins` and `pluginConfigs` when an administrator writes them directly into managed settings (as opposed to Claude Code writing them via `/plugin install` or the `userConfig` prompt) could not be confirmed against a verbatim source page in this corpus. The object-map forms shown above are confirmed for user/project settings and for values Claude Code writes itself. Verify managed-settings shapes against the live settings reference before deploying policy.

## Reference files

- `references/plugin-manifest.md` — every `plugin.json` field, path-field semantics, `userConfig`, `channels`, env vars, cache and symlink rules
- `references/components.md` — skills, agents, hooks, MCP, LSP, monitors, themes, `bin/`, plugin `settings.json`, `@skills-dir` plugins
- `references/marketplace-schema.md` — `marketplace.json` schema, plugin entries, sources, strict mode, reserved names, org sync
- `references/hosting-and-versioning.md` — hosting, private repos, seeding, version resolution, release channels, `renames`
- `references/dependencies.md` — `dependencies` field, semver ranges, cross-marketplace allowlist, tagging, error catalog
- `references/cli-and-debugging.md` — `claude plugin` CLI reference, `/plugin` UI, auto-update, debugging, validation catalog
- `references/team-and-enterprise.md` — install scopes, settings keys, `strictKnownMarketplaces` and friends
- `references/quickstart-and-migration.md` — minimal plugin end-to-end, migrating `.claude/`, official marketplace catalog

## Diagnostic script

- `scripts/lint-plugin-manifests.py` — read-only lint of a `plugin.json` and/or `.claude-plugin/marketplace.json` against documented rules (required fields, component-dir placement, path shapes, dual-version pinning, duplicate/reserved names, `renames` chain termination, cross-marketplace dependency allowlist). Complements `claude plugin validate`; it does not replace it.

## Sources

- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/plugin-marketplaces
- https://code.claude.com/docs/en/plugin-dependencies
- https://code.claude.com/docs/en/discover-plugins
- https://code.claude.com/docs/en/settings

Fetched: 2026-08-05
