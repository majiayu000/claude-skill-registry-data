---
name: blinkpages
description: Work this site's BlinkPages queue — "blinkpages", "process the queue", "work my queued edits", "apply the edits I queued", "anything waiting from the editor?", "drain the queue", "/blinkpages", "$blinkpages". With no argument it takes each queued "Edit with AI" request and admin-console "New <type> with AI" / import-from-a-link content job in turn and delivers it as a previewable draft. You do NOT need this to change the site — to make a change, just say what you want, no command. Run it from inside this site's repository, in whichever AI coding tool you use, at whatever model you've selected.
argument-hint: "[--auto] — no argument works everything queued for this site"
---

<!--
  ════════════════════════════════════════════════════════════════════════════════════════════════
  CENTRALLY MANAGED — DO NOT EDIT THIS SKILL.
  It is owned by the BlinkPages platform and force-overwritten on every update; local changes here
  will be lost on the next sync. Want different or extra behavior? Create your OWN skill in a NEW
  directory under .claude/skills/<your-skill-name>/ (Claude Code) or .agents/skills/<your-skill-name>/
  (Codex and other agentskills.io tools) — those are yours and are never touched.
  This file is stamped, byte-identical, to BOTH .claude/skills/blinkpages/ and .agents/skills/blinkpages/.
  Source of truth: nsquared-team/blinkpages-platform → managed-skills/blinkpages/
  ════════════════════════════════════════════════════════════════════════════════════════════════
-->

# blinkpages — the BlinkPages command for THIS site

Type **`$blinkpages`** in Codex — the CLI, the IDE extension, or the ChatGPT desktop app — and
**`/blinkpages`** in Claude Code. Or just say *"work my queue"*: either tool will pick this up from the
description. Codex also lists skills under `/skills`, and some surfaces offer them in the `/` menu; if a
slash spelling answers "Unrecognized command", use `$blinkpages`. Same skill, same file.

**With no argument, this works the queue** — that is the default and, today, the whole of it. The queue holds
the changes the owner asked for from the in-page **"Edit with AI"** card, and the **"New <type> with AI"** /
import-from-a-link content jobs from the admin console. They wait in this site's own queue; nothing applies
them until someone runs this.

The name is deliberately broad. If BlinkPages later grows other per-site operations worth a command, they
become arguments here rather than a second skill and a third rename — but **the no-argument default stays the
queue**, because that is what an owner who types `/blinkpages` or `$blinkpages` after queueing an edit is asking for.

**You do not need this skill to change the site.** If the owner just says *"add a Black Friday banner"*, do it
— no command, no ceremony. The conventions are the same either way and they are already loaded — Claude Code
through the repo's `CLAUDE.md`, which imports `.claude/blinkpages.md` (draft-by-default, the preview link,
`writableRoots` and the rest); Codex and every other agent through the managed region at the top of `AGENTS.md`.
The full craft is `.claude/blinkpages-editing.md` — a plain Markdown file any tool can open (it lives under
`.claude/` for historical reasons only). This skill exists because a *queued* change needs claiming, fetching
and a status written back — not because editing needs a command.

It is **not** the editor, and it never reaches any other tenant, any shared queue, or any BlinkPages secret —
it only touches this repo, in place, pushing with **your** git identity.

**Model & effort are yours.** This runs at whatever model and reasoning effort you've selected in your AI tool —
nothing here forces a specific one. A big layout or multi-page job is worth a stronger model and higher effort;
a quick copy fix isn't.

## How to invoke

**Interactive is the default** — ask a follow-up whenever a queued request is genuinely ambiguous.

- **No argument** → the default: work the queue. List what's pending, then take each job in turn (**Drain
  your queued requests**, at the bottom). If the queue is empty, say so — don't go looking for something to do,
  and don't offer to invent work.
- **`--auto`** → run non-interactively: make a reasonable assumption instead of asking, and hard-stop only on a
  true blocker (see `.claude/blinkpages-editing.md`).

How you say it is the only thing that differs by tool. Whatever follows the name — `--auto`, or a description
of a change — is plain text in your message; there is no argument syntax to get right (`/blinkpages --auto` and
`$blinkpages --auto` mean the same thing).

If the owner describes a change while invoking this, that is not a queue job — just make the change directly,
following the same conventions.

The long `node …/queue.mjs list` command below is only the mechanism; invoking the skill runs the whole drain
flow for you.

## 1. Confirm you're inside one tenant repo

