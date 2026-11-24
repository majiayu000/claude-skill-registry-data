---
name: release
description: 'Cut a release of the Senzing Bootcamp plugin: bump the version everywhere it is asserted, write the CHANGELOG entry, commit and create the git tag — as one operation, with no path that moves one without the others. Use when the maintainer wants to release, cut a release, bump the version, tag a version, or prepare a version for the downstream repos to port from. Stops short of publishing; /propagate-to-public is the next step. Maintainer tool — not part of the bootcamper experience.'
argument-hint: "[major|minor|patch, or an explicit version like 0.6.0] (omit and you will be asked)"
---

# Release

A **maintainer** tool for developing the Senzing Bootcamp Claude Plugin (SBCP).
Never invoked during a bootcamp. It is the step *before*
[`propagate-to-public`](../propagate-to-public/SKILL.md): this skill decides and
records **which version exists**; that one publishes it.

This is a **release-path action**. The work is done by [`release.py`](release.py) in
this skill's directory, for the same reason `propagate-to-public` fronts `python3 -m tools.bootcamp_build promote` — the operation has to be
all-or-nothing, and a procedure a model follows step by step is exactly a procedure
that can stop after step two. Here the steps are one function call.

## The defect this exists to prevent

The sibling repo `Senzing/senzing-bootcamp-kiro-power` carries a CHANGELOG entry
reading `[0.5.3] - 2026-09-10` while its newest git tag is still `0.5.1`. The
changelog moved; the tag did not.

⛔ **That is not tidiness.** Under the porting model, the downstream development
repositories (Kiro, ChatGPT, Copilot) port from a **tagged release** of Claude
rather than from HEAD. A version that was never tagged is invisible to the
mechanism that governs the whole system: *a port cannot target a release that was
never tagged.*

Of the three things a release moves, two were already guarded here and one was not:

| Moves | Guarded before this skill? |
|---|---|
| `source/bootcamp.json` | — |
| the shipped example recap's `**Plugin version:**` row | ✅ `tests/test_example_recap_sync.py` pins it to the manifest |
| the git tag | ⛔ **nothing related a version to a tag at all** |

So a release could bump both files, pass the whole suite, and ship untagged. That
is the kiro-power shape, and it is what `release.py` and
`tests/test_release_bumps_version_changelog_and_tag_together.py` make impossible.

## What it does, in one unit

1. Rewrites every entry in `VERSION_SITES`: the two files above. `source/bootcamp.json` is
   the one declaration the build copies the version from into every assistant's generated
   manifest, so no generated file is a site.
