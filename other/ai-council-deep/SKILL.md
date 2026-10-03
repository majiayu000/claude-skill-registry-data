---
name: ai-council-deep
description: "Deep, interactive variant of ai-council with three user-in-the-loop checkpoints (clarify, surface assumptions, iterate). Same five advisors and anonymous peer review. Use when the answer is expensive if wrong, or when you are still genuinely unsure what you are asking. Triggers on deep council, interactive council, and high-stakes council."
when_to_use: Use when the user asks for a deep, interactive, or high-stakes council, or when the decision under review is expensive to get wrong and its framing is still unsettled, since this variant pauses three times so the user can clarify the question, correct the assumptions, and iterate on the verdict. Use ai-council instead for a fast, fire-and-forget run with no checkpoints.
---

<!-- Adapted from the interactive-ai-council variant by Freddy Gottesman (GHP Labs, April 2026), itself a fork of the AI Council skill by John Graff (UT Austin McCombs), based on Andrej Karpathy's LLM Council methodology. -->

# AI Council (Deep)

Same five advisors as `ai-council`. Same anonymous peer review. Same chairman synthesis. Three user-in-the-loop checkpoints that turn a 2-minute pressure-test into a genuine consultation.

Use this when the answer is expensive if wrong, or when you are still genuinely unsure what you are asking. For quick pressure-tests, use `ai-council` instead.

---

## When to use deep vs fast

| | Fast (`ai-council`) | Deep (`ai-council-deep`) |
|---|---|---|
| Turnaround | About 2 minutes | 10 minutes to an hour, user-paced |
| User touches | 0 (fire-and-forget) | 3 checkpoints, each skippable |
| Advisor edge | Full, uncushioned | Full, uncushioned (Checkpoint 2 surfaces assumptions, does not hedge) |
| Output | HTML report and transcript | HTML report and annotated transcript showing each checkpoint |
| Best for | "Should I split this PR?" "Is this landing page weak?" | "Should we take this term sheet?" "Which of these three pivots?" "Is this strategy memo sound enough to publish?" |

If a user invokes this skill for a trivial question, tell them so and offer to switch to `ai-council`. Do not run a 30-minute consultation on "what's the capital of France."

---

## When NOT to use this skill

A deep council costs roughly 11 sub-agent calls per round (5 advisors + 5 peer reviewers + chairman) and up to 25 across two rounds. The interactive design also assumes there is a meaningful question to deliberate on. Several input types waste that cost or actively misuse the format. If the user invokes the skill on one of these, surface the mismatch in Phase 0 before proceeding.

- **Time-sensitive decisions (hours, not days).** Use the fast `ai-council` instead.
- **First drafts.** The council evaluates something coherent enough to peer-review. Help the user write the draft first, then bring it back.
- **Late-stage editing (typos, formatting, line edits).** Advisors rebuild what does not need rebuilding. Use direct edits instead.
- **Highly technical artifacts where domain expertise dominates** (legal contracts, compliance filings, technical specs, code). General-purpose advisor archetypes produce non-expert critique.
- **Hard length-constrained pieces** (haiku, tweet, headline, slide title). Advisors restructure beyond the constraint.
- **Highly emotional or interpersonal communications** (apologies, condolences, family disputes). Advisors handle frame and structure, not emotional register.
- **Decisions already made, where the user wants validation.** The skill is for genuine deliberation. If the user's mind is made up, it produces frustration rather than insight.
- **Single-shot creative writing where voice is the product** (poems, fiction passages). Advisors diagnose structure and overwhelm voice.
- **Trivial questions with one right answer.** Answer directly.

When the input matches one of these, tell the user which category seems to match, offer the right alternative, and wait for confirmation before proceeding.

---

## Integration with other analysis tools

Workflow positioning (same options as `ai-council`):

- **Fact-checking or rhetorical analysis alone:** sufficient for source credibility and surface-level claims.
- **Deep council alone:** best for decisions, strategy questions, and evaluating ideas where multiple theoretical perspectives add value.
- **Fact-check first, then deep council:** strongest combined analysis. The fact-check handles source credibility and claim verification; the council handles structural and theoretical critique. Use for high-stakes evaluative work (source material evaluation, policy analysis, strategic decisions).
- **Deep council first, then fact-check:** run the council first when you want to identify which questions to investigate, then use a fact-check pass to verify the specific claims the council flagged.

