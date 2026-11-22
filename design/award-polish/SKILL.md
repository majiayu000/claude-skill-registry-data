---
name: award-polish
description: 'Use for a website, web app, landing page, prototype, or other browser UI when the request says "build a website / landing page / web app / prototype / app interface to award level", "polish", "redesign", "stand out through visuals / interaction / motion", "everyone has the same features, how do we do better", "keep improving until nothing is left", or "use Awwwards as the bar", or when a timed take-home, portfolio, or hackathon web project needs finishing. Includes an optional helper to split polish changes into reviewable commits. Not for prose, documents, or non-web work.'
version: 1.0.4
license: MIT
homepage: https://github.com/Ekko237/award-polish
allowed-tools: Read Write Edit Grep Glob Bash Agent WebFetch
permissions: [network, Write]
---

# award-polish: polish an interface toward award level

Given the same brief, everyone ships about the same features; the gap comes from visuals, UI, motion, smoothness and interaction. The finish line is real users finding it **easy to use, good-looking and smooth, and wanting to come back**. Every change must say which part of the product it makes better.

**The top goal is Awwwards award level**; every other rule is a floor. design-taste-frontend, the polish checklist and the written checks guard against "looks AI-made, has errors"; clearing the floor is not reaching the goal. Scoring, finishing and review references are always Awwwards. Bold techniques common on award sites (custom cursors, scroll storytelling, kinetic type, vertical text, full-screen transitions) are off by default in the taste skill; use them when all three hold: they grow out of the product's core concept; a reference award site uses something similar; they do not hurt usability, performance or reduced-motion. Write the reason in the log; if reviewers call it showing off, remove it.

## When to use

Use this skill for a website, web app, landing page, prototype, or other browser UI when the request says "build a website / landing page / web app / prototype / app interface to award level", "polish", "redesign", "stand out through visuals / interaction / motion", "everyone has the same features, how do we do better", "keep improving until nothing is left", or "use Awwwards as the bar". Also use it when a timed take-home, portfolio, or hackathon web project needs finishing. Do not use it for prose, documents, or non-web work.

It covers a new site and a redesign of anything that runs in a browser: websites, web apps, prototypes, and tablet or phone app interfaces. The sections below are the workflow: study award sites of the same kind, polish on localhost in batches of goal, process, check and iterate, score each batch on 10 items with two reviewers who did not build it, on one shared ruler, with a blind side-by-side against the best version so far. Before/after images go to the user on the schedule in User checkpoints. Ship only when it is good. Deploy first only when a reachable link is required up front and the user has explicitly confirmed that deploy. Finish, stuck, and deadline stops are in When to stop.

## Pick a mode (decide from the project)

Decide the mode from the project and write it on the first line of the log. Choosing a mode is a design decision and stays autonomous. Destructive, irreversible, deploy, and publish actions need an explicit yes from the user before they happen.

| Situation | Mode |
|---|---|
| No site yet, or the request says "build", "from scratch", "new site" | **1 New site** → `references/mode-new.md` |
| A website, web app, or other browser UI that already opens, and the request says "polish", "redesign", "improve", "stand out" | **2 Redesign** → `references/mode-redesign.md` |

When unsure, look at the part you own: if it already has a page that opens, mode 2; if it is empty, mode 1 (a team repo exists but your part starts from zero: mode 1). Write the mode on the first line of the log. For hackathons, team work or owning one part, pick the mode as usual and also read `references/hackathon-team.md`; where they conflict, it wins.

The two modes start differently; after that both go: study the bar → polish in a loop → ship and finish.

## Replying to the user

Plain language, 5 lines at most, no headings: what is done, where things stand, what the user needs to do (only what only the user can give: accounts, real material, the go-ahead to ship). Issue lists, numbers and command output go in the log; the reply only says where the log is. Do not end with a multiple-choice question.

## Find the constraints (look them up, no multiple-choice questions)

