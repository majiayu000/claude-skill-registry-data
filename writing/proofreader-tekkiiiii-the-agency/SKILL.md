---
name: proofreader
version: 2.0.0
description: "Proofread any text in English or Vietnamese (or mixed) - check for typos, grammar errors, tone mark errors, clarity issues, and logical flow problems, while understanding the content's context, tone, and intended audience. Calibrates standards to document type so a CV bullet's deliberate parallelism is preserved while a blog post is checked for flow. Use whenever the user shares writing and asks to proofread, check, review writing, fix errors, or pastes a block of text expecting feedback. Even if the user only asks about one aspect, always run the full context-aware review."
---

# Proofreader Skill

A context-aware proofreading skill that reads content, understands its purpose and audience, checks for errors, and delivers structured, actionable feedback **without flattening intentional format conventions**.

---

## Workflow

### Step 1 - Understand the Content (REQUIRED)

Before flagging anything, read the full selection and identify:

- **Content type** - email, social post, report, article, marketing copy, press release, **CV bullet**, **cover letter**, chat message, technical doc, etc.
- **Tone register** - formal / semi-formal / casual / professional / creative
- **Intended audience** - general public, colleagues, management, customers, recruiters, media, etc.
- **Language** - English? Vietnamese? Mixed? (adapt all feedback to match)
- **Purpose** - inform, persuade, instruct, entertain, announce, request, etc.
- **Was this just humanized?** - If the user mentions running the humanizer skill first, OR if the text has the telltale signs of having been humanized (recent edits, em-dash-removed structure, parallel CV bullets), apply the **post-humanizer mode** in Step 2.

Use this context to calibrate what "good" looks like for this specific piece - a casual Zalo message and a bank press release have very different standards, and **a CV bullet has different standards from a blog paragraph**.

---

### Step 2 - Run the Format-Calibrated Review

Apply different bars to different formats. **Do not flag intentional format conventions as errors.**

#### Format-Specific Calibration

**CV / Resume bullets:**
- Parallel grammatical structure across bullets is REQUIRED, not a problem
- Sentence fragments starting with action verbs ("Led X...", "Managed Y...") are correct CV grammar
- Bullets of 12-35 words are normal - DO NOT flag long bullets as "too long" if the content justifies the length
- Past tense for past roles, present for current - flag only if mixed within one role
- Flag: actual typos, wrong tense, broken parallelism, vague verbs ("worked on", "helped with"), missing metrics where they should be
- Flag: bullets that have been over-fragmented into multiple short sentences instead of one connected unit

**Cover letter:**
- First-person warmth is correct
- Flag: opening cliches ("I am writing to apply..."), generic closings, mismatched company name, repeated content from CV verbatim

**LinkedIn post / Social:**
- Sentence fragments for emphasis are intentional
- Line breaks for rhythm are intentional
- Flag: actual typos, factual errors, claims without specifics

**Blog post / Article:**
- Long flowing sentences are fine
- Variety of sentence lengths is good
- Flag: real grammar errors, ambiguous pronouns, broken logical flow, missing transitions where the reader gets lost

**Email:**
- Calibrate to recipient register (Slack-casual vs client-formal)
- Flag: tone mismatches, missing context, unclear ask

**Press release / Formal report:**
- Third-person neutral is correct
- Longer sentences with subordinate clauses are correct
- Flag: marketing puff, vague attributions, missing dates/numbers, register slips into casual

**Marketing copy:**
- Fragments are intentional
- Punchy short lines are intentional
- Flag: actual unclear claims, typos, broken legal/compliance lines

#### Standard Review Dimensions

After format calibration, check:

**Spelling & Typos**
- Misspelled words
- Wrong word used (their/there, affect/effect, role/roll)
- Missing or extra letters
- Autocorrect errors that produce real but wrong words
- Brand/product name spelling (VPBank capitalization, etc.)

