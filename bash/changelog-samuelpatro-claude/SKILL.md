---
name: changelog
description: Generate a single unified changelog from git history that works for everyone in the company (managers and non-tech colleagues as well as developers). Outputs Slack mrkdwn so it can be pasted straight into Slack. Defaults to Slovak (English only on explicit request) and to comparing the release branch (main) against develop to show unreleased changes; also supports date ranges like "today", "yesterday", "last week", or an explicit git range. User-invoked only via /changelog.
allowed-tools: Bash(git *), Bash(gh *)
disable-model-invocation: true
---

# Changelog generator

Turn git history into one unified changelog that works for everyone in the
company: clear enough for managers and non-tech colleagues, detailed enough for
the developers. There is no "dev vs non-tech" split. Write a single changelog
from both worlds.

## Pre-loaded git context

The data below is injected automatically when the skill loads (each `!` block
runs as its own plain command, so the preload also works inside worktree
sessions whose sandbox rejects compound shell). Use it directly. Only fall back
to the **Bash** tool for cases this data does not cover: an explicit custom
range (`v2.0.0..HEAD`), a window older than 14 days, or to `git fetch` for
freshness.

Today's date:

```!
date +%Y-%m-%d
```

Working branch (the branch the session is on):

```!
git rev-parse --abbrev-ref HEAD
```

Origin URL. Derive the repo web url yourself: `git@host:owner/repo.git` becomes
`https://host/owner/repo`, and a trailing `.git` is dropped:

```!
git remote get-url origin
```

RELEASE REFS. Every `main` ref this repo has, local and remote (all company
repos use `main` as the release branch; `master` is never used). If this list
is **empty**, the repo has no release branch and the UNRELEASED block below is
meaningless (it lists the whole history): ignore it and use the fallback in
section 1.

```!
git for-each-ref --format='%(refname:short)' 'refs/heads/main' 'refs/remotes/*/main'
```

UNRELEASED: commits on HEAD that are not on `main`, local or remote. (The
bracket glob `mai[n]` is deliberate: a non-glob pattern such as
`--branches=main` gets `/*` appended by git and matches nothing. Never
"simplify" it away.) Capped at 300 commits; if exactly 300 show, the range is
likely bogus, treat it like an empty RELEASE REFS list:

```!
git log HEAD -n 300 --not --branches='mai[n]' --remotes='*/mai[n]' --no-merges --pretty=format:"%h|%ad|%s" --date=format:"%Y-%m-%d %H:%M"
```

LAST 14 DAYS on the working branch:

```!
git log --since="14 days ago" --no-merges --pretty=format:"%h|%ad|%s" --date=format:"%Y-%m-%d %H:%M"
```

## 1. Pick the commit range from the injected data

