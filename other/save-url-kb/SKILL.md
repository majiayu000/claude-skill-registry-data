---
name: save-url-kb
description: >-
  Capture public or signed-in web content into a local Markdown knowledge base
  as an auditable source bundle with local assets. Use when the user asks to
  clip, save, scrape, or archive an article, social post or thread, GitHub or
  Discourse discussion, feed, inbox, private document, WhatsApp conversation,
  YouTube page, or another page already visible in their browser. Supports URL
  capture, the current signed-in tab, temporary browser-profile snapshots,
  saved HTML, media, evidence, honest completeness, and knowledge-base linking.
---

# Capture web content

Use the installed `wordcell` CLI. Check the available local routes when the capture may need a browser or optional media tools:

```sh
wordcell doctor
wordcell adapters
```

Resolve `<vault>` to the directory containing its authored or managed
`index.md` front door, then set
the shell-local `KB_ROOT` to that path (`KB_ROOT=kb` from a typical repository
root, or `KB_ROOT=.` from inside the vault). Pass `--output "$KB_ROOT/articles"`
to captures and read the vault's applicable agent instructions before writing.

## Pick the read surface

Start ordinary URL capture with the layered default:

```sh
wordcell clip https://example.com/article --output "$KB_ROOT/articles"
```

The command tries stable structured data, bounded HTTP extraction, and rendered-browser fallback as needed. If those routes produce no usable source material, URL capture may perform one read-only lookup for an existing Archive.today-family snapshot. It never submits the source for archival. A useful structured provider result, including a partial Hacker News result, remains authoritative over the archive fallback.

When the source is already open in a signed-in browser, read the current tab in place:

```sh
wordcell clip current --browser-live --output "$KB_ROOT/articles"
wordcell clip current --cdp 9222 --output "$KB_ROOT/articles"
```

For `--browser-live`, first enable Chrome's local debugging connection at `chrome://inspect/#remote-debugging` (Chrome 144+). If Chrome was launched with an explicit loopback debugging port, pass that numeric port to `--cdp` instead.

Current-tab capture derives the source URL from the attached tab. It does not navigate, click, type, submit, upload, or scroll that tab.

To open a URL with existing browser state, select a profile. A path-backed profile is copied into a temporary snapshot for the capture, so the source profile remains unchanged:

```sh
wordcell clip https://example.com/member/article --browser-profile "$KB_CAPTURE_PROFILE" --output "$KB_ROOT/articles"
```

Use cookie-backed HTTP when the page does not require browser-only local state, or import a page already saved from any browser:

```sh
wordcell clip https://example.com/member/article --cookie-source chrome --cookie-profile "Default" --output "$KB_ROOT/articles"
wordcell clip https://example.com/member/article --cookies-file "$KB_COOKIES_FILE" --output "$KB_ROOT/articles"
wordcell clip https://example.com/article --html "$KB_SAVED_HTML" --output "$KB_ROOT/articles"
wordcell clip https://example.com/article --html - --output "$KB_ROOT/articles" < page.html
```

Read [references/authentication.md](references/authentication.md) for current-tab, profile, cookie, and saved-page selection details.

## Keep the boundary ingestion-only

Capture reads source material. It never posts, likes, follows, sends, deletes, reacts, or submits. URL-based browser capture may navigate to the requested URL and scroll within fixed work limits, taking bounded observations as content is rendered; those operations exist only to reveal content for ingestion.

If a new surface needs support, add an extraction route, fixture coverage, or a generic rendered-page fallback. Do not add a write-capable provider integration to clipping.

## Choose scope and artifacts

```sh
wordcell clip https://example.com/post --scope page --output "$KB_ROOT/articles"
wordcell clip https://example.com/post --scope thread --output "$KB_ROOT/articles"
wordcell clip https://example.com/discussion --scope comments --output "$KB_ROOT/articles"
wordcell clip https://example.com/post --media none --output "$KB_ROOT/articles"
wordcell clip https://example.com/post --media all --output "$KB_ROOT/articles"
wordcell clip https://example.com/post --evidence source --output "$KB_ROOT/articles"
wordcell clip https://example.com/post --evidence all --output "$KB_ROOT/articles"
wordcell clip https://example.com/post --output "$KB_CAPTURE_OUTPUT"
wordcell clip https://example.com/post --force --output "$KB_ROOT/articles"
```

With the resolved output path, `wordcell clip` installs one atomic bundle under
`$KB_ROOT/articles/<slug>/`:

```text
<slug>/
  <slug>.md
  capture.json
  assets/
  evidence/       # only when requested
```

