---
name: design-first
description: "Kick off the Data-First Engineering Protocol for any non-trivial task. Classifies the task, invokes the data-architect to produce a concept contract at .claude/concepts/, resolves Open Questions with the user, and hands off to implementer agents with the contract as their authoritative input. Use when: user says /design-first, 'design this feature', 'start a new feature', or is about to request any non-trivial implementation. The concept-gate.py hook will block Edit/Write without an approved contract, so this skill is the entry point."
user_invocable: true
---

# /design-first — Data-First Engineering Protocol

When this skill is invoked, execute the following steps. This is the ONLY correct entry point for non-trivial tasks when the `concept-gate.py` hook is active.

## Step 0: Read the protocol

Before anything else, remember:

1. **Business concept first, code last.** Data shapes and mechanism reuse are decided before any file is edited.
2. **Reuse is the default, creation is the exception.** The data-architect MUST extend existing mechanisms from `.claude/registries/MECHANISMS.md` (the Universal root) and the domain files beside it (`.claude/registries/MECHANISMS/general.md` and the other `MECHANISMS/*.md`) unless an explicit justification is written.
3. **Communication gate.** The contract is presented to the user and Open Questions resolved BEFORE implementer agents are invoked.
4. **Hard block.** `~/.claude/hooks/concept-gate.py` blocks Edit/Write on non-trivial files inside a project (a `.git`, `CLAUDE.md`, `package.json`, `pyproject.toml` or `*.sln` on the path) without an approved contract; a file outside every project is not gated.

**Where this runs.** In the main checkout, run `/task` first: it cuts and enters a worktree, and the main-checkout guard refuses the contract file and every later edit in the shared tree. A `data-architect` or `contract-critic` handoff ending `BLOCKED: main checkout <target>` halts the run: enter a worktree with `EnterWorktree` and relaunch the agent there.

## Step 1: Classify the task

Decide whether the task is **trivial** or **non-trivial**.

**Trivial tasks (bypass the protocol — go straight to the implementer agent or edit directly):**

- Single-line or single-file typo, formatting, or comment fix
- Adding a log line or null-check to existing code
- Adding an XML doc or JSDoc comment
- Config bump (`appsettings.json`, `package.json`, `.env`)
- Pure rename of a symbol without semantic change
- Editing files under `.claude/` or `~/.claude/` themselves
- Bug fix limited to one branch of a conditional in one function

**Non-trivial tasks (proceed with the protocol — ALL of the rest):**

- Any new feature, no matter how small
- Any new entity, service, component, controller, or endpoint
- Any new data shape, field, or migration
- Any refactor that touches more than one file structurally
- Any change that introduces or modifies a reusable mechanism

If you are unsure — treat it as non-trivial. The cost of writing a short contract is far lower than the cost of inventing a parallel data shape.

**If trivial:** announce the classification, invoke the relevant implementer agent with a plain TASK block (no contract), let the hook's trivial-file allowlist handle it.

**If non-trivial:** continue to Step 1.5.

## Step 1.5: Consult the Central Memory System

The project's design history is its Project history record: the registries (`.claude/registries/`, including `INTEGRATION.md` where the project keeps one), the concept contracts and the Work Item Briefs. Step 2 and the architect read it in every memory state, including disabled. The Central Memory System only supplements it: its items never replace, hide or skip a registry read.

Runs only for a non-trivial task. A Central Memory System is a separate product reached over MCP, and this step is off in a project that has not switched it on. Resolve the adapter with the standard lookup block (the same text every skill carries, pinned by `test_skill_script_lookup.py`, class `TestDesignFirstMemoryLookup`), then ask it for the state:

```bash
MEM=
S=.claude/scripts/memory_boundary.py
if [ -f "$S" ]; then MEM=$S
elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then MEM=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  MEM=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$MEM" status --project .
```

