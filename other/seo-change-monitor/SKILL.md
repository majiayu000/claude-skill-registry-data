---
name: seo-change-monitor
description: Catch SEO regressions after a deploy by snapshotting key URLs (status, redirects, canonical, robots, titles, schema, hreflang, robots.txt, sitemaps) and diffing against a saved baseline. Use for "did the release break SEO", "monitor SEO changes", "add an SEO check to CI" or before and after a launch.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/seo-change-monitor
---

# SEO change monitor

Takes a snapshot of the SEO signals on a site's most important URLs, keeps it with the project as a baseline, and compares a fresh snapshot after every release. Hands back a prioritised list of what changed, a Search Console watch list for the weeks after the release, a pre-release checklist, and a small script that can fail a CI job when a release would hurt search.

> **Romeo's rule:** Most traffic drops after a release come from one boring line (a noindex, a canonical, a robots.txt rule), so check the boring lines every time and catch them before Google does.

## Use this when

- A redesign, replatform, theme change, CMS or plugin update, or framework upgrade is about to ship and nobody has a record of the current SEO state.
- Someone asks "did the release break SEO?" after a deploy.
- The team wants an automatic SEO gate in CI/CD.
- Indexing or traffic dropped and a recent release is the suspect.
- A staging build is being promoted to production and staging settings (noindex, `Disallow: /`) might come along.

## Don't use this for

- A full crawl-and-index audit of the site → `technical-seo-audit`
- Domain or URL moves that need a redirect map → `site-migration-check`
- Explaining a traffic change from Search Console data → `seo-performance-audit`
- Checking sitemap contents in depth → `xml-sitemap-check`

## What you need

### Required
- The key URLs, 20 to 200 of them, all on one host (see step 1).
- Where the baseline lives in the project, e.g. `seo/baseline.json` committed to the repo.
- The release: what shipped, to which environment, and when.

### Helpful
- Search Console access: Page indexing, Performance, Crawl stats, URL Inspection, and permission to add annotations.
- A staging or preview URL, and the CI system in use (GitHub Actions, GitLab CI or similar).
- A crawler with crawl comparison (Screaming Frog, Sitebulb) for full-site diffs on big releases.
- Python 3.8 or newer for the script (standard library only).

### No tools?
Make the snapshot by hand in a spreadsheet: one row per URL, one column per field from step 2. Read status codes, redirects and the `X-Robots-Tag` header in the browser's DevTools Network tab, and everything else in view-source. Save `/robots.txt` as text and note the sitemap URL count. After the release, fill a second sheet the same way and compare the two side by side. Search Console's URL Inspection shows what Google itself sees for any single URL.

## Ground rules

- Snapshot what crawlers receive: status, headers and raw HTML. On client-rendered sites the raw HTML may be nearly empty; compare the rendered page too (URL Inspection live test or a headless browser).
- Compare like with like: production against a production baseline, staging against a staging baseline. Staging is often noindexed on purpose; the alarm is when that setting reaches production.
- Choose URLs by template as well as by traffic. One broken template breaks thousands of pages, and one URL per template catches it.
- Severity follows consequence, not size of the code change. A one-character robots.txt edit that blocks the shop is `Fix now`; a rewritten article is not.
- An intended change is not a regression. Re-baseline deliberately, after someone confirms the change, never automatically on every run (that hides the regressions you built this to catch).
- Remove noise rather than ignoring alerts: exclude A/B-tested or personalised URLs, and allowlist the monitor's user agent in bot protection so it doesn't record 403s.
- Search Console lags by days; the snapshot catches problems within minutes. Use both.
- Read-only: the monitor fetches pages and reports. It never edits robots.txt, code, CMS settings or Search Console.

## Steps