When the council runs after a prior analysis pass, include that analysis as additional context for all advisors:

- Advisors should not repeat fact-checking. The prior analysis already covers source classification, claim verification, and rhetorical technique identification.
- Advisors should focus on structural and theoretical critique: gaps in the argument's logic, unstated assumptions, alternative explanations, practical implications, and forward-looking considerations.
- The chairman should note where the council's findings extend or challenge the prior analysis.

Include the prior analysis in the framed question under a "Prior Analysis" heading so advisors build on it rather than duplicate it.

---

## The five advisors

Identical to `ai-council`. Repeated here so the skill is self-contained.

### 1. The Contrarian
Actively looks for what is wrong, what is missing, what will fail. Assumes the idea has a fatal flaw and tries to find it. Not a pessimist; the friend who saves you from a bad deal by asking the questions you are avoiding.

### 2. The First Principles Thinker
Ignores the surface question and asks "what are we actually trying to solve?" Strips away assumptions. Rebuilds the problem from the ground up. Sometimes the most valuable output is this advisor saying "you are asking the wrong question entirely."

### 3. The Expansionist
Looks for upside everyone else is missing. What could be bigger? What adjacent opportunity is hiding? What is being undervalued? Does not care about risk; that is the Contrarian's job.

### 4. The Outsider
Has zero context about the user, their field, or their history. Responds purely to what is in front of them. The most underrated advisor; experts develop blind spots and the Outsider catches what is obvious to insiders but confusing to everyone else.

### 5. The Executor
Only cares whether this can actually be done and what the fastest path is. Ignores theory, strategy, and big-picture thinking. Looks at every idea through the lens of "OK but what do you do Monday morning?"

The three tensions: Contrarian vs Expansionist (downside vs upside), First Principles vs Executor (rethink vs ship), Outsider keeping everyone honest.

---

## How a deep session runs

```
0.   Frame and enrich context              (parent, no pause)
0.5. Fact-check pass                        (only if source material is being evaluated)
1.   CHECKPOINT 1: clarifying questions     (parent asks, user answers)
2.   First-pass advisor responses           (5 sub-agents in parallel)
3.   CHECKPOINT 2: assumption surfacing     (user reads, user clarifies)
4.   Advisor redraft                        (only those flagged by user)
5.   Anonymous peer review                  (5 sub-agents in parallel)
6.   Chairman synthesis
7.   CHECKPOINT 3: post-synthesis iteration (up to 2 rounds)
8.   Final report and annotated transcript
```

Each checkpoint has a "skip" affordance: `skip`, `ok`, `proceed`, or empty reply moves on. This keeps deep mode useful when the user realizes partway through that the question is simpler than they thought.

After every completed phase, write a `session_state.json` marker so the session can be resumed. See "Resume" below.

---

## Phase 0: Frame and enrich context

Scan the workspace for context files that would help advisors give grounded, specific advice rather than generic takes:

- `CLAUDE.md` or `claude.md` (workspace context, preferences, constraints)
- Any `memory/` or `.auto-memory/` directory (audience profiles, voice docs, past decisions)
- Files the user explicitly referenced
- Files obviously relevant to the question (pricing question: revenue files; launch question: launch notes)

Do not spend more than 30 seconds. Reframe the user's raw question as a clear, neutral prompt that all five advisors will receive. The framed question should include:

1. The core decision or question
2. Key context from the user's message
3. Key context from workspace files (stage, audience, constraints, past results, relevant numbers)
4. What is at stake (why this decision matters)
5. **Publication context** (when analyzing a source): who wrote it; when; what was happening at the time; conflicts of interest or incentives. If the source is a corporate publication, note what corporate events preceded it. Advisors evaluate the piece in context, not as an abstract argument.
6. **Author credibility:** if a co-author's credentials are stated or implied, verify they are current. Note conflicts of interest (board seats, equity, investment relationships).
7. **If running after a prior analysis pass:** include that analysis under a "Prior Analysis" heading.

Do not add your own opinion or steer the framing. If the question is too vague ("council this: my business"), ask one clarifying question, just one, then proceed.

