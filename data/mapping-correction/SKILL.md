---
name: mapping-correction
description: Use when changing a series that already exists in the catalog — a new season aired, the manga published past the last mapped arc, an arc boundary was wrong, a film is missing, or the `mapping-audit` script reported an error to fix. For a series with no catalog entry at all, use arc-mapping instead.
---

# Mapping Correction

`arc-mapping` creates a series that does not exist yet and stops there. Everything after that first insert lands here: extending, renumbering, and correcting rows that users are already reading.

**REQUIRED BACKGROUND:** `arc-mapping` defines the schema, the cumulative-episode convention, and the research sources. This skill assumes them.

Corrections are database writes. No commit, no release. Clients pick them up on next launch, which also means a bad write is live immediately.

## Before writing anything

1. **Read the current rows.** Never edit blind.
   ```sql
   select s.id, s.title, s.anilist_anime_id, s.anilist_manga_id, s.source_notes,
          a.position, a.episode_start, a.episode_end, a.chapter_start, a.chapter_end, a.arc, a.season
   from series s join arc_mappings a on a.series_id = s.id
   where s.title ilike '%<show>%' order by a.position;
   ```
2. **Re-fetch the counts.** The AniList `curl` in `arc-mapping` step 1. Never carry forward a count from the original insert; that is what went stale.
3. **Confirm the boundary against a source** (fandom wiki, Wikipedia episode list, AniList forum guide) before changing a number. An audit finding is a prompt to research, not a fact.

## The four corrections

| Situation                     | What changes                                                                                                                                               |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Manga published further**   | Extend the last arc's `chapter_end`, or append a new arc with `episode_start`/`episode_end` `NULL`. Update `source_notes` with the new chapter count.      |
| **New season aired**          | Convert the affected tail arcs from `NULL` episodes to real **cumulative** ranges, and/or insert new arcs. Set `season`. Update `source_notes` arithmetic. |
| **Boundary was wrong**        | Change `chapter_start`/`chapter_end` on **both** adjacent arcs so they stay contiguous. Fixing one side creates a gap or an overlap.                       |
| **Film missing or misplaced** | Insert into `movies` at the right `position` and renumber the rest. `movies.length` is what the series page displays.                                      |

## Inserting into the middle

`arc_mappings` and `movies` both carry `unique (series_id, position)`, so a naive insert collides. Shift the tail first, in one statement, descending:

```sql
-- make room at position 5
update arc_mappings set position = position + 1
where series_id = <id> and position >= 5;

insert into arc_mappings (series_id, position, episode_start, episode_end, chapter_start, chapter_end, arc, season)
values (<id>, 5, 137, 148, 302, 327, 'Culling Game Arc', 3);
```

Deleting an arc requires the mirror: delete, then `position = position - 1` for everything after it. Positions must stay a dense 0-based run.

## Always finish with

```bash
bun run scripts/audit-mappings.ts --series "<show>" --no-ignore
```

`--no-ignore` matters here: if the series has triaged entries, the default run hides exactly the codes you are most likely to have just broken.

## Common mistakes

| Mistake                                            | Consequence                                                                                             |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Treating new-season episodes as starting at 1      | Episodes are cumulative across seasons. S3E1 of a 24-episode run is episode 25.                         |
| Changing `anilist_anime_id` to the new season's id | The first season's id is the stable key. Changing it orphans user progress and breaks existing links.   |
| Fixing one side of a boundary                      | Leaves a gap or an overlap. Always edit both adjacent arcs.                                             |
| Extending the last arc past the real chapter count | `catalog-behind-manga` becomes `catalog-ahead-of-manga` and the UI promises chapters that do not exist. |
| Leaving `source_notes` stale                       | It is the only record of the cumulative arithmetic and manga state. The next correction depends on it.  |
| Inserting without shifting `position`              | Violates `unique (series_id, position)`; the write fails or, worse, you renumber by hand and skip one.  |
