---
name: browser-game-hosting
description: Get a self-contained HTML/JS browser game (or any static page) in front of a user so it actually runs, comparing Claude Artifacts, GitHub Pages, direct file sharing, and gist+preview — with the specific failure modes each one hits (login walls, private-repo limits, mobile preview sandboxing) and how to diagnose which one you're looking at. Use when asked to host, deploy, share, publish, or make a browser-based game/page accessible to a user, especially on mobile.
---

# Hosting a browser game

## Prerequisite: bundle as one self-contained file

Before picking a hosting option, inline everything — `<style>` and `<script>` directly in the HTML, no separate `.js`/`.css` files, no external requests (fonts, CDNs, APIs). This is a hard requirement for Claude Artifacts (strict CSP blocks external hosts) and removes an entire class of "works locally, breaks when shared" bugs for every other option too. A multi-file dev version is fine for local iteration; bundle before distributing.

## Options, in the order to reach for them

### 1. Claude Artifact — fastest, but has a login wall

Use the `Artifact` tool. Gives you a `claude.ai/code/artifact/{uuid}` URL instantly, runs JS properly (it's a real hosted page, not a preview).

**Catch:** the viewer must be logged into claude.ai to open it. This fails silently or bounces to a sign-in screen — and mobile sign-in flows (particularly Sign in with Apple) can get stuck for reasons outside your control. Good for: your own testing, or a recipient you know is already logged in on that device. Risky as the *only* channel to someone on a phone you can't debug interactively.

### 2. GitHub Pages — real no-login URL, but needs repo changes

Gives a plain `https://{owner}.github.io/{repo}/...` URL. No login, full JS execution, works everywhere.

**Requirements, both of which are real changes you need the user's sign-off on:**
- The repo must be **public**. If it's currently private, this is a visibility change — confirm with the user before flipping it (`private: true → false` isn't something to do silently, and check whether repo-scoped GitHub MCP tools even expose this — they often don't; if not, ask the user to do it in Settings).
- Pages must be **enabled** (Settings → Pages → source). Standard repo-scoped GitHub MCP tool access (file read/write, PRs, branches) typically does *not* include a "create Pages site" call — check what's actually available before promising this route works end-to-end without the user touching GitHub's UI themselves.

Best when: the user is fine with the repo being public, or it already is.

### 3. Send the file directly as a chat attachment — zero setup, but often sandboxed

Simplest thing to try, and sometimes it's enough. But many chat clients open HTML attachments in a lightweight preview (iOS Quick-Look-style) that renders CSS but **does not execute `<script>` tags** for security. Symptom: the page's static layout/styling shows up, but nothing is interactive and any JS-populated content (like a game board) is empty.

If a user reports "it opened but nothing happens" after you sent a file, this is almost always the cause — not a bug in the code. Fix: have them explicitly save the file (Save to Files / Downloads) and reopen it *from there* rather than the inline chat preview, which more often uses a full browser-grade renderer.

### 4. Gist + htmlpreview.github.io — no login, keeps the repo private, but manual

`https://htmlpreview.github.io/?<raw-file-url>` renders a raw HTML URL live with proper `Content-Type: text/html`, so scripts execute. Works with a public gist's raw URL.

**Catch:** you likely don't have a gist-creation tool (repo-scoped GitHub MCP access covers repo files, not the Gist API), so the user has to manually create the gist and paste the code themselves. Fine for small snippets; painful and error-prone past a couple hundred lines — say so up front rather than dumping a huge code block and hoping.

### 5. Local static server — for *your own* testing only, never a real delivery option

`python3 -m http.server` + a headless browser (Playwright/`chromium-cli`) is how *you* verify the game actually runs before shipping it — see the Verify section below. In an ephemeral remote/cloud execution container this is not reachable from the user's device (no inbound access), so never present a `localhost` URL as something for the user to open.

## Diagnose before switching options

Each hosting path fails in a *different, recognizable* way. Before jumping to a different option, get the user to describe exactly what they saw — it tells you which fix actually applies:

| Symptom | Likely cause | Fix |
|---|---|---|
| Link led to a claude.ai login/SSO screen | Artifact, viewer not authenticated | Get them logged into claude.ai on that device, or switch options |
| Page/file opened, static layout visible, nothing interactive, no dynamic content populated | Script execution blocked (sandboxed preview) | Open from Files/Downloads instead of inline preview, or switch options |
| 404 on a raw.githubusercontent.com / Pages URL | Repo is private | Confirm with user before making public, or use an option that doesn't need public hosting |
| Nothing happens when tapping a link at all | Could be anything — don't guess | Ask what app they're using to open it and what happens step by step |

## Verify before declaring it done

Don't hand over a link on faith. Before telling the user it's ready:
- Start a local static server and drive it with a headless browser (`chromium-cli`, or Playwright directly if that's unavailable — see the project's `run` skill for the pattern) to confirm the page actually renders and responds to input.
- For an Artifact or Pages URL specifically, `WebFetch` can load `claude.ai/code/artifact/{uuid}` URLs using your own claude.ai session — use that to confirm the artifact itself is live, though it can't tell you whether the *user's* login will succeed.
- Screenshot the result and actually look at it — a blank frame or unstyled dump is a failure to load, not a successful test.
