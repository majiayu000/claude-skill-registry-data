---
name: readme-doctor
description: Audit a GitHub repo's README against best-practice patterns and produce a prioritized punch list of fixes. Runs a structured review covering hero presence, install-to-first-success length, "what is this in one sentence" clarity, audience-jargon match, scannability, and drift signals (stale versions, dead links, badge sprawl). Read-only diagnostic; opens a PR only when the user explicitly asks.
---

# readme-doctor

Most README problems aren't typos or missing sections — they're shape problems: the hero never lands, install-to-first-success buries the lede, the "what is this" sentence assumes prior context, the badge row is louder than the content. This skill audits a README against patterns that consistently correlate with maintainer outcomes (stars, contributor onboarding, issue quality) and produces a punch list a maintainer can act on in an afternoon.

The skill's quality comes from the **rubric being grounded in the repo's actual audience and category**, not from a generic checklist. A README for a 50K-star framework needs different things than a personal-project utility.

## Phases

1. **Discovery** — pick operating mode (Auto / Semi-auto / Manual, §1.1), input the README, infer the repo's category and audience from the scan, agree on what "good" looks like for this specific repo.
2. **Audit** — walk the rubric, score each criterion, gather evidence (cite line numbers).
3. **Punch list** — prioritize findings P0 (blocking) / P1 (high-leverage) / P2 (nice-to-have), each with a one-line fix.
4. **Optional output** — read-only summary by default; on user request, open a PR with concrete edits.

---

## Phase 1 — Discovery

### 1.1 Operating mode (ask first)

Same three modes as `repo-visuals` — Auto, Semi-auto (recommended), Manual. Use `AskUserQuestion`. Mode affects how many decisions are silent vs surfaced; it does not skip rubric checks.

### 1.2 Input

User may provide:

- **GitHub URL** → `gh repo view` + clone shallow
- **Local path** → read directly
- **Pasted README text** → analyze in place, but the rubric loses any check that needs file-tree context (manifest signals, screenshot presence, `examples/` dir, etc.). Flag these as "skipped — paste-only mode."
- **Nothing** → ask first

### 1.3 Scan (collect before judging)

- README full text + rendered length (lines, words, time-to-scan estimate at 250wpm)
- Manifest: `package.json`, `Cargo.toml`, `pyproject.toml`, etc. — version, description, keywords
- File tree (depth 2): does an `examples/` exist? `docs/`? Image assets?
- Recent commits (last 10): is the repo active? When was last release?
- GitHub signals: stars, topics, open issues count, latest release date

### 1.4 Repo classification (drives rubric weighting)

Categorize the repo from the scan — different categories get different rubric weights:

- **Library / package** — installable, imported by other code (npm, PyPI, crates). Weight: install-to-first-success, concrete example, API stability signal.
- **CLI tool** — terminal-run binary or script. Weight: one-line install, single-command demo, output screenshot/GIF.
- **Framework** — opinionated structure others build on (Next, Rails, etc.). Weight: "why this over alternatives," opinionated example, conceptual model.
- **App / service** — runnable thing, not imported (self-hosted, web app). Weight: deploy story, config surface, screenshot.
- **Standard / spec / docs** — knowledge artifact, not code. Weight: scope statement, navigation, change log.
- **Personal project / experiment** — explicitly unstable. Weight: honest scope, "what this isn't," low-friction trial.

State the inferred category back to the user with one-line evidence ("inferred CLI tool — `bin/` entry in package.json, README opens with a `$ npx` line"). In Auto mode proceed silently; Semi-auto/Manual let the user override.

### 1.5 Audience inference

Who is this README written for? Infer from jargon density, claimed prerequisites, comparison points named.

- **Working developers in the same domain** — assumes vocabulary, optimizes for "do I want this in my project."
- **Newcomers to the domain** — explains terms, shows simple example before deep one.
- **Maintainers / power users** — assumes deep familiarity, optimizes for reference.
- **Mixed** — most common; means the README needs explicit on-ramps for each.

A README that's pitched at the wrong audience for its category is the single most common shape problem. Catch it here.

---

## Phase 2 — Audit (the rubric)

Each criterion: **score 1–5** with one-line evidence and (for any score ≤3) one-line fix. Default 3, evidence required to move.

### 2.1 The "what is this" sentence

The first sentence after the title should answer "what is this thing" without prior context. Test: imagine a stranger landing here from a Hacker News link. Do they know what it is in 10 seconds?

- 5: One sentence, no jargon, names the category and the differentiator
- 3: Says what it is but buries the "why" or assumes prior context
- 1: Slogan, brand-voice, or lists features before saying what it is

### 2.2 Hero presence above the fold

