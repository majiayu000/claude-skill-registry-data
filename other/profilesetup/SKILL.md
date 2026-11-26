---
name: profileSetup
description: Give a Facebook account its profile picture and cover photo with `log facebook profile setup`. Dry run first to read the profile page and check its controls from the recording, then --live when the owner asks. Use when setting up a new account's profile, when the owner says "profile photo", "cover photo", "background profile", or when an upload step stops with profileControlNotFound.
---

# profileSetup

A new account gets a real-looking profile photo and a cover photo on days 1-2
of its warm-up. This does that for one account, both photos in one run (the owner's choice).

## Hard boundaries

1. **Dry run first, `--live` only when the owner asks** (rule 8). Over MCP,
   `--live` is `facebookProfileLive`, with `confirmLive: true`.
2. **Read before clicking** (rule 25). The upload clicks in
   `python/session/profileSession.py` were written before the page was seen. The dry
   run writes every button, link and file input the profile page has to
   `profileFound.txt`; check the patterns (`PROFILE_PICTURE`, `COVER`,
   `UPLOAD`, `SAVE`) against it, and fix them, before the first `--live`.
3. **Only the two photos change.** With `profileName` set, the dry run also reads
   the name page (`nameFound.txt`); the rename itself is built from an inspect
   recording first (rule 29). Bio and every other field stay read-only.
4. **It is a launch** (rule 35): it counts against the 8 a day, 10 minutes
   apart, and needs waking hours, the proxy gate and a saved
   session (`log facebook connect` first).
5. **Run it live** (rule 26): through Monitor, every machine state prints.

## The routine

1. Put the photos in Twenty: `socialAccounts.profilePhoto` (a real-looking
   face, not a logo) and `coverPhoto` (business-related is fine), each a URL
   or a local path. URLs are fetched through the account's proxy, never from
   this machine, and every file is varied so its bytes are new
   (`media/photo`).
2. Look first (rule 29): `log inspect start --account <a> --url https://www.facebook.com/me`,
   then `log inspect do snapshot` (skills/inspect). The upload clicks come from that.
3. Dry run:

   ```bash
   log facebook profile setup --account <a> 2>&1 | tee <log>
   ```

   It prints each photo as `would upload`, `no photo set in Twenty` or
   `no control for it on the page`, and the run folder
   (`~/.logCli/runs/profile/<time>_<a>/`).
4. Read `profileFound.txt` in that folder and the step HARs (`firefox/steps/`).
   If the picture or cover control isn't the one the patterns match, fix the
   pattern in `python/session/profileSession.py` and its test, commit, and dry run
   again after the launch gap.
5. When the owner says go: `--live`. The machine uploads the profile photo, then
   the cover; any failed step stops the run (nothing is retried on
   Facebook). A failed step saves `<item>Failed.txt` with what the page had.
   On success `profileSetAt` is set in Twenty.
6. Rebuild the Facebook client docs: the profile requests are new.

   ```bash
   log capture docs
   ```

## Codes

| Code | Means | Do |
| --- | --- | --- |
| `profilePhotoMissing` | `--live` without both photos, or a photo that can't be read | Set both fields in Twenty |
| `profileControlNotFound` | No opener, no "Upload photo" item, no file input | Read `profileFound.txt` / `<item>Failed.txt`, fix the pattern |
| `profileUploadNotSaved` | Save never enabled, or the dialog stayed open | Read the capture; run again after the gap |
| `sessionExpired` | The profile wasn't signed in | `log facebook connect --account <a>` first |
