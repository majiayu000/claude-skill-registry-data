---
name: research-prompt
description: >
  Use this skill when the owner wants a ready-to-paste research prompt for a "deep
  research" AI tool (Claude, ChatGPT, Gemini, Perplexity, DeepSeek, or similar) to
  investigate a topic before writing content. Invoke when the user says "give me a
  research prompt for X", "write me a deep research prompt", "I need to research
  this before drafting", or "generate a prompt I can run in ChatGPT/Perplexity for
  research". This produces only the prompt text — it does not run research itself,
  call any external tool, or save results anywhere.
allowed-tools: Read, Write, Bash
argument-hint: "[optional: research topic]"
---

# Research Prompt Generator

You are generating a single, vendor-neutral prompt the owner can paste into the "deep
research" feature of any AI tool they have available (Claude, ChatGPT, Gemini,
Perplexity, DeepSeek, or similar). This skill produces the prompt only — it does not
run research, call any tool or API, or prescribe where the owner saves the result.
Keep it that way: no tool-specific phrasing, no "upload this to context/" instructions
in the generated prompt. Where the owner stores the research report afterward is
entirely up to them.

## Step 0: Recall learnings

If `.claude/learnings.md` exists, read it silently. Apply all entries relevant to this
run. Do not announce this step. If the file is absent, continue normally.

## Step 1: Gather the topic

If `$ARGUMENTS` contains a topic, use it. Otherwise ask:

> "What topic do you want researched?"

Wait for the answer.

## Step 2: Refine scope (optional)

Ask once, offering a sensible default:

> "Any specific angle, sub-questions, or things to exclude — or should I keep it a
> broad, comprehensive overview of [topic]?"

If the owner gives a specific angle or sub-questions, fold them into the prompt as
explicit coverage points. If they say broad/no preference, proceed with a general
comprehensive-overview framing.

## Step 3: Generate the prompt

Produce a single research prompt with this structure:

- Open with a role framing appropriate to the topic (e.g. "You are a research analyst
  investigating...") — do not name or assume any specific AI tool or vendor.
- State the topic and scope clearly, including any sub-questions or exclusions from
  Step 2.
- Ask for a comprehensive, well-structured response using headers to separate major
  areas of coverage.
- Require credible, verifiable sources throughout, with in-text citations.
- Require a formatted source list in APA style at the end.
- Request the output in Markdown, since the owner will save the response as a `.md`
  file.

## Step 4: Present the prompt

Present the generated prompt in a single, clearly delimited copy-paste block:

```
─────────────────────────────────────────────
Research prompt: <topic>
─────────────────────────────────────────────
<the generated prompt text>
─────────────────────────────────────────────
```

Follow it with one line:

> "Paste this into the deep-research feature of whichever AI tool you're using. Save
> the response as Markdown wherever you keep research for this project."

## Step 5: Feedback

**Auto-store phase.** Before asking for feedback, review this run. For each
qualifying observation, append one tagged line to `.claude/learnings.md` (create with
the standard header if missing):

```text
[cc-content:research-prompt] <concise observation> — <YYYY-MM-DD>
```

Qualifies: recurring scope or format preferences not already in context (e.g. "owner
always wants a competitor-landscape sub-section"); corrections the owner made.

Does not qualify: standard behavior applied without deviation; facts already in
context files or `CLAUDE.md`; facts semantically equivalent to an existing
`.claude/learnings.md` entry under any plugin tag — when in doubt, skip.

Check for the file before appending:

```bash
ls .claude/learnings.md 2>/dev/null && echo "exists" || echo "missing"
```

Standard header when creating the file:

```markdown
# Learnings

Corrections and feedback collected during content sessions.
Entries are tagged by skill and dated.

---
```

**Explicit feedback.** After the auto-store phase, ask:

> "Does this prompt cover what you need? Any corrections — or press Enter to finish."

- If the owner **provides a correction**: append it as a tagged entry using the same
  format and qualification criteria above. Confirm: "✓ N learning(s) saved to
  `.claude/learnings.md`."
- If the owner **confirms or skips**: if any entries were auto-stored, confirm
  "✓ N learning(s) auto-saved to `.claude/learnings.md`." Then exit. If nothing was
  stored, exit directly.
