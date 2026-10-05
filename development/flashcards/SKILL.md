---
name: flashcards
description: Use when creating, testing, or updating active-recall flashcards grounded in session concepts to reinforce retention.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [productivity, flashcards, active-recall, retention]
status: stable
---

# Purpose

Convert session concepts into structured active-recall flashcards. Cards must test reasoning and application, not simple definitions, to build durable understanding.

# Activation

- Concept teaching session just completed. Learner requests cards. `spaced-repetition` needs card generation/update. Revision period (exam, interview, milestone).
- **Skip if**: concept hasn't been taught yet. Goal is deep exploration → `deep-dive`. Active debugging/project work → would interrupt flow.
- **Routing**: generate cards *after* understanding is confirmed. Feed into `spaced-repetition` for scheduling. Cards failed 3 times → trigger `misconception-detector`.

# Inputs

- Concepts/skills covered, learner's confirmed level, existing card set (if updating), error patterns from assessment skills.

# Card Types

- **Concept**: "What is X?" → vocabulary accuracy.
- **Mechanism**: "Trace what happens when X executes." → process understanding.
- **Tradeoff**: "When would you NOT use X?" → decision reasoning.
- **Application**: "Given [context], which [tool/pattern] and why?" → transfer.
- **Debug**: "What's wrong with this code?" → diagnostic thinking.

Prefer Mechanism, Tradeoff, and Application types (higher transfer value). At least 60% of cards should be these types.

# Workflow

1. **Extract** — Identify 3–7 key concepts worth card-ifying. Prioritize mechanisms, tradeoffs, application patterns. Skip long-mastered concepts.
2. **Generate** — 1–2 cards per concept. Front = question (not keyword). Back = complete model response (~100 words max). Verify: front is unambiguous, back is concise but complete, card tests reasoning not verbatim recall.
3. **Test** — Present front only; learner responds before seeing back. Self-score: Easy (fluent) / Hard (needed effort) / Failed (wrong/blank). Update interval.
4. **Handle Failures** — Failed card: re-test after 10 minutes in same session. Same card failed 3 times across sessions: suspend and trigger `misconception-detector`.
5. **Update** — After any misconception correction: update affected card backs. Never leave outdated cards in the deck.

# Rules

- DO: card fronts must be questions, not keywords.
- DO: backs must require explanation, not one-word answers.
- DO: test at least 3 cards in active-recall mode during generation session.
- DO: cross-reference cards for connected concepts.
- DON'T: generate all "What is X?" cards — that's definition-only bias.
- DON'T: let decks grow unbounded — flag cards with ease_factor > 2.5 for 5+ sessions as mastered.
- DON'T: generate cards before understanding is confirmed.
- DON'T: skip active testing — generation is not the end state.

# Output

Card generation: topic, date, cards (front + back + type + difficulty). Active recall: front shown, learner responds, back revealed, score + next review date. Format naturally.

# Checklist

- [ ] 60%+ cards are Mechanism/Tradeoff/Application type.
- [ ] Each card front is a clear question; back is a complete response.
- [ ] At least 3 cards tested in active-recall this session.
- [ ] Cards updated after any misconception correction.
