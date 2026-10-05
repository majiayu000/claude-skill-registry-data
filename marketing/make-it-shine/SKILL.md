---
name: make-it-shine
description: Polish a public-facing project for launch. Four modes picked upfront via AskUserQuestion (combinable). POLISH = README + LICENSE + .gitignore + CONTRIBUTING + topics + description + issue templates, grounded in actual code via parallel exploration subagents. MARKETING = repo-tied copy (hook, one-liner, tagline, value props, social blurbs, vs-alternatives). RESEARCH = paper variant (CITATION.cff, TL;DR + reproduce-the-paper + checkpoints + results-vs-baselines, academic-crisp voice, research topic taxonomy). SOCIAL = enqueue share snippets for X and/or Show HN via the tech-firehose queue (never auto-posts; hands off drain command). Use on "polish this repo", "ship this", "launch this", "make this shine", "fix my README", "write marketing copy", "announce this", "post about my paper", "Show HN for this", "make it discoverable", "star farming", "research repo". Reads code before writing. No AI slop, no badge salad, no hallucinated features.
---

# make-it-shine

A project's public surface (GitHub page, marketing copy, social post) is its storefront. This skill makes it shine. but only after **actually reading the code**: No hallucinated features. No "Welcome to my project!" intros. No AI slop.

## Hard rules

1. **Read before write.** Spawn parallel Explore subagents to map the repo. Never write a line that isn't grounded in actual code.
2. **Length follows content, not vanity.** If 4 lines explain it, write 4. Most repos need ~150-400 README lines, not 1500.
3. **No AI slop.** No badge salad, no "Welcome to <project>!", no emoji confetti, no "comprehensive solution leverages cutting-edge..." Drop em dashes. Drop AI vocab (delve, crucial, robust, leverage, foster, landscape, tapestry). Voice rules: `references/voice-crisp.md` + `references/voice-warm.md`.
4. **Direct commit to default branch.** Each meaningful change = its own commit so individual pieces are revertable.
5. **Never co-author commits.** Standard.
6. **Confirm destructive actions.** Overwriting existing CONTRIBUTING.md, LICENSE, or force-setting topics. ask first.
7. **Never auto-post.** Social mode enqueues. The user pulls the trigger via the drain command.

## Phase 0. Mode select (ALWAYS first)

Before anything else, ask the user which mode(s) to run via AskUserQuestion (multi-select):

| Mode | What it does | When to pick |
|------|--------------|--------------|
| **polish** | README + LICENSE + .gitignore + topics + description + CONTRIBUTING + issue templates | First-time public polish, "repo looks dead", "ship-ready it" |
| **marketing** | Repo-tied copy: hook lines, one-liner, taglines, social blurbs, value props | "write marketing copy", "give me a one-liner", "tagline help" |
| **research** | Paper variant: CITATION.cff + reproduce-the-paper + academic voice + research topics | "this is for a paper", "research repo", auto-suggested if `scripts/detect_research.sh` returns `yes` |
| **social** | Enqueue share snippets (X, Show HN) via tech-firehose queue | "announce this", "post about my repo / paper", "Show HN for this" |

**Defaults / common combos:**
- Bare "polish this repo" → polish
- "Ship this + announce" → polish + social
- "Post about my paper" → research + social
- "Write copy for this" → marketing only
- "Make this shine" → ASK (could mean polish, polish+social, all-four)

If `scripts/detect_research.sh` returns `yes`, recommend research mode in the question. If `ambiguous`, ask explicitly.

Modes can stack. Phase order below shows which phases run for each mode.

## Phase map (which phases run per mode)