Look in the conversation and project files (README, ITERATION_LOG.md); where nothing is found, use a sensible default and write it in the log:

- Live URL, repo, local path, how it deploys; **the real deadline** (find it out, do not guess, leave margin).
- Hard constraints: can the domain change, light only or both themes, commit author, backend or paid services allowed, where images come from, fonts, dashes. **Every existing user and project constraint stays.**
- Design rules: if design-taste-frontend is installed, follow it (it may live in the project's `.claude/skills`). Where it conflicts with user constraints, the user wins; note it. It only covers marketing pages and portfolios; back-office parts borrow only its general rules: one accent color, one radius set, loading/empty/error states, button contrast, zero dashes.
- Log: `ITERATION_LOG.md` at the repo root (template `templates/ITERATION_LOG.md`); if the project does not want it public, keep it somewhere local and uncommitted.
- **Budget**: at kickoff, estimate how many rounds this is worth; when tight, fix only fatal and experience problems, or push a branch, write a handoff and continue in a cloud session.
- **Subagents**: reviews, blind tests and small reviews all use your own fresh subagents, a new one each time (if your agent has no subagents, use a separate new agent session for each). Their prompts say to use only a headless Playwright browser, and if it will not start, stop and return the error text; never switch to the user's own browser, desktop control, or install a browser. Check what comes back before counting it. **When the user stops subagents**, the main session scores reviews itself following `references/reviewer.md`, the log says "scored by the main session, not an independent review", and the independent-review finish condition becomes the user approving side-by-side images.
- **Machine**: check memory first (macOS `sysctl -n hw.memsize`, Linux `free -g`). At 8GB or less run one browser job at a time (screenshots, checks, reviews, Lighthouse in sequence, one reviewer at a time).
- **Where the scripts are**: bundled scripts live in `<skill dir>/scripts`. `<skill dir>` is where this skill is installed (for example ~/.claude/skills/award-polish, ~/.codex/skills/award-polish, a plugin's copy, or wherever your agent keeps skills).
- **Network** (frontmatter `WebFetch` and `permissions: [network, Write]`): `seo_keep.py` GETs only the live and local URLs on its command line, and, when `--sitemap` is set, the sitemap linked from the live site, to compare title, description, canonical, hreflang, structured data, and the other search fields, so a redesign can show those fields did not shrink. `wait_live.py` opens the live URL it is given and the stylesheets and scripts that page references, to see when a release is actually being served. `asset_check.py` does not open a connection; it only reads files on disk and uses a path parser to drop the query and fragment from a local reference. Award sites and the site under polish are opened only at addresses the user or the reference list already named.
- **Files** (`Write`): `seo_keep.py --dump` writes the search-baseline JSON for the log. The path is relative and must stay inside the repo or the working directory. Absolute paths and `..` are refused.
- **When the user does not want questions, only results**: make the design choices yourself and write them in the log and report; send side-by-side images without waiting. A destructive, irreversible, deploy, or publish action still needs an explicit yes. Direction-level redesigns (new key visual, type system, color system, site concept) need the user to pick from images; if the user does not look at images, only push the baseline look further.

## Study award-winning sites as the bar (once, keep the notes)

Follow `references/reference-study.md`: pick 6-8 recent award winners of the same kind from Awwwards (SOTD / SOTM), Webby and FWA (tools and back offices: 4-6 award sites plus 3 back-office UIs), open, scroll and click each one, and note what is good, what to borrow, and key screenshots (in `refs/`, uncommitted). Borrow techniques, never copy wording or layouts. Mode 1 studies before design and then makes 2-3 direction mockups for the user to pick; mode 2 studies before touching anything, to find the gaps.

## Polish directions

Details in `references/polish-checklist.md`:

- **Easy to use**: few steps, every page shows at a glance what to do, errors say how to fix them.
- **Copy**: headings, buttons, hints and empty states are design; run a de-AI rewrite pass (e.g. humanizer) when done.
- **Good-looking**: consistent type, whitespace, hierarchy and color, one spacing scale. Pictures (photos, illustrations, scenes, icons that carry meaning) come from an image generator the user has authorized first; anything animated is SVG layered over a generated image; only action symbols like back and close use an icon library. The checklist says what may be sent to a generator. Colors match the site, avoid portraits that look AI-made, diagrams (maps, flows) must read at a glance.
- **Smooth**: no white flash or jump between pages, instant feedback on press, skeletons, touch that follows the finger; short motion that never blocks, respecting reduced-motion.
- **Worth coming back**: progress, growth, small achievements, recaps, shortcuts, done sincerely, no click bait.
- **Signature moments**: pick the key beats of the core flow (first screen, core action done, result reveal, value change, transitions) and polish them until they feel solid, satisfying and worth clicking again.
- **Prototypes for reviewers or demo audiences**: ask whether they want a guide first and only start on yes; the guide points at what to click. One product with a phone and a desktop interface, viewer picks and can switch any time.

If a design cannot say how it makes the product easier, better-looking, smoother or more worth returning to, do not do it.

## The iteration loop

At kickoff copy `templates/POLISH_BRIEF.md` into an uncommitted brief and fill the five parts below for this project; read it before every batch and add anything new the user asks for (it survives context compression).

### 1. Goal

- One line: real users find it easy, good-looking, smooth and worth returning to; it holds up next to the reference award sites. The finish line is section 5.
- Floor: user and project constraints, core flow works, existing features do not regress, the red lines.
- Core concept: one sentence for what only this product has (even a clickable prototype can name its one unique action); originality grows from it.
- Baseline: tag a version the user approved; no later batch may be worse than it.

### 2. What each batch does

1. **Read**: the brief (especially "rejected looks" and "decided not to do") and the latest full issue list in the log.
2. **Filter**: merge and dedupe both reviewers' lists, strike items that repeat those two sections without a new reason, and record them under "not done and why". Direction-level changes stay out of the list and follow "score stuck".
3. **Do**: fix the whole filtered list in one go, fatal first (unusable, white screen, core flow broken, live site down), then experience (hard to use, hard to read, broken on phones, guide unclear), then polish ("what would add 1 point", structural changes, refinement). Only build in between; park what you cannot fix with a reason; for choices like fonts and colors, make candidates and let a small review pick.
   - **Commit each change as soon as it is verified, one change per commit**, with a message saying what it improves; when an item turns out worse, only those commits' changes get edited back. If changes already piled up, split them with `split_commits.py` (`references/scripts.md`).
   - When a flow's behavior changes, rerun every check script (they click the old flow and will stall or screenshot the wrong screen).
   - New hints, buttons and explanations push key elements out of the first screen most often; remeasure every page.
4. **Self-check**: run the pass/fail checks of section 3; fix failures first.
5. **Review**: two independent reviewers on a local production build (`references/reviewer.md`). Review versions come only from commits (`snapshot.py`; projects that build do so from a clean checkout), because files that exist in the working tree but not in the commit are 404s in the snapshot.
6. **Compare**: score and decide with `calibrate.py` (copied into the project's work directory at kickoff, unchanged for the round). On "new best version", `--save`; fatal and experience problems found in this version still go first in the next batch and get fixed before release, without changing the verdict. To revert, edit the worse items back to the best version's look as a new commit on top.
7. **Record**: per section 4, and tell the user in one plain sentence what this batch changed.
8. **Next batch**: start it in the same turn. A scheduled wake-up (ScheduleWakeup in Claude Code, or your agent's equivalent) is only for waiting on outside things (deploys, background reviews) or as a fallback heartbeat (about 1200 s) if a turn ends unexpectedly. When a background review returns, check it and continue in the same turn. While reviewers use the local preview, do not rebuild, restart the preview or start other browser jobs; you may write the next batch's code.

**When the same kind of issue shows up a second time** (a reviewer raises it again, or the user points it out again), turn it into a test, lint rule or check script in the self-check.

**Score stuck**: three reviews in a row in the same band means a direction review (`reviewer.md`, "Direction review"), with directions that avoid the rejected looks. Before merging a direction-level redesign, show the user three columns side by side (before, baseline, new direction; home and key pages; 1440 and 375) and merge and ship only what the user picks (on a content site, a new direction scored 80 by reviewers looked ugly to the people who saw it, and the 74-point batch 4 went back live). If the user does not look at images, skip direction-level redesigns: let a small review pick the cheapest-looking screen, redo it within the baseline look, and compare side by side. Merging is not finishing; the loop continues.

**Shipping**: by default everything stays local until it is good. Pushing a branch that publishes the site is a deploy, and it needs an explicit yes from the user before the push. Deploy-first, staged updates, deploy sources, assembling the best version and post-release checks are in `references/release.md`.

### 3. How to check

Every "pass" needs evidence: screenshot path, measured value, console output, steps a browser automation actually clicked through. Reasoning from code does not count. Script usage is in `references/scripts.md`.

**Pass/fail (every batch; fix failures before raising scores):**
- **Layout check**: 375, 768, 1024, 1280, 1440 (desktop-only back offices use the project's main widths and only check phones do not break), including states after interactions (just posted, selected, expanded, dialogs, toasts, each business state), written as states.json for `layout_check.py --states`.
- **Automated checks**: `layout_check.py` overflow, clipping, truncation, h1 line count, errors, broken images, small text and small tap targets, `--forbid` for banned strings; `asset_check.py` for every local file the site references; code rules (light only means no `dark:`) via grep.
- **Key elements in the first screen**: each page's most important thing (main button, first result, core number) fully in the first screen and not covered by banners or overlays at 375 and at 1440x900, 1536x864 and 1280x800, including the first-visit state (cookie banner, onboarding dialog); integer-scaled canvases measured at device pixel ratio 1 and 2. Use `--keep` and log the y values.
- **Core flow** clicks through end to end.
- **Performance and accessibility**: thresholds and frequency in `polish-checklist.md`.
- **Sound** (sites with sound): `sound_levels.py` clicks every action in the core flow and checks mute gives zero; silent actions, same-kind actions more than 2x apart in loudness, and overlaps above 0.55 go on the list; level files go to reviewers.
- **Blind test** (sites with a guide): a fresh subagent told only "follow the on-screen hints to the end", once on phone and once on desktop; getting stuck or a wrong highlight fails.
- **Overlays on images**: accept by the numbers and the "3-second test" in `polish-checklist.md`.
- **Detail checklist** (page titles, share cards, icons, 404, hover and selected states): before the first review and before every release.
- **Product screenshots embedded in the site**: reshoot with a new file name whenever the app's look or content changes; rotating shots share one height; remeasure annotations.
- **Time-dependent content**: freeze the clock and demo data with `--clock` before screenshots and measurements; fixed test expectations use relative positions, never absolute coordinates.

**Scoring**: 10 items (typography, whitespace, hierarchy, color, motion, micro-interactions, responsive, originality, usability, retention), defined in `references/scoring.md`. Ruler: 10 = top SOTD, 9 = average SOTD, 8 = Honorable Mention, 7 = mature product site, 6 = good template site. Every batch (and before finishing) two fresh reviewers do anchor calibration, averaging and blind comparison with the best version per `reviewer.md`, with model and effort recorded. Self-scores only point the way; they do not count.

**User checkpoints** (AI reviewers can all miss the same thing):
- Every 3 batches and after big visual changes, send before/after of the first screen and key pages (1440, 375) via `side_by_side.py` with a sentence or two, and keep working without waiting.
- When the user finds it ugly, wrong or confusing, stop visual changes at once. If no version is named as the reference, line up several versions for the user to pick (`--urls` with three addresses gives three columns). If one is named, edit the look back to it (non-visual fixes stay), run the five-width check, and send it next to that version; when the user asks to see it before release, hold the push.
- The picked version becomes the baseline, and the log says "no AI score overrides it"; every rejected look goes into "rejected looks". Problems the user sees outrank any review score.

**Signature moments** are not scored; mark them "not started / needs polish / done". Their quality shows in the motion, micro-interactions, usability and retention scores.

### 4. What to record

In the log:
- **Once at kickoff**: mode, constraints, deadline, core concept, reference notes, to-do list ordered by gap, signature moments, spacing scale and colors, key element y values, search baseline (redesigns); when the anchor set is fixed, its screenshot folder and scores.
- **One entry per batch**: batch N · list size · what changed (with commit hashes) · not done and why · reviewer model and effort · calibrated scores · blind comparison verdict (last line of calibrate.py) · signature moment status.
- **Any time**: "rejected looks" and "decided not to do" live in the brief; the log notes when and why; where each set of images sent to the user is and the user's reply.
- **Paused or stuck**: which step, what is not live yet, what comes next. **Finished**: finish conditions checked one by one, the final live version, 3 highlights, what is left.

### 5. When to stop

**Finish** when all of these hold:
- The latest independent review (calibrated, averaged) has all 10 items at 9 or above.
- Every signature moment is "done": clicked by hand on a local production build at phone and desktop width, each with one sentence on how it was done and why it feels solid or satisfying; clicked again live after release.
- It holds up next to the reference sites, and you can name 1-2 things no template has.
- Two batches in a row with nothing obvious left to improve.

Then say "done", with the link and 3 highlights. "Feels done" and "the redesign won the A/B" do not count; check each condition before stopping and write the result in the log.

**Stop early and report**: hard deadline (after the user explicitly confirms the push, push before it and stop once the live check passes, leaving a fix-only stretch before the deadline); the user says stop (wrap up to a working live state, record where you stopped); the live site is broken and rolling back does not save it.

**Change approach and keep going** (unless the brief says to ask when stuck):
- Same problem unsolved for 3 batches: revert to the last working version, note it, park it, work on something else.
- No progress: do a direction review first; if the redesign still does not raise scores, stop and report. If the user does not look at images: after 3 batches of ties or totals within ±1, assemble the best version (`release.md`), ship it on the user's go-ahead and report.
- The same spot flipped back and forth a second time: keep the higher-scored version and add it to "decided not to do".

**Wrap-up**: stop the loop (cancel any scheduled wake-up), stop test servers, restore demo data, remove temp files, turn off keep-awake. On finishing, delete every screenshot this project produced (reviews, checks, anchor set, side-by-sides) and the frozen old builds (they rebuild from branches), and remove preview config entries pointing at them; keep original generated images and prompts. When pausing, keep screenshots (the anchor set is still needed for scoring). **Delete folder by folder** (`rm -r <screenshot dir>`), never by file extension across the work directory: local builds live there too, and `find` with `-delete` ignores `-prune`.

## Red lines

- A live link that has been handed out must always open: the build must pass before shipping; if it breaks, get an explicit yes and push the last good version back first, then fix.
- Pushing a branch that publishes the site is a deploy. Do not push, deploy, or publish without an explicit yes from the user.
- Revert code only by editing it back as a new commit on top; never git revert, reset, checking out earlier commits or restore to rewrite history or overwrite whole files.
- Do not change a delivered domain, repo name or hosting platform, and do not make a public repo private.
- No outside services, analytics or ads the user did not ask for.
- Back up localStorage and other demo data before testing, restore before finishing.
- A changed image gets a new file name; never overwrite a file of the same name.
- The user's scope is the scope: "for reference" means reference only; "change the logo" means only the logo.

## Lessons learned

`references/lessons.md`; skim it before starting.
