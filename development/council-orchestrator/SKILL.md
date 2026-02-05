---
name: council-orchestrator
description: Orchestrates multi-model LLM consensus through a three-phase deliberation protocol. Use when you need collaborative AI review, multi-model problem-solving, code review from multiple perspectives, or consensus-based decision making. Coordinates OpenAI Codex, Google Gemini, and Claude CLIs for opinion collection, peer review, and chairman synthesis.
---

# Council Orchestration Protocol

## Overview

Three-phase consensus protocol coordinating multiple LLMs for collaborative decision-making.

**Architecture:**
- **Phase 1**: Parallel opinion collection from available LLMs
- **Phase 2**: Cross-examination peer review
- **Phase 3**: Chairman synthesis of consensus

**Council Members:**
- Claude CLI (required minimum)
- OpenAI Codex CLI (optional, enhances consensus)
- Google Gemini CLI (optional, enhances consensus)

## Quick Start

### Prerequisites Check

```bash
# Resolve path to council_utils.sh
if [[ -n "${COUNCIL_PLUGIN_ROOT:-}" ]]; then
    UTILS_PATH="${COUNCIL_PLUGIN_ROOT}/skills/council-orchestrator/scripts/council_utils.sh"
elif [[ -n "${CLAUDE_PLUGIN_ROOT:-}" ]]; then
    UTILS_PATH="${CLAUDE_PLUGIN_ROOT}/skills/council-orchestrator/scripts/council_utils.sh"
else
    UTILS_PATH="${CLAUDE_PROJECT_DIR}/skills/council-orchestrator/scripts/council_utils.sh"
fi

source "$UTILS_PATH"
get_cli_status
```

**Quorum Requirements:**
- **Minimum**: 1 CLI (Claude) - single-model mode for testing
- **Recommended**: 2+ CLIs - enables peer review and synthesis
- **Optimal**: All 3 CLIs - full consensus protocol

