---
name: dossier
description: >-
  Use when asked to research, survey, compare, evaluate, or investigate any
  topic. Research triggers: research this, brief me on, state of the art,
  market research, survey the landscape, what's out there, how does X work,
  background on. Decision triggers: compare options, evaluate alternatives,
  find the best, product comparison, technology evaluation, which should I use,
  pros and cons, recommendation report, what are my options. Also: dossier.
compatibility: claude-code, cursor
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "1.3.1"
---

# Dossier

Structured research producing cited, well-edited reports. Two genres: **research dossiers** that map the state of a topic so the reader draws their own conclusions, and **decision dossiers** that rank options and recommend one. Optional decision ballots. Works for any domain — tech, travel, health, policy, finance, art.

**Pick the genre before researching — it changes every stage below.** Getting it wrong is the most expensive error this skill can make: it is invisible until delivery, and it cannot be patched by editing, because the two genres want different documents built from the same facts.

## Workflow: SCOPE → GATHER → EVALUATE → SYNTHESIZE → REVIEW → DELIVER

### 0. Preflight — verify the request is actionable, and settle the genre

Before starting research, confirm all three:

1. **Specific** — what to investigate is bounded: a named topic, a concrete comparison, or a clear question. "Look into the X space generically" fails this.
2. **Unambiguous** — contested terms are defined by context. If the request uses a word with multiple plausible meanings and context doesn't resolve which, flag it.
3. **Well-understood** — you can state the objective back to the operator in 1–2 sentences without hedging. If you'd have to pad with "I think you mean…" or "depending on what you want from this…", you don't understand it yet.

If one or more checks fail, **ask before starting**. A dossier built on unclear objectives wastes more research time than the clarifying turn costs. Batch questions; offer choices where reasonable; skip the obvious.

Then settle the genre — a fourth, independent check:

4. **Genre** — does the reader want to *learn the state of a topic and conclude for themselves*, or to *be handed a ranked recommendation*? **Infer it when the request makes it obvious; ask when it doesn't.**

| Request | Genre | Why |
|---|---|---|
| "brief me on the CMS MCP landscape" | Research | Asks about the world |
| "which CMS should we standardise on?" | Decision | Asks for a choice |
| "research X and tell me if we should do it" | Research + assessment | Explicitly both |
| **"evaluate this pitch"** | **Ask** | *Evaluate* reads both ways: "tell me if it's good" and "tell me about this space so I can judge" |
| "what are my options for X?" | Ask | Could be a survey of the field or a shortlist to pick from |

The four ambiguity smells, all of which mean ask: the verb is *evaluate / assess / look into* with no named options; the request names a hypothesis rather than a field; the reader is the author of the thing being researched; or no decision, decider, or deadline is anywhere in the context.

**Note that the actionability tests do not catch this.** "Evaluate this pitch" is specific, unambiguous in its terms, and restatable in one sentence — it passes 1–3 cleanly while leaving the genre wide open. Genre is a separate question from actionability, which is why it is a separate check.

Default when you genuinely cannot ask (async, no reply expected): **research**. It is the recoverable error. A research dossier that omits a recommendation can have one appended in minutes; a decision dossier that adjudicated when the reader wanted to conclude for themselves has to be rebuilt, because the framing is in every heading.

If all four check out, proceed to SCOPE. Do not ask just to perform diligence — the bar is "the answer isn't obvious from context," not "I want to be extra sure."

### 1. SCOPE

- **Genre** (from Preflight 4) — this is not a label. It selects the template and changes EVALUATE and SYNTHESIZE:

| | Research dossier | Decision dossier |
|---|---|---|
| **Template** | `templates/report.md` | `templates/dossier.md` |
| **EVALUATE** | Survey mode — map, taxonomise, grade evidence | Scoring mode — score options against requirements |
| **Key Facts box** | Scope, method, evidence quality, research window | Who decides, decision model, deadline |
| **Headings name** | Subjects | Options and verdicts |
| **Ends with** | What could not be determined | Ranked recommendations |
| **Reader concludes** | Yes — that is the deliverable | No — you conclude, they ratify |

