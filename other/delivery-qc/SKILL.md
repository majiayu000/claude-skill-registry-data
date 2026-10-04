---
name: delivery-qc
description: Probe finished film, trailer, social, and audio deliverables against explicit delivery specifications for file existence, streams, codecs, resolution, frame rate, duration, audio properties, checksums, and optional signal warnings.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Delivery QC

## Workflow

1. Read `../../references/RELEASE_DELIVERY.md` and the relevant delivery specification.
2. Use `scripts/delivery_qc.py` to inspect actual files.
3. Treat missing required files, unreadable containers, missing required streams, or specification mismatches as blockers.
4. Treat optional black/freeze detectors as evidence and warnings unless a project rule makes them blocking.
5. Record SHA-256 for every final deliverable.
6. Never infer QC from a successful generation command alone.

## Done

Each final media deliverable has an evidence-backed QC report and checksum.
