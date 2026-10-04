---
name: feature-guide
description: "Helps non-technical Claude users instantly understand any Claude feature or capability.
  Given a feature name or a description of what the user wants to accomplish, generates a structured
  feature card: what it is, where it's available, how to activate it, limitations, current status,
  and an applicability verdict. Use when users ask about Claude capabilities, features, or how to
  accomplish specific tasks with Claude. Triggers: feature lookup, capability check, does Claude
  support, how to enable, what can Claude do, can Claude, Claude feature scout, what features does
  Claude have, how do I use this Claude feature."
version: 1.0.0
---

# Skill: feature-guide

Generates a structured feature card for any Claude capability — given a feature name or
a description of what the user wants to accomplish. Covers: what it is, where it's available,
how to use it, limitations, current status, and an applicability verdict.

---

## Triggers

**Russian:** «что умеет Claude», «есть ли у Claude», «умеет ли Claude», «поддерживает ли Claude», «как включить фичу», «расскажи о фиче», «scout», «какие возможности у Claude», «как использовать», «feature scout»
**English:** "what can Claude do", "does Claude have", "does Claude support", "how to enable", "Claude feature", "scout", "can Claude", "what features", "how to use", "feature scout", "Claude capabilities"

---

## Language Detection

Determine the language of the user's request:
- Request in Russian → respond entirely in Russian
- Request in English → respond entirely in English
- Mixed request → default to Russian

---

## Input

**Required:** a feature name OR a description of what the user wants to accomplish
(free text, 1–2 sentences is enough)

**Examples:**
- «Есть ли у Claude память?»
- «Хочу чтобы Claude помнил мой контекст»
- "What is the Projects feature?"
- «Умеет ли Claude создавать файлы?»
- "Does Claude support voice?"

## Output

One feature card per request, in structured format.

---

## Instructions

### Step 1 — Identify the request type

Classify the incoming request:

| Type | Signal | Action |
|------|--------|--------|
| Direct feature name | User names a specific feature: "Projects", "Memory", "Voice" | Proceed to Step 2 |
| Need description | User describes a goal: "I want Claude to remember things" | Identify the closest feature, ask one clarifying question |
| Ambiguous | Multiple features match | Offer up to 3 options, ask user to choose |
| Too general | "What can Claude do?" with no further context | Ask one question: "What specifically do you want to accomplish with Claude?" |
| AI comparison | Request mentions another AI product: ChatGPT, Gemini, Copilot, etc. | Decline: "This skill covers Claude's features only. Want to explore [feature from request]?" |

Do not ask more than one clarifying question. When context is minimal, act on the most probable interpretation.

### Step 2 — Search for current data

Run a web search to get the feature's current status. Priority sources:
1. `site:docs.anthropic.com [feature name]`
2. `site:support.anthropic.com [feature name]`
3. `Claude [feature name] 2025 OR 2026`

Goal: current status (available / beta / Pro+ only / announced / not released), platforms, and activation steps.

If web search is unavailable — continue based on training data and mark the card:
"Based on training data — status may be outdated."

### Step 3 — Fill in card parameters

Determine each parameter from search results:

| Parameter | How to determine |
|-----------|-----------------|
| Name | Official name from Anthropic documentation |
| Description | 1–2 sentences: what it does, why it matters to the user |
| Platforms | Claude.ai / Projects / Claude Code / API / Cowork / mobile app |
| Plans | Free / Pro / Team / Enterprise / all plans |
| How to activate | Specific steps or trigger phrase |
| Limitations | What the feature does NOT do, technical limits |
| Status | Available / Beta / Pro+ only / Announced / Not released |
| Verdict | Applicability to the user's specific goal |

If a parameter is unknown — write "No data". Do not fabricate information.

### Step 4 — Generate the feature card

Output the card strictly in the following format:

---
## [Feature name]

**What it is:** [1–2 sentences]

**Where available:** [platforms] — [plans]

**How to use:** [specific steps or trigger phrase]

**Limitations:**
- [limitation 1]
- [limitation 2]

**Status:** [Available / Beta / Pro+ only / Announced / Not released]

**Verdict:** [Fits / Partially fits / Does not fit] — [1 sentence with reasoning]

---

After the card, add one line: "Explore related features: [name 1], [name 2]?" —
only if related features are clearly relevant to the request.

### Step 5 — Handle edge cases

| Situation | Action |
|-----------|--------|
| Feature does not exist | Do not generate a card. Output: "Feature [name] not found in Claude documentation. Related features: [name 1], [name 2] — explore?" |
| Feature announced but not released | Status: "Announced", include date if known |
| Feature is Claude Code only, non-technical audience | Add to Limitations: "Requires technical setup" |
| Different versions across platforms | Note differences under "Where available" |
| Request covers multiple features at once | Generate card for the first feature, offer to continue with the rest |

---

## Constraints

- Does not compare Claude to other AI products (ChatGPT, Gemini, etc.)
- Does not provide pricing details — only plan names for availability
- Does not configure or enable features on the user's behalf
- Does not fabricate parameters — writes "No data" when information is unavailable
- Generates one feature card per request
- Web search is required for accurate, current status
