---
name: rename-project
description: Rename this SaaS Bootstrap project from its neutral "SaaS Bootstrap" branding to a real project name. Use when the user asks to rename the boilerplate, configure the project name, rebrand package metadata, Docker/image names, docs, UI metadata, seeds, or remaining legacy project-name references.
disable-model-invocation: true
---

# Rename Project

Use this skill to turn the neutral boilerplate branding into a concrete product name without leaving stale project references behind.

## Workflow

1. Confirm the target name from the user request. If the request only gives one name, treat it as the display name and derive:
   - `slug`: lowercase kebab-case, for package names, buckets, Docker/image tags, client IDs and URLs.
   - `python_name`: lowercase underscore form, only if a Python import/package identifier is needed.
   - `display_name`: the exact user-facing name.
2. Read project context first: `AGENTS.md`, `README.md`, `PRODUCT.md`, `DESIGN.md`, and package metadata in `backend/pyproject.toml`, `frontend/package.json`, and `docs/package.json` when present.
3. Run the bundled script in dry-run mode from the repo root:

```bash
python3 <skill-dir>/scripts/rename_project.py "New Name" --root . --dry-run
```

Resolve `<skill-dir>` from this loaded `SKILL.md`. The canonical source is
`.claude/skills/rename-project`; Codex and OpenCode read the synchronized copy in
`.agents/skills/rename-project`.

4. Review the dry-run file list. If it includes generated output or vendor files, stop and narrow the command with `--exclude`.
5. Run the script without `--dry-run`.
6. Search for leftovers:

```bash
rg -n -i "saas[-_ ]?bootstrap" \
  -g '!node_modules' -g '!.git' -g '!**/.next/**' -g '!**/.venv/**' \
  -g '!**/skills/**' -g '!*.lock' -g '!*-lock.*'
```

   The pattern covers the name tokens (`project_name`, `project_slug`,
   `python_name`) in `scripts/branding_tokens.json`. The script does not replace
   `owner_email` (`owner@example.com`); search for it separately and ask the user
   for a real address before changing it:

```bash
rg -n "owner@example\.com" \
  -g '!node_modules' -g '!.git' -g '!**/skills/**' -g '!template/**'
```

   If that inventory gains a token, search for it too instead of adding names
   here.

7. Manually fix context-specific leftovers. Do not blindly replace:
   - `SaaS Bootstrap` if it still describes the template rather than the target product (for example inside this skill's own files).
   - `Llamitai/saas-bootstrap-template` when it identifies the published
     upstream Copier mirror. `preserve_literals` in the branding inventory
     keeps that source URL usable in generated and renamed projects.
   - author emails or GitHub orgs unless the user provided replacements.
   - lockfiles: the script skips them; regenerate them with the package manager (`pnpm -C frontend install`, `pnpm -C docs install`, `uv lock --directory backend`) after renaming instead of editing them by hand.
8. Validate with the repo's normal checks when practical. For this project, prefer:
   - `just frontend typecheck` for frontend metadata/type changes.
   - `just backend typecheck` or `just backend test` for backend/package changes.

## Script Behavior

Tokens, context rules, and exclusions live in `scripts/branding_tokens.json`
at the repo root — the single source shared with `scripts/build_template.py`
(the Copier template builder). The script fails fast if that file is missing;
edit the JSON rather than the script when the token inventory changes.

The script replaces the current neutral branding tokens:

- `SaaS Bootstrap` -> display name
- `saas-bootstrap` -> slug (also covers derived names such as `saas-bootstrap-api`, `saas-bootstrap-web`, `saas-bootstrap-docs`, and `app.saas-bootstrap.web`)
- `saas_bootstrap` -> python_name (snake_case slug)

It is context-aware for common package metadata lines. For `name = "SaaS Bootstrap"` and `"name": "SaaS Bootstrap"`, it writes the slug form instead of the display name, so package metadata stays valid.

The script excludes dependency directories, caches, generated builds, `.git`, lockfiles, `.env.deploy*` files, all skill folders (`.agents/skills`, `.claude/skills`, `.codex/skills`, `.opencode/skills`), and the Copier template scaffolding (`template/`, `scripts/branding_tokens.json`, `scripts/build_template.py`, `just/template.just`, `.github/workflows/publish-template.yml`, `docs/content/docs/equipo/publicacion-de-plantilla.md`) listed in `rename_exclude_extra.paths`. This prevents the skill from renaming its own instructions or corrupting the template machinery.

Note: projects generated with Copier (`uvx copier copy gh:Llamitai/saas-bootstrap-template ...`) arrive already renamed and can be updated with `copier update`; this skill is the path for GitHub-template/clone copies.

## Manual Follow-Up Checklist

After running the script, verify:

- App metadata: `frontend/src/app/layout.tsx`, Open Graph/Twitter image text, manifest files.
- Package metadata: `backend/pyproject.toml`, `frontend/package.json`, `docs/package.json`; regenerate lockfiles if tracked.
- Deployment metadata: Docker Compose `name`, image names, GitHub Actions, Portainer/registry names.
- Runtime defaults: `.env.example`, seed users/tenant names, support email, app URLs.
- Docs: `README.md`, `AGENTS.md`, docs site copy, diagrams.
- Code identifiers: keep replaced identifiers valid, for example `saas_bootstrap_db` must become a valid snake_case name, never a name containing spaces or hyphens.
