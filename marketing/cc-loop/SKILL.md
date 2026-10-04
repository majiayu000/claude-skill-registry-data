---
name: cc-loop
description: >
  Iterative quality loop for any content deliverable. Runs fixer → polish → N parallel critiques → score → loop until pass criteria are met. Default pass criteria: avg score ≥ 80 AND min score ≥ 70 across all critics. Max 3 rounds (configurable). Critic set is domain-configurable: design+content+marketing+pedagogy for decks/presentations; content+marketing+SEO for blog posts; content+marketing for emails; custom list accepted. Each round writes an audit log entry so you can track how the deliverable evolved. Trigger when: user says "run X through the loop", "polish and critique", "iterate to quality bar", "/cc-loop", or any time a deliverable needs systematic multi-axis review with pass criteria. Also trigger when a single critique came back with issues and the user wants a structured fix-and-verify cycle rather than ad-hoc edits. Key capabilities: snapshot-grounded design critique via Playwright at 1920×1080, format-aware humanizer + proofreader polish pass, configurable scoring threshold and max rounds, reframe override for mid-loop goal changes, and full round-by-round audit log at {deliverable-dir}/cc-loop-log.md.
---

# cc-loop — Content Critique Loop

Systematic quality loop for any content deliverable. One command runs fixer →
polish → critics (in parallel) → score → loop until the deliverable passes
or rounds are exhausted.

Agent types used (from Agency catalog):
- **Fixer**: Content Director (`agents/content-creation/content-director.md`)
- **Polish**: Content Editor (`agents/content-creation/content-editor.md`)
- **Design critic**: `agents/critiques/critique-design.md` (Playwright at 1920×1080, screenshot-grounded)
- **Content critic**: `agents/critiques/critique-content.md` (copy/voice/AI-slop)
- **Marketing critic**: `agents/critiques/critique-marketing.md` (positioning/funnel/ICP/CTA)
- **Pedagogy critic**: `agents/critiques/critique-pedagogy.md` (teaching effectiveness/scaffolding/demo ratio)
- **SEO critic**: `agents/critiques/critique-seo.md` (SEO/GEO/AEO)
- **Brand critic**: `agents/critiques/critique-brand.md` (voice/visual identity/positioning drift)
- **Product critic**: `agents/critiques/critique-product.md` (UX/IA/usability/accessibility)
- **Security critic**: `agents/critiques/critique-security.md` (OWASP Top 10)
- **Code critic**: `agents/critiques/critique-code.md` (readability/dead code/complexity/error handling)
- **Data critic**: `agents/critiques/critique-data.md` (chart misrepresentations/misleading axes/dashboard UX, screenshot-grounded)
- **Video critic**: `agents/critiques/critique-video.md` (pacing/captions/visual consistency/audio sync, frame-grounded)
- **Imageprompt critic**: `agents/critiques/critique-imageprompt.md` (AI image-generation prompt quality)
- **SAG critic**: `agents/critiques/sag-critique.md` (technical SEO/AEO/GEO implementation audits)
- **Critique lead**: `agents/critiques/critiques-lead.md` (routes + aggregates all critics)

---

## Invocation

```
/cc-loop [deliverable] [domain] [options]
```

| Argument | Required | Default | Description |
|---|---|---|---|
| `deliverable` | yes | — | Path to the file or URL to review |
| `domain` | no | `deck` | `deck` \| `blog` \| `email` \| `brief` \| `script` \| `custom` |
| `--critics` | no | domain default | Comma-separated: `design,content,marketing,pedagogy,seo` |
| `--avg` | no | `80` | Min average score across all critics to pass |
| `--min` | no | `70` | Min individual score for any critic to pass |
| `--rounds` | no | `3` | Max iterations before loop exits with final state |
| `--no-polish` | no | off | Skip the humanizer+proofreader pass (Step 2) |
| `--no-snapshots` | no | off | Skip Playwright screenshots (design critic still runs) |
| `--reframe` | no | — | Override string: drop obsolete findings for a changed goal |
| `--critiques-dir` | no | — | Path to pre-existing critique reports (skip initial generation) |