See [detailed prerequisites](./REFERENCE.md#prerequisites) for CLI installation.

---

## Execution Flow

### Phase 1: Opinion Collection

**Quick Start:**
```bash
# Initialize working directory
council_init

# Validate user input (security)
validate_user_input "$user_query" || exit 1

# Execute parallel opinion collection
PLUGIN_ROOT=$(get_plugin_root)
"${PLUGIN_ROOT}/skills/council-orchestrator/scripts/run_parallel.sh" "$query" .council
```

**What it does:**
- Consults all available LLMs in parallel
- Captures opinions to `.council/stage1_*.txt`
- Validates outputs and marks absent members
- Checks quorum for proceeding

**Output Files:**
- `.council/stage1_claude.txt` (required)
- `.council/stage1_openai.txt` (if Codex available)
- `.council/stage1_gemini.txt` (if Gemini available)

**Manual Execution:** See [Phase 1 detailed guide](./REFERENCE.md#phase-1-opinion-collection)

---

### Phase 2: Peer Review

**Quick Start:**
```bash
PLUGIN_ROOT=$(get_plugin_root)
"${PLUGIN_ROOT}/skills/council-orchestrator/scripts/run_peer_review.sh" "$original_question" .council
```

**What it does:**
- Each LLM reviews peers' responses anonymously
- Uses structured review template from `templates/review_prompt.txt`
- Executes reviews in parallel
- Outputs to `.council/stage2_review_*.txt`

**Cross-Review Matrix:**

| Reviewer | Reviews |
|----------|---------|
| Claude   | Codex (A) + Gemini (B) |
| Codex    | Claude (A) + Gemini (B) |
| Gemini   | Claude (A) + Codex (B) |

**Output Files:**
- `.council/stage2_review_claude.txt`
- `.council/stage2_review_openai.txt`
- `.council/stage2_review_gemini.txt`

**Manual Execution:** See [Phase 2 detailed guide](./REFERENCE.md#phase-2-peer-review)

---

### Phase 3: Chairman Synthesis

**Quick Start:**
```bash
# Generate chairman invocation prompt
PLUGIN_ROOT=$(get_plugin_root)
CHAIRMAN_PROMPT=$("${PLUGIN_ROOT}/skills/council-orchestrator/scripts/run_chairman.sh" \
    "$original_question" \
    .council)

# Invoke chairman sub-agent
# Use Task tool: council-chairman agent
```

**Prompt for Chairman:**
```
Use the council-chairman agent to synthesize the council's responses.

$CHAIRMAN_PROMPT
```

**After chairman completes:**
```bash
# Retrieve final report for this run
cat .council/final_report.md
```

**What it does:**
- Chairman agent reads all Stage 1/2 files
- Analyzes for consensus and disagreements
- Generates comprehensive verdict report
- Writes to `.council/final_report.md`

**Context Isolation:**
- Chairman operates in isolated context
- Only has Read/Write tools (no Bash, no external CLIs)
- Ensures unbiased synthesis based solely on files

**Manual Execution:** See [Phase 3 detailed guide](./REFERENCE.md#phase-3-chairman-synthesis)

---

## Error Handling

| Error | Handling | Details |
|-------|----------|---------|
| **CLI missing** | Proceed with available members | See [quorum requirements](./REFERENCE.md#quorum-requirements) |
| **Rate limit (429)** | Exponential backoff, retry once | [Rate limit handling](./REFERENCE.md#rate-limiting-http-429) |
| **Empty output** | Mark member absent in report | [Empty output handling](./REFERENCE.md#empty-output) |
| **Timeout (>120s)** | Terminate, mark absent | [Timeout configuration](./REFERENCE.md#timeout-120-seconds) |
| **Quorum failure** | Abort council session | [Quorum check](./REFERENCE.md#quorum-failure) |

**Graceful Degradation:**
- Council proceeds with available members (minimum 1 required)
- Absent members are noted in final report
- Peer review skipped if <2 responses
- Single-model mode if only Claude available

---

## Security Best Practices

⚠️ **Important**: This skill executes external CLI tools with user-provided input. Follow security guidelines to prevent command injection and ensure safe operation.

### Key Security Measures

- **Input Validation**: All user queries validated before passing to external CLIs
- **CLI Verification**: Ensure external CLIs (codex, gemini, claude) are from trusted sources
- **Temporary Files**: All data in `.council/` is stored in a dedicated working directory. By default, files are preserved after synthesis so users can review or reuse the final report. Use `council_cleanup` or `/council-cleanup` to explicitly remove these files when no longer needed.
- **Proper Quoting**: All bash scripts use proper variable quoting to prevent injection

### Usage

```bash
# Always validate user input before processing
# Resolve path to council_utils.sh
if [[ -n "${COUNCIL_PLUGIN_ROOT:-}" ]]; then
    UTILS_PATH="${COUNCIL_PLUGIN_ROOT}/skills/council-orchestrator/scripts/council_utils.sh"
elif [[ -n "${CLAUDE_PLUGIN_ROOT:-}" ]]; then
    UTILS_PATH="${CLAUDE_PLUGIN_ROOT}/skills/council-orchestrator/scripts/council_utils.sh"
else
    UTILS_PATH="${CLAUDE_PROJECT_DIR}/skills/council-orchestrator/scripts/council_utils.sh"
fi

source "$UTILS_PATH"
validate_user_input "$user_query" || {
    error_msg "Invalid input - aborting for security"
    exit 1
}
```

### Detailed Security Information

For comprehensive security guidance including:
- Input sanitization patterns
- CLI authenticity verification
- Threat model and mitigations
- Security audit checklist

See [`SECURITY.md`](./SECURITY.md)

---

## Output Format

The final output is the Chairman's Markdown report containing:

### Report Structure

1. **Executive Summary**
   - Concise answer to original question
   - Key consensus points
   - Critical recommendations

2. **Council Debate Summary**
   - Table of significant divergences
   - Resolution of disagreements
   - Attribution to specific models

3. **Detailed Analysis**
   - Technical accuracy synthesis
   - Code quality assessment (if applicable)
   - Security considerations
   - Alternative approaches

4. **Final Recommendation**
   - Synthesized best practice
   - Implementation guidance
   - Caveats and edge cases

5. **Participation Notes** (if applicable)
   - Absent members
   - Degraded council mode notice

---

## Additional Resources

### Documentation

- **[REFERENCE.md](./REFERENCE.md)** - Detailed bash implementation and manual execution guide
- **[EXAMPLES.md](./EXAMPLES.md)** - Usage scenarios, troubleshooting, and integration examples
- **[SECURITY.md](./SECURITY.md)** - Security best practices and threat mitigation
- **[METADATA.md](./METADATA.md)** - Version history, compatibility, and licensing

### Templates

- **[templates/review_prompt.txt](./templates/review_prompt.txt)** - Peer review prompt template
- **[templates/chairman_prompt.txt](./templates/chairman_prompt.txt)** - Chairman invocation template

### Scripts

- **scripts/council_utils.sh** - Shared utility functions
- **scripts/run_parallel.sh** - Automated Phase 1 execution
- **scripts/run_peer_review.sh** - Automated Phase 2 execution
- **scripts/run_chairman.sh** - Chairman prompt generation
- **scripts/query_claude.sh** - Claude CLI wrapper
- **scripts/query_codex.sh** - Codex CLI wrapper
- **scripts/query_gemini.sh** - Gemini CLI wrapper

---

## Common Usage Patterns

### Full Automated Run
```bash
# Resolve path to council_utils.sh
if [[ -n "${COUNCIL_PLUGIN_ROOT:-}" ]]; then
    UTILS_PATH="${COUNCIL_PLUGIN_ROOT}/skills/council-orchestrator/scripts/council_utils.sh"
elif [[ -n "${CLAUDE_PLUGIN_ROOT:-}" ]]; then
    UTILS_PATH="${CLAUDE_PLUGIN_ROOT}/skills/council-orchestrator/scripts/council_utils.sh"
else
    UTILS_PATH="${CLAUDE_PROJECT_DIR}/skills/council-orchestrator/scripts/council_utils.sh"
fi

source "$UTILS_PATH"

# Phase 0: reset working directory for this run
council_cleanup || true
council_init

# Phase 1
validate_user_input "$query" || exit 1
PLUGIN_ROOT=$(get_plugin_root)
"${PLUGIN_ROOT}/skills/council-orchestrator/scripts/run_parallel.sh" "$query" .council

# Phase 2
"${PLUGIN_ROOT}/skills/council-orchestrator/scripts/run_peer_review.sh" "$query" .council

# Phase 3
CHAIRMAN_PROMPT=$("${PLUGIN_ROOT}/skills/council-orchestrator/scripts/run_chairman.sh" "$query" .council)
# [Invoke chairman agent with $CHAIRMAN_PROMPT]

# Output
cat .council/final_report.md
```

### Check Council Status
```bash
# Resolve path to council_utils.sh
if [[ -n "${COUNCIL_PLUGIN_ROOT:-}" ]]; then
    UTILS_PATH="${COUNCIL_PLUGIN_ROOT}/skills/council-orchestrator/scripts/council_utils.sh"
elif [[ -n "${CLAUDE_PLUGIN_ROOT:-}" ]]; then
    UTILS_PATH="${CLAUDE_PLUGIN_ROOT}/skills/council-orchestrator/scripts/council_utils.sh"
else
    UTILS_PATH="${CLAUDE_PROJECT_DIR}/skills/council-orchestrator/scripts/council_utils.sh"
fi

source "$UTILS_PATH"
get_cli_status
count_available_members
can_council_proceed && echo "Council ready" || echo "Install more CLIs"
```

### Configuration Management
```bash
# View current config
config_list

# Set custom quorum
config_set "min_quorum" "3"

# Enable only specific members
config_set "enabled_members" "claude,gemini"
```

For more examples see [EXAMPLES.md](./EXAMPLES.md)
