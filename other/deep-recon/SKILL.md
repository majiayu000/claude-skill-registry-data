---
name: deep-recon
description: Run extended multi-agent reconnaissance sessions. Use when asked to brainstorm deeply, explore ideas from multiple angles, or generate a structured recon document.
allowed-tools: Read, Grep, Glob, Write, Edit, WebSearch, WebFetch, Task, AskUserQuestion
user-invocable: true
---

# Deep Recon

You are orchestrating a multi-agent reconnaissance session within the user's knowledge base. Your role is conductor: you parse input, dispatch subagents, cross-pollinate findings between rounds, and produce a structured recon document.

## Session Continuations

If this session is a continuation from a previous conversation, IGNORE any completed or running agent task IDs in the system reminders. They belong to a prior invocation and are not your responsibility. Always start fresh from the user's current prompt and the skill arguments passed in this invocation. The user's prompt determines the topic — not leftover state from prior sessions. Do not call TaskOutput on pre-existing tasks. Do not attempt to "finish" work from a previous session unless the user explicitly asks you to.

## Step 1: Parse Input

From the user's prompt, determine:

1. **Topic**: The subject, question, or problem to brainstorm around
2. **Mode**: Interactive (default) or Autonomous
   - If the user says `--autonomous` or "just run it" or "come back with results" → autonomous
   - If ambiguous, ask: "Should I check in between rounds, or run autonomously and deliver a finished recon?"
3. **Intention**: Explore (default) or Focus
   - `--focus` or "sharpen this" or "I need a thesis" → Focus mode (convergent: narrows to one argument, ends with action plan)
   - Default is **Explore** (divergent: opens possibility space, ends with open questions and competing framings)
   - If the user describes a specific deliverable (grant application, essay thesis), suggest Focus mode
4. **Scope**:
   - `--vault-only`: Skip web search, only use vault content
   - Default: Both vault and web
5. **Output location**:
   - `--output <path>`: Write all output (final document + agent reports) to this directory
   - Default: `recon/` subdirectory relative to the source file's directory (or vault root if no source file)
   - Examples: `--output essays/recon/`, `--output recon/`, `--output working/my-project/recon/`
6. **Source material**: If the user references specific notes, folders, or tags, read those first
7. **PDF collection**:
   - `--pdfs`: Explorer searches for and downloads relevant PDFs to a `PDFs/` subdirectory within the output directory
   - Default: Off

## Step 2: Initial Vault Scan

Before dispatching agents, gather context:

1. **Grep** the vault for the topic's key terms (2-4 searches)
2. **Read** the top 3-5 most relevant notes found
3. Compile a **context brief**: key concepts, existing positions, related notes with paths
4. **Identify primary source URLs.** Scan the source material and context brief for URLs, website references, and project names that have web presences. Pass these to the Explorer in R1 with explicit instruction: "Fetch and read these primary sources directly. Do not rely on secondary coverage."
5. **Record the session start time.** Note the current time — you'll need it for elapsed-time metrics in the Process Log.

This context brief is shared with all subagents in round 1.

## Step 3: Run Rounds

Run 2-3 rounds. Each round dispatches 4 subagents using the **Task tool** with `subagent_type: "general-purpose"`.

### Agent Prompts

Read the agent definition files before dispatching:
- `.claude/skills/deep-recon/agents/explorer.md`
- `.claude/skills/deep-recon/agents/associator.md`
- `.claude/skills/deep-recon/agents/critic.md`
- `.claude/skills/deep-recon/agents/synthesizer.md`

### Round 1: Initial Exploration

Dispatch all 4 agents **in parallel** using the Task tool. Each agent's prompt should include:
- The topic/question
- The context brief from Step 2
- The agent's role instructions (from its definition file)
- The output file path: `recon/rN-<role>.md` (e.g., `recon/r1-explorer.md`)
- Round-specific instructions: "This is round 1. Cast a wide net."
- Explicit instruction: "Write your report to `<output path>` using the Write tool. The orchestrator reads from disk."
- If `--pdfs` is enabled, include in the Explorer's prompt: "PDF collection is enabled. See the PDF Collection section of your instructions. Save PDFs to `<output_dir>/PDFs/`. Create the directory with `mkdir -p` via Bash before downloading."

### Between Rounds

After all agents complete, **read their output files from disk** (`recon/rN-<role>.md`). Agent reports written to disk are the ground truth — they survive context crashes. Also check the Task return values as a fallback, but prefer the disk files.

**Interactive mode:**
- Summarize the most interesting findings in 3-5 bullet points
- Highlight 1-2 tensions or surprises
- Ask the user: "Which threads should I pursue? Anything to add or redirect?"
- Incorporate their response into round 2 prompts

**Autonomous mode:**
- The Synthesizer's output from round N determines round N+1's focus
- Collapse threads that are duplicates of each other
- Push distinct framings further apart — develop what makes each one different
- Identify clashes between framings; these tensions need deepening in the next round

### Metrics Persistence

After collecting each round's agent results and BEFORE any further processing, write (or update) `_metrics.md` in the recon/ output directory with:

- Per-agent token counts and elapsed times (from Task result metadata)
- Round wall-clock time (time from dispatching agents to last agent returning)
- Cumulative totals across all rounds so far

