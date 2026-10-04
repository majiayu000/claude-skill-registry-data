---
name: github-repo-i18n
description: Internationalize the user-facing language layer of a GitHub repository, including its repository description, repository topics, README files, release notes, changelogs, and other explicitly selected documentation, with English as the default and any user-requested locales as mirrors. Use when a user asks to translate, localize, add language mirrors, or check cross-locale parity for a GitHub repository. Confirm the exact document and metadata scope when it is not explicit, identify existing locales, preserve facts, code, commands, links, images, and structure, and provide local Markdown plus GitHub-style previews. Do not use for product UI or runtime i18n, database content, visual README redesign or assets, public-release suitability or security scans, Issue or PR label taxonomies, Git tags, or Git, PR, release, deployment, or production operations.
---

# GitHub Repository Internationalization

Synchronize the selected language layer of a GitHub repository while keeping every locale faithful to the same project facts. Treat repository description and repository topics as separate metadata surfaces, and treat each documentation locale as a complete mirror rather than a shortened translation.

## Scope gate

Before editing, identify the exact documentation categories, files, metadata surfaces, and target locales.

If the request does not name the documentation scope, ask:

> Which parts should be internationalized: repository description, repository topics, README files, release notes, CHANGELOG, docs pages, documentation indexes, templates, or specific files? Which locales should be added or updated? Everything else will remain unchanged.

Treat repository description and repository topics as independent choices. Do not infer that a request for a README includes GitHub metadata, or that a metadata request includes documentation.

A short read-only inventory is allowed before the scope answer when it helps present the choices. Do not write, rename, delete, or remotely update anything until the scope is explicit. Preserve unrelated working-tree changes and never switch or overwrite another worktree.

## Workflow

### 1. Inventory the selected repository

Read the applicable repository instructions, then inspect only enough of the repository to establish the confirmed scope:

- Check the current worktree, branch, other worktrees, and uncommitted changes.
- Locate README files, documentation files, release notes, changelogs, indexes, templates, and the version facts they reference.
- Identify existing locale filenames and infer the language of each selected document from its filename and content.
- Record links, images, code blocks, commands, product names, contact links, feature claims, limitations, and license references that must remain aligned.
- Record the selected GitHub description and topics separately when metadata is in scope.

Produce a compact scope matrix before editing:

| Surface | Existing path or value | Locale | Action | User-confirmed |
| --- | --- | --- | --- | --- |
| README | README.md | English or detected locale | preserve, translate, or create | yes/no |
| Documentation | selected path | detected locale | preserve, translate, or create | yes/no |
| Metadata | description or topics | repository-level | draft or update | yes/no |

If README.md is non-English, preserve its content as README.<locale>.md using the detected locale before generating the English default entry. Do not silently discard, rename over, or reduce the original.

### 2. Establish the locale matrix

Read [locale-strategy.md](references/locale-strategy.md) when adding a locale, renaming a localized document, or handling a non-English README.md.

Use English as the default README.md entry. Support any locale explicitly requested by the user; do not hard-code Chinese or assume that a second locale is required. Reuse existing repository naming conventions where they are clear. Use standard locale tags such as en, ja, zh-CN, fr, or ar when a new filename is needed.

For each selected document, map one default-language path to the requested locale mirrors. Add or update language-switch links only for the confirmed set of locales. Check every link from every selected locale when the user requests a language switch.

### 3. Handle repository description and topics

Read [github-repository-metadata.md](references/github-repository-metadata.md) when repository description or topics are in scope.

The GitHub description is one repository-level field, not a locale table. Keep English as the default value unless the user explicitly chooses another final value. Present translated alternatives rather than concatenating several languages into one description by default.

Topics are discovery identifiers, not prose translations. Keep a small, stable set of canonical English or language-neutral topics; preserve useful existing topics, remove duplicates only when requested, and do not mechanically add a translated copy of every topic. Treat Issue or PR labels and Git tags as different surfaces and leave them unchanged unless explicitly included.

A local draft or metadata snapshot is not evidence that GitHub changed. If the user explicitly authorizes a remote metadata write, show the exact final description and topic list first, then re-read the remote values after the write.

### 4. Build complete document mirrors