Find the single tenant marker and read your identity from it:

```bash
ls .migrate-to-astro/tenant.*.json
```

- **Exactly one match** → read it. Take `tenantId` and `github.writableRoots` (the roots you may write to,
  usually `public/` and `src/`). If the marker is missing, fall back to `wrangler.jsonc` for the worker name,
  but `writableRoots` then defaults to `["public/", "src/"]`.
- **Zero or many matches** → **stop.** You're not at the root of a single BlinkPages tenant repo. `cd` into
  the site you want to edit and re-run.

You do **not** clone anything and you do **not** need any token — you're already in the repo, authenticated
to push to it as yourself.

## 2. Understand the change

In interactive mode, the change is whatever you describe (in your message, or after the command in it).
If you queued an edit request from the in-page **Edit with AI** card and want to apply it here, paste that
prompt. Read it carefully; if it's genuinely ambiguous, ask before editing (in `--auto`, make a reasonable
assumption instead — see the methodology doc).

## 3. Make the edit

Follow **`.claude/blinkpages-editing.md`** — the shared editing craft: read the page
first, make the multi-file / layout / image edits, place/crop/optimize any images, and **stay inside
`writableRoots`**. Keep **one logical concern per commit**.

**Draft by default — protect the live site.** A *draft* is a `draft-<slug>/v1` branch + a regular **open** PR off
the live branch — never a GitHub draft-status PR (no `--draft`, ever; PRs stay ready to merge). A
*variation/option* is a sibling draft in the same `draft-<slug>/…` group, its PR **also off `main`** — never a
sub-PR off another draft. If the owner references an existing draft or option, commit on that branch. Everything
else is about the live site and becomes a **new draft** by default — even small text fixes. Commit straight to
the live branch only when the owner has explicitly confirmed they want to skip the preview (recommend the draft
first). Full rule, recipe, and how to build options: `.claude/blinkpages-editing.md` →
**Draft by default**, **The draft loop**, and **Multiple options**.

**Asked for multiple options ("a few variations", "three versions to choose from")?** Follow
**`.claude/blinkpages-editing.md` → "Multiple options: sibling drafts in a group"**: build
them as **flat siblings** in one `draft-<slug>/…` group — `draft-<slug>/v1`, `/v2`, … each a PR **`--base main`**
(`git checkout -b draft-<slug>/vN draft-<slug>/v1`, push, `gh pr create --base main`), never a sub-PR off another
draft. Each becomes its own preview in the editor's drafts list + compare view, clustered by folder; publishing
any one goes live and discards the rest. If you're on `main`, create `…/v1` first — don't pile options onto the
live branch.

**Images:** edit / replace / crop / restyle only — there is no image generator. If the change truly needs a
brand-new photo or raster, **stop** and add the image to the repo yourself (e.g. under `public/`), then
re-run referencing it. Never fabricate an image as a substitute. (Full rule: `.claude/blinkpages-editing.md`.)

**Check what the site already has before you add anything.** `ls public/assets/media` is *not* the
inventory — large files are stored in the site's media bucket, where they have **no local file** at all.
Ask for the real list:

```bash
node .blinkpages/queue.mjs media --q <term>     # add --kind image|video|audio|doc, --all for everything
```

