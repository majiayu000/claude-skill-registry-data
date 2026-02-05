---
name: assess
description: >
  Step back and critically reassess project state. Use when asked to "assess",
  "step back", "fresh eyes", "check alignment", "sanity check", "health check",
  or "evaluate what's working". Offer to run after major changes (don't auto-run).
allowed-tools: Bash, Read, Glob, Grep
triggers:
  - assess the project
  - assess this
  - assess this directory
  - assess this folder
  - reassess this
  - reassess the project
  - re-evaluate the project
  - step back and analyze
  - step back
  - take a step back
  - fresh eyes
  - big picture check
  - check alignment
  - does the code match the docs
  - what's working and what isn't
  - evaluate code quality
  - reality check
  - sanity check
  - health check
  - project health check
  - quick audit
  - project audit
  - gap analysis
  - status check
  - project status
  - take stock
metadata:
  short-description: Step back and critically reassess project state
---

# Assess Skill

Step back and critically reassess the project state. This skill guides the agent through systematic, **collaborative** evaluation to catch drift between intent and reality.

## Key Principle: Collaborative Assessment

Assessment is a dialogue, not a report. Ask clarifying questions to:
- Understand what the user considers most important
- Clarify intent when documentation is ambiguous
- Prioritize findings based on user's goals
- Confirm assumptions before making recommendations

## Assessment Flow

### Step 1: Scope the Assessment

**If scope is clear** (e.g., "assess the auth module"), skip questions and proceed.

**If scope is open** (e.g., "step back and assess this"), ask:
- "What areas are you most concerned about?"
- "Should I focus on code quality, doc accuracy, or both?"
- "Any known issues I should acknowledge but not re-report?"

### Step 2: Find Project Root & Detect Ecosystem

Locate the project root and detect the ecosystem before reading metadata.

**Detect ecosystem first** by looking for these marker files:

| File | Ecosystem |
|------|-----------|
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python |
| `package.json`, `package-lock.json`, `yarn.lock` | Node.js/JavaScript |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `pom.xml`, `build.gradle` | Java |
| `Gemfile` | Ruby |
| `composer.json` | PHP |

**Then read ecosystem-specific metadata:**
- Python: `pyproject.toml` for dependencies, scripts, project info
- Node: `package.json` for scripts, dependencies
- Rust: `Cargo.toml` for crate info
- etc.

**Universal project docs (all ecosystems):**
```
README.md         # Project overview (check project root)
CONTEXT.md        # Agent-focused current status
AGENTS.md         # Agent skill discovery
docs/             # Documentation directory
```

**Fallback discovery** if no obvious metadata:
- Scan for `*.md` files in root
- Look for `src/` or `lib/` structure
- Check for test directories (`tests/`, `test/`, `spec/`)
- Find entry points by extension (`.py`, `.js`, `.rs`, `.go`)

### Step 3: Quick Scan & Initial Findings

Do a fast pass:
1. Read project metadata (pyproject.toml, package.json, etc.)
2. Read README.md for stated goals and features
3. Glob for structure understanding
4. Note 2-3 initial observations

Then check in (unless scope was already clear):
- "I see X, Y, Z - should I dig deeper on any of these?"
- "The docs claim [feature] - is this a priority to verify?"

### Step 4: Deep Dive

Based on user guidance, investigate thoroughly. For each finding, consider:
- Is this blocking or just technical debt?
- Does the user already know about this?
- What's the fix complexity?

### Step 5: Collaborative Report

Present findings and ask:
- "Which of these would you like me to fix now?"
- "Should I update the docs to reflect reality?"
- "Are any of these 'known issues' I should deprioritize?"

## Assessment Categories

### 1. Doc-Code Alignment
Compare what's documented vs what's implemented:
- **README claims** - Do advertised features actually exist?
- **CONTEXT.md** - Does "current status" reflect reality?
- **pyproject.toml scripts** - Do declared entry points work?
- **Config options** - Do all documented settings have effects?
- **Examples** - Do code samples in docs actually run?

**Ask:** "I found X documented but not implemented - should I implement it or update docs?"

### 2. Aspirational vs Implemented
Find gaps between intent and reality:
- Stub implementations (`pass`, `raise NotImplementedError`)
- TODO/FIXME blocking core functionality
- Features in code structure but no actual logic
- Dependencies declared but not used

**Ask:** "Is [aspirational feature] still on the roadmap, or should I remove it?"

### 3. Brittle Code
Find fragile patterns:
- Hardcoded values (URLs, paths, magic numbers)
- Missing error handling in I/O paths
- Regex/parsing that breaks on edge cases
- Version pins that may be stale

**Ask:** "I see hardcoded [value] - is this intentional for now or should I externalize it?"

### 4. Non-Working Code
Find features that exist but fail:
- Dead code paths (unreachable branches)
- Silent exception swallowing (`except: pass`)
- Integration points returning wrong data
- Import errors or missing dependencies

**Ask:** "This [feature] appears broken - is it actively used or can we remove it?"

### 5. Over-Engineered Code
Find unnecessary complexity:
- Abstractions with single implementation
- Config for hypothetical flexibility

**Ask:** "Is [abstraction] expected to grow, or can we simplify?"

### 6. Working Well
Acknowledge solid code - helps calibrate the assessment.

## Example Dialogue

**User:** "Step back and assess this project"

**Agent:** "I'll assess the project. A few quick questions first:
1. Are there specific areas you're concerned about?
2. Should I focus on code quality, doc accuracy, or both?
3. Any known issues I should acknowledge but not re-report?"

**User:** "Focus on whether the skills actually work as documented"

**Agent:** "I'll check the documented skills. Should I run any tests or commands to verify they work, or just review the code?"

**User:** "Yes, run the sanity tests"

**Agent:** *reads pyproject.toml, README.md, runs sanity tests*

"I've checked the documented skills. Here's what I found:

**Working as documented:**
- memory skill - recall/learn commands work
- scillm skill - batch completions working

**Drift found:**
- arxiv skill claims 'citation export' - I don't see this implemented
- youtube-transcripts example in SKILL.md uses old API format

Should I:
1. Fix the arxiv implementation to add citation export?
2. Update the docs to remove the claim?
3. Fix the youtube-transcripts example?

Which would you prefer I tackle first?"

## Output Format (When Presenting Findings)

```markdown
# Assessment: <project-name>

## Summary
<2-3 sentences: overall health, key findings>

## Scope
- **Covered:** [what was assessed]
- **Not covered:** [what was skipped or out of scope]

## Questions for You
- [Clarifying question about intent/priority]
- [Question about known issues]

## Findings

### Doc-Code Alignment
| Claim | Reality | Action? |
|-------|---------|---------|
| "Redis caching" | Not implemented | Remove claim / Implement? |

### Issues Found
1. **file.py:123** - [Issue description]
   - Severity: High/Medium/Low
   - Suggested fix: [brief]

### Working Well
- [Solid code to acknowledge]

## Recommended Next Steps
1. [Immediate fix]
2. [Doc update]
3. [Future improvement]

Which should I start with?
```

## When to Use

**On Request:**
- "Step back and assess this"
- "Sanity check the project"
- "Fresh eyes review"
- "Quick audit"
- "Health check"
- "Gap analysis"
- "Assess this directory/folder"
- "Big picture check"
- "Project status"
- "/assess"

**Proactively (always ask first, never auto-run):**
- "I've made significant changes - want me to do a quick assessment?"
- "Before I update the docs, should I verify the current state?"

## File Writing Policy: Read-Only by Default

**Core principle: Assessment is read-only. Never write files without explicit user consent.**

This prevents:
- Unexpected file changes
- Dirty git status
- Permission issues
- "Agent edited my repo" distrust

### The Print-First Pattern

When suggesting documentation, **show the content first, then offer to write**:

```
Agent: "I notice there's no README.md. Here's what I'd suggest:

---
# ProjectName

One-liner description based on pyproject.toml...

## Install
pip install ...

## Quick Start
...
---

Should I write this to README.md, or would you like to modify it first?"
```

This gives the user full control:
1. See exactly what will be written
2. Request changes before committing
3. Copy/paste themselves if preferred
4. Decline without friction

### Common Missing Docs

- `README.md` - Project overview, quick start
- `CONTEXT.md` - Current status for agents
- `CONTRIBUTING.md` - How to contribute
- `CHANGELOG.md` - Version history
- Inline docstrings for public APIs
- `--help` text for CLIs

### For Incomplete Docs

```
Agent: "The README mentions 'API endpoints' but doesn't list them.
Options:
1. I'll show you the endpoint docs to add (you approve before write)
2. Remove the mention until it's ready
3. Mark it as 'coming soon'

Which approach?"
```

**Key principle:** Print first, write only with explicit consent.

## External Research (When Needed)

Sometimes assessment requires external context. Ask before using paid services.

**Available research skills:**
| Skill | Use For | Cost |
|-------|---------|------|
| `/context7` | Library/framework documentation | Free |
| `/brave-search` | General web search, deprecation notices | Free |
| `/perplexity` | Deep research, complex questions | Paid |

**When to suggest research:**
- Verifying if a dependency is deprecated or has security issues
- Checking correct API usage for unfamiliar libraries
- Researching best practices for patterns you're unsure about
- Finding changelogs for version upgrades

**How to offer:**
```
Agent: "I see you're using library X v2.3. I'm not certain if this version
has known issues. Want me to check with /context7 or /brave-search?"
```

```
Agent: "The authentication pattern here looks unusual. Should I research
current best practices with /perplexity? (Note: this uses paid API)"
```

**Key principle:** Don't silently research - ask first, especially for paid services. Quick doc lookups with /context7 are usually fine.

## Escalation to Code Review

When assessment reveals significant issues, suggest `/code-review`:

**When to suggest code-review:**
- Complex refactoring needed across multiple files
- Architecture concerns that need deeper analysis
- Security-sensitive code paths
- Performance-critical sections
- When a second opinion from another AI provider would help

**How to suggest:**
"I've found [issues] that might benefit from a deeper code review. Want me to run `/code-review` with [provider] to get a structured analysis and patch suggestions?"

**Example:**
```
Agent: "The authentication module has several issues:
- Hardcoded secrets in 3 places
- Missing input validation
- No rate limiting

This is security-sensitive - would you like me to run `/code-review`
with OpenAI (high reasoning) to get a thorough security review and
suggested fixes?"
```

## Command Preferences

When running shell commands, prefer modern fast tools:

| Task | Prefer | Over | Why |
|------|--------|------|-----|
| Search content | `rg` (ripgrep) | `grep` | 10x faster, better defaults, respects .gitignore |
| Find files | `fd` | `find` | Faster, simpler syntax, respects .gitignore |
| List files | `eza` or `ls` | - | eza has better output if available |

Example patterns:
```bash
# Search for TODOs
rg "TODO|FIXME|HACK|XXX" --type py

# Find Python files modified recently
fd -e py --changed-within 7d

# Search for stub implementations
rg "raise NotImplementedError|pass$" --type py
```

## Tips

- **Collaborate** - Assessment is dialogue, not monologue
- **Ask before running** - Get permission before running tests, builds, or expensive commands
- **Skip questions if scope is clear** - Don't ask "what areas?" if user said "assess the auth module"
- **Prioritize** - Not every finding needs immediate action
- **Be specific** - File paths and line numbers
- **Be actionable** - Each finding should suggest next steps
- **Update as you go** - If you find drift, offer to fix it immediately
- **Escalate wisely** - Suggest code-review for complex/critical issues
- **State your scope** - Always clarify what was and wasn't assessed
- **Use fast tools** - Prefer rg/fd over grep/find for speed