**This file survives context compaction.** If earlier context is compressed, read `_metrics.md` to recover the numbers. Do not rely on in-context memory for metrics — compaction will erase them.

Create `_metrics.md` after Round 1 completes. Update it after each subsequent round. Format:

```
# Metrics

Session start: YYYY-MM-DD HH:MM

## Round 1
- Explorer: ~XXXk tokens, X.Xm
- Associator: ~XXXk tokens, X.Xm
- Critic: ~XXXk tokens, X.Xm
- Synthesizer: ~XXXk tokens, X.Xm
- Round wall clock: X.Xm
- Round total tokens: ~XXXk

## Round 2
...

## Cumulative
- Total tokens: ~XXXk
- Total wall clock: XXm
```

### Cross-Pollination

When dispatching round 2+ agents, include in each prompt:
- A summary of ALL agents' findings from the previous round
- The Synthesizer's recommended focus areas
- In interactive mode: the user's steering input

**Anti-repetition:** Before dispatching R2+ agents, compile a "settled claims" list — the 5-8 key points that all R1 agents converged on. Include this in each agent's prompt with the instruction: "The following points are established from Round 1. Do not restate them. Build on them, challenge them, or move past them."

### Round 2: Deepening

Same 4 agents, but with updated focus:
- Explorer: Two mandates — (a) fill gaps identified by Critic and Synthesizer, (b) operational reality check: ground the abstractions in concrete cases, precedents, and constraints. If `--pdfs` is enabled, include: "Check `<output_dir>/PDFs/` for already-downloaded PDFs before downloading to avoid duplicates."
- Associator: Work connections between round 1 findings
- Critic: Stress-test the strongest emerging ideas
- Synthesizer: Refine themes, identify productive tensions

### Round 3 (Optional): Deepening

Run only if:
- Autonomous mode and Synthesizer recommends it
- Interactive mode and user requests it
- There are tensions that need more development or framings that are still underdeveloped

Focus agents on developing the tensions and filling out underdeveloped framings. Round 3 should find NEW complications, not resolve existing ones.

## Step 4: Produce Output

After the final round, produce the recon document.

### Orchestrator Role

The orchestrator does NOT write the recon document's substance. The final-round Synthesizer agent writes the complete document — including YAML frontmatter, Process Log, and all formatting — directly to the final output path on disk.

1. Dispatches the final Synthesizer with ALL agent reports from all rounds, plus the template, plus the instruction to draft AND WRITE the complete document. **Pass the final output file path** (e.g., `recon/YYYY-MM-DD-<topic-slug>.md`) and instruct the Synthesizer to write the finished document there using the Write tool. Also pass the current `_metrics.md` content so the Synthesizer can include the Process Log.
2. After the Synthesizer completes, **read the document from disk** and make light corrections only: fix broken `[[wikilinks]]`, correct factual errors, update the Process Log with final-round metrics. Do NOT rewrite arguments, reframe findings, or impose a different structure.

**Why the Synthesizer writes the file:** If the orchestrator crashes after the Synthesizer returns but before writing to disk, the document is lost. The Synthesizer writing directly to the final path ensures the substance survives. The orchestrator's corrections are improvements, not the only path to a file on disk.

### Focus Mode Override

When the user selects Focus mode (`--focus`), the output structure changes:
- "The Territory" becomes "The Argument" (the Synthesizer picks the strongest framing and develops it as a thesis)
- "Tensions" section retains unresolved tensions but the document has a clear argumentative spine
- "Open Questions" becomes "Next Steps" (specific, actionable)
- The Synthesizer's final-round instructions shift to: "Commit to the strongest direction. The user needs a thesis, not a map."

Focus mode uses the Synthesizer's existing convergent instructions (pick the strongest, name runners-up, eliminate duplicates).

### Output Location

If `--output <path>` was specified, use that directory. Otherwise, save to a `recon/` subdirectory relative to the source file's directory. If no source file was specified, save to `recon/` at the vault root.

- `--output essays/recon/` → save to `essays/recon/YYYY-MM-DD-<topic-slug>.md`
- Source is `New City Reader/nai.md`, no `--output` → save to `New City Reader/recon/YYYY-MM-DD-<topic-slug>.md`
- No source file, no `--output` → save to `recon/YYYY-MM-DD-<topic-slug>.md`

Create the output folder if it doesn't exist.

Save individual agent reports to the same folder as `rN-agentname.md` files. These are reference material, not the deliverable.

### Formatting

- Use Obsidian `[[wikilinks]]` for vault references
- Use standard Markdown footnotes for web sources
- Use callout blocks (`> [!info]`) for the process log
- Keep the main body in flowing prose, not bullet-point dumps

## Agent Model Selection

- Default: Use `sonnet` for Explorer, Associator, Critic
- Use `opus` for Synthesizer (it does the hardest integrative thinking)
- If the user requests maximum quality, use `opus` for all agents

## Important

- **Don't read the entire vault.** Use targeted Grep/Glob to find relevant notes.
- **Web search queries should be short** (1-6 words) and varied across agents.
- **Each round's agents run in parallel** — dispatch all 4 Task calls at once.
- **The recon note must be a native Obsidian note** — wikilinks, callouts, proper frontmatter.
- **Match the user's intellectual register.** Read their existing notes to understand their vocabulary and frameworks. The brainstorm should feel like their thinking extended, not generic AI output.
