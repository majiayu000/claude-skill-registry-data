---
name: the-quorum
description: Invocation-only five-member decision council. Run only when the user asks to invoke or convene The Quorum, including "quorum this", "council this", or "convene the quorum". Do not run when the user merely mentions The Quorum, asks how it works, or asks to prepare material for it. Produces independent expert verdicts, anonymous peer review, a chairman synthesis, a pre-mortem, and an interactive HTML dashboard.
---

# The Quorum

A decision gets sharper when it survives disagreement. The Quorum convenes five differentiated experts who each form a verdict **independently**, then challenge each other anonymously, before a chairman calls it. The point is not consensus — it's surfaced, structured disagreement that you can actually act on.

The single most important design rule: **the five members must reason independently before they see each other's work.** If they anchor on one another, you get five flavors of the same answer and the whole exercise is theater. Protect the independence above all else.

---

## Trigger

Runs only when the user asks to invoke or convene it: `quorum this <decision>`, `council this <decision>`, `convene the quorum`, or a direct request to use The Quorum on a decision. Merely mentioning The Quorum, asking how it works, or asking to prepare material for it is not invocation. Never fires proactively. If the invoked decision is trivial or easily reversible, say so and offer a quick take instead of spinning up five agents for a coin-flip.

---

## Step 0 — Intake (don't skip this)

Garbage in, five confident guesses out. Before convening anyone, establish four things. Infer what you can from context; ask **one** batched question only for what's genuinely missing:

1. **Options** actually on the table (including "do nothing").
2. **Constraints** — budget, time, irreversible commitments, non-negotiables.
3. **Success** — what a good outcome looks like in concrete terms.
4. **Reversibility & stakes** — is this a *two-way door* (cheap to undo) or a *one-way door* (expensive or impossible to reverse)? How high are the stakes?

Then do one more thing that pays for itself every time: **name the decisive variable(s)** — the one or two unknowns that would most move the answer — and ask for them now. If you skip this, you get five members all hedging "medium confidence" around the same missing fact, which is wasted deliberation. Surface it up front so the council reasons on something solid. (This is the job the Analyst would otherwise do *inside* the room, too late.)

Keep intake to ~20 seconds of effort. A short, sharp decision brief beats a long interrogation.

---

## Step 1 — Frame check & roster

Before spawning, do three quick things:

**Pick the door.** Classify the decision as one-way or two-way, high or low stakes. This calibrates everything downstream — and it should change what you actually *do*, not just a label. A trivial two-way door earns a **lightning round**: three voices (Skeptic, Operator, Reframer), skip peer review, fast call. A one-way high-stakes door earns the full council plus a heavier pre-mortem. Most decisions sit in between and get the standard treatment.

**Pressure-test the options.** Before anyone deliberates, look hard at the option menu — especially if *you* generated it rather than the user. Are these the real options, or is one a padded compromise that won't survive contact (the tempting "do a small version of both")? Is a genuine option missing? A flawless deliberation over a bad menu is just eloquent garbage. Fix the menu now; the Reframer has explicit license to kill or add options later, but don't rely on that to rescue a weak starting set.

**Pick the roster.** Always seat the **core five**. For decisions dominated by people — hiring, firing, org design, partnerships, anything where buy-in or relationships are the crux — swap **The Reframer** for **The Steward** (defined below), or seat six if the decision genuinely needs both.

### The core five

Each owns a distinct failure mode of real decisions, so they don't blur into each other:

1. **The Analyst** — *epistemics.* What do we actually know vs. assume? What evidence is missing? What's being asserted without support? No speculation without flagging it.
2. **The Skeptic** — *downside.* The strongest case *against* the leading option. Failure modes, second-order risks, who or what could sink this. Push hard, but constructively.
3. **The Strategist** — *time.* How does this look in 12 months and 3 years? Compounding effects, both directions. Cost of waiting vs. acting now. Where's the highest-leverage move?
4. **The Operator** — *execution.* What does doing this actually take — time, money, focus? Real blockers, fastest path to a result. And the honest baseline: what happens if we just *don't*?
5. **The Reframer** — *the frame itself.* Is this even the right question? Is there a third path, a reframe, or an unconventional move that dissolves the original tension instead of resolving it?

### The bench

- **The Steward** — *people.* Who's affected, who resists, whose buy-in you need, the relational and morale cost, the politics. Swap in for people-heavy decisions.

---

## Step 2 — Convene the council (independent verdicts)

**Primary path (parallel subagents available):** Spawn the seated members as parallel agents in a single turn. Give each **only** the decision brief from Steps 0–1 — never another member's output. Use the persona prompts in `references/persona-prompts.md`.

**Fallback path (no subagents — e.g. the chat interface):** Run the members one at a time, but preserve independence by hand: for each member, reason *only* from the original brief, as if the others don't exist. Do **not** let member 2 react to member 1. Write each verdict before moving on, and resist the pull toward consensus. This is less rigorous than true isolation but works if you're disciplined.

Every member returns a committed verdict — but the *shape* of the verdict fits the member's job. Forcing all five to pick from the option menu homogenizes the two voices whose entire value is questioning the menu. So:

**Option-pickers — the Skeptic, Strategist, Operator** — return:

