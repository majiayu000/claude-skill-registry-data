---
name: regenerate-diagrams
description: Re-render the architecture diagrams — regenerate Mermaid SVGs from the .mmd sources in docs/diagrams/src, or find the editable Lucid originals.
---
# Regenerate diagrams

Every architecture diagram exists twice: an editable Lucidchart original (the
design surface) and a Mermaid twin committed at `docs/diagrams/src/<f>.mmd`,
rendered to `docs/diagrams/<f>.svg` — the SVGs are what READMEs and docs embed.
After editing a `.mmd`, re-render its SVG and commit both.

## Read first
- docs/diagrams/README.md — the diagram index, the links to the editable Lucid originals, and the conventions both twins follow.
- The `.mmd` source you are changing, in docs/diagrams/src/.

## Commands
```bash
# one diagram
npx -y @mermaid-js/mermaid-cli -i docs/diagrams/src/<f>.mmd -o docs/diagrams/<f>.svg \
  --iconPacks @iconify-json/logos

# all of them
for f in docs/diagrams/src/*.mmd; do
  npx -y @mermaid-js/mermaid-cli -i "$f" -o "docs/diagrams/$(basename "${f%.mmd}").svg" \
    --iconPacks @iconify-json/logos
done
```

## Gotchas
- Keep `--iconPacks @iconify-json/logos` — the sources use logo icons and drop them silently (or fail) without it.
- The output SVG basename must match the source basename: docs across the repo embed `docs/diagrams/<f>.svg` by exact path.
- The Lucid documents are the editable originals; a change made only in Lucid must be mirrored into the `.mmd` twin (and vice versa) or the two drift.
- mermaid-cli renders via headless Chromium (the first run downloads it). No CI job re-renders diagrams — you render locally and commit the SVG.
- Never hand-edit the generated SVGs; they are build artifacts of the `.mmd` files.
