---
name: libgen-safe-book-browser
description: Use when searching or opening LibGen book search/detail pages through Chrome/CDP, selecting best book candidates by exact metadata and PDF > EPUB > other format preference, and preventing ad or Trip.com redirects with request interception.
triggers:
  - libgen redirect
  - Trip.com redirect
  - open libgen
  - book candidate selection
  - PDF EPUB preference
  - no redirect browser
tools:
  - run_command
  - read_file
  - search_files
---

# LibGen Safe Book Browser

## Core Rules

Use this skill for visible LibGen search/detail-page work where ads or redirect
scripts may hijack tabs. Prefer bibliographic/detail pages. Do not open mirror
or final download pages unless the user explicitly frames the work as lawful
public-domain/open-license material.

Candidate choice:

1. Prefer exact title, author, language, and edition/volume matches.
2. If quality is comparable, prefer `PDF > EPUB > other`.
3. Reject unrelated bundles, summaries, study guides, wrong languages, and weak
   title-only matches unless no better candidate exists.

## Candidate Discovery

Use the LibGen API before opening many tabs:

```bash
python3 - <<'PY'
import requests, urllib.parse
q = "Victor Hugo Les Miserables Hapgood"
url = "https://libgen.pw/api/search/by-params?query=" + urllib.parse.quote_plus(q) + "&collection=libgen&from=0"
books = requests.get(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}, timeout=30).json()["result"]["books"]
for b in books[:20]:
    print(b.get("id"), b.get("title"), b.get("author"), b.get("year"), b.get("language"), b.get("fileExtension"), b.get("fileSize"))
PY
```

If direct Python HTTP receives `403 Forbidden`, switch to browser-context API
search through Chrome/CDP. This runs `fetch()` inside an already loaded LibGen
tab and returns the hidden book IDs behind Vue result cards:

```bash
python3 skills/libgen-safe-book-browser/scripts/libgen_browser_context_search.py \
  --cdp-url $XYQ_CDP_URL \
  --language jpn \
  --title-term "レ・ミゼラブル" \
  --author-term "ユーゴー" \
  "レ・ミゼラブル"
```

Use the scored `https://libgen.pw/book/<id>` output as the candidate detail
page. Avoid relying on DOM `.click()` for LibGen result cards; the cards may not
have direct anchors and programmatic clicks may not trigger Vue routing.

The search helper uses a disposable `about:blank` tab by default and closes it
after disabling request interception. This prevents a killed run from leaving a
visible LibGen tab paused. Use `--reuse-tab` only when explicitly debugging an
existing tab.

Search is non-destructive: it does not close existing tabs. The legacy cleanup
path requires the explicit `--close-ad-targets` option.

The detail-page opener also disables `Fetch` in a `finally` cleanup before
detaching. Let it finish its guard interval when possible; cleanup is still
attempted on load errors or other controlled exits.

Open selected detail URLs with the bundled redirect guard:

```bash
python3 skills/libgen-safe-book-browser/scripts/libgen_no_redirect_open.py \
  --cdp-url $XYQ_CDP_URL \
  --guard-seconds 600 \
  --label "Les Miserables EN" https://libgen.pw/book/113160300
```

The redirect guard allows `libgen.pw`, `libgen.li`, `libgen.fyi`,
`libgen.stream`, and `freescienceengineering.org` by default. The last host is
a selectable mirror that can sometimes redirect; treat the later off-list
navigation as the ad, not the mirror tab itself.

The guard keeps top-level navigation restricted to LibGen hosts, but allows
required static render resources from `cdn.jsdelivr.net` and `code.jquery.com`
by default. This prevents the common half-rendered page state where the HTML
loads but Bootstrap CSS/JQuery are missing. Add `--allowed-resource-host` only
for another trusted static host that is needed for page rendering.

For long manual sessions, run the persistent companion instead of relying on a
one-shot guard interval:

```bash
python3 skills/libgen-safe-book-browser/scripts/libgen_persistent_guard.py \
  --cdp-url $XYQ_CDP_URL
```

It attaches to existing and newly opened allowed tabs, blocks off-list
requests, and restores tabs after delayed off-site navigation. It does not
close tabs by default. Navigation hosts and static resource hosts are separate:
CDN hosts can load CSS/JS but can never become a top-level destination.

If an existing tab looks half-loaded, reload and verify it instead of just
checking `document.body` text:

```bash
python3 skills/libgen-safe-book-browser/scripts/libgen_reload_verify_tabs.py \
  --cdp-url $XYQ_CDP_URL \
  --url "https://libgen.li/edition.php?id=138479359"
```

The reload verifier supports both `libgen.pw` Vue detail pages and classic
`libgen.li` pages. It checks `document.readyState` and real body text; for
`libgen.li`, it also verifies declared Bootstrap and JQuery resources. Concise
`libgen.pw` records require the exact title plus format metadata on book pages,
or the exact title plus `Get`/`Libgen` controls on links pages. Use
`--verify-only` to audit current DOM state without reloading already good tabs.

## Browser Setup

Use an existing Chrome only if it has a CDP endpoint:

```bash
curl $XYQ_CDP_URL/json/version
```

Otherwise launch a controlled browser:

```bash
google-chrome \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --no-first-run \
  --no-default-browser-check
```

If a tab is already hijacked, reopen its intended page under the redirect
guard. The guard preserves the target and prevents or reverses later Trip/ad
navigation instead of closing the tab. Use `--close-ad-targets` only when the
user explicitly requests destructive cleanup.

## Known Japanese Test Outcomes

For the five-book Japanese LibGen check, exact detail candidates were found for:

```text
嵐が丘（上）: https://libgen.pw/book/98203289
レ・ミゼラブル 全巻セット: https://libgen.pw/book/107073063
```

No strong exact Japanese detail candidate was found for `百年の孤独`,
`モンテ・クリスト伯`, or `ノートルダム・ド・パリ`; open the exact Japanese
search pages instead of unrelated results.

## Completion Evidence

Report the exact LibGen detail URLs opened and the selected candidate reason
when relevant, for example:

```text
Opened EN PDF: Les Misérables - https://libgen.pw/book/113160300
Opened ZH PDF: 悲惨世界（上、下）【文字版】 - https://libgen.pw/book/113867689
```

If local files were downloaded by the user and need organization, copy rather
than move them into topic/work folders such as
`resources/curated-books/world-literature/hugo-les-miserables/`.
