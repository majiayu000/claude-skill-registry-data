---
name: grammar-checker
description: This skill should be used when performing systematic scans of research paper text to identify and fix typos, grammar errors, inappropriate words, and awkward expressions. Use for thorough proofreading and error correction in academic writing for computer science conferences.
---

# Grammar Checker

Systematically scan research paper text through multiple passes to identify and fix typos, grammar errors, inappropriate word choices, and awkward expressions.

## When to Use This Skill

- Proofreading research papers before submission
- Performing systematic error detection across multiple categories
- Fixing specific grammar and usage issues
- Cleaning up text after major revisions
- Final pass before conference submission
- Non-native speakers checking for common errors

## Multi-Pass Scanning Approach

Perform systematic scans in the following order, completing each pass before moving to the next:

### Pass 1: Typos and Spelling
Scan for:
- Misspelled words
- Incorrect technical terminology
- Inconsistent capitalization (e.g., "LaTeX" vs "Latex")
- Inconsistent hyphenation (e.g., "real-time" vs "real time")
- Common typos (e.g., "teh", "recieve", "seperate")
- Missing or extra spaces
- Duplicated words (e.g., "the the")

### Pass 2: Grammar Errors
Scan for:
- Subject-verb agreement errors
- Incorrect verb tenses
- Wrong article usage (a/an/the)
- Incorrect prepositions
- Pronoun-antecedent agreement
- Sentence fragments
- Run-on sentences
- Comma splices
- Misplaced modifiers

### Pass 3: Inappropriate Words and Phrases
Scan for:
- Informal language (e.g., "gonna", "kinda", "a lot of")
- Colloquialisms and slang
- Contractions (e.g., "don't", "can't", "won't")
- First-person pronouns overuse in inappropriate contexts
- Vague quantifiers (e.g., "very", "really", "quite")
- Weasel words (e.g., "perhaps", "might", "possibly" when not needed)
- Emotional or subjective language
- Anthropomorphization (e.g., "the system thinks", "the paper argues")

### Pass 4: Awkward Expressions
Scan for:
- Unnecessarily complex sentence structures
- Passive voice where active is clearer
- Wordy phrases that can be simplified
- Redundant expressions (e.g., "past history", "future plans")
- Unclear pronoun references
- Dangling participles
- Split infinitives (when awkward)
- Awkward word order
- Non-idiomatic phrases for non-native speakers

### Pass 5: Academic Writing Style
Scan for:
- Inconsistent terminology across sections
- Undefined acronyms on first use
- Incorrect tense (present for current work, past for related work)
- Inappropriate use of hyphens to connect clauses
- Missing transitions between ideas
- Inconsistent formatting (citations, equations, etc.)
- Overly casual or overly complex language

## Output Format

For each pass, provide:

### 1. Pass Header
```
===== Pass X: [Category Name] =====
```

### 2. Issues Found
For each issue detected:
```
Location: [section/paragraph/line reference]
Issue Type: [specific error type]
Original: "[quoted text with error]"
Fixed: "[corrected text]"
Explanation: [why this is an error and why the fix is appropriate]
```

### 3. Pass Summary
```
Total issues found: [number]
Issues fixed: [number]
```

### 4. Final Summary
After all passes:
```
===== Overall Summary =====
Total scans performed: 5
Total issues found: [number]
Total fixes applied: [number]

Issues by category:
- Typos and Spelling: [count]
- Grammar Errors: [count]
- Inappropriate Words: [count]
- Awkward Expressions: [count]
- Academic Style: [count]
```

### 5. Corrected Text
Provide the fully corrected version of the text with all fixes applied.

## Scanning Guidelines

### Be Systematic
- Complete each pass fully before moving to the next
- Don't skip passes even if earlier passes found few errors
- Reread the text in each pass with fresh focus on that category

### Be Specific
- Quote the exact text with the error
- Provide precise location references
- Explain why something is an error
- Justify the proposed fix

### Be Conservative
- Only flag genuine errors, not stylistic preferences
- Don't "fix" correct but unusual constructions
- Preserve technical terminology even if uncommon
- Respect author's voice and style when appropriate

### Be Consistent
- Apply the same standards throughout the text
- Don't flag similar issues differently
- Maintain consistency with previous fixes

## Common Errors in Academic Writing

