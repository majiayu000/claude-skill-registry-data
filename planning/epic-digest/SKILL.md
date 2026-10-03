---
name: epic-digest
layer: method
description: Generate a daily "where are we?" digest from this repo's GitHub epics — a render-only HTML + plain-text email summarising the last 24h of activity plus a progress snapshot of every open epic. Use when asked for a "daily digest", "epic report", "status rapport", "what moved this week", or "where are we on the epics".
allowed-tools: mcp__github__search_issues, mcp__github__list_issues, mcp__github__issue_read, Read, Write, Bash
---

# Epic Digest — the daily "where are we?" email

Turns the GitHub issue tree (`FriendlyInternet/nuxt-crouton`) into a **skimmable digest**: a
**"🧪 Needs your eyes"** band up top (what *landed*, one skimmable line per item — title, type
badge, 👁 for visual changes, PR/preview link — with the How-to-test steps folded into a
tap-to-expand `🧪 How to test (N)` dropdown so the band stays light on mobile), then a short
"since yesterday" activity band, then one card
per open **epic** with a progress bar and a one-line status — the sub-issue breakdown tucked
into a collapsible section so the overview stays clean. Built to be **read at a glance, drilled
into if needed**.

**Interactively this is render-only.** A by-hand run *makes* the digest (HTML +
plain text under `writeups/reports/`) and shows you where it landed. The
**scheduled** job is what delivers — by **email** via Resend (see below).

## When to use
- A daily/weekly "where are we?" check, a status rapport, or "what moved".
- Before a planning session, to see which epics are close to done or blocked.
- **Skip** if you just need one issue's detail — open the issue directly.

## What it produces
| Artifact | Path |
|----------|------|
| HTML digest (forward / view in browser) | `writeups/reports/epic-digest-<YYYYMMDD>.html` |
| Plain-text digest (terminal / paste into email) | `writeups/reports/epic-digest-<YYYYMMDD>.txt` |

These are **generated artifacts** — render them on demand; don't commit them.

## Step 1 — Pick the window
Default is the **last 24h**. For a Monday digest covering the weekend, or a weekly,
widen it: compute the cutoff date (e.g. `2026-06-17`) and use it in the searches
below. Set `windowHours` in the data accordingly (24 / 72 / 168).

## Step 2 — Gather the data (GitHub MCP, read-only)
Build the JSON object described in **Step 3** using these calls (all `owner: pmcp`,
`repo: nuxt-crouton`):

1. **Open epics** — `search_issues`, query `repo:FriendlyInternet/nuxt-crouton is:issue is:open label:epic`.
2. **Each epic's children** — `issue_read` with `method: get_sub_issues`. Count
   `done` = children with `state: "closed"`, `total` = all children. Read each
   child's labels (or the `get_sub_issues` state) to set its `status`
   (`in-progress` / `blocked` from the `status:*` label) and `state`.
   Mark the epic `blocked` if it carries `status:blocked` or any child is blocked.
   **Initiatives (super-epics).** Among the `label:epic` results, treat an issue as an
   **initiative** if it carries `label:initiative` **or** its title starts with `Initiative:`.
   An initiative *groups other epics*: parse its member epic numbers from the `#NN` links in
   its body's `## Member epics` / `## …constituent epics` section (that section only — a `#NN`
   in a prose/"consolidation" section is not a member), keep only those that are themselves
   gathered open epics, and roll them up into an `initiatives[]` entry (`epicsTotal`,
   `activeCount`, `blockedCount`, `childrenTotal`/`childrenDone` summed from the members, and a
   `members[]` list of `{number,title,url,done,total,status,blocked}`). **Remove initiatives
   from `epics[]`** so they don't render as misleading `0/0` epics. `gather.mjs` does all this
   deterministically; the interactive flow mirrors it.
3. **Activity in the window** (the "since yesterday" band) — use date-filtered search,
   substituting `<cutoff>` (YYYY-MM-DD):
   - Closed: `search_issues` → `repo:FriendlyInternet/nuxt-crouton is:issue is:closed closed:>=<cutoff>`
   - Opened: `search_issues` → `repo:FriendlyInternet/nuxt-crouton is:issue created:>=<cutoff>`
   - Merged PRs: `search_issues` → `repo:FriendlyInternet/nuxt-crouton is:pr is:merged merged:>=<cutoff>`
     (note: `search_issues` is scoped to issues; for PRs use `mcp__github__search_pull_requests`
     if available, else `list_pull_requests` filtered client-side.)
