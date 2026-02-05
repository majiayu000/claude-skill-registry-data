---
name: hti-zen-orchestrator
description: Guidelines for using Zen MCP tools effectively in this repo. Use for complex multi-model tasks, architectural decisions, or when cross-model validation adds value.
---

# HTI Zen Orchestrator

This Skill defines **when and how** to use Zen MCP tools in the **hti-zen-harness** project.

Zen provides multi-model orchestration (`planner`, `consensus`, `codereview`, `thinkdeep`, `debug`, `clink`). Use them deliberately when they add real value, not reflexively.

---

## ⚡ Recommended Approach: Use API Tools Directly

**Prefer direct Zen MCP tools over clink**:
- ✅ `chat`, `thinkdeep`, `consensus`, `codereview`, `precommit`, `debug`, `planner`
- ✅ Work via API (no CLI setup needed)
- ✅ Already configured and tested
- ✅ Simple, reliable, fast

**Avoid clink unless absolutely necessary**:
- ❌ Requires separate CLI installations (gemini CLI, codex CLI, etc.)
- ❌ Requires separate authentication for each CLI
- ❌ Uses your API credits anyway (no cost benefit)
- ❌ More complexity for minimal gain in this project

**Bottom line**: Direct API tools (`mcp__zen__chat`, `mcp__zen__consensus`, etc.) do everything you need without the CLI overhead.

---

## When Zen Tools Add Value

### Consider using Zen MCP tools when:

**Complex architectural work**
- Multi-file refactors spanning 5+ files
- New subsystems or major feature additions
- Changes to core HTI abstractions (bands, adapters, guards, probes)
- Redesigning interfaces or data flows

**Safety-critical code**
- Modifying timing bands or HTI invariants
- Changes to error handling or recovery logic
- Adapter implementations that interact with external models
- CI/CD pipeline changes that affect safety guarantees

**Ambiguous or contentious decisions**
- Multiple valid implementation approaches exist
- Trade-offs between performance, safety, and complexity
- Unusual patterns where you're unsure of best practice

**Deep investigation needed**
- Complex bugs with unclear root cause
- Performance issues requiring systematic analysis
- Understanding unfamiliar codebases or dependencies

### When Zen is overkill:

**Simple changes**
- Single-file bug fixes
- Adding straightforward tests
- Documentation updates
- Simple refactors (renaming, extracting functions)
- Configuration tweaks

For these, direct implementation is faster and more appropriate.

---

## Zen Tool Selection Guide

### `planner` - Multi-step planning with reflection

**Use when:**
- Task has 5+ distinct steps
- Multiple architectural approaches possible
- Need to think through dependencies and ordering
- Want progressive refinement of a complex plan

**Example**: "Plan migration of adapter interface to support streaming responses"

### `consensus` - Multi-model debate and synthesis

**Use when:**
- Two+ valid approaches with different trade-offs
- Safety-critical decisions need validation
- Controversial architectural choices
- Want diverse perspectives on a design

**Example**: "Should we use async generators or callback patterns for streaming? Get consensus from multiple models."

**Models to include**: At least 2, typically 3-4. Mix code-specialized models with general reasoning models.

### `codereview` - Systematic code analysis

**Use when:**
- Reviewing large PRs or branches
- Safety-critical changes to core logic
- Unfamiliar code needs audit
- Want comprehensive security/performance review

**Example**: "Review the new HTI band scheduler implementation for correctness and edge cases."

### `thinkdeep` - Hypothesis-driven investigation

**Use when:**
- Complex architectural questions
- Performance analysis and optimization planning
- Security threat modeling
- Understanding subtle interactions

**Example**: "Investigate why adapter timeout logic behaves differently under load."

### `debug` - Root cause analysis

**Use when:**
- Complex bugs with mysterious symptoms
- Race conditions or timing issues
- Failures that only occur in specific conditions
- Need systematic hypothesis testing

**Example**: "Debug why HTI band transitions occasionally skip validation steps."

