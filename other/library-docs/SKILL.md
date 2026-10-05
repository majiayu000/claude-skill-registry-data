---
name: library-docs
description: Generate and refresh a per-repo `library-use` reference — official docs, changelog links, pinned versions, and distilled correct-usage conventions for the repo's fast-moving / niche libraries. Use when the user says "library-docs", "doc links", "document the libraries we use", "generate/refresh library docs", "library conventions", or wants a per-repo doc-links reference the agent (and `review-library-use`) can consult. On re-run it version-checks every entry and updates it.
argument-hint: '[target dir] [--refresh] [--force-all]'
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Library Docs

Build (and keep current) a **per-repo reference** of the libraries this project actually
depends on: canonical docs + changelog URLs, the version the repo resolves, and a short
list of the *most important correct-usage conventions* for that version — the things a
model gets wrong from stale training data.

The reference is written as a repo-local skill at **`.claude/skills/library-use/SKILL.md`**
so it (a) auto-triggers when the agent touches one of those libraries and (b) is the
convention source that `review-library-use` audits code against. This skill is the
**generator/maintainer**; `review-library-use` is the reviewer. Keep them distinct.

## What this skill is NOT
- Not a full doc dump — distill to a few high-value bullets per library (token-lean, on-demand).
- Not for every dependency — curate to the tail the model doesn't already know (see Step 2).
- Not a reviewer — it writes the reference; `review-library-use` checks code against it.

## Instructions

### Step 1: Resolve the target repo and mode
- Target dir = the non-flag argument, else the current working directory. Must be a git repo root (has `.git` or a manifest).
- **First run** (no `.claude/skills/library-use/SKILL.md` yet) → generate from scratch.
- **Re-run** (it exists, or `--refresh`) → refresh mode (Step 6).
- `--force-all` reconsiders the full dependency list even for entries you previously excluded.

### Step 2: Read dependencies and curate to the tail
Read the manifest(s) and their lockfiles to get **declared deps + the resolved (pinned) version**:

| Ecosystem | Manifest | Lockfile (pinned version source) |
|---|---|---|
| Node | `package.json` | `pnpm-lock.yaml` / `package-lock.json` / `yarn.lock` |
| Dart/Flutter | `pubspec.yaml` | `pubspec.lock` |
| Go | `go.mod` | `go.sum` / `go.mod` |
| Rust | `Cargo.toml` | `Cargo.lock` |
| Python | `pyproject.toml` / `requirements.txt` | `uv.lock` / `poetry.lock` / pinned `==` |
| Ruby | `Gemfile` | `Gemfile.lock` |

**Curate — this is the point of the skill.** Include a library only if it earns its tokens:
- **Include:** fast-moving libs with API-changing releases in roughly the last 6–12 months; niche / lower-popularity libs under-represented in training; anything whose *version-specific* behavior matters here; libs the user names explicitly.
- **Exclude:** ubiquitous, stable stalwarts the model already uses correctly — e.g. `react`, `express`, `lodash`, `axios`, `pg`, `dayjs`, `zod`, standard test/lint tooling. Documenting these is always-on noise.
- When unsure, lean **include for niche, exclude for popular+stable**. Announce the split so the user can override: `Documenting 7 of 41 deps (skipped popular/stable). Add one back with: library-docs --force-all` or by naming it.