A **bucket-only** file has no path on disk, but its `/assets/media/...` URL works on the live site and on
every preview: reference it by path in HTML/Markdown, and **never `import` one** via `astro:assets`, which
needs a file to exist. Never delete a reference just because the file is missing locally — for these that is
normal. Prefer reusing what is there over adding another copy. (If the command says this site's editor
doesn't list media yet, fall back to `ls public/assets/media`, knowing it will miss the bucket.)

## 4. Deliver it: commit → push → PR → preview link

Stage only files inside `writableRoots`, one logical concern per commit. Then route by where you are:

- **On a `draft-*` branch** (the editor pre-created it, or the owner pointed you at an existing draft/variation)
  → commit and push; the draft's open PR rebuilds its preview:

  ```bash
  git add <changed paths within writableRoots>
  git commit -m "blinkpages-ai: <short summary of the change>"
  git push
  ```

  If the branch somehow has **no open PR**, open one now (`gh pr create --base main` — every draft and option
  bases on `main`; a regular open PR, never `--draft`): without it there is no preview and the owner can't see
  the draft.

- **On the live branch (`main`)** → do **not** just push. Run **the draft loop** (full version with caveats:
  `.claude/blinkpages-editing.md` → **The draft loop**):

  ```bash
  git fetch origin && git checkout -b draft-<slug>/v1 origin/main   # foldered from birth (keep <slug> short)
  git add <changed paths> && git commit -m "blinkpages-ai: <what changed>"
  git push -u origin draft-<slug>/v1
  gh pr create --base main --head draft-<slug>/v1 \
    --title "<short human title — names the draft in the owner's editor>" \
    --body "<one-line plain-language summary>"      # a regular open PR — NEVER --draft
  gh pr checks draft-<slug>/v1 --watch
  gh pr view draft-<slug>/v1 --json comments \
    --jq '[.comments[].body | select(contains("pr-preview-summary"))] | last'
  ```

- **The owner explicitly confirmed a live edit** → commit and push on `main`; that triggers the production
  deploy. Tell the owner it's live.

**No `gh`, or not signed in** (common in a local Codex setup that has `git` only): push the branch anyway, then
**stop** and tell the owner to press **Create PR** in their AI tool — never hand back a bare branch as a draft;
without an open PR there is no preview. **No network at all** (a cloud task): you cannot push or read the queue —
follow `AGENTS.md` → **Delivering a draft** → **Route B** (commit only, then tell the owner what to press), and
never report the queue as empty when you could not look. Queued jobs are unaffected by the first case: their
branch and PR already exist, so they need only `git push`.

For drafts, the loop isn't done until the owner has the **preview link** — the URL in the PR's sticky
"🔍 Open Preview" comment (fallback: `https://<alias>--<tenantId>.blinkpages.dev`, where `<alias>` is the branch
lowercased with every non-alphanumeric run collapsed to `-`, e.g. `draft-holiday/v2` → `draft-holiday-v2`; slugs
over 37 characters get a hash instead, so trust the comment). Previews ask for the site login the first time —
say so. Hand it over in their language — draft / preview / publish, not branch / commit / PR; the methodology's
**What the owner means** table maps every such word (undo, remove, compare, "another version"…) to its mechanic.
There's still no status to report anywhere and no queue to update in interactive mode.

## 5. Make it your own (but not this file)

This skill is centrally managed and will be overwritten when the BlinkPages team ships an update — **don't
edit it.** If you want different behavior, extra steps, or a site-specific workflow, create a **new** skill in
its own directory under `.claude/skills/<your-skill-name>/` (Claude Code) or `.agents/skills/<your-skill-name>/`
(Codex and other agentskills.io tools). Anything outside `.claude/skills/blinkpages/` and
`.agents/skills/blinkpages/` is yours and is never touched by the platform sync.

---

## Drain your queued "Edit with AI" requests

Instead of pasting a prompt, you can pick up the edits you queued from the in-page **Edit with AI**
card. This talks **only to your own site's worker** (the `/_blink` endpoints) — no shared queue, no BlinkPages
secret. You authorize once, then list → claim → edit → push → report status, and the in-page progress card
resolves on its own.

**It needs the network, and a writable home folder.** `node .blinkpages/queue.mjs` talks to this site over
HTTPS and caches its login under `~/.config/blinkpages/`. Some tools run commands in a sandbox by default —
Codex does: network off, writes limited to the workspace. If a queue command fails with `fetch failed`,
`ECONNREFUSED` or `EACCES`, ask to run it outside the sandbox (or approve the escalation your tool offers) and
retry. **A failure here is never "nothing queued"** — say the queue was unreachable, don't report it empty.

1. **Authorize (single click, lasts a day).** Run:

   ```bash
   node .blinkpages/queue.mjs list
   ```

   It prints a one-click link — open it, confirm the shown code, click **Approve**. Nothing to copy or paste
   back. The login is cached for **24 hours**, so this comes round about once a day — that is normal, not a
   fault (and a session that starts from a fresh sandbox authorizes once per session). The command then lists
   your pending edits.

2. **Pick a job, claim it, pull its images.** Take a `<id>` from the list:

   ```bash
   node .blinkpages/queue.mjs claim --job <id> --by "$(git config user.email)"
   node .blinkpages/queue.mjs pull-images --job <id> --dest .precision-images
   ```

   The claim returns the job's `prompt`, `pageKey`, `targetBranch`, and a `claimToken` (keep it — pass it as
   `--claim-token` on every status write). Make sure you're on `targetBranch` before editing. The job's `targetBranch` is the owner's explicit
   choice, made on the editor's "Save as a new draft" checkbox — honor it even when it's the live branch; don't
   re-route a queued job into a new draft.

   A row tagged **`✎ CONTENT`** is not a page edit — it's a **new post/page** queued from the admin console
   (a brief to draft from, a link to import, or both). Claim it the same way, then follow **Content jobs**
   below instead of steps 3–4.

