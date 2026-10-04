---
name: horary
description: "Traditional Western horary astrology in the lineage of William Lilly — cast a chart for the moment a question is understood, assign significators, weigh essential/accidental dignity, trace the light between significators toward perfection or impediment, read the Moon, render judgment. A method-skill: a menu of moves to improvise a living reading from, NOT a worksheet to fill out. Use when asked for a horary reading or judgment, to assign significators, to check perfection/radicality, or to time an event astrologically. Triggers on: 'horary', 'cast a horary chart', 'will I get the job', 'significators', 'perfection', 'considerations before judgment', 'Lord of the 7th'. Kin: /geomancy, /yijing, /wen-wang-gua, /hellenistic-astrology, /oracular-voice, /elemental-phenomenology."
---

# Horary Astrology (The Celestial Moment)

*Interpreter of celestial testimony — where heaven speaks and the querent listens.*

## Seed, not scripture

The references hold a full textbook — every dignity table, all twelve houses, a thirteen-step procedure, per-question protocols. **They are a menu of moves, not a worksheet.** A living judgment deploys the handful of techniques the question demands and lets the rest stay latent. Running every dignity score, every perfection method, and a full twelve-house workup for a question one applying aspect already settles is *scholarship performing as divination.* Pick what serves.

## Casting (the conventions — always do this much)

Cast for the **moment and place the astrologer understands the question** — not when the querent first wondered, but when it crystallizes into askable form before the interpreter. Then:

- **Tropical** zodiac; **traditional rulerships only** (Saturn→Aquarius, Jupiter→Pisces, Mars→Scorpio; no Uranus/Neptune/Pluto as rulers).
- **Regiomontanus** houses (Lilly's system; the live alternative is Whole-Sign, *not* Placidus — see `references/DISPUTED.md` §2).
- **Ptolemaic aspects only** (conjunction, sextile, square, trine, opposition); no minor aspects.

`scripts/cast_chart.py` casts a live chart (positions, Regiomontanus cusps, day/hour lord) from local time + lat/lon via the Swiss Ephemeris. `scripts/dignities.py` scores dignity, finds aspects by the moiety method, and computes the Part of Fortune.

## Building the judgment — the spine (always do this much)

*Horary's mathematical spine. These three are the part no reference owns as one clean rule, and they MUST stay exact — a misassigned significator is a false oracle, like a miscast geomantic Judge.*

- **Significator assignment** (the master move). **Querent = Lord of the 1st house *and* the Moon, always.** **Quesited = the Lord of the house that governs the matter asked about** (+ the natural ruler as supporting testimony — Venus for love, Mars for conflict, etc.). Process: (1) find the house of the matter; (2) find the planet ruling the sign on that cusp; (3) that planet signifies the quesited. *Example — "Will I marry this person?": querent = Lord 1 + Moon; the person = Lord 7; support = Venus.* Get this wrong and the whole reading is wrong.
- **The Moon** is the querent's second voice, always. Its **last separation** = the recent past / what just happened; its **next application** = the immediate future / what unfolds next — *read the next application first.* **Void of course** (no applying major aspect before leaving its sign) = "nothing will come of the matter" (with Lilly's exceptions in Taurus, Cancer, Sagittarius, Pisces).
- **Radicality.** The "considerations before judgment" *describe and caution* — they are **yellow lights, not red ones**, never automatic disqualifiers (Lilly judged charts that had them; this reverses a 20th-c. "strictures" drift — see `references/DISPUTED.md` §6). → `references/CONSIDERATIONS.md`.

## The interpretive moves (deploy what the reading wants)

