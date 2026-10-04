---
name: arc-mapping
description: Use when adding a new show's arc mapping — i.e., the user asks to "map <show>", "add a mapping for <show>", or the catalog has no entry for the show. Covers AniList GraphQL ID/count lookup, web research for arc boundaries, and inserting the `series` + `arc_mappings` (+ `movies`) rows into Supabase.
---

# Arc Mapping

## Overview

**Arc mappings** align anime episode ranges to manga chapter ranges, named by arc. They power `EpisodeChapterRail` and related UI that lets users jump between an anime episode and the corresponding manga chapters. Each mapping also carries theatrical **films**; the series page renders their count next to the episode count (e.g. Demon Slayer: `63 eps · 4 movies`).

Mappings live in **Supabase**, in the `series`, `arc_mappings`, and `movies` tables, **not** in the repo. (They used to be JSON files in `src/data/mappings/` registered in `src/data/index.ts`; that was migrated away. If you see references to that workflow anywhere, they are stale.) Adding a mapping is a database write, not a code change or a git commit: clients pick it up on next launch.

This skill walks through creating a **new** mapping (a show with no existing catalog entry). Updates and corrections to existing mappings are out of scope; use `mapping-correction` for those.

**Invariants:**

- Do not guess counts. Step 1's GraphQL lookup is mandatory.
- Catalog tables are read-only under Row-Level Security. Write via the **Supabase MCP** (`execute_sql` / `apply_migration` run as the service role and bypass RLS), the Supabase dashboard, or a service-role script, never the app's publishable key.
- Project ref is `obtgldkascmxbtpnvscn` (confirm via the URL in `src/api/supabase.ts` or `list_projects`).
- One show at a time; verify the rows landed before moving on.

## The Workflow

Follow these in order. Do not skip step 1, do not guess counts.

### 1. AniList GraphQL lookup

Run this `curl` to resolve the show's title to its AniList IDs, counts, and relations:

```bash
curl -s https://graphql.anilist.co \
  -H 'Content-Type: application/json' \
  -d '{"query":"query($s:String){Page(perPage:5){media(search:$s,sort:SEARCH_MATCH){id type title{romaji english} episodes chapters relations{edges{relationType node{id type title{romaji english}}}}}}}","variables":{"s":"<SHOW>"}}' \
  | jq
```

Substitute `<SHOW>` with the user's title (English or romaji, AniList search is fuzzy).

**Reading the response:**

- Pick the `MANGA` entry. It is the source of truth for `anilist_manga_id` and `chapters`.
- Follow `relations.edges` where `relationType === "ADAPTATION"` and `node.type === "ANIME"` to get `anilist_anime_id` and `episodes`.
- If the user named the anime first, do the inverse: pick the `ANIME` entry, follow `relationType === "SOURCE"` and `node.type === "MANGA"`.
- `episodes` / `chapters` may be `null` for the wrong partner type or for ongoing series. Always read `episodes` from the `ANIME` entry and `chapters` from the `MANGA` entry.

**Sequels vs re-airs:**

- **Sequels** (S2/S3 of the same adaptation, surfaced as `relationType === "SEQUEL"`): use the **first season's** AniList anime ID as `anilist_anime_id`; episode counts in the arcs are cumulative across seasons. (My Hero Academia uses id `21459` (S1) for all eight seasons.)
- **Re-airs** (alternate full adaptations of the same manga, e.g. HxH 1999 vs 2011, Fruits Basket 2001 vs 2019): pick the canonical one. Note: two series can share the same `anilist_manga_id`; the catalog resolves a manga-id lookup to the series with the **lowest `id`** (i.e. inserted first). Inserting a re-air later means the existing canonical entry keeps winning the lookup, which is usually what you want.

### 2. Web research for arc boundaries

In priority order:

1. **Show's fandom wiki**, best for arc names + per-arc chapter ranges. Try `<show>.fandom.com/wiki/Story_Arcs` or `/wiki/<Arc_Name>`.
2. **AniList forum threads**, search "Episode-to-Chapter Guide for `<show>`". Community-curated and tend to use cumulative episode counts already, matching this catalog's convention.
3. **Wikipedia "List of `<show>` episodes"**, authoritative for episode counts per season and corresponding manga volumes/chapters.
4. **r/`<show>` "where to start reading from the anime" / "anime-manga sync" threads**, useful sanity check.

Canonical arc names typically come from the fandom wiki. Precise chapter boundaries typically come from per-arc chapter lists on the same wiki.