**Research + assessment:** a research dossier may carry an assessment as its **final section**, when the reader asked for one. The survey spine is unchanged; the assessment is confined to the end and clearly labelled, so a reader can take the research and skip the opinion. It never leads, and it never supplies the headings.

- **Requirements:** R1-Rn with weights (Critical/High/Medium) — decision genre only
- **Selectivity:** 5-8 options, not a laundry list — decision genre; for research, selectivity means *coverage of the field*, so state the inclusion rule instead ("every vendor with a documented server, excluding aggregator listings")
- **Decision model** (decision genre, or a research dossier whose assessment feeds a real choice): note who decides, by when, and how — record in the Key Facts box before GATHER. **Do not invent one for a research dossier**; an empty decision model is a signal you picked the wrong genre.
- **Sources:** consult `${CLAUDE_SKILL_DIR}/references/sources-by-domain.md`
- **Output folder:** Check existing `research/` directories first — if one matches the current topic, add to it rather than creating a new folder. Ask the user when unsure. Only create `research/YYYY-MM-DD-slug/` for genuinely new topics.

### 2. GATHER

Dispatch parallel subagents scaled to complexity:

| Complexity | Strategy |
|-----------|----------|
| Quick (1-2 options) | Sequential, no subagents |
| Standard (3-6) | 1 Explore agent per option |
| Deep (6+ or broad) | 1 per option + 3 fact-checkers post-synthesis |
| Architecture decision | 3 Plan agents with named perspectives |

Each agent returns structured findings with URLs for every claim. Check `/last30days` first for topics with social signal (consumer, OSS). Skip for B2B, academic, niche. Pivot to WebSearch if <3 results.

**Dated-claim verification.** Every deadline, CFP date, release-window, or "closes X 2026" claim must be re-verified against a primary source accessed on the production date. Dates stale silently; they are the single most common source of drift in multi-session dossiers. Reviewed via `${CLAUDE_SKILL_DIR}/references/review-checklist.md` (dated-claim-freshness item).

**Source archival.** Capture each cited source to disk — `"${CLAUDE_SKILL_DIR}/scripts/archive-source.sh" <url> <citation-id> <dossier-folder>/sources`. **Assign the citation ID when you collect the URL, not when you write §Sources** — that is what lets archival run here in GATHER rather than becoming a sixth stage. Keep a running URL→ID list as findings come back; SYNTHESIZE then groups those IDs into source categories instead of inventing them. A citation is a promise that someone can check the claim; a bare URL keeps that promise only until the page moves, changes, or 404s, and the sources that rot fastest — forum threads, issues in dormant trackers, vendor pages for discontinued products — are exactly the ones a dossier leans on. The script captures depth-0 (the cited page only, never a site mirror), degrades from `monolith` to `curl` to whatever is present, and **never fails a dossier** — an unreachable source becomes an index row saying so. Two things to know before running it: it flags `thin-capture` on JS-rendered pages it cannot see into, and `--wayback-save` is an **outward-facing publish** to a public archive, never a default. Details in `${CLAUDE_SKILL_DIR}/references/source-archival.md`. Reviewed via `${CLAUDE_SKILL_DIR}/references/review-checklist.md` (source-archival item).

### 3. EVALUATE

Both genres: cross-reference across agents — multi-source citations get highest weight — and flag contradictions.

**Scoring mode (decision genre):**

- Score options against requirements
- Build attribute tables appropriate to the domain

**Survey mode (research genre):** scoring answers "which is best", which is the wrong question here. Instead:

