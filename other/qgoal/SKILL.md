---
name: Qgoal
description: Explicit single-Goal alias for Qplan. Use when the user enters Qgoal with the active client prefix.
invocation_trigger: When the user enters `/Qgoal {goal}` or `$Qgoal {goal}`.
user_invocable: true
recommendedModel: haiku
---

# Qgoal — Explicit Single-Goal Qplan Alias

Use `/Qgoal {목표}` in Claude or `$Qgoal {목표}` in Codex to request Full SIVS for one Goal. Qgoal delegates the unchanged intent to Qplan; it is not a separate workflow or an automatic natural-language route.

Ordinary requests remain on the native client path even when they are long, mention many files, or contain planning and risk words. QE may recommend Qplan, but only an active-prefix Qplan or Qgoal invocation activates Full SIVS.

Legacy `!direct` and `!full` tokens do not change this contract: explicit Qgoal remains Full SIVS and ordinary prose remains native.

## Execution Procedure

Step 1 — Ensure the shared `QE.md` and active-client instruction pointer exist. The explicit
`/Qgoal` or `$Qgoal` entry bootstrap creates missing files without overwriting user instructions.
Then delegate the original Goal text to Qplan. If UserPromptSubmit injected a `[QE GOAL]`
hint, treat it as workflow admission context, not as authorization.

Step 2 — Resolve the target Plan. Create a one-Goal Plan or add the Goal to an active compatible Plan. If the intent contains multiple independently verifiable outcomes, Qplan may split it into ordered Goals rather than pretending it is atomic.

Step 3 — Enter `Qplan` and run the selected Goal's internal pipeline. `Qgoal` must
preserve Qplan's machine-validated assurance lane before reporting it complete:

```text
Qplan knowledge preflight
  → lane selection
      ├─ bounded micro: immutable acceptance contract → bounded implementation
      └─ formal: Qgenerate-spec (TASK_REQUEST + VERIFY_CHECKLIST) → Qexecute
  → independent verification and Goal-alignment evidence
  → Qplan completion evidence and verified knowledge write-back
```

Formal-lane `Qgenerate-spec` and `Qexecute` stages are internal components, not
separate user commands. A bounded-micro lane is valid only with the immutable
ledger admission declared in `core/GOAL_ACCEPTANCE_CONTRACT.md`; Qgoal cannot
infer or issue it. Preserve the active Plan/Goal and any generated UUID across
the selected stages. On scope growth, risk discovery, execution failure, or
verification failure, Qplan blocks the immutable micro Goal through the audited
transition and creates a linked formal successor Plan/Goal with a fresh contract;
Qgoal never rewrites the original lane or silently continues.

Qplan is the sole owner of tacit-knowledge intake before this pipeline. Qgoal
delegates the original intent and client mode unchanged, then consumes Qplan's
confirmed synthesis or blocker. It must not create a second question inventory,
format progress labels, maintain interview counters, infer skipped material
answers, or reproduce intake state transitions.

Step 4 — Marker handling: a `goalRuntime` marker records explicit workflow admission. It is not a security authorization boundary. If marker persistence fails, retain the Plan as blocked rather than silently executing an internal stage outside the Plan contract.

Step 5 — Report the Plan and current Goal, not a chain of commands. Ask only for material scope, risk, or irreversible decisions.