| Phase | polish | marketing | research | social |
|-------|--------|-----------|----------|--------|
| 1 Detect + audit | ✓ | ✓ | ✓ | ✓ |
| 2 Deep exploration | ✓ | ✓ | ✓ (research variants) | ✓ |
| 2.5 Fresh language scan | ✓ | ✓ | skip | ✓ |
| 3 Voice + length | ✓ | ✓ | ✓ (academic-crisp) | reuses prior or asks |
| 4 Write README | ✓ | | ✓ (research skeleton) | |
| 4M Marketing copy | | ✓ | | |
| 5 Ancillary files | ✓ | | ✓ (+CITATION.cff) | |
| 6 Commits + meta | ✓ | | ✓ | |
| 7 Share-snippet enqueue | | | | ✓ |
| 8 Summary | ✓ | ✓ | ✓ | ✓ |

Always track all running phases with TaskCreate.

## Phase 1. Detect + audit (2 min)

1. `scripts/detect_repo.sh` → resolve `owner/repo` from `git remote get-url origin`. If user passed explicit `owner/repo`, use that.
2. `scripts/audit_repo.sh` → key=value report: description, topics, homepage, LICENSE, .gitignore, CONTRIBUTING, issue templates, README size, default branch, primary language, has-tests, has-CI, visibility, stars.
3. `scripts/detect_research.sh` → `research=yes|ambiguous|no` + signal list. If `yes` and research mode NOT in selection, surface as suggestion. If `ambiguous`, ask once.
4. Print audit summary. Don't write yet.

## Phase 2. Deep exploration (5-10 min, parallel)

Spawn **5 parallel `Explore` subagents** in a single message. Sharp, non-overlapping questions. Read `references/exploration-plan.md` for exact prompts.

| # | Question | Returns |
|---|----------|---------|
| 1 | What does this project actually do? Entry points, primary user flow. | "What it is" + "what it does" paragraphs |
| 2 | How is it built? Stack, deps, architecture, data flow. | Stack list, architecture sketch, key abstractions |
| 3 | How does a user install + run it? | Verified install + quickstart |
| 4 | Directory layout + why? | Annotated tree (top 2 levels) |
| 5 | Who is this for? Read commits, issues, demos, naming. The *problem* solved. | Target user + problem statement + differentiators |

Synthesize. Cross-check claims against actual files. No subagent claim through without a source-file reference.

**Research mode swaps Agents 1 and 2** for paper-claim extraction + code-to-paper mapping. See `references/research-mode.md#mode-specific-phase-2-subagents`.

## Phase 2.5. Fresh language calibration (30 sec, skip in research mode)

Pull a small sample of how devs are talking about this topic **right now**: Combats stale training-data slop.

1. Pick 2-4 keywords (project name + stack + domain). Avoid one-word generics ("AI", "agent"). pair them.
2. Run `scripts/fetch_lang_samples.sh "<kw1>"`. Returns recent HN titles, Reddit posts, dev.to articles.
3. Read `references/fresh-language-context.md` for what signals to extract (overused phrases to AVOID, live terminology, cadence, pain points). DO NOT copy phrases verbatim. samples are a tuning fork.
4. Write one synthesis line: `Fresh-lang scan: "agent harness" is the live term, "RAG" framing saturated, short fragments dominate.`

If script errors or returns empty, skip silently.

## Phase 3. Pick voice + length (1 min)

Read `references/voice-crisp.md` + `references/voice-warm.md`. Pick one:

- **Crisp**: libraries, SDKs, CLIs, devtools. Audience = engineers. Repo name is a noun.
- **Warm**: side projects, hackathons, anything with a story. Author talks in first person elsewhere.

Default crisp when unsure. Warm done badly is cringe.

Length tier from `references/readme-skeletons.md`:
- **4-line**: joke repos / single-script tools.
- **1-page** (~80-200 lines). most repos. Default.
- **Multi-section** (~200-500 lines). frameworks, multi-persona projects.
- **Full guide** (500+ lines). only if genuinely a platform.

State the choice in one line: `Voice: crisp. Length: 1-page. README ~180 lines.`

**Research mode** uses the research README skeleton + academic-crisp voice (numbers-over-adjectives, name baselines, declare limitations). See `references/research-mode.md`.

## Phase 4. Write the README (polish + research only)