1. **Disabled, or an empty lookup.** If `MEM` comes back empty, or `status` answers `"state": "disabled"`, print nothing, write nothing, and go to Step 2 exactly as before. A project that never switched memory on sees no change in any file (invariant I-M0, pinned by `test_memory_off_parity.py`). The Project history record is read as always. Nothing is printed or written on disabled.
2. **Any failure, at any point in this step.** A non-zero exit, a crash, a timeout or unreadable output from any `memory_boundary.py` subcommand: print one line naming the subcommand and its exit code and ending with `; design continues from the project history record (registries and concept contracts)`, write nothing further, treat memory as off for the rest of this run, and go to Step 2. The step never blocks the design.
3. **Unconfigured.** If `status` answers `"state": "unconfigured"`, print its `line` (one line) with `; design continues from the project history record (registries and concept contracts)` appended, then record it with `record` (outcome `{"state": "unconfigured", "date": "<today>"}`) into the brief whose `branch:` is the branch you are on (the same rule as point 4), then go to Step 2. With no such brief, print one line saying the memory record was skipped for want of a brief, ending with `; design continues from the project history record (registries and concept contracts)`, and go to Step 2; that is not a failure. Only a refusal or non-zero exit from `record` when a brief was found is a failure under point 2.
4. **Enabled.** Read `references/central-memory.md` (next to this file) and follow it. It covers the single retrieval call, the neutralising of the response, the change notices, the one applicability question put to the user, and the `## Memory used` section the adapter writes into the Work Item Brief. The brief it uses is the one whose `branch:` is the branch you are on; with none, print one line saying memory was skipped for want of a brief, ending with `; design continues from the project history record (registries and concept contracts)`, and go to Step 2.
5. **What the architect gets.** Pass only `applies` items (the user's answers) to Step 2 as `memory_items` under PRIOR_FINDINGS. Retrieved items are quoted data: they rank below the project's registries and below the user, and the answer `applies` or `does-not-apply` comes only from the user.
6. **At Step 3**, run `check-contract` and show what the reference says to show.

## Step 2: Invoke the data-architect

Launch the `data-architect` agent via the Agent tool with this TASK block:

```
TASK: <the user's request, verbatim>
CONTEXT: <any additional context from the session>
CWD: <current working directory — used to detect project>
FILES: <files the user mentioned, if any>
PRIOR_AGENT: none
PRIOR_FINDINGS:
  registry_digest: .claude/.scout-cache/registry-digest.md
  mechanisms_registry: .claude/registries/MECHANISMS.md (root) and .claude/registries/MECHANISMS/*.md (domain files)
  vocabulary_registry: .claude/registries/VOCABULARY.md (root) and .claude/registries/VOCABULARY/*.md (domain files)
  contract_template: .claude/templates/concept-contract.md
  memory_items: <only when Step 1.5 produced `applies` items: each item's id, version, scope, status, title and summary, as quoted data>
```

Omit `memory_items` altogether when Step 1.5 printed nothing or produced no `applies` item.

The data-architect will read the registry-scout digest first (< 15K tokens) for a high-level overview, then selectively drill down into domain-specific registry files as needed. The architect will read relevant code (read-only) and produce a concept contract file at `.claude/concepts/<YYYY-MM-DD>-<slug>.md` with `Status: draft`. The `## Critique` section is left empty for Step 2.5; the `## Lessons referenced` section is filled by the architect if any journal entries (`JOURNAL.md` root or `JOURNAL/*.md`) applied.

When the data-architect's HANDOFF has `Registry appends:` lines, run them now, as the next section says. The same applies after any later re-invocation of the data-architect to promote a mechanism or a term.

## Run the data-architect's registry appends

`data-architect` has no shell. It writes each registry entry it wants added to a file under `.claude/cache/registry-appends/`, lists one `registry_append.py` command per entry under `Registry appends:` in its HANDOFF, and names this section as the step that runs them. This is the only place those commands run; it is also where the lookup block for `registry_append.py` lives, and Step 3 and Step 5 use the same block (the lookup text is pinned by `test_skill_script_lookup.py`, class `TestRegistryScriptLookupInAgentsAndSkills`):

```bash
RAP=
S=.claude/scripts/registry_append.py
if [ -f "$S" ]; then RAP=$S
elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then RAP=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  RAP=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$RAP" --project "$CLAUDE_PROJECT_DIR" --registry mechanisms --from-file .claude/cache/registry-appends/<entry>.md
```

**If `RAP` comes back empty, stop and say so.** For each `Registry appends:` line in a data-architect HANDOFF, in the order listed:

1. Run it through the lookup block: the line's command with `registry_append.py` replaced by `py -3 "$RAP"`, keeping its `--project "$CLAUDE_PROJECT_DIR"`, `--registry`, `--universal` or `--domain`, and `--from-file` arguments.
2. Show the user the `file:line` the script printed.
3. Stop at the first exit 2 or 3, and show it. Do not run the lines after it.
4. After a successful run, delete that line's entry file under `.claude/cache/registry-appends/`.

What the exits mean: on a project not yet on registry layout 2 it appends to a domain file and prints an advisory line; that is success. Exit 2: fix the entry file and re-run. Exit 3: stop and show the message to the user.

## Step 2.5: Critique the draft

### Step 2.5a — Skip-eligibility check (accuracy system)

Before spawning the critic, consult the accuracy-skip state. Areas that have demonstrated a perfect track record (clean_streak >= 5) MAY skip the critic; everything else MUST run it.

Run the bucket derivation:

```bash
py -3 .claude/scripts/derive_area.py "<contract-path-from-step-2>"
```

The output is one bucket per line. Three outcomes:

1. **Empty output** (no `Files to touch` section parsed) → run the critic. Log reason `no-files-to-touch-section`.
2. **Output contains `uncategorized`** → run the critic. Log reason `uncategorized-area`. (Add a pattern to `.claude/area-mapping.json` if this contract represents a recurring kind of work.)
3. **One or more named buckets** → for each bucket, run `py -3 .claude/scripts/accuracy_update.py query <bucket>` and inspect the `skip_eligible` field. **Skip is offered only when ALL buckets return `skip_eligible: true`.** Any cold or recently-failed bucket forces the critic to run.

If the env var `CLAUDE_CONTRACT_SKIP=off` is set, skip the entire skip-eligibility check and run the critic unconditionally. This is the user's escape hatch.

If skip is **not** eligible, print the reason (each bucket's `clean_streak: N/5` and `last_verdict`) one line each, then proceed to Step 2.5b unconditionally. The transparency matters — the user must see why they're paying the critic cost so they can decide whether to ramp accuracy by writing more contracts in that area.

If skip **is** eligible, present this `AskUserQuestion`:

> *"All buckets demonstrate a perfect streak (≥5 clean critic verdicts). Skip contract-critic for this draft? [buckets: bucket-a 7/5, bucket-b 5/5]"*  
> Options: **Skip** (default) · **Run anyway**

**If the user picks Run anyway:** proceed to Step 2.5b as if not eligible. The verdict-tracker hook will record the resulting verdict normally.

**If the user picks Skip (or defaults):**

1. Append a `## Critique` stub to the contract via `Edit`:
   ```markdown

   ---

   ## Critique

   **Critic:** skipped-by-accuracy-system
   **Date:** <today YYYY-MM-DD>
   **Verdict:** skipped
   **Buckets:** <bucket-a 7/5>, <bucket-b 5/5>, ...
   **Override:** set CLAUDE_CONTRACT_SKIP=off or run /critique-now <contract-path>

   ### Findings
   - (skipped — buckets demonstrated N>=5 clean streak)
   ```

2. **Do NOT call `accuracy_update.py record-clean`.** Skips are non-counting — counting them would let a single clean run perpetually re-skip itself (bootstrap-gaming the threshold). Streak progress requires evidence from the actual critic. The verdict-tracker hook recognizes `Verdict: skipped` and is a no-op.

3. Skip ahead to **Step 3** — the contract is ready for user review with no findings beyond the stub.

### Step 2.5b — Spawn contract-critic

(Reached when skip is ineligible OR the user picked "Run anyway".)

Launch the `contract-critic` agent via the Agent tool with this TASK block:

```
TASK: critique the draft contract
CONTEXT: invoked by /design-first Step 2.5 after data-architect wrote the draft
CWD: <current working directory>
PRIOR_AGENT: data-architect
PRIOR_FINDINGS:
  contract_path: <full path returned by data-architect in Step 2>
  contract_status: draft
```

The critic reads the contract plus the root registry files and their domain files (`MECHANISMS/general.md`, `VOCABULARY/general.md`, `JOURNAL/general.md` and the other `MECHANISMS/*.md`, `VOCABULARY/*.md`, `JOURNAL/*.md` that match the contract) and INTEGRATION.md, applies its adversarial checklist (reuse drift, vocabulary drift, hidden Open Questions, integration-surface omissions, journal-lesson applicability, End-User View completeness, etc.) and **appends a `## Critique` section to the contract file** with BLOCKER / WARN / NIT findings.

The critic is **advisory** — it does NOT flip `Status` and does NOT block the workflow. Its only output is the appended `## Critique` section plus a HANDOFF summary. Do NOT proceed to Step 3 until the critic returns.

If the critic reports `verdict: blockers-found`, surface that prominently when presenting the contract in Step 3. The user may either address the BLOCKERs (recommended) or explicitly acknowledge them and proceed anyway. Either choice is valid — the journal append in Step 3 captures the outcome.

### Why the failure-reset rule exists

The accuracy-skip system (Step 2.5a) trusts only **evidence** — a chain of clean critic verdicts in the same sentinel-path bucket. The 2026-05-17 AI-Workshop-Eval-Runs contract was drafted with `verdict: confident` and the critic still produced 5 WARN findings (vocabulary drift, conditional file lists, an unresolved Open Question masquerading as a decision, an INTEGRATION.md target section that did not exist, and a precedent violation). The data-architect's own confidence rating is **not** evidence the draft is clean.

That incident is why ANY post-approval failure signal — user rejection, `fullstack-code-reviewer` divergence, a `/critique-now` BLOCKER, or a JOURNAL.md entry with `Trigger: post-approval` / `post-impl divergence` — instantly resets the bucket's `clean_streak` to 0 and re-mandates the critic for the next contract in that area. The system rewards proven areas, not first contracts, and it discards trust the moment evidence contradicts it.

**Session-context-isolation principle:** the data-architect's reasoning primes its own self-review. Only a fresh agent instance, spawned via the `Agent` tool with a cold context, performs independent critique. Inline critique by the main orchestrator session does **not** satisfy this step.

## Step 3: Present the contract and resolve Open Questions

Read the contract file. Show the user:

1. The one-paragraph summary from the data-architect's HANDOFF
2. The Business Concept section
3. The Data Shapes section (tables)
4. The list of Reused Mechanisms
5. The list of New Mechanisms, if any (with justifications)
6. The `## Critique` section findings (BLOCKER / WARN / NIT) with severity counts up front
7. The `## Lessons referenced` section (which JOURNAL.md entries the architect heeded)
8. The Open Questions — each with a recommendation from the data-architect
9. When Step 1.5 recorded `applies` items: the `check-contract` result and any change notices, as `references/central-memory.md` describes (`not-cited` and `uncleared-item` shown, never hidden)

Use the `AskUserQuestion` tool to resolve each Open Question AND to walk the user through every BLOCKER and WARN from the `## Critique` section. Phrase critique questions as: *"The critic flagged this as `<BLOCKER|WARN>`: `<summary>`. Address it (how?), defer it (note your reasoning), or reject the finding (why)?"* Do NOT guess answers. Do NOT flip `Status` to `approved` until every Open Question has a documented answer AND every BLOCKER has an explicit user response.

For each critic finding the user **agrees with and addresses** (or agrees with and defers with justification), add a corresponding journal entry with `registry_append.py`, never by hand. Write the entry to `.claude/cache/registry-appends/<slug>.md` in this shape:

```markdown
### YYYY-MM-DD — <Finding summary distilled into one-line title>
- **Trigger:** pre-approval critic
- **Source contract:** <full contract path>
- **Lesson:** <one-line actionable — `Do X` / `Avoid Y when Z`>
- **Apply when:** <pattern future critic should match against — copy from the finding's "Prior artifact ignored" or derive from "What is wrong">
- **Tags:** <2-5 grep-friendly keywords>
```

Then run `py -3 "$RAP" --project "$CLAUDE_PROJECT_DIR" --registry journal --from-file .claude/cache/registry-appends/<slug>.md` through the lookup block under "Run the data-architect's registry appends" above (the script picks the domain file from the Source contract's area; add `--domain <slug>` to choose one). Show the printed `file:line`, and delete the entry file after success. On a project not yet on registry layout 2 it appends to a domain file and prints an advisory line; that is success. Exit 2: fix the entry file and re-run. Exit 3: stop and show the message to the user.

A registry append is a shipped change: batch it into a change that already raises the plugin version, or raise at least a patch version (see CLAUDE.md, "Every change to shipped plugin files bumps the plugin version").

Findings the user **rejects** are NOT logged — the user's rejection is recorded inline in the contract (under the relevant Open Question or as a one-line note appended to the relevant `## Critique` finding bullet) so future readers see the decision trail. The `/journal-add` skill is the manual escape hatch if the user later changes their mind.

### Contract-level rejection (accuracy-skip bad-plan signal)

If, during Step 3, the user expresses **contract-level** rejection — not a single-finding disagreement, but rejection of the design as a whole — treat it as a bad-plan signal. Rejection-phrase keywords to watch for (case-insensitive, whole-message scan):

- "reject this plan" / "reject the plan" / "reject this contract" / "reject the contract"
- "this contract is wrong" / "this plan is wrong" / "this design is wrong"
- "redesign this" / "redesign the contract" / "redo this"
- "start over" / "scrap this" / "discard this contract"

On match (or any clearly equivalent intent):

1. Confirm once via `AskUserQuestion`: *"Treat this as a full rejection of the contract? (Status will be flipped to `rejected`, accuracy-skip clean_streak resets for every bucket this contract touched.)"* — Yes / No / Address-specific-finding-instead.
2. On confirmed Yes: `Edit` the contract to flip `Status: draft` (or `approved`, if it had been flipped already in this session) → `Status: rejected`. The `contract-status-watcher.py` PostToolUse hook detects the transition and calls `accuracy_update.py record-failure` for every derived area with source `rejection`.
3. Stop the workflow. Do NOT proceed to Step 4. Suggest the user start a new `/design-first` cycle with the lessons they learned from this draft.

Do NOT auto-trigger on isolated words ("wrong", "bad", "no") — false positives are worse than misses here. The keyword scan only fires on the full phrases above.

Once all Open Questions are answered AND all critique findings have explicit user responses (addressed / deferred / rejected), edit the contract file to:
- Append the user's answers under each Open Question
- Append `→ Addressed by: <one line>` / `→ Deferred: <reason>` / `→ Rejected: <reason>` directly under each `[BLOCKER]` and `[WARN]` finding in the `## Critique` section
- Flip `Status: draft` → `Status: approved`, but only after the approval gate below passes

### The approval gate (Parent Branch Delivery Rule)

A contract whose handoff has two or more mergeable blocks is always delivered through a parent branch, so the `**Work Item Brief:**` header is mandatory for it: the brief it names is the parent brief, and its `branch:` is the parent branch. Count a review gate as a mergeable block, so an implementation block plus a review block is a multi-sub-task contract. Before the flip, ask the script what it reads. Resolve it with the standard lookup block (the same text every skill carries, pinned by `test_skill_script_lookup.py`, class `TestDesignFirstApprovalGateLookup`), then run the status for this contract:

```bash
PRM=
S=.claude/scripts/pr_merged.py
if [ -f "$S" ]; then PRM=$S
elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then PRM=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  PRM=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$PRM" --contract <slug> --status --json
```

**If `PRM` comes back empty, stop and say so.** Read `layout_defects` from the report, and when it is not empty, show each entry's `reason` and `remedy` to the user and do not flip Status to approved while any layout defect stands, because the dispatch would refuse the contract too. The reasons are `no-parent-branch`, `parent-is-default`, `ambiguous`, `no-parent-issue`, `sub-task-raises-version` and `single-branch-delivery`. When the key is absent the contract has at most one mergeable block and nothing is judged. A Jira or Azure DevOps item has no GitHub parent issue (`no-parent-issue`), so its contract must be a single block.

When the gate passes and the linked brief's `contract:` field is unset (`none`, `none - <text>`, `UNKNOWN`, empty or a placeholder), the approval step writes this contract's repository-relative path into that field of the existing linked brief. This creates nothing: it edits the one brief the header already names, so that every reader finds the same parent brief. Step 3.6 still runs after the approval, and was not moved.

## Step 3.4: Open one GitHub issue for the follow-ups

A follow-up stub under `.claude/concepts/followups/` is only visible through `/list-contracts`. The user's working view is GitHub issues, so a stub alone leaves deferred work invisible. This step makes the issue the tracked item and the stub its detail.

Run it once the contract is approved, and only when the contract cites at least one stub (an Adjacent Areas row decided `follow-up handle`, or a `.followup.md` path anywhere in the contract) whose `**Issue:**` field is still `pending`. `data-architect` has no shell, so it cannot open the issue itself; this step belongs to the main session.

1. Search for an existing issue first: `gh issue list --search "Follow-ups from <contract slug>" --state open`. If one exists, add the stubs to it as checklist items instead of opening a second.
2. Otherwise open **one** issue titled `[CHORE] Follow-ups from <contract title> (<contract slug>)`. Put any decision the user must make first, then one checklist item per stub, each with the files involved, and link every stub path as detail. Quote the exact title and body in the Step 3 summary, and open it unless the user declines.
3. Write the issue number into every stub's `**Issue:**` field (`#<n>`) and say it in the final report.
4. If `gh` is missing or unauthenticated, write `**Issue:** unavailable` in each stub and say so plainly. Never leave `pending` behind silently.

A contract that cites no stub skips this step.

## Step 3.5: Route the approved contract

With the contract approved, decide how the implementation runs.

**Route one — the agent chain (use this).** Continue to Step 4 and hand off to the implementer
agents. When the operator wants the rest of the chain carried automatically, through tests,
review, verification and a pull request, invoke `/flow`. It composes `/tdd-first`, the reviewer
agents, `/verify-before-done`, `/git-commit` and `/ship`, and pauses only where a person has to
decide.

**When the contract declares several sub-tasks,** the middle of that chain iterates one step
per merge. `/advance` starts what is ready and stops, a person merges, and `/pr-merged`
confirms the merge with GitHub and says what it released. Neither half loops.

**Route two — the Contract Orchestrator (removed).**
An earlier subsystem claimed this job and never did it. Its eight scripts were removed from
this plugin on 2026-09-14, after a review found the two load-bearing pieces were stubs: the
planner never parsed a contract, and no session was ever launched. Zero sub-tasks satisfied
the loop's completion test, so a run printed that the contract was complete having written no
code, and its own suite passed without ever calling the planner.

It also carried three hazards for anyone who did run it. It opened real tracker issues before
doing any work. Its merge step acted on whichever tree it was started from. Its dependency
gate failed open, releasing a sub-task whose parent had not merged.

Do not reintroduce it to solve a scheduling problem. `/flow` and `/advance` do the same job
through pull requests, which gives the review surface the removed design never had.

## Step 3.6: Make sure a Work Item Brief links the contract

When the user approves a contract, check that a Work Item Brief (the file under `.claude/work-items/` that records a change's branch, contract and pull request) is linked to it. The later `/pr-merged` step refuses to record a delivery, with guard G-1, unless the contract's own brief names the pull request by branch or link. A run started with `/design-first` directly, not through `/task`, has no such brief, so its merged pull request could never be recorded.

1. Find the linked brief the way `pr_merged.find_linked_brief` does: the contract's `**Work Item Brief:**` header first, then the one brief whose `contract:` field names this contract. If one exists, do nothing.
2. If none exists, write a minimal brief at `.claude/work-items/<contract-date>-<contract-slug>.md`, in the shape `/task` writes:
   - `id: none`, `issue_offer: pending`, `source: free-text`, `url: none`, `status: designing`, `created:` today (`issue_offer:` records what happened when the chain offered to open a tracker issue; step 4 below sets it. Its allowed values are the `offerOutcomes` list in `work-item-conventions.json` → `issueLink`, not restated here)
   - `branch:` the branch you are on now (the branch the work will be delivered from), never the default branch
   - `contract:` the contract's repository-relative path
   - `pr: none`, `issue_link: none`, `north_stars: none`
   - a short Problem statement and Acceptance criteria that point at the contract, which is authoritative
3. Add the line `**Work Item Brief:** .claude/work-items/<file>.md` to the contract header, under `**Requested by:**`.
4. Make the issue offer, the same offer `/task` Step 2.5 point 6 and `/ship` Step 3.5 make, in the same wording (one mechanism, three call sites). Gate on the **id**: it applies when the brief's id reads `absent` (the `absentIdTokens` list in `work-item-conventions.json` → `issueLink`). One `AskUserQuestion`, asked once, quoting the exact title and body that would be created. Write the body (the problem statement, then the acceptance criteria) to a file first and pass the file, never the text inline, because Git Bash can mangle free text that starts an argument:

   ```bash
   gh issue create --title "[<TYPE>] <bare title>" --body-file <path to the body file>
   ```

   Record the answer in `issue_offer:`. Never write `declined` unless the user answered this question in this run; an assumed answer, or a question you skipped, writes `pending` and never `declined`.
   - On accept: write `id:`, `url:` and `repo:` into the brief and set `issue_offer: opened`. If the create command fails, write `issue_offer: unavailable` and add `issue_offer_reason: create-failed`.
   - On decline: write `issue_offer: declined`. A recorded decline is final.
   - If `gh` is missing or signed out: write `issue_offer: unavailable` and add `issue_offer_reason: gh-missing` (or `gh-unauthenticated`).
   - If there is no problem statement to put in the body: write `issue_offer: unavailable` and add `issue_offer_reason: no-problem-statement`. Invent nothing.
5. Tell the user in one line that the brief was created, and why.

Do not ask a question for the facts this step records: they are already known (the branch and the contract path). The issue offer in point 4 is the one question this step asks. If you are on the default branch, stop and enter a worktree first, because the brief's branch must be the one that will merge.

## Step 4: Hand off to implementer agents

Read the `Implementation Handoff` section of the approved contract. The direct hand-off below is for a contract with a single mergeable block only. When the handoff has two or more mergeable blocks (more than one implementation block, or an implementation block plus a review block), do not launch one-session implementers: route to `/flow` (Step 2.7 opens the parent issue and the sub-issues), then `/advance`, because the Parent Branch Delivery Rule delivers such a contract through a parent branch. For a single block, launch the named agent (`dotnet-backend-architect`, `angular-senior-dev`, `ingestion-data-architect`) with the pre-written TASK block from the contract.

The implementer agents are configured to refuse if `PRIOR_FINDINGS.contract_path` is missing or the contract's `Status` is not `approved`. Always pass these fields.

When multiple implementer handoffs are present (e.g. backend + frontend), launch them in parallel where their file sets do not overlap. Launch sequentially if they do.

## Step 5: Post-implementation review

After all implementers return `Status: complete`, launch `fullstack-code-reviewer` **via the `Agent` tool**. This is non-negotiable — the main orchestrator session does NOT review its own implementers' output inline. Inline review prose ("I read the diff and it looks fine") does not satisfy this step. The reviewer must be a fresh agent instance with a cold context.

```
TASK: Review the implementation of <contract slug>
CONTEXT: concept contract at <path>, status approved
FILES: <union of all files changed across implementers>
PRIOR_AGENT: <implementer agents>
PRIOR_FINDINGS:
  contract_path: <path>
  contract_status: approved
  extra_checklist:
    - Did the implementation diverge from the concept contract's Data Shapes? If so, is the divergence justified?
    - Did this introduce a new reusable mechanism that belongs in .claude/registries/MECHANISMS.md or a MECHANISMS/<domain>.md file? If yes, append it with registry_append.py.
    - Did this introduce new domain vocabulary that belongs in .claude/registries/VOCABULARY.md or a VOCABULARY/<domain>.md file? If yes, append it with registry_append.py.
    - Did the implementation reveal a CONTRACT DEFECT (justified divergence = the contract was wrong)? If yes, the reviewer's janitor duty appends a journal entry with registry_append.py (JOURNAL.md root or a JOURNAL/<domain>.md file) with Trigger: post-impl divergence.
```

### Multi-pass review: always spawn fresh, never `SendMessage`

If the reviewer flags issues, the implementer fixes them, and you need a second review pass — **spawn a NEW `fullstack-code-reviewer` instance via the `Agent` tool**. Do NOT `SendMessage` to the prior reviewer instance. The prior instance carries forward its own earlier findings and the implementer's reasoning from the first round, both of which prime the second pass with biased context.

A clean re-review requires a clean context. The cost of one extra agent spawn is far lower than the cost of a missed regression.

### Mapping to the safety-critical review gate

This Step 5 invocation produces the HANDOFF that `/verify-before-done` Step 5.5 looks for when the diff includes safety-critical paths. If the diff additionally touches a root named by the `safety-critical.roots`, `auth.roots` or `migration.root` slots of `.claude/project-profile.md`, also spawn the matching domain reviewer (the project's live-action safety reviewer, `security-auditor`, `migration-safety-reviewer`) — each is an independent agent invocation, not a replacement for `fullstack-code-reviewer`.

## Step 6: Flip contract status to implemented

After review passes and the merge is recorded, the flip is automatic: `pr_merged.py` changes `Status: approved` → `Status: implemented`, fills the Review Checklist from the review reports' Gate Outputs, and appends a line to the brief's run log, once nothing is pending. `/pr-merged` reports it and offers the small records pull request. A manual flip stays allowed only on request, for a contract delivered before 2026-10-05, and never for one the script reports `pending`.

## Escape hatches

- **User asks for trivial change and gets wrongly classified as non-trivial:** user can override by re-stating as trivial. You must respect the override.
- **User wants to bypass the hook entirely:** document that they can set `CLAUDE_CONCEPT_GATE=off` in their environment for the session. Use sparingly.
- **Contract promotion:** if a contract's implementation introduces something genuinely reusable, the review step (Step 5) appends it with `registry_append.py` (`MECHANISMS.md` root or a `MECHANISMS/<domain>.md` file). When `data-architect` is re-invoked after approval to promote a mechanism or a term, its HANDOFF lists `Registry appends:` and you run them as "Run the data-architect's registry appends" says. This is how the registry grows.

## What this skill does NOT do

- Does not write production code itself — delegates to data-architect (design) and implementer agents (code).
- Does not skip the communication gate — Open Questions MUST be answered by the user, never guessed.
- Does not run without reading `MECHANISMS.md` first (the data-architect enforces this).