3. **Mark it running, then make the edit.** Set status `running`, then do the change exactly as in steps 3–4
   above — follow `.claude/blinkpages-editing.md`, stay inside `writableRoots`, place
   the pulled images, and commit + push on **your** identity (one logical concern per commit):

   ```bash
   node .blinkpages/queue.mjs set --job <id> --status running --claim-token <claimToken>
   ```

4. **Report status back.** After the push lands, write the outcome so the in-page card resolves:

   ```bash
   node .blinkpages/queue.mjs set --job <id> --status done --commit <sha> --claim-token <claimToken>
   # or, if it didn't work out:
   node .blinkpages/queue.mjs set --job <id> --status failed --error "what went wrong" --claim-token <claimToken>
   ```

If your site's worker doesn't have the queue endpoints yet, the script says so and exits cleanly — fall back
to **interactive mode** (describe / paste the prompt, per the steps above) and edit in place.

### Content jobs (`kind:"content"`)

The admin console's **New <type>** flows queue a different kind of job: not a change to an existing page but a
**new entry in one of the site's content collections** — "New Post with AI", or "New Post" with a link to
import (a Google Doc, a public Claude artifact, a web page). The console has already done every deterministic
step: the draft branch and its PR exist (`targetBranch`), the entry's address is decided, and — when the
collection's schema allows it — a stub file with valid frontmatter is already on the branch. What's left for you
is the *content*.

**How they appear in `list`** — tagged `✎ CONTENT`, plus `import <host>` when a link was snapshotted and
`⚠ <warning>` when that snapshot is suspect; the second line names the file and its address, the third is the
first line of the prompt:

```
  • d_9f1…  pending/queued-for-precision ✎ CONTENT import docs.google.com  ·  4m old
      posts → src/content/posts/q3-launch-recap.md  (/q3-launch-recap/)
      Import the linked Google Doc into a new Post "Q3 launch recap".
```

`[no stub — create the file]` on the second line means the console could **not** write a stub (the schema
needs values no template can guess) — you create the file.

**The record** (from `claim`, or `list --json`) adds to the usual shape:

```jsonc
{ "kind": "content", "source": "content-console", "targetBranch": "draft-q3-launch-recap/v1",
  "entry": { "type": "posts", "collection": "posts", "path": "src/content/posts/q3-launch-recap.md",
             "url": "/q3-launch-recap/", "stub": true, "required": ["title", "date", "slug"],
             "dir": "src/content/posts", "ext": ".md" },
  "importSource": { "url": "https://docs.google.com/document/d/…/edit", "finalUrl": "…/export?format=html",
                    "kind": "google-doc", "attachmentId": "a_…", "contentType": "text/html", "bytes": 48213,
                    "title": "Q3 launch recap", "warning": null },   // absent for a brief-only job
  "prompt": "…" }   // written by the console: the brief (if any), the import facts, the entry's path/URL/required keys
```

**Procedure** — replaces steps 3–4 above (claim, `running`, and the final status write are the same):

1. **Check out the target branch.** `git fetch origin && git checkout <targetBranch>`. It's the console's fresh
   draft (its PR is already open) — commit there; never re-route a content job to another branch. If the branch
   is gone (the owner discarded the draft before you got here), set `failed` with
   `--error "draft was discarded — nothing to write"` and stop.
2. **Learn the collection.** Read `src/content.config.ts` (or `src/content/config.ts`) for the collection's
   schema, then open one or two **sibling entries** in `entry.dir` — they show the frontmatter keys actually
   used, the date format, how images are referenced, and the body conventions (MD vs MDX, components, callouts).
3. **Make sure the file exists with valid frontmatter.**
   - `entry.stub === true` → `entry.path` is already on the branch with valid frontmatter. Its body is a notice
     block ("Importing from …" / "AI is drafting this") and, for an import, a plain-text first pass under a
     `---` rule. **Replace the whole body.** Keep the frontmatter's `title`, `date` and `draft` exactly as the
     console wrote them unless the brief says otherwise — the owner chose the title, and `draft: false` is
     deliberate (the *branch* is the draft; publishing the branch is what makes it live).
   - `entry.stub === false` → create `entry.path` yourself. Every key in `entry.required` must be present and
     valid per the schema: copy a sibling's frontmatter shape and fill it honestly (a real category from the
     enum, the `slug` from `entry.url`, today's date in the sibling's format, `draft: false` where the field
     exists). Never invent a value you can't know (a required headshot, a `canonical` URL) — ask, or set `failed`
     with `--error "<field> is required for a <Type> — tell me <what to provide>"`.