### `clink` - Delegating to external CLI tools

**Use when:**
- Need capabilities of a specific AI CLI (gemini, codex, claude)
- Want to leverage role presets (codereviewer, planner)
- Continuing a conversation thread across tools

**Example**: "Use clink with gemini CLI for large-scale codebase exploration."

### `chat` - General-purpose thinking partner

**Use for:**
- Brainstorming approaches
- Quick sanity checks
- Explaining concepts
- Rubber-duck debugging

---

## Model Selection Guidelines

When calling Zen tools, choose models deliberately based on the task:

### For reading, exploration, summarization:
- **Prefer**: Models with large context windows and good efficiency
- **Pattern**: Large-context, efficient models
- **Use case**: "Scan 50 test files to find coverage gaps"

### For core implementation and refactoring:
- **Prefer**: Code-specialized, high-quality models
- **Pattern**: Code-specialized models (e.g., models with "codex" in the name or any available code-focused equivalent)
- **Use case**: "Implement new HTI adapter with proper error handling"

### For safety-critical validation:
- **Use**: Multiple models via `consensus` or sequential `codereview`
- **Pattern**: Mix of code-specialized and general reasoning models for diverse perspectives
- **Use case**: "Validate timing band logic won't introduce deadlocks"

### Document your choices:

When model selection matters for auditability:
```python
# HTI-NOTE: Implementation reviewed by code-specialized models (consensus check).
# No race conditions detected in band transition logic.
def transition_band(current: Band, target: Band) -> Result:
    ...
```

---

## Shell Access via `clink`

Zen's `clink` tool can execute shell commands. Use it responsibly.

### ✅ OK without asking (read-only, low-risk):

- File inspection: `ls`, `pwd`, `cat`, `head`, `tail`, `find`
- Git inspection: `git status`, `git diff`, `git log`, `git branch`
- Testing: `pytest`, `python -m pytest`, test runners
- Linting: `ruff check`, `black --check`, `mypy`, static analysis
- Info gathering: `python --version`, `uv --version`, dependency checks

### ⚠️ Ask user approval first:

- **Installing packages**: `pip install`, `uv add`, `npm install`
- **Git mutations**: `git commit`, `git push`, `git reset`, `git checkout -b`, `git rebase`
- **File mutations**: `rm`, `mv`, file deletions/moves
- **Network operations**: `curl`, `wget`, API calls
- **Environment changes**: Modifying config files, `.env` files

**How to ask:**
```
I need to run: `pip install pytest-asyncio`
Reason: Required for testing async adapter implementations
Approve?
```

---

## Failure Handling with Zen

When Zen tools or model calls fail, follow these rules (aligned with `hti-fallback-guard`):

### ❌ Do NOT:
- Pretend the call succeeded
- Silently switch to a different model without explanation
- Invent outputs or fake data
- Swallow errors and continue as if nothing happened

### ✅ DO:

**1. Report clearly:**
```
Zen `codereview` call failed:
  Tool: codereview
  Model: <model-name>
  Error: Rate limit exceeded (429)
  Step: Reviewing src/adapters/openai.py
```

**2. Propose alternatives:**
- "Retry with a different model (another available code-specialized option)?"
- "Split the review into smaller chunks?"
- "Proceed with manual review instead?"
- "Wait 60s and retry?"

**3. Document in code if relevant:**
```python
# HTI-TODO: Codereview via Zen failed (rate limit).
# Manual review needed for thread safety in adapter pool.
```

### Structured failure result pattern:

When appropriate, return explicit error states:
```python
@dataclass
class ZenResult:
    ok: bool
    tool: str
    data: dict | None = None
    error: str | None = None

# Never set ok=True when Zen call actually failed
```

---

## Recommended Workflow for Substantial Changes

For non-trivial work (multi-file refactors, new features, safety-critical edits):

### 1. Plan (if complexity warrants it)
- Use Zen `planner` for complex, multi-faceted tasks
- For simpler changes, a bullet list is fine
- Show plan to user, get confirmation

