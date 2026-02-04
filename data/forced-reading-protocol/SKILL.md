---
name: forced-reading-protocol
description: Use when analyzing critical documents, specifications, or large files (>3000 lines), before any synthesis or conclusions - enforces complete line-by-line reading with quantitative verification to prevent skimming that leads to incomplete understanding
---

# Forced Complete Reading Protocol

## Overview

Prevent skimming and superficial reading through mandatory line-by-line comprehension with quantitative verification.

**Core principle**: Thoroughness cannot be optional. Complete reading is architectural enforcement, not best practice suggestion.

**Violating the letter of this protocol is violating the spirit of this protocol.**

## When to Use

**Automatic activation for**:
- All `.md` files (specifications, plans, documentation)
- All files >=3000 lines (large files most likely to be skimmed)
- SPEC_* and PLAN_* files (critical documents)
- **/SKILL.md files (skill definitions)
- User prompts >3000 characters (~500 words)

**Manual activation**:
- `/shannon:read_complete <file>` - Force protocol for any file
- Skill auto-injected by hooks when triggers detected

**Don't use for**:
- Quick reference lookups (API syntax, command flags)
- Repeated reads of same file (if previously verified complete)
- User explicitly wants fast skim (use `/sh_read_normal <file>`)

## The Iron Law

```
NO SYNTHESIS WITHOUT COMPLETE READING FIRST
```

If you haven't verified lines_read == total_lines, you cannot make conclusions.

## The Four-Step Protocol

### Step 1: PRE-COUNT (Before reading begins)

**MANDATORY**: Count total lines BEFORE reading ANY content.

**Commands**:
```bash
# Count lines first
total_lines=$(wc -l < file.md)
```

**Output required**:
```
File has {N} lines. Now I will read all {N} lines completely.
```

**No exceptions**: You cannot read without knowing total line count first.

### Step 2: SEQUENTIAL READING (Line-by-line)

**Read EVERY line sequentially from 1 to N**.

**NOT allowed**:
- ❌ "Read relevant sections"
- ❌ "Scan for key points"
- ❌ "Quick overview then deep dive"
- ❌ offset=0, limit=100 (partial reading)
- ❌ grep/search without complete reading

**REQUIRED**:
- ✅ Read line 1
- ✅ Read line 2
- ✅ Read line 3
- ✅ ...continue sequentially...
- ✅ Read line N (last line)

**Tracking**: Count each line as you read it.

### Step 3: VERIFY COMPLETENESS (Before synthesis)

**Verify**: `lines_read == total_lines`

**Formula**:
```
IF lines_read < total_lines THEN
  missing_lines = total_lines - lines_read
  ERROR: "INCOMPLETE READING: Missing {missing_lines} lines"
  BLOCK: No analysis, no synthesis, no conclusions
  REQUIRED: Return to Step 2, read missing lines
END IF
```

**Verification output**:
```
✅ COMPLETE READING VERIFIED
   Total lines: {N}
   Lines read: {N}
   Completeness: 100.0%
   Status: READY FOR SYNTHESIS
```

### Step 4: SEQUENTIAL SYNTHESIS (After complete reading only)

**Use Sequential MCP for deep thinking about what was read**.

**Minimum thinking steps** (based on file size):
- Small (<500 lines): 50+ thoughts
- Medium (500-2000 lines): 100+ thoughts
- Large (2000-5000 lines): 200+ thoughts
- Critical (5000+ lines): 500+ thoughts

**NOT allowed until verified complete**:
- ❌ Analysis during reading
- ❌ Patterns identified during reading
- ❌ Conclusions during reading
- ❌ "I noticed that..." during reading

**ONLY after verification**:
- ✅ Synthesis via Sequential MCP
- ✅ Pattern identification
- ✅ Comprehensive analysis
- ✅ Actionable conclusions

## Known Violations and Counters

Captured from baseline testing (RED phase):

### ❌ VIOLATION 1: "I'll read the relevant sections first"

**Baseline behavior**: Agent uses grep/search to find "relevant" sections, skips complete reading.

**Rationalization captured**:
> "Let me search for the key requirements first to understand scope"

**Shannon counter**:
```
⚠️ STOP. "Relevant sections" = incomplete understanding.

REALITY CHECK:
- You don't know what's relevant until you've read everything
- "Relevant" is determined by your assumptions, not reality
- Critical details are often in "irrelevant" sections

REQUIRED ACTION:
1. Count total lines
2. Read ALL lines sequentially (line 1, 2, 3, ..., N)
3. THEN identify what's relevant (after complete reading)

NO EXCEPTIONS.
```

### ❌ VIOLATION 2: "Read offset=0, limit=200 to get started"

**Baseline behavior**: Agent reads partial file to "get started", never returns to read rest.

**Rationalization captured**:
> "I'll read the first 200 lines to understand structure, then continue"

**Shannon counter**:
```
⚠️ STOP. Partial reading is incomplete reading.

REALITY CHECK:
- "Get started" reading = never finish reading
- Lines 201-N contain critical details you'll miss
- "Overview" = superficial understanding

REQUIRED ACTION:
1. Count total lines
2. Read ALL lines (not just first 200)
3. Verify lines_read == total_lines
4. NO synthesis until verification passes

NO EXCEPTIONS.
```

### ❌ VIOLATION 3: "File is too long, I'll skim efficiently"

**Baseline behavior**: Agent rationalizes skimming for files >2000 lines.

