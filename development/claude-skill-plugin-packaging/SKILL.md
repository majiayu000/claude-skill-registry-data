---
name: claude-skill-plugin-packaging
description: Package Claude Code skills as a plugin plus marketplace and install them into other repos — globally, pinned per project via committed settings, or as a skills-dir plugin. Use when sharing skills across repos, wiring an existing skill plugin into a project, choosing flat project skills versus a plugin, aggregating other people's skill repos by reference, or when a submodule or nested folder of skills is not being discovered. Does not cover PR/issue mechanics (github-contribution-workflow) or how to write the skill itself (skill-authoring-patterns).
---

# Claude Code Skill Plugin Packaging

## Native mechanism

[Plugins](https://code.claude.com/docs/en/plugins) and [plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) are Claude Code's own distribution mechanism — a marketplace repo with `.claude-plugin/marketplace.json` gives "centralized discovery, version tracking, automatic updates". What the official docs don't spell out in one place is the depth-1 discovery trap and the install-model tradeoffs below — that's what this skill adds.

- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.

## When to invoke

- You have skills in one repo and want them reusable across other repos/projects.
- Wiring an existing skill plugin (e.g. `apple-dev-skills`) into a new project.
- Deciding **flat project skills** vs a **plugin**.
- A submodule/nested folder of skills "isn't being discovered" and you don't know why.
- Aggregating *other people's* skill repos without copy-pasting.
- User asks "how do I share/install skills", "why is my `.claude/skills/<lib>/...` not found".

## The one rule that explains everything: plain-skill discovery is depth-1 — unless the nested tree is itself a plugin

Claude Code discovers **plain project skills only at depth 1**:
`.claude/skills/<skill>/SKILL.md`. It does **not** recurse into subdirectories.

Consequences (each has burned someone):
- A **git submodule** of skills at `.claude/skills/<lib>/` puts SKILL.md at
  `.claude/skills/<lib>/skills/<skill>/SKILL.md` (depth ≥ 2) → **NOT discovered as a
  plain skill**.
- A bare folder of skills nested one level down → **NOT discovered as a plain skill**.
- An in-repo submodule of a plugin you *also* installed via a marketplace is
  **vestigial for that installed copy** — the marketplace-installed copy is what loads,
  the submodule does nothing for discovery.

**But** a nested skill *tree* is still found if its root is itself a plugin (carries
`.claude-plugin/plugin.json`) — it self-loads on the next session as `<lib>@skills-dir`,
with no marketplace and no install step (project scope: after the workspace-trust
dialog; must launch from the session's primary working directory, no walk-up to a
parent project). This is `claude plugin init`'s documented default, not an
experimental feature — see Model D below. It only fails to help when the repo you're
vendoring is a *marketplace* (root has `marketplace.json` but no `plugin.json`) rather
than a single plugin — which is this catalog's own shape, so a bare submodule of
*this* repo still needs Model B1 or B2.

## Packaging: make your skills a plugin + marketplace

A repo becomes a Claude Code **plugin** with a manifest, and a **marketplace**
(catalog) with a second manifest. One repo can be both (single-repo model):

```
your-skills-repo/
├── .claude-plugin/
│   ├── plugin.json        # makes it a plugin; "name" becomes the namespace
│   └── marketplace.json   # makes it a marketplace; lists plugins
└── skills/
    └── <skill>/SKILL.md   # one dir per skill
```

`plugin.json` (the `name` is the **plugin** namespace prefix — skills surface as `plugin-name:<skill>`; this is independent of the marketplace name):
```json
{ "name": "your-skills", "version": "0.1.0", "description": "…", "license": "MIT" }
```

The **marketplace** `name` is the catalog identifier used in `/plugin install plugin-name@marketplace-name`. These are two distinct names that happen to be the same string in the single-repo model — that identity is a coincidence, not a requirement. A real-world example where they differ: `"code-formatter@company-tools"` (plugin name = `code-formatter`, marketplace name = `company-tools`).

`marketplace.json` — lists this plugin (and can list MANY plugins from other sources):
```json
{
  "name": "your-skills",
  "owner": { "name": "you" },
  "plugins": [
    { "name": "your-skills", "source": "./", "description": "…", "version": "0.1.0" }
  ]
}
```
`"source": "./"` = the plugin is at the marketplace repo root.

## Installing (consuming) into a project — pick a model

| Model | Pinned? | Per-repo commit? | Install step? | Use when |
|---|---|---|---|---|
| A. Global marketplace | No (latest) | No | `/plugin install` once, globally | Personal use across many repos |
| B1. Marketplace `github`+`ref` | Yes (git ref) | Yes (`settings.json`) | None for this plugin; **external-source plugins still need `claude plugin install` per collaborator (≥v2.1.195)** | Team default — no submodule needed |
| B2. Vendored submodule + `directory` source | Yes (commit SHA) | Yes | None | SHA-level pin, or fully offline vendoring |
| D. Submodule of a single-plugin repo | Yes (commit SHA) | No (self-loads) | None, after trust dialog | The repo you vendor already ships `plugin.json` at its root |
| C. npm (flat, non-plugin) | Depends on registry | No | `npx skills add` | One skill set, no aggregation needed |

### A. Global marketplace (simplest, latest)
```
/plugin marketplace add owner/your-skills-repo
/plugin install your-skills@your-skills
```
Loads globally (every project), namespaced. Not pinned per repo.

### B1. Marketplace `ref` pin, no submodule (recommended default for a team)

Commit to the project's `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "your-skills": {
      "source": { "source": "github", "repo": "owner/your-skills-repo", "ref": "v0.1.0" }
    }
  },
  "enabledPlugins": { "your-skills@your-skills": true }
}
```
No submodule, no vendoring — Claude Code resolves the pinned `ref` on trust. **Caveat
(since v2.1.195)**: auto-install-on-trust applies to plugins declared via a relative/
`directory` source; a plugin whose source is *external* (`github`, `npm`, `url`,
`git-subdir`) — like the aggregated github / git-subdir entries in §Aggregating —
is *enabled* in settings but each collaborator still has
to run the `claude plugin install` command Claude Code prints on first load. The
**marketplace source** (`extraKnownMarketplaces` / `marketplace add`) — where this
`marketplace.json` itself is fetched from — takes `ref` but not `sha`; for an
exact-commit pin use B2.

### B2. Vendored submodule + project-scope committed settings (SHA-level pin, offline-capable)

Use this when a repo must depend on an exact **commit SHA**, or must work without
network access to the plugin's origin — B1 only pins a `ref`, not a `sha`.

1. Vendor + pin:
   ```
   git submodule add https://github.com/owner/your-skills-repo.git .claude/skills/your-skills
   cd .claude/skills/your-skills && git checkout v0.1.0 && cd -
   ```
2. Commit this to the project's `.claude/settings.json` (the **shared, committed**
   file — not `.claude/settings.local.json`, which is personal/gitignored):
   ```json
   {
     "extraKnownMarketplaces": {
       "your-skills": {
         "source": { "source": "directory", "path": "./.claude/skills/your-skills" }
       }
     },
     "enabledPlugins": { "<plugin-name>@<marketplace-name>": true }
   }
   ```
   Replace `<plugin-name>` with the `name` from the plugin's `plugin.json` and `<marketplace-name>` with the `name` from the marketplace's `marketplace.json`. In the single-repo model these happen to be the same string (e.g. `"your-skills@your-skills": true`), but they are conceptually distinct — the plugin namespace and the catalog identifier.
   - The marketplace `source` for a local dir is an **object** `{"source":"directory","path":"./relative"}` — a **relative** path. Relative plugin sources resolve for marketplaces added from a git source *or* a local directory; they fail only when the marketplace was added by a direct URL to `marketplace.json`. A `directory` source path resolves against the *containing* repo's main checkout — including from inside a worktree of it — regardless of whether the target itself is a git repo. The docs label `directory` sources "for development only"; prefer B1 for a team default and reserve B2 for the SHA-pin/offline case.
3. On `git clone --recurse-submodules` + workspace-trust, Claude Code
   auto-registers the marketplace and enables the plugin. Skills load as
   `your-skills:<skill>`. **No `/plugin install` step** for this relative/`directory`-sourced
   plugin — but see B1's v2.1.195 caveat if this marketplace also aggregates externally-sourced
   plugins.

Why both pieces: the **submodule** pins the exact version (a commit SHA); the
**committed settings.json** is what actually makes Claude Code load it. Either alone
is insufficient (submodule-only = not discovered; settings-only = nothing to point at).

### D. Submodule of a single-plugin repo (self-loading, no settings.json needed)

If the repo you're vendoring has `.claude-plugin/plugin.json` at its **root** (not just
a `marketplace.json`), a plain submodule under `.claude/skills/` or `~/.claude/skills/`
is enough:
```
git submodule add https://github.com/owner/single-plugin-repo.git .claude/skills/their-plugin
cd .claude/skills/their-plugin && git checkout v0.1.0 && cd -
```
On the next session (after the project-scope trust dialog), it self-loads as
`their-plugin@skills-dir` — no marketplace, no install step, no settings.json edit.
Caveats: the same primary-working-directory / trust-dialog rule stated above applies
(exact version gate: `references/official-docs.md`); and because a project-scope
skills-dir plugin's content comes from the repository, its code-running components are
gated further — MCP servers it declares go through the same per-server approval as a
project `.mcp.json`, LSP servers start only after you trust the workspace, and
background monitors do not load (personal-scope `~/.claude/skills/` plugins have none of
these restrictions). **This repo's own root has only `marketplace.json`,
not `plugin.json`, so a bare submodule of *this* repo does not self-load this way — use
B1 or B2.**

### C. npm (flat, non-plugin install)

`npx skills add` installs skills flatly — see README §C and `scripts/install-flat.sh`.
It reads `marketplace.json` / `plugin.json`, but only follows locally-declared skill
paths — it does not fetch the aggregated externals' remote `github` / `git-subdir`
sources (below), so those are skipped. Use it for a single skill set with no
aggregation needs, not for this catalog's full plugin set.

## Aggregating other skill repos (don't reinvent)

A marketplace is a catalog of plugins from **many sources** — that is the native
aggregation mechanism, no submodule required. Add more entries to `plugins[]`,
each with its own source:

```json
"plugins": [
  { "name": "your-skills",        "source": "./" },
  { "name": "someones-testing",   "source": { "source": "github", "repo": "them/testing-skills" } },
  { "name": "vendored-thing",     "source": { "source": "git-subdir", "url": "https://…", "path": "tools/plugin" } }
]
```
Accepted plugin source types (relative path, `github`, `url`, `git-subdir`, `npm`, `archive`,
`command`) and the exact fields and Claude Code version each requires drift with new
releases — read `references/official-docs.md` rather than trusting a hardcoded list. Use a
submodule only when you need to **vendor + pin** another repo's content into yours (Model B2
or D above).

## Gotchas (verified)

- **Bare submodule of a multi-plugin repo (root has only `marketplace.json`) ≠ discovered.**
  Pair it with the `extraKnownMarketplaces` + `enabledPlugins` settings (Model B2) — or,
  if the submodule's own root has `plugin.json` instead, it self-loads on its own (Model D).
- **Marketplace state is per-user** (`~/.claude/plugins/known_marketplaces.json`), but the **committed project `.claude/settings.json` declaration** is what makes it reproducible for everyone on trust. Marketplace names are checked against a reserved list (`claude-code-marketplace`, `anthropic-marketplace`, `agent-skills`, …) — adding a new marketplace under a reserved name is rejected outright, and Claude Code re-checks the name on every load, so an *existing* marketplace whose name later becomes reserved stops loading too, erroring with "is registered from an untrusted source" ([errors reference](https://code.claude.com/docs/en/errors#marketplace-is-registered-from-an-untrusted-source)). Fix: remove it and re-add from the official source, or rename it and have users re-add from yours.
- **Token cost**: every enabled skill's description is always-on context — for the exact
  mechanism see the listing-budget reference doc under `skill-authoring-patterns`. `/doctor`
  and `/skill-doctor` show the actual per-session cost. `skillOverrides: "name-only"` only
  demotes personal/project skills — it does **not** apply to plugin skills ("Plugin skills
  are not affected by `skillOverrides`. Manage those through `/plugin` instead."); for a
  plugin the only levers are disabling it via `/plugin`, or raising the consumer's
  `skillListingBudgetFraction`.
- **Relative marketplace paths**: see B2 step 2 above for the exact resolution rule and its
  one exception (direct-URL marketplaces) — [Create and distribute a plugin
  marketplace](https://code.claude.com/docs/en/plugin-marketplaces#relative-paths).
- **A skill/plugin `name` containing "claude"** loads fine in Claude Code — this skill's own
  name is proof, and `claude-hud`/`claude-mem` ship the same way — but is rejected by the
  platform Agent Skills spec's reserved-word rule. This only matters if the skill is ever
  uploaded to claude.ai, the Skills API, or packaged with `package_skill.py`; the Claude Code
  plugin path this skill describes is unaffected.

## Verification

- `git commit -a` skips new files — `plugin.json`/`marketplace.json` are new, so `-a` silently omits them. Use explicit `git add` and verify with `git show --stat --summary` (plain `--stat` doesn't print the `create mode` lines new files need).
- `/reload-plugins` then check the skills list shows `your-skills:<skill>` entries.
- `claude plugin details your-skills@your-skills` lists the bundled skills, agents, and
  token cost — not scope. **Scope** (`user` / `project`) comes from `claude plugin list`;
  a project-scope plugin only resolves from inside that project, so running either command
  from elsewhere returns `Plugin "…" not found`.
- For model B2: `git ls-files .claude/settings.json` (it's committed) and the submodule
  gitlink point at the intended version.

## Related skills

- `github-contribution-workflow` — routes plugin distribution/installation questions here; that skill owns PR/issue mechanics, this one owns packaging and discovery.
- `skill-authoring-patterns` — routes distribution/packaging questions here once a skill is authored; that skill owns authoring conventions, this one owns how the finished skill gets shared.
