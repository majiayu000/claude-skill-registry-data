---
name: devils-advocate
version: 1.0.0
description: Get an outside-Anthropic second opinion on any piece of work by sending it to Google Gemini with an adversarial critique prompt. Use when the user wants to pressure-test a decision, plan, assumption, blog draft, landing page, positioning statement, campaign, or chunk of code with a non-Claude model. Trigger when the user says 'devil's advocate,' 'play devil's advocate,' 'poke holes,' 'stress test this,' 'second opinion,' 'outside perspective,' 'non-Anthropic read,' 'sanity check from another model,' 'challenge this,' 'critique this from outside,' or '/devils-advocate.' This is explicitly a cross-model sanity check — do NOT substitute your own critique; the whole point is to surface blind spots Claude might share.
---

# Devil's Advocate

Get a critique from an outside model (Google Gemini 3.1 Pro by default) to pressure-test work before it ships. The whole reason this skill exists is that Claude and the user may share the same blind spots after working on a piece of content together. Sending the work to a model in a different lineage surfaces weaknesses that neither of you will catch alone.

**Never substitute your own critique for this tool.** If you find yourself about to write "here's what I think the weak points are" without running the script, stop — you are defeating the entire purpose of the skill.

---

## When to use this skill

Use it when the user explicitly asks for a second opinion, a devil's advocate read, or to poke holes in something. Also proactively suggest it when:

- The user is about to ship high-stakes work (a public launch plan, executive-level messaging, a pricing decision, a bet-the-quarter initiative).
- You and the user have been iterating for a while and the work feels "done" — fresh eyes matter most when confirmation bias is strongest.
- The user is weighing a decision with several defensible answers (a strategy shift, a channel bet, an org change).
- A plan makes a claim that would be expensive to get wrong (projected revenue, headcount, conversion lift).

Do NOT reach for this skill for quick copy edits, tactical wordsmithing, or requests the user clearly wants done inside Claude. This is a heavier tool meant for moments where an outside critique has real value.

---

## Prerequisites

- `GOOGLE_AI_STUDIO_API_KEY` must be available as an environment variable or in a `.env` file at your project root.
- The script uses only the Python standard library. No installs required.

If the key is missing, the script will exit with a clear error and a link to create one.

---

## How to run it

The script lives at `.claude/skills/devils-advocate/scripts/challenge.py` (relative to your project root, once the skill is installed in `.claude/skills/`).

### 1. Critique files

Most common case. Pass one or more files you want challenged:

```bash
python3 .claude/skills/devils-advocate/scripts/challenge.py \
  --files docs/plan.md
```

Multiple files are fine — the critic reads them together and judges them as one body of work:

```bash
python3 .claude/skills/devils-advocate/scripts/challenge.py \
  --files landing/hero.html landing/proof.html
```

### 2. Critique an inline statement, decision, or assumption

```bash
python3 .claude/skills/devils-advocate/scripts/challenge.py \
  --statement "We should move our posting cadence from 3x/week to daily because engagement rose 18% in Q1."
```

### 3. Critique content piped in

```bash
cat draft.md | python3 .claude/skills/devils-advocate/scripts/challenge.py --stdin
```

### 4. Give the critic supporting context

This is where the skill gets sharp. The critic produces much better work when it knows the positioning, the audience, and the brief. Pass the relevant context files so the critique is judged against your actual strategy and audience:

```bash
python3 .claude/skills/devils-advocate/scripts/challenge.py \
  --files docs/newsletter-plan.md \
  --context-files context/positioning.md context/audience.md \
  --note "Audience: technical practitioners at mid-to-large companies. Goal: newsletter signups as top-of-funnel. Cadence: monthly."
```

Rules of thumb for `--context-files`:

- Add a positioning/messaging file for any marketing or comms content — it keeps the critic inside your actual audience and message pillars.
- Add a source-of-truth / product-facts file when the work makes product claims, so the critic can flag invented facts.
- Add a voice/tone or audience-language file when voice is part of the critique.
- For plans, also add the matching strategy file if the target work should tie into it.
- Don't dump every context file you have. Pick the ones that actually apply.

### 5. Save the critique to a file

```bash
python3 .claude/skills/devils-advocate/scripts/challenge.py \
  --files docs/newsletter-plan.md \
  --context-files context/positioning.md \
  --out reviews/newsletter-plan-devils-advocate.md
```

Default location for saved critiques: `reviews/<target-name>-devils-advocate.md`.

### 6. Override the model

