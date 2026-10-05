---
name: content-audit
description: Audit prose against content-design.md for AI-writing tells, voice violations, and register mismatches. Use when asked to audit copy, check content quality, review prose for AI slop, or check writing against the content guide.
icon: spellcheck
displayDescription: "Scans shipped prose against content-design.md: banned words, em dashes, promotional register, first person where the system should be the subject, and rhythm problems no word list catches. Reports each finding with its location, the offending text, and a suggested rewrite. Accepts a page, a data file, or a whole surface as scope."
invoke: ["content audit","audit the copy on [page]","check this prose against the content guide","any AI slop in [file]"]
---

# content-audit

Audit prose against `content-design.md`, and report violations with suggested rewrites.

## When invoked

Use this skill when asked to audit copy, check prose quality, find AI-writing tells, or review text against the content guide — phrases like "content audit", "audit the copy on the homepage", "does this read like AI", "check this against content-design.md".

## Instructions

1. **Determine scope.** Accept one of:
   - A specific file path (a page, a data file, a markdown doc)
   - `case-studies` → the `title` and `dek` fields in `website/src/data/case-studies.json` (shipped copy on /work and the home page), plus the TLDR points in `website/src/data/case-study-tldrs.ts` (the key-claims block atop each /work study — content-design.md's register row owns its rules; `validate-shipped-prose.mjs` build-covers the em dash, register, voice and banned words stay this scope's)
   - `corpus-prose` → the hand-written connective paragraphs inside `scripts/generate-site-corpus.mjs` (the chat model can repeat any of them verbatim to a visitor — its register row holds them to the page-prose bar; the corpus validators screen for leaks, never for voice, so the judgement rules stay this scope's. Fix the generator's strings, never the generated file)
   - `readme` → `README.md` prose. The repo is public, so this is the first thing a stranger reads
   - `skills` → the `displayDescription` frontmatter strings and the `invoke` phrase lists across `.claude/skills/` (both render on /skills — the descriptions as card copy, the invoke phrases as visible chips — so both are published copy; skill instruction *bodies* are out of scope)
   - `website` → user-visible strings in `website/src/app/**` page files; a page slug (e.g. `about`) scopes to that page folder
   - `chat` → the site chat's shipped prose: the greeting in `website/src/components/SiteChat/greeting.ts`, the starter pools in `website/src/components/SiteChat/starters.ts` and the written follow-up fallbacks in `website/src/lib/chat-followups.ts` (chip length is build-covered by `scripts/validate-chat-starters.mjs`; register, voice and banned words stay this scope's), the welcome tagline, the disclaimer line and the locked-model line inline in `SiteChat.tsx`, the model names and one-line descriptions in `website/src/lib/chat-model.ts` (rendered in the composer's picker; unscanned by any validator), the persona and easter-egg strings in `website/src/app/api/chat/`, the notice strings in `website/src/app/api/chat/route.ts`, and the guardrail notices in `website/src/app/api/chat/guardrails.ts` (all visitor-visible; the em-dash half is build-covered through `validate-shipped-prose.mjs`'s module scan, and the guardrail notices' register row is content-design.md's — say what happened and what to do next, never blame the visitor). Every judgement-level rule stays this scope's
   - `covers` → the alt text in the two cover registries, `website/src/data/cover-renders.json` (the case-study covers) and `website/src/data/essay-covers.json` (the essay illustrations). Alt text is read aloud and indexed, so it is shipped copy, and its rule in the guide is its own: describe what the picture shows, never restate the title. Neither file is a page, so the `website` scope misses both
   - `footer` → the sitemap footer's shipped copy: the column titles and copyright in `website/src/components/SiteFooter/SiteFooter.tsx`, and the link labels in `website/src/config/social.ts` (visible on every non-chromeless page, but outside `app/**`, so the `website` scope misses them — the same gap the `chat` scope closes for the panel)
   - `palette` → the command palette's shipped copy: the group labels, per-item descriptions, the ask-chat row's trailing chip label and the search placeholder in `website/src/components/SitePalette/` (reachable from every non-chromeless page, but outside `app/**`, so the `website` scope misses it — the same gap the `chat` and `footer` scopes close for theirs; no validator scans it). The ask-chat row's *label* is the visitor's own typed query — unauthored by design, never a finding — but its trailing chip ("Ask robr0 GPT") is authored copy in scope; the empty state is unreachable (the ask row matches every query), so there is none to audit
   - `nav` → the navigation config's shipped copy: the section and link descriptions, group labels and the mega showcase card's overline, title and description in `website/src/config/navigation.ts` (rendered in the mega panel, the sidebars, the footer's derived columns and the home and DS-landing cards — outside `app/**`, so the `website` scope misses it, the same gap the `chat`, `footer` and `palette` scopes close for theirs; no validator scans it)
   - `page-summaries` → the FAB panel's per-page TLDR copy: the `title`, `text` and chip labels in `website/src/data/page-summaries.json` (`routes` and `essays` maps — rendered to every visitor on the chat FAB's summary panel, but a data file outside `app/**`, so the `website` scope misses it, the same gap the `covers` scope closes for alt text). `scripts/validate-page-summaries.mjs` build-covers length, the full stop and the em-dash ban; register, voice and banned words stay this scope's — its register row lives in the guide's table