- **Map the field** — state the inclusion rule and what it excludes, so a reader knows what "all of them" meant
- **Establish a taxonomy** — group by a property that carries explanatory weight (hosted vs self-hosted, vendor-built vs community), not alphabetically. The grouping *is* a finding
- **Grade evidence per claim** — distinguish what was verified first-hand from what was taken from a summary, and say which is which in the text. A reader drawing their own conclusions needs to know which facts bear weight
- **Record what could not be determined** — an explicit section, not silence. Gaps are findings; hiding them fakes completeness and quietly removes the reader's ability to judge
- **Note the trap-shaped facts** — self-assigned "official" labels, dead projects still listed in directories, vendor pages describing unshipped roadmap items
- **Flag commercial incentives:** when sources have financial motivation, call this out explicitly in the dossier (e.g. "most links are vendor/affiliate sites") rather than silently discarding them

### 4. SYNTHESIZE

Write the dossier using the template the genre selected in SCOPE — `${CLAUDE_SKILL_DIR}/templates/report.md` for research, `${CLAUDE_SKILL_DIR}/templates/dossier.md` for decision:

- **Key Facts box** (required, one screen). Readers with five minutes read only this section — make every line count. Its fields depend on the genre:
  - **Decision:** who decides, decision model, deadline, hard constraints, audience, 3–5 load-bearing claims.
  - **Research:** scope (and the inclusion rule), method, evidence quality, research window, audience, 3–5 headline findings. **Findings are facts about the world, not verdicts on a proposal** — "eight vendors shipped per-user auth before August 2026" is a finding; "the pitch is not differentiated" is a verdict.
- **Headings name subjects, in the research genre.** A reader skims by heading to find a topic; if the headings are stances, there is nothing to skim for and the document can only be read start to finish. "Per-user auth is table stakes, not a differentiator" is a stance — the section is *about* how per-user authentication works across the market, so say that and let the conclusion land inside it.
- **Open with a lede, not a verdict** (research genre). The first section states what is true — the most important fact the research established. It does not tell the reader what to do, and it never precedes the content it summarises with a judgement of someone's proposal.
- **Glossary / Key Concepts** (3–8 terms): after Key Facts, **before** any summary or content section. Glossary is *read-support* — a reader needs definitions before encountering terms in content.
- **Insights section** (3–6 items, both genres, optional but encouraged). Research always turns up things that are interesting without being load-bearing — a striking parallel, a number that reframes the scale of something, an adjacent field that solved the same problem differently, a primary source that is a pleasure to read. The usual fate of those is deletion, because they do not serve the brief. Collect them instead. **The test is inversion: if removing it would change a finding or a recommendation, it is not an insight — it is a buried finding, and it belongs in the body.** Give each a stable ID (`I1`, `I2` …) and **tease it once or twice from the body** where it naturally fits, as a one-line inline pointer that links down (`([→ I3 — what the ventilation actually cost][in-I3])`). Teasers sit at the end of a paragraph, never mid-argument; a paragraph carrying three of them has stopped being prose. An insight with no teaser is fine — an insight nobody can find from the body is wasted. **Insights carry the same evidence standard as findings.** The register is looser, the sourcing is not: an insight states what the sources support and stops there. Check the last sentence hardest — that is where a paragraph of sound facts turns into a verdict the reader was not shown the basis for.
- **Hyperlink every entity** on first mention.
- **Cite factual claims** with clickable reference-link syntax: `claim [S1][ref-S1]` where each citation token (`S1`, `G6`, `R1`, `O3` — pick a consistent category-prefix scheme) has a matching `[ref-S1]: https://...` definition at the end of §Sources. The raw markdown preserves the `[S1]` bracket token for anyone reading the file directly; the rendered link reads as `S1` and clicks through to the URL. Inline `([text](url))` also works for one-off sources. Bar: "could someone verify this?". If your target renderer supports them, the footnote form `[^S1]` is lighter — see `${CLAUDE_SKILL_DIR}/references/review-checklist.md` (citation-integrity) for the portability trade-off.
- **Source categories** adapt to domain (see template).
- **Template-order rule.** Glossary stays at the top; Sources stay at the end. The asymmetry is deliberate — glossary is read-support (before), sources are trust-support (after). Do not move glossary to the appendix by analogy with sources.
- **Anti-revision rule.** An in-progress / unpublished dossier reads as a single current version. No "Revision note" block, no `rev. <date>` suffix on the date line, no "first draft framed X / corrected after feedback" phrasing in the body. When you receive corrections mid-session, **rewrite** the affected lines as plain present-tense facts — don't append a changelog. Keep a point if it is load-bearing for the conclusion, but state *why it matters* (`X was considered because Y`), not *that it was added later* (`edited to also consider X because Y was raised`). Document history belongs in commit messages and the sessionlog. (Deliberate dated addenda on already-published dossiers are a different case and out of scope here.) Reviewed via `${CLAUDE_SKILL_DIR}/references/review-checklist.md` (single-current-version item).