Default is `gemini-3.1-pro-preview`. Other text-capable models on the same key include `gemini-3-pro-preview`, `gemini-2.5-pro`, `gemini-pro-latest`. Use a different model only if the user asks, or if the default times out / fails.

```bash
python3 .claude/skills/devils-advocate/scripts/challenge.py \
  --files plan.md --model gemini-2.5-pro
```

---

## Picking the target type

The script auto-detects a `target-type` hint from the file extensions and paths, but you can set it explicitly with `--target-type`:

| Value | When to use |
|---|---|
| `content` | Blog posts, landing pages, emails, social posts, case studies, datasheets |
| `code` | Email HTML templates, HTML/CSS/JS, scripts |
| `plan` | Strategy docs, campaign plans, roadmaps, launch plans |
| `assumption` | A belief the team is acting on ("channel X is our best channel") |
| `decision` | A choice the team is about to make ("We should kill the free tier") |
| `statement` | A one-line claim, hypothesis, or framing |

Set this explicitly when the default guess would be wrong. For example, if you pass an `.html` file that you want judged as rendered content (not code), pass `--target-type content`.

---

## What the output looks like

The critic always returns Markdown with these sections, in order:

1. **Steelman** — the strongest honest case FOR the work.
2. **What the work is actually claiming** — a literal restatement, to prevent strawmanning.
3. **Specific weaknesses** — numbered list with Location, Problem, Why it matters, Fix or test.
4. **Counter-evidence and missing evidence** — what would weaken the argument, what should be cited.
5. **Alternative framings** — one or two different angles, with tradeoffs.
6. **Risks and failure modes** — realistic ways it backfires, ranked.
7. **Bottom line** — one of SHIP, SHIP WITH FIXES, REWORK, KILL, plus one sentence of reasoning.

The top of the file is a comment tag identifying which model produced the critique and what target type was assumed, so reviews stay traceable.

---

## After you get a critique

Do not silently accept every point the critic makes. It is an outside voice, not an oracle. Your job after running it is:

1. **Read the critique end to end.** Don't skim.
2. **Flag which specific items you agree with, disagree with, and want the user to decide.** Being concrete is the whole value — "the Q1 engagement lift isn't enough evidence for a 3x cadence change" is useful; "it raises good points" is useless.
3. **Ask the user which ones they want to act on** before editing. Some critiques come from a model that doesn't know the project as deeply as you do; others expose real problems you missed.
4. **When the user says go, make the specific changes.** Don't rewrite from scratch unless the critique says REWORK and the user agrees.

If the critic returns SHIP, that's a useful signal — but still read the weaknesses section. Good critiques say SHIP with caveats; bad critiques either rubber-stamp or gratuitously complain. Treat suspicious uniformity (all SHIP, all KILL) as a signal to re-run with different context.

---

## Example invocations

**A blog draft:**
```bash
python3 .claude/skills/devils-advocate/scripts/challenge.py \
  --files blog/2026-04-monitoring-is-dead.md \
  --context-files context/positioning.md context/audience.md \
  --note "Author: executive voice. Goal: drive inbound demo requests from technical buyers."
```

**A positioning statement (inline):**
```bash
python3 .claude/skills/devils-advocate/scripts/challenge.py \
  --statement "We are the only platform that detects the problem in real time without instrumenting the target system." \
  --context-files context/positioning.md context/truth.md \
  --target-type statement
```

**An email HTML template:**
```bash
python3 .claude/skills/devils-advocate/scripts/challenge.py \
  --files templates/newsletter-email.html \
  --target-type code \
  --note "Must render in Outlook 2019, dark mode iOS Mail, and Gmail web."
```

**A campaign plan with full context:**
```bash
python3 .claude/skills/devils-advocate/scripts/challenge.py \
  --files docs/pipeline-growth-strategy.md \
  --context-files context/positioning.md context/customer-journey.md \
  --out reviews/pipeline-growth-strategy-devils-advocate.md
```

---

## Failure modes to watch for

- **API timeout or 5xx.** Retry once. If it keeps failing, try `--model gemini-2.5-pro` as a fallback.
- **Critique that reads like a rewrite request.** The critic sometimes slips into copy-editing mode. Re-run with `--note "do NOT rewrite prose; challenge logic, evidence, and risk only."`
- **Critique that doesn't know the project.** Add your positioning and source-of-truth files to `--context-files` and re-run.
- **Critique that contradicts something in your source-of-truth files.** Trust your own verified facts; flag the disagreement to the user rather than editing to match the critic.

## Learnings

<!-- Updated by /reflect. Promote stable patterns to the main skill body. -->
