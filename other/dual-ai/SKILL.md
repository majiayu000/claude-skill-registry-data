---
name: dual-ai
description: '[User-Invoked] Use ONLY when the user explicitly types /dual-ai or /dual-ai <workflow-id> — fans out one prompt, or one workflow invocation per tool, to two fresh parallel AI sessions (Claude Code + Codex CLI), both pre-set to xhigh reasoning effort and full-permission mode before the prompt executes. NEVER auto-activate.'
disable-model-invocation: false
---

> Codex compatibility note:
>
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - User-question prompts mean to ask the user directly in Codex.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, execute each listed child-skill step explicitly and report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.

<!-- CODEX:PROJECT-REFERENCE-LOADING:START -->

## Codex Project-Reference Loading (No Hooks)

Codex uses static project-reference loading instead of runtime-injected project docs.
When coding, planning, debugging, testing, or reviewing, open project docs explicitly using this routing.

**Always read:**

- `docs/project-config.json` (project-specific paths, commands, modules, and workflow/test settings)
- `docs/project-reference/docs-index-reference.md` (routes to the full `docs/project-reference/*` catalog)
- `docs/project-reference/lessons.md` (always-on guardrails and anti-patterns)

**Missing/stale context route:** If `docs/project-config.json`, the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any task-required reference doc is missing or stale, auto-run `$project-init` or the narrow setup route (`$project-config`, `$docs-init`, `$scan-all`, `$scan --target=<key>`, `$claude-md-init`) before ordinary project-specific work. If Codex mirrors or `AGENTS.md` are missing/stale, ask the user to run `$sync-codex`; do not auto-run it.

**Situation-based docs:**

