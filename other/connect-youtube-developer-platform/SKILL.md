---
name: connect-youtube-developer-platform
description: Connect the user's YouTube channel to every agent through their own Google developer account, fully on its own. It creates the Google Cloud project, turns on the YouTube Data and Analytics APIs, creates the access key in Chrome AI with dev-browser, signs the user in locally, then uses connect-tool's format to write a global /youtube-cli skill that runs on the user's own daily quota. Use for "connect YouTube", "YouTube API", "youtube-cli", "read my YouTube stats", "reply to my YouTube comments". Run on the user's computer.
argument-hint: "[email of the Google account that owns the channel, default the one signed in to Chrome AI]"
user-invocable: true
---

Give the user's agents their YouTube channel (videos, stats, comments, uploads) through a small CLI that talks to the YouTube APIs with the user's own Google Cloud project, so every call uses their own free daily quota (10,000 units) and no third-party service. Do every step yourself in Chrome AI with the `dev-browser` skill; the user only signs in, picks their channel and clicks "Allow" in Google's pages. Talk to the user in their language, short messages, no jargon (never say "OAuth", "client secret", "scope" or "token" to them; say "YouTube access" and "the key").

If you got this skill from a link instead of a local folder, install nothing else from the repo: download [scripts/youtube.py](scripts/youtube.py) and [scripts/youtube-oauth.sh](scripts/youtube-oauth.sh) with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/connect-youtube-developer-platform/scripts/<file> -o <scratch>/<file>`, and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

Never print, log or repeat the key's secret, a sign-in code or what `youtube.py` keeps in `~/.config/youtube-cli/config.json`. Browser scripts that read the secret write it straight to a file with `writeFile` and log only `{ saved: true }`. Ask the user before you accept Google Cloud's terms or publish the app (steps 3 and 6), once for both.

1. Check the tools. `chrome-ai start` and `dev-browser --help` must answer (otherwise run `setup-dev-browser`), and `python3 --version` must be 3.9 or newer. If `~/.agents/skills/youtube-cli/` already exists, run `python3 ~/.agents/skills/youtube-cli/scripts/youtube.py channel`: if it answers, tell the user YouTube is already connected and skip to step 10.
2. Pick the account: the argument, or the Google account signed in to Chrome AI (open `https://myaccount.google.com` in a page named `connect-youtube` and read the email). If Chrome AI is not signed in to Google, ask the user to sign in there with the account that owns their YouTube channel and say "done". Then open `https://www.youtube.com/account` and read the channel name, so you can confirm it with the user in one line.
3. Find or create the Google Cloud project, in the page `connect-youtube`. A project of its own keeps YouTube's quota apart from anything else. Open `https://console.cloud.google.com/cloud-resource-manager` and look for a project named `YouTube CLI`: reuse its ID. If there is none, open `https://console.cloud.google.com/projectcreate`, name it `YouTube CLI`, create it, wait for the notification, and read its ID (the `project=` part of the address once it opens). On a first visit, Google Cloud asks for a country and its terms: ask the user before you accept. Read each page with `snapshotForAI()` before clicking: the console speaks the user's language and moves its buttons.
4. Turn on YouTube: open `https://console.cloud.google.com/flows/enableapi?apiid=youtube.googleapis.com,youtubeanalytics.googleapis.com&project=<id>` and confirm. Wait until the page says they are on.
5. Set up the sign-in screen: open `https://console.cloud.google.com/auth/overview?project=<id>`. If it offers to get started, fill: app name `YouTube CLI`, support email = the account, audience **External**, contact email = the account, tick the Google API Services User Data Policy box, then create. If it is already set up, keep it as it is.
6. Keep the access for good: open `https://console.cloud.google.com/auth/audience?project=<id>`. If the status is "Testing", click "Publish app" and confirm. A Testing app loses YouTube access every 7 days; published, it keeps it (Google does not review a personal app, it only shows a warning when signing in).
7. Create the key: open `https://console.cloud.google.com/auth/clients/create?project=<id>`, type **Desktop app**, name `YouTube CLI`, create. In the same browser script, read the client ID and the secret from the dialog that opens and save them without logging them:

   ```js
   await writeFile("youtube-client.json", JSON.stringify({ installed: { client_id, client_secret } }));
   console.log(JSON.stringify({ saved: true, client_id_end: client_id.slice(-30) }));
   ```

   The secret is shown only once: if the dialog closed before you read it, create a new key the same way.
