---
name: investigate
description: "Multi-provider adversarial investigation. Claude (Opus) and Codex (GPT, model from ~/.codex/config.toml) debate through structured rounds. Use for ideation, architecture decisions, risk analysis, or any topic that benefits from adversarial scrutiny before committing to an approach."
argument-hint: "<topic or question to investigate>"
---

# Investigate: Adversarial Multi-Provider Debate

Structured debate between Claude (Opus) and Codex (GPT, model from ~/.codex/config.toml) where they challenge each other's ideas through multiple rounds. **Runs in background** — you can continue working while the debate happens.

/investigate runs in background — adversarial Claude + Codex debate, returns convergence report

User-input prompt presentation in this skill follows the banner
convention in `docs/user-input-banner-convention.md`. The async-result
follow-up fork in "When Results Arrive" carries the `AWAITING YOUR INPUT`
banner.

### Caveman activation in this flow

Caveman compression is mandatory in this flow. The wire prefix `[COMPRESSION:terse]` MUST be prepended to every subagent Task description and to every Codex MCP `developer-instructions:` field within this flow. Machine-output payloads (haiku scorer JSON, `render_findings` / `dedupe_findings` IO, parser inputs) are exempt per `skills/caveman/SKILL.md` §7.

## When to use

- Architecture decisions ("should we use X or Y?")
- Risk analysis before major changes
- Evaluating tradeoffs between approaches
- Stress-testing an idea before implementation
- Any decision that benefits from adversarial scrutiny

## Argument Parsing

- `$ARGUMENTS` is the topic or question to investigate
- Optional flags:
  - `--rounds N` — number of debate rounds (default 3, max 5)
  - `--codebase` — include repository context in the debate (auto-detected if topic references code)
  - `--focus <area>` — narrow the debate to a specific aspect

**Examples:**
```
/investigate should we migrate from Axelar to Wormhole for the bridge?
/investigate --rounds 4 --codebase is our current fee calculation safe against precision loss?
/investigate --focus security what are the risks of adding flash loan support?
```

---

## Execution: BACKGROUND

**DO NOT block the main conversation.** Dispatch to the `investigator` agent and return control immediately.

### Step 1: Parse arguments

Extract:
- **topic**: the core question
- **max_rounds**: from `--rounds` or default 3
- **codebase_context**: true if `--codebase` flag or topic references files/code
- **focus**: from `--focus` or null

### Step 2: Launch investigator agent

Use the Agent tool to launch the `investigator` subagent with `run_in_background: true`:

**Prompt template:**
```
Investigate the following topic through adversarial debate.

topic: [parsed topic]
max_rounds: [N]
codebase_context: [true/false]
focus: [area or "general"]
working_directory: [cwd]

[If codebase_context: brief summary of relevant files/architecture]
```

### Step 3: Inform the user

Immediately respond:
> Investigation started in background: **"[topic]"**
> Claude (Opus) and Codex (GPT, model from ~/.codex/config.toml) will debate for up to [N] rounds.
> I'll present the convergence report when they finish. You can continue working.

**Then return control.** Do NOT wait.

---

## When Results Arrive

When the investigator agent completes:

1. Present the convergence report to the user
2. Highlight:
   - **Key agreements** (high confidence conclusions)
   - **Unresolved tensions** (genuine tradeoffs to decide on)
   - **Recommended approach** (synthesized from both perspectives)
3. Ask the user to pick the next move via the banner below.

---
## ⏸ AWAITING YOUR INPUT

Investigation finished — pick the next move.

- `investigate-deeper` — re-open the debate with a narrower angle (e.g. a specific tension, a new constraint, an alternative framing).
- `accept-and-proceed` — take the current recommendation as the decision and move on.
- `pivot` — abandon this line and start a new investigation on a different angle.

**Which path?**

---

## How the Debate Works (for context)

The investigator agent runs structured rounds:

1. **Claude** generates a thorough position with rationale, risks, and tradeoffs
2. **Codex** critiques via MCP — finds flaws, challenges assumptions, proposes alternatives
3. **Synthesis** — identifies agreements, disagreements, evolved positions
4. **Convergence check** — stops early if no new critiques emerge
5. Repeat until converged or max rounds

Each round builds on the previous. Codex maintains conversation context via `codex-reply` threadId. Both sides must acknowledge good arguments from the other (intellectual honesty).

---

## Tips

1. **Frame as a question, not a statement** — "should we use X?" triggers better debate than "we should use X"
2. **Add constraints** — "given our 2-week timeline" or "with 3 validators" narrows the debate productively
3. **Use --codebase for technical decisions** — agents will read actual code instead of speculating
4. **3 rounds is usually enough** — use more only for genuinely complex tradeoffs
5. **Act on the results** — the report is designed to be actionable, not academic
