---
name: pattern-language
description: >-
  Write an Alexandrian pattern language (pattern-language.yaml) for a
  repository: read the existing materials, mine recurring force-configurations,
  and emit a YAML file in the fixed format shared by the existing pattern
  languages (declarative-agents, agent-failure-modes). Also validates and
  extends existing languages. Triggers: pattern language, design patterns
  yaml, extract patterns, mine patterns, pattern-language.yaml, Alexander
  patterns, forces and solution, pattern grammar, write the patterns file.
---

# Pattern language (mine materials, write the YAML)

This skill turns a repository's materials into a `pattern-language.yaml` in
the Alexandrian tradition: not a catalogue of tips but a *language* — each
pattern names a field of forces and the configuration that resolves them, and
the grammar connects each pattern to the ones that create its context and the
ones that complete it.

## Where things live

- **Format:** `references/format-spec.md` — the schema (header block,
  top-level keys, entry keys, grammar semantics, quality bar), distilled from
  the three existing instances.
- **Method:** `references/mining-guide.md` — forces-first extraction, the
  confidence rubric, disqualifiers, ordering, sizing.
- **Skeleton:** `assets/template.yaml` — copy to start a new language; it
  validates as-is.
- **Validator:** `scripts/validate_language.py <file>` — structural checks
  (keys, unique ids/numbers, grammar resolution, cites, connectivity);
  `--fix-plan` adds a concrete suggested edit per finding (read-only).

## Known instances (study before writing)

| File | Role |
|---|---|
| `declarative-agents/design-patterns/pattern-language.yaml` | the canonical: 11 build-time patterns, full field set, rich external examples |
| `agent-failure-modes/aaai-2027/pattern-language.yaml` | extends the canonical (`da:` prefix); paper scaffolding with `paper` bindings |
| `agent-failure-modes/ieee-tse/pattern-language.yaml` | paper scaffolding with `paper_sections`/`experiments`; delegates citations via `bibliography_note` |

## The workflow

### 1. Study the neighbors

Read the known instances (above) and any pattern language already in or near
the target repository. Two things come from this: the format by example, and
the **scope boundary** — a structure already named in a sibling language is
never restated; it is linked (`extends` with a prefix, `grammar.overlaps`, or
`examples.kind: sibling`). Decide up front what this language covers that no
sibling does, and write that boundary into the header comment.

### 2. Read the materials

Read what the target repository actually contains — architecture docs, specs,
code, papers, experiment results, review history. The patterns live where the
friction lived: invariants defended in review, structural bug fixes,
validation rules, reverted experiments. Collect tensions, not features.

### 3. Mine candidates

Apply `references/mining-guide.md`: for each candidate, write the forces (the
constraint side) and the solution (the recipe side) — if you cannot write
both, it is not a pattern. Hunt recurrence in shipped systems and prior
literature; every independent occurrence becomes an `examples` entry with a
full citation. Score `confidence` 0–2 from the external examples list, not
from conviction. Apply the disqualifiers ruthlessly (a feature, a preference,
a sibling's pattern, a pattern with no liabilities).

### 4. Order and connect

Number from largest context to smallest refinement. Fill the five grammar
relations for every pattern; the language must form one connected graph.
Test: read the `intent` lines in number order — they should reconstruct a
single argument, which you then write out as the header's "THE ARGUMENT,
TOP TO BOTTOM" paragraph.

### 5. Write the YAML

Copy `assets/template.yaml` and fill it per `references/format-spec.md`.
Keep the conventions block verbatim. If the language is paper scaffolding,
include the INTERNAL-ONLY RULE in the header and a `paper` field per pattern
— the coined names never reach the paper's prose. Every example's `cite`
gets a full bibliography entry (author, year, title, venue), or use
`bibliography_note` to delegate to the repo's existing references file.

### 6. Validate and iterate

```bash
python3 <skill>/scripts/validate_language.py <path>/pattern-language.yaml
```

Fix findings until clean. The validator checks structure only; the quality
bar (3+ forces, real liabilities, imperative solutions, self-containment) is
in the format spec and is judged by reading, not by the script.

### 7. Prose pass

The file carries substantial prose (intents, contexts, solutions). Run the
`filter-tells` skill over it — pattern languages are exactly where coined-bigram and
compressed-conversation tells accumulate, and every coined *pattern name* is
intentional but everything else must survive a cold reader.

## Repairing an existing language

Run the validator with the plan flag:

```bash
python3 <skill>/scripts/validate_language.py <file> --fix-plan
```

Each finding carries a concrete suggested edit — the verbatim conventions
block to insert, a skeleton for a missing key, a bibliography stub or a
close-match rename for a broken cite, wiring candidates for an orphan.
Apply the plan by **editing the file in place**: never regenerate a pattern
language through a YAML dumper — the header block is comments, and a
round-trip destroys them. The script is read-only by design.

Two kinds of repair, treated differently:

- **Structural** (missing conventions/keys/grammar stubs, broken references,
  unresolved cites): mechanical — apply the suggested edit as written.
- **Content** (fewer than 2 forces, missing liabilities, confidence out of
  range): the plan routes these to the mining guide — a pattern missing its
  tension needs mining, not boilerplate. Filling `forces` with filler to
  silence the validator produces a catalogue entry, not a pattern.

Re-validate to zero findings. Bump `version` only if the pattern set changed
(a pure repair does not). If prose was touched, run the filter-tells pass.

## Extending an existing language

Adding a pattern to an existing file: mine and write the one entry (steps
2–5 apply to it alone), place its `number` by context size (renumbering
neighbors is allowed — ids are the stable keys, numbers are the reading
order), wire its grammar into the existing graph, and re-validate. Bump
`version` when the pattern set changes.

## Dependencies

PyYAML for the validator (the pixi environment supplies it; see the agent
directory's `pixi.toml`). Everything else is reading and writing.
