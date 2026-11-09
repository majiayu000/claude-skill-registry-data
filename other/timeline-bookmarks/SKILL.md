---
name: timeline-bookmarks
description: "Use when the saved-post archive is read, scraped or published."
license: CC0-1.0
---

# Timeline bookmarks

Three stages, one CLI, plain files. Every command below runs from the repository root in any shell.

```
your Chromium --store scrape--> Maintain/Storage/Shadow/   (gitignored)
                                       |
                                store publish
                                       v
                    Source/Content/Bookmark/<id>.json      (tracked)
                                       |
                                 pnpm run build
                                       v
                                    Target/                (gitignored)
```

## Preflight

```bash
node --version                            # >= 22.23.4 - Astro 7 refuses older
pnpm --version                            # >= 11
curl -s http://127.0.0.1:9222/json/version # JSON with a Protocol-Version
```

No answer on the last one means the browser is not exposing CDP. Relaunch the browser you are logged
into with `--remote-debugging-port=9222`. Do not start a second browser: it has no session, so every
page comes back logged out and the scrape quietly archives nothing.

## Setup

```bash
pnpm install
pnpm run Build                              # capital B: Maintain/Source -> Maintain/Target
pnpm maintain config init                   # writes the map from the tracked example
pnpm maintain config init --force --profile <handle> --list <slug>=<list-id>
pnpm maintain config show                   # ids masked; --reveal prints them
```

`pnpm maintain` is `node Maintain/Target/Index.js`, so it does not exist until `pnpm run Build` has
run. `pnpm run build` (lowercase) builds the site instead - the two scripts differ only by case and
are not interchangeable.

The map is `Maintain/Configuration/Local/Configuration.local.json`: gitignored, mode `0600`.
`MAINTAIN_CONFIG` points one command at a different file; `MAINTAIN_CDP_PORT` overrides the port.

## Ingest

```bash
pnpm maintain store scrape --source bookmark   # bookmark | like | history
pnpm maintain store status                     # shadow vs public counts
pnpm maintain store publish --all              # or --id / --source / --since
pnpm run build
pnpm run Run                                   # dev server, port 9999
```

`store scrape` writes only under `Maintain/Storage/`. `store publish` is the only command that
writes `Source/Content/`. A second scrape of the same page prints `"new": 0` - identity is the
status id, so a rising `new` means the scrape fell back to reading text. `store publish` on an empty
shadow store fails `no-post` (exit 2): the scrape found nothing, so check the browser and the login
before the configuration.

## Lists are configuration

A slug is your word for a list; no code enumerates them.

```json
{
	"lists": [{ "slug": "alpha", "name": "Alpha", "id": "<list-id>" }]
}
```

`--list alpha=<list-id>` writes `name` equal to the slug; edit the file for a longer label. The site
groups posts by the slugs in `Source/Content/Bookmark/<id>.json` and files the rest under
`Unsorted`. An unconfigured slug fails `unknown-list` and the object names the configured set:

```json
{
	"error": "unknown-list",
	"detail": "\"nope\" is not configured; configured lists: alpha",
	"configured": ["alpha"]
}
```

## Acting on posts

```bash
pnpm maintain tab list --json                       # {"tabs":[{id,title,url,active}]}
pnpm maintain post like --url <permalink> --dry-run # resolve only
pnpm maintain post like --url <permalink>           # act
pnpm maintain page list open --name <slug>          # id comes from the map
pnpm maintain page list member add --name <slug> --handle <handle>  # dry run
pnpm maintain author distribute apply               # plan only
```

`post like` / `post bookmark add` read the control's state first, so a second run reports
`was: true` and clicks nothing. `page list member add` and `author distribute apply` change nothing
without `--apply`.

## Discover the surface

```bash
pnpm maintain --help
pnpm maintain store publish --help
pnpm maintain store publish --schema
```

Help and schema are rendered from the table the parser matches against, so they cannot drift from
what runs. Every command prints one JSON object and exits `0` or `2`; `--json` is implied when
stdout is not a TTY.

## Failure codes

