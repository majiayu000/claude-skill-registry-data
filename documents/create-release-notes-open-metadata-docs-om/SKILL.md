---
name: create-release-notes
description: Create or update product-update / release-notes content for a given OpenMetadata/Collate patch version across getcollate, openmetadata-site, and docs-om. Sources getcollate's changelog from openmetadata-collate + OpenMetadata + ai-platform; openmetadata-site's from OpenMetadata only; docs-om reuses openmetadata-site's already-written content, reformatted into its Mintlify snippet structure. Filters to customer-facing changes only, runs each target's own doc-review checklist, verifies every link live, and requires explicit approval before any commit.
user-invocable: true
argument-hint: "<version, e.g. 2.0.4> [--targets=getcollate,openmetadata-site,docs-om|all] [--skip-docs-om]"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Agent
---

# Create Release Notes

Produces the release-notes/product-update content for one patch version,
for up to three targets, following the exact process worked out
interactively across the getcollate v2.0.1–v2.0.3 and v1.13.5–v1.13.6
releases. Read `references/process.md` before doing any real work — it has
the full step-by-step mechanics, the per-target repo config, and every
gotcha this process has actually hit.

## When to activate

The user asks to create, draft, or update release notes / product updates
/ a changelog for a specific version, for getcollate, openmetadata-site,
docs-om, or "all three" / "everywhere."

## Repos this touches

All three are expected as sibling directories next to this one
(`~/Documents/GitHub/<repo>`), already cloned:

| Repo | Role |
|---|---|
| `getcollate` | Collate's own site. Output: `content/product-updates/vX.Y.Z.md` |
| `openmetadata-site` | OSS-only public site. Output: `content/product-updates/vX.Y.Z.md` (same format, independent id/versions.json, OSS-only content) |
| `docs-om` | OSS docs site. Output: `snippets/releases/X.Y.Z.mdx`, imported into `vX.Y.x/releases/X.Y-release.mdx` |

If any expected repo isn't present at that path, stop and ask for its
location rather than guessing or skipping it silently.

## High-level flow (detail in references/process.md)

Run this once per target the user asked for, in this order: **getcollate
→ openmetadata-site → docs-om** (docs-om depends on openmetadata-site's
finished content, so it must run last, and only after openmetadata-site's
file is written — it is never independently re-derived from commits).

For **getcollate** and **openmetadata-site** (same mechanics, different
source-repo set and content scope — see the table in
`references/process.md` §1):

1. `cd` into the repo, `git checkout main && git pull`.
2. Determine the previous version and next id from `versions.json`.
3. Create a new branch: `product-updates/vX.Y.Z`.
4. Resolve the commit range per source repo (tag-to-tag if the next
   version's tag already exists, else tag-to-branch-HEAD with the
   re-verification caveat in `references/process.md` §2).
5. Fetch, paginate, filter, categorize, bundle (§3–§5).
6. Write the file, update `versions.json`.
7. Customer-facing filter pass (§6) — re-read every bullet, drop anything
   with no stated end-user/admin-facing symptom.
8. Doc-review pass using **that repo's own** `.ai/doc-review/` checklist
   (§7).
9. Live link-check every citation (§8).
10. Run the repo's build (`yarn build` for both Next.js sites) (§9).
11. Start the local server and give the user the preview URL. **Do not
    commit.** Wait for the user to say to commit, exactly as they asked.

For **docs-om** (§10 — a reformat, not a re-derivation):

1. `cd` into `docs-om`, `git checkout main && git pull`, new branch
   `release-notes/vX.Y.Z`.
2. Take the **finished, already-approved** openmetadata-site content for
   this version (not a fresh commit pull) and wrap it into an `<Update>`
   snippet per `references/process.md` §10.
3. Add the new snippet's import + `<ReleaseNotes />` tag at the top of
   the matching `vX.Y.x/releases/X.Y-release.mdx`, update the "Upgrade to
   X" card text.
4. Run docs-om's **own** `.ai/doc-review/` checklist against the new
   snippet (its rules may differ from openmetadata-site/getcollate's).
5. Live link-check again (the GitHub-release link line is new to this
   format and easy to typo).
6. Preview (Mintlify dev server if available, otherwise render the mdx
   mentally and show the user the file) and wait for commit approval.

## Non-negotiable checks (every target, every run)

These came from real mistakes made while building this process by hand —
see `references/process.md` §11 for the full incident behind each one:

- **Verify every commit's merge timestamp falls strictly between the
  previous and current release tags.** A commit that merges after the
  target tag was cut does not belong in that release, even if its PR
  title matches the theme — cite it in the *next* version instead.
- **Cite the actual merged/backport PR, never a referenced issue number
  or an earlier PR the commit message happens to mention in passing.**
  Verify with `gh api repos/<owner>/<repo>/pulls/<n>` before trusting any
  number.
- **Never fabricate a commit SHA for a fallback link.** If citing a raw
  commit instead of a PR, fetch the real full SHA first.
- **Cap every bundled bullet at 3 PR links.** Split into two bullets if a
  natural bundle would exceed that.
- **Collapse a fix that landed as matching PRs in both OpenMetadata and
  openmetadata-collate down to the OpenMetadata link only** — they are
  the same fix, not two.
- **Link labels are plain `[#NNNNN]`** — no `Collate`/`OSS`/`AI Platform`
  prefix in the visible text (the URL itself already disambiguates).
- **No trailing period after the date** in frontmatter or in
  `versions.json` entries for files this skill creates — check the
  target repo's own existing convention before assuming, since it can
  differ per repo/file vintage.
- **Bold the symptom, not the fix** — every bullet title states the
  problem a user or admin would recognize; the sentence after the colon
  states what changed and, where it isn't obvious, why it matters.

## Output discipline

- Never commit or push without the user explicitly saying to, even if
  everything passed every check. Build success and a clean doc-review are
  not the same thing as approval.
- Never touch `yarn.lock` or `public/sitemap.xml` on purpose — if
  `yarn install`/`yarn build` regenerates them as a side effect,
  `git checkout --` them back before staging anything, and don't stage
  them even if the user says "commit everything."
- One branch per repo per version. Don't reuse a branch across versions,
  and don't put more than one version's content in a single branch/PR
  unless the user asks for that explicitly.
