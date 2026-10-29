---
name: authoring-prime
description: |
  Orient before writing or reviewing a docs page (content/) or a blog draft
  (blogs/): where a page goes, the Markdown constructs the renderer supports,
  the NEVER/ALWAYS rules that break pages or releases, title strategy, and an
  on-demand catalog of exemplar pages per content type. Load it before
  drafting, planning placement, or reviewing style; skip it for git, build, or
  single-fact questions.
---

# authoring-prime: orientation for docs and blog authoring

Read this once at the start of an authoring or review task. It points at the
sources of truth instead of restating them. Open those only for the step that
needs them.

## Where things live

| Kind | Home | Contract | Criteria |
|---|---|---|---|
| Docs page | `content/<project>/<bucket>/<NNN-slug>.md`, or `<NNN-slug>/index.md` beside `snippets/` when it has runnable code | [`content/README.md`](../../../content/README.md) | [`docs/design/docs-quality.md`](../../../docs/design/docs-quality.md) |
| Blog draft | `blogs/<slug>/index.md` (+ `snippets/`, `assets/`) | [`blogs/CONVENTIONS.md`](../../../blogs/CONVENTIONS.md) | [`blogs/QUALITY.md`](../../../blogs/QUALITY.md) |

- **Projects:** `unitycatalog`, `delta`, `open-lakehouse` (`content/vocab.json`).
- **Buckets:** `tutorials` (one happy path, learn by doing), `how-to` (one
  task, reader knows their tools, multi-interface tabs), `explanation`
  (understanding, engine-neutral, no steps), `reference` (complete,
  scannable, e.g. R01 features and limitations).
- **Navigation:** `content/<project>/nav.yml` arranges pages. Every page needs
  an entry, and orphans fail the build. A `planned: <id>` slot is a page
  reviewers asked for. Filling it means writing the page and replacing the
  slot with `page: <bucket>/<slug>` and the same `id:`.
- **Facts about the lakehouse** live in the LikeC4 model (`architecture/`).
  Query it with `uv run docsnip query …` (skill `docs-query`). Don't paraphrase
  the model from memory.
- **Release pins** live in `content/<project>/release.yml`. **Environments**
  are generated (`envs/<name>/`) and registered in `envs/environments.yml`.
- **Status** is the release (ADR-0002): `idea`, `draft`, `ready`, `private`.

## Renderer constructs (the cheat sheet)

Source stays builder-agnostic Markdown. These constructs degrade to plain
Markdown on GitHub and are upgraded by the preview, the emitter, and the docs
sites.

