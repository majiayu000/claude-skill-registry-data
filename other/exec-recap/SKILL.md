---
name: exec-recap
description: Summarizes what shipped in a version range, date range or commit range as a plain-language TLDR for a non-technical executive who has never seen the project. Use when the user asks for a TLDR, recap, summary or "what changed" for executives, leadership, stakeholders or a non-technical audience, across versions ("1.6 to 1.7"), a time window ("last two days", "since Oct 1") or commits ("since a1b2c3d", "between two hashes").
---

# Exec recap

Turn a range of work into a recap a busy executive who has never heard of the product reads in under a minute. Every claim traces to a release note, merged PR or commit; the wording carries none of the engineering.

## 1. Pin the range

Run `git fetch --tags` first, then resolve the request into two lists: the **releases** in range and the **commits** in range on the main branch (`origin/main`; when development and public repos are split, use the one the user points at). The user's wording picks one of three kinds:

- **Versions** ("from 1.6 to 1.7.1", "since 1.5"). Read the release list (`gh release list -L 50`; no GitHub releases: tags plus `CHANGELOG.md`). **From** = the first release of the starting line ("from 1.6" means 1.6.0); **To** = the version named, or the latest release when none is. If **To** is not released yet, the recap ends at the latest release and the first line says so plainly ("The latest release is 1.7.0. There is no 1.7.1 yet."). Commits = `<tag before From>..<To>`, plus `<latest-tag>..origin/main` as pending work.
- **Dates** ("last two days", "this week", "since Oct 1", "Oct 1 to Oct 7"). Calendar days in the user's local time zone, today counted as day one ("last two days" = yesterday and today); an open end runs to now. Releases = those whose `publishedAt` falls in the window (`gh release list -L 50 --json tagName,publishedAt`; `publishedAt` is UTC, so convert to the user's zone before comparing). Commits = `TZ=<user zone> git log origin/main --since=<start 00:00> --until=<end 23:59>` (git reads the window in the process time zone).
- **Commits** ("since a1b2c3d", "between a1b2c3d and e4f5a6b"). Confirm each hash exists (`git cat-file -e <sha>^{commit}`) and that the first is an ancestor of the second (`git merge-base --is-ancestor A B`; swap them when given in reverse). "Since A" = `A..origin/main`, A itself excluded; "between A and B" = `A..B`. Releases = tags in that span (`git tag --merged B --no-merged A`); a release tagged on A itself stays out, like A.

A hash that is missing, a window with no commits, or two hashes on unrelated histories: stop and say which, in one line. Done when both lists are written down with dates (your working notes; the recap carries only the dates in its title).

## 2. Gather the facts

- Read the notes of every release in the range: `gh release view <tag> --json body -q .body`. Notes already in this conversation count as read.
- Read every commit in range that no release covers: `git log --format='%h %ad %s%n%b' --date=short <range>`, and the merged PR body behind it when there is one (`gh pr list --state merged --search <sha>`). This work becomes themes like any release, and the status line names which themes are finished but not yet released. With nothing pending, the status line says so in a few words.
- Status facts come only from evidence in this session, the artifacts (release notes stating builds are attested count), or the user's own word: where it is installed and verified, build attestation, what is pending. A fact you lack is left out. When the installed release is newer than the range's end, say "the latest release, which includes all of this".
- Done when each release-note bullet and each uncovered commit in range is accounted for: used in a theme, or dropped as invisible to an executive (checksums, upgrade commands, version bumps, CI, docs-only changes, internal refactors with no visible effect).

## 3. Write it

Format, in this order:

1. **First line**: the range as resolved, in the user's terms ("Here's 1.6.0 through 1.7.0:", "Here's Oct 6 to 7, five releases:", "Here's everything since a1b2c3d (Oct 6):"), plus the unreleased-version note from step 1 when it applies.
2. **Title**, bold: `<Product>, <first date> to <last date>: what changed`, dates taken from the first and last release or commit in range (one date when they fall on the same day), with the month written once when both dates share it ("Oct 6 to 7").
3. **Orientation**, two sentences: what the product does for its users, in words an outsider knows; how many updates shipped in the range (releases, or changes when the range is mostly unreleased commits) and their overall theme (reliability, polish, speed).
4. **Themes**, a numbered list of 3 to 5. Group bullets by the benefit people feel, never one item per release. Each item: a bold outcome label of two to four words ("Safer undo.", "Upgrades no longer get stuck."), then one or two sentences on what people notice now. The label covers every sentence under it ("Everyday fixes" when visual and non-visual fixes share an item).
5. **Status**, one bold-labeled line: where it is live and verified, whether downloads are verifiable, and any finished work waiting on the next release.

Plain-language rules:

- Translate every term an outsider would stop on: for example, a plugin becomes "built-in controls", a bundled coding agent becomes "the built-in AI assistant", a config conflict becomes "upgrades got stuck". Product and company names stay.
- Leave out file names, commands, flags, config keys, hashes, issue numbers, and version numbers inside theme items (versions belong only in the first line).
- Describe the effect on people, past to present: "Small windows no longer show a stray colored band at the top."
- Calm, factual verbs. Superlatives and hype words stay out.
- Commas, periods and parentheses carry the punctuation; no em dashes.

## 4. Check before sending

- **Trace**: every theme sentence maps to a release-note bullet, a merged PR or commit in range, or a verified session fact.
- **Outsider read**: reread as someone who never saw the repo; any word that needs a glossary gets translated.
- **Length**: the recap fits on one phone screen, about 200 words.

## Reference: a recap that landed

Range: versions 1.6.0 to 1.7.0. This shows the shape and register. Write each recap's wording fresh from its own range's facts.

> **Herdr Electrified, Oct 6 to 7: what changed**
>
> Herdr Electrified gives a workspace for AI coding assistants (Claude, Codex) a polished, consistent look, and lets people undo it cleanly. In the last two days we shipped four updates focused on reliability and polish.
>
> 1. **Safer undo.** Undo now shows exactly what it will change and asks before doing anything. People can preview it without changing anything.
> 2. **Built-in controls that work.** Check, preview and undo now have keyboard shortcuts inside the app, with results shown in a pop-up window.
> 3. **Upgrades no longer get stuck.** One update blocked people upgrading from the version before it. The next update fixed that, and the release notes now steer people to the latest version.
> 4. **Fewer confusing messages.** The built-in AI assistant stopped offering software updates it could never install.
> 5. **Visual fixes.** Small windows no longer show a stray colored band at the top. The list of running assistants always shows a clear name. Restarting no longer opens the same Claude conversation twice.
>
> **Status:** live on both of our machines and verified, and every download is independently verifiable as built from our public code. One cosmetic fix (the plugin was reporting an old version number) is finished and will go out with the next release.
