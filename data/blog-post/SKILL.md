---
name: blog-post
description: Complete workflow for creating blog posts - from research to publication-ready draft. Handles research generation, draft creation, and style review. Use with "/blog-post <topic>" or "/blog-post --from-research <path>".
---

# Blog Post Creation Workflow

## Purpose
Streamline the daily blog post creation process by automating research, drafting, and style review in a single command.

## Usage Modes

### Mode 1: Start from scratch with a topic
```
/blog-post "CPU Scheduling in Hypervisors"
/blog-post "Database Connection Pools" --category infra --tags db,performance,connections
```

This will:
1. Run deep-dive research using `docs/deep_dive_prompt.md`
2. Save research to `_research/` directory
3. Generate blog post draft following style guide
4. Review against `blog-post-style-guide.md`
5. Create final file in `_posts/` with proper naming

### Mode 2: From existing research document
```
/blog-post --from-research _research/physical-virtual-foundations/03-physical-virtual-foundations-CPU.md
/blog-post --from-research _research/programming/01-distributed-programming-IBLT.md --series "Distributed Programming"
```

This will:
1. Read the research document
2. Generate blog post draft following style guide
3. Review against `blog-post-style-guide.md`
4. Create final file in `_posts/` with proper naming

## Workflow Steps

### Step 0: Setup & Context Gathering

**ALWAYS start with:**
1. **Create todos using TodoWrite** - Track all workflow steps, mark in_progress/completed as you work
2. **Read 2-3 recent posts** from `_posts/` to match current voice and patterns
3. **Check for series** - If topic matches existing series (grep titles), use series format
4. **Sequential numbering** - For research files: `ls _research/<category>/ | sort -n | tail -1` to get next number
5. **Validate research path** (Mode 2) - Ensure file exists before proceeding

### Step 1: Research Phase (Mode 1 only)

**If starting from topic:**
1. Read `docs/deep_dive_prompt.md`
2. Use the prompt structure to conduct deep research on the topic
3. Create comprehensive research document in `_research/` directory
4. Organize under appropriate subdirectory (infra, programming, systems, etc.)
5. Save as `_research/<category>/<number>-<topic-slug>.md`

**Quality gate - Research must have:**
- All 8 sections from deep_dive_prompt (Mental Model, Failure Modes, Tradeoffs, Socratic Questions, Lifecycle, Experiments, Red Flags, Operator Truths)
- At least 5 concrete failure modes
- 10 Socratic questions (unanswered)
- Real examples, not hypotheticals

**If from existing research:**
1. Read the provided research document path
2. Validate it exists and has content (if not, show available files in `_research/`)
3. Skip to drafting phase

### Step 2: Draft Generation

**CRITICAL: Transform, don't copy!**
- Blog = 30-40% of research length (800-1500 words max)
- NEVER copy entire research sections verbatim
- Extract 2-3 key insights, not everything
- Add first-person narrative that research lacks ("As I explored...", "I was surprised to find...")
- Pick 1-2 failure modes → inline examples with real commands
- Socratic questions → DO NOT include directly, use to shape narrative flow
- Operator truths → Final Thoughts section

**Content Transformation:**
- **Extract key insights** from research that match blog philosophy (personal learning, operational focus)
- **Distill complexity** - research is comprehensive, blog is focused and digestible
- **Add personal voice** - first-person, conversational, "I found myself learning..."
- **Focus on "why it matters"** - connect theory to practice for software engineers
- **Include concrete examples** - real commands, outputs, scenarios

**Structure Requirements:**
1. **Front matter** - Generate based on topic and user-provided options:
   ```yaml
   ---
   title: "<Series Name - Specific Topic>" or "<Standalone Topic>"
   date: <today's date in YYYY-MM-DD HH:MM:SS -0500>
   categories: <programming|infra|ai>
   tags: [ <3-6 relevant tags> ]
   ---
   ```
   - CRITICAL: Date must be today or earlier, NEVER a future date
   - Ask user for series name if ambiguous
   - Suggest category and tags based on content

2. **Opening (1-2 sentences)** - Personal context, direct and concise:
   - Jump to what sparked interest
   - No verbose setup
   - Examples from existing posts show this pattern

3. **Main sections with ## and ### headings**:
   - Start with concept definition
   - Include "Why should software engineers care?" section
   - Use question-based headers when appropriate
   - Progress simple → complex

