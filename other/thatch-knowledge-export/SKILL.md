---
name: thatch-knowledge-export
description: 'Compile everything thatch knows about a topic into a curated, self-contained markdown file for knowledge transfer to another engineer. Searches across stores with varied query phrasings, curates out personal noise, fact-checks code-related memories against the current codebase, and generates a clean export. Use when the user asks to export, compile, or transfer knowledge about a topic.'
---

You are a knowledge exporter.
Your job is to find everything thatch knows about a topic, verify it, curate it, and write it into a markdown file that another engineer can use to get up to speed.

# The Use Case

The user and a teammate work on the same project. The user's agent has accumulated memories across sessions. The teammate needs that knowledge. This skill compiles it into a portable, self-contained document.

The export is **knowledge transfer**, not personality transfer. It contains technical and project context that a colleague needs to be productive. It does not contain the user's inner monologue about their teammates.

# Method

## Step 1: Store Selection

Call `thatch_store_list` to enumerate all available stores.

Ask the user which stores are relevant to this export. The user may have personal and work stores on the same machine. Including personal stores would add confusing noise. The user is the filter.

Present the store list and ask: "Which of these stores should I search? Exclude any that are personal or unrelated."

Default to all stores if the user says "all" or does not specify. But asking is the right default because the personal-vs-work distinction matters.

## Step 2: Broad Search

`thatch_memory_recall` caps at 20 results per call and uses semantic search. A single query will miss memories that use different vocabulary for the same concept. To be comprehensive, issue multiple calls with deliberately varied phrasings.

For each selected store, run `thatch_memory_recall` with:
- The topic name directly
- Synonyms and alternate phrasings (e.g. "rotation keys" and "key rotation" and "KMS key cycling")
- Broader framings (e.g. "database architecture" when the topic is "migration system")
- Narrower framings (e.g. "batch cursor implementation" when the topic is "rotation system")
- Related subsystem names (e.g. "scanner API" when the topic is "scanning pipeline")
- Jargon variants the team might use

Set `limit` to 20 (the maximum) on each call to cast the widest net.

Also call `thatch_memory_list` for each selected store. This enumerates every label, catching memories that semantic search missed because the label text does not match the query but the content is relevant.

Set `includeArchived: true` on recall calls. Archived memories are historical context that may be valuable for the export, even though they are excluded from default search.

## Step 3: Dedup by Label

Multiple recall calls with different phrasings will return overlapping results. Collect unique labels only. A memory that appears in three query results is still one memory.

## Step 4: Read and Classify

Call `thatch_memory_show` for each unique label. Read the full content.

Classify each memory into one of three categories:

- **Code-related** — architecture, data models, file paths, function names, conventions, API contracts, configuration. These need fact-checking.
- **Preference/process** — user preferences, workflow decisions, review attitudes, coding style guidance. These do not need fact-checking but need curation.
- **Archived** — historical records, flagged with `archived:true`. Included in the export as-is. No fact-checking.

## Step 5: Curation Filter

Review every memory for content that is personal to the user or could cause friction if shared with a colleague. This applies to all categories, including code-related ones.

**Exclude or sanitize content that includes:**
- Attitudes toward specific reviewers, reviewees, or managers (e.g. "Jeff finds Cody's PRs frustrating because...")
- Emotional reactions to code, people, or process (e.g. "OMFG this react was written like COBOL")
- Interpersonal dynamics or opinions about individuals' coding ability
- Anything the user would not want a colleague to read

**When in doubt, exclude.** The export is for a colleague, not for the user's therapist.

Strip the "who said what" and keep the "what is true about the code." If a memory says "Jeff prefers X because Nik's approach caused a bug in PR #123," the export should say "Approach X is preferred. Approach Y caused a bug in PR #123." Keep the technical fact, drop the personal framing.

This curation applies to the export file only. Do not modify the original memories in the store. The user's memories are the user's memories. The export is a curated view.

## Step 6: Fact-Check

Load the `thatch-memory-verify` skill. Apply it to each code-related, non-archived memory.

If your harness supports sub-agent dispatch, you may process multiple memories concurrently by dispatching `thatch-memory-verify` for each one in parallel.

Wait for all verifications to complete before proceeding to generation. Each verification may correct stale memories in the store.

**After all verifications complete**, re-read each memory that was corrected by calling `thatch_memory_show` again. The verify skill corrects memories in-place via `overwrite: true`, so the version in your context may be stale. You need the corrected version for the export.

## Step 7: Generate the Export

Ask the user where to write the export file. Write to the specified path.

Structure the markdown as follows:

```
# Knowledge Export: <topic>

Generated: <date>
Stores: <list of stores searched>

## Summary

<2-3 paragraph synthesis of what is known about this topic. Write for an engineer who is new to this area. Lead with the most important architectural facts, then conventions, then gotchas.>

## Verified Knowledge

### <memory label>

Store: <store> | Confidence: <n>/10 | Verified: <date>

<memory content, corrected if needed. Include `path:line` citations from the fact-check where available.>

### <next memory label>

...

## Historical Context

### <memory label>

Store: <store> | Archived

<memory content as-is. These are historical records and may describe a state that no longer exists. They are included for context, not as current truth.>

## Preferences & Process

### <memory label>

Store: <store>

<memory content, curated for professional relevance. Personal opinions and interpersonal observations have been removed.>
```

**Do not include a corrections section in the export file.** The receiving LLM or engineer should see only the corrected state, not the history of what was wrong. Including stale-then-corrected facts risks hallucination about the old version. Corrections are reported to the user separately (Step 8).

Branch-scoped memories get a note: `(scoped to branch: <branch>)` after the store name.

## Step 8: Report to User

Tell the user:
- Where the export file was written
- How many memories were included (by category: verified, historical, preferences)
- A brief summary of corrections made during fact-checking (which memories were updated and what changed)

This correction summary is for the user only. It does not go in the export file.

# Notes

- The export file is self-contained. The receiving engineer should not need thatch database access to use it. Include full memory content, not just labels.
- Confidence scores and store names are included so the reader can assess reliability.
- If the user asks to export knowledge for a specific purpose (e.g. "for Nik to review my project"), tailor the summary to that purpose.
- Archived memories are valuable for understanding why code looks the way it does. Include them, but label them clearly as historical.
- The curation step is about professional relevance, not about hiding technical truth. If a memory records that a specific approach caused a bug, that is technical information the colleague needs. The personal framing around it is what gets stripped.
