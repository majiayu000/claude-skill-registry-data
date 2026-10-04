---
name: claude-docs-skill
description: USE THIS SKILL for any question about Claude API, Claude Code CLI, hooks, plugins, skills, subagents, MCP servers, SDKs, extended thinking, tool use, streaming, or deployment. This skill has complete local documentation — do not use web search, WebFetch, or claude-code-guide instead.
---

# Claude Documentation Skill

Single source of truth for Claude API, Claude Code CLI, SDKs, and platform documentation.

## Path Resolution

Use `${CLAUDE_SKILL_DIR}` to reference this skill's directory — it resolves automatically whether the skill is symlinked or local.

## Reference Files

### API Domain

| Tier | File                       | Size    | Use For                                                                         |
| ---- | -------------------------- | ------- | ------------------------------------------------------------------------------- |
| 1    | `references/primer.md`     | 18KB    | Model IDs, Messages API, tool use, streaming, extended thinking, prompt caching |
| 2    | `references/cookbook/*.md` | 8 files | Real-world patterns: RAG, agents, optimization, multimodal                      |
| 3    | `references/changelog.md`  | ~30KB   | Claude Code changelog (v2.0.0+), recent changes                                 |
| 4    | `references/llms-full.txt` | 24MB    | Complete API documentation — every endpoint, parameter, SDK reference           |

### CLI Domain

| Tier | File                                | Size  | Use For                                                                                             |
| ---- | ----------------------------------- | ----- | --------------------------------------------------------------------------------------------------- |
| 1    | `references/cli-quick-reference.md` | 27KB  | Installation, quickstart, workflows, settings, key features                                         |
| 2    | `references/cli-section-index.md`   | 11KB  | Page directory — find the right page before going to Tier 3                                         |
| 3    | `references/cli-full-docs.txt`      | 1.8MB | Complete CLI docs (58 pages) — plugins, hooks, skills, subagents, deployment, MCP, IDE integrations |

## How to Use This Skill

### Step 1: Understand the Question

Read the full question and its context. Don't route based on a single keyword — understand what the user actually needs.

Questions fall on a spectrum:

**Quick fact** — "What's the model ID for Haiku 4.5?"
Load Tier 1 only. Answer in one line.

**Focused lookup** — "How do I create a PostToolUse hook?"
Load the relevant Tier 1 to orient, then go to Tier 3 for the specific page.

**Implementation guidance** — "What's the best way to handle streaming in our agent?"
This may touch both domains. Check API docs for streaming mechanics AND CLI docs for agent/subagent patterns.

**Cross-reference** — "Are we using hooks correctly according to the docs?"
Read the user's code, then verify against CLI Tier 3 hook documentation. May also need API docs if the hook involves API calls.

**What changed** — "What's new in the latest Claude Code release?"
Go straight to `changelog.md`.

### Step 2: Load the Right Tiers

**Always start light, escalate as needed:**

1. For API questions → load `primer.md` first. If it has the answer, stop.
2. For CLI questions → load `cli-quick-reference.md` first. If it has the answer, stop.
3. If more detail needed → use Tier 2 to find the right section, then extract from Tier 3.
4. For deep/specific API questions → grep into `llms-full.txt` (never load the whole file).
5. For cross-domain questions → pull from both domains as needed.

**Tier 3/4 search patterns:**

```bash
# CLI: list all available pages
grep "^PAGE:" references/cli-full-docs.txt

# CLI: extract a specific page (adjust -A for page length)
grep -A 200 "^PAGE: /hooks" references/cli-full-docs.txt

# API: search for a topic
grep -n "tool_choice" references/llms-full.txt

# API: extract a section (use line numbers from grep)
sed -n '45000,45500p' references/llms-full.txt
```

### Step 3: Cross-Reference When Needed

Many real questions span both domains. Examples:

| Question                                     | API docs needed                      | CLI docs needed                             |
| -------------------------------------------- | ------------------------------------ | ------------------------------------------- |
| "Best way to implement tool use in a plugin" | Tool use parameters, response format | Plugin structure, hooks                     |
| "How should our agent handle rate limits"    | Rate limit headers, retry logic      | Subagent configuration, headless mode       |
| "Set up streaming with extended thinking"    | Streaming API, thinking blocks       | Terminal config, output styles              |
| "Deploy Claude Code on Bedrock for our team" | Bedrock model IDs, auth              | Bedrock setup page, server-managed settings |

Don't force an either/or choice. Pull from whatever sources answer the question.

### Step 4: Cite Sources

Always tell the user where the answer came from:

- "From the API primer: ..."
- "From the CLI hooks page: ..."
- "Cross-referencing the API streaming docs with the CLI output styles page: ..."

This helps the user verify and also helps them know where to look next time.

## Updating Documentation

When user asks to update (trigger: "update claude documentation"):

```bash
# Update API docs: primer.md, llms-full.txt, changelog.md (~30-60 sec)
"${CLAUDE_SKILL_DIR}/scripts/update-llms.sh"

# Update CLI docs: 3-tier output via shared doc-builder (~60-90 sec)
"${CLAUDE_SKILL_DIR}/scripts/update-cli-docs.sh"
```

Run both scripts. Report results including file sizes, line counts, and any failures.

**Selective updates:**

```bash
# Only update changelog
"${CLAUDE_SKILL_DIR}/scripts/update-llms.sh" --changelog

# Only update API primer
"${CLAUDE_SKILL_DIR}/scripts/update-llms.sh" --primer
```

**Automated refresh:** A launchd daemon runs every 12 hours to keep all doc skills fresh (see `scripts/refresh-all-docs.sh` in the toolkit root).

## Bundled Agent: cli-changelog

For a curated "What's new" summary (not just raw changelog), run the bundled agent:

```
agents/cli-changelog.md
```

This reads the local `references/changelog.md`, diffs against its state file (`~/.claude/cli-updates/state.json`), and produces an educational report at `~/.claude/cli-updates/LATEST.md` explaining what changed, why it matters, and how to use new features. Reports are archived by date.

## Coverage

**What this skill covers:**

- Claude API (Messages, Batches, Models, Admin)
- Claude Code CLI (plugins, skills, hooks, subagents, MCP, settings)
- Agent SDK / TypeScript SDK / Python SDK
- Platform integrations (Bedrock, Vertex, Foundry)
- Tool use, extended thinking, streaming, vision, PDF, prompt caching
- Deployment, security, monitoring, CI/CD
- IDE integrations (VS Code, JetBrains)

**What this skill does NOT cover:**

- Claude.ai web interface
- Third-party libraries beyond official SDKs
- Anthropic company/pricing information
- OpenRouter (use openrouter-docs-skill)
- Warp terminal (use warp-docs-skill)

## Rules

1. **Go as deep as needed.** Quick lookups stay light. Complex questions deserve thorough cross-referencing.
2. **Never load full Tier 3/4 files.** Always use grep/sed to extract relevant sections.
3. **Don't guess from memory.** Check the actual docs, especially for model IDs, parameter names, and recent changes.
4. **Cross-reference freely.** A question about "hooks for streaming" needs both domains — don't pick one.
5. **Cite every answer.** Name the file and section so the user can verify.

---

**Skill Version:** 3.0.0
**Sources:** platform.claude.com (API), code.claude.com (CLI)
