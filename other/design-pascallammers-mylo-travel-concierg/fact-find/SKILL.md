---
name: fact-find
description: Quick lookup of specific facts about Bottlerocket with citations
---

# Fact Find

Fast, focused answers to specific factual questions about Bottlerocket with proper citations.

## Purpose

Quickly find and cite concrete facts about Bottlerocket:
- Configuration values and defaults
- Partition schemes and disk layouts
- Systemd units and targets
- File paths and locations
- Version numbers and dependencies

## When to Use

- Need a specific fact, not an explanation
- Question has a concrete, definitive answer
- Looking for "what is" or "where is" information

For broader questions about architecture or design, use **deep-research** instead.

## Roles

| Role | Reads | Does |
|------|-------|------|
| Orchestrator (you) | SKILL.md | Creates workspace, spawns subagent, returns answer |
| Subagent | phases/FACT-FIND.md | Searches, reads files, writes cited answer |

⚠️ **You do NOT read the phase file** — pass it to the subagent via context_files. The subagent handles all search and file reading, keeping that context out of yours.

## Orchestrator Instructions

```
workspace = "planning/<question-slug>"
mkdir workspace
write workspace/question.txt with the user's question

result = spawn(
    prompt = "Answer the factual question in the workspace.",
    context_files = ["skills/fact-find/phases/FACT-FIND.md"],
    context_data = {"workspace": workspace},
    allow_tools = True
)

read workspace/ANSWER.md
present to user
```

## Inputs

- User's factual question about Bottlerocket

## Outputs

- `workspace/ANSWER.md`: Concise answer with inline citations, sources section, and Research Quality Indicator

## Citation Format

The final answer uses this format:

```markdown
<Answer text with inline citations <sup>[1]</sup>.>

## Sources

<sup>[1]</sup> [`path/to/file.md`](../path/to/file.md)
- What this source provided

---

✅ **Answered from documentation** | ⚠️ **Answered from source code** | 🔍 **Partial documentation**
```

## Validation

A good fact-find response:
- ✓ Directly answers the specific question
- ✓ Concise (2-4 sentences typically)
- ✓ Superscript citations inline
- ✓ Sources section with numbered references
- ✓ Research Quality Indicator at end
- ✓ No unnecessary context or explanation