Save the framed question as `framed_question.md` in the session folder.

### Sanity-check input fit

After framing, check whether the input matches a category from "When NOT to use this skill." If it does:

- Name the category that seems to match.
- Offer the right alternative (fast council, write a draft first, edit directly, answer the question without convening, etc.).
- Wait for explicit confirmation before proceeding to Phase 0.5 or Checkpoint 1.

Do not refuse outright; the user may have a reason for invoking the deep council on an unusual input. The goal is to surface the mismatch before spending advisor cycles on a poor fit.

### Output paths

Session folder lives flat in the working directory: `<working_dir>/council-<YYYY-MM-DD-HHMM>/`.

```
council-2026-04-25-1430/
├── framed_question.md
├── fact_check.md                   (only if Phase 0.5 ran)
├── session_state.json
├── advisor_<n>_first_pass.md       (×5)
├── advisor_<n>_second_pass.md      (only if redrafted)
├── peer_review_<n>.md              (×5)
├── chairman_synthesis.md
├── chairman_synthesis_v<round>.md  (only if re-run)
├── <project_name>-COUNCIL REPORT.html
└── <project_name>-COUNCIL TRANSCRIPT.md
```

The HTML report and Markdown transcript write to the working directory itself, not inside the session folder. Intermediate artifacts stay in the session folder.

After Phase 0 completes, write `session_state.json`:

```json
{
  "last_completed_phase": 0,
  "next_checkpoint": 1,
  "session_id": "council-2026-04-25-1430",
  "anonymization_seed": "<sha256 of session_id, first 16 hex chars>",
  "round": 0,
  "status": "in_progress"
}
```

The seed is fixed for the lifetime of the session. See Phase 5 for how it is used.

---

## Phase 0.5: Fact-check pass (source material only)

Run this only when the council is evaluating a published piece (essay, article, white paper, corporate announcement). Skip for decision questions, strategy questions, or when running after a prior analysis pass that already handles fact-checking.

Use web search to verify the source's key factual claims: statistics, historical assertions, attributed quotes, characterizations of third parties, and author credentials. Focus on claims the argument depends on, not trivia.

Produce a short fact-check summary (one bullet per claim) categorized as:

- **Verified:** claim is accurate
- **Inaccurate/misleading:** claim is wrong or materially misleading (provide correction)
- **Unverified:** claim could not be confirmed or denied

Save as `fact_check.md`. Include the summary in the framed question under a "Fact-Check Results" heading so advisors build on verified ground rather than accepting claims at face value.

After Phase 0.5 completes, update `session_state.json` (`last_completed_phase: 0.5`).

---

## Checkpoint 1: Clarifying questions (consolidated)

**Design choice:** the *parent* asks clarifying questions on behalf of the collective advisors, not five parallel advisors asking their own questions. This avoids duplicated "what's the budget?" noise. The parent generates a single list of the highest-leverage unknowns by mentally simulating what each advisor would struggle with.

### Produce the clarification prompt

Internally generate this prompt:

> Given the framed question and each advisor's thinking lens (Contrarian, First Principles, Expansionist, Outsider, Executor), list the three to five specific unknowns that, if clarified, would most sharpen the council's analysis. For each, note which advisor's perspective depends on it most.

Render to the user as:

```
Before I dispatch the council, three to five quick clarifications would sharpen the advisors' analysis. Answer what you can; skip what you can't or don't want to.

1. [question] (which advisor perspective needs it)
2. [question] (which advisor perspective needs it)
3. [question] (which advisor perspective needs it)

(Reply with answers, or type "skip" to proceed with what we have.)
```

### Handle the response

- **Substantive reply:** append to `framed_question.md` under a "Clarifications" heading. Proceed to Phase 2.
- **"skip", "ok", "proceed", or empty:** proceed with the original framed question. Note the skip in the transcript.
- **Partial reply:** append what the user gave. Do not push for more.

Update `session_state.json` (`last_completed_phase: 1`).

---

## Phase 2: First-pass advisor responses

Tell the user what is about to happen: "Convening the council: 5 advisors are analyzing your question independently. Roughly 90 seconds."

