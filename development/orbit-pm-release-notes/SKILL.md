---
name: orbit-pm-release-notes
description: Auto-draft release notes for a WordPress plugin from CHANGELOG.md + git diff + visual regression diffs. Generates user-facing announcement (blog post, email, in-plugin notice), readme.txt changelog, GitHub release notes, and a tweet-thread. Use when the user says "release notes", "draft announcement", "changelog → blog post", "what to write for v2.4".
---

# 🪐 orbit-pm-release-notes — Auto-draft release notes

Most plugin teams write release notes 90 minutes before pushing. This skill does the heavy lift in 5 minutes — you edit, you don't draft.

---

## Quick start

```bash
claude "/orbit-pm-release-notes Draft v2.5 release notes from CHANGELOG.md and the git diff since v2.4."
```

Or via the script:
```bash
bash ~/Claude/orbit/scripts/draft-release-notes.sh --from v2.4.0 --to HEAD
```

Output: 4 files in `reports/release-notes/`:
- `blog.md` — long-form announcement (blog post)
- `email.md` — newsletter / customer email
- `readme.txt` — WP.org-formatted changelog entry
- `social.md` — tweet thread / LinkedIn / social

---

## What it does

### 1. Read the inputs
- `CHANGELOG.md` — what the dev team wrote
- `git log v2.4.0..HEAD --oneline` — every commit since last release
- `reports/version-compare-*.md` — what `/orbit-version-compare` measured
- `reports/screenshots/release-diff/` — what changed visually

### 2. Classify changes
- 🆕 New features (top of the post — most exciting)
- ⚡ Performance improvements (with measurable numbers)
- 🐛 Bug fixes
- 🔒 Security patches (mention but don't dwell — Patchstack-style restraint)
- 🌐 Translations / i18n
- 🧹 Internal refactors (often skipped from user-facing notes)

### 3. Pull metrics where possible
- "30% faster page load" — back it up with the Lighthouse / Editor perf number
- "Reduced bundle by 80KB" — pull from `/orbit-bundle-analysis` diff
- "Fixed crash affecting 3% of users" — only if you have the data

### 4. Adopt the right voice per channel

| Channel | Tone | Length |
|---|---|---|
| Blog | Excited but measured, screenshots, deep dive | 800-1500 words |
| Email | Warm, customer-focused, scannable | 250-500 words |
| readme.txt changelog | Terse, factual, bullet list | 50-150 words |
| Social | Headline + 1-2 visuals, links | 280 chars × 3-5 thread |
| In-plugin notice | Subtle, dismissible | 1-2 sentences |

### 5. Hide what shouldn't be public
- Internal refactors (mention only if user-affecting)
- Codenames / sprint names
- Failed experiments (keep in private retro)

---

## Example output (blog.md)

```markdown
# My Plugin 2.5 — Faster, Cleaner, Now with Block Bindings

April 29, 2026 · Orbit Team

We just shipped 2.5 with three focuses: speed, the new Block Bindings API,
and a refresh of the settings UI.

## ⚡ 30% faster admin (and we have the receipts)

Lighthouse on the Settings page: **74 → 95 (Performance score)**. We got there by:
- Lazy-loading the colour picker (only loads when needed)
- Dropping a 60KB icon font in favour of inline SVGs
- Switching the activity log to virtualised rendering

[Lighthouse before/after screenshot]

## 🆕 Block Bindings API support

If you're on WP 6.5+, you can now bind any block attribute to data from your
plugin via the official Block Bindings API. No more custom render filters.

[Tutorial link]

## 🎨 Settings UI refresh

The Settings page got a real design pass — empty states with CTAs, error
messages that actually help, dark mode that respects your admin colour scheme.

[Before/after screenshots from /orbit-version-compare]

## Plus 12 bug fixes
[bullet list]

— Orbit Team
```

---

## Output

```
reports/release-notes/
├── blog.md          ← long-form for blog
├── email.md         ← newsletter
├── readme.txt       ← WP.org changelog (paste into your readme.txt)
├── social.md        ← tweet thread
└── notice-html.txt  ← in-plugin admin notice HTML
```

Each is a draft — you ALWAYS edit before publishing. Treat as 80% complete, your job is the last 20%.

---

## Pair with

- `/orbit-changelog-test` — verify every claimed change has a test
- `/orbit-version-compare` — measure-backed claims
- `/orbit-pm-rice` — what's worth highlighting (top RICE = top of the post)

---

## Sources & Evergreen References

### Canonical docs
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) — format spec
- [WP.org readme.txt format](https://wordpress.org/plugins/readme.txt) — submission format
- [Conventional Commits](https://www.conventionalcommits.org/) — commit message → release-note pipeline

### Rule lineage
- Keep a Changelog format — stable since 2014, widely adopted
- WP.org readme — format unchanged for years

### Last reviewed
- 2026-04-29
