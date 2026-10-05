---
name: lesson-quiz
version: 1.0.0
description: Interactive lesson-level quiz for Claude Code tutorials. Tests understanding of a specific lesson (01-10) with 8-10 questions mixing conceptual and practical knowledge. Use before a lesson to pre-test, during to check progress, or after to verify mastery. Use when asked to "quiz me on hooks", "test my knowledge of lesson 3", "lesson quiz", "practice quiz for MCP", or "do I understand skills".
---

# Lesson Quiz

Interactive quiz that tests understanding of a specific Claude Code lesson with 8-10 questions, provides per-question feedback, and identifies areas to review.

## Instructions

### Step 1: Determine the Lesson

If the user provided a lesson as an argument (e.g., `/lesson-quiz hooks` or `/lesson-quiz 03`), map it to the lesson directory:

**Lesson mapping:**
- `01`, `slash-commands`, `commands` → 01-slash-commands
- `02`, `memory` → 02-memory
- `03`, `skills` → 03-skills
- `04`, `subagents`, `agents` → 04-subagents
- `05`, `mcp` → 05-mcp
- `06`, `hooks` → 06-hooks
- `07`, `plugins` → 07-plugins
- `08`, `checkpoints`, `checkpoint` → 08-checkpoints
- `09`, `advanced`, `advanced-features` → 09-advanced-features
- `10`, `cli` → 10-cli

If no argument was provided, present a selection prompt using AskUserQuestion:

**Question 1** (header: "Lesson"):
"Which lesson do you want to quiz on?"
Options:
1. "Slash Commands (01)" — Custom commands, skills, frontmatter, arguments
2. "Memory (02)" — CLAUDE.md, memory hierarchy, rules, auto memory
3. "Skills (03)" — Progressive disclosure, auto-invocation, SKILL.md
4. "Subagents (04)" — Task delegation, agent config, isolation

**Question 2** (header: "Lesson"):
"Which lesson do you want to quiz on? (continued)"
Options:
1. "MCP (05)" — External integration, transport, servers, tool search
2. "Hooks (06)" — Event automation, PreToolUse, exit codes, JSON I/O
3. "Plugins (07)" — Bundled solutions, marketplace, plugin.json
4. "More lessons..." — Checkpoints, Advanced Features, CLI

If "More lessons..." is selected, present:

**Question 3** (header: "Lesson"):
"Select your lesson:"
Options:
1. "Checkpoints (08)" — Rewind, restore, safe experimentation
2. "Advanced Features (09)" — Planning, permissions, print mode, thinking
3. "CLI Reference (10)" — Flags, output formats, scripting, piping

### Step 2: Read the Lesson Content

Read the lesson README.md file to refresh context:
- Read file: `<lesson-directory>/README.md`

Then use the question bank from `references/question-bank.md` for that lesson. The question bank provides 10 pre-written questions per lesson with correct answers and explanations.

### Step 3: Present the Quiz

Ask the user about quiz timing context:

Use AskUserQuestion (header: "Timing"):
"When are you taking this quiz relative to the lesson?"
Options:
1. "Before (pre-test)" — I haven't read the lesson yet, testing my prior knowledge
2. "During (progress check)" — I'm partway through the lesson
3. "After (mastery check)" — I've completed the lesson and want to verify understanding

This context affects how the results are framed (see Step 5).

### Step 4: Present Questions in Rounds

Present 10 questions from the question bank in rounds of 2 questions each (5 rounds total). Each question uses AskUserQuestion with the question text and 3-4 answer options.

**IMPORTANT**: Use AskUserQuestion with max 4 options per question, 2 questions per round.

For each round, present 2 questions. After all 5 rounds, proceed to scoring.

**Question format per round:**

Each question from the question bank has:
- `question`: The question text
- `options`: 3-4 answer choices (one correct, labeled in the bank)
- `correct`: The correct answer label
- `explanation`: Why the answer is correct
- `category`: "conceptual" or "practical"

