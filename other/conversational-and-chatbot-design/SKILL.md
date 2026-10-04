---
name: conversational-and-chatbot-design
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P016
  - P015
  - P023
  - P027
  - P037
  - P040
  - P067
  - P068
  claims:
  - C01367
  - C01368
  - C01414
  - C01415
  - C01253
  - C01272
  - C00840
  - C00841
  - C01270
  - C01289
  - C00838
  - C00839
  - C01003
  - C01004
  - C01271
  - C01326
  - C01383
  - C01384
  evidence:
  - E00514
  - E00515
  - E00526
  - E00527
  - E00478
  - E00487
  - E00378
  - E00379
  - E00485
  - E00490
  - E00376
  - E00377
  - E00390
  - E00391
  - E00486
  - E00501
  - E00520
  - E00521
  source_anchors:
  - 2c3bf56d4ce6-c0000
  - 2c3bf56d4ce6-c0001
  - e16b4082ee9c-c0000
  - e16b4082ee9c-c0001
  - 2cf0ebac9e78-c0000
  - 2cf0ebac9e78-c0005
  - e16b4082ee9c-c0002
  authored_from_digest: 44c984b89261124931f8d981fc3e4c786e1c6d7bd77f6406999bb6ac5c917c81
---

# Conversational and Chatbot Design

Design conversation as genuine, cooperative, context-aware, sequential interaction grounded in human
conversation — with naturalness and emotionality as the baseline and avatars as tested choices — not
a chat or voice facade.

## When this applies

- Designing an interface that is meant to feel recognizably conversational (P001).
- Assessing whether a person, machine, or conversational agent understands a concept, topic, or conversational action (P016).
- designing the opening and everyday phrasing (P015).
- designing or reviewing any interface that uses words (P023).
- adding or reviewing a visual avatar or identity cue (P027).
- any human-centered interaction design task (P037).
- diagnosing why a product feels disjointed, or structuring how a team collaborates (P040).
- deciding how much emotional expressiveness the chatbot shows (P067).
- The task involves multi-turn requests, incremental specification, references to earlier turns, repair, or sequence closure (P068).

## Procedure

Apply these principles to the situation under review; for each, name the user need at stake and the trade-off the choice carries.

1. Design conversational interfaces as ordered interaction sequences grounded in human conversation, not as response text or visual controls with language attached. (P001)
2. Evaluate claims of machine understanding by demonstrated performance across varied probing and phrasing, and scope those claims to the domains where that performance holds. (P016)
3. Apply naturalness practices - self-introduction, a welcoming opening that states capabilities and optionally collects the user's name, addressing the user by name, small talk, echoing user responses, casual language, and humanization techniques such as adaptive response speed - to raise perceived anthropomorphism and social presence and reduce user resistance; naturalness is the baseline for every chatbot. (P015)
4. Never run verbal (writing) design on a separate track from visual and interaction design—splitting it produces an interface of boxes later filled with language and disserves the whole experience—so make decisions about verbal language and nonverbal cues part of the same process at the same time, and give writers and designers a feedback loop on how successful their work was so they can learn and improve. (P023)
5. Do not treat avatars as context-independent improvements: avatar gender and appearance shape user impressions before any message, effects are inconsistent across studies, human-like avatars raise expectations and frustration after failures, and auto-activation can worsen anthropomorphic avatars - pair avatar choices with transparency and failure handling, and test them. (P027)
6. Make systems conversational at a deep level (cooperative, goal-oriented, context-aware, fault-tolerant) rather than adding a surface chat or voice facade, because a facade forces users to fixate on the technology's limits instead of their goals. (P037)
7. Run the work culture on the same conversational principles as the interface—cooperative, goal-oriented, context-aware, quick and clear, turn-based, truthful, polite, and error-tolerant—waiting your turn and truly listening (an underrepresented skill), treating the work as an interactive collective process, and building a safe, error-tolerant environment where ideas that may fail are welcome; some authority and documentation is a normal fact of organizational life, but keep clear goals and a standing willingness to reflect and improve. (P040)
8. Use emotionality practices - exclamatory feedback, graphical media (emoji, emoticons, GIFs, memes), a social-oriented informal style, and humor - to raise social presence and positive perceptions such as enjoyment, credibility, engagement, and behavioral intentions. (P067)
9. Avoid a two-turn valid-query model when users need to build on prior turns; preserve sequential context so follow-ups, references, repair, and closings have an interactional target. (P068)

## Principles applied

- **P001** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P016** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P015** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P023** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P027** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P037** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P040** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P067** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P068** (high) — grounded in claims/evidence and chunk anchors in `sources/`.

## Provenance

Grounded in principles P001, P016, P015, P023, P027, P037, P040, P067, P068, their backing claims
and evidence records, and paragraph-level source anchors under `sources/anchors/`. Every cited id
resolves into this package's distilled spine; see `provenance-ledger.md` and `reports/faithfulness-
report.yaml`.
