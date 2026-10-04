---
name: vedic-astrology
clawhub-slug: vedic-astrology
clawhub-owner: eamanc-lab
homepage: https://github.com/eamanc-lab/fortune-telling-skills
description: |
  A Vedic astrology (Jyotish) analyzer based on the Indian Jyotish tradition, using the Sidereal
  zodiac to read birth charts. Covers 27 Nakshatras (Lunar Mansions), the Vimshottari Dasha
  (Major Period) system, and the Navagraha (Nine Planets). Triggered when users mention
  "Vedic astrology," "Jyotish," "Vedic," "Nakshatra," "Dasha," or "Indian astrology."
  Pure LLM reasoning for interpretation (precise charts require an astronomical engine).
  No external API required.
  Not applicable for: Western astrology horoscopes, BaZi, tarot, Zi Wei Dou Shu, or other
  domains → use the fortune-hub router instead.
license: MIT
compatibility:
  platforms:
    - claude-code
    - claude-ai
    - api
metadata:
  author: eamanc
  version: "1.0.0"
  tags: ["vedic", "jyotish", "astrology", "吠陀", "月宿", "fortune-telling"]
---

# Vedic Astrology Analyzer

Grounded in the Indian Jyotish tradition, this Skill reads the sidereal birth chart to reveal your Moon Nakshatra (Lunar Mansion), Dasha (planetary period) trajectory, and the energy patterns of the Navagraha (Nine Planets).

> **Important Note**: This Skill provides Vedic astrology knowledge-based interpretation and framework analysis from the information you provide. Degree-level chart precision (exact Ascendant degree, exact planetary positions) is best verified using a dedicated astronomical engine such as Kerykeion or Astropy. The chart estimates in this Skill are based on average planetary velocities — suitable for Nakshatra determination and Dasha calculation, with a possible margin of error of ±1 day near sign boundaries.

## Quick Start

```
"Give me a Vedic astrology reading — I was born June 15, 1990, in Beijing, at 8 AM"
"Which Nakshatra is my Moon in?"
"Which Mahadasha am I currently running?"
"Interpret the Navagraha planetary influences in my chart"
"What does Vedic astrology say about my year ahead?"
```

**Full example**:

Input: `I was born March 22, 1988, in Shanghai, at 2 PM. Please do a Vedic astrology reading.`

Output:
> # ✨ Vedic Astrology Report
>
> ## Foundation Chart (Sidereal Zodiac · Lahiri Ayanamsa)
>
> **Moon Nakshatra: Bharani (Lunar Mansion 2)**
> Moon is approximately at Taurus 13°, falling in Bharani (13°20'–26°40' Taurus sidereal)
> Ruling Planet: Venus
> Your emotional instincts lean toward carrying and transforming — there's a deep sense of responsibility within you...
>
> ## Vimshottari Dasha (Planetary Periods)
> Current Mahadasha: Saturn — 2021 to 2040
> Saturn Mahadasha theme: discipline, boundaries, and the long harvest of patient work...
>
> ## Navagraha Planetary Picture
> [Planetary sign placements and energy interpretations]

## User Context

This Skill requires the user's birth date, birth time, and birthplace to analyze the chart.

**Reading**: Before running, check in this order:
1. This directory's `MEMORY.md` — use first
2. `fortune-hub/MEMORY.md` in the same repo (if it exists) — fill in any missing base profile fields

If data is available, use it directly without asking again.

**Writing**: After collecting user info, write it to **this directory's** `MEMORY.md`:

```markdown
# User Info

## Basic Profile
- Date of birth: YYYY-MM-DD
- Birth time: HH:MM (24-hour)
- Birthplace: City name
- Birth time zone: UTC+X

## Chart Cache
- Sun sign (sidereal): Sign, approx. °
- Moon sign (sidereal): Sign, approx. °
- Moon Nakshatra: Name (Nakshatra #N)
- Nakshatra ruling planet: Planet
- Birth Dasha planet: Planet
- Current Mahadasha: Planet (YYYY–YYYY)
```

| Field | Required | How to ask |
|-------|---------|------------|
| Date of birth | ✅ | "Please share your birth date (year, month, day)" |
| Birth time | ✅ Needed for Ascendant and precise planetary positions | "What time were you born? (If unsure, a rough time of day is fine — it affects the Ascendant calculation)" |
| Birthplace | ✅ Needed for time zone and geographic latitude | "What city or region were you born in?" |

**Updating**: Update `MEMORY.md` when the user requests changes.

## Workflow

### Step 1: Parse User Intent

Identify from the user's input:

| Parameter | Parsing rule | Default |
|-----------|-------------|---------|
| **Analysis type** | Full reading / single query (Nakshatra / Dasha / planets / yearly outlook) | Full reading |
| **Birth date** | Provided directly or read from MEMORY.md | Required |
| **Birth time** | Provided directly or read from MEMORY.md | Required; note impact on precision if missing |
| **Birthplace** | Provided directly or read from MEMORY.md | Required for time zone conversion |