1. **Pick the key URLs.**
   - Homepage; the top 20 to 50 landing pages by organic clicks (Search Console Performance → Pages, last 3 months); one or two URLs per template (category, product, article, location, docs); every page that carries revenue or leads; a couple of hreflang alternates.
   - Add a control set: one URL that should stay noindexed (e.g. `/cart` or `/search`) and one that should redirect. If either starts behaving like a normal page, the diff reports a `noindex` or `final_url` change.
   - Save as `seo/urls.txt`, one URL per line, `#` for comments. The script reads robots.txt and sitemaps from the first URL's host, so keep one file per host.
2. **Know what is captured.**
   - Per URL: HTTP status, final URL after redirects, canonical, meta robots (`robots` and `googlebot`), `X-Robots-Tag` header, title, H1s, meta description, visible word count, internal link count, structured-data types (every `@type` in JSON-LD, nested ones included), hreflang map.
   - Per site: robots.txt status and contents, total URLs across the sitemaps listed in robots.txt (or `/sitemap.xml`).
   - Not captured: rendered DOM, individual redirect hops, Core Web Vitals, Open Graph tags, microdata or RDFa, where internal links point. Check those separately when a release touches them.
3. **Take the baseline.**
   - Run `snap` against production before the release and commit the JSON next to the URL list, with the deployed commit or version in the commit message.
   - Re-take it when the URL list changes or the script is updated; older snapshots may lack fields.
4. **Apply the severity rules.**
   - `Fix now`: indexable page now `noindex` (meta tag or header, `none` included); canonical now pointing to a different URL; status 200 now 4xx, 5xx or unreachable; robots.txt gains a `Disallow` rule for all crawlers (`*`), Googlebot or Bingbot; robots.txt now returns 5xx or can't be fetched (Google treats that as "don't crawl" for a while; check current Google documentation for the timings); sitemaps now list zero URLs.
   - `Fix next`: title or H1 changed; structured-data types removed (a JSON-LD block that stops parsing loses its types too); final URL changed (a new redirect, treat as `Fix now` when it lands on the homepage or an unrelated page); canonical removed; hreflang changed; internal links down more than 30% (a lost menu or footer); sitemap URL count down more than 10%; word count changed more than 30%; a page that lost its `noindex` (a cart, search or staging page about to be indexed); a key URL missing from the new snapshot; a new robots.txt `Disallow` for any other crawler; an `Allow` rule removed.
   - `Worth doing`: meta description changed. Check it's intended and not a template default.
   - `Leave it`: word count drift of 10 to 30%, which is normal for dates, prices and rotating blocks.
   - The script compares robots.txt rules per `User-agent` group, so a `Disallow: /` that moves from one AI crawler's group into `User-agent: *` is caught. A new rule for another crawler (an AI bot, say) is `Fix next`: confirm it was intended, then re-take the baseline.
5. **Run the script.** Save the block below as `seo/seo_snapshot.py` (standard library only, Python 3.8+). It sits outside the list on purpose, so it copies without stray indentation.