4. Write the **human lines** per epic — these are the heart of the digest, the part a
   busy person actually reads. We write issues as **hypotheses** (see the `github-tasks` skill),
   so the digest surfaces the hypothesis and its signal. Keep them plain English, no file paths,
   no jargon:
   - `theHypothesis` — the epic's hypothesis, pulled from its "## Hypothesis" (or legacy
     "## 🎯 The bet") / "We think that…" line: *if we do X, then Y will happen — and Y is
     what we want*. This is the lead line.
   - `weWillKnowBy` — the hypothesis's signal, from the epic's "We'll know by…": how we'll know
     the assumption paid off (a measurable/checkable outcome).
   - `whereWeAre` — the **current status in plain words**: what's done, what's next, any
     blocker. This is where the last-24h movement gets folded in.
   - `whatItIs` (optional) / `recentActivity` (optional) — back-compat fallbacks: `theHypothesis`
     falls back to the legacy `theBet`, then to `whatItIs`; `whereWeAre` falls back to
     `recentActivity`. Prefer the hypothesis-framed fields.

5. **Loose tickets** (the "no epic" band) — open issues tracked under *no* epic, so
   they don't vanish from the roundup. `search_issues` →
   `repo:FriendlyInternet/nuxt-crouton is:issue is:open -label:epic`, then **drop anything with a
   `parent_issue_url`** (those already roll up under an epic). For each survivor keep
   `number`, `title`, `url`, and its `type:*` label (as `type`). The renderer groups
   them by type so a pile of chores reads as one block. Omit the section entirely when
   there are none — re-parent strays into epics first; this only catches the genuinely
   standalone.

6. **Actionables** (the "🧪 Needs your eyes" band) — the things that *landed* and want the
   owner's eyes, each carrying the human **How to test** steps the author already wrote (no
   LLM needed — every closeable PR/issue is required to have a `## 🧪 How to test` section):
   - **Merged PRs in the window** — for each, read its body, pull the `## 🧪 How to test`
     section into `testSteps` (a list of plain step strings). Set `hasVisual: true` if the PR
     touched a UI surface (a `.vue`/`.css` file, `app/components|layouts|pages/**`, `crouton-themes`/
     `crouton-editor`) or carries a `ui-approved` / `ui:*` label. Capture a `previewUrl` if the
     body links a `*.pmcp.dev` / `*.friendlyinter.net` URL. `label` = `<type> · merged` from the
     conventional-commit title (`fix · merged`).
   - **Epics that hit 100% but are still open** (done = total, awaiting QA + close) — one
     `kind: "epic"` actionable whose `testSteps` come from the epic's `## 🧪 Verify the whole thing`
     rollup comment.
   - Keep an item even with no steps — the renderer shows a "_author should add 🧪 How to test_"
     nudge rather than dropping it. Omit the whole section only when there are no actionables.