If birth time is unknown, inform the user: "Without a birth time, I can't determine your Ascendant (Lagna), but your Moon Nakshatra and Mahadasha can still be estimated."

### Step 2: Estimate Chart Positions

Load the calculation rules from [references/calculation-rules.md](references/calculation-rules.md).

**Chart estimation sequence**:

1. **Convert to UTC**: Apply birth location time zone → UTC birth moment
2. **Calculate tropical Sun longitude** (using J2000.0 average velocity)
3. **Subtract Ayanamsa** (Lahiri system, currently ~24°) → sidereal longitude
4. **Determine sign placements** for Sun, Moon, and other planets (sidereal zodiac)
5. **Identify Moon Nakshatra** (sidereal Moon longitude ÷ 13°20' = Nakshatra index)
6. **Calculate Vimshottari Dasha**: Use the Moon's position within its Nakshatra to find the fraction elapsed, determine the birth Dasha planet and remaining years, then project forward to the present

> Calculation note: The above is an approximation. For verified results, use an astronomical engine.

### Step 3: Load Interpretation Knowledge

Load the relevant reference material as needed:
- Nakshatra characteristics → [references/interpretation-guide.md](references/interpretation-guide.md)
- Planetary meanings → [references/interpretation-guide.md](references/interpretation-guide.md)
- Dasha interpretation → [references/interpretation-guide.md](references/interpretation-guide.md)

### Step 4: Generate the Reading Report

#### Output Format (Full Reading)

```markdown
# ✨ {Name's / Your} Vedic Astrology Report

> Born: {Month D, YYYY HH:MM} · {Birthplace} | System: Jyotish · Lahiri Ayanamsa

---

## I. Moon Nakshatra Analysis

### Nakshatra: {Nakshatra name} (Lunar Mansion #{N})
📍 Moon is approximately at {Sign} {degree}°, falling in {Nakshatra} ({longitude range})

**Ruling Planet**: {Planet}
**Core Keywords**: {3–5 keywords}

[3–4 sentences of deep interpretation: how this Nakshatra shapes emotional instincts, intuitive patterns, and inner drives]

**Nakshatra Pada (Quarter)**: Moon falls in Pada {N}, {element} element, {keywords}

---

## II. Vimshottari Dasha (Planetary Periods)

### Current Mahadasha: {Planet} ({start year}–{end year})

⏱ Approximately {X} years and {X} months remaining in this Mahadasha

**{Planet} Mahadasha Theme**: [3–4 sentences on the overarching life themes and focus areas during this planetary period]

#### Current Antardasha (Sub-Period)
Currently in {major planet} / {sub-planet} Antardasha (approx. {start} – {end})
[2–3 sentences on how the sub-period overlays and interacts with the main period]

#### Mahadasha Timeline
| Mahadasha Planet | Start Year | End Year | Duration |
|-----------------|-----------|---------|----------|
| [List the next 3–4 Mahadashas] |

---

## III. Navagraha Planetary Picture

> The following sign placements are approximations based on birth date. For precise degree positions, verify with a professional tool.

| Planet | Sidereal Sign (approx.) | Keywords |
|--------|------------------------|---------|
| ☀️ Sun (Surya) | {Sign} | {keywords} |
| 🌙 Moon (Chandra) | {Sign} | {keywords} |
| ♂ Mars (Mangala) | {Sign} | {keywords} |
| ☿ Mercury (Budha) | {Sign} | {keywords} |
| ♃ Jupiter (Guru) | {Sign} | {keywords} |
| ♀ Venus (Shukra) | {Sign} | {keywords} |
| ♄ Saturn (Shani) | {Sign} | {keywords} |
| ☊ Rahu (North Node) | {Sign} | {keywords} |
| ☋ Ketu (South Node) | {Sign} | {keywords} |

### Planetary Spotlight

[Select 2–3 planets that stand out in the chart (e.g., strong, debilitated, conjunct) for deeper interpretation — 2–3 sentences each]

---

## IV. Integrated Insights for This Season of Life

[Weave together the Nakshatra, Mahadasha, and planetary picture to offer 3–4 specific, actionable insights centered on the core growth themes of the current Dasha]

---

*Vedic astrology (Jyotish) readings are for personal exploration and reflection. Chart positions are estimated — for precise calculations, use tools like Kerykeion.*
```

#### Output Format (Single Query)

Output only the module the user asked about (Nakshatra / Dasha / planets / yearly outlook), including the estimation process and interpretation. Do not generate a full report.

### Step 5: Save Results

After the first complete reading, cache the chart estimates to `MEMORY.md`. Subsequent single-module queries can draw from the cache directly.

## Generation Rules

**Estimation transparency**:
- Label each planetary position with "approximately" to remind the user it's an estimate
- State the basis for the estimate (average velocity + Ayanamsa correction)
- Near sign boundaries (e.g., Moon changes signs roughly every 2.5 days), proactively flag the possibility of error

**Expression style**:

Use an **exploratory-inspirational** tone — blending specialist knowledge with spiritual warmth:

- Present the estimation process to demonstrate depth ("Moon is approximately at sidereal Taurus 15°, placing it in Rohini Nakshatra")
- Explain Vedic terminology in everyday language ("Rohini's ruling planet is the Moon itself, symbolizing nourishment and abundance")
- Connect all three layers — Nakshatra, Dasha, and planetary picture — in a unified reading
- Frame challenging placements constructively ("Saturn Mahadasha calls for discipline, but it's also the golden period for building something that truly lasts")

**Prohibited expressions**:

| Do not use | Replace with |
|-----------|-------------|
| ❌ "You are destined to..." | ✅ "Your chart shows a tendency toward..." |
| ❌ "This is a malefic planet / you have a bad chart" | ✅ "This planet brings challenges, and with them, an invitation to deepen" |
| ❌ "You will never be able to..." | ✅ "This configuration calls for more patience and awareness" |
| ❌ "You must perform a ritual to fix this" | ✅ "Understanding these energies can help you respond with greater consciousness" |

Absolutely prohibited: predictions of death or illness, fatalistic pronouncements, fear-based language, and promotion of rituals / mantras / remedial services.

## Error Handling

| Scenario | Response |
|----------|---------|
| Birth date not provided | "Please share your birth date (year, month, day) so I can begin your Vedic chart reading" |
| Birth time not provided | "Without a birth time, I'll skip the Ascendant (Lagna) analysis — Moon Nakshatra and Dasha can still be estimated. Do you have a rough sense of when you were born? (e.g., early morning, midday, afternoon, evening)" |
| Birthplace not provided | "Please share your birth city so I can convert to the correct UTC time" |
| Sign boundary uncertainty | "The Moon is near a sign boundary on this date — it may be in {A} or {B}. I'd recommend verifying with a precision tool. I'll proceed with {A} for this reading." |
| User asks about Western horoscope | "For Western zodiac horoscopes, horoscope-daily is the right Skill. Note that Vedic astrology uses the sidereal zodiac, so your Sun sign may differ from the Western system by about 24° — roughly one sign." |
| User asks about BaZi / tarot | "I'd suggest using fortune-hub to select the right Skill for that" |
| User questions the science | "Vedic astrology is an ancient symbolic framework — it offers a lens for self-reflection rather than scientific prediction. Think of it as a map for knowing yourself more deeply." |

## When Not to Use This Skill

Do **not** invoke this Skill for:
- **Western horoscope / zodiac readings** → horoscope-daily
- **BaZi / Zi Wei Dou Shu / Tarot / Feng Shui** → use fortune-hub to select the right Skill
- **Precise astronomical calculations** → requires an astronomical engine (Kerykeion / Astropy); this Skill provides knowledge-based interpretation
- **Psychological counseling / medical advice** → this Skill is for self-exploration only and does not replace professional services

## Language & Localization

Always detect and respond in the user's language. Preserve Sanskrit terminology (Nakshatra, Dasha, Rashi, etc.) in both languages.

**English:**
- Professional yet approachable Jyotish counselor tone
- Always pair Sanskrit terms with brief English explanation on first use: "your Nakshatra (lunar mansion) is Rohini"
- Emphasize the Vedic concept of karma as growth opportunity, not punishment
- Frame Dasha periods as life chapters: "You're currently in your Saturn Mahadasha — a period that rewards discipline and long-term vision"

**中文:**
- 专业但亲和的吠陀占星顾问语气
- 梵文术语首次出现时附中文解释："你的 Nakshatra（月宿）是 Rohini（角宿）"
- 强调业力（karma）是成长机会而非惩罚
- 大运（Dasha）描述为人生篇章："你目前正处于土星大运期，这是一个奖励纪律和长远眼光的阶段"
- 禁用："命中注定""前世业障""无法改变"

## Atomic Design

This Skill covers one atomic capability: **Vedic astrology (Jyotish) analysis**. It does not include Western horoscopes, BaZi, Zi Wei Dou Shu, I Ching, tarot, or any other divination systems. For other domains, combine with the corresponding Skill in this repo or route through fortune-hub.

## Disclaimer

Chart positions provided by this Skill are approximate estimates based on average planetary velocities and are not guaranteed to be degree-level accurate. Vedic astrology readings are intended for entertainment and personal exploration only and do not constitute medical, legal, financial, or any other professional advice. For major life decisions, rely on rational judgment and professional consultation.