```
VERDICT (one line)
- bullet 1 (the core argument)
- bullet 2
- bullet 3
RECOMMENDS: <which option, or "need more info">
CONFIDENCE: low | medium | high
WOULD FLIP IF: <the single thing that would change their mind>
```

**The Analyst** does *not* have to pick an option — its job is to establish what's true and name the unknown that decides this. It returns the same shape but `RECOMMENDS` becomes **`DECISIVE UNKNOWN: <the fact that, once known, settles the question>`** (it may still endorse an option if the evidence genuinely points one way, but it's never required to).

**The Reframer** is also not bound to the menu — its `RECOMMENDS` may be **a reframe or a third path**, not one of the listed options. That's the point of the seat.

The `CONFIDENCE` and `WOULD FLIP IF` lines are required for everyone regardless of shape. A verdict you can't falsify is an opinion, not analysis.

---

## Step 3 — Anonymous peer review

Relabel the members **A–E** (strip the persona names so authority bias doesn't creep in) and show each the others' verdicts. Each responds briefly:

- What do they **agree** with on reflection?
- What do they **challenge**?
- Does anything move their own confidence up or down?

Keep this tight — two or three sentences per member. The goal is to catch where independent reasoning converged (a real signal) vs. where it collided (the actual decision).

**Guard against false consensus.** Peer review tends to drift toward agreement — sometimes that's good arguments working, sometimes it's just regression to the mean, which is the exact groupthink the anonymization exists to prevent. Two rules: a member who moves their position must name *what specifically* changed their mind (a vague "good points all around" doesn't count); and genuine disagreement gets left standing, not smoothed over. Consensus is earned here, never defaulted to.

---

## Step 4 — Chairman synthesis

The chairman doesn't average the room — it *reads* it. Produce:

1. **The spread.** Where did the five land, and how confident were they? State it plainly. If they clustered, that's a green light. If they split 3–2, **say so** — the split is the finding, not something to smooth over.
2. **Key tensions.** The two or three real disagreements that matter, named honestly.
3. **Strongest 2–3 options** with clear reasoning.
4. **The call** — a recommended next step, calibrated to the door: a reversible call should bias toward action and learning; a one-way door earns more caution. "Gather X specific information first" is a legitimate and often correct call.
5. **Pre-mortem.** The chairman's own verdict gets stress-tested too: *What is the one assumption this recommendation rests on, and what evidence would flip it?* Nobody else checks the chairman — so the chairman checks itself.
6. **Minority report.** If any member holds a *high-confidence* view that contradicts the call, surface it as a named, preserved dissent — in its own words, not averaged into the prose. Do not let a lone high-conviction objector get smoothed into the consensus; that's the voice a council exists to remember. Mandatory on one-way doors.
7. **Deal-breakers.** Anything from the Skeptic or Operator that should hard-stop the leading option.

---

## Step 5 — Output: the dashboard

Build a single self-contained HTML file using `references/report-template.html` as the scaffold (don't reinvent it). Fill every section; remove any bench member you didn't seat. Save it to the outputs directory and present it.

Brand: background `#1C1A1D` (INK), accent `#E2F075` (LIME), text white. The template already encodes these as CSS variables at the top — they're the default theme, not a requirement. Anyone using this skill can swap the `--ink` / `--lime` / `--text` values to their own palette in one place.

Sections, in order: header with the question and a one-way/two-way **door badge**; **the spread** (a visual showing each member's backed option + confidence, so clustering or splits are obvious at a glance); five (or six) **member cards** (name, lane, verdict, three bullets, recommends/confidence/flip); the **peer-review** exchange; and the **chairman box** with the recommendation highlighted and the pre-mortem called out.

---

## Step 6 — Decision journal (the part that compounds)

This is what turns a clever one-off into a system that learns the user's blind spots. It's **optional and depends on a persistent workspace** — in a plain chat session with no durable storage, there may be nowhere to write the file. Don't fail silently: if you can persist it, append a dated entry to `decision-journal.md` (create it if absent) using the format in `references/decision-journal.md`; if you can't, say so plainly and offer to output the entry as text the user can save wherever they keep things. Capture: date, the decision, the door type, the spread, the chairman's call, confidence, and the flip-conditions.

Then — proactively, but briefly — offer the loop: *"Want me to log this so we can check it against what actually happens?"* And when the user returns later, offer to revisit open entries: which calls held up, which flipped, and what that reveals about how they decide. A council that never checks its own track record is just expensive theater. The journal is the calibration loop.

---

## Notes on judgment

- **Match weight to stakes.** Five voices and a pre-mortem for "should I rewrite this email" is overkill — offer a lighter take. Save the full machinery for choices that deserve it.
- **Don't manufacture disagreement.** If the members genuinely agree, the honest output is "they agree, here's why, move." Forced contrarianism is as useless as forced consensus.
- **Independence beats eloquence.** A blunt, differentiated verdict is worth more than a polished one that echoes the others.
- **Know what this is.** The five members are one model role-playing five lenses, not five independent minds — the value is the structured discipline, not literal multiple intelligences. It's a thinking aid, not an oracle, and it shouldn't be used to launder a decision already made. For genuinely irreversible, high-stakes personal calls — medical, legal, large financial — treat the output as a structured prompt, not a substitute for a qualified professional.
