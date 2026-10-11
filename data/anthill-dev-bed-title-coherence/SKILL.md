---
name: anthill-dev-bed-title-coherence
description: "Use when the AntHill client shows one title or none, project counts of 0, an asset 'not in your folder' then 'already in', or TitleVersions missing or all current, or when wiring BranchPaths or title branches into a dev bed. Also when the client lists titles the server does not, or a title is listed but cannot be set up."
---

# AntHill dev bed title coherence

A title is four things that must describe the same world: a `Projects` row with a `Branch`,
a pushed Lore branch on the repo the dashboard serves, a workspace cloned from that repo, and
what the crawler recorded for that branch. Every title symptom is one of these missing or
pointing elsewhere. Work down the chain; each check is cheap and rules out a whole class.

## Symptom → cause map

| Symptom | Cause | Section |
|---|---|---|
| Only one title in the picker, or none | `Projects` table empty (`/api/config` shows `"projects":[]`) | 1 |
| Title listed but cannot be set up; "this machine does not know a branch called X" | no `Branch` on the project, or no matching pushed Lore branch | 1, 2 |
| "not in your folder", then "already in" | workspace is a clone of a *different* Lore repo | 3 |
| Titles listed but counts all 0 | no asset→project membership (snapshot `assets carrying a project: 0`) | 4 |
| Per-title versions missing, or every title reads "current" | no branch crawl, or the branches never diverged | 4, 5 |
| Sidebar lists titles the server does not | stale rows in client `catalogue.db` | 6 |
| Title missing from the folder picker, or a folder under the wrong title | unregistered workspace, or a stale `ProjectId` | 7 |

## 1. Projects: ask the server, then the database

```bash
curl -s http://localhost:5252/api/config
```

`projects: []` means nothing is checkoutable. `ServerConfigService.BuildAsync` reads
`db.Projects`; `CheckoutableProjects` then filters on `!string.IsNullOrWhiteSpace(Branch)`,
so a project with no branch is listed but cannot be checked out.

The client is NOT caching stale config: `ServerConnection.ConfigAsync` fetches live every ask
and only falls back to `server-config.json` when the server is unreachable (15s backoff after
a failure). If the picker is empty, the database is empty — do not go hunting for a sync bug.

Postgres usually runs in Docker, and `psql` is often not on PATH:

```bash
docker exec anthill-db-1 psql -U anthill -d anthill_bed -c 'select * from "Projects"'
```

Create one project per title, with `Branch` set, from the dashboard's **Settings → Add
project** form (`ProjectAdminService.CreateAsync`). Use SQL only to unblock: `Name` has a
unique index, so seed with `on conflict ("Name") do update set "Branch" = excluded."Branch"`.

## 2. A Lore branch per title, created and pushed

The branch must exist on the repo that `/api/config`'s `loreServerUrl` names. A fresh art repo
often has only `main`, and a local branch is not enough — the client clones from the server:

```bash
lore --repository <repo> -P branch create <title>
lore --repository <repo> -P branch push <title>
lore --repository <repo> -P branch list          # confirm under "Remote branches"
lore --repository <repo> -P branch switch main   # branch create switched the working copy
```

Switching back matters when that repo is the server-side working copy.

## 3. Workspaces cloned from the repo the dashboard serves

This is the one that produces the contradictory pair of messages, and it is easy to miss
because both messages are individually true.

```bash
curl -s http://localhost:5252/api/config          # note loreServerUrl + rootPrefix
lore --repository <workspace> -P status           # note "Repository <id>"
ls <workspace>                                    # top-level dirs must match rootPrefix
lore -P repository list lore://127.0.0.1:41337    # map id -> name
```

The id is also in `<ws>/.lore/config.toml`. If `rootPrefix` is `source` but the workspace only
holds `intermediate/`, the asset path genuinely is not in the folder, and Lore then has nothing
to bring for that path on that branch — surfacing as "already in". Re-clone from the correct
repo; `clone` needs the repo name (`lore://host:port/<repoName>`), not the bare host:

```bash
lore -P clone "lore://127.0.0.1:41337/<repo>" "<path>"
lore --repository "<path>" -P branch switch <branch>
```

A full real-art clone takes 1–3 minutes; run it backgrounded. The crawler needs one such clone
per title branch as well (section 4).

## 4. Crawl each title's branch

The per-title model already exists. Verify it before changing anything; do not build a new one.