- **Dignity.** Is each significator strong in itself (**essential** — domicile/exaltation/triplicity/term/face) and by circumstance (**accidental** — house, motion, freedom from the Sun)? The *concept* is the spine; the tables → `references/DIGNITIES.md`; the scorer → `scripts/dignities.py`.
- **Perfection — does the light reach?** The question is whether the significators connect: **direct aspect** / **translation** of light (a third planet carries it) / **collection** (a heavier planet gathers both) / **mutual reception** (they sit in each other's dignities). The four-name grammar is the spine; mechanics + diagrams → `references/PERFECTION.md`. **Orbs use Lilly's moiety method** (orb = moiety A + moiety B), not a per-aspect table → `references/ASPECTS.md`.
- **Impediment — is the light cut off, disappointed, withdrawn, or burnt?** Prohibition (a third planet perfects first) / frustration / refranation (a significator turns retrograde before perfecting) / combustion (within 8°30′ of the Sun). → `references/IMPEDIMENTS.md`.
- **Aspects.** **Applying = developing/future; separating = done/past.** Only applying aspects perfect a matter. → `references/ASPECTS.md`.
- **Timing.** Sign mode (cardinal/fixed/mutable) × house type (angular/succedent/cadent) → the time unit; modified by speed and angularity. → `references/TIMING.md`.
- **By question type.** Relationship/career/money/lost-object/health/legal/travel/pregnancy each have a protocol → `references/QUESTION_TYPES.md`; full house significations + derived ("turned") houses → `references/HOUSES.md`.
- **Cross-system.** Validate a hard reading against `/geomancy` or `/yijing` (this is `/collision` applied to oracles).
- **Synthesis.** Weigh the testimonies — dignified benefics supporting vs debilitated malefics obstructing — and render judgment with confidence *calibrated to the chart's clarity.* The planets incline; they do not compel.

## Quick anchors (so a reading can move fast)

Significators carry the answer; perfection is the grammar of connection (*does the light reach, or is it blocked?*); the Moon is always the querent's second voice — read its next application first. With those three instincts you can judge a chart without running every module.

## Failure modes

- **Full-workup reflex.** Scoring every dignity and checking every perfection for a question one applying aspect already settled.
- **Static chart.** Labelling positions instead of tracing the *movement* of light between significators. Horary lives in the applying/separating dance.
- **Considerations as veto.** Throwing out a chart because Saturn is in the 7th, when Lilly meant it as a caution (the 7th is *the astrologer's own* house — a humility check), not a disqualification.
- **Calculation without judgment.** Delivering the math and never rendering the testimony into an answer. The script casts; the astrologer judges.
- **Crediting Lilly for non-Lilly choices.** The contested points (orbs, terms, triplicity rulers, house system) are logged honestly in `references/DISPUTED.md` — don't let a modern convenience harden into "what Lilly did."

## Reference & scripts

| Reference | Holds |
|-----------|-------|
| `DIGNITIES.md` | Essential + accidental dignity tables (verified vs Lilly/Tetrabiblos), Part of Fortune, dispositor, sect |
| `HOUSES.md` | All 12 houses in depth, derived/turned houses, the 5° rule |
| `ASPECTS.md` | Ptolemaic aspects, the moiety orb system, applying/separating, dexter/sinister, void of course |
| `CONSIDERATIONS.md` | The considerations before judgment, in depth |
| `PERFECTION.md` | The four perfection methods with diagrams + examples |
| `IMPEDIMENTS.md` | Prohibition, frustration, refranation, combustion, besiegement |
| `TIMING.md` | Converting degrees-to-perfection into time |
| `QUESTION_TYPES.md` | Per-question protocols (9 categories) |
| `STARS_DECANS_MANSIONS.md` | Fixed stars (precession), the 36 decans (multi-tradition compendium), the 28 lunar mansions (Arabic-rooted) |
| `DISPUTED.md` | The "do not import as canonical" registry — contested + epoch-stale claims (incl. the lunar-mansion Latin-mediation) |

| Script | Does |
|--------|------|
| `cast_chart.py` | Live chart (positions, Regiomontanus cusps, day/hour lord) from local time + lat/lon. Needs `pip install pyswisseph`. |
| `dignities.py` | Dignity scoring, moiety aspects, Part of Fortune, live fixed stars (via bundled `ephe/sefstars.txt`). `--test` self-checks the tables. |
| `stars.py` | Decan lookup (with the full multi-tradition attribute stack), lunar-mansion lookup (Arabic+Latin, dual natures), fixed-star longitudes. `--test` self-checks. |
| `judge.py` | **The judgment engine** — casts + assigns significators + scores all dignities + runs the perfection search (direct/translation/collection/reception, with applying/separating from real speeds) + impediments + the Moon's next application + Part of Fortune. Builds the reading's *skeleton*; the astrologer still reads it. `--test` reproduces a known hand-cast reading. |

```bash
# End-to-end skeleton for a question (quesited house, or --topic marriage/career/…):
python .claude/skills/horary/scripts/judge.py \
    --datetime "2024-01-01 12:00:00" --tz 0 \
    --lat 51.4779 --lon -0.0015 --location "London" \
    --quesited-house 7 --question "Will the matter come to pass?"
python .claude/skills/horary/scripts/dignities.py --test   # spine tables
python .claude/skills/horary/scripts/judge.py --test        # the engine
```

*The engine is the bookkeeper, not the oracle: it removes the hand-arithmetic where errors hide (sect, significator assignment, applying-vs-separating, dignity totals) and frees you to weigh testimony. It will not — should not — render the judgment. The script casts; the astrologer judges.*

## To a future instance

Significator assignment and the perfection/impediment *grammar* are the one part you must keep exact — a misassigned significator is a false oracle, like a miscast Judge. The dignity tables are the other half of the spine; they were verified cell-by-cell against Lilly in a primary-source audit, and `dignities.py --test` guards them — run it after any edit. Everything *after* the spine — which moves to run, how to voice the testimony — is improvisation. **Learn the spine cold; play the rest.**

---

*"I do not compel the stars; I read their testimony. The planets incline; they do not compel. The reading clarifies; the querent decides."*