4. **Get the source (imports only).** Pull the snapshot the console took when the job was created:

   ```bash
   node .blinkpages/queue.mjs pull-source --job <id> --dest .precision-source
   ```

   It writes `.precision-source/<id>.html` (or `.txt`) and prints `importSource.warning`. `null` → the snapshot
   *is* the document; convert it. Any other value means the snapshot is not trustworthy — fetch the link
   yourself (`importSource.url`, or `finalUrl`):
   - `not-public` — a Google Doc that isn't shared **"Anyone with the link"**; the snapshot is a sign-in page.
     If you can't reach it either, set `failed` with
     `--error "the Google Doc isn't shared publicly — set Share → Anyone with the link → Viewer, then re-create the post"`.
     That text is what the requester reads on the in-page card.
   - `shell-only` — a Claude artifact whose HTML is an app shell with no content in it. Open the URL in a
     browser-capable tool (a headless browser or a fetch tool that renders JavaScript) and read the rendered page.
   - `not-html` — the link returned something other than HTML (a PDF, a JSON API, …). Open it yourself and
     convert whatever it actually is; if you can't read it, `failed` with an error naming the type.
   - `too-large` — the snapshot was cut at 2 MB. Fetch the full document yourself.
   - `timeout` — the fetch didn't finish in 10 s; the snapshot may be empty or partial. Fetch it yourself.

   Then **convert** it to the collection's conventions per
   `.claude/blinkpages-editing.md` → **Importing a document into a content entry** —
   headings, links, lists, tables, footnotes — and **download every image into the site's media convention**
   (look at how siblings reference images, e.g. files under `public/assets/media/blog/<slug>/` referenced as
   `/assets/media/blog/<slug>/<name>.png`). **Never leave a `googleusercontent.com`, `docs.google.com`,
   `claude.ai` or other remote image URL in the entry** — those links expire or 403 for visitors.
   Before you download anything, run `node .blinkpages/queue.mjs media --q <term>` (§3, **Images**) — the
   site may already have the picture, including in the media bucket where `ls` cannot see it.
5. **Draft the body (when the prompt carries a brief).** Write it in the site's voice: read `reference/`
   (voice-and-tone, about-the-company, customers-and-personas) and the site's own style library or brand page if
   it has one (usually `src/pages/style-library.astro`; some sites keep a `brand.astro` or `DESIGN.md`), and match the
   length, heading rhythm and tone of the best sibling entries. Brief **and** import → convert first, then apply
   the brief to the converted text (restructure, tighten, add what's asked) rather than writing from scratch.
6. **Validate.** `npm run build` (or `npx astro check`, when the site has it) must pass — a schema error here
   means the frontmatter is wrong; fix the entry, never loosen the schema. Confirm the entry was emitted at
   `entry.url` under `dist/`.
7. **Commit and push, then report.** One commit, the entry plus the images you added:

   ```bash
   git add <entry.path> <public/… images you added>
   git commit -m 'blinkpages-ai: import "<title>"'     # or: blinkpages-ai: create "<title>"
   git push
   node .blinkpages/queue.mjs set --job <id> --status done --commit "$(git rev-parse HEAD)" --claim-token <claimToken>
   ```

   The draft's preview rebuilds and the owner lands on the new page. **Don't publish** — the branch is the
   draft; the owner reviews it and hits Publish.

**When it doesn't work out**, `set --job <id> --status failed --error "<message>"`. The `error` is shown to the
requester on the in-page card, so write it for *them* — what happened and what to do next:
- source unreachable → `"the Google Doc isn't shared publicly — set Share → Anyone with the link → Viewer, then re-create the post"`,
  or `"couldn't read <url> (<what happened>) — paste the text into the brief instead"`;
- a required field only the owner can supply → `"<field> is required for a <Type> — tell me <what to provide>"`;
- the draft is gone → `"draft was discarded — nothing to write"`;
- the brief needs an image that doesn't exist → `"needs a real image — please upload one"` (never fabricate one).
