---
name: connect-instagram-developer-platform
description: Connect the user's Instagram account to every agent through their own Meta developer account, fully on its own. It registers them as a Meta developer, creates a Meta app linked to their Instagram, generates the access and the app secret in Chrome AI with dev-browser, saves them locally, then uses connect-tool's format to write a global /instagram-cli skill that reads and answers DMs, comments, posts and stats. Use for "connect Instagram", "Meta developer", "Instagram API", "instagram-cli", "manage my Instagram DMs", "reply to my comments". Run on the user's computer.
argument-hint: "[@username of the Instagram account, default the one signed in to Chrome AI]"
user-invocable: true
---

Give the user's agents full control of their Instagram (DMs, comments, posts, stats, publishing) through a small CLI that talks to Meta's official Instagram API with the user's own Meta app: no third-party service, no monthly fee. Do every step yourself in Chrome AI with the `dev-browser` skill; the user only signs in, confirms their phone if Meta asks, and clicks "Allow". Talk to the user in their language, short messages, no jargon (never say "token", "OAuth", "scope" or "Graph API" to them; say "Instagram access" and "the key").

If you got this skill from a link instead of a local folder, install nothing else from the repo: download [scripts/instagram.py](scripts/instagram.py) with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/connect-instagram-developer-platform/scripts/instagram.py -o <scratch>/instagram.py`, and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

Never print, log or repeat the app secret, the access or what `instagram.py` keeps in `~/.config/instagram-cli/config.json`. Browser scripts that read them write them straight to `~/.dev-browser/tmp/instagram-keys.json` with `writeFile` and log only `{ saved: true }`. Ask the user before you accept Meta's developer terms (step 3). Read each page with `snapshotForAI()` before clicking: Meta's dashboard speaks the user's language and moves its buttons often, so look for the meaning, not the exact words below.

1. Check the tools. `chrome-ai start` and `dev-browser --help` must answer (otherwise run `setup-dev-browser`), and `python3 --version` must be 3.9 or newer. If `~/.agents/skills/instagram-cli/` already exists, run `python3 ~/.agents/skills/instagram-cli/scripts/instagram.py me`: if it answers, tell the user Instagram is already connected and skip to step 10.
2. Check the Instagram account, in a page named `connect-instagram`. Open `https://www.instagram.com/accounts/edit/`: if Chrome AI is not signed in, ask the user to sign in there with the account to connect and say "done". The account must be **professional** (Creator or Business): Meta's API refuses personal accounts. Open `https://www.instagram.com/accounts/convert_to_professional_account/` (or Settings > Account type and tools): if it offers to switch, tell the user in one line it is free, changes nothing for their followers, and ask them to pick Creator (or Business) there. Note the @username.
3. Become a Meta developer. Open `https://www.facebook.com`: Meta developer accounts live on a Facebook account, so ask the user to sign in there if needed (the Facebook account they use for their Instagram, if they have one). Then open `https://developers.facebook.com/async/registration/`. If it shows the dashboard or "My Apps", they are already registered. Otherwise go through it: ask the user before you accept the terms, let them confirm their phone number or email with the code Meta sends (they type it), pick "Developer" as their role.
4. Create the app: open `https://developers.facebook.com/apps/creation/`. App name: `<FirstName> Agent` or anything short **without** "Instagram", "Insta", "IG", "Meta" or "Facebook" (Meta refuses those). Contact email: the account's. Use case: **Manage messaging & content on Instagram** (wording may vary: the one about Instagram messages and content). Business portfolio: "I don't want to connect a business portfolio yet". Create; Meta may ask for the Facebook password again: ask the user to type it. Read the app ID from the address (`/apps/<app_id>/`).
5. Add the access: in the app, open the Instagram use case (left menu "Use cases" > Customize, or `https://developers.facebook.com/apps/<app_id>/use_cases/`), go to **API setup with Instagram login**. In "Permissions" make sure these are added: `instagram_business_basic`, `instagram_business_manage_messages`, `instagram_business_manage_comments`, `instagram_business_content_publish`, `instagram_business_manage_insights`. Standard access is enough: the app only acts on the user's own account, so no Meta review.
6. Link the Instagram account: in the same page, section "Generate access tokens", click **Add account**. A window opens on Instagram's sign-in: tell the user right away, in 3 short lines: in the Chrome AI window, sign in to `@<username>` if asked; click Allow (or "Continue as ..."); come back and say "done". If Meta answers "Insufficient developer role", open `https://developers.facebook.com/apps/<app_id>/roles/roles/`, add the @username as **Instagram Tester**, then open `https://www.instagram.com/accounts/manage_access/` > Tester invites > Accept, and click Add account again.
7. Read the keys. Back on "API setup with Instagram login", next to the linked account click **Generate token**; a dialog shows it after a "I understand" box (tick it). In section "Set up Instagram business login" (or "Business login settings"), read the **Instagram app ID** and the **Instagram app secret** (click Show; Meta may ask the Facebook password: ask the user). These are not the Facebook app ID and secret of App settings > Basic. In one browser script, save the three without logging them:

   ```js
   await writeFile("instagram-keys.json", JSON.stringify({ app_id, app_secret, access_token }));
   console.log(JSON.stringify({ saved: true, app_id }));
   ```

   The token dialog shows it only once: if it closed before you read it, click Generate token again.