Read [document-parity.md](references/document-parity.md) when translating or comparing selected documents.

Use the existing document as the factual source, regardless of its current language. If the source is non-English, retain its facts while producing the English default and any requested mirrors. Translate prose naturally, but keep these aligned across locales:

- project identity, value proposition, features, limitations, and compatibility;
- headings and section responsibilities;
- installation commands, code blocks, paths, URLs, versions, product names, and image targets;
- screenshots, output references, contact links, license links, and documentation navigation.

Do not invent claims, benchmarks, features, testimonials, or translations of code identifiers. Do not make the target shorter by omitting necessary source content. If a locale needs a different explanation or image because of a real language-specific constraint, record the difference and ask before diverging.

The audit script checks objective structure and references. Semantic completeness and translation quality require manual review by the agent and user; never report a script pass as proof of translation quality.

### 5. Render previews and get user confirmation

Read [preview-and-github-rendering.md](references/preview-and-github-rendering.md) when a README or other GitHub-rendered Markdown file changes.

For every changed README locale, create both:

1. a preview in the available local Markdown editor or renderer; and
2. a browser preview using a GitHub-style GFM renderer.

Inspect the same content at a wide and narrow content width, including language-switch links, tables, code blocks, images, alt text, raw HTML, details blocks, and light/dark surroundings where the renderer supports them. For other changed Markdown files, preview the affected files and use the same narrow check when layout-sensitive content changes.

Show the user the rendered preview, the exact document diff, the locale matrix, and any metadata draft. Label local-editor rendering, GitHub-style rendering, and actual GitHub-page verification as separate evidence. Do not call a local preview an actual GitHub verification. If no adequate renderer is available, report the preview as unverified rather than silently treating source text as acceptance.

Wait for the user's approval of the preview before treating the content as final. If the user requests a change, update only the requested scope and render the affected locales again.

### 6. Run the deterministic audit

Use the bundled standard-library script from this Skill directory:

~~~bash
python3 scripts/audit_repo_i18n.py /path/to/repository \
  --document en=README.md \
  --document ja=README.ja.md \
  --require-locale-links
~~~

Add another document argument for each selected locale mirror. Pass a local JSON metadata snapshot with the metadata option when the user wants an offline check of a drafted description and topics:

~~~bash
python3 scripts/audit_repo_i18n.py /path/to/repository \
  --document en=README.md \
  --document ja=README.ja.md \
  --metadata /path/to/metadata.json \
  --format text
~~~

The script checks selected-file existence and boundaries, heading and code-fence structure, local link and image targets (comparing cross-locale content links by locale-neutral document family), optional locale-switch links, and the shape of a supplied metadata snapshot. It does not translate, call external URLs, inspect GitHub, scan for secrets or private material, judge public-release suitability, or modify files.

### 7. Report evidence and hand off

Report:

- confirmed scope and excluded scope;
- locale matrix and preserved non-English source content;
- documents and metadata changed or intentionally left untouched;
- parity audit command and result;
- local-editor preview and GitHub-style preview result for each affected README;
- actual GitHub-page verification, only if it genuinely occurred;
- semantic translation review still needed;
- remote metadata writes, Git operations, Release, deployment, and production checks that were not performed.

Keep local document changes separate from any authorized remote metadata operation. Do not commit, push, create a PR, create a Release, deploy, or modify production state as an implicit part of localization.

## Completion criteria

A localization task is complete only when:

- the user-confirmed files and metadata surfaces are the only intended scope;
- English is the default README entry and existing non-English README content was preserved when applicable;
- every requested locale has a complete mirror with matching facts, structure, links, images, code, and navigation;
- the user has seen and approved the affected previews;
- deterministic parity checks have passed, or every failure is reported;
- local preview and actual GitHub verification are not conflated;
- no unrequested GitHub or repository-release operation was performed.

## Invocation examples

~~~text
Use $github-repo-i18n to add Japanese and French README mirrors and keep README.md as the English default.
~~~

~~~text
Use $github-repo-i18n to internationalize the repository description and topics only; do not change documentation.
~~~

~~~text
Use $github-repo-i18n to audit parity between the selected README locales and show local and GitHub-style previews before I approve the result.
~~~