**Rationalization captured**:
> "This 2,500-line specification is quite extensive - I'll skim efficiently for key points"

**Shannon counter**:
```
⚠️ STOP. "Too long" is not an exemption.

REALITY CHECK:
- Long files are EXACTLY why this protocol exists
- "Skim efficiently" = miss critical details
- Mission-critical work cannot tolerate "good enough" understanding

REQUIRED ACTION:
1. Yes, read all 2,500 lines
2. Use Sequential MCP for 200+ synthesis thoughts
3. This takes time (30-60 min) - that's acceptable
4. Complete understanding > speed

NO EXCEPTIONS.
```

### ❌ VIOLATION 4: "I remember this file from earlier"

**Baseline behavior**: Agent skips re-reading based on session memory.

**Rationalization captured**:
> "I already read this file earlier in the session"

**Shannon counter**:
```
⚠️ STOP. Memory is not verification.

REALITY CHECK:
- Remembering != having read every line
- Files may have changed
- "Key points" = selective memory, not complete understanding

REQUIRED ACTION:
1. Re-count lines (file may have changed)
2. Either verify previous complete reading OR re-read:
   - If previous verification exists (100% complete) → synthesis allowed
   - If no verification exists → re-read completely

NO EXCEPTIONS.
```

## Red Flags - STOP Immediately

If you catch yourself using these phrases, **STOP** - you're about to violate:

**Skip-reading triggers**:
- "read relevant sections"
- "scan for", "look for", "find the parts about"
- "overview first", "get started with"
- "skim efficiently", "quick pass through"

**Partial-reading triggers**:
- "offset=0, limit=100"
- "first few hundred lines"
- "initial sections"
- "start with the beginning"

**Length-based rationalization triggers**:
- "file is too long"
- "quite extensive"
- "very large specification"
- "efficiently review"

**Memory-based triggers**:
- "already read this"
- "recall from earlier"
- "familiar with this file"
- "remember the key points"

**ALL OF THESE MEAN**: STOP. Count lines. Read all lines. Verify completeness.

## Quantitative Tracking

**Shannon enhancement**: Track reading completeness across session.

**Save to Serena**:
```python
serena.write_memory("shannon/reading/{file_hash}", {
    "file_path": file_path,
    "total_lines": total_lines,
    "lines_read": lines_read,
    "completeness": lines_read / total_lines,
    "synthesis_steps": synthesis_steps,
    "timestamp": ISO_timestamp,
    "status": "COMPLETE" if completeness == 1.0 else "INCOMPLETE"
})
```

**Query reading history**:
```python
# Check if file was completely read before
history = serena.read_memory("shannon/reading/{file_hash}")
if history and history["completeness"] == 1.0:
    # Previously verified complete
    # Can skip re-reading OR re-verify if file changed
```

## Integration with Shannon Commands

**Enhanced commands that enforce this protocol**:

**/shannon:spec**: Before 8D analysis:
```
1. Count specification lines
2. Read ALL lines sequentially
3. Verify completeness (100%)
4. Sequential MCP synthesis (100+ thoughts)
5. THEN present 8D analysis
```

**/shannon:analyze**: Before analysis:
```
1. For each critical file, count lines
2. Read ALL lines per file
3. Verify per-file completeness
4. Aggregate verification
5. THEN synthesize findings
```

**/shannon:wave**: Before wave execution:
```
1. Count wave plan lines
2. Read ALL tasks sequentially
3. Verify plan completeness
4. Sequential synthesis
5. THEN execute waves
```

## Configuration

**Per-project config**: `.shannon/reading-enforcement.json`

```json
{
  "enforcement_enabled": true,
  "critical_file_patterns": [
    "*.md",
    "SPEC_*",
    "PLAN_*",
    "**/skills/**/SKILL.md"
  ],
  "size_threshold": 3000,
  "minimum_synthesis_steps": {
    "small": 50,
    "medium": 100,
    "large": 200,
    "critical": 500
  },
  "override_allowed": true,
  "override_audit": true
}
```

**Override for legitimate cases**:
```bash
/sh_read_normal <file>  # Disables enforcement
# All overrides logged to Serena for audit
```

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to read completely" | Simple files hide critical details. Read all lines. |
| "I'll complete reading after initial analysis" | Analysis before complete reading = wrong analysis. |
| "File is too long for complete reading" | Long files are EXACTLY why protocol exists. |
| "Relevant sections are enough" | You don't know what's relevant until you've read everything. |
| "I already know this file's content" | Knowledge ≠ verification. Re-verify or re-read. |
| "Skimming is more efficient" | Efficient incompleteness = unreliable results. |

## Integration with Other Skills

**This skill is prerequisite for**:
- **spec-analysis** - MUST read specification completely before 8D scoring
- **shannon-analysis** - MUST read codebase files completely
- **writing-plans** - MUST read requirements completely before planning
- **executing-plans** - MUST read plan completely before execution

**Complementary skills**:
- **verification-before-completion** - Both enforce evidence over claims
- **systematic-debugging** - Both enforce thoroughness over guessing

## The Bottom Line

**For mission-critical work, complete understanding is mandatory.**

Same as NO MOCKS for testing: superficial comprehension = unreliable results.

If you follow "read every line" for code reviews, follow it for specifications.

This protocol is not optional. It's architectural enforcement of thoroughness.

**Target domains**: Finance, Healthcare, Legal, Security, Aerospace - where AI hallucinations from incomplete reading are unacceptable.

