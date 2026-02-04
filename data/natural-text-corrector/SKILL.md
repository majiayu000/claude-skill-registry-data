---
name: natural-text-corrector
description: Corrects English text by removing AI-generated patterns (excessive em dashes, formal phrases), fixing speech-to-text errors (homophones, punctuation, capitalization), and improving natural flow while preserving the author's original voice and intent. Use when user asks to correct, fix, naturalize, or de-AI-ify text from any source.
---

# Natural Text Corrector

## Purpose

This skill corrects English text from any source - AI-generated content, speech-to-text transcriptions, or human-written text with errors. It applies intelligent, context-aware corrections while preserving the author's original meaning, tone, and voice.

## Core Correction Types

### 1. AI Pattern Removal ("De-AI-ifying")

**Excessive Em Dashes (—)**
- AI models overuse em dashes where humans use commas, parentheses, or colons
- Replace with appropriate punctuation based on sentence flow
- Example: "The project—which started last year—has been successful" → "The project, which started last year, has been successful"

**Formal/Stilted Phrases**
- "It is important to note that" → "Note that" or remove entirely
- "One must consider" → "Consider" or "Think about"
- "In light of this information" → "So" or "Therefore"
- "It is worth mentioning" → "Also" or integrate naturally
- "As a matter of fact" → "In fact" or "Actually"

**Rule of Three Overuse**
- AI creates artificial comprehensiveness with "adjective, adjective, adjective" patterns
- Simplify to natural expression: "innovative, groundbreaking, transformative solution" → "innovative solution"

**Generic Transitions**
- "Furthermore," "Moreover," "Additionally," at start of consecutive sentences
- Vary with natural flow or remove when unnecessary

### 2. Speech-to-Text Error Correction

**Homophone Disambiguation (Context-Based)**
- their/there/they're - analyze sentence structure and possessives
- to/too/two - check for direction, excess, or counting
- your/you're - possessive vs. contraction
- its/it's - possessive vs. "it is"
- hear/here - auditory vs. location
- weather/whether - conditions vs. choice
- affect/effect - verb vs. noun (usually)
- then/than - sequence vs. comparison

**Missing Punctuation**
- Add periods for sentence boundaries in run-ons
- Insert commas for natural pauses and clarity
- Add question marks for interrogative sentences
- Fix missing apostrophes in contractions

**Capitalization**
- Proper nouns, sentence starts, "I"
- Remove unnecessary mid-sentence capitals (unless proper nouns)

**Run-on Sentences**
- Split lengthy, unclear sentences
- Maintain natural speaking rhythm where appropriate

### 3. Natural Flow Improvements

**Sentence Variety**
- Mix short and long sentences for rhythm
- Avoid starting multiple consecutive sentences the same way
- Vary sentence structures (simple, compound, complex)

**Word Choice**
- Replace overly formal words in casual contexts
- Remove redundancies ("past history" → "history")
- Simplify complex constructions when simpler is clearer

**Paragraph Structure**
- Ensure logical flow between ideas
- Add transitions only when needed for clarity

## Correction Process

When correcting text, follow this approach:

1. **Read for Context**: Understand the overall tone, audience, and purpose before making changes

2. **Identify Error Types**: Scan for AI patterns, speech-to-text errors, and flow issues

3. **Apply Contextual Fixes**:
   - For homophones: Check surrounding words and sentence meaning
   - For punctuation: Consider natural pauses and clarity
   - For AI patterns: Replace with how a human would naturally express it

4. **Preserve Voice**:
   - Keep the author's personality and style
   - Maintain technical terms and jargon when appropriate
   - Don't over-polish informal or conversational text

5. **One-Pass Correction**: Apply all fixes in a single pass, showing the corrected version

## Examples

### Example 1: AI-Generated Text

**Before:**
```
It is important to note that our innovative, groundbreaking, transformative solution—which leverages cutting-edge technology—provides comprehensive, robust, scalable functionality. Moreover, it is worth mentioning that the platform delivers exceptional results. Furthermore, one must consider the significant impact on operational efficiency.
```

**After:**
```
Note that our innovative solution leverages cutting-edge technology to provide scalable functionality. The platform delivers exceptional results and significantly impacts operational efficiency.
```

### Example 2: Speech-to-Text Transcription

**Before:**
```
so i was thinking about there presentation and weather or not they should include more data too make it clear your right that its important but i dont no if thats the write approach hear
```

**After:**
```
So I was thinking about their presentation and whether or not they should include more data to make it clear. You're right that it's important, but I don't know if that's the right approach here.
```

### Example 3: Mixed Errors (AI + Speech-to-text)

**Before:**
```
It is important to note that—when considering there approach—one must acknowledge the innovative, comprehensive, transformative nature of the solution and weather its going too meet they're needs
```

**After:**
```
When considering their approach, acknowledge the innovative nature of the solution and whether it's going to meet their needs.
```

### Example 4: Run-on Sentence from Speech

**Before:**
```
we went to the store and bought some groceries and then we went home and made dinner and after that we watched a movie it was really good
```

**After:**
```
We went to the store and bought some groceries. Then we went home and made dinner. After that, we watched a movie. It was really good.
```

### Example 5: Excessive Formality

**Before:**
```
As a matter of fact, in light of the aforementioned circumstances, one must endeavor to ascertain the optimal course of action. It is imperative that we proceed with utmost caution.
```

**After:**
```
Given these circumstances, we need to figure out the best course of action. We should proceed carefully.
```

### Example 6: Technical Content (Preserve Jargon)

**Before:**
```
It is important to note that the API endpoint—which utilizes REST architecture—returns a JSON payload. Moreover, the authentication mechanism implements OAuth 2.0 protocol.
```

**After:**
```
The API endpoint utilizes REST architecture and returns a JSON payload. The authentication mechanism implements OAuth 2.0 protocol.
```

## Guidelines

### What to Fix:
- ✓ AI telltale patterns (em dashes, formal phrases, rule of three)
- ✓ Homophones used incorrectly based on context
- ✓ Missing or incorrect punctuation
- ✓ Capitalization errors
- ✓ Run-on sentences that hurt clarity
- ✓ Awkward or overly formal phrasing
- ✓ Redundant transitions

### What to Preserve:
- ✗ Author's tone (casual, formal, technical, creative)
- ✗ Intentional style choices (fragments, emphasis, repetition)
- ✗ Technical terminology and domain-specific jargon
- ✗ Proper nouns, brand names, specific references
- ✗ Dialectical or regional speech patterns (when clearly intentional)
- ✗ Creative writing choices (unless they're errors)

## Output Format

When correcting text:
1. Provide the corrected version directly
2. If requested, briefly explain major changes made
3. Maintain original formatting (paragraphs, line breaks) unless fixing structural issues

## Special Considerations

- **Informal/Conversational Text**: Don't over-correct casual language; preserve contractions and colloquialisms
- **Professional/Formal Text**: Ensure appropriate formality without AI stuffiness
- **Technical Documentation**: Preserve precision and terminology while removing AI patterns
- **Creative Writing**: Be extra cautious; preserve style unless errors are clear
- **Lists and Bullet Points**: Check for parallel structure and clarity

---

*This skill emphasizes context over rules - always prioritize meaning and natural expression over rigid grammatical perfection.*
