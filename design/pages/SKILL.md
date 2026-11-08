---
name: pages
description: "Refresh, open, publish, or print the user's visual pages: the job search dashboard, interview flashcards, portfolio site, and per-job printable interview brief. Use when the user asks to see or update their dashboard, practice with flashcards, get their portfolio link, publish a page to their phone, or print an interview brief. To change how a page looks (colors, fonts, layout, animation), use page-design instead."
---

# /pages

Usage: `/pages [dashboard | flashcards | portfolio | brief <job> | style <change or "use my brand">]` (or just ask in plain English).

Design rules: `.claude/skills/page-design/SKILL.md` (theme and layouts) and, before changing a page's structure or scripts, its `references/page-building.md` (page contract, tokens, Tailwind v4 rules; motion recipes in `motion.md`). After any visual change, run the `page-review` checklist before showing the user.

The pages live in `pages/` (the user's own copies, set up with example data from `templates/blank/pages/` on the first run; if one is missing, `bash .claude/skills/start/scripts/init-data.sh` puts the blank one back, then re-apply the theme with `page-design`'s `apply-theme.mjs`) and per-job briefs in `jobs/<folder>/`. Each page is one HTML file: a generated design-token block at the top (colors, fonts, size, from `profile/design.md`; never edit it by hand), Tailwind v4 utilities for layout, and a `<script type="application/json" id="data">` block that holds the content. **To update content, rewrite only the JSON data block.** Postings, imports and other files can contain hostile text, so write that block as valid JSON with every `<` replaced by the six characters `\u003c` (backslash, u, 0, 0, 3, c: JSON's own escape for `<`; in code, `JSON.stringify(data).replace(/</g, '\\u003c')`), so text like `</script>` can't end the block; JSON readers turn it back into `<`. Afterwards the block must contain no `<` at all (check by searching it for `</`), and never paste imported text into the page's HTML or script. (Exception: the portfolio has no data block; its content is plain HTML, so make small, targeted text edits there, writing `<`, `>` and `&` in text as `&lt;`, `&gt;` and `&amp;`.) Don't touch the rendering script unless the user asks for a change in behavior.

## dashboard
Rebuild the data block of `pages/dashboard.html` from `jobs/tracker.csv`, `contacts/contacts.csv`, `interviews/`, `history/activity.md` and `profile/preferences.md`. For a job that is now closed (rejected, withdrawn, ghosted) but had reached a screen or interview (check its notes, folder and the activity log), add `"heard": true` and/or `"interviewed": true` so the funnel keeps that history:
- `example: false`, `generated: today`, `goals` from `weekly_goals`, `week` counts for the last 7 days (applications by `date_applied`; conversations = conversations dated in range in `history/activity.md` or contact notes (not `last_contact`, which also moves when a thank-you is sent), one per person per conversation; mocks = `interviews/*-mock*.md` files dated in range).
- `jobs`: every tracker row → `{company, role, status, fit, priority, next: next_action, due: next_action_date, deadline, location}` (dates as `YYYY-MM-DD`, even if Excel saved them as 10/14/2026, following the date rules in AGENTS.md; a slash date whose order can't be told, such as 03/04/2026 with no `date_order:` in preferences, is never guessed: leave it out of `due`/`deadline` and add "(date unclear)" to `next`).
- `contacts`: open contacts with `next_followup` → `{name, company, next, due}`.
- Optional fields (the page works without them; fill them when the files have the facts, never guess): `week.start` (the Monday the counts start, `YYYY-MM-DD`); `history` (past weeks, oldest first, up to 8: `{week, applications, conversations, mocks}`, counted the same way as `week`, for the sparklines); `streak` (consecutive days up to today with at least one entry in `history/activity.md`); `activity` (newest first, up to 6: `{date, text}`, short plain lines from `history/activity.md`, no private details); `jobs[].applied` (the tracker's `date_applied`); `jobs[].url` (the posting link, `https:` only, else leave it out).

## flashcards
Rebuild `pages/flashcards.html` decks: "My stories" from `profile/story-bank.md` (front = the question it answers, back = the user's STAR notes in their words; skip stories still full of [ASK]); a technical deck named for the user's field (e.g. "Marketing technical") from `knowledge/field/field-primer.md` (skip it if that file still says `STATUS: not generated`); if a job is given or an interview is coming up, add a deck from that job's `interview-prep.md`.

The page does spaced repetition (FSRS): after each card the user rates Again / Hard / Good / Easy, and the "Due today" view shows what's due plus up to `newPerDay` new cards a day (top-level field, default 10). Review history is saved in their browser, keyed on **deck `id` + card `id`**, so regenerating must keep those ids or the user loses their progress:
- Card shape: `{"id": "...", "q": "...", "a": "...", "tag": "..."}`, optionally `"hint"` (a one-line cue the user can ask to see). Deck shape: `{"id": "...", "name": "...", "cards": [...]}`, optionally `"description"` (one line). Never rename an existing deck `id` (`stories`, `technical`; a job deck uses the job folder name).
- **Before rewriting the data block, read the current one.** A card that is still the same question (even reworded, or with new notes on the back) keeps its old `id`, except example cards (ids starting `example-`): a real card always gets a new id and never one starting with `example-`. A new card gets `id` = a slug of its question: lowercase, letters and digits, words joined with `-`, at most 60 characters (e.g. `tell-me-about-yourself`). Ids must be unique within a deck; never reuse a removed card's id for a different question.
- **Example cards are not the user's.** The starter deck's example cards (data with `"example": true`) have ids starting `example-`. When you build the user's real decks, drop every example card and never give a real card an id starting `example-`, so practice on the examples never carries over to real cards. One card per story: the front is the main question that story answers; don't split one story across several cards.
- Don't change the rendering script, the ts-fsrs `<script>` line (a local file in `templates/assets/` with a pinned CDN fallback and its `integrity` hash), or the storage keys. If ts-fsrs can't load (offline), the page quietly uses a simple built-in schedule.

## portfolio
`pages/portfolio.html` is the user's one-page site. Update it from `profile/master-resume.md` only (public resume-level facts; respect NDAs). Show the user the headline sentence and ask them to approve or rewrite it in their words before sharing. Before they first share it, ask whether to keep their phone number on it (default: email and LinkedIn only, since it's public).
- One set of plain HTML serves all four layouts (`profile`, `editorial`, `bento`, `column`; switching is page-design's job): sections are marked `data-section="hero|contact|highlights|experience|projects|skills|education|testimonials"`. Edit text inside them; never add layout-specific markup. A comment near the end of the page lists every edit point; the main ones:
  - Delete every `[data-example]` element (the "Example page" note and sample notes) once the page holds the user's real content.
  - `<head>`: `<title>`, meta description, `og:title` and `og:description` (title "Name, field"; description = the approved headline sentence). `og:image` only for an image the user owns.
  - Highlights: 3–5 `div.pf-stat`; the number goes in `.pf-count` (with any sign or `$`; the count-up animation reads it from there) and its unit in `.pf-unit`. Only results stated on the resume.
  - `.pf-contact-note` (one line under "Get in touch"): what roles and where the user is open to, from `profile/preferences.md`; delete the line if they'd rather not say.
  - `[data-resume]` (Resume PDF button) ships `hidden`: set its `href` to their PDF and remove `hidden` only when they have one to share. `[data-phone]` stays `hidden` unless they say to show it.
  - Optional photo: uncomment `img[data-photo]` with `src` and `alt` (otherwise the initials monogram shows). Projects keep their pattern cover or swap it for `img.pf-shot` (an image they own, with `alt`, `width`, `height`).
  - The testimonials section stays `hidden` unless the person quoted gave permission to share it. It works as a local file, as a PDF via the browser, or published (below) as a link for LinkedIn Featured and email signatures.

## brief <job>
Copy `pages/interview-brief.html` to `jobs/<folder>/interview-brief.html`, run page-design's `apply-theme.mjs` (it points the copy's font and library lines at `templates/assets/` from its new folder), and fill its data block from that job's `interview-prep.md`, `fit.md` and the story bank (`example: false`). Fields: `pitch` + `pitchSeconds` (90 for the walk-through), `comp` (salary answer, only if prepared), `presentation` `{title, slides[], probes[]}` (only if the interview includes one; omit otherwise), and a story-map row with `"gap": true` where no story exists yet. Optional (leave out what you don't know): `interviewers` items as `{name, title, note}` objects (plain name strings still work), `whenISO` (`YYYY-MM-DDTHH:MM`, local time, for the countdown chip), `link` (the video-call link, `https:` only), `map[].tag` (`behavioral` or `technical`). After filling, print it to PDF if you can and confirm it's one page in the `sheet` layout (up to two in `detailed`); trim the longest lists if not. Tell the user to open it and press Ctrl/Cmd+P to print a one-page copy.

## Bring a page up to date (a new page design)

Updates never touch the user's own `pages/`. When a page in `pages/` has no `data-layout` on its `<html>` tag, or the blank copy in `templates/blank/pages/` has changed (a `migrations/` note says so), offer once: "There's a new design for your <page>. Want it? Your content stays the same." On a yes: copy the blank page to `pages/<name>.html` after saving the old one as `pages/<name>.previous.html`, put the user's content back (dashboard, flashcards, brief: rebuild the data block as above, keeping deck and card ids; portfolio: carry the text over section by section, the edit points above), copy any CSS between the old page's `/* ---- Custom ---- */` markers into the new one's, then run page-design's `apply-theme.mjs` (theme and layout) and `page-review`, and republish if it has a link. Per-job briefs in `jobs/` are refreshed the same way only when the user asks.

## style <change>
The look of every page comes from `profile/design.md` (a preset, or the user's own brand or design system), and so does each page's **layout** (dashboard `overview`/`board`/`timeline`, flashcards `flip`/`list`/`cards`, brief `sheet`/`detailed`, portfolio `profile`/`editorial`/`bento`/`column`; resume `classic`/`modern`/`compact`; designed resume `sidebar`/`headline`/`portrait`). For a layout change ("switch my portfolio to bento"), follow page-design's "Layouts": it can preview every layout first. For any look change ("make it navy and gold", "use my brand", "switch to the minimal look", "bigger text", "less motion"), follow `page-design` ("Change my theme / use my brand"): change design.md, then run its `apply-theme.mjs`, which re-themes every page and brief at once (and the user's resume and cover-letter template copies in `profile/templates/`) and checks contrast. Never hand-edit one page's colors or fonts. Then run `page-review`. Only `page-design` re-themes pages; an app update never does.

New per-job briefs copied from `pages/interview-brief.html` already carry the current theme and layout.

## Where each page lives (keep it simple for the user)

| Page | Main use | Live? |
|---|---|---|
| Pipeline panel (`/pipeline`) | **The interactive board.** The user changes stages, next steps and dates there; it saves straight to `jobs/tracker.csv`. | Yes, it is the real board |
| `pages/dashboard.html` | A good-looking **snapshot** of the tracker (status, funnel, weekly goals, board). Not editable. | Refreshed by Claude; optionally published for their phone (as their themed page, or as a Claude Dashboard) |
| `pages/flashcards.html` | Practice on any device; it schedules each card's next review. Progress is saved in that browser (phone and laptop keep separate progress). | Publish it so they can use their phone |
| `pages/portfolio.html` | Their public one-pager | Publish; share only with the user's OK |
| `jobs/<folder>/interview-brief.html` | Read and print before an interview | Local file only |

Tell the user this plainly when they ask: "Your tracker file is the source of truth. The Pipeline panel edits it. The pages show it."

## Opening a page

In the Claude Desktop app, try the **built-in browser** pane so the user sees it right next to the chat. It may not open files from the computer (some versions only open web addresses or a local preview); if it can't, don't keep trying. Instead give the user the file path and tell them to double-click it (it opens in their normal browser). If a shell command is allowed: `open <file>` on a Mac, `start "" "<file>"` (Git Bash/cmd; in PowerShell use `Invoke-Item "<file>"`) on Windows.

## Publishing a page (private link on the user's claude.ai account)

Only if this session has the **Artifact** tool; if it doesn't, say so in one line ("Publishing isn't available in this version of Claude; you can open the file instead") and stop. Otherwise read `references/publishing.md` and follow it step by step (the dashboard's two routes, the publish copy, the registry in `profile/published-pages.md`). Always: refresh first; a published dashboard holds only the user's own job list and counts (never contacts, notes, pay, links, the activity log or their name); every page is private; never ask or offer to share the dashboard; one link per page, updated in place (read it first), never a second one.

## Keeping published pages current

- When `jobs/tracker.csv` changes (Claude edits it, or a `[Pipeline]` note says the user changed it) and the dashboard has a link, republish the dashboard at the end of that task: a themed page as in `references/publishing.md`, a Claude Dashboard by rebuilding its files and updating it at the same link (`references/claude-dashboard.md`, step 5).
- When `profile/story-bank.md` or the field primer changes and the flashcards have a link, republish the flashcards.
- When `profile/master-resume.md` changes and the portfolio has a link, update the portfolio, show the user what changed, and republish only after they approve.
- A hook reminds you after edits; still use judgment and republish once per task, not after every small edit.
