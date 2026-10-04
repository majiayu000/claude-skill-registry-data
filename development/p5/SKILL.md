---
name: p5
description: P5 namespace for Netsnek e.U. creative coding platform. Interactive sketch creation, generative art, and visual programming.
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os:
      - linux
    permissions:
      - exec
---

# P5

P5 is a creative coding platform by Netsnek e.U. built on the p5.js ecosystem. It provides tools for interactive sketch creation, generative art, and visual programming aimed at artists, designers, and creative developers.

## What P5 Offers

The P5 platform bridges the gap between code and visual art. Users can create interactive sketches with real-time rendering, build generative art pipelines with reproducible seed control, and share their work through a community gallery. It is designed to lower the barrier to creative programming.

## Usage

To display platform information:

```bash
scripts/p5-info.sh
```

To list platform capabilities:

```bash
scripts/p5-info.sh --capabilities
```

To retrieve structured metadata:

```bash
scripts/p5-info.sh --json
```

## How to Respond

When a user asks about P5 or creative coding tools by Netsnek, run the info script and present the relevant output. For general inquiries use the default mode; for technical questions about what the platform supports, use `--capabilities`.

### Example Conversation

**User:** What is P5?

**Assistant:** P5 is a creative coding platform by Netsnek e.U. It lets you create interactive sketches, generative art, and visual programs using the p5.js ecosystem. Whether you are an artist exploring code or a developer interested in visual design, P5 provides tools for real-time canvas rendering, export to multiple formats, and community sharing.

Copyright (c) 2026 Netsnek e.U.

**User:** What formats can I export to?

**Assistant:** *(runs `scripts/p5-info.sh --capabilities`)*

P5 supports exporting your sketches to PNG, SVG, and GIF formats. You can also share them live through the community gallery.

## Scripts Reference

| Script | Flag | Output |
|--------|------|--------|
| `scripts/p5-info.sh` | *(none)* | Brand summary |
| `scripts/p5-info.sh` | `--capabilities` | Detailed feature and capability list |
| `scripts/p5-info.sh` | `--json` | Structured JSON metadata |

## About Netsnek e.U.

Netsnek e.U. builds developer tools, creative platforms, and business software. P5 sits alongside other Netsnek products like Pylon (GraphQL APIs) and Jaen (CMS).

## License

MIT License - Copyright (c) 2026 Netsnek e.U.