While researching, also collect the series' **theatrical films** (see the movie spec in step 3). Step 1's `relations.edges` surface most of them: look for `node.format === "MOVIE"` edges (any `relationType`) hanging off each season node, and walk `SEQUEL` edges season by season since later films attach to later seasons. AniList does NOT track every theatrical release (e.g. the Demon Slayer World Tour bridge screenings, Attack on Titan's THE LAST ATTACK), so cross-check Wikipedia's franchise page or the fandom wiki's "Films" section for the full list.

### 3. Compose the rows

A mapping is one `series` row plus its ordered `arc_mappings` rows (and optional `movies` rows).

**`series`:**

| column             | value                                 |
| ------------------ | ------------------------------------- |
| `anilist_anime_id` | first-season anime ID (int, unique)   |
| `anilist_manga_id` | manga ID (int)                        |
| `title`            | English title if present, else romaji |
| `source_notes`     | one short paragraph (see below)       |

**`source_notes`** covers:

- Cumulative episode arithmetic: `"Cumulative episodes across S1 (11) + S2 (13)"`.
- Manga state: `"Manga complete at 171 chapters"` or `"Manga ongoing (current ch. 432)"`.
- Caveats when applicable: `"4-koma source, chapter ranges are approximate"`, `"Episodic/anthology adaptation, ~1 chapter per episode"`, `"Arc boundaries from well-known manga arcs"`.

**`arc_mappings`**, one row per arc, `position` = 0-based order:

| column                         | value                                                                       |
| ------------------------------ | --------------------------------------------------------------------------- |
| `position`                     | 0, 1, 2, … (defines display order)                                          |
| `episode_start`, `episode_end` | inclusive **cumulative** episode range; both `NULL` for unadapted tail arcs |
| `chapter_start`, `chapter_end` | inclusive chapter range (required)                                          |
| `arc`                          | arc name                                                                    |
| `season`                       | optional season number (drives per-season coverage UI)                      |
| `note`                         | optional                                                                    |

- Episodes are **cumulative** across seasons. S2E1 of a 12-ep S1 is `episode 13`. (My Hero Academia's U.A. Sports Festival arc opens S2 at `episode_start = 14`.)
- **Set `episode_start`/`episode_end` to `NULL`** for unadapted tail arcs. The UI tolerates chapter-only arcs (One Piece's Elbaf arc is chapters 1118–1180 with null episodes).
- The last arc must extend to the final chapter count from AniList, or, for ongoing manga, to the last published chapter.

**`movies`**, theatrical films, `position` = release order. `movies.length` is the count the series page shows, so this defines the answer to "how many movies does this anime have?".

| column                         | value                                              |
| ------------------------------ | -------------------------------------------------- |
| `position`                     | 0, 1, 2, … (release order)                         |
| `anilist_id`                   | int, `NULL` when AniList has no entry              |
| `title`                        | English if present, else romaji                    |
| `year`                         | JP theatrical release year (int)                   |
| `chapter_start`, `chapter_end` | inclusive manga range the film adapts, else `NULL` |
| `after_episode`                | cumulative episode the film follows, else `NULL`   |
| `note`                         | provenance (see below)                             |

- `chapter_start`/`chapter_end` + `after_episode` are **only** for films that adapt a manga range, i.e. gap-fillers like Mugen Train (ch 54–69 after ep 26). Align chapters with the arc boundaries.
- `after_episode` alone is fine for canon side films with a well-known timeline slot; leave it `NULL` when placement is fuzzy.
- `note` states what the film is: `"side story (anime-original)"`, `"recap + early premiere of the next season's opening episodes"`, `"all-new-animation theatrical remake of the <X> arc"`, `"adapts the final arc, never adapted on TV"`.

**Include** (released films only, `status` must not be `NOT_YET_RELEASED`):

- Canon arc adaptations that fill gaps within/between arcs (Demon Slayer: Mugen Train, Infinity Castle; THE FIRST SLAM DUNK). These get chapters + `after_episode`.
- Canon sequel/prequel/side-story feature films in the same continuity (the four My Hero Academia films, JUJUTSU KAISEN 0, SAO Ordinal Scale, The Last: Naruto the Movie).
- Bridge films that premiere new content alongside recap footage (Demon Slayer World Tour films, Solo Leveling -ReAwakening-, Kaiju No. 8: Mission Recon, JJK Execution).
- All-new-animation theatrical remakes of in-series arcs (Gintama: Benizakura, Gintama: Yoshiwara in Flames).

**Exclude:**

- Pure re-edit recap compilations of existing TV footage (Attack on Titan's four compilation films, the Haikyu!! recap tetralogy, Madoka movies 1–2, Eva Death & Rebirth, Gintama "on Theater 2D").
- Alternate-continuity reboots branded as separate productions (Rebuild of Evangelion, Berserk Golden Age trilogy vs the 1997 mapping) and films outside the mapping's scoped continuity per its `source_notes`.
- Multi-franchise crossovers (Isekai Quartet), spin-off-franchise films (Boruto, Koro-sensei Quest), and theatrical shorts/3D theme-park films.

### 4. Insert into Supabase

Insert the series and its arcs in one statement via the Supabase MCP `execute_sql` (a CTE resolves the new `series.id` for the arc rows):

```sql
with s as (
  insert into series (anilist_anime_id, anilist_manga_id, title, source_notes)
  values (21459, 85486, 'My Hero Academia',
          'Cumulative episodes across S1 (13) + S2 (25) + ... Manga complete at 432 chapters.')
  returning id
)
insert into arc_mappings
  (series_id, position, episode_start, episode_end, chapter_start, chapter_end, arc)
select s.id, v.* from s, (values
  (0, 1,   13,  1,   21,  'Entrance Exam / Quirk Apprehension / USJ'),
  (1, 14,  25,  22,  44,  'U.A. Sports Festival'),
  -- ...
  (10, null::int, null::int, 424, 432, 'Epilogue')   -- unadapted tail: null episodes
) as v(position, episode_start, episode_end, chapter_start, chapter_end, arc);
```

Then insert films (if any) against the same series:

```sql
insert into movies
  (series_id, position, anilist_id, title, year, chapter_start, chapter_end, after_episode, note)
select id, v.* from series, (values
  (0, 112151, 'Demon Slayer -Kimetsu no Yaiba- The Movie: Mugen Train', 2020, 54, 69, 26,
     'Canon Mugen Train arc; later retold as TV eps 27-33.'),
  (1, null::int, 'Demon Slayer: Kimetsu no Yaiba -To the Swordsmith Village-', 2023,
     null::int, null::int, 44,
     'World Tour bridge screening: Entertainment District recap + Swordsmith Village premiere.')
) as v(position, anilist_id, title, year, chapter_start, chapter_end, after_episode, note)
where series.anilist_anime_id = 148146;
```

**Nulls in `VALUES`:** cast entirely-null columns with `::int` (as above) so Postgres doesn't type the column as `text` and reject the insert into an integer column. Escape apostrophes in titles/notes by doubling them (`'Chopper''s'`).

### 5. Verify

Round-trip the rows you just wrote:

```sql
select s.title, count(a.*) as arcs,
       (select count(*) from movies m where m.series_id = s.id) as movies
from series s left join arc_mappings a on a.series_id = s.id
where s.anilist_anime_id = 21459
group by s.id, s.title;
```

Confirm the arc count matches what you composed and the last arc reaches the final chapter. Optionally open the series in the app (its route id is the manga id or anime id) to eyeball the rail. No git commit is involved; the data lives only in the database.

## Quick Reference

| Step | Action                                     | Artifact                               |
| ---- | ------------------------------------------ | -------------------------------------- |
| 1    | `curl` AniList GraphQL                     | IDs, counts, relations                 |
| 2    | WebSearch / WebFetch                       | Arc names + chapter boundaries + films |
| 3    | Compose rows                               | `series` + `arc_mappings` (+ `movies`) |
| 4    | `execute_sql` insert (CTE for `series.id`) | rows in Supabase                       |
| 5    | `execute_sql` select                       | verified counts                        |

## Red Flags: STOP and Rewrite

| Thought                                              | Reality                                                                                                         |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| "I'll just guess the chapter count"                  | No. Step 1 GraphQL is mandatory.                                                                                |
| "I'll write a JSON file in `src/data/mappings/`"     | No. That workflow is gone. Insert into Supabase.                                                                |
| "I'll register it in `src/data/index.ts`"            | No. There is no import wall anymore; the catalog is fetched from the DB.                                        |
| "I'll git-commit the mapping"                        | No. Mappings are database rows, not code. There is nothing to commit.                                           |
| "Episode 1 of S2 is episode 1 in the mapping"        | No. Cumulative across seasons. S2E1 with a 13-ep S1 is episode 14.                                              |
| "I'll insert with the app's publishable key"         | No. RLS makes catalog tables read-only for clients. Use the Supabase MCP / dashboard / service role.            |
| "The anime entry's `chapters` field is what I want"  | No. Anime entries return `chapters: null`. Pull `chapters` from the `MANGA` entry.                              |
| "Unadapted tail arc, I'll omit the row"              | No. Include it with `episode_start`/`episode_end` = `NULL` and the chapter range.                               |
| "One all-null column in VALUES is fine"              | No. Cast it `::int`, or Postgres types it `text` and rejects the integer insert.                                |
| "Recap compilation films pad the movie count nicely" | No. Pure re-edit recaps are excluded; only bridge films that premiere new content qualify.                      |
| "AniList has no entry for this film, so skip it"     | No. `anilist_id` is optional. Include the film with title/year/note.                                            |
| "This film hasn't premiered yet but it's announced"  | No. `movies` lists released films only.                                                                         |
| "S2 of this show gets its own series row"            | No. One series row per franchise; the first season's anime ID is `anilist_anime_id`, episode ranges cumulative. |

## Common Rationalizations

| Excuse                                                               | Reality                                                                               |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| "AniList is slow, let me skip and use the wiki for IDs"              | The GraphQL query is one round trip and is canonical. Run it.                         |
| "This show has a single short S1, cumulative doesn't matter"         | Cumulative still applies; it's a no-op for single-season shows. Keep the convention.  |
| "The arc boundary I found has weird half-chapter splits, I'll round" | Round to the nearest published chapter, and note the approximation in `source_notes`. |
| "I'll add it through the app somehow"                                | The client can't write the catalog (RLS). Use the Supabase MCP or dashboard.          |
| "I composed the series row, I'll add arcs later"                     | Insert series + arcs together (one CTE). A series with no arcs renders nothing.       |