Dispatch all 5 advisors as sub-agents in parallel. Each receives the framed question (including clarifications, fact-check results, publication context, and any Prior Analysis).

**Sub-agent prompt for each advisor:**

```
You are [Advisor Name] on an AI Council.

Your thinking style: [paste advisor description]

A user has brought this question to the council:

---
[framed question, including Publication Context, Author Credibility, Fact-Check Results, Prior Analysis, and Clarifications sections if present]
---

Respond from your perspective. Be direct and specific. Do not hedge or try to be balanced; lean fully into your assigned angle. The other advisors will cover the angles you are not.

If the source material contains factual claims not covered in the Fact-Check Results, flag any that the argument depends on and note if they are unverified. Do not repeat verification already provided.

After your main analysis, append a short section titled **"Assumptions I am making"** that lists the 2 to 3 most load-bearing assumptions your analysis depends on. Do not soften your stance. Do not hedge. Surface assumptions plainly so they can be verified. If any of them are wrong, your analysis is wrong, and that is worth knowing now rather than later.

Keep your response between 150 and 300 words for the analysis, plus the assumption section. No preamble.
```

Save each response as `advisor_<n>_first_pass.md`.

Update `session_state.json` (`last_completed_phase: 2`).

---

## Checkpoint 2: Assumption surfacing

Same upstream-propagation principle as Checkpoint 3. When the user flags a wrong assumption, that correction changes the context the analysis was built on. Default: a general correction triggers a **full redraft** across all 5 advisors. The same misread usually lives latently in other advisors too; they just did not surface it.

### Render the assumption summary in two views

**View 1: Per-advisor assumptions:**

```
All five advisors have weighed in. Before I run peer review, here is what each is assuming:

**The Contrarian:** [2-3 assumption bullets]
**The First Principles Thinker:** [2-3 assumption bullets]
**The Expansionist:** [2-3 assumption bullets]
**The Outsider:** [2-3 assumption bullets]
**The Executor:** [2-3 assumption bullets]
```

**View 2: Shared assumptions (3+ advisors):**

After the per-advisor view, scan the assumption lists semantically (not verbatim) and surface assumptions held by 3 or more advisors:

```
**Shared assumptions** (held by 3+ advisors, highest priority to validate):
- [assumption] (held by [advisor list])
- [assumption] (held by [advisor list])
```

Shared assumptions are the highest-leverage targets: correcting one invalidates multiple advisor analyses simultaneously. If no assumption is shared by 3+ advisors, omit this view and note: "No widely shared assumptions; all are advisor-specific."

### Render the menu

```
Any of these wrong? You can:

1. **Proceed:** assumptions look right, run peer review. Type "proceed".
2. **Full redraft with correction** (recommended): all 5 advisors redraft with your correction. Slower, but the peer review reflects the right context. Type: "correct: [your correction]".
3. **Targeted redraft:** only specific advisors redraft. Faster, use when the correction is genuinely local. Type: "targeted: [Advisor1, Advisor2] : [your correction]".
4. **Show analyses:** see the full first-pass responses, then re-prompt with this menu. Type "show analyses".
```

Default: do not show the full first-pass analyses unless the user picks option 4. Showing them up front buries the assumption signal.

### Handle the response

- **Proceed:** move to peer review.
- **Full redraft with correction:** append the correction to `framed_question.md`, re-dispatch ALL 5 advisors in parallel. Default when correction is given without naming advisors.
- **Targeted redraft:** re-dispatch only named advisors. Each keeps perspective and edge, redrafts with new context.
- **Show analyses:** render the five `advisor_<n>_first_pass.md` files inline, then re-render the assumption summary and menu. No state change, no extra cost beyond the render.
- **Unclear or correction without explicit scope:** treat as full redraft. Ambiguity means the correction likely affects more than one advisor.

### When to interpret a correction as targeted vs. full

A correction without explicit "targeted:" scope defaults to **full redraft.** The same misread usually lives latently in advisors who did not voice it.

**Interpret as targeted only when all of these hold:**

1. The correction maps to a critique that 1-2 advisors made load-bearing (visible in the per-advisor assumption view).
2. Other advisors either accepted the same constraint already or addressed a different dimension entirely.
3. The corrected assumption is not in the shared-assumptions view.

