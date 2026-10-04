---
name: learn-best-practice
description: Use when the user wants to actually internalize an installed best practice — not just understand or apply it once, but build durable recall and independent competence so they can use it correctly later without an AI assistant present. Combines active-recall testing, spaced-review scheduling, and a portable memory aid. Distinct from explain-best-practice (one-time why) and teach-best-practice (explaining to others).
source: Roediger & Karpicke (2006) "The Power of Testing Memory" — the testing effect; Cepeda et al. (2006) meta-analysis on distributed/spaced practice; Ebbinghaus (1885) forgetting curve; Feynman Technique (self-explanation); Rohrer & Taylor (2007) interleaving practice research
tags: [learning, retention, active-recall, spaced-repetition, self-testing, independent-competence, memory]
related: [explain-best-practice, teach-best-practice, learn-grimoire, suggest-best-practice, install-grimoire]
---

# Learn Best Practice

Build durable, independent competence with a specific installed best practice, so the user can recall and apply it correctly later without an AI assistant present.

## Why This Is Best Practice

**Adopted by:** Retrieval practice (the testing effect) is the core method behind medical-education spaced-repetition question banks (Anki, UWorld), language-learning platforms, and pilot and surgical simulation training — all fields where "the learner must perform correctly later, unaided" is the actual requirement, not just passing comprehension in the moment.
**Impact:** Roediger & Karpicke (2006) found students given a single practice test retained significantly more of the material a week later than students who reread the same material the same number of times — despite the practice-test group reporting less confidence immediately afterward. Cepeda et al. (2006)'s meta-analysis of over 300 studies found spacing review sessions over time roughly doubles long-term retention compared to massed (crammed) review of the same total study time.
**Why best:** A one-time explanation, however good, produces a feeling of understanding that decays within days without active recall (Ebbinghaus, 1885) — a user can explain a practice right after hearing it and still fail to recall or apply it correctly a week later, which directly defeats the goal of using it without an AI present. Active engagement — retrieval, not rereading — is what closes that gap.

Sources: Roediger & Karpicke, "The Power of Testing Memory," Perspectives on Psychological Science (2006); Cepeda et al., "Distributed Practice in Verbal Recall Tasks," Psychological Bulletin (2006); Ebbinghaus, "Memory: A Contribution to Experimental Psychology" (1885); Rohrer & Taylor, "The Shuffling of Mathematics Problems Improves Learning," Instructional Science (2007)

## Steps

### Step 1: Identify what to learn

Confirm the specific installed practice (or small set of practices) the user wants to internalize. If ambiguous, ask which one, or match against installed skills using the standard scoring model.

**Uninstalled skill fallback:** If the named practice isn't installed (not present in `.grimoire/` or listed in `SKILLS.md`), check whether it exists in a cloned skill repo on disk instead — the current working directory or a path the user names, containing a `skills/` directory (the only structural requirement for grimoire package discovery). If the target `SKILL.md` is found there, read it directly from that path and proceed with the full retention loop, stating which path the content came from — installation is only required for a skill to auto-trigger during normal routing, not to learn from it directly. If the skill isn't found installed or in any cloned repo on disk, say so and give the install/clone command.

### Step 2: Baseline check

Before presenting any content, ask the user to state, in their own words, what they think the practice is for — a light Feynman-style self-explanation prompt. This calibrates how much depth is needed and is itself a first retrieval attempt.

### Step 3: Compress into a memorable form

Present a short "trigger → core steps → one common trip-up" card — built for memorization, not the full deep-dive. If the user wants the complete mechanism, evidence, and failure-mode analysis, hand off to `explain-best-practice` first, then return here for the retention loop.

### Step 4: Active-recall check

Present a realistic scenario and have the user state what they'd do without looking anything up. Compare their answer against the actual skill's steps and give specific feedback on what they got right and what they missed. This retrieval step is the core retention mechanism — never skip it, even if the user seems confident.

**If the recall attempt reveals a real gap** (not just imprecise wording, but a missed step or a wrong mental model): correct only that specific gap, then present a second, different scenario to re-test it. Don't proceed to Step 5 until the user demonstrates correct recall — handing someone a memory aid for a practice they just got wrong reinforces the error, not the practice.

### Step 5: Portable memory aid