The Markdown is the readable source record. `capture.json` records the source and canonical URLs, acquisition attempts, selected extractor, status, counts, warnings, localized asset hashes, and requested evidence outcomes. A partial failure can preserve useful source text without overstating completeness.

The normal image route localizes inline images from ordinary pages and rendered
social posts, including X and LinkedIn, plus exposed video posters or
thumbnails. For YouTube, the default capture (unless `--media none`) asks
yt-dlp for the title, description, duration, channel, local thumbnail, and one
available exact-language transcript. `--media all` additionally localizes
accessible, non-DRM audio or video; the full payload is never downloaded by
default. Missing optional metadata or transcript regions remain explicit in
the capture status and warnings.

## Review X posts and threads

Use `--scope thread` for an X status URL even when the expected result is one long post. Preserve the complete root post or long-form article text, then distinguish same-author continuation posts from quoted posts and third-party replies. Do not flatten reply authorship or treat visible timeline neighbors as part of the requested thread.

When the caller wants a reusable or republished record, review the author's public profile surface as a separate source boundary. Record the display name, `@handle`, canonical profile URL, public bio exactly as exposed, and public external profile link when present. Treat a blank or unavailable bio as missing; never infer one from post prose. If the downstream record needs durable profile provenance, capture the canonical profile URL separately instead of editing the status capture.

Inspect localized X assets individually. Keep the root post's numbered photo assets distinct from the author avatar, profile banner, extractor-generated cover duplicates, quoted-post media, and third-party reply avatars or images. A media-tool warning does not mean normal inline photos are missing when those photos are already present in `assets/`; report the two artifact routes separately. Preserve `partial` whenever X does not expose a trustworthy item tree, even if the complete visible root post and its images were retained.

Source evidence is stored as sanitized inert HTML. Screenshots are viewport pixels and can include everything visible in the tab, so inspect them before retaining or sharing a bundle.

## Backfill saved-URL metadata

With KB installed, build the pinned Rust metadata-search helper and backfill every saved external URL into a separate tool-owned sidecar:

```sh
wordcell url-metadata tool build
wordcell url-metadata backfill --root "$KB_ROOT" --json
```

The backfill runs serially with bounded output and time, resumes compatible sidecars by default, and searches for exact source matches plus existing Archive.today-family snapshots. It never rewrites the saved Markdown or adopts the search library's URL normalization, accepts descriptive metadata only from an exact source match, records partial or failed engines literally, and never promotes search output into `capture.json`. Use `--refresh` for an explicit replacement run after reviewing the provider and archive disclosure policy.

## Report completeness literally

Read [references/platforms.md](references/platforms.md) when selecting or explaining a route. Use `wordcell adapters --json` when software needs the installed capability matrix.

Interpret status as follows:

- `complete`: the selected bounded representation has no known missing boundary.
- `partial`: useful content was retained, but a count, cursor, configured bound, hidden branch, unloaded region, or generic rendered representation prevents a completeness claim.
- `auth-required`: the selected routes reached a sign-in gate.
- `blocked`: the source returned a block or verification shell.
- `unsupported`: no route produced usable source material.

For page scope, item counts cover primary entries. For thread and comment scopes, they cover replies or comments and exclude the root, quotes, ancestors, and pagination markers. A rendered conversation can retain visible prose while reporting `capturedItems: 0` when the page does not expose a trustworthy item tree.

Preserve missing, deleted, blocked, cyclic, depth-limited, item-limited, and pagination-boundary states. Never upgrade a fallback to `complete` when declared counts, cursors, virtualization, or configured bounds disagree.

## Separate source from synthesis

Treat the captured Markdown and manifest as the source record. Put summaries, comparisons, decisions, and changing interpretations in a maintained note rather than rewriting the capture to match a later conclusion.

Connect the maintained note to the capture with an explicit wikilink. Let
`wordcell backlinks` derive incoming relationships; do not insert reciprocal links or
generated backlink sections into authored notes. After adding or linking a
capture, review the maintained note for reusable concepts and relationships,
then run the vault's normal refresh and check loop:

```sh
wordcell percolate "<maintained-note-id>" --root "$KB_ROOT" --limit 25 --json
wordcell refresh --root "$KB_ROOT"
wordcell check --root "$KB_ROOT"
```

## Review the result

1. Compare the Markdown, quoted context, counts, warnings, and assets with the source surface.
2. Confirm the manifest names the route that actually supplied the selected text.
3. Inspect requested screenshots, source evidence, and unexpectedly large assets.
4. Report what was captured, what remains partial, where the bundle was written, and which maintained note links to it.

When changing clipping behavior, add focused fixtures for the affected surface and run the public package checks plus a representative capture.