When any of these is unclear, default to full. The token cost of one extra full redraft is modest compared to a chairman synthesizing on stale advisor responses.

Save redrafted responses as `advisor_<n>_second_pass.md`. Use second-pass responses (or first-pass if no redraft) for peer review.

Update `session_state.json` (`last_completed_phase: 4`).

---

## Phase 5: Anonymous peer review

This step is the core of the LLM Council methodology. Advisors evaluate each other's work, catching blind spots that no single perspective would find.

### Deterministic anonymization

Use the `anonymization_seed` from `session_state.json`. Derive a stable A through E mapping for the session by hashing `seed + advisor_number` and sorting. The same Advisor X maps to the same Response letter across round 1, round 2, and any subsequent rounds within this session. This makes round-to-round diffs meaningful: Response B in round 1 and Response B in round 2 are the same advisor's evolution.

The mapping is revealed only in the final transcript, not to the user mid-flight or to the peer reviewers.

### Dispatch reviewers

Spawn 5 peer reviewers in parallel. Each sees all 5 anonymized responses and answers four questions:

```
You are reviewing the outputs of an AI Council. Five advisors independently answered this question:

---
[framed question]
---

Here are their anonymized responses:

**Response A:**
[response]

**Response B:**
[response]

**Response C:**
[response]

**Response D:**
[response]

**Response E:**
[response]

Answer these four questions. Be specific. Reference responses by letter.

1. Which response is the strongest? Why?
2. Which response has the biggest blind spot? What is it missing?
3. What did ALL five responses miss that the council should consider?
4. What factual claims or contextual assumptions are the responses treating as established that should be verified?

Keep your review under 250 words. Be direct.
```

Save reviews as `peer_review_<1-5>.md`.

Update `session_state.json` (`last_completed_phase: 5`).

---

## Phase 6: Chairman synthesis

The chairman gets everything: original question, all 5 advisor responses (de-anonymized so the chairman knows which advisor said what), all 5 peer reviews, and on a re-run, the annotated transcript of prior rounds. Synthesis reflects the full arc, not just the final snapshot.

```
You are the Chairman of an AI Council. Your job is to synthesize the work of 5 advisors and their peer reviews into a final verdict.

The question brought to the council:
---
[framed question, including all clarifications and prior-round context]
---

ADVISOR RESPONSES:

**The Contrarian:**
[response]

**The First Principles Thinker:**
[response]

**The Expansionist:**
[response]

**The Outsider:**
[response]

**The Executor:**
[response]

PEER REVIEWS:
[all 5 peer reviews]

Produce the council verdict using this exact structure:

## Where the Council Agrees
[Points multiple advisors converged on independently. High-confidence signals.]

## Where the Council Clashes
[Genuine disagreements. Present both sides. Explain why reasonable advisors disagree.]

## Blind Spots the Council Caught
[Things that emerged through peer review. Things individual advisors missed that others flagged. Include unverified claims or contextual assumptions flagged in peer review question 4.]

## Advisor Position Map
[Table: Advisor | Stance (1-2 word label, e.g., Cautious, Critical, Bullish, Pragmatic) | Core Thesis (one sentence)]
Note which advisor was rated strongest by the most peer reviewers, and which was rated weakest. Highlight any 3+ reviewer consensus.

## The Recommendation
[Clear, direct recommendation. Not "it depends." A real answer with reasoning.]

## The One Thing to Do First
[A single concrete next step. Not a list. One thing.]

The chairman can disagree with the majority. Strong reasoning beats a head count.
Be direct. Do not hedge.
```

Save as `chairman_synthesis.md` (or `chairman_synthesis_v<round>.md` for re-runs).

Update `session_state.json` (`last_completed_phase: 6`).

---

## Checkpoint 3: Post-synthesis iteration (bounded)

**Design principle:** clarifications at the chairman stage propagate upstream, not as addenda. When the user reads the synthesis and realizes there is missing context, that context would have changed what the advisors wrote. Default re-run path: **full re-run.** All 5 advisors redraft with new context, peer review runs again (same anonymization seed), chairman re-synthesizes.

Render the synthesis to the user, then:

