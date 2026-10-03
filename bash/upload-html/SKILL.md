---
name: upload-html
description: Publish a local HTML file or static site folder to git@github.com:AyaSakura-comp/TempHtml.git by default, or to another GitHub repo you already have access to, then return a raw.githack CDN URL.
allowed-tools: bash read write
---

# upload-html

Publish a single HTML file or static site folder by staging it in a temp dir, then push it to a GitHub repo and return a shareable raw.githack URL.

## Default behavior

- Default target repo: `git@github.com:AyaSakura-comp/TempHtml.git`.
- If a target repo is provided (`owner/repo`, `https://github.com/owner/repo`, or `git@github.com:owner/repo.git`), use that repo directly.
- **NEW default (no flags): every upload is nested under a unique date/stamp
  sub-path** of the form `YYYY/MM-DD/HHMMSS/<slug>/`, where `<slug>` is derived
  from the input filename (or its parent directory name when the file is a
  generic `index.html` / `main.html` / `site.html` etc.). This guarantees each
  upload gets its own URL and **never overwrites a prior upload**.
- `--flat`: opt out of nesting and keep the legacy behaviour — single-file
  upload lives at the repo root with its original filename (will overwrite
  any same-named file already there). Mutually exclusive with `--name`.
- `--name <slug>`: use a custom stable sub-path (relative to repo root) instead
  of the auto-generated timestamped one. Useful for a memorable, shareable URL
  you want to keep pointing at the latest version. Slashes in the slug are
  collapsed to `_` (treated as a single segment). Mutually exclusive with `--flat`.
- Folder: staged as-is under the same destination sub-path; uses `index.html`
  only if it already exists or is required by the site structure.
- For direct repo pushes, SSH access or GitHub auth must already work.

## Usage

```bash
# NEW default: unique timestamped sub-path (never collides)
./scripts/upload-html.sh /path/to/index.html
./scripts/upload-html.sh /path/to/site-folder

# legacy: live at repo root with original filename
./scripts/upload-html.sh /path/to/index.html --flat

# custom stable sub-path: <repo>/<slug>/index.html
./scripts/upload-html.sh /path/to/index.html --name my-snake

# alternate target repo (works with --flat / --name too; repo is positional arg 2)
./scripts/upload-html.sh /path/to/site-folder owner/repo
./scripts/upload-html.sh /path/to/site-folder owner/repo --name demo
```

## Workflow

1. Validate the input path exists.
2. Stage files into a temp directory.
3. Compute the destination sub-path:
   - default → `YYYY/MM-DD/HHMMSS/<slug>/` (unique per second)
   - `--flat` → repo root
   - `--name <slug>` → `<slug>/`
4. If a target repo was supplied, clone it and sync the staged files into the
   chosen sub-path; otherwise use the default repo
   `git@github.com:AyaSakura-comp/TempHtml.git`.
5. Push the updated branch and return:
   - `Repo URL`
   - `Path` (the relative path of the entry HTML inside the repo)
   - `Raw URL` (`raw.githubusercontent.com`)
   - `Site URL` (`raw.githack.com`)

## Troubleshooting

- If the repo exists but you do not have permission, stop and report the GitHub error.
- If the site has relative assets, include them in the pushed folder.
- raw.githack may cache briefly after the first push.
- Want a stable URL that always reflects the latest version? Use `--name <slug>`;
  re-running with the same slug overwrites that single sub-path deterministically
  (the timestamped default always creates a fresh path and never overwrites).
