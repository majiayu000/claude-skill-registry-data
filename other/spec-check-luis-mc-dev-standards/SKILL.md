---
name: spec-check
description: Validate a specification document's numbering and cross-references — duplicate or out-of-order headings and requirement IDs, orphan subsections, gaps, malformed identifiers, and dangling §/R references including citations into other specs. Use after writing or revising any spec, before handing it to anyone, and whenever a spec cites another document by name. Also use when asked to check, lint, or verify a spec, or when a spec has been renumbered, split, merged, or had sections deleted.
model: sonnet
effort: medium
---

# Spec Check

Runs `assets/spec_check.py` over a specification. It reports every structural
defect it can decide from the text alone. It is the partner to `spec-new`: that
skill writes specs to a numbering discipline, and this one proves the discipline
held. Both ship in the `luismc-specs` plugin.

```bash
python3 assets/spec_check.py specs/mine.md
```

`assets/spec_check.py` sits alongside this file. It uses only the standard
library, so there is nothing to install.

Exit `0` means clean. Exit `1` means findings. Exit `2` means the file could not
be parsed. It takes any number of paths, so a repo's whole `specs/` directory can
go in one run.

## Citing another document

A bare `§4.2` means *this* document's §4.2. A reference to another spec carries
its name: `STACKSPEC §4.2`. Register every document you cite. Otherwise its
references are skipped, not checked:

```bash
python3 assets/spec_check.py specs/mine.md \
  --external STACKSPEC=<plugin>/skills/tech-stack-setup/references/invariants.md \
  --external AUTHSPEC=<plugin>/skills/auth-setup/references/authentication.md
```

Point at the spec where it is *maintained*, inside the `luismc-project-setup`
plugin. Do not point at a copy inside a product. `STACKSPEC §2.1` forbids a
product from vendoring either spec, so a product has no local path to register.
Its Stack Profile names the version instead, and the profile's numbering does not
match the spec's. If you register a Stack Profile here, `STACKSPEC §5.3` resolves
against whatever the profile's own section 5.3 happens to be.

In this repository both specs are registered by default. You need the flag only
for a document that cites something else.

Registration makes an outbound citation *resolve against the other document*.
Without it, `STACKSPEC §9` falls through to internal resolution. It then matches
your own §9 if you have one. That is a silent false pass. It is the reason this
flag exists, rather than the checker guessing.

## What it checks

Three families, all decidable from the document text. None needs judgement, which
is why it can gate a build.

**Headings** — every number unique; heading depth matching the number's depth
(`### 4.2` is level 3); no orphan subsection whose parent is missing; no gap in
a sibling run; ascending order.

**Identifiers** — every `Rn.n` defined once; the prefix matching the section it
sits in (an `R7.3` inside §6 is a copy-paste that will resolve to the wrong
requirement); no gaps; ascending; nothing malformed like `R6.6.1`.

**References** — every `§n.n` resolves to a heading, and every `Rn.n` resolves to
a definition. The target may be in this document or in a registered one.

It deliberately does *not* flag two things. First, statutory citations
(`§164.312`, `§1798.105`). A flat floor of 100 excludes them, not "one past the
highest heading", because a tight ceiling silently reclassifies a dangling
reference as statutory. Second, a lettered insertion (`R4.9a`) is not a gap,
because that is how you add a requirement without renumbering.

## The numbering rules it enforces

These come from the spec discipline `spec-new` writes to. They exist because
citations are the part of a spec that rots invisibly.

- **Numbering is append-only.** Never renumber to tidy up. A deletion leaves a
  gap, and the gap is the record that every citation stayed stable.
- **Insert with a letter**, `R4.9a`, rather than shifting everything after it.
- **`§n.n` and `Rn.n` are different namespaces.** `§9` is a heading; `R9.1` is a
  requirement. They look alike and people routinely confuse them. That is why
  the checker resolves them separately and reports them separately.

## When it finds something

Fix the document, not the reference. A dangling `§12.4` usually means a section
was deleted or renumbered. Repair it by restoring the number, or by pointing the
citation at what actually exists. Never renumber the target so the stale
citation happens to land, which just moves the break somewhere else.

## Scope

It reads structure, not meaning. Two requirements that are each coherent but
contradict each other pass here and need a human. Content checks tied to one
particular document — entity tables, route maps, retention schedules — belong
with that document, not in this skill.
