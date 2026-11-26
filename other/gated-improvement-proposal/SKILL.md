---
name: gated-improvement-proposal
description: Every self-edit of the harness (rule/CLAUDE.md/prompt/hook) becomes a PROPOSAL that passes a gate before being applied — never a sensitive auto-merge
---

> **Auto-Trigger:** When about to modify the harness itself — a rule, CLAUDE.md, a system prompt, a hook, settings, or the agent's policy
> **Keywords:** "update rule", "edit CLAUDE.md", "self-improvement", "change the hook", "change prompt", "self-improve", "evolve the agent"
> **Priority:** HIGH
> **Tools:** Read, Write, Edit, Bash
> **Related doctrine:** `rules/partial-autonomy-slider.md` (levels 0-5), `rules/loop-maker-checker.md` (proposal ≠ who approves).

# gated-improvement-proposal — the harness changes itself UNDER a gate

Self-editing a rule/CLAUDE.md/prompt without validation corrupts the harness; requiring a human for everything stalls evolution. The way out is the **gate**.

## Contract

**INPUT:** proposed diff + rationale + testable acceptance criterion.

**OUTPUT:** change applied (if the gate is green AND below the autonomy ceiling) OR proposal in the `gate-sheet` (if the gate is red OR the path is sensitive).

**EXIT CODES** (from `done_gate.py`, run as a gate BEFORE applying):

| Exit | Meaning |
|---|---|
| 0 | DONE — criterion passed; may apply (if autonomy allows) |
| 1 | NOT-DONE — criterion failed; do NOT apply, it becomes a proposal |
| 2 | invalid use of done_gate |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| `operator-profile.yaml` (`autonomy.by_action`, `autonomy.sensitive_paths_auto_gate`) | Reads | decides auto-apply vs propose |
| target rule/CLAUDE.md/hook/prompt | Writes (if gate green + autonomy allows) | the change itself |
| `gate-sheet` | Writes (if gate red or sensitive path) | proposal pending a human |

## Process
1. **Make it a PROPOSAL**, not a direct edit: `diff` + rationale + **testable acceptance criterion** + which `autonomy.by_action` applies.
2. **Run the gate BEFORE applying:** `python ${CLAUDE_PLUGIN_ROOT}/scripts/done_gate.py --profile <type>` (or your project's existing eval suite). Reuse the existing runner — **do not reimplement eval**.
3. **Consult the autonomy** in `operator-profile.yaml`:
   - `autonomy.by_action.auto_edit_harness` (default 1) decides auto-apply vs propose.
   - Any target in `autonomy.sensitive_paths_auto_gate` (`settings*.json`, `.claude/hooks/**`, `**/.env`, `.claude/rules/**`) = **forced human gate, never auto-merge**.
4. **Apply only if** the gate is green **AND** below the autonomy ceiling; otherwise deliver it as a PR/proposal in the `gate-sheet`.
5. **Record** the change (traceable: what changed, why, which eval passed).

## When NOT to Activate
- Editing ordinary domain content (non-harness) — normal flow.
- When no eval/criterion is possible — do not auto-apply; make it a human gate.

## Executed examples

```console
$ python scripts/done_gate.py "python -c \"print(1)\""
  [OK ] (exit 0) python -c "print(1)"

DONE-GATE: DONE (1/1 criteria)
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python scripts/done_gate.py "python -c \"import sys; sys.exit(1)\""
  [FAIL] (exit 1) python -c "import sys; sys.exit(1)"

DONE-GATE: NOT-DONE (0/1 criteria)
  no pending-work declaration. If this is PARTIAL, declare what is missing
  (--declare-partial "..."); if it is a FAILURE, fix it. Silence is not a state.
```
<!-- executed: 2026-10-30 · exit=1 -->
(criterion failed → the proposal does NOT self-apply; it becomes a gate-sheet item, exactly step 4.)

```console
$ python scripts/done_gate.py --json "python -c \"import sys; sys.exit(0)\""
{
  "done": true,
  "state": "DONE",
  "partial": false,
  "declared": null,
  "results": [
    {
      "cmd": "python -c \"import sys; sys.exit(0)\"",
      "passed": true,
      "exit_code": 0,
      "tail": ""
    }
  ]
}
```
<!-- executed: 2026-10-30 · exit=0 -->

## Proof

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/done_gate.py --self-test
```

## See also
`done_gate.py` (the gate), `partial-autonomy-slider` (levels 0-5), `distill_corrections.py` (the most common source of rule proposals).
