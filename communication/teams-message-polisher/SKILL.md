---
name: teams-message-polisher
description: "Reformule et polit les messages Microsoft Teams (ton simple, clair, convivial), en français ou en anglais. Traduction vers l'anglais via « English » ou « EN: ». Sortie directe sans préambule. Pour rédiger un message Teams, clarifier sa communication d'équipe ou traduire vers l'anglais."
---

# Teams Message Polisher

## Overview

Transforms rough messages into polished, professional yet friendly Microsoft Teams messages: clear, actionable, collaborative, human.

## Core Directive: Direct Output Only

**CRITICAL**: never include preamble, explanation or commentary. Output ONLY the polished message, ready to paste.

NEVER:
```
Voici votre message Teams reformulé :

[polished message]

J'ai simplifié le ton pour Teams.
```

ALWAYS:
```
[polished message]
```

## The Teams Tone

DO: simple and clear (short sentences), friendly and collaborative, action-oriented (next steps and ownership), emoji-light (👍 ✅ 📅 occasionally), scannable, conversational.

DON'T: overly formal corporate speak ("per my previous correspondence"), too casual (excessive emojis, slang, all lowercase), verbose emails disguised as chats, passive-aggressive undertones, unnecessary apologies ("sorry to bother you"), walls of text.

## Workflow

### Step 1: Language detection and translation

- Detect French or English and answer in the same language.
- If the input contains "English" or "EN:" anywhere ("EN: [message]", "[message] English", "Translate to English: [message]"), translate the whole message to English and apply the Teams polish in English.

### Step 2: Content analysis

Identify the type (quick update, question/request, response, announcement, coordination, feedback) and the intent: make the action explicit, flag urgency clearly but professionally, state FYI upfront, end a question with a clear ask.

### Step 3: Teams optimization rules

- Structure: context or intent (1 sentence max), main point or request (2-4 sentences), clear next step, line breaks instead of giant paragraphs.
- Tone: remove excessive politeness, add warmth without over-casualizing ("Thanks!" not "Thx bro"), prefer active voice, simplify jargon, stay human and direct.
- Length: 1-4 sentences for quick messages, 6-8 maximum for complex updates. If longer, suggest several messages or a doc link.
- Clarity: urgent action items first, bold for key points (sparingly), number steps when there are several actions, include context without over-explaining.
- Emoji: OK for acknowledgment (👍), done (✅), meeting (📅), celebration (🎉). Default to none unless the original had them or the context calls for it.

### Step 4: Polish and output

Perfect grammar and spelling, complete message (no hanging thought), clear call to action, professional yet approachable. Output the message text only: no quotation marks or added formatting, preserve intentional formatting, ready to paste into Teams.

## Examples and patterns

Eight input/output examples (quick update, request with translation, action request, meeting coordination, status, polite decline, feedback request, urgent issue), French and English guidelines (tu/vous, greetings, sign-offs), the four Teams context patterns (status, request, meeting follow-up, problem alert) and the edge cases (@mentions, technical terms, already well-written, slang, emoji, long messages) are in `references/examples-and-edge-cases.md`. Read it when the message type or edge case is not obvious.

## Optimization Priorities

Ranked by importance for Teams:

1. **Clarity** - Message must be instantly understood
2. **Action** - Next steps must be obvious
3. **Brevity** - Shorter is better (but complete)
4. **Tone** - Friendly and professional balance
5. **Format** - Scannable and well-structured

## Special Instructions

### When "English" or "EN:" appears:
1. Translate entire message to English
2. Apply all Teams polish rules in English
3. Output in English regardless of input language
4. Maintain professional-casual English Teams tone

### When message is technical/code-related:
- Preserve all code snippets exactly
- Keep technical terminology
- Format code blocks if multi-line
- Maintain technical accuracy over simplification

### When message contains numbers/dates/data:
- Preserve all numbers exactly
- Clarify ambiguous dates if possible
- Keep data formatting consistent

## Critical Reminders

1. **NEVER include preamble** - Output message directly
2. **NEVER add meta-commentary** - No "Here's your polished message"
3. **NEVER over-formalize** - Teams is collaborative, not corporate email
4. **ALWAYS maintain user intent** - Polish, don't transform
5. **ALWAYS respect "English/EN:" trigger** - Translate when specified
6. **ALWAYS keep it actionable** - Clear next steps
7. **ALWAYS balance professional + friendly** - The Teams sweet spot
