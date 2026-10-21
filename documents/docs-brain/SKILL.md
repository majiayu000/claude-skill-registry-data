---
name: docs-brain
description: Use when you need the official documentation of a stack tool at the installed version (WordPress, ACF, Acorn, Laravel, Livewire, Lando, Vite) - "what does the manual say", "check the docs for our version", .docs-brain.json, the corpus, INDEX.md, docs-brain resolve or search. Defines the lookup order. For choosing a skill use roots-router.
---

# Docs brain: look it up before you guess

A docs corpus is a folder of markdown pages (official documentation converted once, pinned to the versions the project has installed). This skill says where to look, in which order, and how to search it without flooding the context.

## When to use

- A behaviour of WordPress, ACF, Acorn, Laravel, Livewire, Lando, Vite, PHPStan, PHPUnit or similar is in question and you are not certain of it.
- Before writing custom code for something that might be native.
- The user mentions the corpus, `.docs-brain.json`, or asks which version of a tool the docs describe.

## Inputs required

- The project root (where `.docs-brain.json` lives, if any) and the lock files it names.
- The tool and version in question: take it from the session context, or run `docs-brain resolve`.

## Procedure

### 1. Lookup order (stop at the first level that answers)

1. **The project's own rules**: `AGENTS.md`, `.ai/`, `.claude/rules/`. They win over any general documentation.
2. **The local source of the installed version**: for behaviour questions the code is the truth. WordPress core (the core dir, `wp-includes/`, `wp-admin/`), ACF `includes/`, the app's `vendor/` (Acorn, ACF Composer, Livewire). Native first: find the WordPress / ACF / Acorn mechanism here before proposing custom code, and cite the file and line.
3. **The corpus**, at the version the lock files pin (see step 3).
4. **The web**, last, and only for what the corpus lacks. Say that you went to the web and which page.

### 2. Read `.docs-brain.json`

```json
{ "roots": ["~/hekivo/kivo-wisdom/corpus"], "locks": ["composer.lock", "package.json"] }
```

- `roots`: corpus folders in **precedence order**; a page found in an earlier root hides the same page in a later one. Expand `~` yourself when you pass a path to a tool; a relative root is relative to the folder that holds `.docs-brain.json`.
- `locks`: the lock files used to pick versions. They are read, never the constraints in `composer.json`.
- No file, or a root that does not exist: say so and fall back to level 2 and 4. Do not invent a path.

### 3. Check the version against the lock

- `docs-brain resolve` prints the table package → installed version → corpus folder. Run it first when the question is version-sensitive.
- `docs-brain status` (or `status --check`) reports project drift (the lock moved past the corpus) and upstream drift (pages changed). If the corpus folder for a tool is older than the installed major, tell the user before relying on it.
- If the CLI is not installed, read the folder name: pages live in `<root>/<source>/<version>/`, so `laravel/13.x/` documents Laravel 13.

### 4. Search with `rg`, narrow to wide

Corpus layout: `<root>/<source>/<version>/*.md` (frontmatter: `title`, `source`, `version`, `url`, `upstream_modified`, `fetched_at`, `license`, `redistribute`), `<source>/<version>/SUMMARY.md` (ordered table of contents), and `<root>/INDEX.md` (one line per page: path, title, source, version, url, updated).

```
rg -n -i "<topic>" <root>/INDEX.md                          # titles first, cheap
rg -n "^## " <root>/<source>/<version>/SUMMARY.md           # browse a source
rg -l "<exact symbol>" <root>/<source>/<version>            # which pages mention a hook, class or method
rg -n -C3 "<exact symbol>" <root>/<source>/<version>/<page>.md   # then read around the hit
rg -l "^title: .*<word>" <root>                             # match on page titles
```

Then read the one page you need. Do not print whole directories, and cap broad hits (`| head -40`). Search for exact identifiers (a hook name, a class, a CLI flag) before prose.

### 5. What `redistribute: false` means

A page whose frontmatter says `redistribute: false` (and every source that `LICENSES.md` marks "no") is licensed or unlicensed material kept for **consultation only**.

- Use it to answer and to verify facts.
- Never quote it, paraphrase it closely, or copy its examples into anything that leaves the private repository: public plugins, skills, README files, MR text on a public repository, issues, blog posts.
- In a public artefact cite the official URL from the `url` field instead, and write the explanation in your own words from the local source.
- Do not run `export-llms` on a root and publish the output; it skips these pages by design, so a manual copy defeats the guard.

### Profile differences

| Topic | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
| --- | --- | --- | --- |
| Local source to read first | theme `vendor/` for Acorn; the core dir for WordPress | plugin `vendor/`; ACF plugin `includes/` | root `vendor/`; no ACF unless installed |
| Lock files to list | theme `composer.lock`, theme `package.json` | plugin `composer.lock`, root `composer.lock` | root `composer.lock`, build-service `package.json` |
| Corpus sources usually needed | roots, acf, wordpress, laravel, vite | roots, acf, wordpress, laravel, livewire, lando | roots, wordpress, laravel, lando, vite |

## Verification

- Every answer built from the corpus names the page path and the version folder.
- The answer shows the search trail: the `rg` command run on `INDEX.md` or `SUMMARY.md` and the hit that led to the page, before any page was read in full.
- The version folder matches `docs-brain resolve` (or the lock) for that tool, or the mismatch is stated.
- No sentence of a `redistribute: false` page appears in an artefact meant to be public.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `rg` returns nothing | Tool not in the corpus, wrong root, or `~` not expanded | Check `INDEX.md` for the source; expand the path; otherwise go to the web and say so |
| Docs describe a method the code lacks | Corpus version older or newer than the lock | Run `docs-brain status`; trust the vendor source |
| Hundreds of hits flood the context | Search term too broad | Search `INDEX.md` titles first, then one page; use `-l` before `-n` |
| Two roots give different answers | Precedence | The earlier root in `roots` wins; report the conflict |
| Project rule contradicts the manual | Project is stricter or legacy | Follow `AGENTS.md` / `.ai/`; mention the difference |

## Escalation

- A fact that matters and is missing from every level: say it is unverified, give the best-supported answer, and ask whether to add the source to the corpus.
- A `docs-brain` command that errors (lock unreadable, root missing): report the exact message; do not work around it by guessing versions.
- Any request to publish licensed pages: refuse and point to the official URL.

<!-- verified: ~/hekivo/kivo-wisdom/README.md — corpus layout, frontmatter fields, INDEX/SUMMARY, lookup order, .docs-brain.json roots/locks, redistribute:false skipped by export-llms; ~/hekivo/kivo-wisdom/LICENSES.md — which sources are consultation-only; design 4.5 and report 04 5.1-5.3 — resolve reads locks, status reports project and upstream drift, precedence of roots. Not verified: the docs-brain CLI itself (built in Phase 4), so command output formats are described, not tested -->
