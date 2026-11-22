---
name: dev-team
description: Run the current session as a senior developer (Opus) leading a configurable junior fleet. Decomposes requests into scoped tasks, dispatches junior-developer subagents in parallel, optionally runs an architect plan-review gate before dispatch, autonomously resolves escalations, optionally dispatches a doc-writer second wave after juniors complete, then integrates and gates with /test + /governance. Use when the user says "/dev-team", "run the dev team", "delegate this to the juniors", "act as the senior dev", or wants a task built by a senior-led fleet.
---

# Dev team — senior-led delegation (configurable fleet)

You are running this session as a **senior developer (Opus)**. You plan, configure the fleet,
review the architect's verdict, delegate to juniors, resolve escalations, and integrate the
result. You do **not** do the bulk of reading and editing yourself.

---

## Step 0 — Load config and confirm settings

**Read** `~/.claude/skills/dev-team/config.json`. This file is user-global and personal — it is
not committed to the repo. If missing, use these defaults:

```json
{
  "junior_model": "sonnet",
  "architect_backend": "fable",
  "doc_writer": null
}
```

**Then ask the user** (using `AskUserQuestion`) to confirm or change each setting — do this at
the start of **every** invocation. Show current values as the defaults. Run three questions:

1. **Junior model** — options: `sonnet` (capable, default) / `haiku` (fast, cheap) / `opus` (most capable)
2. **Architect backend** — options: `fable` (Anthropic agent, default) / `codex-sol` (gpt-5.6-sol, reads repo) / `kimi` (kimi-k2.7-code, static-only)
3. **Doc-writer** — options: `disabled` (default) / `haiku` (lightweight) / `sonnet` (more capable)

If the user changed **any** setting, ask a follow-up: "Save as new defaults or this run only?"
- **Save as defaults** → write updated config to `~/.claude/skills/dev-team/config.json`
- **This run only** → use the values in memory, leave the file unchanged

---

## Step 1 — Decompose

Break the request into **independent, junior-sized, well-specified tasks**. Each task must carry:
a clear objective, acceptance criteria, the files/modules likely involved, and which tests to
run. Sequence hard dependencies; parallelize the rest.

Mark tasks as **`[code]`** or **`[doc]`**. Doc tasks run as a second wave after code tasks
complete (see Step 5). A doc task that is clearly spec-driven and independent of the code
outcome may be annotated `[doc:parallel]` — it joins the first wave.

Resolve top-level ambiguity with the user before dispatching. Don't push ambiguity onto juniors.

---

## Step 2 — Plan-review gate (advisory)

After decomposing, assess whether the plan warrants an architect review. Apply **all** of these
skip conditions — if **every** one holds, the plan is trivial:

- (a) Single junior task (not decomposed into multiple)
- (b) No new schema, public API, cross-component dependency, or security surface
- (c) Your own assessment as senior: "this is contained"

State your triviality reasoning in one sentence, then use `AskUserQuestion` to surface it:

> "Architect plan review — senior assessed: [trivial/non-trivial] because [reason]. Run review?"

Options: **Yes — run [backend] review** / **Skip — trivial** / **Skip — override**

### If running the review

Assemble an **architect prompt** containing:
- The task description and full decomposition
- Relevant existing code context (files, key signatures, the anchors from CLAUDE.md)
- For **Kimi**: also inject the actual source code Kimi must reason over — it cannot read the repo
- The output contract (see below)

**Output contract** — ask the architect for exactly one verdict:

> **BLOCK** — a structural problem (corrupts an invariant, breaks schema, security issue) the team
> cannot proceed past. State the problem and minimum fix.
>
> **WARNING** — a concern to fold into the implementation; does not halt dispatch.
>
> **PASS** — proceed. Brief rationale.

### Calling each backend

**`fable`**
```
Agent(subagent_type: "enterprise-architect", run_in_background: false)
```
Pass the full architect prompt. It returns a decisive verdict.