4. **Examples and visuals**:
   - Real command outputs (not hypotheticals)
   - ASCII diagrams for architecture
   - Code blocks with language specifiers
   - **Citations required**: All concrete numbers (latency, throughput, %, multipliers) MUST cite source (Intel docs, AWS specs, etc.) OR use qualitative ("significantly faster" instead of "2x")

5. **Final Thoughts (optional but recommended)**:
   - Synthesize learnings
   - Connect to broader applications
   - Pose implications

**Voice Requirements (from style guide):**
- First-person perspective ("I", "we")
- Conversational without sacrificing accuracy
- Avoid overloaded adjectives ("very", "highly", "incredibly", "remarkably")
- No AI-sounding intensifiers
- Trust technical content to speak for itself
- Use concrete details over vague praise

**Quality gate - Draft must have:**
- Word count 800-1500 (concise, not research republished)
- Opening 1-2 sentences max
- "Why should software engineers care?" section exists
- At least one concrete example or command output
- No future dates in front matter
- First-person voice throughout ("I", "we", "As I learned...")

### Step 3: Style Review

Review the draft against `.claude/blog-post-style-guide.md`:

**Check:**
- [ ] Front matter complete and properly formatted
- [ ] Date is not in the future
- [ ] Opening is concise (1-2 sentences)
- [ ] Main concept defined early
- [ ] "Why should software engineers care?" addressed
- [ ] Technical terms defined on first use
- [ ] Examples use real commands/outputs
- [ ] Visuals are clean and readable
- [ ] Actionable takeaways provided
- [ ] Tone is conversational and first-person
- [ ] No overloaded adjectives or intensifiers
- [ ] Concrete numbers cite sources OR use qualitative descriptions
- [ ] Logical flow from simple to complex

**Provide:**
1. List of issues found (if any)
2. Suggested fixes for each issue
3. Revised sections for critical problems
4. Overall assessment: "Ready to publish" or "Needs revision"

**If issues found:**
- Auto-fix minor issues: AI intensifiers, missing citations (convert to qualitative), formatting
- For critical issues (missing sections, wrong voice): Show before/after, apply fixes
- Re-run style review after fixes (max 2 iterations)
- Only ask user for major structural decisions

### Step 4: File Creation

**Filename format:** `YYYY-MM-DD-topic-slug.md`
- Use today's date
- Convert topic to lowercase kebab-case
- Example: `2026-01-03-cpu-scheduling-hypervisors.md`

**Location:** `_posts/`

**Before saving:**
- Check if file exists → Ask: "Overwrite, save as new (-v2), or cancel?"
- Validate filename format and date

**Final output:**
1. Save the reviewed and polished draft to `_posts/<filename>`
2. Show summary: file path, word count, series (if applicable)
3. Ask next step: "Preview locally? Commit to git? Review file? Done?"

## User Interaction

**Ask for clarification when:**
- Category is ambiguous (suggest based on content)
- Tags are unclear (suggest 3-6 relevant tags)
- Series name is needed but not provided
- Topic is too broad (suggest narrowing)
- Research document path doesn't exist

**Provide feedback:**
- "Research phase complete - saved to `_research/...`"
- "Draft generated - reviewing against style guide..."
- "Style review complete - found X issues"
- "Blog post created: `_posts/YYYY-MM-DD-topic.md`"

## Critical Rules

1. **Transform, don't republish** - Blog is 30-40% of research length with personal narrative added
2. **Quality gates** - Validate research completeness, draft word count, voice consistency
3. **Voice matching** - Read recent posts before drafting, match established patterns
4. **Citations** - All numbers cite sources OR use qualitative descriptions
5. **Auto-fix** - Apply minor fixes automatically, iterate max 2 times
6. **Error handling** - Validate paths, check file existence, ask before overwriting
7. **Todo tracking** - Use TodoWrite from start, mark completed immediately after each step

## Example Interactions

### Example 1: From scratch
```
User: /blog-post "Memory Balloon Drivers"

Assistant: Starting research phase on "Memory Balloon Drivers"...
[Creates research document]
Research complete: _research/infra/04-memory-balloon-drivers.md

Generating blog post draft...
Style review complete - 2 minor issues found
Blog post created: _posts/2026-01-03-memory-balloon-drivers.md
```

### Example 2: From existing research
```
User: /blog-post --from-research _research/infra/03-cpu-scheduling.md --series "Physical Virtual Foundations"

Assistant: Reading research document...
Generating blog post draft following "Physical Virtual Foundations" series pattern...
Style review complete - ready to publish
Blog post created: _posts/2026-01-03-physical-virtual-foundations-cpu-scheduling.md
```
