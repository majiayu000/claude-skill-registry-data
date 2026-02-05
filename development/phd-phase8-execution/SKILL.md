---
name: phd-phase8-execution
description: Execute PhD Pipeline Phase 8 using Claude Code Task tool with dynamic agents per chapter
version: 1.0.0
category: research
tags:
  - phd
  - pipeline
  - research
  - dissertation
  - phase8
  - claudeflow
author: Claude Flow
---

# PhD Phase 8 Execution - Claude Code Task Tool Integration

## Overview

This skill executes Phase 8 (Final Paper Assembly) of the PhD Pipeline using Claude Code's Task tool. Unlike the basic concatenation approach, this uses **DYNAMIC specialized agents per chapter** from the dissertation-architect structure, following ClaudeFlow methodology.

## Prerequisites

Before using this skill, Phase 8 must be prepared using:

```bash
npx tsx src/god-agent/cli/phd-cli.ts finalize --slug <your-slug> --prepare-for-claude-code
```

This generates `phase8-prompts.json` in the research directory with:
- 4-part ClaudeFlow prompts for each chapter
- Dynamic agent assignment per chapter
- Execution instructions

## ClaudeFlow Methodology

Per `/docs2/claudeflow.md`:

1. **99.9% Sequential Execution**: Chapters MUST be processed one at a time
2. **4-Part Prompt Pattern**: YOUR TASK, WORKFLOW CONTEXT, MEMORY RETRIEVAL, MEMORY STORAGE
3. **Dynamic Agent Assignment**: Each chapter uses its specialized agent from dissertation-architect

## Execution Workflow

### Step 1: Read Prepared Prompts

```javascript
// Read the phase8-prompts.json file
const promptsFile = await Read(`docs/research/${slug}/phase8-prompts.json`);
const phase8Data = JSON.parse(promptsFile);
```

### Step 2: Execute Chapters SEQUENTIALLY

For each chapter in `phase8Data.chapterPrompts`:

```javascript
// SEQUENTIAL execution - one chapter at a time
for (const chapter of phase8Data.chapterPrompts) {
  // Use Task tool with DYNAMIC agent from dissertation-architect
  await Task({
    subagent_type: chapter.subagentType,  // e.g., 'introduction-writer', 'literature-review-writer'
    prompt: chapter.prompt,                // 4-part ClaudeFlow prompt
    description: `Write Chapter ${chapter.chapterNumber}: ${chapter.chapterTitle}`
  });

  // Verify chapter was written
  const exists = await fileExists(chapter.outputPath);
  if (!exists) {
    throw new Error(`Chapter ${chapter.chapterNumber} was not written to ${chapter.outputPath}`);
  }

  // Store progress to memory
  await memoryStore(
    `chapter/${chapter.chapterNumber}/completed`,
    { completedAt: new Date().toISOString(), wordCount: getWordCount(chapter.outputPath) },
    phase8Data.memoryNamespace
  );
}
```

### Step 3: Combine Final Paper

After all chapters complete:

```javascript
// Spawn final-combiner agent to assemble complete paper
await Task({
  subagent_type: 'final-combiner',
  prompt: `Combine all chapters from ${phase8Data.finalOutputDir} into a complete paper`,
  description: 'Combine chapters into final paper'
});
```

## Dynamic Agent Mapping

Agents are assigned DYNAMICALLY per research project from the `05-dissertation-architect.md` structure:

| Chapter Type | Example Agent |
|-------------|---------------|
| Introduction | introduction-writer |
| Literature Review | literature-review-writer |
| Methodology | methodology-writer |
| Technical Chapters | technical-writer-* |
| Cost Analysis | cost-analyst-writer |
| Implementation | implementation-writer |
| Conclusion | conclusion-writer |
| Appendices | appendix-writer |

**IMPORTANT**: These are examples only. The actual agents are read dynamically from the dissertation structure file for each research project.

## Memory Namespace

All Phase 8 operations use namespace: `phd/{slug}/phase8`

Key memory paths:
- `chapter/{n}/completed`: Chapter completion state
- `chapter/{n}/wordCount`: Word count for chapter
- `synthesis/progress`: Overall synthesis progress
- `final/assembled`: Final paper assembly state

## Error Handling

1. If a chapter fails to write, retry with the same agent once
2. If retry fails, store error state and continue with next chapter
3. After all chapters, report which ones failed
4. Failed chapters can be re-run individually

## Manual Invocation

To manually execute Phase 8 for a research project:

```bash
# Step 1: Prepare prompts (generates phase8-prompts.json)
npx tsx src/god-agent/cli/phd-cli.ts finalize --slug your-research-slug --prepare-for-claude-code

# Step 2: In Claude Code, execute the skill
# Claude will read phase8-prompts.json and spawn agents sequentially
```

## Verification

After execution, verify:
1. All chapters exist in `docs/research/{slug}/final/chapters/`
2. Each chapter has proper word count (from prompts)
3. All citations are properly formatted
4. Memory has completion state for all chapters