```
This is the council's verdict. You can:

1. **Accept:** I'll generate the final report and transcript. Type "accept" or "ship it".
2. **Full re-run** (recommended when adding context): all 5 advisors redraft with your clarification, peer review runs again, chairman re-synthesizes. Slower, but the verdict actually reflects the new context instead of treating it as an appendix. Type: "re-run: [your clarification]".
3. **Targeted re-run:** only specific advisors redraft. Faster, only use when the clarification is genuinely local. Type: "targeted: [Advisor1, Advisor2] : [your clarification]".

Up to 2 re-run rounds before the council closes. (Current round: [N] of 2.)
```

### Handle the response

- **Accept:** go to Phase 8.
- **Full re-run:** re-dispatch ALL 5 advisors with original framed question + all prior clarifications + new clarification. Re-run peer review (same anonymization seed). Re-synthesize. Increment round counter, return to Checkpoint 3. Default if scope is ambiguous.
- **Targeted re-run:** re-dispatch only named advisors with new clarification. Run peer review again on the current set of responses (same seed). Re-synthesize. Increment round counter.
- **Unclear:** ask once whether full or targeted re-run. Default to full if still ambiguous.

**Hard cap:** 2 re-run rounds total. After round 2: "Council has concluded at the 2-round cap. Ship the current verdict, or start a fresh council session if you want to go further."

### Before Round 2 dispatch: explicit revision approval

If the user's re-run clarification implies edits to the source artifact (memo, proposal, draft) rather than just additional framing context, do not dispatch Round 2 silently. The user may be approving the *idea* of a re-run while the parent's revisions go beyond their intent.

- **Clarification adds context only** (e.g., "audience is more technical than you assumed"): dispatch directly.
- **Clarification implies artifact edits** (e.g., "agree about X, add Y, fix Z"): produce the revised artifact, render it inline, and ask: "Round 2 will run on this revised version. Proceed, adjust, or revert?" Wait for explicit approval. A bare number choice ("2") is not sufficient approval for revisions the parent authored.

This prevents the parent's interpretation of the user's intent from propagating silently into Round 2.

### When the user's response is a mixed message

The user may reply with both an explanation request and an edit or re-run instruction in the same message ("Explain why X, but also do Y"). Do not silently execute both.

- **Independent explanation + edit** (e.g., explain three points + add a placeholder): execute the edit, render it, then explain the requested points, then re-prompt the Checkpoint 3 menu. State explicitly which actions you took and in what order.
- **Conflicting or interacting** (e.g., explain why X is recommended + change X): explain first, then re-prompt the menu without executing the edit. The user may revise the instruction once they understand.

The point is to keep the user's intent visible.

### Why no chairman-only re-synthesis option

Earlier versions offered a "light re-run" where only the chairman re-synthesized with new context. User feedback surfaced an "appendix" feel: the clarification was acknowledged but not actually integrated into how each advisor thinks. Removed in favor of full re-run as the default.

Update `session_state.json` (`last_completed_phase: 7`, increment `round`).

---

## Phase 8: Final report and transcript

### Backup before overwriting

Before writing the report or transcript, check whether files at the target paths already exist. This is rare in a fresh session folder but common when resuming a completed session for a re-run, or when a prior council on the same project produced a deliverable in the working directory.

If a previous file exists at the target deliverable path, rename it with a timestamp first:

- `<project_name>-COUNCIL REPORT.html` → `<project_name>-COUNCIL REPORT YYYY-MM-DD-HHMMSS.html`
- `<project_name>-COUNCIL TRANSCRIPT.md` → `<project_name>-COUNCIL TRANSCRIPT YYYY-MM-DD-HHMMSS.md`

Then write the new versions.

### Filename resolution

Use `<project_name>-COUNCIL REPORT.html` and `<project_name>-COUNCIL TRANSCRIPT.md`, where `<project_name>` is resolved as: user-specified name, then the source document's filename without extension, then the workspace folder name. If the council is evaluating a specific source document, use that document's name as the project name.

