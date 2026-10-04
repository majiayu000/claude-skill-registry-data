---
name: vault-tend
description: Whole-vault maintenance pass — normalize frontmatter, flag language drift, repair broken wikilinks, find duplicate people or pages, propose archives. Always previews and asks before changing anything. Use when the user says "tidy the vault", "clean up", "normalize", "fix the broken links", "deduplicate", "translate the vault", "vault maintenance".
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, maintenance, cleanup]
    related_skills: [task-roundup, knowledge-stub]
    requires_toolsets: [second_brain]
---

# Vault tend (Hermes edition)

The riskiest skill in the set: it touches notes the user did not just write. Preview first, always,
and remember that `02-people/` and `05-decisions/` are append-only — a "cleanup" there is data loss.

1. `sb_brief` — the working language decides what counts as language drift.
2. `sb_tend(scope=<all | frontmatter | language | links | duplicates | archive>)`, without
   `apply_safe`. Nothing is written by this call.
3. Show the user a grouped preview: counts per `kind`, then up to five example paths per group.
   Never paste the full report; it is long by design.
4. Ask for a go **per group**, not once for everything. Then apply, one group at a time:
   - `safe_fixes` → re-run `sb_tend(scope="frontmatter", apply_safe=true)`.
   - `missing-preamble` → `sb_read` the note, write 2-3 English sentences, `sb_append_section`.
     If the note has no preamble at all, the heading must be created at the top: report those
     rather than guessing at content you have not read.
   - `broken-links` → check for a near-miss first (`sb_find_person`, `sb_search`). A typo gets fixed
     in the source note; a genuinely new concept gets a stub via `/knowledge-stub`; a link to
     something that never existed gets dropped, with the user's ok.
   - `duplicate-people` → `sb_read` both timelines before saying a word. Two people can share a first
     name. A merge is append-only: copy the entries into the survivor with `sb_append_timeline`, then
     propose moving the other to `07-archive/`. Never delete.
   - `body-language` → re-language the body, preserving quotes, names and figures verbatim. The
     preamble stays English. One note per commit for anything long.
   - `archive-candidate` → move to `07-archive/` only after the user confirms, one batch at a time.
5. `sb_commit("vault-tend: <group>")` after each batch, never one commit for the whole pass. If the
   pre-commit hook rejects, read which rule fired and fix it — do not work around it.
6. Report: what changed, what you left alone, and what still needs the user's decision.
7. Hard limits, whatever the user asks: never delete a note, never rewrite a "Compiled truth"
   section, never edit an existing timeline entry, never touch the `(auto-logged)` and
   `(Backfilled)` markers.
