---
name: doc-link-convention
description: This skill should be used when writing or reviewing cross-file links inside Maigo source files (`agents/*.md`, `commands/*.md`, `skills/*/SKILL.md`). It enforces that cross-source links use absolute GitHub URLs — relative links break `mkdocs build --strict` because these files are dual-context (raw GitHub view + include-markdown shim into `docs/`).
---

<!-- mkdocs-include-start -->

# Doc Link Convention

**Owner Agent**: Soyo (Reviewer) — flagged at review-time when editing Maigo source.
**Consumers**: any task editing `agents/` / `commands/` / `skills/` in the Maigo repo.

## When to apply

Maigo's `agents/*.md`, `commands/*.md`, and `skills/*/SKILL.md` are **dual-context**:

- They are read raw on GitHub by contributors / `claude --plugin-dir`.
- They are also pulled into the docs site via `docs/{agents,commands,skills}/<name>.md` include-markdown shims.

A relative cross-source link works in one view but breaks the other.

## The rule

**Cross-source link → absolute GitHub URL. No exceptions.**

```markdown
[/maigo:remember](https://github.com/Lee-W/maigo/blob/main/commands/remember.md)
```

**Not:**

```markdown
[/maigo:remember](remember.md)                         <!-- ❌ relative -->
[/maigo:remember](../commands/remember.md)             <!-- ❌ relative -->
[/maigo:remember](/commands/remember.md)               <!-- ❌ root-relative -->
```

## Why a relative link breaks `mkdocs build --strict`

`include-markdown` defaults to `rewrite-relative-urls=true`. When it inlines
`commands/remember.md` into `docs/commands/remember.md`, it rewrites relative
URLs from the destination page's perspective. But the source path
(`commands/remember.md`) differs from the mkdocs page path
(`docs/commands/remember.md`, which is a shim), so the rewrite points at a
location mkdocs cannot resolve → `Aborted with N warnings in strict mode!`.

Absolute URLs are not rewritten by `include-markdown`, so both the GitHub
raw view and the mkdocs page resolve correctly.

Disabling `rewrite-relative-urls` is also wrong: cross-directory relative
links to *real* reference docs (e.g. `../docs/reference/memory.md`) rely on
the rewrite to become mkdocs-resolvable.

## Exception: links to real reference docs

When the link target is a real doc page under `docs/reference/` or
`docs/guides/` (**not** a shim), a relative link is correct because
`rewrite-relative-urls=true` will produce the right final URL:

```markdown
[Memory reference](../docs/reference/memory.md)
```

From a `commands/<x>.md` source file, that rewrites to `../reference/memory.md`
in `docs/commands/<x>.md` — which correctly points at `docs/reference/memory.md`.

| Link target type | Use |
|---|---|
| Another source file (`agents/*.md`, `commands/*.md`, `skills/*/SKILL.md`) | **Absolute GitHub URL** |
| Real reference doc (`docs/reference/*.md`, `docs/guides/*.md`) | Relative (`../docs/reference/foo.md`) |
| Same source file (anchor only) | Plain anchor (`#section-name`) |

## Review-time enforcement (Soyo)

When `strict-review` runs on a diff that touches `agents/`, `commands/`, or
`skills/*/SKILL.md` in the Maigo repo itself, append this rule as **base
checklist item 10**:

- Search the diff for `]\(` followed by anything that does **not** start with
  `http://` / `https://` / `#` / `../docs/`. If the link target is another
  source file → **must-fix** with改法: rewrite to
  `https://github.com/Lee-W/maigo/blob/main/<source-path>`.

This is only a checklist item when editing Maigo itself. Downstream projects
using Maigo as a plugin do not need this rule — it is specific to Maigo's
own dual-context publishing setup.

## What this skill does NOT cover

- Link targets *outside* the Maigo repo (use whatever the target convention is).
- The 6-step new-skill checklist — see [Skills reference](https://github.com/Lee-W/maigo/blob/main/docs/reference/skills.md#add-new-skill-checklist).
- mkdocs configuration itself — this skill assumes `rewrite-relative-urls=true`
  default and `--strict` build.