2. **Read `content-design.md` first — it is the only rule source.** The Words to Avoid and Patterns to Avoid tables, the Voice rules, the Register by Surface table, and the Microcopy section are the checklist. This skill deliberately maintains no word list and no pattern list of its own: when the guide changes, the audit changes with it. If a rule seems missing, the fix is an entry in `content-design.md` (per its Iteration Guide), never a rule added here.

3. **Scan the scoped prose** and classify every finding at one of three severities:

   **Banned** (the guide allows no use in shipped copy):
   - Hard-ban words and phrases from the Words to Avoid table
   - Em dashes anywhere in shipped copy. `scripts/validate-shipped-prose.mjs` already fails the build on these, so a clean tree means the surfaces it reads are clear and you are checking the ones it cannot judge: the chat's persona and greeting strings, and any prose outside its scope (its doc block is authoritative). Report a hit there as Banned exactly as before
   - Title Case in shipped headings, buttons, or labels
   - First person in surfaces whose register says "None" (check the Register by Surface table for the scoped surface)
   - Emoji, exclamation marks in UI copy, unsourced statistics

   **Rationed** (legitimate in a narrow sense; flag for a density check):
   - Words from the Rationed table — flag every use, note which look literal, and count per page
   - American spellings in prose (colour/color and friends) — never flag code identifiers, token names, CSS properties, or file paths

   **Judgment** (needs a reader, not a regex — quote the passage and say why):
   - Rhythm uniformity: three or more similar-length sentences in a row
   - Rule-of-three adjective stacks, copula avoidance, participial tails, negative parallelism, hedge stacking, elegant variation, bolded-label bullets, summary closers, throat-clearing openers
   - Register mismatches: promotional tone in a neutral surface, a tagline restating its section name, an empty state describing absence instead of the next action

4. **Never flag:**
   - `content-design.md` itself, and quoted examples anywhere (a rule must be able to name what it bans)
   - Skill instruction bodies and `CLAUDE.md` — agent-facing references, out of scope by design (see the guide's Overview)
   - Code, identifiers, token names, class names, and anything inside backticks or code fences
   - Text authored by third parties (external-skill copies keep their upstream voice)
   - The labs rebuilds under `website/src/app/labs/**` and the template screens under `website/src/components/templates/**` (served under `/templates/<slug>`, whether or not they began in labs) — their copy is fictional demo data staging a product screen, excluded from the chat corpus for the same reason, so register and voice rules do not apply to it. The `/templates` index page's own prose is ordinary page copy and stays in scope

5. **For each finding**, output:
   - File path (repo-relative) and line number, or the entry label for JSON surfaces
   - Severity, the offending text, and the guide rule it breaks
   - A suggested rewrite that keeps the sentence's meaning and any links intact

   Format: `website/src/app/example/page.tsx:42 — banned — "a seamless theming journey" → "theming by overriding one primitive"`

6. **Summarise** at the end:
   - Counts per severity, then the strongest single finding
   - If nothing is found: "No content violations found. Prose follows content-design.md."
   - Run the guide's Self-Review Tests over the longest passage in scope and report the result, pass or fail