**Ballot** (when decisions happen async — reviewed over chat, on a PR, after the session ends): use the `ballot` skill. Works for multi-reviewer panels and single async deciders alike. Template at `skills/ballot/templates/ballot-per-reviewer.md`; conventions at `skills/ballot/SKILL.md`.

### 5. REVIEW

**Dispatch three fresh-context subagents over the finished dossier.** Full prompts, inputs, and the artifact format are at `${CLAUDE_SKILL_DIR}/references/review-lenses.md`.

| Lens | Receives | Judges |
|---|---|---|
| **Shape** | the brief + the dossier | genre match, skimmability, section order, Key Facts accuracy |
| **Support** | the dossier + `sources/` | claims traced to sources; uncited assertions; absence claims; dated claims |
| **Insights** | the dossier, nothing else | inversion, reachability, stance |

**The reviewers must not receive the research conversation** — not the transcript, not a summary of your reasoning. That isolation is the entire mechanism, not an implementation detail. A defect survives its author because the author half-remembers the sources and the claim *feels* safe; a reviewer holding that reasoning inherits the feeling, while a reviewer holding only the document asks what the reader asks — *was I shown the basis for this?* Dispatching a subagent gives you fresh context by construction; do not undo it by pasting your notes into the prompt.

The **Insights** lens is starved on purpose. Give it `sources/` and it can verify a claim the document never cited, then pass something the reader cannot verify. Its blindness is why it catches stance.

Record every finding in `review-YYYY-MM-DD.md` beside the dossier, each with `**Disposition:** fixed — …` or `**Disposition:** waived — …`. Waiving is legitimate: a fresh-context reviewer sometimes flags a correctly-cited claim it could not verify, and forcing a fix there makes the dossier worse. The gate requires a *decision*, not agreement.

Run all three for anything a human will read. For a short internal dossier (under ~200 lines, no `sources/`), one combined reviewer running all three lenses is enough. **Review is never skipped** — "this one is internal" is precisely the reasoning that skips review on the dossier that then gets forwarded.

The older `${CLAUDE_SKILL_DIR}/references/review-checklist.md` remains the definition of *what* good looks like, and the lens prompts are drawn from it. Consult it when a reviewer's finding needs adjudicating.

### 6. DELIVER

The mechanical gates (`ballot-filename`, `sources-index-consistency`) fire automatically on Write/Edit via the PostToolUse hook, and `review-artifact-present` fires PreToolUse on `git commit` — a commit that includes a main dossier is denied unless its folder holds a review artifact with every finding dispositioned. Once REVIEW is recorded:

- Commit dossier folder (`D:` intention per commit-notation).
- **Do NOT end the session** — stay available for follow-ups, iterations, or additional dossiers.