### 2. Implement
- Use appropriate model (code-specialized for core logic)
- Follow `hti-fallback-guard` principles
- Document model choice if safety-critical

### 3. Review (for important changes)
- Use Zen `codereview` for:
  - Large PRs (10+ files)
  - Safety-critical logic
  - HTI band/adapter/guard changes
- Use Zen `precommit` before finalizing

### 4. Summarize
Tell the user:
- What changed (files, behavior)
- Which models/tools were used
- Any TODOs or concerns
- Test coverage added/modified

---

## Integration with Testing and CI

When working on tests or CI:

**Prefer changes that tighten guarantees:**
- Tests that assert explicit failures (not silent fallbacks)
- CI checks that fail loudly when invariants break
- Guards that prevent invalid state transitions

**Use Zen tools to:**
- Validate test coverage (`codereview` with focus on testing)
- Check CI logic for edge cases (`thinkdeep` on pipeline behavior)
- Compare testing strategies (`consensus` on approach)

**Document how changes affect:**
- HTI invariants (timing, safety, ordering)
- Existing guards and probes
- CI failure modes

---

## When in Doubt

Ask yourself:
1. **Is this complex enough to need multi-model orchestration?**
   - Yes → Use Zen deliberately
   - No → Direct implementation is fine

2. **Does this change affect safety or timing?**
   - Yes → Consider `consensus` or `codereview`
   - No → Proceed with standard review

3. **Am I using Zen to avoid thinking, or to think better?**
   - Avoid thinking → Don't use Zen
   - Think better → Use Zen appropriately

The goal is **thoughtful tool use**, not **tool maximalism**.

---

## HTI-Specific Model Recommendations

**Available Models** (as of 2025-11-30):
- **Gemini**: `gemini-2.5-pro` (1M context, deep reasoning), `gemini-2.5-flash` (ultra-fast)
- **OpenAI**: `gpt-5.1`, `gpt-5.1-codex`, `gpt-5-pro`, `o3`, `o3-mini`, `o4-mini`

**Recommended by Task**:
- **Planning**: `gpt-5.1-codex` (code-focused structured planning)
- **Architecture**: `gemini-2.5-pro` (deep reasoning, 1M context)
- **Debugging**: `o3` (strong logical analysis)
- **Code Review**: `gpt-5.1` (comprehensive reasoning)
- **Quick Questions**: `gemini-2.5-flash` (ultra-fast, 1M context)
- **Consensus**: Mix 2-3 models (e.g., `gpt-5.1` + `gemini-2.5-pro` + `o3`)

---

## Practical Templates

### Template 1: Planning New HTI Version

**Use Case**: Starting v0.X implementation (5+ files, new subsystems)

**Pattern**:
```
Use planner with gpt-5.1-codex to design [FEATURE]:

Context:
- Current state: [what exists now]
- Goal: [what we're building]
- Constraints: [HTI invariants, backward compatibility]

Plan should include:
1. Architecture changes needed
2. File modifications (existing + new)
3. Testing strategy
4. Migration path (if breaking changes)
```

**Example**:
```
Use planner with gpt-5.1-codex to design v0.6 RL policy integration:

Context:
- Current: PD/PID controllers via ArmBrainPolicy protocol
- Goal: Support stateful RL policies (PPO, SAC, DQN)
- Constraints: Zero harness changes, brain-agnostic design

Plan should include:
1. BrainPolicy extension for stateful policies
2. Episode buffer interface
3. Checkpoint loading/saving
4. Testing with dummy RL brain
```

---

### Template 2: Design Decisions via Consensus

**Use Case**: Multiple valid approaches, safety-critical choices

**Pattern**:
```
Use consensus to decide: [QUESTION]

Models:
- gpt-5.1 with stance "for" [OPTION A]
- gemini-2.5-pro with stance "against" [OPTION A, argue for OPTION B]
- o3 with stance "neutral" (objective analysis)

Context:
[Relevant technical details]

Criteria:
- [Criterion 1]
- [Criterion 2]
```