### Domain defaults (critic sets)

| Domain | Critics |
|---|---|
| `deck` | design, content, marketing, pedagogy, brand |
| `blog` | content, marketing, seo, brand |
| `email` | content, marketing, brand |
| `brief` | content, marketing |
| `script` | content, pedagogy |
| `landing-page` | design, content, marketing, seo, brand, product |
| `app` | design, product, security |
| `code` | security, product |
| `generic` | content, brand |
| `custom` | must supply `--critics` |

---

## Scoring Rubric (embedded in every critic prompt)

Every critic MUST emit the following as the first line of output:

```
SCORE: <0-100> | VERDICT: <BLOCKER|NEEDS WORK|CONDITIONAL PASS|PASS>
```

Rubric (calibration, inform but do not dictate):

| Range | Verdict | Meaning |
|---|---|---|
| 90-100 | PASS | Publish-ready — no blockers |
| 80-89 | PASS | Minor polish only — ship with small fixes |
| 70-79 | CONDITIONAL PASS | Specific fixes needed before shipping |
| 50-69 | NEEDS WORK | Significant rework required |
| 0-49 | BLOCKER | Do not publish — major structural issues |

---

## Step 0: Threshold Prompt (MANDATORY — runs before anything else)

**Before any other action**, prompt the user for score thresholds.

Ask:

```
cc-loop threshold setup.

Default pass criteria:
  avg ≥ 80 (average across all critics)
  min ≥ 70 (lowest individual critic score)

Accept defaults? Or enter overrides (e.g. "avg 85 min 75"):
```

Options:
- User presses Enter or types "yes" / "default" → use `avg=80`, `min=70`
- User types a number or override → parse and apply

Record the chosen thresholds as `threshold_avg` and `threshold_min`. These values:
- Drive Step 4 (score check) in place of `--avg` / `--min` flags
- Are persisted in every audit log entry so the exact bar is auditable

CLI flags `--avg` and `--min` still work as pre-set defaults if provided — they are the
suggested values shown in the prompt. The interactive prompt always fires regardless.

---

## Step 0b: Ingest Existing Critique Reports (Optional)

If `--critiques-dir` is provided AND the directory contains at least one report file matching the pattern `*critique*.md` or `*report*.md`:

1. Read each report file in the directory
2. Map reports to critic types by filename or content heading
3. Mark these as "Round 0 critiques" — they are the input for Step 1
4. Skip to Step 1 immediately (no initial critique generation needed)

If `--critiques-dir` is not provided, proceed to Step 1 with no prior critiques.

---

## Step 1: Fixer Pass

**Agent type:** Content Director

Spawn a Content Director agent with the following instructions:

```
You are running the FIXER PASS of a cc-loop quality cycle.

Deliverable: {deliverable}
Round: {current_round}
Reframe override: {--reframe value, or "none"}

Your job:
1. Read all critique reports provided (Round 0 or prior round).
2. For each report, extract every IMPROVEMENT block from the findings.
3. Execute every IMPROVEMENT block VERBATIM. Do not skip, paraphrase, or substitute.
   - If an IMPROVEMENT is unimplementable as written, escalate back to the critic — do not silently swap it.
   - For design findings: execute the code-fix prescription exactly (file / selector / current / required / reason).
   - For other critics: execute the IMPROVEMENT field exactly as written.
4. If a finding is ambiguous (no IMPROVEMENT block and score < 100), make the better editorial call and note it.
5. If a reframe override is set, DROP all findings that conflict with the new goal
   before applying fixes.
5. After all fixes are applied, report:

FIXER REPORT — Round {n}
Design fixes: {count}
Content fixes: {count}
Marketing fixes: {count}
Pedagogy fixes: {count}
SEO fixes: {count}
Notable decisions: {list any judgment calls made}
Reframe dropped: {list any findings dropped due to --reframe, or "none"}

Deliverable updated at: {path}
```

