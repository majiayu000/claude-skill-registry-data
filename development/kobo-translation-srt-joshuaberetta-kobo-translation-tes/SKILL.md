---
name: kobo-translation-srt
description: "Extension to kobo-translation skill specifically for translating video subtitles and transcripts in SRT format. Adds subtitle-specific guidelines for character limits, spoken language patterns, chunked translation context management, and maintaining readability on screen. Use this skill when translating SRT subtitle files for KoboToolbox tutorials, webinars, or educational videos."
---

# KoboToolbox SRT Subtitle Translation

## Overview

This skill extends the **kobo-translation** skill with specialized guidelines for translating video subtitles in SRT format. All base translation rules still apply, but with additional considerations for on-screen readability, spoken language patterns, and subtitle timing constraints.

**🔴 CRITICAL: This skill is for SUBTITLE TRANSLATION ONLY**

When translating SRT files:
- The source is **spoken language** from video
- Translation must be **concise and readable on screen**
- All **brand terminology rules still apply**
- Translation is done in **chunks** to preserve context while avoiding hallucinations

## Subtitle Translation Principles

### 1. **Inherit All Base Rules**

✅ **ALL rules from the main kobo-translation skill apply**, including:
- Brand terminology (servers, Question Library, Formbuilder, etc.)
- UI terminology and capitalization
- Gender-inclusive language
- Formality levels (vous/tu, usted/tú)
- Technical term handling

**Before translating subtitles:**
1. Read **brand-terminology.md** - Server names, Question Library, etc.
2. Read **ui-terminology.md** - Button names, capitalization
3. Apply all base translation principles

### 2. **Subtitle-Specific Adaptations**

While maintaining base rules, adapt for subtitle constraints:

**Character Limits:**
- **Ideal**: 35-42 characters per line
- **Maximum**: 50 characters per line
- **Lines per subtitle**: Maximum 2 lines

**Conciseness:**
- Spoken language is naturally more verbose than written
- **Compress without losing meaning**
- Remove unnecessary filler words ("um", "you know", "like")
- Combine ideas when possible

**Readability:**
- Break long sentences at natural pauses
- Prioritize comprehension over literal translation
- Match subtitle timing to speech rhythm

### 3. **Technical Terms in Subtitles**

**CRITICAL RULE: XLSForm terms in subtitles are ENGLISH ONLY**

Unlike written documentation, subtitles have character limits and timing constraints.

| Context | Rule | Example |
|---------|------|---------|
| **Documentation** | English + translation on first use | "list_name (nom de la liste)" |
| **Subtitles** | English only | "list_name" |

**Why?** 
- Adding translations doubles character count
- Subtitles must sync with what's shown on screen
- Viewers see the English term in the interface

**Brand terms still follow base rules:**
- ✅ "Servidor Global" (not "de KoboToolbox")
- ✅ "La bibliothèque de questions" (capital L)
- ✅ "Formbuilder" can be translated in speech context

### 4. **Context-Aware Chunked Translation**

SRT files are translated in **chunks** (typically 20-30 subtitles at a time) to:
- Maintain overall context and narrative flow
- Avoid hallucinations from large context windows
- Preserve terminology consistency

**Each chunk includes:**
- **Previous context**: Last 3 subtitles from previous chunk (for continuity)
- **Current subtitles**: 20-30 subtitles to translate
- **Next context**: First 3 subtitles from next chunk (for flow)

**Translation approach:**
- Consider the previous context for continuity
- Translate current subtitles maintaining natural flow
- Be aware of upcoming context to maintain coherence
- Ensure technical terms remain consistent across chunks

## Subtitle Translation Guidelines

### Character Limit Strategies

**When translation is too long:**

1. **Compress naturally:**
   ```
   ❌ "You're going to need to click on the NEW button"
   ✅ "Click on NEW"
   ```

2. **Use shorter synonyms:**
   ```
   ❌ "Vous allez devoir cliquer sur le bouton NOUVEAU"
   ✅ "Cliquez sur NOUVEAU"
   ```

3. **Split across subtitles if needed:**
   ```
   Subtitle 1: "Para crear un nuevo formulario,"
   Subtitle 2: "haz clic en NUEVO"
   ```

4. **Never sacrifice accuracy:**
   - Keep brand terms exact
   - Keep UI element names exact
   - If you must choose: accuracy > brevity

### Spoken Language Patterns

**Adapt written conventions for speech:**

