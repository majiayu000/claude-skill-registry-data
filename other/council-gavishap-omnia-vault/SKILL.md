---
name: council
description: Convene a cross-model council on a hard decision — five seats, each filled by ONE real agent (some Codex, some Claude), giving independent opinions that are anonymized, cross-reviewed by the opposite bench, and synthesized into a ruled verdict. Use when the user says "council this", "convene the council", "get multiple perspectives on this", "I'm torn between X and Y", "which option should we pick", "pressure-test this decision", or faces a genuinely uncertain, expensive-if-wrong choice (pricing, positioning, pivot, architecture direction, build-vs-buy). NOT for questions with one right answer, creation tasks, or code review (that's `sparring`). The war-room is the plan; the council is who you ask before changing it.
---

# The Council — five seats, two models, one verdict

One agent gives you one answer, and you can't tell if it's the good one. The
council fixes that structurally: five seats think about the question
**independently**, each seat is a **real, separate agent** — not one model
wearing five hats — the benches review each other's work blind, and the chair
rules.

What makes this council different from a persona exercise: **the seats run on
different models.** Codex and Claude disagree for real — different training,
different instincts — so the tension between seats is genuine, not
theatrical. (Methodology descends from Karpathy's LLM Council by way of Ole
Lehmann's skill — see THIRD-PARTY-NOTICES.md; this implementation is Omnia
Vault's own.)

**Where it sits in the vault:** `sparring` is depth — one rival attacking one
locked plan. The council is **breadth** — five angles on an unlocked
decision. Convene the council *before* locking a direction; spar the design
*after*. A roadmap restructure or a big `/intel` adoption is exactly a
council question.

## The five seats (and who fills them)

| Seat | Thinking style | Default agent | Why that agent |
|---|---|---|---|
| **The Skeptic** | hunts the fatal flaw — what breaks, what's missing, what the user is avoiding | **Codex** (fresh read-only thread) | proven brutal, and cross-model skepticism can't be charmed by the driver's framing |
| **The Rebuilder** | ignores the asked question, rebuilds it from first principles — "what are we actually solving?" | **Claude** (subagent) | strongest at reframing and structure |
| **The Maximalist** | ignores risk, finds the bigger play — what if this works better than expected? | **Claude** (subagent) | generative expansion is its lane |
| **The Outsider** | knows NOTHING about the project — reacts to the bare question only, catching the curse of knowledge | **Codex** (fresh thread **in an empty directory** — mechanically unable to read the repo) | a real outsider, enforced by the sandbox, not by pretending |
| **The Operator** | only cares whether it can actually be shipped — "what do we do Monday morning?" | **Codex** (fresh read-only thread, repo access) | grounds executability in the actual code and plan |

The tensions are the design: Skeptic vs Maximalist (downside/upside),
Rebuilder vs Operator (rethink it/ship it), Outsider keeping both benches
honest. The **driver** (whichever agent runs the session) is the **Chair** —
it frames, convenes, and rules, but never sits a seat.

## Running a session

### 1. Frame (Chair, ~1 minute)

Pull the vault's context the cheap way — `_relay/STATE.md`,
`python scripts/plan_tool.py context` if a plan exists, `search-catalog` on
the topic — and write ONE neutral framed question: the decision, the options,
the constraints and numbers that matter, and what it costs to get it wrong.
No steering, no chair opinion. If the ask is too vague, ask the user exactly
one clarifying question first. Check `_relay/council/` for a prior session on
the same ground before re-convening.

**The Outsider gets a stripped version:** the decision and options ONLY — no
project name, no history, no vault context. What survives translation to a
stranger is the signal.

### 2. Convene (all five seats in parallel, blind)

Independence rules — the whole value lives here:

- Seats never see each other's opinions.
- Each Codex seat is its OWN fresh `codex exec` thread (never resume one
  seat's thread for another).
- Each Claude seat is its own subagent with only the framed question.
- Launch everything in parallel: Claude seats via the Agent tool in one
  message; Codex seats as background bash calls.

Every seat gets: its seat identity + thinking style, the framed question
(stripped version for the Outsider), and the instruction to argue its angle
at full strength in 150–300 words — no hedging, no balance, the other seats
cover the rest. **A seat must end with one line:**
`POSITION: <one-sentence stance>`.

Codex seat mechanics (per the sparring skill's rules — stdin feeding, `-o`
capture, 10-minute timeout; resolve `$CODEX` the same way):

```bash
# Skeptic / Operator — read-only, repo visible
"$CODEX" exec -s read-only --json -o "$OUT" - < "$PROMPT" 2>/dev/null >/dev/null
# Outsider — same, but from an EMPTY directory so the repo does not exist to it.
# --skip-git-repo-check is REQUIRED here: codex refuses untrusted non-git dirs
# without it (verified 2026-08-27 — the isolated call then reports it can see
# no project and no repo, which is exactly the point).
cd "$(mktemp -d)" && "$CODEX" exec -s read-only --skip-git-repo-check --json -o "$OUT" - < "$PROMPT" 2>/dev/null >/dev/null
```

An empty output file = a dead seat; relaunch it once, and if it dies again,
report the council as four seats — never ghost-write a missing opinion.

### 3. Cross-bench review (two reviewers, anonymized)

Shuffle the five opinions into `Opinion A..E` (note the mapping privately;
randomize order so no bench can be identified by position). Then two blind
reviewers — **each bench reviews the mixed set, without knowing which
opinions are its own model's**:

- One fresh **Codex** thread and one fresh **Claude** subagent each receive
  the framed question + all five anonymized opinions and answer exactly:
  1. Strongest opinion and why (pick one letter).
  2. Biggest blind spot in any single opinion.
  3. What ALL five missed.

Cross-model review is the point: each model grades work partly written by the
other, and neither knows which is which.

### 4. The Chair rules

De-anonymize. The Chair reads everything and writes the verdict — in chat,
in this exact shape:

```markdown
## Council Verdict: <topic>
**The bench:** Skeptic ⚙ codex · Rebuilder ✳ claude · Maximalist ✳ claude · Outsider ⚙ codex (blind) · Operator ⚙ codex

### Consensus
<what multiple seats reached independently — high-confidence signal>
### Dissent
<the real clashes, by seat name, both sides stated fairly>
### Caught in review
<what only surfaced when the benches graded each other>
### The Chair's ruling
<one committed answer with reasoning — the Chair may side with a lone
dissenter against the majority, and says so when it does>
### First move
<exactly one concrete next step>
```

Rules of the ruling: no "it depends," no smoothing dissent into mush, and the
minority position is preserved in writing even when overruled.

### 5. Keep the record

Write the full session to `_relay/council/<date>-<slug>.md`: framed question
(+ the Outsider's stripped version), seat-by-seat opinions with their agent,
both reviews, the verdict. Committed — a council is convened precisely
because the decision is expensive, and expensive decisions deserve receipts.
If the ruling changes the project: update the plan/roadmap or spar the
resulting design, note it in the relay baton, and compile the decision into a
Wiki note citing the council record. Gate, commit.

## When Codex drives (the mirror)

Same session, benches swapped: Codex fills its seats with its own fresh
threads and fills the Claude seats headlessly —
`claude -p "<seat prompt>" --permission-mode plan --output-format json`, one
call per seat, never reusing a session between seats. The Outsider trick
inverts too: run the headless call from an empty directory. The driving agent
chairs; the Chair never sits.

## Hard rules

- One real agent per seat. The Chair sits zero seats. No seat sees another
  seat's opinion before the review round.
- The Outsider's isolation is mechanical (empty directory), not honor-system.
- Dead seats are reported, never impersonated.
- Anonymize before review, always — including from yourself as far as
  practical: shuffle first, map later.
- Don't convene for trivia, validation-seeking, or anything with a testable
  right answer. Five agents agreeing that Paris is the capital of France is
  not insight.
- The record is part of the verdict — no transcript, no council.
