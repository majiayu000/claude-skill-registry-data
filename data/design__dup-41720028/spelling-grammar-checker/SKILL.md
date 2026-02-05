---
name: spelling-grammar-checker
description: >-
  Analyze documentation, UI strings, comments, and user-facing text for spelling, grammar, clarity, and style.
  Scope: validation reports with severity, location, original/corrected text, rationale; external tooling recommendations.
  Triggers: "check spelling", "grammar", "proofread", "review text", "validate documentation".
---

# SPELLING_GRAMMAR_CHECKER

## EXECUTION PHASES

### Phase 1: Clarification (Ask)
**Logic**: Input_Requirement != Complete -> Stop && Ask.
- IF File_Path_Missing AND Text_Pasted_Missing -> Request(Input)
- IF Content_Type_Ambiguous -> Confirm(Docs vs UI vs Code_Comments)
- IF Output_Format_Unclear -> Confirm(Report vs Fix_Suggestions vs Diff)

### Phase 2: Planning (Think)
**Logic**: Task -> Plan -> Approval.
- Identify: File_Paths OR Pasted_Text
- Determine: Content_Type (Docs/UI/Comments)
- Validate: User_Intent (Review vs Auto_Fix)
- IF Impact > Low -> Propose(Files + Changes) -> Wait(Confirmation)

### Phase 3: Execution (Do)
**Logic**: Step_1 -> Verify -> Step_2.

**Step 1: Extraction**
- Input -> Read_File OR Parse_Pasted_Text
- Extract: Natural_Language_Excerpts + Line_Numbers
- Priority: Docs > UI > Comments > Code_Blocks (unless Explicit_Request)

**Step 2: Automated Tool Recommendations**
- Suggest: `codespell`, `cspell`, `languagetool`, `vale`, `aspell`, `hunspell`, `alex`
- Format: Exact_Command_Examples + Installation_Instructions
- **CRITICAL**: DO NOT EXECUTE external tools (run NOT by the agent)
- Action: READ FILE: `@references/commands.md`

**Step 3: Manual Validation**
- Check: Subject-Verb_Agreement, Tense, Pronoun_Clarity, Parallel_Structure, Punctuation
- Validate: Run-on_Sentences, Passive/Active_Voice, Clarity, Jargon_Context
- Verify: Technical_Accuracy (do NOT change validated terms without confirmation)
- Assess: Style_Consistency across document

**Step 4: Classification**
- Priority: User_Visible > Internal
- Assign: HIGH/MEDIUM/LOW Severity
- HIGH: Comprehension_Issues (Misspelled_Terms, Grammar_Errors, Incorrect_Technical_Terms)
- MEDIUM: Professionalism_Issues (Typos, Minor_Grammar, Inconsistent_Style)
- LOW: Minor_Issues (Style_Improvements, Very_Minor_Typos, Word_Choice_Alternatives)

**Step 5: Output Generation**
- Format: Structured_Report (Schema below)
- IF User_Requests_Fixes -> Provide: Diff_Suggestions
- **CONSTRAINT**: DO NOT modify files

### Phase 4: Validation (Check)
**Logic**: Result -> Checklist -> Done.
- [ ] Text_Extracted
- [ ] Tool_Commands_Generated
- [ ] Grammar_Rules_Validated
- [ ] Style_Consistency_Checked
- [ ] Technical_Terms_Verified
- [ ] Severity_Assigned_Correctly
- [ ] Output_Matches_Schema

## OUTPUT SCHEMA (Exact)

[SEVERITY] Issue Type

Description: Clear explanation of error and impact.

Location: file_path:line_number

Original Text:
problematic text here

Corrected Text:
corrected text here

Explanation: Brief rationale for correction.

## COMMON ERRORS (Reference)

### Spelling
```
recieve → receive
seperate → separate
accomodate → accommodate
definately → definitely
occured → occurred
priviledge → privilege
recomend → recommend
sucess → success
```

### Grammar Anti-patterns
```
# Subject-verb disagreement
WRONG: The list of items contain errors.
CORRECT: The list of items contains errors.

# Incorrect tense
WRONG: He go to the store yesterday.
CORRECT: He went to the store yesterday.

# Missing apostrophe
WRONG: The teams strategy was flawed.
CORRECT: The team's strategy was flawed.

# Run-on sentence
WRONG: This is a test it should work.
CORRECT: This is a test. It should work.

# Dangling modifier
WRONG: Running down the street, the trees were beautiful.
CORRECT: Running down the street, I saw that the trees were beautiful.
```

### Clarity Issues
```
# Ambiguous pronoun
UNCLEAR: John told Mike he was wrong. (Who is "he"?)
CLEAR: John told Mike that Mike was wrong.

# Jargon without context
UNCLEAR: We need to leverage synergies in our CI/CD pipeline.
CLEAR: We need to improve integration in our continuous integration/deployment pipeline.

# Passive voice confusion
UNCLEAR: The report was completed by the team.
CLEAR: The team completed the report on Tuesday.
```

## CRITICAL RULES
- Priority: Docs/UI > Comments > Code_Blocks (unless Explicit)
- Context_Aware: Do NOT flag validated technical terms as errors without confirmation
- Tone: Professional. Preserve project-specific terminology when appropriate
- Consistency: Ensure terminology/style used consistently across document
- Accuracy: Confirm technical terms/statements factually correct before changing

## REVIEW GUIDELINES
1. Use appropriate tools for content_type (docs vs comments)
2. Consider audience - technical docs use different conventions than user-facing content
3. Respect project conventions - specific terminology/style preferences
4. Check false positives - technical terms may appear as spelling errors
5. Prioritize user-visible text - docs, UI, comments over internal code
6. Maintain consistency - corrections must align with existing document style

## SECURITY CONSIDERATIONS
- **Input Sanitization**: Validate file paths, prevent directory traversal
- **Path Safety**: Absolute paths only, whitelist allowed directories
- **Command Execution**: NEVER execute suggested external tools directly
- **Error Handling**: Sanitized error messages, no path exposure in failures
- **File Operations**: Require explicit user confirmation for any file modifications

## EXAMPLES

### Example 1: README Review
User: Review README.md for spelling and grammar.
Agent: [Output: JSON-serializable report with HIGH items first + human-readable report using schema above]

### Example 2: Clarity Summary
User: Summarize clarity issues in docs/guide.md.
Agent: [Output: Top 3 clarity issues + suggested rewrites + short rationales]

### Example 3: UI String Check
User: Check UI strings in src/components/ for typos.
Agent: [Output: Priority on UI strings, code comments secondary, unless code explicitly requested]
