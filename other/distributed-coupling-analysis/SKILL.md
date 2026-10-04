---
name: distributed-coupling-analysis
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P023
  - P025
  claims:
  - C00135
  - C00136
  - C00163
  - C00164
  - C00626
  - C00633
  evidence:
  - E00044
  - E00045
  - E00049
  - E00050
  - E00148
  - E00149
  source_anchors:
  - 508117177502-c0006
  - 508117177502-c0007
  - 8afa2d6eafa0-c0004
  authored_from_digest: e60e37f7083525dc10418300ab67cf1f517ed9e82d0b2270c70db81643a0699b
---

# Distributed coupling analysis

## Purpose

Before splitting a distributed system, discern the kinds and strength of coupling between
components and treat data as a first-class architectural concern. The type and strength of
coupling — not the org chart — determine where a system can be cut safely, and operational data
(serving live requests) differs from analytical data (serving reporting and analysis), so ignoring
that distinction when drawing service boundaries produces fragile designs. This skill analyzes
coupling and data ownership before boundaries are fixed.

## When to use

- The caller is decomposing a system into services or drawing data-ownership boundaries.
- A proposed split ignores how components are coupled or who owns the data.
- A decomposition follows team structure rather than the system's actual coupling.

Do not invoke when the system is a single deployable with no distribution or data-partition
question.

## Procedure

1. **Inventory the components and their interactions.** List the candidate services/components and
   how they call, share, or depend on one another.
2. **Discern the kinds of coupling.** For each interaction, characterize the coupling — how
   tightly the components are bound and through what (shared data, synchronous calls, shared
   contracts). The decomposition method rests on naming coupling before cutting.
3. **Find the low-coupling seams.** Identify where coupling is weakest; those are the safe places
   to split. A boundary drawn across strong coupling will be fragile and chatty.
4. **Classify the data.** Separate operational data from analytical data. They have different
   requirements, so a single boundary that mixes them tends to break.
5. **Assign data ownership.** Determine which component owns which data so a split does not leave
   two services co-owning one store. Data ownership is part of where the cut goes, alongside
   coupling.
6. **Test the proposed boundaries.** Check each proposed split against the coupling and
   data-ownership findings; flag any boundary that runs through strong coupling or shared
   ownership as fragile, and recommend re-drawing it along a weaker seam.

## Inputs

- The system's components, their interactions, and the data each reads and writes.
- Any proposed service boundaries or decomposition plan to evaluate.

## Output

A coupling-and-data analysis that names the kinds/strength of coupling, distinguishes operational
from analytical data, assigns data ownership, and judges proposed boundaries by whether they
follow weak-coupling seams and clean ownership rather than the org chart.

## References

- [Laws of software architecture](../../references/laws-of-software-architecture.md) — coupling as
  the basis for decomposition trade-offs.

## Provenance

Distilled from principle(s) **P002/P015/P017**, claims **C00049/C00050/C00226/C00227/C00034/C00041**, evidence **E00016/E00017/E00050/E00051/E00011/E00012**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
