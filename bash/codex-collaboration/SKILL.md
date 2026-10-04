---
name: codex-collaboration
description: Take over, hand off to, or collaborate with an OpenAI Codex CLI session from Claude Code or another agent. Use when the user says "read the codex session", "take over codex's work", "hand this to codex", "let codex continue", "fork/resume the codex thread", "what was codex doing", or when Codex quota is exhausted and another agent must continue its task. Reads rollout JSONL read-only, writes curated handoff packets, gates every Codex launch on quota, and drives codex exec/resume/queue safely.
---

# Codex Collaboration

Three modes, one rule: the Codex rollout is private append-only evidence. Read it, never write it, never kill the process that owns it.

| Mode | Direction | When |
| --- | --- | --- |
| Takeover | Codex -> you | Codex is stalled, out of quota, or the user asks you to continue its task |
| Handoff | you -> Codex | The user wants Codex to continue, or Codex owns a tool/login/skill you lack |
| Collaboration | both | Split work: you plan/verify, Codex executes a bounded task (or vice versa) |

## Setup

```bash
SKILL_DIR="$HOME/.claude/skills/codex-collaboration"   # or ~/.codex/skills/... or LazySkills/skills/...
CS="$SKILL_DIR/scripts/codex_session.py"
```

Read every applicable `AGENTS.md` and `~/.codex/AGENTS.md` before touching the project a session names. `~/.codex/AGENTS.md` carries the shared-workstation runtime and cleanup policy.

## Safety Rules

- Never open a rollout JSONL for writing, never truncate or "repair" it, never copy it into a Git repo.
- Never touch `~/.codex/state_*.sqlite`, `thread_history_*.sqlite`, `history.jsonl`, or lock files.
- Never kill a `codex`, tmux, IDE, or app-server process that owns a rollout (`$CS find NAME` shows `owners`). Ask the user to close or detach it.
- Every Codex launch spends the user's quota. Run `$CS quota` first; the `delegate` and `queue` subcommands refuse below 5 % remaining unless `--skip-quota-check` is passed with the user's explicit consent.
- Do not change model or reasoning effort unless the user asked for that exact change.
- Raw prompts, transcripts, handoffs with private detail, and extracted text stay under `~/.codex/handoffs/` or another ignored private folder. Tracked docs get curated facts only.
- Quota, auth, and compaction failures are reported, not retried in a loop.
- For stalled or multi-gigabyte threads that must keep running inside Codex, use `codex-session-recovery` (official app-server compaction). This skill only reads and hands off.

## Where Codex Keeps Things

| Item | Path |
| --- | --- |
| Session index (thread names) | `~/.codex/session_index.jsonl` (append-only; last row per id wins) |
| Rollout transcript | `~/.codex/sessions/YYYY/MM/DD/rollout-<start>-<UUID>.jsonl` |
| Fork lineage | `session_meta.payload.forked_from_id` in the rollout's first line |
| Skills Codex loads | `~/.codex/skills/<name>/SKILL.md` (mirrors `../LazySkills/skills/`) |
| Config, model, effort | `~/.codex/config.toml` (`model`, `model_reasoning_effort`, `[projects.*] trust_level`) |
| Private handoffs | `~/.codex/handoffs/` |
| Quota probe (no tokens) | `agentic_tools/wechat_gui_agent/scripts/codex_quota_status.py status --json` in AgenticApp |

Rollout event types worth knowing: `session_meta`, `response_item` (`message` with `role`, `function_call`/`custom_tool_call` and their `_output`, `reasoning` summaries), `compacted` (context-compaction summary), `event_msg` (`thread_goal_updated`, `turn_aborted`, `token_count`). A `turn_aborted` user item with no preceding request usually means the user pressed Esc on an idle turn, not that work was lost.

## Mode 1: Takeover

1. Identify the thread and its owner:

```bash
python3 "$CS" list --limit 10
python3 "$CS" find "LabCanvas-CAD"          # name, UUID, or UUID prefix
```

2. Read the ending first, then the whole story:

```bash
python3 "$CS" tail "LabCanvas-CAD" -n 20                 # last user/assistant messages (tail scan, fast)
python3 "$CS" tail "LabCanvas-CAD" -n 60 --all           # include tool calls and reasoning summaries
python3 "$CS" extract "LabCanvas-CAD" --out ~/.codex/handoffs/labcanvas-cad-extract --transcript
python3 "$CS" extract UUID --since-line 390060 --out ...  # only the part after a fork point
```

Multi-gigabyte rollouts take minutes to stream. Delegate the extracted files to subagents by time range when the transcript exceeds what you can read; ask each for a chronological narrative, every numeric decision with its provenance, user corrections verbatim, files and commands touched, and open issues.

3. Verify against disk before believing the transcript: `git log`, `git status`, the design/run folders, and the latest dated reference notes. The transcript explains intent; files are ground truth.

4. Write the handoff packet (skeleton, then fill "Verified facts" and "Open work" yourself):

```bash
python3 "$CS" handoff "LabCanvas-CAD" --out ~/.codex/handoffs/labcanvas-cad-takeover.md --include-compaction
```

Put a curated, non-private version under the project's tracked `references/` when the project keeps dated handoff notes there.

5. Continue the work in your own session. Leave the Codex thread as the archive. If the user later resumes Codex, point it at the handoff packet in its first message.

## Mode 2: Handoff To Codex

1. Write the packet (template in `references/handoff-packet-template.md`): objective, verified state, exact paths, commands, ownership boundaries, stop conditions, evidence. Codex reads files well; it does not see your conversation.
2. Check quota: `python3 "$CS" quota` (add `--probe` to refresh from the app server).
3. Choose the entry point:

| Situation | Command |
| --- | --- |
| Fresh bounded task, capture the result | `python3 "$CS" delegate --cwd DIR --prompt-file packet.md "-"` or `codex exec -C DIR --json -o last.md "PROMPT"` |
| Continue an existing thread non-interactively | `codex exec resume UUID-or-name "PROMPT"` (or `$CS delegate --resume NAME`) |
| Interactive session for the user, in tmux | `tmux new -d -s codex-NAME -c DIR "codex resume UUID-or-name"` |
| Send a message into a live interactive session | `python3 "$CS" queue --thread NAME --message "..."` |
| Branch without disturbing the original | `codex fork UUID "PROMPT"` (interactive) or `codex exec fork UUID "PROMPT"` |

`codex exec` sandboxes: `read-only`, `workspace-write` (default here), `danger-full-access`. Only pass `--full-auto` (bypass approvals and sandbox) when the user runs Codex that way already, as their TUI status line shows.

4. Report the returned last message and event file path to the user; do not paraphrase it as your own verification.

## Mode 3: Collaboration

- Split by ownership, not by turn: one agent owns each file tree, service, device, or run folder. Write it down in the packet's "Ownership boundaries".
- Exchange through files, not chat: packets under `~/.codex/handoffs/`, results under the project's `output/` or `runs/` conventions, commits with clear messages.
- Poll a Codex run through its `--json` event file or `tail`, never by reading the rollout mid-write with a full extract.
- When both agents may commit to the same repo, each rebases before committing and never resets or reverts the other's changes.
- Use `aginti-agentlink` conventions when more than one machine or repo is involved.

## Reporting

State plainly: which thread was read, where it stopped, what was verified on disk, what you changed, what remains, and whether any Codex quota was spent.
