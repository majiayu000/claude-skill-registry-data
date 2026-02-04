---
name: mnemonic-researcher
description: |
  CRITICAL AUTOMATION: Automatically researches PROVEN medical mnemonics during study guide creation.

  ACTIVATES when creating study guides and mnemonics are mentioned. Launches the medical-mnemonic-researcher
  agent to find established USMLE mnemonics from medical education sources.

  NEVER invents mnemonics - only finds ones that already exist and are validated by medical students.
skill_type: domain
enforcement_level: suggest
priority: high
version: 2.1.0
tools_required:
  - Task
  - WebSearch
activation_confidence: high
---

# Mnemonic Researcher

## Core Responsibility

**Automatically research and find PROVEN, ESTABLISHED medical mnemonics** from medical education sources when creating study guides.

**CRITICAL: NEVER invent mnemonics. ALWAYS use the medical-mnemonic-researcher agent to find existing, validated mnemonics.**

## When This Activates

**Prompt triggers:**
- "find mnemonics for [topic]"
- "what are good mnemonics for [topic]"
- "memory tricks for [topic]"
- "how to remember [topic]"
- "USMLE mnemonics for [topic]"
- Creating study guides (automatic during creation)

**File triggers:**
- Working with study guide files (`.docx`, `.xlsx`, `.html`)
- Creating drug charts
- Creating learning objectives guides
- Creating clinical assessment guides

**Intent patterns:**
- Need memorization aids for medical concepts
- Creating study materials requiring mnemonics
- Looking for memory tricks for drugs/diseases/anatomy

## How This Works

### Automatic Agent Invocation

When you need mnemonics, this skill automatically:

1. **Launches the medical-mnemonic-researcher agent**
2. **Agent searches medical education sources:**
   - Reddit r/medicalschool, r/step1, r/step2
   - StudentDoctor Network forums
   - USMLE resources
   - First Aid references
   - Sketchy/Pathoma mentions
   - Medical education blogs

3. **Agent returns comprehensive report:**
   - Top 3 recommended mnemonics with reliability scores
   - Source links for each mnemonic
   - User feedback from medical students
   - Recommendations for USMLE vs general use

### Required Action Pattern

When mnemonics are needed, you MUST:

```
I'll use the medical-mnemonic-researcher agent to find established mnemonics for [topic].
```

Then invoke the agent using the Task tool:

```markdown
Use the medical-mnemonic-researcher agent to research mnemonics for [specific medical topic].
```

**CRITICAL:** Wait for the agent to complete and return the mnemonic research report before continuing with study guide creation.

## Example Workflow

**User request:** "Create an Excel drug chart for HIV drugs"

**Your response:**
1. Complete pre-creation verification checklist
2. Read source file
3. **Recognize need for mnemonics**
4. **Invoke agent:** "I'll use the medical-mnemonic-researcher agent to find mnemonics for HIV drug classes"
5. **Wait for agent report**
6. **Use mnemonics from report** in the study guide
7. **Include source attribution** for each mnemonic

## Agent Integration

### When to Launch Agent

Launch the medical-mnemonic-researcher agent when:
- Creating any study guide that includes mnemonic sections
- User explicitly asks for mnemonics
- Template requires "Memory tricks" or "Mnemonics" sections
- Creating drug charts (need drug class mnemonics)
- Creating anatomy guides (need anatomical mnemonics)

### How to Launch Agent

Use the Task tool:

```
Task(
  subagent_type="general-purpose",
  description="Research medical mnemonics for [topic]",
  prompt="Use the medical-mnemonic-researcher agent to research established medical mnemonics for [specific topic]. Find PROVEN mnemonics from medical education sources (Reddit r/medicalschool, USMLE forums, First Aid, Sketchy, Pathoma). Return comprehensive report with top 3 mnemonics, reliability scores, and source links."
)
```

### Agent Output Format

The agent returns a structured report:

```markdown
# Mnemonic Research Report: [Topic]

## Executive Summary
[Top 3 recommended mnemonics]

## Top Recommended Mnemonics
[Detailed breakdown with reliability scores]

## Sources and References
[Direct links]

## Recommendations
[Which to use and why]
```

## Integration with Study Guide Creation

### During Excel Drug Chart Creation

When creating Excel drug charts:
1. After reading source file
2. Before creating Tab 1 (Drug Details)
3. **Launch agent for drug class mnemonics**
4. Add "Memory Tricks" row after each drug class table
5. Use mnemonics from agent report
6. Attribute sources in footnote

### During Word Study Guide Creation

When creating Word study guides:
1. After reading source file and template
2. For each learning objective
3. **Launch agent for topic-specific mnemonics**
4. Include mnemonics in learning objective answer section
5. Add to High-Yield Summary tab
6. Attribute sources