**Grammar & Punctuation**
- Subject-verb agreement
- Tense consistency (within format rules above)
- Comma splices, missing commas, comma overuse
- Run-on sentences (only if genuinely confusing, not just long)
- Apostrophe misuse (it's/its, possessives)
- Capitalization errors
- Missing or incorrect end punctuation

**Clarity & Readability**
- Sentences that are genuinely confusing (not just long)
- Ambiguous pronouns ("they" with unclear referent)
- Jargon mismatched to audience
- Redundant phrases ("past history", "end result")
- **Active vs passive voice - only flag passive when the actor matters and is hidden, OR when active would clearly be punchier. Do not blanket-flag passive.**

**Logic & Flow**
- Ideas presented out of order
- Missing transitions where the reader would get lost
- Claims made without setup
- Contradictions
- Abrupt endings (in formats where conclusions matter)

**Tone & Register Consistency**
- Tone shifts mid-text
- Word choices off for the stated context
- Stiff phrasing in casual content, or too casual in formal content

**Post-Humanizer Mode (apply if humanizer was run first)**

When the text has just been through the humanizer, apply these *additional* checks because the humanizer can over-correct:

- **Over-fragmentation:** Three or more short sentences (under 12 words) in a row outside of marketing/social. Recommend merging.
- **Lost specificity:** Did concrete details get stripped (numbers, names, dates) in the rewrite? Flag any place where a specific fact was replaced with vague language.
- **Broken parallelism in CV bullets:** If the humanizer broke parallel structure across bullets in the same section, flag for restoration.
- **Lost connective tissue:** Did em-dashes or subordinate clauses get removed in a way that broke logical flow? "X happened. Y followed." reads worse than "X happened, which led to Y."
- **Voice over-correction:** Did the humanizer inject first-person voice or opinions into a format that shouldn't have them (CV, press release, formal report)?

---

### Step 3 - Structure the Output

Present findings in this order:

#### 1. Context Read (1-2 sentences)
Briefly confirm what you understood: type, tone, audience, language. This shows context-aware review, not just spell-checking.

Example: *"Reading this as a CV bullet for a senior marketing role at a Vietnamese bank - formal-professional, recruiter audience, English."*

#### 2. Issues Found (grouped by category)

For each issue:
- Quote the **original text** (short excerpt)
- Give the **suggested fix**
- Add a **brief reason** (one line) if not obvious

Format:
```
- Original: "The team have completed the report."
  Fix:      "The team has completed the report."
  Reason:   "Team" is a collective noun - singular in standard English.
```

**Skip categories with no issues** rather than noting "none found." Keep it clean.

**Group order (high to low priority):**
1. Errors that change meaning (wrong word, wrong tone mark, wrong fact)
2. Grammar & punctuation
3. Format/parallelism issues (especially for CVs)
4. Clarity & flow
5. Tone & register
6. Post-humanizer issues (if applicable)
7. Style suggestions (lowest priority - clearly mark as optional)

#### 3. Overall Assessment (3-5 sentences)
Cover:
- General quality
- Biggest area for improvement
- What's working
- Readiness verdict: "Ready to send", "Needs minor edits", "Revise before publishing"

#### 4. Clean Rewrite (Optional, but ON BY DEFAULT for orchestrator handoff)

If 3+ issues were found, provide a clean rewrite with all fixes applied. This makes the handoff to/from the humanizer skill clean. Mark it clearly as:

```
--- CLEAN VERSION ---
[full rewritten text with all fixes applied]
--- END CLEAN VERSION ---
```

If only 1-2 trivial fixes, skip the clean version - the user can fix in place.

---

## Output Tone

Match feedback tone to content type:
- **Formal documents** (press releases, reports, exec comms): precise and professional
- **CVs / cover letters**: practical, focused on impact and clarity, never condescending
- **Marketing copy / social**: energetic, flag anything that weakens punch or clarity
- **Casual / internal**: friendly, conversational - flag actual errors, not style choices
- **Non-native speaker content**: encouraging, focus on impact errors first, don't over-correct style

---

## Vietnamese-Specific Rules

When content is fully or partially in Vietnamese, apply these on top of the standard review.

### Diacritics & Tone Marks
Vietnamese meaning is entirely dependent on tone marks. Most common errors:

- **Missing tone marks**: "ban" vs "ban" vs "ban" vs "ban" - all different words
- **Wrong tone mark**: "suc khoe" not "suc khoe"
- **Missing diacritics on base vowels**
- **Telex/VNI ghost errors**: leftover sequences like "aws" instead of the intended character
- **Mobile autocorrect stripping**: phones sometimes drop tone marks silently

Flag with **high priority** - a single missing tone mark can completely change meaning.

### Grammar & Word Choice
- **Classifier misuse**: correct classifier for the noun
- **Redundant subject repetition**: Vietnamese often omits subjects - flag unnatural repetition
- **Tense/aspect particles**: "da", "dang", "se", "vua", "moi" - check consistency
- **Southern vs Northern dialect mixing**: flag if inconsistent in formal writing
- **Register-inappropriate pronouns**: "tao/may" in professional content, or stiff "toi" in casual Zalo

### Formal Writing Conventions
- **Honorifics**: check correct usage
- **Closing formulas**: press releases and letters have expected closing structures
- **Number formatting**: dau cham (.) as thousands separator - "1.000.000 dong" not "1,000,000 dong"
- **Date formatting**: "ngay 01 thang 04 nam 2025" formal; "01/04/2025" semi-formal
- **Capitalization of institutional names**: consistent caps
- For government/legal document proofreading: load `skills/vietnamese-language/references/formal-documents.md` (pronoun protocol, capitalization rules, address conventions)
- For press release proofreading: load `skills/vietnamese-language/references/press-releases.md` (THÔNG CÁO BÁO CHÍ structure, quote attribution, boilerplate)

### Vietnamese-English Code-Switching
- Flag English terms ignored when standard Vietnamese exists without reason
- Flag English used in wrong grammatical position for Vietnamese sentence structure
- Flag inconsistent capitalization of brand names
- Loan words should use consistent spelling

---

## Edge Cases

- **Very short content** (1-3 sentences): Skip section headers, give compact inline feedback + one-line verdict
- **Mixed language**: Review each language by its own standards; flag awkward code-switching only if it affects readability
- **Already clean content**: Say so directly - "This is well-written and ready to use." Don't invent issues.
- **User only asked about typos**: Run the full check silently, but lead with typos and mention other issues briefly at the end
- **Intentional style choices** (sentence fragments in ads, parallelism in CVs): Note as intentional, not errors
- **Just-humanized content**: Apply post-humanizer mode in Step 2

---

## What NOT to Do

- Don't rewrite the entire text unless it's the optional clean rewrite at the end (or the user asks)
- Don't flag personal style choices as errors unless they create confusion
- Don't over-explain - one-line reasons are enough unless something is nuanced
- Don't be condescending - keep feedback constructive and specific
- **Don't flag long sentences as "too long" just because they're long.** Flag only if genuinely confusing.
- **Don't flag passive voice as an error.** Flag only if active voice is clearly stronger AND the format calls for it.
- **Don't flatten CV bullets into prose.** Parallelism is the format.
- **Don't flag fragments in marketing copy or social posts** unless they break meaning.