### Step 3: Resolve canonical URLs (pinned to the resolved version)
For each kept library, find the **official** docs URL and the changelog/releases URL — prefer
first-party sources (project site, the repo's `CHANGELOG.md` or GitHub Releases), and prefer
a **version-specific** docs URL when the docs are versioned. Use the project's normal
doc-fetching path (web search + read the page; GitHub for changelogs). Do not invent URLs —
open the page and confirm it resolves before recording it.

### Step 4: Distill the conventions (the money content)
Read enough of the docs for the **pinned version** to write **3–6 bullets** per library covering
the correct-usage rules most likely to be gotten wrong:
- API contracts that changed across versions (renamed/removed/relocated APIs, new required config).
- Setup/config order, required initialization, mandatory options.
- Documented footguns, deprecations, "don't do X — do Y" guidance.
- Prefer **version-specific and non-obvious** rules over generic advice. Cite the doc section when it helps.

Keep bullets short and imperative. If a library's docs yield nothing beyond what the model
obviously knows, record just the links and a single note — don't pad.

### Step 5: Write the reference
Write `.claude/skills/library-use/SKILL.md` from `assets/library-use.template.md`:
- Fill `{LIB_LIST}` in the description with the documented library names (drives auto-trigger).
- Fill `{REPO_NAME}`, `{DATE}` (from `git log -1 --format=%cd --date=short`, since wall-clock isn't available), `{MANIFESTS}`.
- One `## <library> \`<version>\`` block each, with Docs, Changelog, and Conventions.
- Add the `.agents/skills/library-use` symlink pointing at the Claude copy if the repo uses the `.agents/skills` convention (match sibling skills), so other agents pick it up.
- Optional: add a one-line pointer to the repo's `CLAUDE.md` if none exists — `Library docs & conventions: see .claude/skills/library-use` — but only with the user's ok, and only one line.

Report what you documented (a table of lib → version → #conventions) and stop.

### Step 6: Refresh mode (re-run) — version-aware
For each existing entry, compare the **recorded version** to the **current lockfile version**, and
handle new/removed deps:

1. **Unchanged version** → re-verify the URLs still resolve; refresh conventions only if the docs changed materially. Preserve hand-added convention bullets.
2. **Newer version, same API** (no breaking changes in the changelog between the two versions) → **update silently**: bump the version tag, refresh links + conventions. Note it in the summary.
3. **Newer version, API changed** (breaking changes — major bump, `BREAKING`, removed/renamed/relocated APIs in the changelog) → **do NOT silently rewrite**. Instead:
   - Report the delta: `<lib> <old>→<new>` with the specific API changes (from the changelog).
   - **Grep the repo for the affected APIs** and list the files/lines that use them.
   - **Draft the migration** (the concrete edits) and **ask before applying**. Only update the code and the entry's conventions once the user approves. If they decline, record the pending upgrade as a note in the entry and leave code untouched.
4. **New dependency** (passes Step 2 curation) → add an entry. **Removed dependency** → drop its entry.

To decide "same API vs API changed", read the changelog/releases **between** the two versions;
semver-major is a strong signal but confirm against the changelog (minors sometimes break; majors
sometimes don't touch what this repo uses).

End refresh with a summary: `{n} unchanged, {n} auto-updated (same API), {n} need migration (asked), {n} added, {n} removed`.

## Examples

### Example 1: First run in a Flutter app
User: `library-docs`
Actions:
1. Read `pubspec.yaml` + `pubspec.lock`. 41 deps; curate to 7 (keep `maplibre-react-native`, `better_auth`, niche plugins; skip `http`, `provider`, etc.).
2. Resolve official docs + changelog for each, pinned to the locked version.
3. Distill 3–6 conventions per lib from the pinned-version docs.
4. Write `.claude/skills/library-use/SKILL.md` + `.agents/skills/library-use` symlink.
Result: "Documented 7 of 41 deps. `maplibre-react-native 10.0.0` (4 conventions), … Skipped 34 popular/stable. Re-run `library-docs` after upgrades to refresh."

### Example 2: Re-run after a dependency bump
User: `library-docs --refresh`
Actions:
1. `drizzle-orm 0.36→0.38`: changelog shows no API change to what the repo uses → auto-update version + conventions.
2. `better-auth 1.2→2.0`: major, changelog lists renamed `emailAndPassword` config → report the delta, grep finds 3 files using it, draft the migration, ask before applying.
Result: "5 unchanged, 1 auto-updated (drizzle-orm), 1 needs migration (better-auth 1.2→2.0 — 3 files) — proposed changes below, approve to apply."

## Troubleshooting

### Docs URL can't be found or won't resolve
**Cause:** Library has no official hosted docs (common for small packages).
**Solution:** Fall back to the repo's `README`/`CHANGELOG.md` on GitHub as both docs and changelog. If there's genuinely nothing, record the repo URL and one note; don't fabricate a docs site.

### Can't tell if a version bump broke the API
**Cause:** Changelog is thin or missing.
**Solution:** Compare the two release tags' notes/diffs on GitHub; check for major-version bump and any removed/renamed exports. If still unclear, treat it as **API changed** (the safe side — report + ask rather than silently rewrite).

### The reference is getting large / too many libraries
**Cause:** Curation was too permissive.
**Solution:** Re-run and tighten Step 2 — drop popular/stable libs back out. The reference should be the tail, not the whole `package.json`.

### Name collision with this skill
**Cause:** The repo artifact must not be named `library-docs` (this skill's name) or both load at once.
**Solution:** The artifact is always `library-use`. Never write a repo-local skill named `library-docs`.

## Notes
- Pair: `library-docs` (this, generates) → `library-use` (per-repo reference) → `review-library-use` (audits code against it, auto-invoked by `code-review`).
- Wall-clock time isn't available in this environment — take dates from `git` (`git log -1 --date=short`), not from a live clock.
- Keep the reference committed; it's version-controlled project context that travels with the code.