- **Default** (no range args, or "unreleased" / "vs main" / "branch"): use the
  **UNRELEASED** block above.
  - **If UNRELEASED is empty** (common here: `main` and `develop` are kept in
    sync with no release tags), fall back to the **last 3 days** from the LAST 14
    DAYS block and tell the user ("main and develop are in sync, showing the
    last 3 days instead").
  - **If RELEASE REFS is empty, or UNRELEASED hit the 300-commit cap**, the
    UNRELEASED data is unusable: fall back to the last 3 days the same way and
    say why ("this repo has no main branch to compare against").
- **Date ranges**: filter the LAST 14 DAYS block by date using "today" from the
  injected header.
  - "today" → commits dated today
  - "yesterday" → commits dated yesterday only
  - "today and yesterday" → both
  - "last week" / "7 days" → last 7 days
- **Explicit range** (`v1.2.0..HEAD`, two tags/branches, or a window > 14 days):
  the injected data won't cover it. Run the **Bash** tool yourself:
  `git log <range> --pretty=format:"%h|%ad|%s" --date=format:"%Y-%m-%d %H:%M" --no-merges`

If the chosen range is genuinely empty, say so plainly and stop (don't invent entries).

## 2. Decide language

There is only **one** changelog style (see section 3), so the only choice is
language. If the user named it in args ("slovak", "sk", "en", "english"), use it.
Otherwise **default to Slovak** — do not ask. Only produce English when the user
explicitly requests it ("en" / "english").

## 3. Write the changelog

One changelog, for the whole company. Each entry must be understandable by a
manager or non-tech colleague, while still carrying enough detail that a developer
recognizes exactly what shipped. Aim for "plain language first, precise detail
second" on every line.

- Read the commit subjects (and PR titles when a subject is terse) to understand
  what each change does. Translate intent into clear language; don't just reformat
  the raw subject line.
- Map Conventional Commit prefixes: `feat`→new feature, `fix`→fix,
  `perf`→speed/performance, `chore`/`deps`→housekeeping, `revert`→rolled back,
  `docs`→documentation.
- **Plain language, but not baby talk.** Lead with what changed and where, in
  words anyone in the company understands. Don't expose deep code internals (table
  names, function names, query patterns, commit hashes) in the wording. But *do*
  keep the vocabulary people recognize: UI elements (badge, menu, nav, hero,
  banner, filter, checkout, product card, modal, dropdown, tab) and plain
  technical concepts that matter (login, permissions, security, backups, speed).
  Translate the *mechanism*, keep the *meaning*: e.g. "N+1 queries" → "pages load
  faster with less strain on the server".
- **Keep the proper names people recognize.** Code internals get translated
  away, but real names that identify the change must stay: product and section
  names (Exclusive Club, special box, tester kit), campaign and integration
  names (Bloomreach, Packeta, Doklado), badge and page labels ("Skvelé na
  cesty"), and concrete numbers (product IDs, prices, percentages) when they're
  the point of the change. Stripping these out makes the line useless. When in
  doubt whether a name is "internal noise" or "the thing that shipped", keep it.
- **Carry detail for both worlds.** Say specifically what changed and where (which
  page, section, element, or area), not just "something was improved". Where it
  helps a developer trace the change, a short area tag (`payroll`, `auth`) may join
  the PR link in the closing parentheses. Keep these unobtrusive: plain meaning
  first, reference last. Never lead with a hash or internal name.
- **End every line with its PR link.** Close each entry with the PR id as a
  linked hashtag in parentheses, built from the `repo web url` in the injected
  header: `([#1234](https://github.com/acme/shop/pull/1234))`. When one line
  covers several PRs, link each id inside the same parentheses, comma-separated.
  Finding the PR id for a commit:
  - Squash merges carry it in the subject as `(#1234)`. Use that directly.
  - Subjects without an id: map commits in one batch with
    `gh pr list --state merged --json number,title,mergeCommit` (or per commit
    `gh api repos/{owner}/{repo}/commits/{sha}/pulls`).
  - A direct commit with no PR gets no link. Never invent an id.
- **Be detailed, don't collapse changes.** Give every meaningful change its own
  line. Do not merge several distinct changes into one fuzzy summary, and do not
  drop a change just because it seems minor. The only things to omit are pure
  internal noise with zero impact on anyone (CLAUDE.md edits, throwaway-script
  cleanup, doc-file deletes, lint/formatting-only commits, CI tweaks with no
  behavior change).
- **Group by what people notice, and use as many sections as the changes
  warrant.** Don't force everything into three buckets. Pick the sections that
  actually fit what shipped, and split a broad area into finer sub-sections when
  it has several distinct changes. A useful palette to draw from (use only the
  ones that apply, add your own when needed):
  - **Shopping experience** — storefront, product pages, cart, checkout, badges,
    navigation, search, filters
  - **Marketing & campaigns** — promos, discount codes, gift cards, newsletter,
    Bloomreach / integration-driven campaigns
  - **Speed** — anything that makes a page or action faster
  - **Back office** — admin lists, widgets, order/parcel management, internal
    tools the team uses
  - **Sign-in & security** — login, permissions, auth, data protection
  - **Under the hood** — refactors, infrastructure, deploy/CI, dependency bumps
    that still matter, written plain-first so a manager gets the gist and a
    developer gets the specifics
  When a section would hold only one line, fold it into the nearest fitting
  section rather than leaving a one-item heading. When a section runs long,
  split it (e.g. "Shopping experience" → "Product pages" + "Cart & checkout").
- **Calibrate length per line: one tight sentence by default.** State what
  changed and where, then stop. Add a second sentence or a nested sub-bullet
  ONLY when it carries information the reader needs (an exact name, number,
  edge case, or who it affects). Don't pad with restated mechanism, and don't
  strip a line down so far it loses its point. If a line reads as a vague
  "something was improved", it's too short; if it explains how the code works,
  it's too long.
- **Link to e-shop pages when you can.** If a change adds a new page or updates
  an existing user-facing page/section, and you know the live URL, link it so the
  reader can click straight to it (see the link syntax in section 4):
  `- New [size guide](https://shop.example.com/size-guide) page in the footer`.
  - Find the base URL without guessing: check the repo for it (`.env` `APP_URL`
    / `APP_FRONTEND_URL`, `package.json` `homepage`, a config or constants file,
    or the production domain in deploy config). If you genuinely can't determine
    it, ask the user once for the storefront base URL, or skip the link rather
    than invent a domain.
  - Build the full URL from the base plus the route the change touches (e.g.
    base `https://shop.example.com` + route `/exclusive-club` →
    `https://shop.example.com/exclusive-club`). Only link routes you can see in
    the commit/diff or that the user confirms. Never fabricate a path.
  - Link the most specific page that changed, not the bare homepage. For
    back-office/admin-only pages, link only when it's genuinely useful.
- Respect global doc style: **no em-dashes** and no sentence-joining hyphens;
  rephrase with periods, commas, or parentheses.
- For Slovak output, write natural Slovak (not a literal translation), and keep
  product/section names (Exclusive Club, "looks", special box) as the team uses them.

## 4. Output format (Slack mrkdwn)

The changelog is meant to be **pasted into the Slack message composer** by a
human. That target matters: Slack has two different formatting dialects, and
they disagree about links.

- The **composer** (what a person types or pastes) is what this skill targets.
- **API mrkdwn** (`chat.postMessage`, Block Kit) uses `<https://url|text>` for
  links. That syntax renders as literal text in the composer. Never use it here.

Syntax rules for the composer:

| Purpose | Use | Never use |
| --- | --- | --- |
| Bold | `*text*` (one asterisk) | `**text**` |
| Italic | `_text_` | `*text*` |
| Strikethrough | `~text~` | `~~text~~` |
| Inline code | `` `text` `` | (same, this one is fine) |
| Link | `[text](https://url)` | `<https://url\|text>` |
| Heading | a bold line, see below | `#`, `##`, `###` |

Structure rules:

- **Title**: a single bold line with the date range / scope, then a blank line.
  Slack has no headings, so the title is just bold text.
- **Sections**: a bold label on its own line (`*Shopping experience*`), with a
  blank line before each one.
- **Bullets**: `-` at the start of the line. Slack converts these to real
  bullets. Nest up to 3 levels deep by indenting **with spaces, never tabs** (two
  spaces per level); tabs break the nesting. Only nest when it adds clarity; keep
  flat lists flat.
- **Links**: `[Exclusive Club](https://shop.example.com/exclusive-club)` for new
  or changed e-shop pages when the live URL is known (see the linking rule in
  section 3). The composer converts this to a real hyperlink. A link inside a
  bullet is fine.
- Bare URLs with no label can be pasted as-is; Slack auto-links them.
- Use `inline code` for version numbers or literal labels when helpful.
- **Always output directly in the chat. Never write it to a file.** Print it
  inside a single fenced code block so the raw mrkdwn survives copy-paste.

If the user explicitly asks for Markdown (`/changelog md`, "as markdown", "for
GitHub"), output GitHub-flavored Markdown instead: `##` title and `**bold**`
section labels. Lists and links are written the same way in both.

Example shape (Slack mrkdwn):

```
*Changelog (unreleased: main → develop)*

*Shopping experience*
- New [Exclusive Club](https://shop.example.com/exclusive-club) page, with product cards that match the regular e-shop layout ([#1231](https://github.com/acme/shop/pull/1231))
- Limited editions show in-stock products first ([#1236](https://github.com/acme/shop/pull/1236))
- New "Sale" badge on discounted product cards ([#1240](https://github.com/acme/shop/pull/1240), [#1244](https://github.com/acme/shop/pull/1244))
  - Shows the exact percentage off
  - Hidden once a product sells out
- Main navigation menu reordered, with a clearer "My account" dropdown ([#1242](https://github.com/acme/shop/pull/1242))
  - Account dropdown now groups orders, wishlist, and settings
    - Wishlist count appears as a small badge next to the icon
- Homepage hero banner now links straight to the active campaign ([#1245](https://github.com/acme/shop/pull/1245))

*Speed*
- Storefront and account pages load faster ([#1238](https://github.com/acme/shop/pull/1238))
- Product listing filters apply without a full page reload ([#1243](https://github.com/acme/shop/pull/1243))

*Under the hood*
- Stronger sign-in security: login sessions expire reliably and sign-in is limited to the approved company domain (auth, [#1248](https://github.com/acme/shop/pull/1248))
- Daily backups now exclude session data and secrets, so backups are smaller and safer
- Payroll code consolidated into one shared module, reducing duplication (payroll, [#1247](https://github.com/acme/shop/pull/1247))
```

## Argument cheatsheet

There is one unified style for everyone. The options are language (defaults to
Slovak) and output format (defaults to Slack mrkdwn).

- `/changelog` → default: main vs develop (unreleased), Slovak, Slack mrkdwn
- `/changelog sk` → unreleased, Slovak
- `/changelog en` → unreleased, English
- `/changelog today` → today's commits, Slovak
- `/changelog yesterday sk` → yesterday, Slovak
- `/changelog v2.0.0..HEAD` → explicit range (Bash), Slovak
- `/changelog md` → GitHub-flavored Markdown instead of Slack mrkdwn