Wait for Fixer to complete before proceeding.

---

## Step 2: Polish Pass

Skip this step entirely if `--no-polish` flag is set.

**Agent type:** Content Editor

Spawn a Content Editor agent with the following instructions:

```
You are running the POLISH PASS of a cc-loop quality cycle.

Deliverable: {deliverable}
Round: {current_round}

Run two sub-passes in sequence on the deliverable:

SUB-PASS A — Humanizer
Check for and fix:
- AI-slop patterns (hedging, filler phrases, "it's worth noting", "in conclusion")
- Generic opener/closer phrases
- Rhythm issues (monotone sentence length, all-parallel structure)
- Repetition within 3 paragraphs
- Register inconsistency (formal/casual mixing without intent)

SUB-PASS B — Proofreader
Check for and fix:
- Spelling and typos (including diacritics for Vietnamese/French content if present)
- Punctuation (consistent em/en dash usage, Oxford comma policy)
- Number format (thousands separator, decimal style)
- Capitalization (title case consistency, proper nouns)
- Inline HTML integrity (if deliverable is HTML: no broken tags, no unclosed elements)

After both sub-passes, report 2-3 before/after examples showing the most impactful fixes.

POLISH REPORT — Round {n}
Humanizer fixes: {count}
Proofreader fixes: {count}
Before/after examples:
  1. BEFORE: {text} → AFTER: {text}
  2. BEFORE: {text} → AFTER: {text}

Deliverable updated at: {path}
```

Wait for Polish to complete before proceeding.

---

## Step 3: Critics (Parallel)

Spawn all critics in a SINGLE message (parallel). Each critic receives:
- The current deliverable
- The scoring rubric (see above)
- Critic-specific instructions below

**MANDATORY first line:** Every critic output MUST begin with:
```
SCORE: <0-100> | VERDICT: <BLOCKER|NEEDS WORK|CONDITIONAL PASS|PASS>
```

**MANDATORY for every critic:** The FIRST action in every critic session is to read its own memory
file at `{agency-root}/agents/critiques/memory/{critic-slug}.md`. Prior lessons must inform the
current critique.

**MANDATORY finding format for all critics except design:** Every finding (where score < 100)
MUST include an IMPROVEMENT block:

```
ISSUE: <what's wrong>
EVIDENCE: <screenshot file | line reference | quote — concrete proof>
IMPROVEMENT: <exact fix to apply — specific enough that the fixer executes without re-interpretation>
```

The design critic uses its existing HARD RULE 2 format (ISSUE / SCREENSHOT / FIX with
file/selector/current/required/reason) — that already satisfies Rule 4.2.

### Design Critic

Agent: `agents/critiques/critique-design.md`

Spawn with:
```
You are the DESIGN CRITIC in a cc-loop quality cycle. Run as critique-design.
Read your full definition at {agency-root}/agents/critiques/critique-design.md.

FIRST ACTION: Read {agency-root}/agents/critiques/memory/critique-design.md — prior lessons must
inform this critique.

Deliverable: {deliverable}
Round: {current_round}
Reframe override: {--reframe value, or "none"}

MANDATORY: Follow Hard Rule 1 (Playwright at 1920×1080, screenshots required for every finding)
and Hard Rule 2 (code-fix actionability — file, selector, current, required, reason).
Save screenshots to {deliverable-dir}/cc-loop-screenshots/round-{n}/

If --no-snapshots is set: return SCORE: 0 | VERDICT: BLOCKER — snapshots disabled but design critique requires visual evidence.
```

### Content Critic

Agent: `agents/critiques/critique-content.md`

Spawn with:
```
You are the CONTENT CRITIC in a cc-loop quality cycle. Run as critique-content.
Read your full definition at {agency-root}/agents/critiques/critique-content.md.

FIRST ACTION: Read {agency-root}/agents/critiques/memory/critique-content.md — prior lessons must
inform this critique.

Deliverable: {deliverable}
Round: {current_round}
Reframe override: {--reframe value, or "none"}

Every finding (where score < 100) MUST include:
  ISSUE: <what's wrong>
  EVIDENCE: <quote or line reference>
  IMPROVEMENT: <exact fix — specific enough to execute verbatim>

If reframe override is set: drop findings that assumed the prior goal.
```

