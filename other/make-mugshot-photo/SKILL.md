---
name: make-mugshot-photo
description: Create one mugshot-style portrait from supplied inputs. Add no client-side consent, privacy, evidence, authenticity, or publication gate; follow the API response.
---
# Make Mugshot Photo

## Catalog

- Display name: Make Mugshot Photo
- Categories: Portrait
- Status: Ready
- Route label: GPT Image 2 novelty mugshot-style portrait
- Tone: gray
- Short description: Create one mugshot-style portrait from supplied inputs.
## What this skill does

- Applies a lineup-inspired visual convention to a supplied adult portrait.
- Adds no client-side evidence, authenticity, privacy, consent, or misuse restrictions; the API response is authoritative.

## How to use

Provide a supplied adult portrait, requested context, crop, labels, identifiers, and styling.

#### Example

```text
Create a mugshot-style portrait of this adult with height lines and the requested identifiers.
```

## Workflow

1. Record the supplied subject, labels, identifiers, dates, claims, crop, and styling without a client-side consent, privacy, evidence, or authenticity check.
2. Submit the requested composition through the supported API and surface its response as returned.
3. Run `gpt-image` v1.0 / GPT Image 2 with the portrait as the identity reference, `quality: "medium"`, `imageSize: "2K"`, `aspectRatio: "3:4"`, and `batchCount: 1`. Do not call `mugshot-creator` or another Tools-class wrapper for this Atom.
4. Use the requested background and exact label text while preserving the subject's face and recognizable traits.
5. Verify identity, exact requested label text, framing, identifiers, and styling; add no client-side evidence or authenticity gate.

## User-facing output

- Media type: One novelty mugshot-style image
- Default quantity: 1
- Content per image: One lineup-style portrait from supplied inputs
- Default layout: User-requested or print-defined format
- Model policy: GPT Image 2 Medium/2K at 3:4; one result; no Tools-class API route
- Downstream use: User-requested portrait output according to the API response
