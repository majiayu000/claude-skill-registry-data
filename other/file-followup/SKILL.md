---
name: file-followup
description: Spawn the architect briefly to file a new package spec for an out-of-scope finding. pkg82/pkg83/pkg84 are the templates.
invocation: /file-followup <one-line reason>
---

# /file-followup \<one-line reason\>

Spawn the `architect` agent in a brief goal-capture pass to file a new
package spec for an out-of-scope finding surfaced during another session.

## Input

Pass the architect:
- The one-line reason (from the invocation)
- The source context: which package discovered it, which PR, what the
  finding was
- The constraint: this is a follow-up spec, not a strategy discussion.
  The architect should skip the dialogue phase and go directly to writing
  the spec, unless the scope is genuinely unclear.

## Output

The architect should produce:
- A new spec file at `.astroray_plan/packages/<pkgNN>-<slug>.md`, passing
  `python scripts/project_index.py lint` against `TEMPLATE.md`
- Auto-tagged with `Track:`
- A one-PR doc update (spec file only; STATUS.md gets updated at round close)

## Templates

- pkg82: filed after pkg78 bisect refused on §1 grounds (measurement carries)
- pkg83: filed from pkg81 H2 finding (accumulator-reset-per-pan)
- pkg84: filed from pkg81 H5 finding (cold CUDA context 12 s first frame)

The pattern: a finding from one package becomes a new spec for the next
available package number, scoped tightly to the finding.