| `error`           | Meaning                                       | Next step                                    |
| ----------------- | --------------------------------------------- | -------------------------------------------- |
| `no-config`       | the identifier map is missing                 | run the `copy` command it prints             |
| `config-exists`   | `config init` would overwrite an existing map | add `--force` if replacing it is intended    |
| `unknown-list`    | a slug is not declared in the map             | `config init --force --list <slug>=<id>`     |
| `schema-invalid`  | the map or a content file has the wrong shape | read `field` and `reason`; fix the file      |
| `cdp-unreachable` | nothing is listening on the DevTools port     | relaunch the logged-in browser with the flag |
| `no-post`         | the shadow store matched nothing              | scrape before publishing                     |
| `no-tab`          | no tab matched the target                     | `tab list`, then target by `id`              |
| `usage`           | argv does not match the command               | re-read `--help`                             |
| `rate-limited`    | the site refused a write                      | stop and retry later                         |

## Pitfalls

- **A click is not a write.** The control flips in the DOM before the request lands, so closing the
  tab in that window drops the mutation. The CLI waits for network quiet and re-reads the server
  state before printing.
- **Two debuggers, one tab.** A browser extension can hold its own debugger on a tab; attaching over
  CDP to that tab detaches it. Resolve targets by url and skip the tab that is already attached.
- **A redirect is not a failed navigation.** `/i/bookmarks` can land on `/i/history`, so navigation
  is confirmed by the page's load event, not by the requested url prefix.
- **The archive has no `bookmarkedAt`.** The interface never exposes when a post was saved.
  `firstSeenAt` is the first scrape that saw it: a lower bound, never the save time.
- **`hidden` is a tombstone, not a delete.** It survives re-scrapes and blocks publish. There is no
  unhide command; reversing it means editing the shadow record deliberately.
- **Content config follows `srcDir`.** This site sets `srcDir: "./Source"`, so the content config is
  `Source/content.config.ts`. `pnpm exec astro sync` is the probe: it writes `.astro/content.d.ts`
  naming each collection, and one `.astro/collections/<name>.schema.json` per collection.
- **Build output is ignored, not tracked.** `Target/` and `Maintain/Target/` are both regenerated
  and both gitignored. A committed build publishes every post id the archive held.
- **Never write identifiers into a tracked file.** Handles, list ids and post ids belong in
  `Maintain/Configuration/Local/`. Docs use `<handle>`, `<slug>`, `<list-id>`.
- **The identifier rule covers the whole tree.** No tracked file names a person, a handle, a list id
  or a machine path. A published dependency scope is public rather than account data, so a hit on
  one is not a leak; narrowing the review to `Source/`, `Documentation/` and `README.md` would be
  the wrong fix, because it stops covering `Maintain/` and `.github/`, exactly where a stray
  identifier lands. `Documentation/README.md` records the decision.

## Claim → test

| Claim                         | Test                                                                        |
| ----------------------------- | --------------------------------------------------------------------------- |
| Browser exposes CDP           | `curl -s http://127.0.0.1:9222/json/version`                                |
| The CLI is built              | `pnpm run Build` → `Maintain/Target/Index.js` exists                        |
| Command surface is described  | `pnpm maintain store publish --schema`                                      |
| Onboarding is non-interactive | `pnpm maintain config init` writes a map with no prompt                     |
| An existing map is protected  | second `config init` without `--force` → `config-exists`, exit 2            |
| Ids are masked by default     | `config show` → `"id": "*…"`; `--reveal` prints the id                      |
| Slugs come from the map       | `config init --force --list alpha=1`, then `config show` lists `alpha`      |
| An unknown slug is named      | `page list open --name nope` → `unknown-list` with `configured`             |
| Scrape is idempotent          | run twice; second prints `new: 0`                                           |
| Scrape publishes nothing      | after `store scrape`, `git status --short Source/Content` is empty          |
| Shadow store is untracked     | `git check-ignore -v Maintain/Storage/Shadow/Post/<id>.json`                |
| Site builds                   | `pnpm run build` → `Target/index.html`, `Target/Bookmark/index.html`        |
| Save time is not fabricated   | the detail page says "Saved at or after"; no `bookmarkedAt` field           |
| No tracked file names an id   | review the diff: no handle, list id, post id or home path in a tracked file |