**Example**:
```
Use consensus to decide: RL framework for HTI v0.6

Models:
- gpt-5.1 with stance "for" Stable-Baselines3
- gemini-2.5-pro with stance "against" SB3, argue for CleanRL
- o3 with stance "neutral"

Context:
- Need PPO, SAC, DQN implementations
- Must integrate with HTI ArmBrainPolicy protocol
- Want good documentation and active maintenance

Criteria:
- Ease of integration with HTI
- Code quality and maintainability
- Performance and stability
```

---

### Template 3: Deep Investigation

**Use Case**: Complex questions about control theory, physics, tuning

**Pattern**:
```
Use thinkdeep with [MODEL] to investigate: [QUESTION]

Known evidence:
- [Observation 1]
- [Observation 2]

Initial hypothesis:
[What you think might be happening]

Files to examine:
[Absolute paths]
```

**Example**:
```
Use thinkdeep with o3 to investigate: Why does PD with Kd=2.0 converge faster than Kd=3.0?

Known evidence:
- Kd=2.0: avg 455 ticks to converge
- Kd=3.0: avg 520 ticks to converge
- Both use same Kp=8.0

Initial hypothesis:
Over-damping (Kd too high) slows response

Files to examine:
/home/john2/claude-projects/hti-zen-harness/hti_arm_demo/brains/arm_pd_controller.py
/home/john2/claude-projects/hti-zen-harness/hti_arm_demo/env.py
```

---

### Template 4: Code Review Before Release

**Use Case**: Before committing v0.X release (10+ files changed)

**Pattern**:
```
Use codereview with gpt-5.1 to review [SCOPE]:

Review type: full
Focus areas:
- Code quality and maintainability
- Security (HTI safety invariants)
- Performance (timing band compliance)
- Architecture (brain-agnostic design preserved)

Files to review:
[List of absolute file paths]
```

**Example**:
```
Use codereview with gpt-5.1 to review HTI v0.5 implementation:

Review type: full
Focus areas:
- Brain-agnostic design preserved
- EventPack metadata extension correct
- No timing band violations
- Fallback logic compliance (hti-fallback-guard)

Files to review:
/home/john2/claude-projects/hti-zen-harness/hti_arm_demo/brains/arm_imperfect.py
/home/john2/claude-projects/hti-zen-harness/hti_arm_demo/run_v05_demo.py
/home/john2/claude-projects/hti-zen-harness/hti_arm_demo/shared_state.py
/home/john2/claude-projects/hti-zen-harness/hti_arm_demo/bands/control.py
```

---

### Template 5: Context-Isolated Subagents (clink)

**Use Case**: Large codebase exploration, heavy reviews, save tokens

**Pattern**:
```
Use clink with [CLI] [ROLE] to [TASK]

Available CLIs: gemini, codex, claude
Available Roles: default, planner, codereviewer
```

**Examples**:
```
# Code review in isolated context (saves our tokens)
Use clink with gemini codereviewer to review hti_arm_demo/ for safety issues

# Large codebase exploration
Use clink with gemini to map all brain implementations and document their interfaces

# Strategic planning
Use clink with gemini planner to design phase-by-phase migration to MuJoCo physics
```

**Why use clink**:
- Gemini CLI launches fresh 1M context window
- Heavy analysis doesn't pollute our context
- Returns only final summary/report
- Can use web search for latest docs

---

### Template 6: Pre-Commit Validation

**Use Case**: Before `git commit` on major changes

**Pattern**:
```
Use precommit with gpt-5.1 to validate changes in [PATH]:

Focus:
- Security issues
- Breaking changes
- Missing tests
- Documentation completeness
```

**Example**:
```
Use precommit with gpt-5.1 to validate changes in /home/john2/claude-projects/hti-zen-harness:

Focus:
- HTI safety invariants preserved
- No regressions in existing tests
- New tests for v0.6 features
- CHANGELOG and SPEC updated
```