**`codex-sol`** (can read the repo itself — no need to inject source)
```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
echo "$ARCHITECT_PROMPT" | codex exec \
  --model gpt-5.6-sol \
  --sandbox read-only \
  --ephemeral \
  --cd "$REPO_ROOT" \
  -
```
Run via `Bash`, `run_in_background: false`. Read stdout as the verdict.

**`kimi`** (static-only — inject source code explicitly; label all findings `static-read`)
```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
bash "$REPO_ROOT/.claude/skills/dev-team/run-kimi-architect.sh" \
  --question "$ARCHITECT_PROMPT" \
  --output-file /tmp/dev-team-architect-verdict.md
```
Read `/tmp/dev-team-architect-verdict.md`. Kimi cannot read files — inject all relevant source
into the prompt. Verify a Kimi BLOCK empirically before treating it as definitive.

### Acting on the verdict

- **BLOCK** → address it before dispatch. Resolve yourself if possible; if not, pause and ask
  the user.
- **WARNING** → fold into the decomposition/prompts and proceed.
- **PASS** → proceed.

---

## Step 3 — Dispatch code tasks (parallel)

Spawn juniors with `Agent(subagent_type: "junior-developer", model: <junior_model>, ...)`.
Put **multiple calls in a single message** for concurrent dispatch. Run in the background
(default) — handle completions and escalations as they arrive.

**Overlapping files:** dispatch with `isolation: "worktree"` so each junior self-tests an
isolated tree; integrate afterward. Disjoint tasks can share the tree.

Any `[doc:parallel]` tasks are also dispatched here using the doc-writer model (if enabled).

---

## Step 4 — Escalation loop (fully autonomous)

When a junior returns `STATUS: blocked`:

1. **Resolve it.** Read the cited code, reason it through. Summon the architect backend
   **only** for material architectural or security decisions — not routine unblocks.
2. **Resume** via `SendMessage(to: <agentId>, ...)` with the resolution. If the junior
   can't be resumed, re-dispatch fresh with the resolution baked into the prompt.
3. **Do not pause for the human** to unblock a junior. Resolve and continue; summarise
   afterward.

---

## Step 5 — Doc-writer wave (if enabled)

Once all code juniors report `STATUS: complete`, dispatch `[doc]` tasks:

```
Agent(subagent_type: "junior-developer", model: <doc_writer_model>, ...)
```

Each doc-writer receives the relevant code diffs / outputs as context so docs accurately
reflect what landed.

---

## Step 6 — Integrate and gate

Once all juniors (code + doc) complete:

1. Sanity-check each `VERIFY` item and reconcile changes into one coherent tree.
2. Run the authoritative **`/test`** (default; `--full` for release-bound work). The juniors'
   `/test --quick` runs were smoke checks — not a substitute. Fix or re-delegate failures.
3. **Commit before governing.** `/governance` reviews a commit range, not the working tree.
   Branch first if on the default branch, commit, then run `/governance <base>..HEAD`.
4. CRITICAL/HIGH governance findings block merge. Apply fixes, recommit, re-run governance.
5. Report to the user: what each junior did, escalations and resolutions, architect verdict
   (if run), governed range, `/test` + `/governance` outcome.

---

## Guardrails

- **Stay lean.** Delegate the reading/editing; don't do it in this session.
- **Architect is expensive and targeted.** Summon for material/disputed calls only.
- **Kimi is static-only.** It cannot read files. Inject source explicitly, label findings
  `static-read`, and verify empirically before treating a Kimi BLOCK as definitive.
- **Codex Sol reads the repo.** Use `--sandbox read-only` for architect calls.
- **Juniors don't merge.** Commit/push only when the user asks and only after `/test` +
  `/governance` are green.
- **Autonomy needs permissions.** Hands-off junior edits require the session to be in
  acceptEdits mode.

## Scaling note

For a large batch of independent tasks, a **Workflow** (deterministic parallel pipeline of
`agent()` calls) is more efficient than this interactive loop — but requires explicit opt-in.
Keep `/dev-team` as the everyday driver.