- Project structure/architecture/tech-stack/deployment/setup (any layer — backend, frontend, or infra): `project-structure-reference.md`
- Backend/CQRS/API/domain/entity changes: `backend-patterns-reference.md`, `domain-entities-reference.md`
- Frontend/UI/styling/design-system: `frontend-patterns-reference.md`, `scss-styling-guide.md`, `design-system/README.md`
- Spec authoring, `docs/specs/` pathing, or TC format: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`
- Behavior/public-contract changes or spec-test-code sync: `workflow-spec-test-code-cycle-reference.md` plus the spec docs above
- Derived spec indexes/ERDs/reimplementation guides: `spec-system-reference.md` and source Feature Specs under `docs/specs/`
- Integration test implementation/review: `integration-test-reference.md`
- E2E test implementation/review: `e2e-test-reference.md`
- Code review/audit work: `code-review-rules.md` plus domain docs above based on changed files

Do not read all docs blindly. Start from `docs-index-reference.md`, then open only relevant files for the task.

<!-- CODEX:PROJECT-REFERENCE-LOADING:END -->

## Quick Summary

**Goal:** Take a user prompt, or a workflow id, and spawn TWO brand-new AI sessions in parallel — one Claude Code, one Codex — each launched with xhigh effort and full-permission mode already applied, then auto-submit the prompt in both.

**Workflow:**

1. **Capture** — persist USER_PROMPT to a run folder (avoids shell-quoting corruption)
2. **Generate launchers** — one launcher script per tool, OS-specific (`.ps1` on Windows, `.sh` on macOS/Linux), effort and full-permission mode set via launch flags
3. **Spawn** — open two new terminal windows via the OS spawner, one session per tool, prompt auto-submitted
4. **Report** — run folder path + how to find each window; `--orchestrate` (alias `--headless`) instead supervises both sessions via the bundled Node runner — waits for completion, watches statuses, collects both results, and presents a comparison

**Key Rules:**

- **MANUAL-ONLY:** This skill spawns external AI sessions that consume quota. Run it ONLY on explicit user invocation (`$dual-ai ...`). NEVER auto-activate it because a task "could benefit" from parallel AI
- Effort and full-permission mode MUST be set via launch flags (`claude --dangerously-skip-permissions --effort xhigh`, `codex --dangerously-bypass-approvals-and-sandbox -c model_reasoning_effort="xhigh"`) — flags apply BEFORE the prompt is processed; NEVER attempt to type `/model`, `/effort`, permission, approval, or sandbox commands into a running TUI
- The prompt is read from the per-tool prompt file (`prompt-claude.txt` / `prompt-codex.txt`) INSIDE the launcher script (`Get-Content -Raw` / `cat`) — NEVER inline-escape multi-line prompts through shell argument chains
- Detect the OS first (`uname -s`) and use the matching launcher + spawn branch; never assume Windows
- This skill ONLY orchestrates the two external sessions. Do NOT answer the prompt yourself in the current session
- Orchestrated mode (`--orchestrate`) is the ONLY way to get results back into this session — interactive TUI window output cannot be captured. The runner persists `status.json` + `events.ndjson` start-to-end as the external status report
- Verify both CLIs exist (`claude --version`, `codex --version`) before spawning; report which one is missing instead of half-launching

# Dual AI Session Fan-Out

## Purpose

Run the same task through two independent frontier agents at maximum reasoning effort and let the user compare results side by side. Each session is a NEW session (no shared context with the current one) so both agents reason from a clean slate in the repo working directory.

## Variables

- `USER_PROMPT`: $ARGUMENTS (required — if empty, ask the user for the prompt before doing anything)
- `WORKFLOW_ID`: optional first non-mode token. If it exactly matches a workflow id (a key under `.claude/workflows.json` `workflows`), treat it as a workflow invocation instead of free-text prompt. This preserves plain `$dual-ai` behavior: non-matching text remains the original fan-out prompt.
- `WORKFLOW_ARGS`: any remaining non-mode text after WORKFLOW_ID. Append it verbatim to BOTH per-tool workflow prompts as extra instructions.
- `CLAUDE_PROMPT` / `CODEX_PROMPT`: per-tool prompt values. Default: both = USER_PROMPT. Workflow-id mode sets `CLAUDE_PROMPT` to `/$WORKFLOW_ID` and `CODEX_PROMPT` to `$WORKFLOW_ID`, then appends WORKFLOW_ARGS to both when present. Treat both prompt values as opaque literals — do not expand, rewrite, or "fix" `$`/`/` prefixes.
- `MODE`: `--orchestrate` (alias `--headless`) flag anywhere in $ARGUMENTS → non-interactive orchestrated run: both sessions supervised by the bundled runner, statuses watched, outputs collected and compared (strip the flag from USER_PROMPT)
- `RUN_DIR`: `.ai/workspace/dual-ai/{YYMMDD-HHmm}/` (absolute path when generating launchers)

## Workflow

### 1. Validate + detect OS

- Strip MODE flags from USER_PROMPT first.
- Resolve workflow-id mode before validation:
    - Read `.claude/workflows.json` and parse the `workflows` id set.
    - If the first non-mode token exactly matches a `workflows` key, set WORKFLOW_ID to that token and remove it from USER_PROMPT.
    - Set `CLAUDE_PROMPT = "/" + WORKFLOW_ID`.
    - Set `CODEX_PROMPT = "$" + WORKFLOW_ID`.
    - If remaining text exists, append one space plus that remaining text verbatim to both prompts.
    - Example: `$dual-ai workflow-review-changes --orchestrate` writes `$workflow-review-changes` for Claude and `$workflow-review-changes` for Codex, preserving the former review wrapper behavior.
- If USER_PROMPT is empty AND no per-tool prompts were derived from WORKFLOW_ID → ask the user, stop.
- Check tool availability: `claude --version` and `codex --version`. If either is missing, report it and offer to run the available one only.
- Detect OS in the same Bash call: `uname -s` → `MINGW*`/`MSYS*`/`CYGWIN*` = Windows, `Darwin` = macOS, `Linux` = Linux. Pick the matching launcher + spawn branch below.

### 2. Persist prompts

Write CLAUDE_PROMPT verbatim (no escaping, no reformatting, no expansion) to `{RUN_DIR}/prompt-claude.txt` and CODEX_PROMPT to `{RUN_DIR}/prompt-codex.txt` using the Write tool. When no per-tool override exists, both files contain USER_PROMPT.

### 3. Generate launchers (Write tool, absolute paths)

Both CLIs accept a positional prompt that starts the new interactive session with that prompt auto-submitted; the effort and full-permission flags take effect at session init — before prompt execution. Replace `<REPO_ROOT>` with the absolute repo root.

**Windows** — `{RUN_DIR}/launch-claude.ps1` / `{RUN_DIR}/launch-codex.ps1`:

```powershell
$ErrorActionPreference = 'Stop'
Set-Location '<REPO_ROOT>'
$prompt = Get-Content -Raw "$PSScriptRoot\prompt-claude.txt"
Add-Content "$PSScriptRoot\events.ndjson" ('{"at":"' + (Get-Date -Format o) + '","event":"session-start","agent":"claude"}')
claude --dangerously-skip-permissions --effort xhigh -n 'dual-ai-claude' $prompt
Add-Content "$PSScriptRoot\events.ndjson" ('{"at":"' + (Get-Date -Format o) + '","event":"session-end","agent":"claude","exitCode":' + $LASTEXITCODE + '}')
# codex variant: reads prompt-codex.txt, runs codex --dangerously-bypass-approvals-and-sandbox -c model_reasoning_effort="xhigh" $prompt, logs agent "codex"
```

**macOS / Linux** — `{RUN_DIR}/launch-claude.sh` / `{RUN_DIR}/launch-codex.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "<REPO_ROOT>"
here="$(cd "$(dirname "$0")" && pwd)"
prompt="$(cat "$here/prompt-claude.txt")"
echo "{\"at\":\"$(date -u +%FT%TZ)\",\"event\":\"session-start\",\"agent\":\"claude\"}" >> "$here/events.ndjson"
code=0
claude --dangerously-skip-permissions --effort xhigh -n 'dual-ai-claude' "$prompt" || code=$?
echo "{\"at\":\"$(date -u +%FT%TZ)\",\"event\":\"session-end\",\"agent\":\"claude\",\"exitCode\":$code}" >> "$here/events.ndjson"
# codex variant: reads prompt-codex.txt, runs codex --dangerously-bypass-approvals-and-sandbox -c model_reasoning_effort="xhigh" "$prompt", logs agent "codex"
exec "$SHELL"   # keep the terminal interactive after the session ends (reachable even on nonzero exit)
```

After writing `.sh` launchers run `chmod +x {RUN_DIR}/launch-*.sh`.

### 4. Spawn both sessions (single Bash call, per OS)

**Windows** (`<RUN_DIR_WIN>` = Windows-style absolute path):

```bash
pwsh -NoProfile -Command "Start-Process pwsh -ArgumentList '-NoExit','-ExecutionPolicy','Bypass','-File','<RUN_DIR_WIN>\launch-claude.ps1'; Start-Process pwsh -ArgumentList '-NoExit','-ExecutionPolicy','Bypass','-File','<RUN_DIR_WIN>\launch-codex.ps1'; Write-Output 'both spawned'"
```

- `-NoExit` keeps each window open as a live interactive session after the prompt completes.
- Prefer `pwsh` (PowerShell 7+, check `pwsh -v`) over `powershell` — Windows PowerShell 5.1 mangles embedded double quotes when passing args to native executables; fall back to `powershell` only if `pwsh` is absent.
- If a path-boundary or similar hook blocks `cmd //c start ...`, this `Start-Process` form is the workaround — it contains no slash-prefixed flags.