Files write to the **working directory** (the user's project folder), not inside the `council-*` session folder.

### Report structure

`<project_name>-COUNCIL REPORT.html` is a single self-contained HTML file with inline CSS. Clean, professional, easy to scan:

1. The question at the top
2. Chairman's verdict prominently displayed
3. Agreement/disagreement visual across advisors (grid, spectrum, or position breakdown)
4. **Checkpoint history:** timeline showing clarifications asked, assumptions flagged, re-runs requested. The "show your work" section that distinguishes a deep session from a fast one.
5. Collapsible sections for each advisor's final response (collapsed by default)
6. Collapsible section for peer review highlights
7. Footer with timestamp, round count, total session time

**Styling:** white background, subtle borders, readable sans-serif (system font stack), soft accent colors to distinguish advisor sections. Professional briefing document, nothing flashy.

`<project_name>-COUNCIL TRANSCRIPT.md` contains: original question; framed question; fact-check results (if any); all clarifications; all advisor passes (first and second, if any); all peer reviews with the anonymization mapping revealed; chairman synthesis (all rounds, if re-run); checkpoint timeline.

After generating, present the report to the user via a link to the file.

Update `session_state.json` (`last_completed_phase: 8`, `status: "complete"`).

---

## Resume

A council session can be resumed if interrupted (terminal closes, user steps away, Claude Code session ends or compacts). It can also be reopened later when new context arrives.

### Triggers

`resume council`, `resume the council`, `reopen council`.

### How resume works

1. Scan the working directory for `council-*` folders. If multiple, list them with timestamps and ask which to resume. If one, use it.
2. Read `session_state.json` to determine `last_completed_phase`, `next_checkpoint`, `round`, `status`, and `anonymization_seed`.
3. Reload artifacts that exist: `framed_question.md`, `fact_check.md`, all advisor passes, peer reviews, chairman synthesis.
4. Re-enter at the next phase or checkpoint:
   - `last_completed_phase: 0` → continue at Phase 0.5 (if source material) or Checkpoint 1.
   - `last_completed_phase: 1` → continue at Phase 2 (dispatch advisors).
   - `last_completed_phase: 2` → render Checkpoint 2 from existing first-pass files.
   - `last_completed_phase: 4` → continue at Phase 5 (peer review).
   - `last_completed_phase: 6` → render Checkpoint 3 from existing chairman synthesis.
   - `last_completed_phase: 8, status: "complete"` → ask whether the user wants to start a fresh Checkpoint 3 round with new context. Treat new context as round 1 against the existing synthesis. The hard cap of 2 re-run rounds resets per resumed session.
5. Use the existing `anonymization_seed` for peer review consistency across rounds.

### Use cases

- Mid-session interruption: meeting, terminal close, accidental new thread, Claude Code compaction.
- Returning the next morning to finish a Checkpoint 3 iteration.
- Adding new information days or weeks later to a completed session ("now we know X, what would the council say?").

---

## Important rules

- **Always spawn advisors and reviewers in parallel.** Sequential runs waste time and leak thinking between advisors.
- **Use the deterministic anonymization seed** for the duration of a session. Same A through E mapping across all rounds. New session: new seed.
- **Anonymize for peer review every round** with the session-stable seed. Reveal the mapping only in the final transcript.
- **Never soften the advisor edge.** Checkpoint 2 surfaces assumptions; it does not soften stance. The assumptions layer is additive, not a hedge.
- **Cap Checkpoint 3 at 2 rounds.** Past that, the session is diverging, not converging.
- **The chairman can disagree with the majority.** Strong reasoning beats a head count.
- **"skip" is always valid.** At any checkpoint, the user can bypass interaction and proceed with current state.
- **Tell the user what is happening between phases.** "Advisors weighing in (5 sub-agents in parallel; about 90 seconds)." "Peer review running." "Chairman synthesizing." Silence in deep mode is worse than in fast mode because the session is longer.
- **Do not run the council on trivial questions.** If the user invokes this skill for something with one right answer, offer to switch to `ai-council` or answer directly.
- **Always write `session_state.json` after each completed phase** so resume works reliably.
- **Backup before overwriting deliverable files** in the working directory.

---

## Session continuity

If the user has installed the `handoff-resume` skill (or maintains an equivalent session-continuity protocol), offer at the end of the council to record key strategic decisions, rejected paths, and the council's recommendation in the project's session log. This makes the verdict legible to future sessions that pick up the same project, rather than buried in a one-off HTML report.