### During HTML Guide Creation

When creating HTML guides:
1. After identifying all topics
2. **Launch agent for comprehensive mnemonic list**
3. Add mnemonics to Summary tab
4. Create dedicated "Memory Aids" section
5. Include source links

## Quality Assurance

### Mnemonic Validation Checklist

Before adding mnemonics to study guides, verify:
- ✓ Mnemonic came from agent report (not invented)
- ✓ Source link included
- ✓ Reliability score noted (3+ stars preferred)
- ✓ Acronym/phrase fully explained
- ✓ Medical accuracy verified against source file

### What Gets BLOCKED

❌ Inventing mnemonics without research
❌ Using mnemonics without source attribution
❌ Adding mnemonics that contradict source material
❌ Skipping mnemonic research for study guides

## Enforcement

This skill works with study guide creation workflow:
- **Suggests**: "Use medical-mnemonic-researcher agent for mnemonics"
- **Does not block**: Creation can proceed, but quality may suffer without mnemonics
- **High priority**: Strongly recommended for all study guides

## Examples

### Example 1: HIV Drug Classes

**Trigger:** Creating Excel drug chart for HIV drugs

**Skill activation:**
```
I'll use the medical-mnemonic-researcher agent to find mnemonics for HIV drug classes (NRTIs, NNRTIs, PIs, integrase inhibitors).
```

**Agent searches for:**
- NRTI mnemonic
- NNRTI mnemonic
- Protease inhibitor mnemonic
- Integrase inhibitor mnemonic

**Returns:** Top 3 mnemonics for each class with sources

**Result:** Add to "Memory Tricks" row in drug table

### Example 2: Cranial Nerves

**Trigger:** Creating anatomy study guide

**Skill activation:**
```
I'll use the medical-mnemonic-researcher agent to research cranial nerve mnemonics.
```

**Agent searches for:**
- Cranial nerve names mnemonic
- Cranial nerve functions mnemonic
- Sensory/motor classification mnemonic

**Returns:** Classic mnemonics with reliability scores

**Result:** Add to anatomy learning objective section

### Example 3: Heart Failure Signs

**Trigger:** Creating clinical assessment guide for heart failure

**Skill activation:**
```
I'll use the medical-mnemonic-researcher agent to find mnemonics for heart failure signs and symptoms.
```

**Agent searches for:**
- Left-sided heart failure symptoms
- Right-sided heart failure symptoms
- Decompensated heart failure criteria

**Returns:** Mnemonics for clinical presentations

**Result:** Add to clinical decision tree section

## Troubleshooting

### Agent not launching

**Check:**
- Is medical-mnemonic-researcher.md in `.claude/agents/` directory?
- Is Task tool available?
- Is subagent_type specified correctly?

**Fix:** Verify agent file exists and launch manually

### No mnemonics found

**Agent will report:**
- "No established mnemonics found for [topic]"
- Suggests alternative memory strategies
- Notes to create custom mnemonic but mark as unvalidated

**Action:** Document in study guide: "No established mnemonic found. Create custom memory aid if needed (mark with *)."

### Mnemonics conflict with source

**Agent validates against medical accuracy**

**If conflict found:**
- Agent notes the discrepancy
- Recommends most accurate version
- Warns about outdated mnemonics

**Action:** Prioritize source file accuracy over mnemonic

## Best Practices

1. **Launch agent early** - Before creating study guide content
2. **Research comprehensively** - Ask for multiple related mnemonics in one agent call
3. **Verify accuracy** - Cross-check mnemonics against source material
4. **Attribute sources** - Always include source links
5. **Prefer high-reliability** - Use 4-5 star mnemonics when available
6. **Update when needed** - If agent finds outdated mnemonics, note in study guide

## Progressive Disclosure

**This skill is lightweight:**
- Main instructions: This file (~300 lines)
- Agent file: Loaded only when agent launched
- Deep-dive resources: Loaded on-demand when needed

**Performance:** Agent call takes 30-60 seconds, but provides comprehensive mnemonic research that would take 5-10 minutes manually.

### Deep-Dive Resources

For comprehensive guidance on mnemonic research:

**[Research Methodology](resources/research-methodology.md)** - Detailed guide to the agent's research sources (r/medicalschool, First Aid, SDN), evaluation criteria, and reliability ranking system

**Note:** Resources provide deep-dive into how the agent finds and validates mnemonics. Load when you need to understand the research methodology.

---

**Remember:** The medical-mnemonic-researcher agent is your automation tool for finding PROVEN medical mnemonics. Always use it instead of inventing mnemonics.
