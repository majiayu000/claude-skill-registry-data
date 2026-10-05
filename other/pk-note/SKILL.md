---
name: pk-note
description: Use the note-management skill to capture a new fleeting note titled
---

Use the note-management skill to capture a new fleeting note titled
$ARGUMENTS.

After capturing the note, you MUST perform the Zettelkasten link
suggestion workflow:

(a) Query `index-management` (`search_entities`) for the top 5
    semantically overlapping Notes, WorkItems, DecisionRecords, and
    Artifacts that relate to this note's topic.

(b) Propose 2–5 qualified links using the Note schema's 7 relation
    types:
      - elaborates   — this note expands on or adds depth to target
      - contradicts  — this note challenges or refutes target
      - supports     — this note provides evidence for target
      - is-example-of — this note is a concrete case of an abstract
                        claim in target
      - see-also     — loosely related; reader may find target useful
      - refines      — this note improves on or supersedes target
      - sourced-from — this note's ideas draw from target (literature
                       notes)
    For each proposed link, provide a one-sentence `context:` field
    explaining why the connection matters — not just that it exists.

(c) Present the proposed links to the user for confirmation. Add only
    the confirmed links to the note's `links:` field. Dismissed links
    are not recorded.

This workflow builds a knowledge web incrementally with every capture.
