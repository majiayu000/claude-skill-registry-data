---
name: context-setter
description: Generate comprehensive context-setting markdown files for coding tasks by intelligently exploring codebase and structuring work with ROLE, CONSTRAINTS, STYLE, file reading order, and structured tasks. Use proactively when the user is starting a complex dev task requiring multiple steps or file reads.
---

# Context Setter Skill

Creates context-setting markdown files that transform vague user requests into comprehensive, structured prompts for coding tasks. Output files follow proven patterns: ROLE definition, CONSTRAINTS (locked decisions), STYLE guidelines, ordered file reading lists, and numbered tasks with clear deliverables.

**Primary use:** Extract and sequence constraints from existing docs (PRDs, AGENTS.md, specs) into executable task structure. **Secondary use:** When docs don't exist, explore codebase and ask clarifying questions to build structure from scratch

## How to Use

Once the context file is generated, start a fresh Claude Code conversation and reference the file in your first message:

```
Read /path/to/context-file.md and execute the tasks
```

This gives Claude a clean context window with all necessary structure, constraints, and task sequencing upfront.

---

## Process

### Phase 1: Understand User Intent

**Clarify vague requests** - If user provides rough/unclear prompt, ask:
- What are you trying to build/fix/test?
- Any specific constraints or locked decisions?
- Testing requirements (manual/automated/verifiable)?
- Key deliverables expected?
- Timeframe or urgency?

**Identify scope:**
- New feature development
- Bug fix with verification
- Infrastructure/deployment setup
- Documentation/testing task
- Integration work

### Phase 2: Explore Codebase Intelligently

**File Discovery Priority:**
1. `AGENTS.md` / `CLAUDE.md` - project guidelines and conventions
2. `README.md` - project overview and setup
3. `workings/prds/` or `workings/*.md` - product requirements documents
4. Relevant source code - based on user's task domain
5. `tests/` folder - patterns for verification and testing approach
6. Config files - deployment, environment, build configs
7. Related context-setting files in `workings/context-setting/`

**Search Strategy:**
- Use Glob for broad pattern matching (`**/*.md`, `**/tests/**`, `src/**/*.ts`)
- Use Grep for content search (function names, error patterns, config keys)
- Read key files to understand constraints, conventions, dependencies
- Use Task tool with Explore agent for complex codebase exploration

**Extract from codebase:**
- Locked decisions/constraints → CONSTRAINTS section
- Coding style patterns, tone → STYLE section
- Testing patterns and verification approach → for TASK sections
- File dependencies and reading order → ORDER OF FILES section
- Key technologies, frameworks, APIs → context for ROLE and TASKS

### Phase 3: Generate Context Document

**Document Structure Template:**

```markdown
# ROLE

[Single line: persona + responsibility for this specific task]

## MISSION

[2-4 sentence non-technical sketch of what you're building/fixing and why]
[Answer: What's the goal? What's already done? What needs doing?]
[Keep it lean - business/user value, not implementation details]

## CONSTRAINTS

[Numbered list of locked decisions, constraints, specs that must not change]
[Source these from AGENTS.md, PRDs, existing specs - never invent]

## STYLE

British English. Concise, shippable. When proposing edits: filename + bullets (+ line numbers if needed).
[Add task-specific style notes if relevant]
Never invent spec; if missing, mark "out of scope for v0.1".

## ORDER OF FILES (read in this order)

1) [absolute path to first file]
2) [absolute path to second file]
...

## TASK 1 — [Clear task name]

[Clear objective with specific deliverables]
[Sub-steps if complex, each actionable]
[Expected output format if relevant]

## TASK 2 — [Next task name]

[Continue sequential tasks...]

[Include testing/verification tasks if code changes involved]

## OUTPUT FORMAT

[Specify expected format: compact results, bullets, pass/fail tables, fixture contents, etc.]
[Set expectation for verbosity - "compact", "exact contents", "no extra prose"]

---

## P.S. Meta Notes

[2-4 sentences explaining key decisions made while structuring this context doc]
[Surface interesting tradeoffs, assumptions, or reasoning about task sequencing/scope]
[Examples: why certain files are prioritized, why tasks are ordered this way, what's intentionally deferred]
[Think: what would the user find valuable to know about how you approached this? Especially if they skim read the document.]
```

**Section Guidelines:**

