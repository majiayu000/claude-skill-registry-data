---
name: docs-to-skill
description: Turn a product or project documentation website into a skill backed by local references. Use when the user wants to download docs, mirror llms.txt or sitemap pages, generate a documentation skill, refresh an existing docs skill, or create a lean SKILL.md that indexes official documentation.
---

# docs to skill

Create or refresh a documentation skill whose `SKILL.md` is only an index to downloaded pages under `references/`.

## Inputs

Collect:

- source site, `llms.txt`, or `sitemap.xml` URL;
- generated skill name;
- concise triggering description;
- target directory, defaulting to `~/.fx/skills/<name>`.

## Build

Load the installed agent-browser workflow before downloading:

```bash
agent-browser skills get core --full
```

Run:

```bash
python3 scripts/build_docs_skill.py \
  --source <url> \
  --name <skill-name> \
  --description '<triggering description>' \
  --target ~/.fx/skills/<skill-name>
```

The generator:

1. uses an explicit `llms.txt` or `sitemap.xml`, or tries `<site>/llms.txt` then `<site>/sitemap.xml`;
2. downloads every discovered page with `agent-browser read`;
3. mirrors pages under `references/`;
4. writes `references/source-index.txt` and `references/manifest.json`;
5. generates a compact `SKILL.md` grouped by documentation path;
6. on refresh, replaces only files tracked by the previous manifest and preserves unrelated files.

## Verify

Run:

```bash
python3 scripts/build_docs_skill.py \
  --source <url> \
  --name <skill-name> \
  --description '<triggering description>' \
  --target ~/.fx/skills/<skill-name> \
  --check
```

Report the target path, discovery source, downloaded page count, and validation result.