```python
"""Usage: seo_snapshot.py snap urls.txt > new.json | seo_snapshot.py diff old.json new.json (exit 1 on Fix now)"""
import gzip, json, re, sys, urllib.error, urllib.parse as up, urllib.request; from html import unescape
def get(url):
    try: r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "seo-change-monitor/3"}), timeout=20)
    except urllib.error.HTTPError as e: r = e
    except OSError as e: return 0, url, "", str(e)
    b = r.read(); b = gzip.decompress(b) if b[:2] == b"\x1f\x8b" else b
    return r.getcode(), r.geturl(), ", ".join(r.headers.get_all("X-Robots-Tag") or []).lower(), b.decode("utf-8", "replace")
def text(html): return " ".join(unescape(re.sub(r"<[^>]+>", " ", html)).split())
def jsonld(blob):  # every @type in the blob, nested ones included (Offer, PostalAddress, ...)
    found = []; grab = lambda d: found.extend(d["@type"] if isinstance(d.get("@type"), list) else [d.get("@type")]) or d
    try: json.loads(blob, object_hook=grab)
    except ValueError: return ["INVALID_JSON-LD"]
    return [str(t) for t in found if t]
def page(url):
    code, final, x_robots, html = get(url); attr = r"""([\w:-]+)\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)"""
    tags = [(t.lower(), {k.lower(): unescape(v.strip("\"'")).strip() for k, v in re.findall(attr, raw)})
            for t, raw in re.findall(r"(?is)<(meta|link|a)\s([^>]*)>", re.sub(r"(?is)<script\b.*?</script>", " ", html))]
    full, host = lambda a: up.urljoin(final, a.get("href", "")), up.urlsplit(final).netloc
    meta = {a.get("name", "").lower(): a.get("content", "") for t, a in tags if t == "meta"}
    links = [(a.get("rel", "").lower().split(), a) for t, a in tags if t == "link"]
    robots = " ".join(a.get("content", "") for t, a in tags if t == "meta" and a.get("name", "").lower() in ("robots", "googlebot")).lower()
    body = re.sub(r"(?is)<(head|script|style|noscript|template)\b.*?</\1>", " ", html)
    return dict(status=code, final_url=final, robots=robots, x_robots=x_robots, description=meta.get("description"),
        noindex=bool(re.search(r"(?<![\w:-])(noindex|none)\b", robots + " " + x_robots)),
        title=text("".join(re.findall(r"(?is)<title[^>]*>(.*?)</title>", html)[:1])),
        h1=[text(h) for h in re.findall(r"(?is)<h1\b[^>]*>(.*?)</h1>", html)], words=len(re.findall(r"\w+", text(body))),
        canonical=next((full(a) for rel, a in links if "canonical" in rel), None),
        hreflang={a["hreflang"].lower(): full(a) for rel, a in links if "alternate" in rel and "hreflang" in a},
        internal_links=sum(up.urlsplit(full(a)).netloc == host for t, a in tags if t == "a" and a.get("href", "")[:1] not in "#"),
        schema=sorted({t for s in re.findall(r"(?is)<script[^>]*ld\+json[^>]*>(.*?)</script>", html) for t in jsonld(s)}))
def sitemap_count(url, depth=0):  # follows one level of sitemap index; reads .xml.gz too
    xml = get(url)[3]; locs = [unescape(l) for l in re.findall(r"<loc>\s*(.*?)\s*</loc>", xml)]
    return sum(sitemap_count(l, 1) for l in locs) if "<sitemapindex" in xml and depth == 0 else len(locs)
def snap(urls):
    origin = "{0.scheme}://{0.netloc}".format(up.urlsplit(urls[0])); code, _, _, txt = get(origin + "/robots.txt")
    txt = txt if code == 200 else ""; maps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", txt) or [origin + "/sitemap.xml"]
    return dict(robots_status=code, robots_txt=txt, sitemap_urls=sum(map(sitemap_count, maps)), pages={u: page(u) for u in urls})
def rules(t):  # {"googlebot|disallow:/x", ...}: every rule keyed by each user-agent in its group
    out, agents, in_rules = set(), [], False
    for l in t.splitlines():
        k, _, v = re.sub(r"\s+", "", l.split("#")[0]).lower().partition(":")
        if k == "user-agent": agents, in_rules = ([] if in_rules else agents) + [v], False
        elif k in ("allow", "disallow"): in_rules = True; out |= {f"{ua}|{k}:{v}" for ua in agents}
    return out
def diff(a, b):
    out, bad, site = [], lambda c: c == 0 or c >= 500, lambda lvl, k, old, new: out.append((lvl, "site", k, old, new))
    for r in sorted(rules(b["robots_txt"]) - rules(a["robots_txt"])):  # a Disallow for *, Googlebot or Bingbot can hide the site
        ua, rule = r.split("|", 1); rule != "disallow:" and rule.startswith("dis") and site("Fix now" if ua in ("*", "googlebot", "bingbot") else "Fix next", "robots.txt new rule", "", r)
    for r in sorted(r for r in rules(a["robots_txt"]) - rules(b["robots_txt"]) if "|allow:" in r): site("Fix next", "robots.txt allow removed", r, "")
    if bad(b["robots_status"]) > bad(a["robots_status"]): site("Fix now", "robots.txt status", a["robots_status"], b["robots_status"])
    if (sm := (a["sitemap_urls"], b["sitemap_urls"]))[1] < 0.9 * sm[0]: site("Fix next" if sm[1] else "Fix now", "sitemap URLs", *sm)
    for u, o in a["pages"].items():
        if not (n := b["pages"].get(u)): out.append(("Fix next", u, "page", "in baseline", "missing")); continue
        f = lambda lvl, k, old=None, new=None: out.append((lvl, u, k, o[k] if old is None else old, n[k] if new is None else new))
        if o["status"] == 200 != n["status"]: f("Fix now", "status")
        if n["noindex"] != o["noindex"]: f("Fix now" if n["noindex"] else "Fix next", "noindex")
        if n["canonical"] != o["canonical"]: f("Fix now" if n["canonical"] not in (None, n["final_url"]) else "Fix next", "canonical")
        for k in ("final_url", "title", "h1", "hreflang"): o[k] != n[k] and f("Fix next", k)
        if gone := sorted(set(o["schema"]) - set(n["schema"])): f("Fix next", "schema removed", gone, "")
        if n["internal_links"] < 0.7 * o["internal_links"]: f("Fix next", "internal_links")
        if n["description"] != o["description"]: f("Worth doing", "description")
        if (drift := abs(n["words"] - o["words"]) / max(o["words"], 1)) > 0.1: f("Fix next" if drift > 0.3 else "Leave it", "words")
    for row in sorted(out, key=lambda r: ["Fix now", "Fix next", "Worth doing", "Leave it"].index(r[0])): print(" | ".join(map(str, row)))
    return int(any(r[0] == "Fix now" for r in out))
cmd, args = (sys.argv[1:] or ["help"])[0], sys.argv[2:]
if cmd == "snap": print(json.dumps(snap([l.strip() for l in open(args[0]) if l.strip()[:1] not in "#"]), indent=1))
else: sys.exit(diff(*(json.load(open(f)) for f in args)) if cmd == "diff" else __doc__)
```

   - Baseline: `python3 seo/seo_snapshot.py snap seo/urls.txt > seo/baseline.json`
   - After a release: `python3 seo/seo_snapshot.py snap seo/urls.txt > after.json && python3 seo/seo_snapshot.py diff seo/baseline.json after.json`
   - Output is one line per change, `priority | URL | field | before | after`, sorted `Fix now` first. Exit code 1 means at least one `Fix now`.
   - Limits: it reads raw HTML with regular expressions (consistent between runs, not a validator), doesn't run JavaScript, fetches one URL at a time with a 20-second timeout, and follows one level of sitemap index. It treats an `X-Robots-Tag` aimed at another crawler (`otherbot: noindex`) as a plain `noindex`, which errs on the side of a false alarm.