| Construct | Use | Notes |
|---|---|---|
| ` ```python file=./snippets/x.py start=start:r end=end:r ` | every displayed code block | Regions are `# --8<-- [start:r]` / `[end:r]`. SQL uses `-- --8<--` and Scala/Java/Rust use `// --8<--`. `file=` alone inlines a whole file (blogs). Add `collapse` for copy-only boilerplate and `title="x.py"` for a filename header. |
| `:::tab[Label]` … `:::` | one tab per interface | Adjacent tabs form one label-synced group. Use `::::tab` when a tab wraps a `:::` directive. |
| `:::prerequisites` … `:::` | how-to and tutorial opener | Holds tools to install (linked) and the state the page assumes, a line each. Never Docker, the server, ports, or pins (`content/README.md`). |
| `:::environment` … `:::` | a page whose task *is* starting a stack | Must be a container: an empty pair, or keyed `:::environment{key="uc-aws/compose.yaml"}`. |
| `:::deployment{key="uc-hybrid/compose.yaml"}` … `:::` | walking through a generated stack's whole deployment | Renders the download, then Trestle's steps (provision, configure, start) as a numbered list. The key must be a generated environment. |
| `::::journey` … `::::` | tutorial or blog walkthrough | `###` headings inside become timeline steps. A tutorial's first step (start the environment) is added by the emitter. |
| `:::note`, `:::tip`, `:::info`, `:::warning`, `:::danger`, `:::caution` | callouts | Use `:::warning` for surprising replacement or data loss and `:::danger` for irreversible cascades. Tutorial side information goes in `:::note`/`:::tip`. |
| `:::tldr` … `:::` | blogs only | 3–5 fact-rich bullets near the top. |
| `[label](model:<element-id>)` | inline concept link | Validated against `architecture/dist/model.json`. It renders as a link only for `#public` elements. |
| ```` ```likec4 <viewId> ```` + alt text body | a model diagram | The view lives in `architecture/model/views/*.likec4` (blogs use `blog-views.likec4`, docs use `docs-views.likec4`); a sequence is a `dynamic view` with `variant sequence`. Sites draw the interactive view; the `.md` twin gets its Mermaid. No PNG. The alt text says what the flow shows. |
| ```` ```trestle <name> ```` + alt text body | an environment's topology | `<name>` is a generated environment; its snapshot is generated (`docsnip envs --fix`, `just env-render`). For a stack no environment runs, use `trestle ./assets/<stem>.trestle-graph.json` (exported from Trestle's editor). Sites draw the interactive canvas; the `.md` twin gets Trestle's Mermaid. The alt text says what talks to what. |
| `<!-- compat:<table> -->` … `<!-- /compat:<table> -->` | compatibility tables | Generated by `uv run docsnip compat --fix`. Never edit inside. |

## NEVER / ALWAYS

**Never:**

- Inline code in a page, or show a command no script runs. Code comes from a
  tested region. The one exception is the pinned command that opens a session
  (`uv run --with <pkg>==<pin> python -m asyncio`), which `docsnip versions`
  checks.
- Edit generated files: `content/<project>/compatibility.json`, the
  `compat:` blocks, anything under `envs/<name>/` except `env.toml` (regenerate
  with `just env-render <name>`), `envs/environments.generated.json`,
  `architecture/dist/**`, `sites/**`, `site/src/generated/**`.
- Set `status: ready` without an approval in the review app, or on a
  `private` page.
- Name the release in prose ("In 0.7.0 the server…") or write "currently" or
  "not yet". Absences and quirks are recorded in R01, which is private: never
  link it from a page that isn't.
- Put seeding, `main()`, or asserts inside a region. Only the `seed_dataset(...)`
  line may sit inside, for pages that read pre-existing data.
- Invent a flag, default, limit, error string, or console step. Leave an open
  question instead.
- Copy Databricks-only concepts (workspaces, Catalog Explorer, `/Volumes`)
  into task text. Mention them only to mark a boundary.

**Always:**

- Give a page frontmatter: `title`, `diataxis`, `project`, and usually
  `summary`. An explanation adds `explains: <element>`. Pages that discuss
  other concepts add `references: [...]` or inline `model:` links.
- Give a runnable script a PEP 723 block, `[tool.docs-factory]` (compose,
  services, claims), and inline asserts in `__main__`. Running it is its test.
- Run `uv run docsnip check` (includes `docsnip prose`),
  `uv run ruff format --check .`, and `node site/scripts/check-nav.mjs` before
  handing off.
- Use sentence-case headings, H2 for tasks or main ideas, H3 for detail, and
  no H4 outside reference pages.

## Titles

- **H1/`title`:** at most 60 characters, specific enough to stand alone in a
  search result. How-tos are "Manage X", not "Create and manage X". Tutorials
  name the outcome ("Create your first catalog"). Explanations name the
  concept.
- **Nav label:** `label:` in `nav.yml` when the title is too long for the
  sidebar. Keep the page title complete.
- **`summary`:** at most 160 characters, an answer rather than a description of
  the page. Never "Learn how to…" or "This page…".

## Exemplars

[`references/exemplars.md`](references/exemplars.md) lists the pages to imitate,
grouped by type. Read it **only when drafting or reviewing**, find the type you
are writing, and read only that type's pages. Other types' pages add context
without helping. There is no separate exemplar skill or command: the reference
file is the catalog.