8. Install the CLI the connect-tool way, as a global skill folder: `mkdir -p ~/.agents/skills/youtube-cli/scripts`, copy [scripts/youtube.py](scripts/youtube.py) to `~/.agents/skills/youtube-cli/scripts/youtube.py`, then save the key (this deletes the file): `python3 ~/.agents/skills/youtube-cli/scripts/youtube.py auth-url --client-file ~/.dev-browser/tmp/youtube-client.json --project <id> >/dev/null`.
9. Connect the channel: `bash scripts/youtube-oauth.sh` (from this skill's folder). Run it in the background: it opens Google's sign-in page in Chrome AI and waits up to 10 minutes. Tell the user right away, in 3 short lines: in the Chrome AI window, pick `<email>` (then the channel, if Google asks which one); on "Google hasn't verified this app", click Continue (it is their own app); tick every access asked and click Continue. It ends with `connected=<channel> channel=<id>`. Exit code 4 means they did not allow access in time: ask, then run it again. Exit code 5 with "no lasting access": remove "YouTube CLI" at `https://myaccount.google.com/permissions` in Chrome AI, then run it again.
10. Prove it works with real reads, each must answer without an error: `youtube.py channel`, `youtube.py videos --max 3` and `youtube.py analytics --days 7` (full path `python3 ~/.agents/skills/youtube-cli/scripts/youtube.py`). If Google says an API is off, redo step 4. Analytics can be empty on a brand new channel: that is fine.
11. Write the skill with connect-tool's format (read `connect-tool`, steps 5 and 6, from the user's skills or from the repo): `~/.agents/skills/youtube-cli/SKILL.md`, exactly this, then link it for Claude Code like connect-tool step 6.

   ```markdown
   ---
   name: youtube-cli
   description: YouTube from the terminal with the user's own Google quota: channel stats, videos, analytics, comments, replies, title and description changes, uploads. Use when the user asks how their videos are doing, their best videos, to read or answer comments, to change a title or description, or to upload a video.
   ---

   Run `python3 ~/.agents/skills/youtube-cli/scripts/youtube.py <command>`; run it with no command to see them all. Access: the user's own Google Cloud project `<id>`, set up by /connect-youtube-developer-platform (run it again if access is lost).

   - Channel stats: `channel` · latest videos: `videos --max 10` · one video: `video <id>`
   - Analytics: `analytics --days 28` (day by day) · best videos: `top --days 28`
   - Comments: `comments [videoId]` · reply: `reply <commentId> "<text>" --yes`
   - Change a video: `update <videoId> --title ".." --description ".." --yes`
   - Upload (private by default): `upload <file> --title ".." --yes`
   - Quota left and costs: `quota` · anything else: `api GET /<path> --query k=v`

   Quota: 10,000 units a day (reads cost 1, search 100, reply or update 50, an upload much more), reset at midnight Pacific time. Read before writing. Show the user the exact text and get their OK before `--yes` (reply, update, upload, delete). Docs: https://developers.google.com/youtube/v3/docs
   ```

12. If the user has a brain folder with an `AGENTS.md`, add one line there: YouTube (stats, comments, videos) goes through `/youtube-cli`, channel `<name>`, read before writing, ask before replying, changing or uploading.

End with a short check list, a check or a cross on each line: Google Cloud project, YouTube APIs on, app published, key saved, channel connected, channel / videos / analytics answer, `/youtube-cli` skill written. Then tell the user in 3 lines: their YouTube is connected with their own quota, a new session shows `/youtube-cli`, and one thing to try now, for example "What are my 5 best videos of the last 28 days?".