6. **Wire it into CI.**
   - To block a bad release, run it against the staging or preview deploy before promotion, with its own URL file (`seo/urls-staging.txt`) and its own baseline. Run it again right after the production deploy, compared with the production baseline, to alert.
   - GitHub Actions example step: `run: python3 seo/seo_snapshot.py snap seo/urls.txt > after.json && python3 seo/seo_snapshot.py diff seo/baseline.json after.json`. The non-zero exit fails the job; post the output to the PR or team channel.
   - Fail the job only on `Fix now`; report `Fix next` without blocking. Retry once before failing on status 0 (network errors) so a flaky connection doesn't block a deploy.
7. **Triage the diff.**
   - Confirm every `Fix now` by hand first: `curl -sI <url>`, view-source, or a URL Inspection live test. Rule out bot protection, a CDN error page or a timeout.
   - Find the cause in the release (commit, config, CMS setting, environment variable) and recommend a rollback or same-day hotfix. Drafting the fix is fine; applying it needs permission.
   - For intended changes, write down why, then re-baseline with a commit that says so.
8. **Watch Search Console after the release.**
   - On release day, add a custom annotation to the Performance chart (Search Console supports these) so everyone reading the data later sees the date.
   - Days 1 to 3: URL Inspection live test on 5 to 10 key URLs (indexing allowed, Google-selected canonical, rendered HTML), and the robots.txt report for fetch errors.
   - Weeks 1 to 4, Page indexing: watch "Excluded by 'noindex' tag", "Blocked by robots.txt", "Alternate page with proper canonical tag", "Not found (404)", "Server error (5xx)" and "Page with redirect" rising after the release date. Crawl stats: spikes in 5xx responses, 404s or response time.
   - Performance: compare 28 days after with 28 days before, same weekdays, by page and by query. Clicks and CTR down with steady impressions and position usually means the snippet changed (title rewritten, rich result lost). Impressions down means indexing or ranking; position down on one template points at that template.
   - Enhancement and Shopping reports (Product snippets, Merchant listings, Breadcrumbs): a falling valid-item count after the release is a structured-data regression.
   - Small sites with few clicks: compare the changed pages with a control group of unchanged pages before blaming the release.
