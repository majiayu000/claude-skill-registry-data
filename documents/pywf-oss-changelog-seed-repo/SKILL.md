---
name: pywf-oss-changelog-seed-repo
description: "Seed repo only: bump the version this cookiecutter seed repo shares with its template repo, and write that version's section in release-history-seed-repo.rst, never in release-history.rst. Use in the seed repo instead of pywf-oss-changelog, and before the changelog step of pywf-oss-release, whenever the user wants to update the changelog, record a change, bump the version, or release."
---

This repo is the **seed repo** of the cookiecutter template [cookiecutter-pywf_open_source](https://github.com/MacHu-GWU/cookiecutter-pywf_open_source) (the **template repo**). The template repo turns this repo into a template, so a change here is a change to every project generated afterwards. This skill bumps the shared version and writes its section in `release-history-seed-repo.rst`. It is never copied into the template.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/22-versioning-and-changelog.md, for the section format and the categories only

## Rules

- **Two changelogs, two jobs.**

  | File | What it is | Edited by a seed release? |
  | :--- | :--- | :--- |
  | `release-history-seed-repo.rst` | This seed repo's own changelog | yes, by this skill |
  | `release-history.rst` | Template content: the starting changelog of every generated project | **never** |

  `pywf-oss-changelog`, and step 2 of `pywf-oss-release`, write to `release-history.rst`. In this repo, use this skill for that step instead. `mise run sync` in the template repo fails when `release-history.rst` has a section for the current version.

- **One version for two repos.** `version` in this repo's `pyproject.toml` is the version of the template too. The template repo copies it on `mise run sync`, links every template release to its section here, and refuses to publish when the two differ. Never bump the version in the template repo.
- **Seed-only files.** `release-history-seed-repo.rst` and this skill are listed in `EXCLUDE` of the template repo's `.mise/tasks/make_template.py`, so they stay out of the template. The `pywf-oss-*` skills in the template never mention them.
- **A released version is frozen.** Never reuse a version that has a tag in this repo or in the template repo. Fix a bad release with a new PATCH version.
- **Every template release needs a new seed version.** When a template release changes only the template repo (its parameterization or hooks), still bump the version here, and write a section with one **Miscellaneous** entry: "No changes to the seed; this version changes the template repo only."

## Step 1: Gather state

```bash
git status --short                          # uncommitted work is invisible to git log
git describe --tags --abbrev=0              # last seed tag: the baseline
grep '^version' pyproject.toml              # current version
git ls-remote --tags https://github.com/MacHu-GWU/cookiecutter-pywf_open_source  # template tags
```

Tags older than `3.0.0` are from the time the seed had its own version. Show any uncommitted work, and ask for the user's yes to include it.

## Step 2: Choose the version

Judge from the side of **a person generating a project from the template**, not from `api.py`: the sample package of the seed has no users.

| Level | When | Examples |
| :--- | :--- | :--- |
| MAJOR | Existing template input breaks: a cookiecutter variable is renamed, removed, or changes meaning, or the core toolchain of generated projects is replaced | rename a variable, switch the package manager |
| MINOR | Generated projects gain something, compatibly | a new mise task, docs page, CI step, or skill |
| PATCH | Fixes and small adjustments | fix a doc, upgrade a dependency, adjust a default |

The new version must be above the current version, the last seed tag, and the last template tag. Propose the level with a one-line reason, then apply it after the user's yes: edit `pyproject.toml`, then `mise run inst`, so the bump changes exactly `pyproject.toml` and `uv.lock`.

## Step 3: Read the changes

```bash
git log <last_tag>..HEAD --oneline
git diff <last_tag>..HEAD --stat
```

Read the diffs of whatever changed: skills, mise tasks, CI, docs, dependencies, sample code. They are the ground truth.

## Step 4: Write the section

- Insert `VERSION (YYYY-MM-DD)` with today's date directly below the `x.y.z (Backlog)` block, or correct the section if it exists. Never edit the Backlog.
- Follow the format and the category order of `22-versioning-and-changelog.md`.
- Write each entry as what a newly generated project gets or loses, not which seed file changed.
- Keep the heading exactly `VERSION (YYYY-MM-DD)`: the template repo builds its link to this section from that heading, such as `#300-2026-10-23` for `3.0.0 (2026-10-23)`.

Edit the file directly: it is tracked by git.

## Next steps

In this order; each public step needs the user's yes:

1. **This repo:** `mise run cov`, `mise run lint`, and `mise run build-doc` pass.
2. **Template repo:** `mise run e2e` passes (it regenerates the template from this working tree, checks it, and runs a generated project's `cov` and `build-doc`); the user reviews the artifact diff there.
3. **This repo:** commit and push to `main`, then `mise run publish` and `mise run release`, the same as steps 4 to 6 of `pywf-oss-release`. The tag `<version>` is what the template's changelog links to.
4. **Template repo:** `/cctpl-release-cn`.