**ROLE:**
- Single line defining persona + responsibility
- Examples: "You are the Lead Engineer for Cloudflare Workers deployment", "You are the Product Owner × Lead Engineer for Symbient PubStack"
- Make it specific to the task at hand

**MISSION:**
- 2-4 sentences, non-technical sketch
- Answer: What's the goal? What's already done? What needs doing?
- Focus on business/user value, not implementation details
- Keep it lean and clear for handoffs

**CONSTRAINTS:**
- Numbered list (1, 2, 3...)
- Extract from existing docs (AGENTS.md, PRDs, specs)
- Include locked decisions, constraints, key specs
- Examples: "ULID id", "HMAC replay window 300s", "2 MB binary limit"
- **Never invent** - only source from existing documentation
- If constraints missing, note in STYLE to mark "out of scope for v0.1"

**STYLE:**
- Always start with: "British English. Concise, shippable. When proposing edits: filename + bullets (+ line numbers if needed)."
- Add: "Never invent spec; if missing, mark 'out of scope for v0.1'."
- Include any task-specific communication preferences

**ORDER OF FILES:**
- Numbered list with **absolute paths** (never relative)
- Prioritize: guidelines → specs/PRDs → source code → tests → configs
- Include only files directly relevant to the task
- Use format: `1) /absolute/path/to/file.md`

**TASKS:**
- Number sequentially: TASK 1, TASK 2, TASK 3...
- Use format: `TASK N — [Clear descriptive name]`
- Each task should have:
  - Clear objective (what to achieve)
  - Specific deliverables (what to produce)
  - Sub-steps if complex (numbered or bulleted)
  - Expected output format if relevant
- Include verification/testing tasks if code changes involved
- Make tasks sequential and buildable (each task can reference previous)

**OUTPUT FORMAT:**
- Specify how results should be presented
- Examples: "compact result", "PASS/FAIL per sample", "fixture filenames + exact contents"
- Set verbosity expectation: "no extra prose", "bullets only", "with line numbers"

### Phase 4: Create and Save File

**Filename Convention:**
`keyword-keyword-keyword.md`

**Filename creation:**
- Derive from task description (3-5 keywords)
- Lowercase, hyphen-separated
- Descriptive of the actual work, not generic placeholders
- Examples: `cloudflare-mailbox-mcp-handshake.md`, `pubstack-core-system-build.md`, `digit-export-implementation.md`

**Save Location:**
`/workspace/project/workings/context-setting/`

**After saving:**
1. Output the **full absolute path** to the file (so user can click to open)
2. Provide brief summary (2-3 sentences) of what was generated
3. Confirm next steps if relevant

---

## Example Outputs

### Example 1: Infrastructure Setup Task

**User prompt:** "setup cloudflare worker with secure handshake from mcp server, add logging"

**Generated context file:**

```markdown
# ROLE

You are the DevOps Engineer for Cloudflare Workers deployment and observability.

## MISSION

Build secure MCP server integration with Cloudflare Workers mailbox. MCP servers (running in Claude/ChatGPT) need to post events to our Worker using HMAC authentication. Worker already validates and writes to GitHub - we need the MCP side implemented with proper handshake and observability via Workers Logs.

## CONSTRAINTS

1) HMAC-SHA256 handshake for secure MCP → Worker communication
2) 300s replay window for request validation
3) 2 MB binary payload limit
4) console.log statements visible in Workers Logs
5) Environment vars via wrangler.toml or dashboard secrets

## STYLE

British English. Concise, shippable. When proposing edits: filename + bullets.
Never invent spec; if missing, mark "out of scope for v0.1".

## ORDER OF FILES (read in this order)

1) /workspace/project/AGENTS.md
2) /workspace/project/workings/mailbox-brief-v01.md
3) /workspace/project/README.md
4) /workspace/project/tests/
5) https://developers.cloudflare.com/workers/observability/logs/workers-logs/

## TASK 1 — Implement HMAC handshake validation

Add request signature verification:
- Extract signature from Authorization header
- Compute HMAC-SHA256 of request body with shared secret
- Validate timestamp within 300s window
- Return 401 if validation fails
- Return 200 with {status: "authorized"} if valid

## TASK 2 — Setup Cloudflare Workers Logs

Configure logging per Cloudflare docs:
- Enable Workers Logs in dashboard
- Add strategic console.log statements for debugging
- Test that logs appear in real-time stream
- Document log access for team

## TASK 3 — Test handshake locally

Create test script:
- Generate valid HMAC signatures
- Test replay window enforcement
- Verify 401 responses for invalid signatures
- Verify 200 responses for valid requests

## OUTPUT FORMAT

Compact results. For each task, confirm completion with:
- Filename + line numbers for code changes
- Test results (PASS/FAIL)
- Log output samples

---

## P.S. Meta Notes

[2-4 sentences explaining key decisions made while structuring this context doc]
[Surface interesting tradeoffs, assumptions, or reasoning about task sequencing/scope]
[Examples: why certain files are prioritized, why tasks are ordered this way, what's intentionally deferred]
[Think: what would the user find valuable to know about how you approached this?]
```

