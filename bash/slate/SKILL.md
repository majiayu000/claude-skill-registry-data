---
name: slate
description: Create and publish standalone HTML artifacts through private Slate drafts, and read or manage existing drafts. Use for any HTML report, lesson, document, visual artifact, or preview that is not source code owned by a project.
---

# Slate

Slate is a private-by-default service and CLI for publishing static HTML drafts. Each upload returns a stable URL; re-uploading the same file publishes a new version at the same URL. Drafts are only readable by their owner unless uploaded with `--public`.

## HTML artifact owner

Slate is the only delivery path for standalone HTML artifacts. Reports,
lessons, generated documents, visual summaries, and one-off previews all use
this skill. A temporary local HTML file may exist only as upload staging or as
the fallback described below. Do not return a local path when Slate succeeds.

This does not apply to HTML that is source code inside a website or
application repository. Keep that source in the project and use its normal
build and deployment path.

Uploading is an external write. Read-only auth checks and local staging do not
authorize it. If the current request does not explicitly authorize publishing,
ask immediately before `slate upload`. Keep the draft private unless the user
explicitly requests public access.

If Slate is unavailable, unauthenticated, or the user requests local-only
output, keep the complete HTML in the OS temp directory and return that path.
State why Slate was not used. Do not silently choose local delivery.

## Auth check

Before any write (upload, disable, delete) or listing, verify auth:

```bash
slate whoami
```

If the `slate` command is missing, run it via the repo instead: `npx github:satyasaibhushan/Slate whoami` (same for all other commands). If whoami shows no authenticated account, do not attempt to log in or set keys. For a new HTML artifact, use the declared local fallback and tell the user Slate needs `slate auth set <key>`. For reads or management of an existing draft, stop because there is no authorized fallback.

## Reading drafts

Read drafts with `curl` only. Never use a browser, computer use, or any other web-fetching tool for Slate URLs — draft URLs serve the uploaded HTML byte-for-byte with no wrapper page, so `curl` always returns the full content.

Strip any trailing slash and append `/raw` unless the URL already ends in `/raw` (an alias for the same bytes, kept as the canonical agent URL). Most drafts are private, so send the owner's API key:

```bash
curl -fsSL -H "Authorization: Bearer ${SLATE_API_KEY:-$(python3 -c "import json;print(json.load(open('$HOME/.slate/credentials.json'))['apiKey'])")}" <draft-url>/raw
```

Public drafts also work without the header. A 401 means the draft is private and the key doesn't own it; a 404 means it doesn't exist or was disabled/deleted. Report the actual status or network error — do not fall back to web search or a browser.

To check metadata without the body, read the response headers (`X-Slate-Draft-Id`, `X-Slate-Draft-Version`):

```bash
curl -fsSI -H "Authorization: Bearer $SLATE_API_KEY" <draft-url>
```

## Writing drafts

Create a complete static HTML document in the OS temp directory, then upload
it after the external-write approval gate:

```bash
slate upload ./draft.html --description "short label"
```

Return the stable Slate URL after a successful upload.

- Re-running `upload` for the same file creates a new version of the existing draft; pass `--new` to force a separate new draft instead.
- `--description` sets or updates the draft's label; omitting it leaves the existing label untouched.
- Visibility: drafts are **private** by default (owner-only). Pass `--public` only when the user explicitly asks for a shareable/public link; pass `--private` to flip a public draft back. Omitting both keeps the draft's current visibility.

Author drafts as complete static HTML documents: semantic HTML, inline CSS or a `<style>` block, links to ordinary HTTPS pages, and images from HTTPS or data URLs. Do not include:

- JavaScript of any kind — `<script>` tags, inline event handlers, `javascript:` URLs. The upload API rejects most of these, and the serving CSP (`script-src 'none'`) blocks execution of the rest, so any JS is dead weight.
- Forms, iframes/embeds/objects, or meta-refresh redirects (rejected at upload time).
- Secrets, tokens, private URLs, or local filesystem paths.

### Privacy

Private drafts are readable only with the owner's API key or a signed-in web session, so work-in-progress content is fine by default. **Public** drafts are readable by anyone with the URL — before using `--public`, make sure the content contains nothing from work repositories, no user data, credentials, or internal details. If in doubt, keep it private or ask.

## Managing drafts

```bash
slate list                      # account's drafts: repo, version, visibility, updated
slate disable <draft-id>        # stop serving (URL returns 404); --reason "why"
slate delete <draft-id>         # soft-delete the draft
```

Only disable or delete a draft when the user asks for it.