**macOS**:

```bash
open -a Terminal "{RUN_DIR}/launch-claude.sh" && open -a Terminal "{RUN_DIR}/launch-codex.sh" && echo "both spawned"
```

If the user runs iTerm2, `open -a iTerm <script>` works the same way. If macOS Gatekeeper/automation permission blocks Terminal from running the script, fall back to headless mode and tell the user.

**Linux**:

```bash
x-terminal-emulator -e "{RUN_DIR}/launch-claude.sh" & x-terminal-emulator -e "{RUN_DIR}/launch-codex.sh" & echo "both spawned"
```

(Substitute `gnome-terminal --`, `konsole -e`, or `xterm -e` if `x-terminal-emulator` is absent. No display server → fall back to headless mode.)

### 5. Orchestrated mode (`--orchestrate` / `--headless` only)

Skip steps 3–4 (no terminal windows). The bundled supervisor `scripts/dual-ai-runner.mjs` (relative to this skill's directory) runs both sessions as supervised child processes — main-agent → external-main-agents orchestration with start-to-end status reporting.

**a. Write `{RUN_DIR}/run-config.json`** (the runner pipes each prompt via stdin — quoting-proof; args hold fixed flags ONLY, never prompt content). The runner enforces exactly the supported `claude`/`codex` identities, at most 2 agents, fixed flag templates, `cwd` inside the project/run dir, and bounded output (`maxOutputBytes`, default 25 MiB):

```json
{
    "runId": "{YYMMDD-HHmm}",
    "cwd": "<REPO_ROOT>",
    "timeoutSec": 3600,
    "maxOutputBytes": 26214400,
    "agents": [
        {
            "name": "claude",
            "command": "claude",
            "args": ["-p", "--dangerously-skip-permissions", "--effort", "xhigh"],
            "promptFile": "prompt-claude.txt",
            "outputFile": "claude-output.md",
            "outputMode": "stdout"
        },
        {
            "name": "codex",
            "command": "codex",
            "args": ["exec", "--dangerously-bypass-approvals-and-sandbox", "-c", "model_reasoning_effort=xhigh", "-o", "<RUN_DIR>/codex-output.md"],
            "promptFile": "prompt-codex.txt",
            "outputFile": "codex-output.md",
            "outputMode": "file"
        }
    ]
}
```

(`codex exec -o` writes the final message itself → `outputMode: "file"`; its live session log streams to `codex-progress.log`. The `-o` value MUST be the ABSOLUTE `<RUN_DIR>` path — the child runs from `cwd` = repo root, so a relative `-o` would land outside the run dir while the runner collects from `{RUN_DIR}/codex-output.md`. `outputFile` stays the bare file name; the runner always resolves it inside the run dir. `claude -p` prints the result on stdout → `outputMode: "stdout"`. Do not add more agents; use separate runs for additional tools.)

**b. Launch the supervisor** in ONE background Bash call (`run_in_background: true`) and let the harness notify on completion — do NOT busy-poll:

```bash
node <SKILL_DIR>/scripts/dual-ai-runner.mjs --run-dir "{RUN_DIR}"
```

The runner maintains the external status report start-to-end:

- `status.json` — atomically updated snapshot: run state + per-agent `starting|running|completed|failed|timeout`, pid, exit code, output bytes, last activity timestamp
- `events.ndjson` — append-only audit: `run-start`, `agent-start`, `agent-failed` (spawn error / unreadable prompt file), `agent-exit`, `kill`, `run-timeout`, `run-end`
- `<name>-stderr.log` / `codex-progress.log` — diagnostics

**c. Watch** — report initial per-agent statuses right after spawn; while the background task runs, read `{RUN_DIR}/status.json` on demand (user asks, or before long waits) and report each agent's state + outputBytes + lastActivityAt. Caveat: stdout-mode agents (`claude -p`) buffer the result until the end — `outputBytes: 0` / `lastActivityAt: null` is NORMAL for a healthy long run; only treat it as a stall after checking `runnerPid` and the process itself.

**d. Collect & compare** — when the background runner exits (exit 0 = all agents succeeded; 1 = at least one failed/timed out; 2 = config error), read `status.json` + both output files and present a comparison (agreements, disagreements, unique findings) citing the output files. On per-agent failure, surface `stderrTail` from `status.json` verbatim.

### 6. Report

State: run folder, the two window titles (or output file paths in orchestrated mode), effort level and permission mode applied to each, and that both sessions are independent new sessions. In interactive mode also state: TUI results cannot be collected back into this session — `events.ndjson` records session start/end lifecycle only; re-run with `--orchestrate` to wait, watch, and auto-collect both results.

## Failure Modes

- **Window opens then closes instantly** → launcher threw; re-run the launcher script (`.ps1`/`.sh`) directly in a foreground Bash call to surface the error, fix, respawn.
- **No GUI terminal available** (SSH session, container, no display server) → use headless mode and tell the user why.
- **Codex rejects xhigh** → the configured codex model does not support xhigh; fall back to `-c model_reasoning_effort="high"` and tell the user which model/effort was actually used.
- **Quota/auth errors** → surface verbatim from the session window or orchestrated output; do not retry silently.
- **Runner exits 2** → `run-config.json` missing/invalid; fix the config, relaunch.
- **Agent state `failed` in `status.json`** → read `{name}-stderr.log` and the `stderrTail` field; report verbatim.
- **`status.json` stops updating** (no heartbeat, `lastActivityAt` stale) → check whether `runnerPid` is still alive; if dead, treat outputs as partial and report what was collected. Note: stale `lastActivityAt` alone is NOT a stall signal for stdout-mode agents — they print only at the end (see Watch caveat).
- **Headless free-text prompts vs interactive-only hooks** → a spawned session's project hooks may demand interactive answers; slash-command prompts are exempt. If orchestrated output looks gate-blocked, mention this and suggest interactive mode for that prompt.

---

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

<!-- SYNC:ai-mistake-prevention -->

> **AI Mistake Prevention** — Failure modes to avoid on every task:
>
> **Re-read files after context changes.** Context compaction, resume, or long-running work can make memory stale; verify current files before acting.
> **Verify generated content against source evidence.** AI hallucinates APIs, names, claims, and document facts. Check the relevant source before documenting or referencing.
> **Check downstream references before deleting or renaming.** Removing an artifact can stale docs, generated mirrors, configs, and callers; map references first.
> **Trace the full impact chain after edits.** Changing a definition can miss derived outputs and consumers. Follow the affected chain before declaring done.
> **Verify ALL affected outputs, not just the first.** One green check is not all green checks; validate every output surface the change can affect.
> **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Before changing or reporting a constant, limit, flag, cutoff, wording, or pattern, read nearby context and history, the CALLER's ordering, and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard.
> **Surface ambiguity before acting — don't pick silently.** Multiple valid interpretations require an explicit question or stated assumption with risk.
> **Assert the outcome your system owns, not the intermediate state your infrastructure owns.** When verifying async work, assert the final business state — never the delivery/retry bookkeeping held in shared infrastructure that any co-running process can write. Such a check passes when run alone and flakes the moment anything else shares that infrastructure.
> **Keep shared guidance role-relevant.** Universal guidance must help every receiving skill or agent; code-specific obligations belong only in code-specific protocols.

<!-- /SYNC:ai-mistake-prevention -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Take a user prompt, or a workflow id, and spawn TWO brand-new AI sessions in parallel — one Claude Code, one Codex — each launched with xhigh effort and full-permission mode already applied, then auto-submit the prompt in both.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Critical Thinking:** traced proof per claim, confidence >80% to act, never guess as fact.

**IMPORTANT MUST ATTENTION** verify both CLIs are installed before spawning; never half-launch
**IMPORTANT MUST ATTENTION** set effort and full-permission mode via launch flags only — never via keystrokes into a running session
**IMPORTANT MUST ATTENTION** pass each prompt through its per-tool prompt file (`prompt-claude.txt` / `prompt-codex.txt`) read inside the launcher — never inline shell escaping
**IMPORTANT MUST ATTENTION** detect OS first (`uname -s`) and use the matching launcher/spawn branch
**IMPORTANT MUST ATTENTION** do not answer the prompt in the current session — orchestrate only
**IMPORTANT MUST ATTENTION** orchestrated mode: launch the runner ONCE in background, watch `status.json`, collect + compare outputs when it exits — never re-implement supervision inline and never busy-poll

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:START -->

## Hookless Prompt Protocol Mirror (Auto-Synced)

Source: `.claude/.ck.json` + `.claude/skills/shared/sync-inline-versions.md` (`:full` blocks) + `.claude/scripts/lib/hookless-prompt-protocol.cjs`

## [WORKFLOW-EXECUTION-PROTOCOL] [BLOCKING] Workflow Execution Protocol — MANDATORY IMPORTANT MUST CRITICAL. Do not skip for any reason.

**Generic portability boundary:** Reusable skills and protocol text stay project-neutral; project-specific conventions are discovered from docs/project-config.json and docs/project-reference/. Apply shared AI-SDD from `shared/sdd-artifact-contract.md`. Read `docs/project-config.json` and `docs/project-reference/docs-index-reference.md`, then open the project reference docs named there. For spec, test-case, behavior-change, public-contract, or `docs/specs/` work, route through the local spec docs named by the docs index: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`, and `workflow-spec-test-code-cycle-reference.md` when specs/tests/code must stay synchronized. If either file or a required reference doc is missing or stale, auto-run `$project-init` (or the narrow lower-level route such as `$project-config`, `$docs-init`, `$scan-all`, or `$scan --target=<key>`) before ordinary project-specific work. Any supported AI tool may execute when this shared context and local docs are available.

1. **DETECT:** If the prompt starts with an explicit slash skill/workflow command, execute it directly. Otherwise match the prompt against the workflow catalog and skill list.
2. **ANALYZE:** Choose the best option: execute directly, invoke a skill, activate a standard workflow, or compose a custom step combination.
3. **AUTO-SELECT:** Pick the best option yourself. Do not ask the user to choose between direct execution, skill, standard workflow, or custom workflow.
4. **ACTIVATE:** For a selected workflow, call `$start-workflow <workflowId>`; for a selected skill, invoke that skill; for a custom workflow, sequence custom steps directly; for direct execution, proceed with the task.
5. **CREATE TASKS:** task tracking for ALL workflow/skill/custom steps before execution when the selected path has multiple steps.
6. **PARALLELIZE:** Before executing the task list, tag each task `PAR` (independent inputs + write set disjoint from every other `PAR` task) or `SEQ` (name the blocking dependency), group `PAR` tasks into waves, declare the wave plan, and spawn each wave's sub-agents in ONE message — all-return barrier per wave, fan-out one level deep unless a sub-agent's own definition authorizes further fan-out. Sequential-by-default is a defect when tasks are independent; do not parallelize shared write targets, output-consuming tasks, trivial single-file work, ordering a skill or workflow explicitly fixes, or user-approval gates.
7. **EXECUTE:** Advance per the **Workflow Step Advancement & Parallel Phases** rule in your context instructions — model-driven; a sub-agent completion advances a step identically to an inline call; a parallel-phase group is an all-return barrier (advance only after ALL members return, never serialize it)

## Shared AI-SDD Protocol Markers

Source: `.claude/skills/shared/sync-inline-versions.md`

## SYNC:ai-sdd-artifact-contract

> **AI-SDD Artifact Contract** — Shared spec-driven development rules stay portable and source-owned.
>
> 1. Keep reusable AI-SDD principles in `.claude`; put repository-specific paths, commands, owners, products, and formats in project config/reference docs.
> 2. Preserve cycle: `spec -> plan -> tasks -> implement -> verify -> update spec/docs`.
> 3. Trace every requirement or invariant through decision, task, TC/test, source evidence, and docs/spec update.
> 4. Treat code-to-spec extraction as reference-only until accepted by the canonical spec owner.
> 5. Any supported AI tool may plan, implement, review, or verify with synced context; using multiple tools is optional.
> 6. Update `.claude` source first, then sync generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`. — why: mirrors are generated artifacts; hand-edits are overwritten on the next sync
> 7. If `docs/project-config.json`, root instruction files, or a required project-reference doc is missing or stale, auto-run `$project-init` or the narrow lower-level route before ordinary project-specific work.
>
> **Active reference:** `shared/sdd-artifact-contract.md` in the active skills root.

---

## SYNC:ai-sdd-artifact-contract:reminder

- **MANDATORY** Apply `shared/sdd-artifact-contract.md`; keep reusable AI-SDD in `.claude` and local rules in project docs.
- **MANDATORY** Code-to-spec extraction is reference-only until canonical acceptance; any supported AI tool may execute with synced context.
- **MANDATORY** Update `.claude` source before syncing generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`.
- **MANDATORY** Missing or stale project config, root instruction files, or required reference docs route project-specific work through `$project-init` or the narrow setup route automatically.
  **[TASK-PLANNING] [MANDATORY]** BEFORE executing any workflow or skill step, create/update task tracking for all planned steps, then keep it synchronized as each step starts/completes.

## [LESSON-LEARNED-REMINDER] [BLOCKING] Task Planning & Continuous Improvement — MANDATORY. Do not skip.

Break work into small tasks (task tracking) before starting. Add final task: "Analyze AI mistakes & lessons learned".

**Extract lessons — ROOT CAUSE ONLY, not symptom fixes:**

1. Name the FAILURE MODE (reasoning/assumption failure), not symptom — "assumed API existed without reading source" not "used wrong enum value".
2. Generality test: does this failure mode apply to ≥3 contexts/codebases? If not, abstract one level up.
3. Write as a universal rule — strip project-specific names/paths/classes. Useful on any codebase.
4. Consolidate: multiple mistakes sharing one failure mode → ONE lesson.
5. **Recurrence gate:** "Would this recur in future session WITHOUT this reminder?" — No → skip `$learn`.
6. **Auto-fix gate:** "Could `$code-review`/`$code-simplifier`/`$security-review`/`$lint` catch this?" — Yes → improve review skill instead.
7. BOTH gates pass → ask user to run `$learn`.
   **[CRITICAL-THINKING-MINDSET]** Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
   **Anti-hallucination principle:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.
   **AI Attention principle (Primacy-Recency):** Put the 3 most critical rules at both top and bottom of long prompts/protocols so instruction adherence survives long context windows.
   **Goal-driven execution:** Define success criteria first, loop until verified, and stop only when observable checks pass.
   **Tests verify intent:** Tests must protect business rules/invariants and fail when the protected intent breaks, not only mirror current behavior.

## Common AI Mistake Prevention (System Lessons)

- **Re-read files after context compaction.** Edit requires prior Read in same context; compaction wipes read state. Re-read before editing.
- **Grep for old terms after bulk replacements.** AI over-trusts find/replace completeness. Grep full repo after bulk edits for missed refs in docs/configs/catalogs.
- **Check downstream references before deleting.** Deletions cascade doc/code staleness. Map referencing files before removal.
- **After memory loss, check existing state before creating new.** Compaction wipes prior-work memory. Query current state to resume — never blindly duplicate.
- **Verify AI-generated content against actual code.** AI hallucinates APIs, class names, method signatures. Grep to confirm existence before documenting/referencing.
- **Trace full dependency chain after edits.** Changing a definition misses downstream consumers. Trace the full chain.
- **When renaming, grep ALL consumer file types.** Some file types silently ignore missing refs (no compile error). Search code, templates, configs, generated files.
- **Trace ALL code paths when verifying correctness.** Code existing ≠ code executing. Trace early exits, error branches, conditional skips — not just happy path.
- **Update docs that embed canonical data when source changes.** Docs inlining derived data (workflows, schemas, configs) go stale silently. Update all embedding docs alongside source.
- **Verify sub-agent results after context recovery.** Background agents may finish while parent compacted — grep-verify output, don't trust assumed completion.
- **Cross-check full target list against sub-agent assignments.** Parallel sub-agents by category miss boundary items. Reconcile union of assignments against target list before proceeding.
- **Sub-agents inherit knowledge only from their agent .md definition — use custom agent types, not built-in Explore.** Tool adoption = permission + knowledge + enforcement (numbered workflow step).
- **Persist sub-agent findings incrementally, not as a final batch.** Long sub-agents hit cutoffs before final write — findings lost. Instruct append-per-section to report file.
- **When debugging, ask "whose responsibility?" before fixing.** Trace caller (wrong data) vs callee (wrong handling). Fix at responsible layer — never patch symptom site.
- **Test failure → record a provisional verdict before trace/edit, then investigate.** Use the full five-way taxonomy: SOURCE-WRONG (production violates intent), TEST-WRONG (assertion/setup is stale), TEST-NOT-OPTIMAL (valid but fragile or low-signal test), ENVIRONMENT-BLOCKED (external state prevents a verdict), or AMBIGUOUS (intent/evidence cannot choose safely). Then trace root cause and triangulate against the governing spec (`docs/specs/**` if one exists) AND source. NEVER weaken an assertion, add a skip, relax a timeout, or change source merely to force green.
- **Grep ALL removed names after extraction/refactoring.** Primary file "done" ≠ secondary files clean. Grep entire scope for every removed symbol before declaring complete.
- **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Pattern-matching as "wrong" skips context. Before changing or reporting any constant/limit/flag/cutoff: read comments, git blame, the CALLER's ordering (the guarantee that makes the value correct usually lives in code running immediately BEFORE the cited line), and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard — and in a validation pass, an accurate `file:line` citation proves the transcription, never the defect.
- **Verify ALL affected outputs, not just the first.** One build green ≠ all green. Multi-stack changes (backend/frontend/tests/docs) require verifying EVERY output.
- **Evaluate fit before copying a nearby pattern.** Closest example ≠ matching preconditions — verify the new context shares the same constraints, base classes, scope, lifetime.
- **Holistic-first debugging — resist nearest-attention trap.** Don't dive into first plausible cause. List EVERY precondition (config, env vars, paths, DB, endpoints, creds, versions, DI, data). Verify each against evidence (grep/query — not reasoning). Ask "what would falsify this?" — if nothing, it's not a hypothesis. Most expensive failure: going deeper in "obvious" layer while bug sits in layer never questioned.
- **Surgical changes — apply the diff test (context-aware).** Two modes: (1) Bug fix → every line traces to the bug; no restyling; orphan cleanup only for imports YOUR changes made unused. (2) Review/enhancement → implement improvements AND announce as "Enhancement beyond main request: [what]". Never silently scope-creep. Diff test: "Would this line exist if I wasn't asked to do X?" — if no, delete or announce.
- **Surface ambiguity before coding — don't pick silently.** Multiple valid interpretations → present each with effort: "[Request] could mean (1) [N h], (2) [N h]. Which matters?" List scope/format/volume/constraints assumptions first. If simpler path exists, say so. Never silently pick.
- **[MANDATORY FIRST ACTION] ALWAYS activate a suitable skill or workflow BEFORE responding.** Match task against workflow catalog + skill list; invoke via skill invocation or `$start-workflow <workflowId>`. NEVER answer or write code before checking. Skip = protocol violation.
- **Why-Review adversarial mindset — apply when reviewing any plan, decision, or design.** Default SKEPTIC not VALIDATOR: steel-man a rejected alternative, invert each stated reason ("what does it sacrifice?"), stress-test top 2-3 assumptions, run pre-mortem ("ships, fails in 3 months — what breaks?"), surface 1-2 alternatives author missed. Section presence ≠ quality; quality = causal reasoning + concrete mitigations + evidence, not "it's better" or "monitor closely".
- **Front-load report-write in sub-agent prompts for large reviews.** Many-file sub-agents hit budget before final write — findings lost. Design prompts so: (1) report-write is first explicit deliverable, (2) append per-file/section (not batched), (3) scope bounded so reads don't exhaust budget. Truncated mid-sentence with no report file → spawn narrower scope, don't retry same prompt.
- **After context compaction, re-verify all prior phase outcomes before continuing.** Summaries describe intent, not environment state (git index, filesystem, processes). On resume, FIRST audit: git status, re-read modified files, verify filesystem. Every "completed" claim is an untested hypothesis until evidence confirms.
- **OOM/memory: check row count before row size.** Triage: (1) Unbounded query — no DB filter for trigger? Push filter to DB; eliminates OOM. (2) Large rows? Projection reduces proportionally. Row reduction > projection in ROI.
- **Assert the outcome your system OWNS, never the intermediate state your INFRASTRUCTURE owns.** When testing anything asynchronous (queue/broker delivery, retries, background jobs, caches, replication), assert the final business/entity state. NEVER assert the delivery bookkeeping — consume/send status, attempt counts, last-error, row existence or counts in a broker, scheduler, or outbox/inbox table. That bookkeeping lives in shared infrastructure that ANY co-running process (a peer worker, a second replica, a leftover local container) can write, usually under a deterministic shared key, so the assertion silently tests the developer's environment instead of the system: green when run alone, flaky the instant anything else shares that broker + database. Gate question for every assertion: "would this hold no matter WHICH process did the work?" — if no, assert the converged data state instead. Corollary: process-local fault injection and in-process telemetry cannot gate work any process may perform — use them as stress amplifiers (arm → bounded window → disarm → assert convergence), never as preconditions.
- **Keep domain concepts out of generic/shared/infrastructure layers.** Reusable layer (shared library, framework, infra module) must reference NO consumer-specific domain concept — tenant/customer/product IDs, business entities, feature rules. Leak compiles + runs → passes review silently while coupling the "reusable" layer to one consumer. Keep shared type domain-free; push domain fields/logic down into the consumer via subclass/composition. — why: a layer coupled to one consumer's domain is no longer reusable.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:END -->