### Marketing Critic

Agent: `agents/critiques/critique-marketing.md`

Spawn with:
```
You are the MARKETING CRITIC in a cc-loop quality cycle. Run as critique-marketing.
Read your full definition at {agency-root}/agents/critiques/critique-marketing.md.

FIRST ACTION: Read {agency-root}/agents/critiques/memory/critique-marketing.md — prior lessons must
inform this critique.

Deliverable: {deliverable}
Round: {current_round}
Reframe override: {--reframe value, or "none"}

Every finding (where score < 100) MUST include:
  ISSUE: <what's wrong>
  EVIDENCE: <quote or location reference>
  IMPROVEMENT: <exact fix — specific enough to execute verbatim>

If reframe override is set: drop findings that assumed the prior goal.
```

### Pedagogy Critic

Agent: `agents/critiques/critique-pedagogy.md`

Spawn with:
```
You are the PEDAGOGY CRITIC in a cc-loop quality cycle. Run as critique-pedagogy.
Read your full definition at {agency-root}/agents/critiques/critique-pedagogy.md.

FIRST ACTION: Read {agency-root}/agents/critiques/memory/critique-pedagogy.md — prior lessons must
inform this critique.

Deliverable: {deliverable}
Round: {current_round}
Reframe override: {--reframe value, or "none"}

Every finding (where score < 100) MUST include:
  ISSUE: <what's wrong>
  EVIDENCE: <slide/section reference>
  IMPROVEMENT: <exact fix — specific enough to execute verbatim>

If reframe override is set: drop findings that assumed the prior goal.
```

### SEO Critic (blog/page/landing-page domains)

Agent: `agents/critiques/critique-seo.md`

Spawn with:
```
You are the SEO CRITIC in a cc-loop quality cycle. Run as critique-seo.
Read your full definition at {agency-root}/agents/critiques/critique-seo.md.

FIRST ACTION: Read {agency-root}/agents/critiques/memory/critique-seo.md — prior lessons must
inform this critique.

Deliverable: {deliverable}
Round: {current_round}
Reframe override: {--reframe value, or "none"}

Every finding (where score < 100) MUST include:
  ISSUE: <what's wrong>
  EVIDENCE: <title/heading/section reference with measurement if applicable>
  IMPROVEMENT: <exact fix — specific enough to execute verbatim>

If reframe override is set: drop findings that assumed the prior goal.
```

### Brand Critic (deck/blog/email/landing-page domains)

Agent: `agents/critiques/critique-brand.md`

Spawn with:
```
You are the BRAND CRITIC in a cc-loop quality cycle. Run as critique-brand.
Read your full definition at {agency-root}/agents/critiques/critique-brand.md.

FIRST ACTION: Read {agency-root}/agents/critiques/memory/critique-brand.md — prior lessons must
inform this critique.

Deliverable: {deliverable}
Round: {current_round}
Reframe override: {--reframe value, or "none"}

Load brand guidelines from {project}/memory/brand-guidelines.md if available.

Every finding (where score < 100) MUST include:
  ISSUE: <what's wrong>
  EVIDENCE: <section/element with exact quote or value>
  IMPROVEMENT: <exact fix — specific enough to execute verbatim>

If reframe override is set: drop findings that assumed the prior goal.
```

### Product Critic (landing-page/app domains)

Agent: `agents/critiques/critique-product.md`

Spawn with:
```
You are the PRODUCT CRITIC in a cc-loop quality cycle. Run as critique-product.
Read your full definition at {agency-root}/agents/critiques/critique-product.md.

FIRST ACTION: Read {agency-root}/agents/critiques/memory/critique-product.md — prior lessons must
inform this critique.

Deliverable: {deliverable}
Round: {current_round}
Reframe override: {--reframe value, or "none"}

Every finding (where score < 100) MUST include:
  ISSUE: <what's wrong>
  EVIDENCE: <screen/component/flow reference>
  IMPROVEMENT: <exact fix — specific enough to execute verbatim>

If reframe override is set: drop findings that assumed the prior goal.
```