- `AssetRevisions` is UNIQUE on `(AssetId, Branch)` — one recorded version per asset per
  branch. `AssetLibraryContext` defines this.
- `TitleVersion.Current` compares by **ContentHash, not date**. Two titles holding identical
  bytes both read current; older bytes read `Behind`.
- `TitleVersionsPanel` (asset page) reads the **catalogue**, not workspaces — so it works
  offline and dashboard and client agree.
- Populated only by the crawler via `Indexer:BranchPaths`.

`RunOnce` seeds; drop it for the 5-minute loop:

```
ConnectionStrings__AssetLibrary=Host=...;Database=<db>;...
Indexer__RepositoryPath=<workspace on main>      # the library
Indexer__BranchPaths__0=<title workspace>
Indexer__BranchPaths__1=<title workspace>
Indexer__Rules=bigant-source                     # authored art; bigant = cooked
Indexer__RootPrefix=source
Indexer__RunOnce=true
dotnet run --project src/AntHill.Indexer.Host
```

Expect per branch `Crawled branch workspace <path>: N entries recorded`, then
`Filed N asset(s) into projects by the branch holding them`.

Membership, which the sidebar counts: a project with a `Branch` is filed by the branch holding
its assets after every branch crawl, whatever its `RootPath`. Without a `Branch` it falls back
to `RootPath` and hand-tagging; `RootPath` must be a real prefix of the tree (e.g. under
`source/`), so an empty or wrong one reads 0 however many assets exist (verified 2026-09-24,
`Project.cs`, `CrawlRunner.cs`).

Traps:

- **A title's crawl deliberately concludes very little**: it records that branch's revision
  only. It will not add or remove assets or rewrite derived fields. Crawling a title *as if it
  were main* empties the catalogue on the first pass.
- Main is crawled first on purpose, so new assets land everywhere in one pass.
- **Never point BranchPaths at folders being edited** — the crawl records uncommitted work as
  what the title holds. Use dedicated read-only clones.
- The indexer refuses to start if migrations are pending (the web app owns the schema).

## 5. Force divergence

Branches created from one revision are byte-identical, so every title reads "current" —
correct and useless. Modify a file in one title's workspace, then (the message is POSITIONAL,
`-m` is rejected):

```bash
lore --repository <ws> -P stage <path>
lore --repository <ws> -P commit "message"
lore --repository <ws> -P push
```

Re-crawl, then verify in the catalogue, not the UI:

```sql
select r."Branch", r."RevisionId", left(r."ContentHash",16)
from "AssetRevisions" r join "Assets" a on a."Id"=r."AssetId"
where a."Path" like '%<asset>%' order by r."Branch";
```

The diverged branch shows a different RevisionId *and* ContentHash. Multiple rows per branch =
a multi-file asset; only the changed files differ.

## 6. Clear stale local catalogue rows

Catalogue sync reconciles assets but leaves `Projects` and `AssetProject` rows behind, so
titles from an old bed linger with 0 counts. Stop the client first, then:

```bash
sqlite3 "$LOCALAPPDATA/BigAntStudios/AntHill/catalogue.db" \
  "delete from AssetProject; delete from Projects;"
```

They repopulate from the next snapshot.

## 7. Workspace registration

`workspaces.json` (`$LOCALAPPDATA/BigAntStudios/AntHill/`) lists working copies, and
`FolderChoices` shows only these — it never lists catalogue projects, so a title without a
registered folder cannot appear in the folder picker. `ProjectId` must match the *current*
catalogue id; ids from a previous bed silently point at the wrong project. It is read at
startup, so **restart the client** after editing.

## Verify

```bash
curl -s http://localhost:5252/api/config                    # projects with branches
curl -s "http://localhost:5252/api/sync/snapshot?since=0"   # assets + projects
ls <workspace>/<rootPrefix>/...                             # a real catalogue path resolves
```

Add the section 5 query when per-title versions are the claim.

## Gotchas

- `lore` is on PATH from `C:/Users/alex.mollard/bin`; `D:/AntHillTesting/tools/lore.exe` is
  the same build (0.8.6+373, verified 2026-09-24).
- Lore CLI: `--repository <path>`, not `-o`. `history <N>` is positional, not `-c N`.
- PowerShell inside bash double quotes eats `$_` and `$var`. Write a `.ps1` and run it with
  `-File`, or the script silently mangles.
- An orphan `AntHill.Web` holding 5252 makes your own fail with
  `Failed to bind to address ... address already in use`; find and stop it as in
  `anthill-test-environment`.