Use matching skeleton from `references/readme-skeletons.md` (or research skeleton from `references/research-mode.md`). Fill in only what's grounded by Phase 2.

Mandatory checks before save:
- First 3 lines hook the **problem** + outcome. Not "X is a Y for Z".
- All install/build/run commands match what audit + exploration found.
- Badges only if they carry information.
- Demo asset: if visual, check for existing screenshot/GIF; if none, add `<!-- TODO: add demo.gif -->`.
- Compare-table only if there are genuine, named alternatives. Be honest about what they do better.
- Last section: LICENSE link + one-line credit. No begging.

## Phase 4M. Marketing copy (marketing mode only)

Read `references/marketing-copy.md`. Produce a single `MARKETING.md` (or output inline if user prefers) with:

- **Hook line** (≤15 words). what hurts without it, what it gets you. Not "X is a Y for Z".
- **One-liner / repo description** (≤100 chars). lead with the verb, name the outcome.
- **Tagline / sub-hook** (≤80 chars). punchier riff on the hook.
- **3 value props** (1-line each). concrete outcomes, not adjectives.
- **Vs-alternatives framing** (only if named alternatives exist). what you do differently + what they do better.
- **Social blurbs**: one for X (≤280), one for Show HN title (≤80). These feed Phase 7 if social mode also picked.

Voice follows the Phase 3 pick. Fresh-language scan informs which phrases to avoid (anything overused this month). NEVER use AI vocab.

If polish mode is ALSO selected, fold these into the README (hook → first 3 lines, one-liner → repo description, social blurbs → Phase 7).

## Phase 5. Polish ancillary files (polish + research, 3 min each, parallel where safe)

For each audit-flagged missing/weak item:

- **Description** (`gh repo edit --description`). ≤100 chars, lead with verb. See `references/seo-topics.md`. Research: lead with paper title or method + venue.
- **Topics** (`gh api PUT /repos/{owner}/{repo}/topics`). 10-20 topics. Polish: from `references/seo-topics.md`. Research: from `references/research-mode.md#research-specific-topics-taxonomy`. GitHub's #1 search lever. Only real indexed topics.
- **CITATION.cff**: research mode only. Required for the "Cite this repository" button. Template in `references/research-mode.md`. Use `{{TODO}}` placeholders for unknown fields + list in summary.
- **Homepage**: only if real (demo, docs, npm/crates page). No 404s.
- **LICENSE**: if missing, ask which (default MIT). Don't invent.
- **.gitignore**: if missing or stack mismatch, `curl https://www.toptal.com/developers/gitignore/api/<langs>`. Merge into existing, don't overwrite.
- **CONTRIBUTING.md**: only if repo accepts PRs (look at issues / recent contributor activity). ~40 lines max.
- **Issue templates** (`.github/ISSUE_TEMPLATE/`). `bug_report.md`, `feature_request.md`. Skip if <1 issue/month.
- **Social preview brief**: `gh` can't upload (web UI only). Generate spec: "1280×640 PNG, dark bg, project name 96pt, tagline 32pt." Tell user in summary.

## Phase 6. Commit + push (polish + research)

Per-step commits on default branch:

```
docs: rewrite README with project overview, install, architecture
chore: add MIT LICENSE
chore: add .gitignore for Swift + Node
docs: add CONTRIBUTING.md
chore(github): bug + feature issue templates
```

Research adds:
```
docs: research README. TL;DR, reproduce-the-paper, checkpoints, citation
docs: CITATION.cff for "Cite this repository" button
```

Then `scripts/apply_meta.sh` for description / homepage / topics (no commit needed. repo metadata).

`git commit` direct, never `--no-verify`, never co-author. After push, print the live repo URL.

## Phase 7. Share-snippet enqueue (social mode)

**QUEUED, never auto-sent.** Surface drain command, let the user fire.