### Security Critic (app/code domains)

Agent: `agents/critiques/critique-security.md`

Spawn with:
```
You are the SECURITY CRITIC in a cc-loop quality cycle. Run as critique-security.
Read your full definition at {agency-root}/agents/critiques/critique-security.md.

FIRST ACTION: Read {agency-root}/agents/critiques/memory/critique-security.md — prior lessons must
inform this critique.

Deliverable: {deliverable}
Round: {current_round}

Every finding (where score < 100) MUST include:
  ISSUE: <vulnerability class and specific description>
  EVIDENCE: <file:line reference or config section>
  IMPROVEMENT: <exact fix — parameterized query / config value / code change — specific enough to execute verbatim>

CRITICAL findings explicitly block publishing — flag clearly.
```

Wait for ALL critics to complete before proceeding to Step 4.

---

## Step 4: Score Check

After all critics complete:

1. Parse the first line of each critic's output for `SCORE: <N>`
2. Compute:
   - `avg_score` = mean of all critic scores
   - `min_score` = lowest individual score
3. Evaluate pass criteria using thresholds from Step 0:
   - PASS if: `avg_score >= threshold_avg` AND `min_score >= threshold_min`
   - FAIL otherwise

Display score table:

```
ROUND {n} SCORES
---
Design:    {score} — {verdict}
Content:   {score} — {verdict}
Marketing: {score} — {verdict}
Pedagogy:  {score} — {verdict}

Average:   {avg_score} (threshold: {threshold_avg})
Minimum:   {min_score} (threshold: {threshold_min})

Result: PASS / FAIL
```

---

## Step 5: Loop or Exit

**If PASS:**
1. Write final round entry to audit log (see Audit Log section)
2. Open the deliverable in the browser: `open {deliverable}`
3. Report:

```
cc-loop COMPLETE — Round {n}
{deliverable} passed quality criteria.
Average: {avg} | Min: {min}
Scores: {per-critic table}
Audit log: {deliverable-dir}/cc-loop-log.md
```

Stop.

**If FAIL and rounds remaining:**
1. Write round entry to audit log
2. Save all critic reports to `{deliverable-dir}/cc-loop-critiques/round-{n}/`
3. Increment round counter
4. Return to Step 1 with the new critic reports as input

**If FAIL and max rounds reached:**
1. Write final round entry to audit log
2. Report final state:

```
cc-loop STOPPED — Max rounds ({--rounds}) reached without passing.
Final scores: {per-critic table}
Remaining gaps:
  {list all CRITICAL and HIGH findings from the final round's critics}
Audit log: {deliverable-dir}/cc-loop-log.md
```

Then proceed to Step 6.

---

## Step 6: Post-Loop Critic Reflection (runs after every cc-loop exit, PASS or FAIL)

After the loop exits (PASS, FAIL, or max rounds), trigger each critic that participated
in the final round to write a reflection entry to its memory file.

Send each participating critic a message:

```
cc-loop run complete for {deliverable}.
Final result: {PASS|FAIL} — avg: {avg_score}, min: {min_score}

Append ONE reflection entry to {agency-root}/agents/critiques/memory/{critic-slug}.md.

Format:
## {YYYY-MM-DD} — {brief title, 5-10 words}

{3-8 lines describing one lesson from this run. Be specific:
- If round was clean (PASS): what worked that should be repeated?
- If round needed iteration: what did you miss initially? What feedback wording produced a
  clean fix vs. confused the fixer?
- Any calibration corrections, blind spots discovered, or prompts that worked/wasted rounds.}

Append only. Do not delete or rewrite prior entries.
```

Wait for all reflection appends to complete before closing the skill.

---

