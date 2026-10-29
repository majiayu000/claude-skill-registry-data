---
name: llms-txt-from-website
description: Generate `llms.txt` and `llms-full.txt` for a docs/product website from just a URL. Detect and reuse an existing `/llms.txt`, discover the docs source repo via “Edit this page”/GitHub links, fall back to `sitemap.xml` or an internal crawl when needed, and optionally use Context7 when the target is a known library.
disable-model-invocation: true
---

# llms.txt from Website

Use this skill when a user provides a website URL and wants a curated `llms.txt` plus a fuller `llms-full.txt`. It works without knowing the site framework or having a sitemap. The generator tries existing files first, then the docs repository, then a sitemap or bounded internal crawl.

## Generate the files

Run the bundled script with the docs or product URL and an output directory:

```bash
python "<path-to-skill>/scripts/generate_llms_files.py" \
  --url "https://docs.example.com/" \
  --out "./llms-out"
```

The script creates a URL-derived subdirectory containing:

- `llms.txt`: the curated manifest.
- `llms-full.txt`: the available full-text bundle.
- `metadata.json`: the source and generation details.

Add `--json` to print the metadata to stdout for debugging or chaining:

```bash
python "<path-to-skill>/scripts/generate_llms_files.py" \
  --url "<url>" --out "./llms-out" --json
```

## How the generator chooses sources

The script follows this order; use the first successful source and keep the generated metadata with the outputs.

1. **Existing files.** It looks for `llms.txt` at the supplied URL's root and the site origin, including an exact docs subpath. If it finds `llms-full.txt`, it downloads that too. Otherwise, it builds the full file from links in `llms.txt`, preferring Markdown endpoints and using `uvx markitdown` for pages it converts.
2. **Docs repository.** If no existing `llms.txt` is found, inspect the homepage for “Edit this page”, “View source”, GitHub, repository, or similar links. The generator discovers a linked GitHub repository, shallow-clones it, and looks for docs sources (`.md`, `.mdx`, `.rst`). For large repositories, `repomix` packs the selected sources. If discovery is unclear but a public docs repository likely exists, search the web for `<project> docs github`, then rerun with the relevant docs URL.
3. **Sitemap or crawl.** When repository discovery does not produce usable docs, the generator checks `robots.txt` for sitemap hints and tries `/sitemap.xml`. If it finds no usable sitemap, it crawls internal links from the supplied URL within the configured page and depth limits.

The repository path produces links to the live site when those pages resolve, and otherwise uses GitHub source links. By default, provenance stays in `metadata.json`; pass `--include-source-links` to include absolute source URLs beside manifest links.

## Shape the outputs

`llms.txt` should help a reader choose relevant documentation quickly:

- Start with `# <Project/Docs name>` and a one-sentence `> summary`.
- Add a few lines of useful context without introducing headings.
- Group absolute links under `##` sections, with each link as `- [Name](URL)`.
- Put non-essential links under `## Optional`.
- Keep local paths and provenance out of the manifest unless source links are requested.

`llms-full.txt` should include the documentation text available from the chosen source. Repository sources are packed from Markdown where possible; website pages are converted to Markdown and concatenated with clear separators.

## Use Context7 for library documentation

For a known library or framework, use Context7 when its MCP tools are available to fill gaps or cross-check the generated material:

1. Call `resolve-library-id` with `libraryName` and `query`.
2. Call `query-docs` with the returned `libraryId` and a focused `query`.
3. Compare the result with the repository or crawl output and use it to identify missing references.

## Script options

- `--max-pages`: maximum pages to process during sitemap or crawl work; default `60`.
- `--max-depth`: maximum internal-crawl depth; default `3`.
- `--max-links`: maximum links in `llms.txt`; default `30`.
- `--full-scope all|selected`: include all repository docs sources or only the curated subset; default `all`.
- `--max-full-bytes`: repository full-text size limit before falling back to `selected`; default `12 MB`.
- `--force-full`: ignore `--max-full-bytes` and use the requested `--full-scope`.
- `--no-crawl`: stop if existing `llms.txt` and repository discovery both fail, instead of trying a sitemap or crawl.
- `--include-source-links`: include absolute source URLs beside links in `llms.txt`.
- `--json`: print generation metadata to stdout.
