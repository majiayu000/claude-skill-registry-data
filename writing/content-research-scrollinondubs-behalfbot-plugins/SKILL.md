---
name: content-research
description: Research a topic and write a blog-post stub - a structured outline the writer expands, not a finished draft. Use when asked for a topic brief, a content radar, or a stubbed post.
---

# Skill: Content research and blog stub

Produce a blog-post stub ready for the writer to expand and publish.

**A stub is not a draft.** It is the architecture: headline, angle, hook,
section skeleton, sources, tone notes. The writer writes the prose. Handing
back finished prose in someone else's voice is the failure mode this skill is
shaped to avoid - it reads fine and gets thrown away.

## Trigger

An explicit request for a stub, an issue tracker item carrying `task_label`, or
an unattended session where content research is the assigned work.

## Step 1 - check memory first

Search memory for `topic:<slug>` before spending a single search. If prior
research exists and is recent (under 30 days), skip to step 3 and build on it.

This step is the whole reason the skill is cheap to run repeatedly.

## Step 2 - research the topic

Using the chassis search tooling:

1. Find the 3-5 most relevant recent articles and discussions.
2. Identify the **dominant narrative** - what everyone else is already saying.
3. Identify a **contrarian or underexplored angle**. This is the only part of the stub that cannot be got anywhere else, so it is where the effort goes.
4. Find 2-3 concrete examples, data points, or stories to anchor the argument. An abstract point with no anchor is where a draft stalls.
5. If `publication_url` is set, check what the writer has already published there. Restating your own prior post is worse than not writing.

Store in memory:

- Entity: `topic:<slug>`
- Observations: dominant narrative, the angle, key sources, anchor examples, related prior posts, date

## Step 3 - write the stub

Read `voice_guide_path` first, especially for headline and hook style. Voice
guides are personal and stay install-local, so this plugin ships none and only
knows where to look. If the file is absent, say so in the tone notes rather than
inventing a house style.

```
# [Working headline - specific and punchy]

**Angle:** [1-2 sentences. What makes this different from the dominant narrative.]

**Hook:** [Scene, question, or surprising fact to open with]

## Section 1: [Subheading]
- Key point
- Supporting example or data

## Section 2: [Subheading]
- Key point
- Supporting example or data

## Section 3: [Conclusion]
- Main takeaway
- [Bridge to cta_target, if one is configured. If not, end on the takeaway - a
  bolted-on CTA to nothing is worse than no CTA.]

**Suggested sources:** [URL + one line each]

**Tone notes:** [Relevant guidance from the voice guide]
```

House style: no em dashes, use " - " (space-dash-space).

## Step 4 - file it into the pipeline

Content moves forward one stage at a time through `pipeline_stages`.

### `files` backend (default)

One directory per stage under `pipeline_root`, created on first use. A new stub
is written to the first stage as `YYYY-MM-DD-<slug>.md`. Moving a stage forward
is moving the file. Nothing external is needed, and the pipeline state is
visible with `ls`.

```bash
mkdir -p "$CONTENT_PIPELINE_ROOT/1-researching"
# write the stub to $CONTENT_PIPELINE_ROOT/1-researching/YYYY-MM-DD-<slug>.md
```

### `siyuan` backend

File the stub as a sub-document under the stage's parent block.

**Identify stages by block id, never by path.** The folder names and the paths
above them get renamed and moved; the ids do not. Resolve the notebook and the
path at runtime from the stage id:

```sql
-- notebook that currently holds the stage
SELECT box FROM blocks WHERE id = '<siyuan_stage_ids["1-researching"]>'
-- current path of the stage, to append the new title to
SELECT hpath FROM blocks WHERE id = '<siyuan_stage_ids["1-researching"]>'
```

Then create the sub-document with the resolved notebook and `<hpath>/<Post
Title>`, and confirm it exists:

```sql
SELECT id FROM blocks
WHERE path LIKE '%/<stage_id>/' || id || '.sy'
  AND content = '<Post Title>'
  AND type = 'd'
```

To list everything in the pipeline, match on the `path` column against each
stage id. **Do not use `parent_id`** - it is empty for document blocks and only
populated for paragraph blocks, so the query returns nothing and looks like an
empty pipeline:

```sql
SELECT id, content, hpath FROM blocks
WHERE type = 'd' AND (
  path LIKE '%/<stage_id_1>/' || id || '.sy'
  OR path LIKE '%/<stage_id_2>/' || id || '.sy'
  -- one clause per configured stage
)
ORDER BY path, content
```

Do not use a child-blocks call on a stage node either. That returns the
paragraph blocks inside the stage document itself, usually a single
placeholder, not the child documents. Wrong tool, and it returns a convincing
false empty.

Move between stages with the move-document call, by block id.

## Step 5 - close the loop

If the work came from an issue tracker item labelled `task_label`, comment with
where the stub landed and close it.

Content lives in the pipeline, not in the issue tracker. Issues are for
software work.

## Notes

- `stubs_per_session` stubs per unattended session, default one. Research quality falls off a cliff when the same session grinds out a fourth outline.
- If `priority_topics` is set, prefer topics that connect to them. If it is empty, pick on merit.
- Always read the voice guide before writing the headline and the hook. Those two lines carry the voice; the rest of a stub is structure.
- Do not write the full post. Prepare the architecture and stop.