2. **Re-renders the shipped example recap PDF** from the `.md` it just rewrote, because
   that version is *drawn* — onto the cover card and again as the certificate colophon —
   and no text substitution can reach it.

   ⛔ **(INV-301) A rendered artifact is a record that asserts the version, and a drawn
   version moves only by rendering.** This is not optional tidying: the 0.7.0 release
   moved every text site and left the committed PDF reading 0.6.1 — the artifact
   `README.md` offers as the sample deliverable (#697).
3. Creates `CHANGELOG.md` if absent — **seeded from the tags that already exist**,
   one entry each, newest first — and prepends the new entry thereafter. The entry it
   writes is **curated**, and what it leaves out it reports; see
   [CHANGELOG.md](#changelogmd) below.
4. Commits those files, and **only** those files.
5. Tags **that commit**, annotated — annotated because `git push --follow-tags` silently skips lightweight tags (INV-301).

⛔ **(INV-301) The commit comes before the tag, and that ordering is load-bearing.** Edit the
files and then run `git tag` and you tag **HEAD** — the commit *before* the bump. The
tag exists, the name is right, and checking it out gives you the previous release
under the new name. The test reads the three files *out of the tag* for exactly this
reason; asserting only that a tag exists passes against the broken version.

⛔ **(INV-301) There is no flag that performs part of a release.** No `--no-tag`, no
`--changelog-only`. Any such flag reintroduces the defect, and a test asserts the
interface offers none.

## How to run it

```console
.claude/skills/release/release.py --minor          # preview (writes nothing)
.claude/skills/release/release.py --patch --apply  # do it
.claude/skills/release/release.py 0.6.0 --apply    # explicit target
```

**The argument names the bump.** Pass `major`, `minor` or `patch` as
`--major`/`--minor`/`--patch`, and an explicit `MAJOR.MINOR.PATCH` version positionally.
With no argument, run the dry run with no bump named, show the maintainer the current
version and the newest tag, and ask, as *Never invent the version* under Guardrails says.

⛔ **Dry run is the default; `--apply` is what writes.** This script is fronted by a
slash command, so it can be run by a model. Git tags are **repository-global** — a
tag is not scoped to a worktree, and once anyone has fetched it, it cannot be taken
back. A destructive default is not acceptable under those conditions. `--dry-run` is
accepted explicitly so a caller can state the intent rather than depend on a default
staying what it is.

**Always show the maintainer the dry run and let them approve it before `--apply`.**
The dry run prints the exact diff of both version sites, the changelog entry it would
write, every commit subject it kept out of that entry and why, and the three git
commands — that is what approval is given on.

### The refusals

The script exits non-zero and changes nothing when:

| Refusal | Why |
|---|---|
| the working tree is dirty | the release commit must carry the bump and nothing else, and the tree is what `python3 -m tools.bootcamp_build promote` builds from — an uncommitted file is either swept into the release commit or published untracked |
| the version does not advance | past the manifest **and** past the newest tag; a version that is not strictly newer stops being a key |
| the tag already exists | re-pointing a tag rewrites what a downstream repo may already have fetched |
| the manifest and the newest tag disagree | the kiro-power split as a *starting* state — releasing from it buries the inconsistency one version deeper. `--allow-divergent-base` exists but only after you have decided which of the two is right |
| a version site is missing, or stops matching | releasing now would advance the other site and leave this one stale — the exact split the tool exists to prevent |
| the example recap PDF cannot be re-rendered | a shipped artifact whose version is *drawn* can only be moved by rendering it, so releasing without that ships it stating the previous version |
| the re-render fell back to the stdlib writer | the fallback embeds no images and draws no branded certificate, so accepting it would swap the shipped keepsake for a plainer one at exit 0. Install `fpdf2` and release again |
| the branch is not `main` | a tag made on a feature branch survives a squash-merge as a pointer to a commit that never lands on `main`, so a downstream repo porting from it gets a tree `main` does not contain. `--allow-branch` if you mean it |

⚠️ **The dirty-tree refusal has no override, deliberately.** The acceptance criterion
is that it refuses; a flag to proceed anyway is the path that makes it advisory.

## CHANGELOG.md

`CHANGELOG.md` did not exist in this repo before this skill, so the first `--apply`
**creates** it, reconstructing one entry per existing tag from the commit subjects
between tags. Two things about that seed are deliberate:

- ⚠️ **It is labeled as reconstructed, and the label names the versions it covers**
  ("entries *X.Y.Z and earlier*"), not "entries below". Written positionally, the
  sentence is true the day the file is seeded and false the next release, because a
  prepended entry lands between the note and the entries it describes.
- The **earliest** tag is not itemized. Everything before the first release would
  otherwise land in it, which is noise rather than history.

⚠️ **Seeded entries are commit subjects, not release notes**, and the seed note says so
of exactly the versions it names. They are honest about what happened and say nothing about
why. Curating them by hand is a fine thing to do; just never edit an entry's
`## [version] - date` heading, because the version, the file and the tag were written
together on purpose.

⛔ **(INV-381) A standing note about what a file's entries are is a promise the writer owes,
not a label on the past (#698).** The seed note's boundary is the newest tag at seed time, so
every entry above it was written by a release — and read either way round the note tells the
downstream porter, at the one place they look, that those entries are curated release notes
rather than commit subjects. So `release.py` curates each entry it writes, in three
mechanical operations and no others:

1. **Drop the subjects that describe no change** — a bare word such as `Savepoint`, with or
   without a leading `#456`; a subject that is bookkeeping only, an issue reference or a type
   prefix with nothing after it, such as `#456` or `fix:`; and a merge subject. Nothing else is
   dropped.
2. **Keep every remaining subject's own wording verbatim.**
3. **Group the kept bullets under their own conventional-commit type** — `### fix`,
   `### docs`, and `### other` for a subject carrying no type — in the order the types first
   appear in the range.

⛔ **(INV-381) No bullet's description is ever written here.** A subject whose meaning cannot be read
out of its own text is kept exactly as the commit wrote it: dropping it would lose a real
change, and rewriting it would put words in the maintainer's mouth about a release they cut.
Curation here is mechanical, or it is fabrication.

⛔ **(INV-382) What it drops, it reports: the dry run prints every subject it kept out of the entry,
with the reason, under `--- subjects carrying no change description ---`.** A badly named
commit is something only the maintainer can fix, and only for the next one; a silent filter
would make the next `Savepoint`-shaped subject vanish without anyone learning the commit was
named that way.

⚠️ **The entries this repository already carries were curated to match the note** when the
rule landed: `[0.7.0]`, `[0.6.1]` and `[0.6.0]` lost seven contentless bullets between them
and their remaining subjects were grouped. `[0.5.3]` and earlier were deliberately left as
they are — the note says they are reconstructed commit subjects, which is true and is what a
reader should be told about them. `tests/test_changelog_entries_are_what_the_note_says.py`
holds the file to both halves and derives the boundary from the note itself.

⚠️ **Tag dates are read off the commit, not off the tag object.** The seven tags this
repo already carries are lightweight and have no date of their own. New tags are
annotated, so both shapes keep working.

## After it runs

⛔ **(INV-301) `/release` does not publish, and must not.** It does not push and it does not
invoke `/propagate-to-public`. Report the new version, the commit and the tag, then
name the next steps and stop:

1. Run the suite — `python3 -m unittest discover -s tests` — against the release
   commit. Nothing in `release.py` runs it, and a red release is worth catching before
   it is published rather than after.
2. `/propagate-to-public` to mirror the shippable plugin into the public access repo.
3. Push the branch **and the tag**. ⚠️ `git push` alone does not send tags; an unpushed
   tag is invisible to the downstream repositories that port from it, which is the
   original defect wearing a different hat.

Steps 2 and 3 are the maintainer's to run. Do not run them as part of a release unless
asked.

## Guardrails

- **Never run the script without showing the dry run first.** Approval is given on the
  diff, not on the intent.
- **Never push.** Not the branch, not the tag.
- **Never hand-edit one of the three things.** Bumping `bootcamp.json` by hand, or adding
  a changelog entry by hand, is how the two repos drifted in the first place. If the
  script refuses, fix what it refused on — do not do its job manually.
- **Never invent the version.** (INV-333) Ask the maintainer for the bump size (or the explicit
  version) if they did not say; `release.py` refuses a bare invocation for the same
  reason, so a defaulted patch bump cannot slip through.
- If a **new** file starts asserting the version, add it to `VERSION_SITES` in
  `release.py`. `tests/test_release_covers_every_version_site.py` scans the tracked
  files and fails on the commit that introduces an unlisted one, so this is caught
  before a release ships it stale rather than after. That guard scans in **both**
  directions (#697): a file stating the version about to move, and a file left behind at
  a version already moved past — the second being how three sites survived the 0.7.0
  release unnoticed.
- **Never hand-edit the example recap `.md` without re-rendering its `.pdf`.** The guard
  compares the PDF's extracted text to the manifest, so the pair cannot drift silently;
  the command sits in the docstring of `tests/test_example_recap_sync.py`.

⚠️ **If `tag.gpgsign` is set in the maintainer's git config, the tag is signed** and
git may prompt for a passphrase. The script does not override that setting — a
maintainer's signing policy is not a release tool's to switch off — so an unattended
run can block there. Say so rather than retrying.

## Scope note

⛔ **This skill is development-repo only and must NOT be propagated to the public
plugin repo.** `.claude/` is not among the paths `python3 -m tools.bootcamp_build promote`
writes: every assistant's package under `plugins/`, each assistant's catalog file, `docs/`
from `site/`, and each file under `public/` at the same path from the root.
