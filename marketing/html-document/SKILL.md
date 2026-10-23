---
name: html-document
description: "Use when creating or changing the shell of a web page or app (the root HTML template, the layout, the head), or before launching a site: doctype, character encoding, viewport, language and direction, head integrity, favicons, a real 404 page, the no-script message and validity of the rendered HTML."
paths: "**/*.html, **/index.html, **/app.vue, **/layouts/**, **/_document.*, **/_app.*"
---

# html-document

Step 6 of the pipeline (`WORKFLOW.md`). The few lines at the top of every page that everything else
assumes: get them wrong and the failure shows up elsewhere, as a layout that differs between browsers, text
that turns into symbols, a canonical tag nobody reads or a missing page that answers 200. The rules follow
the HTML Living Standard and are written for any framework or none. The title and description are
`skills/seo` §1; landmarks, headings and the skip link are `skills/accessibility` §1.

## When
A root template, layout or document shell is created or changed, a new site or app is bootstrapped, a
framework or build tool changes how the head is produced, or a launch checklist is run.

## Steps

1. **The first line is the doctype.** `<!doctype html>` before anything else, including comments and
   whitespace-producing template output. Without it browsers render in quirks mode, where box sizing and
   table behaviour differ from the standard and from each other.
2. **The encoding is declared early and agrees with the server.** `<meta charset="utf-8">` is the first
   element in the head and falls inside the first bytes of the document, where the standard says the
   browser looks for it (HTML Living Standard, the `meta` charset declaration). If the `Content-Type`
   header also names a charset it is the same one, because the header wins when they disagree. The file
   itself is saved in that encoding. Symptoms of getting it wrong are replacement characters and doubled
   accents.
3. **The viewport meta exists and does not block zoom.** `<meta name="viewport" content="width=device-width,
   initial-scale=1">`. Without it, mobile engines lay the page out on a wide virtual canvas and scale it
   down. Never add `user-scalable=no` or a `maximum-scale` that prevents zoom (`skills/accessibility`
   §3.10).
4. **Language and direction are on the root.** `lang` on `html` with a valid BCP 47 tag
   (`skills/accessibility` §1.11); `dir="rtl"` for right-to-left languages, set from the same locale
   source, and `dir="auto"` on elements that show user-written text whose direction is unknown. When a
   single-page app switches language without a reload, `lang` and `dir` on the root are updated with
   it. Alternate-language links are `skills/seo` §1.5; logical CSS properties are
   `skills/responsive-layout` step 28.
5. **Only head content lives in the head, and only meta lives there.** The parser closes the head at the
   first element that does not belong in it, such as a stray `div`, an invalid tag from a template bug or
   text, and every tag after that lands in the body: a canonical link, a robots directive or a social tag
   can be silently ignored. Conversely, a `meta`, `title` or `link` for the document inside the body is
   a defect. The check is on the parsed result of the rendered page, not on the template.
6. **Order the head for the parser.** Charset, viewport, title, then the resources that start downloads
   (stylesheets, preloads, fonts), then scripts with `defer` or `async` (`skills/webperf` §4.1, §4.3). A
   policy meta tag that must apply to everything after it comes before them.
7. **Declare icons deliberately.** Browsers request a default icon address when none is declared and log a
   missing file. Provide one icon in a format current browsers accept, declared with `rel="icon"`, plus
   a larger one for home-screen use (`rel="apple-touch-icon"`), and serve the default address or declare the
   others so it does not 404. One set per site, not one per template. A web app manifest and an offline
   worker are a separate decision for products that are installed; this block does not require them.
8. **The missing-page response is a real page with a real status.** Unknown paths return status 404 (410 for
   content removed on purpose), with the site's layout, a visible way back (home, search, main sections)
   and no dead-end. Redirecting every unknown path to the home page, or serving a "not found" body with
   status 200 (a soft 404, common with single-page apps whose server answers every path with the shell)
   misleads crawlers and tooling (`skills/seo` §5.3). A single-page app needs the server or the prerender
   step to know which paths exist, or a route-level 404 that is returned as a status.
9. **Say so when the page needs scripts.** Content a public page needs is in the served HTML (`skills/seo`
   §2.2); where an app truly cannot run without scripting, a `noscript` element in the body states
   that and what to enable, in the page's language. A `noscript` in the head may only hold `link`,
   `style` and `meta`. The message is a courtesy, not a substitute for serving content.
10. **The rendered HTML is valid.** Run an HTML conformance checker over the page as served, not over the
    template sources: the errors that matter are the ones that change the parse, such as unclosed or
    wrongly nested elements (an interactive element inside another, a block inside a paragraph, a list
    with direct children that are not items), duplicate identifiers (`skills/accessibility` §6.9) and
    misused attributes. Stylistic warnings are read and decided, not auto-fixed. Framework hydration
    warnings about mismatched markup are the same defects found at runtime.
11. **No comments, drafts or debug markup in the output.** The served HTML carries no template comments,
    no leftover conditional comments and no development-only elements (`CONVENTIONS.md`, the no-comment
    rule applies to templates).

## Output / checkpoint
No pipeline checkpoint: the findings go to the author of the shell. A launch checklist run records which of
the eleven points were checked on the served pages, not on the sources.

## Guardrails
- **Validate the served output.** A clean template proves nothing about what the framework emits.
- **A missing page never answers success** and never redirects blindly to the home page.
- **No zoom-blocking viewport value**, whatever the layout problem it hides (`skills/responsive-layout`).
- A check by pattern over source files finds hints; the parsed page is the authority.

## Mechanical checks

```
curl -s "$URL" | head -c 1024 | grep -i '<!doctype html'
curl -s "$URL" | head -c 1024 | grep -i 'charset'
curl -sI "$URL" | grep -i '^content-type'
curl -s "$URL" | grep -iE '<meta name="viewport"'
curl -s "$URL" | grep -ciE 'user-scalable=no|maximum-scale'
curl -s -o /dev/null -w '%{http_code}\n' "$URL/this-page-does-not-exist-xyz"
curl -sI "$URL/favicon.ico" | head -1
curl -s "$URL" | grep -iE 'rel="(icon|apple-touch-icon)"'
curl -s "$URL" | grep -iE '<html[^>]*\blang='
```

- The missing-page request must print 404; read the body for navigation.
- Parse the rendered page (a standard-library HTML parser is enough) and report any `meta`, `title` or
  `link rel=canonical` found inside the body, and any element between the first head tag and the first
  `meta`/`title` that is not allowed there.
- Run the project's HTML conformance checker over the served pages in the pipeline; it is a check run by
  the project, not a dependency of this block.
- Fetch the page with scripting disabled and confirm the expected content or the `noscript` message is
  present.

## Origin
The topic list comes from reading the public `Front-End-Checklist` repository (its README and package
metadata declare MIT; the repository carries no licence file, so only the list of topics was taken and no
sentence), on 2026-10-02. Every rule was written from the HTML Living Standard (the doctype, the encoding
declaration, the `meta`, `link`, `html` and `noscript` elements, and the parsing rules for the head),
RFC 9110 (status codes) and MDN, and the order-of-the-head point from web.dev's guidance on resource
loading. Not taken: a validity service as a required tool, an app manifest and offline worker (a PWA
decision for products that need installing, not a baseline for every page), and a specific favicon size
list (it changes with platforms; read the platform's current documentation). Written, not yet run on a
real launch.
