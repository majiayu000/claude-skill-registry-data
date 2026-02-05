---
name: source-only-enforcer
description: |
  CRITICAL QUALITY GATE: Enforces source-only policy for ALL medical study guide creation.

  ACTIVATES when creating study guides for ANY medical specialty: pharmacology, pathophysiology,
  clinical medicine, physical examination, or procedures.

  BLOCKS creation without pre-creation verification checklist confirming source file and template.

  This skill prevents adding external medical facts (except researched mnemonics) and ensures
  all study guide content comes exclusively from the specified source file.
skill_type: guardrail
enforcement_level: block
priority: critical
version: 2.1.0
tools_required:
  - Read
  - Write
  - Edit
  - WebSearch
activation_confidence: high
---

# Source-Only Enforcer

## Core Responsibility

Ensure ALL medical study guides are created from source material only, with mandatory pre-creation verification.

**NO external medical facts** - Only information from source file (exception: researched mnemonics via WebSearch).

**Works for ALL medical specialties**: Pharmacology, pathophysiology, clinical medicine, physical examination, procedures.

## When This Activates

**Prompt triggers:**
- "create drug chart" (Excel or HTML)
- "create learning objectives guide" (HTML)
- "create clinical assessment guide" (HTML)
- "make study guide from lecture"
- "generate word/excel/html study guide"
- "/drugs-3-tab-excel [source-file]"
- "/LO-word [source-file]"
- "/drugs-html [source-file]"
- "/LO-html [source-file]"
- "/clinical-assessment-html [source-file]"

**File triggers:**
- Working with files in `Claude Study Tools/` directory
- Files ending in `.xlsx`, `.docx`, `.html`

## Pre-Creation Verification Checklist

Before creating ANY study guide, you MUST state:

```
VERIFICATION CHECKLIST:
☐ Source file: [exact path to source file]
☐ Instruction template: [Drug Chart HTML / Excel Drug Chart / HTML LO / Clinical Assessment / Word LO]
☐ Source-only policy: I will ONLY use information from source file
☐ Learning objectives: I will extract LO statements EXACTLY as written (NO paraphrasing)
☐ Exception: Memory tricks/mnemonics WILL be researched via WebSearch
☐ MANDATORY: I will WebSearch for mnemonics/analogies - I will NOT invent them
☐ Save location: [Class]/[Exam]/Claude Study Tools/
```

## Required Actions

1. **Read ENTIRE source file first** - No skipping or partial reads
2. **Read COMPLETE template file** - Understand all formatting requirements
3. **STATE the verification checklist** - Must be explicitly stated
4. **Create verification marker:**
   ```bash
   mkdir -p "$CLAUDE_PROJECT_DIR/.claude/study-guide-cache/${session_id}"
   echo '{"verified":true,"timestamp":"'$(date -Iseconds)'"}' > \
     "$CLAUDE_PROJECT_DIR/.claude/study-guide-cache/${session_id}/verification.json"
   ```
5. **ONLY THEN proceed with creation**

## Enforcement

This skill works with the `verification-guard.sh` hook:
- Hook BLOCKS file writes without verification marker
- You must create the verification marker before proceeding
- Session-aware: First study guide blocks, subsequent ones in same session allowed

## What Gets BLOCKED

❌ Creating study guides without stating verification checklist
❌ Adding external medical facts not in source file
❌ Inventing mnemonics without WebSearch research
❌ Skipping template file review
❌ Not specifying exact source file path
❌ **Paraphrasing learning objective statements**

## What's ALLOWED

✅ Information from source file only
✅ Researched mnemonics via WebSearch (must cite source)
✅ External additions marked with asterisk (*) if absolutely necessary
✅ Page references from source file
✅ Paraphrasing of answers/explanations (same meaning from source)
✅ Formatting changes to content (bullets, tables, etc.)

## Learning Objective Verbatim Requirement

<verbatim-requirement>
CRITICAL: Learning objective STATEMENTS must be copied EXACTLY as written in the source.
- Copy word-for-word, character-for-character
- Do NOT rephrase, summarize, or "improve" wording
- Preserve original numbering and sequence
- If an LO is long, still copy it completely
</verbatim-requirement>

**This applies to:** The LO statement text itself (e.g., "Describe the mechanism of action of beta-blockers")

**This does NOT apply to:** Answers, explanations, or content that responds to the LO (these can be paraphrased from source)

**Example - CORRECT:**
```
Source: "1. Describe the mechanism of action of beta-blockers"
Guide:  "1. Describe the mechanism of action of beta-blockers"
```

**Example - INCORRECT:**
```
Source: "1. Describe the mechanism of action of beta-blockers"
Guide:  "1. Explain how beta-blockers work"  ← WRONG: Paraphrased
```

## Emergency Override

If hooks malfunction:
```bash
export SKIP_STUDY_GUIDE_VERIFICATION=1
# Your study guide creation command
unset SKIP_STUDY_GUIDE_VERIFICATION
```

## Post-Creation

After creating study guide, you'll automatically see a post-verification reminder. Complete all 4 checks:

1. ✓ Source Accuracy
2. ✓ Template Compliance
3. ✓ Completeness
4. ✓ Quality Checks

Then state: "Post-creation verification complete"

## Common Failures

**If hook blocks your creation:**

**Reason:** Verification marker not present
**Solution:**
1. Read entire source file first
2. State verification checklist
3. Create verification marker (command shown above)
4. THEN proceed with file creation

**Reason:** Trying to add external medical facts
**Solution:**
- Use ONLY source file information
- For mnemonics: WebSearch for established mnemonics, cite source
- Mark any external additions with asterisk (*)

## Tips

💡 Use slash commands for automatic verification:
- `/drugs-3-tab-excel [source-file]` - Automatically handles verification
- `/LO-word [source-file]` - Automatically handles verification
- `/verify-accuracy [file] [source]` - Deep accuracy check

💡 Session-aware: Once verified this session, create multiple study guides without repeated blocking

💡 Source-only policy protects you from inaccurate study materials

---

## Deep-Dive Resources

For comprehensive guidance on specific topics, see the resources/ directory:

### Source Validation
**[Source Validation Guide](resources/source-validation-guide.md)** - Complete guide to validating source files, checking content coverage, and ensuring source quality before creation

### Preventing Hallucinations
**[Hallucination Prevention](resources/hallucination-prevention.md)** - Strategies to avoid adding external medical facts, recognizing common hallucination patterns, and maintaining source fidelity

### Marking External Information
**[External Info Marking](resources/external-info-marking.md)** - How to properly mark researched mnemonics with (*) and source attribution, using the mnemonic-researcher agent

### Citation Best Practices
**[Citation Patterns](resources/citation-patterns.md)** - Methods for citing source material (page numbers, section headers) to enable verification

### Complete Examples
**[Complete Examples](resources/complete-examples.md)** - Real-world examples of correct vs. incorrect source-only enforcement across different template types

### Verification Checklists
**[Verification Checklists](resources/verification-checklists.md)** - Step-by-step checklists for pre-creation, during-creation, and post-creation verification

### Learning Objective Preservation
**[Learning Objective Preservation](resources/learning-objective-preservation.md)** - CRITICAL guide for extracting learning objectives verbatim (exact text, no paraphrasing), with examples of correct vs. incorrect extraction

**Note:** Resources are loaded on-demand when you need detailed guidance on specific topics. The main skill provides the essential workflow; resources provide deep-dive documentation.