Present each question using AskUserQuestion. Record the user's answer for each.

### Step 5: Score and Present Results

After all rounds, calculate the score and present results.

**Scoring:**
- Each correct answer = 1 point
- Total possible = 10 points

**Grade scale:**
- 9-10: Mastered — Excellent understanding
- 7-8: Proficient — Good grasp, minor gaps
- 5-6: Developing — Fundamentals understood, needs review
- 3-4: Beginning — Significant gaps, review recommended
- 0-2: Not yet — Start from the beginning of this lesson

**Output format:**

```markdown
## Lesson Quiz Results: [Lesson Name]

**Score: N/10** — [Grade label]
**Quiz timing**: [Before / During / After] the lesson
**Question breakdown**: N conceptual correct, N practical correct

### Per-Question Results

| # | Category | Question (short) | Your Answer | Result |
|---|----------|-----------------|-------------|--------|
| 1 | Conceptual | [abbreviated question] | [their answer] | [Correct / Incorrect] |
| 2 | Practical | ... | ... | ... |
| ... | ... | ... | ... | ... |

### Incorrect Answers — Review These

[For each incorrect answer, show:]

**Q[N]: [Full question text]**
- Your answer: [what they chose]
- Correct answer: [correct option]
- Explanation: [why it's correct]
- Review: [specific section of the lesson README to re-read]

### [Timing-specific message]

[If pre-test]:
**Pre-test score: N/10.** This gives you a baseline! Focus your study on the topics you missed. After completing the lesson, retake the quiz to measure your improvement.

[If during]:
**Progress check: N/10.** [If 7+: Great progress — keep going! If 4-6: Review the incorrect topics before continuing. If <4: Consider re-reading from the beginning.]

[If after]:
**Mastery check: N/10.** [If 9-10: You've mastered this lesson! Move on to the next. If 7-8: Almost there — review the missed topics and retake. If <7: Spend more time with the lesson, especially the sections marked above.]

### Recommended Next Steps

[Based on score and timing:]
- [If mastered]: Proceed to the next lesson in the roadmap: [next lesson link]
- [If proficient]: Review these specific sections, then retake: [list sections]
- [If developing or below]: Re-read the full lesson: [lesson link]. Focus on: [list weak categories]
- [Offer]: "Would you like to retake this quiz, try a different lesson, or get help with a specific topic?"
```

### Step 6: Offer Follow-up

After presenting results, use AskUserQuestion:

"What would you like to do next?"
Options:
1. "Retake this quiz" — Try the same lesson quiz again
2. "Quiz another lesson" — Switch to a different lesson
3. "Explain a topic I missed" — Get a detailed explanation of an incorrect answer
4. "Done" — End the quiz session

If **Retake**: Go back to Step 4 (skip timing question, use same timing).
If **Quiz another lesson**: Go back to Step 1.
If **Explain a topic**: Ask which question number, then read the relevant section from the lesson README.md and explain it with examples.

## Error Handling

### Invalid lesson argument
If the argument doesn't match any lesson, show the valid lesson list and ask the user to pick one.

### User wants to quit mid-quiz
If the user indicates they want to stop during any round, present partial results for questions answered so far.

### Lesson README not found
If the README.md file doesn't exist at the expected path, inform the user and suggest checking the repository structure.

## Validation

### Triggering test suite

**Should trigger:**
- "quiz me on hooks"
- "lesson quiz"
- "test my knowledge of lesson 3"
- "practice quiz for MCP"
- "do I understand skills"
- "quiz me on slash commands"
- "lesson-quiz 06"
- "test me on checkpoints"
- "how well do I know the CLI"
- "quiz me before I start the memory lesson"

**Should NOT trigger:**
- "assess my overall level" (use /self-assessment)
- "explain hooks to me"
- "create a hook"
- "what is MCP"
- "review my code"
