---
name: vp-note-quality
description: "Reference checklist for Basic Memory note quality — rules preventing self-referential content in subject-domain notes (the fourth-wall anti-pattern). Preloaded into knowledge-maintainer and knowledge-gardener agents via the skills frontmatter field."
user-invocable: false
allowed-tools: []
---

# Note Quality Checklist

When writing or editing Basic Memory notes, apply these rules to prevent the
"fourth-wall anti-pattern" — self-referential content that references the
knowledge graph, the enrichment process, or the state of personal knowledge
sources instead of focusing on the note's subject.

**Root cause:** Task-boundary collapse. When an agent evaluates whether a topic
fits the graph AND writes the note, the evaluation leaks into the content. The
fix is a firewall: discard graph-fitting analysis before writing.

**Diagnostic question:** "If this note were exported and read by someone who
knew nothing about the enrichment session and had never heard of Basic Memory,
would every sentence make sense?" If no — it is harmful self-reference.

## Rules

1. **Subject test.** Every sentence — including frontmatter prose fields like
   `description` — must be about the note's declared subject. Content about the
   knowledge graph, the enrichment session, or personal knowledge sources must
   be deleted before writing.

2. **No inventory claims.** Never write "X has zero presence in
   Raindrop/Readwise/Basic Memory." Coverage state is ephemeral and becomes
   false immediately. It belongs in session notes, not permanent knowledge notes.

3. **No significance rankings.** Never write "this is the most significant gap"
   or "this is the most important connection." These are editorial judgments
   about the session, not facts about the subject.

4. **Firewall graph-fitting analysis.** If you assessed whether a topic fills a
   graph gap before writing, discard that analysis entirely. The note is not a
   report on the assessment; it is knowledge about the subject.

5. **`[gap]` means subject gap, not coverage gap.** A `[gap]` observation
   records something unknown about the subject itself (e.g., "The mechanism by
   which X spread to Y is undocumented"). It never records that the subject was
   absent from Raindrop or Readwise.

6. **`[raindrop]` and `[readwise]` must cite artifacts.** Only add these
   observations if you have a specific bookmark URL, title, or highlight text.
   "No Raindrop bookmarks exist" is not a valid observation. Prefer `[quote]`,
   `[source]`, `[pattern]`, or `[connection]` for the insight itself — use
   `[raindrop]`/`[readwise]` only when the provenance IS the point.

7. **No self-referential sections.** Headings must describe aspects of the
   subject. Sections named "Connection to the Knowledge Graph," "Graph
   Coverage," "Significance to the Graph," or "Why This Note Exists" are
   forbidden.

8. **Export test.** Read the overview paragraph as if to someone who has never
   heard of Basic Memory. If it would not make sense without knowing you are
   building a knowledge graph, rewrite it.

9. **Lede paragraph is subject-first.** The first sentence must state what the
   subject is, not what the graph lacks. Write "Scandinavian Participatory
   Design is a tradition originating in 1970s Scandinavia..." not "This topic
   is completely absent from all personal knowledge sources."

10. **Session observations go in session notes.** Insights about the enrichment
    session itself (which topics cluster, what the session revealed about the
    graph's shape) belong in a separate session summary note, not embedded in
    the subject notes created during the session.

11. **Relation types describe subject relationships.** Types like `depends_on`,
    `relates_to`, `extends`, `maintained_by` describe how subjects relate.
    Types like `fills_gap_in`, `adds_coverage_for`, or `documents_gap_in`
    describe graph topology and are fourth-wall violations. Replace with a
    subject-appropriate relation type.

12. **No session-boundary references.** Never reference the note-creation
    session boundary — phrases like "prior to this session" or "prior to this
    note" describe when the note was written, not the subject. State the
    subject fact directly, with a date if the timing matters.

## Rule Registry

The rules above are the human-readable form of the canonical registry in
`lib/fourth-wall-rules.mjs`; each carries a stable `fw-*` id. Rules marked
**deterministic** have a grep-able `detect` pattern in the registry (the basis
of the "Red Flags" scan below and the knowledge-gardener Step 10 audit); the
rest require judgment. `npm run check:fourthwall` asserts this checklist
documents every registry id and that each `detect` pattern catches a planted
violation on a fixture.

| Rule | ID | Detection |
|------|----|-----------|
| 1. Subject test | `fw-subject-test` | judgment |
| 2. No inventory claims | `fw-inventory-claim` | deterministic |
| 3. No significance rankings | `fw-significance-ranking` | deterministic |
| 4. Firewall graph-fitting analysis | `fw-graph-fitting` | judgment |
| 5. `[gap]` means subject gap | `fw-gap-is-subject` | judgment |
| 6. `[raindrop]`/`[readwise]` must cite artifacts | `fw-provenance-cite` | judgment |
| 7. No self-referential sections | `fw-self-ref-section` | deterministic |
| 8. Export test | `fw-export-test` | judgment |
| 9. Lede is subject-first | `fw-lede-subject-first` | judgment |
| 10. Session observations go in session notes | `fw-session-obs` | judgment |
| 11. Relation types describe subject relationships | `fw-relation-type` | deterministic |
| 12. No session-boundary references | `fw-session-boundary` | deterministic |

## Exception: Meta-Notes

These rules apply to **subject-domain notes** — people, patterns, history,
packages, tools, projects. Notes whose subject IS the knowledge graph itself
(axioms, conventions, tool catalogs, `engineering/agents/*` methodology notes)
may reference Basic Memory, Raindrop, and Readwise freely — that is their
subject matter.

## Red Flags (Scan Targets)

When auditing existing notes, search for these phrases:

- "zero presence in"
- "absent from the knowledge graph"
- "prior to this session" / "prior to this note"
- "most significant gap" / "most important connection"
- "Connection to the Knowledge Graph" (section header)
- "Significance to the Graph" (section header)
- "not yet in Basic Memory"
- "no presence in Raindrop"
- `fills_gap_in` / `adds_coverage_for` / `documents_gap_in` (relation type)

## Enforcement Guidance

**For the knowledge-maintainer (write agent):**
- Before every `edit_note` call on a subject-domain note, re-read the content
  you are about to write and apply the diagnostic question.
- If you find a violation in a note you are editing, queue a rewrite as a
  confirmation item (content-level change — requires user approval).
- When delegating to `/intel`, the skill output
  should already conform — but verify the result before moving on.

**For the knowledge-gardener (read-only auditor):**
- In the fourth-wall audit step, use `search_notes` with red-flag phrases.
- Classify violations by severity: (A) section-level, (B) paragraph-level,
  (C) observation-level, (D) relation-level.
- Report in Warning tier with the specific offending sentence quoted.
- Do not attempt to fix — that is the maintainer's job.
