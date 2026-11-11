---
name: scaffold-agent-project
description: Scaffold a project-root agent-guidance layout with AGENTS.md, domain and specification indexes, and an application-delivery skill. Use when starting a repository or standardizing its agent documentation; do not use to modify an established layout without review.
---

# Scaffold agent project

Create the personal project-standard layout without overwriting existing guidance.
The scaffold supplies structure; domain details and project commands remain unconfigured.

## Before scaffolding

1. Confirm the intended project root and inspect existing `AGENTS.md`, `.agents/`,
   `docs/`, and tracker state.
2. For an established repository, show planned files first. Preserve existing
   guidance and delivery authority; do not replace it or merge around collisions
   unless the user explicitly requests a separate customization step.
3. Reuse a known tracker: choose `--tracker beads` for Beads or
   `--tracker repository` for another repository-declared tracker. If none exists
   or is requested, use the default `--tracker none`. Do not infer tracker setup
   permission from the presence of its executable.

## Run the scaffold

Resolve `scripts/scaffold.py` relative to this loaded skill's directory; it need
not exist inside the target project. Preview first:

```text
python3 <skill-directory>/scripts/scaffold.py --target <project-root> --tracker <none|beads|repository> --dry-run
```

If preview succeeds, run with the same target, name, and tracker options without
`--dry-run`:

```text
python3 <skill-directory>/scripts/scaffold.py --target <project-root> --tracker <none|beads|repository>
```

Use `--project-name` only when a display name other than the directory name is
requested. The script refuses existing destination entries, symlinks, invalid
parent paths, unreadable templates, and observable write restrictions before
writing. Never bypass a refusal or delete existing files to proceed. A preview
cannot guarantee later writes will succeed; report actual results separately.

`--tracker beads` selects guidance without initializing Beads. Confirm its actual
state before reporting it as usable. Add `--with-beads` only when the user requests
local Beads initialization; this flag implies `beads` if `--tracker` is omitted,
and rejects an explicitly incompatible tracker. `--initialize-beads` is a
compatibility alias. Initialization delegates to `setup-beads`, which remains the
single owner of Beads storage, safety, and hook policy.

If creation fails unexpectedly, report the created and missing files, preserve
partial output, and stop. Do not rerun over it. If guidance creation succeeds but
Beads setup fails, report those stages separately and use `setup-beads` for any
authorized retry rather than rerunning the scaffold.

## Verify and hand off

Confirm the five expected files exist and reflect the selected tracker. Report
preview and actual creation results, tracker selection, whether initialization
was attempted and succeeded, and any blocked or partial output. Do not describe
this layout as a fully configured project: commands and domain content still
need a separately requested customization step.

After successful scaffolding, stop. Do not fill placeholders or modify generated
files unless customization is explicitly requested. Small, well-understood
changes may use the generated delivery workflow directly without new
specifications or vertical-slice plans; substantial or consequential changes
retain those planning steps and all changes retain relevant validation.

## Resulting layout

The scaffold creates `AGENTS.md`, `GLOSSARY.md`, `docs/specs/README.md`, and the
project-local `application-delivery` skill with its workflow reference. Read
[the layout reference](references/layout.md) when assessing the generated files.
