---
name: msb-repo-sandboxes
description: "Sandboxes with no project folder: source = \"repo\", msbctl add --repo, fetch_repo_policy() through github_api() pinned to a resolved commit, policy update, the named -workspace disk volume made by bootstrap's do_clone with an inline credential helper, and every rule that differs from a folder sandbox (edit_target always the registry, guest_path may be neither host nor dotted, extra_rules and secret_binds ADD to the repo's, require_project_file and move refuse, ssh_keys = []). Use when changing repo-sourced sandboxes or when policy fetching, cloning or rebuilding one misbehaves."
---

# Repo Sandboxes

Detail carved out of `AGENTS.md`, which keeps only what has to hold in
every session. Repo-specific throughout; the facts here are verified against
msb 0.7.6 and re-checked on 0.7.7.

`source = "repo"` entries (`msbctl add --repo`, `cmd_add_repo()`) have `repo`/`ref` and no `project`. `Sandbox.project` is then `policy_dir(name)` (`STATE_DIR/policy/<name>/`): the repo's `.msb/sandbox.toml` and `dev.yaml` fetched by `fetch_repo_policy()` through `github_api()` (which, unlike `http_json()`, tells a 404 — "no file" — from every other failure, and dies on the latter) at a resolved commit, plus `meta.json`. It is never mounted; the clone is a named disk volume (`workspace_volume`, `-workspace`) at `guest_project`, made by bootstrap's `do_clone` (`MSB_CLONE_URL`/`MSB_CLONE_REF`) with an inline credential helper handing git the `GH_TOKEN` placeholder. `rebuild` never refetches (`ensure_repo_policy()` only fills a missing dir, at the approved `_commit`); `msbctl policy <name> update` moves the pin. `project_policy()` includes `_commit`. For these sandboxes `extra_rules` and `secret_binds` from the registry ADD to the repo's (`registry_binds` tracks which may use `global.env`), `edit_target()` is always the registry, `require_project_file()`/`move` refuse, `guest_path` may be neither `"host"` nor dotted, GH_TOKEN is always bound when stored, and `ssh_keys = []` lets the agent filter run with no host agent at all.