Produce a short, carry-with-you cue: a one-line trigger phrase plus a 3–5 item checklist the user can recall mentally in the real world with no AI present.

### Step 6: Schedule spaced review

Recommend concrete re-test intervals — tomorrow, in three days, in a week — and explain exactly how to self-test next time without the AI: try to recall the checklist before re-reading it, then check.

### Step 7: Interleave if learning multiple practices

If the user is learning several practices in one session, mix scenarios across them rather than mastering one fully before starting the next — interleaving improves discrimination between similar practices and long-term transfer.

### Step 8: Offer to install, if it wasn't already installed

If the practice was read from a cloned repo rather than an installed copy (per Step 1's fallback), offer once the learning loop completes: "Want to install `[skill-name]` as a global skill now, so it auto-triggers automatically going forward? [y/n]" If yes, hand off to `install-grimoire` with the specific skill path pre-filled (`grimoire install --skill [domain]/[subdomain]/[skill-name]`) rather than re-implementing the install/confirm/report flow here. If the practice was already installed, skip this offer entirely — asking to install something already installed is just noise.

## Rules

- Never skip the active-recall step (Step 4) even when the user seems confident — confidence after a single explanation is a known unreliable signal of actual retention.
- If the recall check reveals a real gap, correct it and re-test before producing the memory aid — never hand out a memory aid for a practice the user just got wrong.
- A skill doesn't need to be installed to be learned from — installation is for auto-triggering during routing, not a prerequisite for reading and internalizing a skill file directly.
- Only offer to install at the end if the skill wasn't already installed — never ask to install something the user already has installed.
- Delegate the actual install/confirm/report flow to `install-grimoire` rather than reimplementing it here.
- The portable memory aid must be short enough to actually memorize — 3 to 5 items, not a restatement of the full step list.
- State recommended review intervals explicitly — don't leave spaced review as an implicit, unstated expectation.
- Search the internet to verify a claim about the specific practice when uncertain or the topic is recent — don't rely solely on training-data recall. If no internet-access tool is available, say so and proceed on best available knowledge, flagged as unverified. After searching, state what was found before proceeding, and keep queries general and factual, not the user's personal details.

## Examples

**Learning a specific practice for later, unaided use:** A user says "I want to actually learn the margin-of-safety concept, not just apply it once." The skill asks the user to explain it in their own words first, presents a compressed trigger-steps-trip-up card, then poses a realistic stock-valuation scenario and has the user state their approach before checking it against `calculate-margin-of-safety`'s actual steps — closing with a 4-item memory checklist and a recommended re-test in three days.

**Learning multiple related practices together:** A user wants to internalize three related code-review practices at once. Rather than mastering the first fully before starting the second, the skill interleaves scenarios across all three from the start, since discriminating between similar practices under mixed conditions is closer to how they'll need to be recalled in the real world.

## Common Mistakes

- **Re-explaining instead of quizzing** — when the user asks to "review" a practice they've seen before, defaulting to another explanation skips the retrieval practice that actually builds retention.
- **Producing a memory aid too long to memorize** — a 10-item checklist isn't a memory aid, it's the original document restated; keep it to 3–5 items.
- **Skipping the baseline or active-recall step because the user "already knows this"** — self-reported familiarity is not the same as demonstrated recall; the check takes one exchange and catches real gaps.
- **Producing the memory aid despite a failed recall check** — moving to Step 5 right after Step 4 reveals a real gap skips the correction and re-test, and cements the wrong version as the "memorized" one.
- **Offering to install a skill that's already installed** — only make the install offer when the practice was actually read from a cloned repo, not an installed copy; otherwise it's a redundant, slightly confusing prompt.
- **Blocking practice by skill instead of interleaving** — when learning several practices in one sitting, mastering one fully before starting the next is worse for long-term discrimination than mixing scenarios across them.

## When NOT to Use

- The user wants a one-time explanation of why a practice works with no retention goal — use `explain-best-practice` instead.
- The user wants to explain or advocate for a practice to someone else (a team, manager, client) — use `teach-best-practice` instead.
- The user wants to understand grimoire itself rather than one specific practice — use `learn-grimoire` instead.
- The user hasn't picked a practice yet — use `suggest-best-practice` or `discover-best-practices` instead.