If the reader wants the dossier on an e-reader rather than on screen, see the `send-to-kindle` skill (and `pandoc`'s `md2kindle-epub.sh` for the file itself).

## Output Convention

```
research/YYYY-MM-DD-slug/
├── DOSSIER-Title-Words-YYYY-MM-DD.md           # Main report
├── DOSSIER-Title-Words-BALLOT-Max.md           # Optional: one per decider
├── DOSSIER-Title-Words-BALLOT-Patrick.md       # Optional: one per decider (multi-reviewer case)
├── DOSSIER-Followup-Title-YYYY-MM-DD.md        # Follow-up dossiers in same folder
├── review-YYYY-MM-DD.md                        # REVIEW findings + dispositions (gates the commit)
├── sources/                                    # Archived copies of cited sources
│   ├── index.md                                #   citation ID ↔ URL ↔ access date ↔ file
│   ├── S1-example.com-docs.html                #   captured page
│   └── S1-example.com-docs.md                  #   text extraction (when pandoc present)
└── (attachments — rare)
```

Location: workspace `research/` for standalone; `projects/{name}/research/` for project-specific.

Multiple dossiers per folder is expected.

## Gates (hooks)

Two mechanical gates run PostToolUse on `Write|Edit` through `.claude-plugin/hooks/dossier-hook-dispatcher.sh`. Exit 2 pipes stderr back to Claude. **Alerting-level** — the file is already on disk when it fires; a motivated agent can ignore.

One gate runs **PreToolUse on `Bash`** through `.claude-plugin/hooks/dossier-commit-gate.sh` and genuinely blocks.

| Gate | Timing | Fails on |
|------|--------|----------|
| `ballot-filename.sh` | PostToolUse | Ballot file not matching `DOSSIER-<slug>-BALLOT-<Reviewer>.md` (owned by the `ballot` skill) |
| `sources-index-consistency.sh` | PostToolUse | `sources/index.md` referencing a missing file, or a captured file with no index row. Silent when there is no `sources/` archive |
| `review-artifact-present.sh` | **PreToolUse on `git commit`** | A staged main dossier whose folder has no `review-*.md`, or whose review has a finding without a disposition. During a merge, only files the merge itself contributes (differing from every parent) are checked — integrating a dossier that another branch already committed is not delivery |

**Why the review gate is PreToolUse on commit and not PostToolUse on Write.** The point of the stage is that "I reviewed it" must stop being answerable without the work, so alerting-level is not enough — PreToolUse exit 2 denies the call and the gate actually holds. Write is also the wrong *moment*: a dossier is edited dozens of times during SYNTHESIZE, and demanding a review artifact on each one would fire constantly during normal authoring, which trains the reader to ignore it. `git commit` is the delivery act in this skill, which makes it the one moment where the check is both meaningful and rare.

**Why there is no "review must be newer than the dossier" check.** The obvious freshness test is wrong, and only writing the script exposed it: the correct workflow is review → findings → fix the dossier, which necessarily leaves the dossier newer than the review that prompted the fixes. An mtime gate would fire on every properly-executed review and pass only when the author changed nothing — exactly inverting the behaviour it is meant to enforce. Staleness is a warning (dossier edited >14 days after its review), never a block. The gate proves review *happened* and was *dispositioned*; it cannot prove the review is semantically current, and no file-level check can.

All three check **file-level facts** — a filename shape, whether a directory matches its own index, whether a review artifact exists and is dispositioned — never document prose. That is the property the removed six lacked, and it is what makes the review gate legitimate rather than a revival of them: it never reads the dossier's sentences, only whether a review of them was recorded. Judgement stays with the reviewers.

Everything else is reviewed by the lenses and the checklist, not by grep. Earlier iterations shipped grep-gates for citation integrity, forbidden words, section ordering, dated claims, and ballot cover-block archaeology — a 2026-04-18 polish pass removed them after they proved overfit to the a11y-extension session. `dossier-framing-declared.sh` was removed in the 2026-04-18 preflight-gate pass: the framing-mode convention it enforced doesn't generalize across dossier styles.

**The genre check added in 2026-08 is not a revival of that gate.** The axis is different: those modes (`oss`/`commercial`/`hiring`/`vendor`/`personal`) classified the *character of the sources*, while genre classifies *what document the reader wants*. Genre was never covered by that convention, so it was not lost when it died. The mechanism differs too, and that is why this one should survive. `dossier-framing-declared.sh` linted for a *declared label* that changed nothing downstream — a word you had to remember to write, enforced by grep, with identical output whether you wrote it or not. That is a rule wearing a gate's clothing, and it correctly died. The genre instead **selects the template and switches the EVALUATE and SYNTHESIZE stages**, so it cannot be declared-and-ignored: choosing wrong produces a visibly wrong-shaped document rather than a lint failure. There is no script for it, and there should not be — the check is "does this document's shape match what the reader asked for", which is a judgement, not a pattern match. See `${CLAUDE_SKILL_DIR}/references/review-checklist.md`.

Both surviving gates check **file-level facts** — a filename shape, and whether a directory matches its own index — rather than grepping document prose. That is the property the removed six lacked: what a dossier *says* varies by topic and author, but whether an archive describes itself is the same question every time. `sources-index-consistency.sh` is deliberately a *consistency* check and not a *coverage* one: it never demands that every citation be archived, because on a machine where nothing could be captured that would block the dossier outright.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Orphan citations | Reviewed in the checklist (citation-integrity item) — every inline reference should match a §Sources entry |
| Glossary at the back of the dossier | Glossary first (read-support); Sources last (trust-support) |
| Dates treated as static | Reviewed in the checklist (dated-claim-freshness item) — re-verify each |
| Citations left as bare URLs that will 404 later | Archive each source during GATHER; reviewed in the checklist (source-archival item) |
| Submitting sources to a public archive by default | `--wayback-save` publishes the user's reading list — opt-in only (see `${CLAUDE_SKILL_DIR}/references/source-archival.md`) |
| Exhaustive list, not selective | Set selectivity in SCOPE ("5-8, not all"); reviewed in the checklist |
| Generic recommendations | Tailor to THIS user's context and infrastructure |
| Adjudicating when the reader wanted to learn | Settle the genre in Preflight 4. "Evaluate this pitch" is ambiguous — ask. Default to research when you cannot |
| Research findings phrased as verdicts | Headings name subjects; findings state facts about the world. Put any assessment in one labelled final section |
| Assessment leading the document | It goes at the end. A verdict placed before the content asks the reader to accept a conclusion about a world they have not been shown |
| Compiled report that doesn't link its own research files | The compiled document must point at the underlying analysis files, or the reader only ever sees the summary layer |
| Discarding the interesting-but-not-load-bearing | Collect it in §Insights. The adjacent find is often the most memorable thing in the dossier, and the brief is the reason it gets deleted |
| A load-bearing fact filed under §Insights | If removing it changes a finding or a recommendation, it is a buried finding. Promote it into the body |
| §Insights that nobody reaches | Tease each one from the body where it fits, as a one-line pointer. A section only reachable by scrolling past the conclusion is a section nobody reads |
| An insight that ends by telling the reader what to conclude | The looser register invites it, and a research dossier has no assessment section to hold a stance legitimately, so the insight becomes the hiding place. Watch the last sentence especially. Absence claims ("the debate has ignored this") need you to have looked — if you did not, move it to §What could not be determined and say so |
| Teasers breaking the argument | One line, at the end of a paragraph. Never mid-thread, never three in one paragraph |
| Bare product names without URLs | Hyperlink every entity on first mention |
| Same source categories every time | Adapt to domain (see `references/sources-by-domain.md`) |
| Narrating edit history in the body | Collapse to one current version; recast research-driven points as facts, not as a changelog. Reviewed in the checklist (single-current-version item) |
| Ending or re-starting session after delivery | Stay open — auto-compact handles context |

For ballot-specific mistakes (anti-options, pre-ticked checkboxes, cover-block archaeology, single-file two-column ballots, reconciliation placement), see `skills/ballot/SKILL.md` §Common Mistakes.

## Related Skills

| Skill | Integration |
|-------|-------------|
| `ballot` | Extracted decision-ballot format. SYNTHESIZE hands off when a decision surface is needed. |
| `last30days` | Social signal for consumer/OSS topics |
| `commit-notation` | `D:` prefix for dossier commits |
| `bye` | Sessionlog at session end (NOT after each dossier) |
| `challenge-the-plan` | Optional: interview-style requirements refinement |