9. **Pre-release checklist.**
   - robots.txt diffed in the pull request; no staging `Disallow: /` heading to production.
   - No `noindex` meta tag or `X-Robots-Tag` on production templates. Staging is protected with authentication, and any noindex switch is tied to an environment variable that is set correctly in production.
   - Canonicals use the production host and https, and are self-referencing on indexable pages.
   - Changed or removed URLs have 301s to their closest equivalent, without chains.
   - Titles, H1s and meta descriptions on every template, not falling back to the site name or a placeholder.
   - Structured data present and valid on one URL per template (Rich Results Test, code input works for staging).
   - Sitemaps generate, list only indexable 200 canonical URLs, and are referenced in robots.txt.
   - hreflang tags still link both ways; navigation and footer links present in the server HTML; no links to the staging host.
   - The script run against staging shows no `Fix now`, and a rollback plan exists.

## What to hand back

Fill this in after each comparison.

```markdown
## Summary
What I found: <one sentence>
What matters most: <one sentence>
What to do first: <one sentence>

## Release
- What shipped: <version or commit>, <environment>, <date and time>
- Baseline: <file>, taken <date>, <environment>

## Changes
1. [Fix now] <plain-English problem> (<term>): <URL or "site">
   Before: <value>. After: <value>.
   Evidence: <seen | tool | inferred>, <high | medium | low> confidence. Confirmed by hand: <yes / no>
   Likely cause and fix: <commit, setting or template; rollback or hotfix>
2. ...
- Intended changes to re-baseline: <list, with who confirmed them>

## Search Console watch list
- <report and filter to check>, <date to check it>, <what would count as a problem>

## What I could not check
- <item>: <why>, and what would verify it
```

## Stop and flag if

- A `Fix now` change is live on production. Report it immediately with the evidence and recommend rollback or a hotfix; don't touch code, robots.txt or the CMS without explicit permission.
- There is no baseline, or it comes from another environment or an older script version. Take a new one, and say clearly that it can't reveal regressions already live.
- Fetches come back as 403, 429 or challenge pages. The comparison is unreliable until the monitor's user agent is allowlisted.
- Raw HTML is nearly empty because the site renders in the browser. Word count, H1 and link results mean nothing; switch to rendered checks.
- The output claims "no regressions" without a baseline, re-baselines automatically, or estimates traffic impact without Search Console data. That output is unacceptable.

## Next step

- `technical-seo-audit` on any template that produced a `Fix now`, to find related damage.
- `seo-performance-audit` 4 weeks after the release, with Search Console exports for the 28 days before and after.
- `xml-sitemap-check` if the sitemap URL count changed.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
