---
name: publish
description: Put the current website changes live — check them, save them to GitHub, and let Vercel deploy attoset.com. Use whenever someone says publish, make it live, ship it, deploy, push, put it online, or save my changes to GitHub. Also use to undo a publish.
---

# Publish the Attoset site

Pushing to `main` on GitHub makes the change **public** — Vercel redeploys the live site
automatically. Treat this as the outward-facing step it is.

**Assume the person running this is not a developer.** No jargon, no raw git output.
Say "your changes are saved and going live", not "rebased onto origin/main".
If something goes wrong, explain what happened in one plain sentence and what you'll do about it.

Git commands run from the repo root; `npm` commands from `attoset-web/`.

## 1. Show what's changing, and get a yes

```bash
git status --short
git diff --stat
```

Translate that into plain English before asking anything — page and section names, not file paths:

> Here's what's ready to publish:
> • Home page — the pricing wording in the hero
> • Contact page — new email address
> Nothing else has changed. Publish this to the live site?

Then **wait for a clear yes.** Never publish on your own initiative, and never publish work
that hasn't been looked at. If they only wanted to *see* the changes, stop here.

Also check before going further:
- On the `main` branch? (`git branch --show-current`) If not, say so and ask before switching.
- Anything in the list that shouldn't ship — `.env` files, passwords, API keys, personal notes,
  the `qr/` folder, stray screenshots? Flag it and leave it out rather than committing it.
- Nothing changed at all? Say "there's nothing new to publish" and stop.

## 2. Check it won't break the site — never skip this

```bash
cd attoset-web
npm run lint && npx tsc --noEmit && npm run build
```

**If the build fails, do not push.** A broken build means a broken live site.
Say plainly: "This change has an error, so I haven't published it — here's what's wrong."
Fix it (see the `site-edit` skill), re-run the checks, then continue.

If the change is visual, screenshot it first and look at it:
`node scripts/shot.mjs --page home --w 1440,390` (needs `npm run dev` running).

## 3. Save and send it to GitHub

```bash
cd ..
git pull --rebase origin main    # pick up anything published from another machine
git add <the specific files>     # never `git add -A` — it sweeps up junk
git commit -m "Short plain-English description of the change"
git push origin main
```

Commit messages are written for a human skimming the history: *"Update contact email and
fix hero spacing on mobile"* — not "wip" or "changes".

End every commit message with:

```
Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01XCPchD2h1ugYkfg56EyYN2
```

If the push is rejected because someone else published first: run `git pull --rebase origin main`,
re-run the build check, push again. Explain it as "someone else published a change first, so I
merged it in and tried again". If git asks for a login it can't get, say the GitHub sign-in has
expired and the repo owner needs to sign in again — don't try to work around it.

## 4. Tell them where it's going

Vercel starts building the moment the push lands; the live site usually updates in **1–2 minutes**.

- Repo: https://github.com/mohamed161001/Attoset-website
- Deploy progress: the Vercel dashboard for this project

**Say "it's deploying now", not "it's live"** — until you've actually seen it. To confirm,
wait ~90 seconds and load the live site (`https://attoset.com`, or the Vercel URL if the
domain isn't attached yet) and check the changed text is really there. If it 404s or times out,
report that honestly rather than assuming success.

## 5. Undo a publish

If something looks wrong on the live site, the fix is to publish the *reverse* of the last change —
not to delete anything:

```bash
git log --oneline -5            # find the commit to undo
git revert <commit-id> --no-edit
git push origin main
```

Vercel redeploys the previous state within a couple of minutes. Tell them the site is
"rolling back to how it was before, live again in about two minutes."

Never use `git reset --hard`, `git push --force`, or delete branches to fix a bad publish.