| Written | Spoken/Subtitle |
|---------|-----------------|
| "First, navigate to the Form page" | "Go to the FORM page" |
| "Subsequently, you will observe" | "Next, you'll see" |
| "It is necessary to configure" | "You need to configure" |

**Spanish - Informal tone matches speech:**
- ✅ "Ahora vas a ver" (Now you'll see)
- ✅ "Haz clic aquí" (Click here)
- ✅ "Fíjate en esto" (Notice this)

**French - Formal but conversational:**
- ✅ "Vous allez voir" (You'll see)
- ✅ "Cliquez ici" (Click here)
- ✅ "Remarquez ceci" (Notice this)

### Timing Awareness

**Consider subtitle duration:**

- Short subtitles (<2 seconds): Must be very concise
- Medium subtitles (2-4 seconds): Standard translation
- Long subtitles (>4 seconds): Can be more complete

**Reading speed:**
- Average: 15-20 characters per second
- Adjust translation length to subtitle duration
- Never exceed what can be read in the time shown

### Natural Speech Flow

**Maintain conversational feel:**

```
✅ GOOD (natural):
"Let's create a new form.
Click on NEW at the top."

❌ BAD (too formal):
"We shall proceed to create a new form.
Navigate to the NEW button located at the top of the interface."
```

**Contractions are acceptable in subtitles:**
- EN: "you'll", "it's", "we're"
- ES: Already naturally contracted
- FR: "c'est", "vous allez" → "vous aurez" (when natural)

### Cross-Chunk Consistency

**When translating chunks:**

1. **Terminology consistency:**
   - If chunk 1 uses "formulario" don't switch to "forma" in chunk 2
   - Track how you translate recurring terms

2. **Narrative flow:**
   - Check previous context before translating
   - Ensure smooth transition from previous chunk
   - Maintain speaker's tone and style

3. **Technical accuracy:**
   - Brand terms must be consistent across all chunks
   - UI elements must match exactly across entire subtitle file

## Common Subtitle Translation Patterns

### Tutorial/Educational Content

**Pattern: Instruction → Action → Result**

```
English subtitles:
[1] "Now we'll add a new question to our form."
[2] "Click on the plus icon here."
[3] "And you'll see the question types appear."

Spanish subtitles:
[1] "Ahora agregaremos una nueva pregunta."
[2] "Haz clic en el ícono de más aquí."
[3] "Y verás aparecer los tipos de pregunta."

French subtitles:
[1] "Nous allons ajouter une nouvelle question."
[2] "Cliquez sur l'icône plus ici."
[3] "Vous verrez apparaître les types de question."
```

**Key observations:**
- Compressed but complete
- Maintains instructional flow
- UI element names preserved
- Natural spoken language

### Demonstrative Content

**Pattern: Showing → Explaining**

```
English:
[10] "Here in the Question Library,"
[11] "you can see all the template questions"
[12] "that are available for your project."

Spanish:
[10] "Aquí en La biblioteca de preguntas,"
[11] "puedes ver todas las preguntas plantilla"
[12] "disponibles para tu proyecto."

French:
[10] "Ici dans La bibliothèque de questions,"
[11] "vous pouvez voir toutes les questions types"
[12] "disponibles pour votre projet."
```

**Key observations:**
- "Question Library" → "La biblioteca de preguntas" / "La bibliothèque de questions" (capital L!)
- Conversational but informative
- Pronouns match base skill rules (tú/vous)

### Technical Walkthrough

**Pattern: Technical term → Usage**

```
English:
[25] "In the list_name column,"
[26] "enter the name of your list."
[27] "This connects your cascading select."

Spanish:
[25] "En la columna list_name,"
[26] "escribe el nombre de tu lista."
[27] "Esto conecta tu cascading select."

French:
[25] "Dans la colonne list_name,"
[26] "saisissez le nom de votre liste."
[27] "Cela connecte votre cascading select."
```

**Key observations:**
- XLSForm terms stay in English: "list_name", "cascading select"
- No parenthetical translations (unlike documentation)
- Character limits respected
- Natural flow maintained

## Subtitle Quality Checklist

Before finalizing subtitle translation:

**🚨 Brand & Terminology (inherited from base skill):**
- [ ] All server names use EXACT translations with correct articles
- [ ] "Question Library" has capital L in target language
- [ ] Formbuilder translated appropriately for context
- [ ] UI elements match official translations exactly
- [ ] XLSForm technical terms kept in English (no translations)

**📏 Subtitle-Specific:**
- [ ] All subtitles under 50 characters per line (35-42 ideal)
- [ ] Maximum 2 lines per subtitle
- [ ] Natural spoken language (not overly formal)
- [ ] Maintains conversational flow
- [ ] Reads naturally at normal speed
- [ ] Compressed appropriately without losing meaning

**🔄 Context & Consistency:**
- [ ] Terminology consistent across all chunks
- [ ] Natural transitions between chunks
- [ ] Speaker's tone maintained throughout
- [ ] No terminology drift in longer videos

**🎯 Language-Specific:**
- [ ] **Spanish**: Informal tú throughout, gender-inclusive
- [ ] **French**: Formal vous throughout, gender markers
- [ ] Formality matches base skill rules

**⏱️ Timing (if reviewing with video):**
- [ ] Subtitles match speech timing
- [ ] Readable in time shown on screen
- [ ] Natural reading pace maintained

## Subtitle vs Documentation: Key Differences

| Aspect | Documentation | Subtitles |
|--------|--------------|-----------|
| **XLSForm terms** | English + translation first use | English only |
| **Length** | Can be verbose | Must be concise |
| **Style** | Formal written language | Natural spoken language |
| **Formatting** | Full markdown, HTML | Plain text only |
| **Context** | Self-contained sections | Sequential narrative |
| **Character limits** | No limits | 35-42 chars ideal, 50 max |
| **Processing** | Full document or diff | Chunked with context |

## Error Examples for Subtitles

### Example 1: Too Long

**❌ WRONG (57 characters, too formal):**
```
[5] "Vous devez maintenant naviguer vers la section des formulaires"
```

**✅ CORRECT (28 characters, natural):**
```
[5] "Allez à la section FORMULAIRES"
```

### Example 2: Technical Terms

**❌ WRONG (added translation, too long):**
```
[12] "Dans list_name (nom de la liste)"
```

**✅ CORRECT (English only, fits):**
```
[12] "Dans la colonne list_name"
```

### Example 3: Brand Term Error

**❌ WRONG (missing article):**
```
[8] "Ouvrez bibliothèque de questions"
```

**✅ CORRECT (capital L article):**
```
[8] "Ouvrez La bibliothèque de questions"
```

### Example 4: Overly Literal

**❌ WRONG (too literal, awkward):**
```
[15] "Procederemos a hacer clic en el botón"
```

**✅ CORRECT (natural spoken language):**
```
[15] "Haremos clic en el botón"
```
**OR EVEN BETTER:**
```
[15] "Haz clic en el botón"
```

## Chunked Translation Best Practices

### Managing Context Windows

**When translating a chunk:**

1. **Read previous context** (last 3 subtitles)
   - Note any terminology used
   - Understand narrative position
   - Check speaker's tone

2. **Translate current chunk** (20-30 subtitles)
   - Maintain consistency with previous
   - Keep natural flow
   - Apply all base rules

3. **Check next context** (first 3 subtitles)
   - Ensure your translation leads naturally into next section
   - Verify no awkward transitions

### Handling Repeated Terms

**If a term appears across chunks:**

- First mention in video → Follow first reference rules if applicable
- Subsequent mentions → Use shortened form consistently
- Track your translations → Don't vary terminology

**Example across chunks:**

```
Chunk 1:
[5] "This is the KoboToolbox Formbuilder"
[5] "C'est l'interface de création de formulaires KoboToolbox"

Chunk 3:
[45] "Back in the Formbuilder..."
[45] "De retour dans l'interface de création..."
```

### Maintaining Voice

**Keep the instructor's voice consistent:**

- If they're casual and friendly → Keep that tone
- If they're more formal → Maintain formality
- If they use analogies → Translate analogies naturally
- If they emphasize certain words → Maintain emphasis

## Notes

**Reference documents:**
All base translation reference documents apply:
- brand-terminology.md
- ui-terminology.md  
- form-building-terms.md
- question-types.md
- data-collection-terms.md

**Additional considerations:**
- Subtitle translation may need to prioritize on-screen readability over perfect literal translation
- When in doubt, test by reading subtitle aloud at normal speed
- Character limits are HARD limits for readability

**Working document:**
This skill is an extension of the base kobo-translation skill. All base rules apply unless explicitly overridden here for subtitle-specific needs.