### Example 2: Feature Development Task

**User prompt:** "build the digit export, N=50 latest public posts, SHA-256 etag"

**Generated context file:**

```markdown
# ROLE

You are the Lead Engineer for Symbient Digit export API.

## MISSION

Build a public JSON export of the latest 50 posts for consumption by external apps. Posts are stored as markdown files with front matter - we need to filter public-only, extract clean text (stripping code/quotes), and serve with proper ETag caching. This powers the "what's new" feed for subscribers.

## CONSTRAINTS

1) N=50 latest public-visibility posts only
2) ETag = SHA-256 hash of JSON response body
3) Monotonic `updated` timestamp field required
4) Self-authored permalink fallback if in_reply_to null
5) Text extraction drops fenced code blocks and `> @` quote lines

## STYLE

British English. Concise, shippable. When proposing edits: filename + bullets.
Never invent spec; if missing, mark "out of scope for v0.1".

## ORDER OF FILES (read in this order)

1) /workspace/project/AGENTS.md
2) /workspace/project/workings/digits-v0.1-prd.md
3) /workspace/project/src/

## TASK 1 — Query latest N=50 public posts

Implement query logic:
- Filter by front matter `visibility: public`
- Sort by filename timestamp DESC
- Limit to 50 results
- Return array of post objects

## TASK 2 — Generate Digit JSON format

Transform each post to Digit schema:
- Extract title, body, permalink
- Strip fenced code (```...```) and quote lines (> @...)
- Add monotonic `updated` timestamp
- Use self-authored permalink if no in_reply_to

## TASK 3 — Compute SHA-256 ETag

Hash the JSON response:
- Serialize JSON deterministically
- Compute SHA-256 hash
- Return in ETag header as `sha256:[hash]`

## TASK 4 — Verifiable test

Create test:
- Generate 60 posts (30 public, 30 private)
- Verify export returns exactly 50 public posts
- Verify ETag matches SHA-256 of response
- Verify text extraction drops code/quotes correctly

## OUTPUT FORMAT

For each task:
- Filename + line numbers for implementation
- Test output showing PASS/FAIL
- Sample JSON response (first 2 Digits)

---

## P.S. Meta Notes

[2-4 sentences explaining key decisions made while structuring this context doc]
[Surface interesting tradeoffs, assumptions, or reasoning about task sequencing/scope]
[Examples: why certain files are prioritized, why tasks are ordered this way, what's intentionally deferred]
[Think: what would the user find valuable to know about how you approached this?]
```

---

## Validation Checklist

Before saving context file, verify:

- [ ] ROLE is single line, task-specific persona
- [ ] MISSION is 2-4 sentences, non-technical sketch of the goal
- [ ] CONSTRAINTS items sourced from existing docs (not invented)
- [ ] STYLE includes British English + "never invent spec" guidance
- [ ] ORDER OF FILES uses absolute paths, numbered
- [ ] TASKS are sequential, numbered, with clear deliverables
- [ ] Testing/verification included if code changes involved
- [ ] OUTPUT FORMAT specifies expected verbosity/format
- [ ] Filename follows `keyword-keyword-keyword.md` pattern (3-5 descriptive keywords)
- [ ] File will be saved to `workings/context-setting/`
- [ ] P.S. section included with meta-guidance on prompt structure

---

## Important Notes

- **Always use absolute paths** for ORDER OF FILES section
- **Never invent CONSTRAINTS items** - source from existing docs or omit
- **Include testing tasks** for any code changes (verifiable testing required)
- **Keep OUTPUT FORMAT realistic** - match to task complexity
- **Save file and display clickable path** in conversation
- **Ask clarifying questions** if user request is too vague to structure properly
- **Use Explore agent** for complex codebase exploration needs
- **Always append P.S. section** at end of generated context files with meta-guidance
