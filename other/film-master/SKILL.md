---
name: film-master
description: Render and verify the complete finished movie from the executable picture timeline, synchronized audio master, subtitles, and delivery specification.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Film Master

## Workflow

1. Read `../../references/FILM_MASTERING.md`, executable timeline, audio mix/master, media approvals, production coverage, and delivery spec.
2. Stop on unresolved production-coverage blockers or selected hard QC failures.
3. If the audio master does not exist but its valid mix manifest does, run `audio-master` first.
4. Run `scripts/film_master.py PROJECT` for the actual master.
5. Run `delivery-qc` on the output.
6. Register the verified film master with `asset-approval`.
7. Mark the film-master artifact approved only after rendering and QC succeed.

## Done

An actual finished film file exists at the declared project-relative path, has synchronized audio, and passes blocking delivery checks.