8. Install the CLI the connect-tool way, as a global skill folder: `mkdir -p ~/.agents/skills/instagram-cli/scripts`, copy [scripts/instagram.py](scripts/instagram.py) to `~/.agents/skills/instagram-cli/scripts/instagram.py`, then `python3 ~/.agents/skills/instagram-cli/scripts/instagram.py login --from ~/.dev-browser/tmp/instagram-keys.json`. It turns the access into a 60-day one, checks it, deletes the file and ends with `connected=@<username>`. If it says the access is refused, redo step 7 (a new token).
9. Prove it works with real reads, each must answer without an error: `instagram.py me`, `instagram.py posts --max 3` and `instagram.py dms --max 3` (full path `python3 ~/.agents/skills/instagram-cli/scripts/instagram.py`). If `dms` says the permission is missing, check `instagram_business_manage_messages` in step 5, then regenerate the token (step 7) and log in again. Also check Instagram > Settings > Messages and story replies > Message controls > Connected tools > **Allow access to messages** is on (in the Instagram app on the phone: ask the user if you cannot find it on the web). An empty list is fine if they have no DMs.
10. Write the skill with connect-tool's format (read `connect-tool`, steps 5 and 6, from the user's skills or from the repo): `~/.agents/skills/instagram-cli/SKILL.md`, exactly this, then link it for Claude Code like connect-tool step 6.

    ```markdown
    ---
    name: instagram-cli
    description: Instagram from the terminal with the user's own Meta app: DMs (read, answer), comments (read, reply, hide), posts and their stats, publishing photos and reels. Use when the user asks about their Instagram DMs, to answer messages or comments, how their posts are doing, or to publish on Instagram.
    ---

    Run `python3 ~/.agents/skills/instagram-cli/scripts/instagram.py <command>`; run it with no command to see them all. Access: the user's own Meta app `<app_id>` for `@<username>`, set up by /connect-instagram-developer-platform (run it again if access is lost).

    - Account: `me` · latest posts: `posts --max 10` · stats of a post: `post-stats <mediaId>`
    - DMs: `dms` (conversations) · `messages <conversationId>` · answer: `send <with_id> "<text>" --yes`
    - Comments: `comments <mediaId>` · `reply-comment <commentId> "<text>" --yes` · `hide-comment <commentId> --yes`
    - Publish (public link to the file): `publish <image_url> --caption ".." --yes` · reel: `publish --video <url> --caption ".." --yes`
    - Anything else: `api GET <path> --query fields=..`

    DMs can only be answered within 24 hours of the person's last message. Show the user the exact text and get their OK before every `--yes`. The access lasts 60 days and renews itself when used. New DMs in real time need a webhook on a server (not here). Docs: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login
    ```

11. If the user has a brain folder with an `AGENTS.md`, add one line there: Instagram (DMs, comments, posts) goes through `/instagram-cli`, account `@<username>`, read before writing, always ask before sending a DM, replying or publishing.

End with a short check list, a check or a cross on each line: professional account, Meta developer, app created, permissions added, Instagram linked, keys saved, me / posts / dms answer, `/instagram-cli` skill written. Then tell the user in 3 lines: their Instagram is connected through their own Meta app, a new session shows `/instagram-cli`, and one thing to try now, for example "Summarize my unread Instagram DMs and draft a reply for each".