## Audit Log

Write a log entry after every round to `{deliverable-dir}/cc-loop-log.md`.
Create the file if it does not exist.

Entry format:

```markdown
## Round {n} — {YYYY-MM-DD HH:MM}

**Result:** PASS / FAIL (avg: {score}, min: {score})
**Thresholds:** avg ≥ {threshold_avg}, min ≥ {threshold_min}

### Fixes Applied (Fixer)
- Design: {count}
- Content: {count}
- Marketing: {count}
- Pedagogy: {count}
- Notable decisions: {list or "none"}
- Reframe dropped: {list or "none"}

### Polish Applied
- Humanizer: {count} fixes
- Proofreader: {count} fixes

### Critic Scores
| Critic | Score | Verdict |
|---|---|---|
| Design | {n} | {verdict} |
| Content | {n} | {verdict} |
| Marketing | {n} | {verdict} |
| Pedagogy | {n} | {verdict} |

### Remaining Gaps (CRITICAL / HIGH only)
{list from failing critics, or "none"}

### Screenshots
{list of screenshot files for this round, or "none / disabled"}
```

This log is append-only. Do not overwrite prior entries.

---

## Session Reference

This skill was built from a real loop run on 2026-05-22 (AI for CEO Day 4 deck):

- **Fixer pass** → Content Director agent applied fixes from 4 critique reports
- **Polish pass** → Content Editor ran humanizer + proofreader in sequence
- **Critics (parallel)** → critique-design (Playwright at 1920×1080), critique-marketing, critique-content, critique-pedagogy
- **Score check** → avg/min thresholds evaluated; loop continued until pass or max rounds

That session demonstrated the value of: (a) ingesting pre-existing critique reports rather than generating them from scratch, (b) dropping obsolete pedagogy findings after a reframe ("this is intro-level, not funnel"), and (c) parallel critics for speed with sequential fixer/polish for coherence.

---

## Key Rules

- **Critics are purpose-built specialist agents.** Use `agents/critiques/critique-*` agents — not generic role-leads. Every critic agent is permanently in a bad mood, standards-driven, and brief. They target the artifact, not the maker.
- **Domain-agnostic.** The loop works for HTML decks, Markdown blog posts, plain-text emails, scripts, briefs, landing pages, apps, code — anything text, HTML, or renderable.
- **Threshold prompt is mandatory.** Step 0 always fires — the user confirms avg/min thresholds before the loop starts. Never silently apply defaults.
- **Snapshot-grounded design critique is non-negotiable.** critique-design runs Playwright at 1920×1080. Every design finding must cite a screenshot filename. No screenshot = no finding. Unbuilt deliverables get SCORE: 0 | BLOCKER.
- **Code-fix actionability on every design finding.** critique-design returns file/selector/current value/required value/reason — the fixer agent executes without interpretation.
- **IMPROVEMENT block on every non-design finding.** Every finding with score < 100 must include ISSUE / EVIDENCE / IMPROVEMENT. The fixer executes IMPROVEMENT verbatim — no paraphrase, no substitution.
- **Fixer executes verbatim.** If an IMPROVEMENT is unimplementable as written, fixer escalates to the critic — does not silently swap it.
- **Critics read their memory first.** Every critic reads `{agency-root}/agents/critiques/memory/{critic-slug}.md` as its first action in every session.
- **Critics write reflection after every run.** Step 6 fires regardless of PASS or FAIL. Each participating critic appends one reflection entry to its memory file.
- **Reframe discipline.** If `--reframe` is set, critics drop findings that assumed the old goal. Encode the new goal explicitly.
- **Audit log is mandatory.** Every round writes a log entry including the thresholds used. This is the audit trail for how the deliverable evolved.
- **Polish is on by default.** Skip with `--no-polish` only when the deliverable has already been humanized or when speed is prioritized over quality.
- **SCORE on first line, always.** If a critic's output does not begin with `SCORE: <0-100> | VERDICT:`, treat it as a malformed response — re-spawn that critic.