1. **Draft the snippet** matching voice + fresh-lang. Per `references/star-farming.md#share-snippets`. If research mode also picked, use the variants in `references/research-social-variants.md` (Show HN format, X thread, tagline-only).
2. **Write to** `/tmp/share-<repo-name>.md`.
3. **Ask which platforms** via AskUserQuestion (multi-select): x, hn. Recommend x for builder-facing tools; hn ONLY if Show HN criteria met (working, original, on-topic, ready for scrutiny).
4. **For research repos:** ALSO ask which variant via AskUserQuestion: Show HN announce | X thread (hook + key result + URL) | tagline + repo link. Each variant has different content shape. See `references/research-social-variants.md`.
5. **Enqueue** via `scripts/post_share_snippets.sh /tmp/share-<repo>.md <repo-url> <platforms-csv>`. STAGES into tech-firehose queue at `~/.config/tech-firehose/queue/<id>.json`.
6. **Hand off drain command:** script prints entry id + exact next command (`bun run bin/queue-drain.ts --id=<id> --yes`). Surface clearly.
7. **Do NOT auto-drain.** Even if user says "go ahead and post," prefer one-more-confirmation by having them run the drain command themselves.

Read `references/share-queue.md` BEFORE acting on share-snippet work.

**Hard rules:**
- Never auto-post.
- HN restraint: only if Show HN criteria met. Bad submissions burn karma + the one-shot.
- HN title: ≤80 chars, no "I built", no clickbait, no marketing copy.
- X and HN need Brave with debug port. tell user to run `bash bin/browser-up.sh` once before draining.
- Length: HN ≤80, X ≤280 (auto-thread).

If user declines posting, end with copy-paste-ready snippet in chat. No queue entry.

## Phase 8. Final summary (always)

- Done: changes committed + meta applied + queue entries created.
- Needs human action: social preview upload, demo GIF recording, drain command for queue.
- Repo URL + recommended next click.

## Edge cases

- **Repo already has a great README.** Don't gut it. Propose specific diffs, confirm.
- **Repo is private.** SEO matters less. Ask if public-polish is really wanted.
- **Multiple READMEs.** Detect + ask which. Don't auto-rewrite non-English.
- **Monorepo.** Top-level by default; sub-packages only if asked.
- **`gh` not auth'd.** `gh auth status` first. If fails, tell user `! gh auth login` (session-shell prefix) and stop.
- **Default branch protected.** Branch + PR fallback.
- **Commit-message linter.** Detect `.github/commitlint*` / `commitlint.config.*` and match.

## Files in this skill

**Scripts:**
- `scripts/detect_repo.sh`. resolve owner/repo from cwd.
- `scripts/audit_repo.sh`. current state of README, LICENSE, topics, etc.
- `scripts/detect_research.sh`. score for research signals.
- `scripts/apply_meta.sh`. apply description + homepage + topics via `gh`.
- `scripts/fetch_lang_samples.sh`. fresh dev-language samples (HN + Reddit + dev.to). Phase 2.5.
- `scripts/post_share_snippets.sh`. ENQUEUE share snippets into tech-firehose queue. Phase 7.

**References (loaded on demand):**
- `references/exploration-plan.md`. 5 parallel-subagent prompts. Phase 2.
- `references/fresh-language-context.md`. Phase 2.5 output interpretation.
- `references/voice-crisp.md`. Linear/Vercel-style voice rules.
- `references/voice-warm.md`. indie-hacker voice rules.
- `references/readme-skeletons.md`. 4-line, 1-page, multi-section, full-guide templates.
- `references/marketing-copy.md`. hook lines, one-liners, taglines, value props, social blurbs. Phase 4M (marketing mode).
- `references/seo-topics.md`. GitHub topic taxonomy + description rules.
- `references/star-farming.md`. badges, demo GIF, compare tables, share snippets.
- `references/research-mode.md`. research-repo workflow overrides. Load when research mode picked.
- `references/research-social-variants.md`. 3 share-snippet shapes for research: Show HN announce, X thread, tagline + link. Phase 7 (research + social).
- `references/share-queue.md`. tech-firehose queue model. Phase 7.