### Article Errors (for non-native speakers)
- Missing articles: "We propose ~~system~~ → a system"
- Wrong article: "We use ~~a~~ HTTP → the HTTP protocol"
- Unnecessary article: "The ~~the~~ latency is low → Latency is low"

### Preposition Errors
- "Different ~~with~~ → from"
- "Consist ~~in~~ → of"
- "Depend ~~from~~ → on"
- "Focus ~~to~~ → on"

### Verb Tense Errors
- Related work: "Smith et al. ~~propose~~ → proposed"
- Current work: "We ~~proposed~~ → propose"
- Results: "Figure 1 ~~showed~~ → shows"

### Common Typos in Technical Writing
- "seperator" → "separator"
- "occured" → "occurred"
- "sucessful" → "successful"
- "thier" → "their"
- "recieve" → "receive"

### Awkward Constructions
- "In order to" → "To" (simpler)
- "Due to the fact that" → "Because"
- "At this point in time" → "Now"
- "Make use of" → "Use"

### Inappropriate Informal Language
- "a lot of data" → "substantial data" or "large amounts of data"
- "get better results" → "achieve better results" or "obtain better results"
- "pretty good" → "quite good" or "favorable"
- "kind of interesting" → "somewhat interesting" or remove qualifier

## Error Severity Levels

Classify errors by severity to prioritize fixes:

### Critical (Must Fix)
- Grammar errors that change meaning
- Technical term misspellings
- Factual errors in text
- Undefined acronyms

### Major (Should Fix)
- Grammar errors that don't change meaning but are incorrect
- Awkward expressions that confuse readers
- Inconsistent terminology
- Informal language in formal sections

### Minor (Nice to Fix)
- Stylistic improvements
- Slightly awkward but correct constructions
- Overly complex sentences that could be simpler
- Minor redundancies

## Special Considerations for Academic Papers

### LaTeX Integrity
- Do not modify LaTeX commands or environments
- Only fix text content within commands
- Preserve math mode content unless clearly erroneous
- Maintain citation formatting

### Technical Terminology
- Verify technical terms against standard usage
- Don't "correct" domain-specific jargon
- Preserve acronym formatting (e.g., "RDMA", "TCP/IP")
- Check consistency of system/protocol names

### Common Academic Patterns
- "We propose X" ✓ (correct present tense)
- "The system achieves Y" ✓ (correct)
- "As shown in Figure Z" ✓ (correct)
- "This demonstrates that..." ✓ (correct)

## Target Audience

Research papers for top-tier computer science conferences (OSDI, NSDI, SOSP, SIGCOMM, etc.) written by both native and non-native English speakers.

## Important Guidelines

### Do Not Over-Correct
- Accept correct but uncommon constructions
- Don't impose one "right" way when multiple are valid
- Preserve author's voice when possible
- Focus on errors, not preferences

### Provide Explanations
- Explain why something is an error
- Note when a fix improves clarity vs correctness
- Indicate severity of each issue
- Help authors learn from corrections

### Be Thorough But Efficient
- Complete all five passes systematically
- Don't redundantly flag the same error type
- Group similar errors when reporting
- Focus on patterns, not just individual instances

### Maintain Academic Tone
- All corrections should preserve formal academic style
- Don't make text too casual or too stuffy
- Maintain appropriate technical level
- Keep language precise and clear

## Example Output

```
===== Pass 1: Typos and Spelling =====

Location: Abstract, line 3
Issue Type: Spelling error
Original: "We achive low latency"
Fixed: "We achieve low latency"
Explanation: "Achive" is a common misspelling of "achieve"

Location: Introduction, paragraph 2
Issue Type: Duplicated word
Original: "the the system"
Fixed: "the system"
Explanation: Duplicated article

Total issues found: 12
Issues fixed: 12

===== Pass 2: Grammar Errors =====

Location: Section 3, paragraph 1
Issue Type: Subject-verb agreement
Original: "The results shows that"
Fixed: "The results show that"
Explanation: Plural subject "results" requires plural verb "show"

...

===== Overall Summary =====
Total scans performed: 5
Total issues found: 47
Total fixes applied: 47

Issues by category:
- Typos and Spelling: 12
- Grammar Errors: 15
- Inappropriate Words: 8
- Awkward Expressions: 9
- Academic Style: 3

===== Corrected Text =====

[Full corrected version of the text]
```