Keep the rest lean: titles, numbers, URLs, states. (Actionables are the one place we *do* read
PR/rollup bodies — that's where the test steps live.)

## Step 3 — Write the data file
Write the gathered object to a temp path (e.g. `writeups/reports/.epic-digest.data.json`).
Shape (`example.data.json` next to this skill is a complete, renderable sample):

```jsonc
{
  "generatedAt": "<ISO now>",
  "windowHours": 24,
  "repo": "FriendlyInternet/nuxt-crouton",
  "activity": {
    "opened":    [{ "number": 358, "title": "...", "url": "https://github.com/...", "kind": "issue" }],
    "closed":    [{ "number": 351, "title": "...", "url": "...", "kind": "issue" }],
    "mergedPRs": [{ "number": 352, "title": "...", "url": "...", "kind": "pr" }]
  },
  "actionables": [                        // optional — the "🧪 Needs your eyes" band (rendered first)
    {
      "number": 391, "title": "...", "url": "https://github.com/...",
      "kind": "pr",                       // "pr" (merged) | "epic" (hit 100%, do one QA pass)
      "label": "feat · merged",           // optional badge; epics default to "✓ Epic complete · do one QA pass"
      "hasVisual": true,                  // → 👁 visual-change badge + preview link
      "previewUrl": "https://velo.pmcp.dev/bookings",   // optional
      "testSteps": ["Open Bookings…", "Each row shows a status pill", "Filter by pending → amber only"]
    }
  ],
  "initiatives": [                        // optional — the "🎛 Initiatives" band (super-epics grouping epics)
    {
      "number": 1632, "url": "https://github.com/...",
      "title": "🎨 Visual Layout & Builder",   // the "Initiative:" prefix is stripped
      "epicsTotal": 5, "activeCount": 2, "blockedCount": 1, "blocked": true,
      "childrenTotal": 31, "childrenDone": 14,  // summed across member epics
      "members": [
        { "number": 983, "title": "...", "url": "...", "done": 7, "total": 12, "status": "blocked", "blocked": true }
      ]
    }
  ],
  "epics": [                              // regular epics only — initiatives are pulled out into `initiatives`
    {
      "number": 249, "title": "...", "url": "https://github.com/...",
      "status": "in-progress",          // in-progress | blocked | open | done
      "blocked": false,
      "total": 5, "done": 4,            // sub-issue counts → drives the progress bar
      "theHypothesis": "We think that if we do X, then Y will happen — and Y is what we want.",
      "weWillKnowBy": "The signal that tells us the hypothesis paid off.",
      "whereWeAre": "Plain status: what's done, what's next, any blocker.",
      "whatItIs": "(optional, back-compat) → theHypothesis falls back to this.",
      "recentActivity": "(optional, back-compat) → whereWeAre falls back to this.",
      "children": [
        { "number": 254, "title": "...", "url": "...", "state": "open", "status": "in-progress" },
        { "number": 253, "title": "...", "url": "...", "state": "closed" }
      ]
    }
  ],
  "loose": [                            // optional — open issues under no epic, grouped by type
    { "number": 322, "title": "...", "url": "https://github.com/...", "type": "chore" }
  ]
}
```

## Step 4 — Render
```bash
node .claude/skills/epic-digest/render.mjs writeups/reports/.epic-digest.data.json
# options: --out-dir DIR   --date 20260618   --format md   (default: out-dir=writeups/reports, date=today, format=all)
```
Dependency-free (no npm deps, no network). Default writes the `.html` + `.txt`;
`--format md` writes a GitHub-flavoured `.md` instead (used by the daily job).

## Automated daily run (no LLM)
The interactive flow above gathers via GitHub MCP. The **scheduled** daily digest
runs entirely deterministically — `.github/workflows/epic-digest.yml` (cron
`0 5 * * *`, ~06:00 Europe/Brussels) does:
```bash
GITHUB_TOKEN=… node .claude/skills/epic-digest/gather.mjs > digest.data.json   # API → same JSON shape
node .claude/skills/epic-digest/render.mjs digest.data.json --out-dir .         # email-safe HTML + .txt
# → email the HTML (+ text mirror) via Resend
```
- **`gather.mjs`** parses `Hypothesis` (or legacy `The bet`) / `We'll know by` from each epic body and
  **computes** `whereWeAre` from child counts — no model in the loop. It also detects **initiatives**
  (super-epics; `label:initiative` or an `Initiative:` title), rolls their member epics up into
  `initiatives[]`, and removes them from `epics[]` — no model in the loop.
- **Delivery is email-only, via Resend** (#551). The job emails the rendered HTML
  (+ text mirror) when `secrets.RESEND_API_KEY`, `vars.RESEND_FROM` (shared with the
  red-team daily) and `vars.DIGEST_REPORT_EMAIL` are set; unset ⇒ the step warns and
  skips so the job stays green. The old standing-issue comment rail was retired (it
  produced duplicate GitHub-notification mail).
- The render is the same `render.mjs`, so the hand-run and the cron stay in lockstep.

## Step 5 — Hand off
- Show the user where the files landed and a short text summary of the headline
  numbers (epics, closed, PRs merged).
- HTML is for forwarding / browser viewing; text is for pasting into an email or
  reading in a terminal. (Optional: render the HTML to a PNG with
  `.claude/skills/ui-proposal/render.mjs <html> screenshots/epic-digest.png` to
  preview it inline.)

## Conventions & gotchas
- **Actionables surface, don't author.** The "Needs your eyes" steps come verbatim from each
  PR/epic's required `🧪 How to test` / `🧪 Verify the whole thing` section. If an item lands
  with no steps, that's a signal the *author* skipped the required section — the nudge in the
  digest is intentional, don't paper over it by inventing steps.
- **Epics are the unit.** Lead with epics + progress, not a flat issue list — that's
  the whole point ("focus on epics").
- **Interactive = render-only.** A by-hand run just writes files and shows them; the
  *scheduled* job is what delivers (emails via Resend, see above).
- **`<details>` in email:** the collapsible sub-issue section renders expanded in
  mail clients that strip `<details>` — that's fine, it degrades gracefully.
- The renderer sorts **blocked epics first**, then by % complete, so attention
  lands where it's needed.
