---
name: preview-site
description: Use when starting, checking, or debugging the local Eleventy dev server for this site, previewing unuploaded media, or when images 404, the page is stale, or the production build fails on unregistered media.
---

# Preview The Site Locally

Paths are relative to the repository root.

## Start it

```bash
COMFY_MEDIA_ORIGINALS=/mnt/e/ai/comfy-with-comfyui-media npm run dev
```

`npm run dev` alone works **only** if the shell already exports `COMFY_MEDIA_ORIGINALS`. It is exported from `~/.bashrc`, which is read once per shell, so a terminal opened before that line was added does not have it. Passing it inline always works.

Normal preview checks local originals only for media that is not registered in `media.json`. When replacing an already registered image or video and the local replacement must appear before sync, use the slower replacement-preview mode:

```bash
COMFY_MEDIA_ORIGINALS=/mnt/e/ai/comfy-with-comfyui-media npm run dev:media
```

That mode hashes registered originals to find replacements, so use it only while replacing media.

Never start a server without being asked. Check for one first, and never leave one running.

## Diagnose

Who holds the port, and does that process have the originals root?

```bash
P=$(ss -ltnp 2>/dev/null | grep -oP ':8080.*pid=\K[0-9]+' | head -1); echo "pid=${P:-none}"
[ -n "$P" ] && tr '\0' '\n' < /proc/$P/environ | grep -i COMFY_MEDIA_ORIGINALS || echo "NOT SET"
```

List every dev server, including ones left over from an earlier session:

```bash
pgrep -af "eleventy --serve" | grep -v grep || echo "(none running)"
```

Is an unuploaded original actually reachable?

```bash
curl -s -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" \
  http://localhost:8080/__media-originals/<section>/<slug>/<file>.png
```

## Gotchas

**A stale server squats the port.** Only the first process to bind 8080 serves; later ones still write `_site`. So the HTML can be correct while images 404, because the *serving* process is an older one with no `COMFY_MEDIA_ORIGINALS`. Symptom: `<img src="/__media-originals/...">` is right in the HTML, and the image request returns 404. Kill every `eleventy --serve` and start one.

**`_data/*.js` is cached per process.** Editing `src/_data/nav.*.yml`, a slug, `navId`, or `ops/ia.md` does **not** take effect until the server restarts — the running process keeps the nav it loaded at startup. It can also fail loudly: a renamed page left the old placeholder path in memory and the build died with `ENOENT: ... _site/ja/data-utilities/loops/index.html`. Article text and media are picked up normally; nav and identity changes are not.

**`npm run build` refusing unregistered media is correct.** Production builds throw on a `/media/...` that is not in `src/_data/media.json`; dev servers only warn and render the original instead ([.eleventy.js:489](.eleventy.js:489)). So the build failing while an article is still uncommitted is expected; it clears when the pre-commit `media:sync` uploads and registers the files. After that the build must pass — see [release-check](../release-check/SKILL.md). Do not "fix" it by editing `media.json` by hand.

**Video posters do not exist before upload.** In the dev preview a video's poster is empty, because the poster is a frame `media:sync` extracts and uploads. `{media=player}` therefore shows no thumbnail locally; `{media=loop}` plays regardless. Nothing is wrong.

**`_site` keeps deleted pages.** After a rename, the old URL still answers 200 from the stale output directory. `rm -rf _site/<lang>/<section>/<old-slug>` to check a rename honestly.

## Next

- [article-authoring](../article-authoring/SKILL.md) — writing the page whose media you are previewing
- [release-check](../release-check/SKILL.md) — the checks to run once it looks right