Above-the-fold = first ~25 lines, before any heading deeper than H2. Does the README open with an image, GIF, or visible-output block that makes the project's value legible without reading?

- 5: Visual hero matches the project's identity (CLI: terminal screencast; UI: screenshot; framework: code sample)
- 3: Has a visual but it's generic (logo only, badge row pretending to be a hero)
- 1: No visual; opens with prose or badge sprawl

### 2.3 Install-to-first-success length

Count the lines (or clicks) from "I want to try this" to "I see the thing working." Less is more. Measure as: line of first install command → line of first runnable example → line of first observable output.

- 5: ≤ 3 lines, all copy-pasteable
- 3: 4–8 lines, requires switching contexts (file edits)
- 1: > 8 lines, or requires a full project setup before any output

### 2.4 Concrete example before API docs

Does a runnable, real-world-shaped example appear before the reference docs / option list / config schema?

- 5: Example is realistic (named entities from the domain, not `foo/bar/baz`), runs end-to-end as shown
- 3: Has an example but it's contrived or after the API table
- 1: No example, or example is just `import foo from 'foo'`

### 2.5 Audience-jargon match

Does the jargon density match the audience inferred in §1.5?

- 5: Jargon load matches audience; unfamiliar terms are linked or briefly defined on first use
- 3: Mostly matches but a few terms are introduced cold
- 1: Pitches a tool to newcomers using domain-expert vocabulary, or vice versa

### 2.6 Scannability

Headings, paragraphs, lists, tables — can a skim-reader find what they need in 30 seconds?

- 5: Clear H2s, short paragraphs, tables for comparable choices, no walls of prose
- 3: Has structure but inconsistent heading depth or one big prose blob hides key info
- 1: Wall of text, deep heading nesting, or so many H2s the TOC is unusable

### 2.7 Drift signals

Things that should not be in a README a year later:

- **Stale versions** — hardcoded version numbers in prose (not badges) that don't match latest release
- **Dead links** — broken anchors, removed-org URLs, archived dependencies
- **Badge sprawl** — more than ~5 badges, or badges from defunct services
- **TODO / WIP markers** in shipped sections
- **Outdated screenshots** — UI shown doesn't match current build

Score:
- 5: None
- 3: 1–2 signals
- 1: 3+ signals

### 2.8 "What this isn't" honesty

For non-1.0 / personal / experimental projects: does the README set scope honestly? "This is a weekend project. It works for X. It will not handle Y."

- 5: Explicit scope statement; unsupported cases named
- 3: Stable / production framing implied but not earned
- 1: Personal experiment pitched as production-ready

(Skip this check for repos clearly past 1.0 with active maintenance.)

### 2.9 Contribution surface

For repos that want contributors: is there a low-friction on-ramp? `CONTRIBUTING.md`, "good first issue" labels, dev-setup section?

- 5: Clear contribution path with at least one named entry point
- 3: `CONTRIBUTING.md` exists but is generic boilerplate
- 1: No contribution surface, but the repo otherwise reads as wanting contributors

(Skip for repos that explicitly don't accept contributions.)

---

## Phase 3 — Punch list

Convert scored criteria into a prioritized list:

- **P0 (blocking)** — score ≤ 2 on §2.1, §2.2, §2.3, or §2.4. These are the criteria that determine whether a stranger-from-HN tries the repo at all.
- **P1 (high-leverage)** — score ≤ 2 on any other criterion, OR score = 3 on a P0 criterion.
- **P2 (nice-to-have)** — everything else with room to improve.

For each item: **what's wrong** (one sentence, citing line numbers), **why it matters** (one sentence tied to the inferred audience), **suggested fix** (one sentence, concrete enough to act on).

Display the punch list grouped by priority. In Auto mode, also output an overall README health score (simple average of the rubric × 20 = /100).

---

## Phase 4 — Optional output

By default this skill is **read-only**. The punch list lives in the chat.

If the user asks ("write the fixes," "open a PR," "apply P0/P1"):

1. Confirm scope (which priority tier, which specific items)
2. Edit `README.md` locally — minimal diffs, one item per commit ideally
3. Same upstream-PR machinery as `repo-visuals` Phase 5: detect ownership, fork if needed, open PR with the punch list as the PR description, alt-text where relevant

Never auto-apply edits without explicit user confirmation. This skill's value is the diagnosis; the surgery is the user's call.

---

## What this skill does NOT do

- Does not rewrite the README in the maintainer's voice — that's a different skill (and risky)
- Does not auto-open PRs — only on explicit ask, and only after showing the diff
- Does not score visual quality of screenshots/GIFs (that's `repo-visuals`'s job)
- Does not lint markdown syntax (use `markdownlint` for that)
- Does not generate badges or shields.io URLs
