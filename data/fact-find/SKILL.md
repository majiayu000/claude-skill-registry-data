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

## Procedure

### 1. Search

Create a focused query with key terms:
```bash
crumbly search "specific terms from question"
```

Check top 3-5 results for relevant files.

### 2. Read

Read the most relevant files to find the answer:
```bash
# Pattern search for targeted reading
grep -n "relevant terms" path/to/file.md

# Full file if needed
cat path/to/file.md
```

### 3. If Documentation Is Insufficient

Crumbly indexes documentation, not source code. If you can't find the answer in docs, search the codebase directly:

```bash
# IMPORTANT: Always scope searches to specific directories!
# The forest is 80GB+ - unscoped searches will hang.
rg "search_term" --type rust bottlerocket/sources/
find bottlerocket/sources -name "*relevant_name*"
```

This indicates a documentation gap - note it in your Research Quality Indicator.

### 4. Answer with Citations

Provide a direct, concise answer with inline superscript citations and a Sources section:

```
Bottlerocket uses a dual partition scheme with sets A and B <sup>[1]</sup>. The default API socket is `/run/api.sock` <sup>[2]</sup>.

## Sources

<sup>[1]</sup> [`sources/updater/signpost/README.md`](../sources/updater/signpost/README.md)
- Partition set structure

<sup>[2]</sup> [`sources/api/README.md`](../sources/api/README.md)
- API socket configuration
```

**Citation guidelines:**
- Use `<sup>[1]</sup>`, `<sup>[2]</sup>`, etc. inline with facts
- Paths relative to the target repository
- Markdown links for file paths
- GitHub URLs for cross-repo references: `https://github.com/bottlerocket-os/REPO/blob/develop/FILE.md`
- Brief bullet points describing what each source provided

## Validation

A good fact-find response:
- ✓ Directly answers the specific question
- ✓ Concise (2-4 sentences typically)
- ✓ Superscript citations inline
- ✓ Sources section with numbered references
- ✓ No unnecessary context or explanation

## Research Quality Indicator

End your response with:

- ✅ **Answered from documentation** - Found in README files, design docs, or narrative documentation.
- ⚠️ **Answered from source code** - Had to read implementation files due to insufficient documentation.
- 🔍 **Partial documentation** - Required both docs and source code to answer fully.
