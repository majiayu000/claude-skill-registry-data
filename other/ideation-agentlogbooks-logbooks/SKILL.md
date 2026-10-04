---
name: ideation
description: "Use when the user needs ideas or a name — brainstorming, naming, developing an idea further, hybridizing ideas, stress-testing candidates, reframing a problem, or picking a final direction. Ideas persist in a per-topic logbook across sessions."
---

# Ideation — Orchestrator

You are a lightweight orchestrator for the `ideation` skill. You do NOT generate ideas yourself. You spawn a planner subagent to produce a plan, show it to the user for approval, then execute operator subagents one step at a time against a per-topic SQLite idea logbook.

## Three concepts

- **Idea logbook** — per-topic SQLite database at `./.logbooks/ideation/<topic-slug>/logbook.sqlite`. Multi-entity: `topic_meta`, `frames`, `facts`, `ideas`, `lineage`, `assessments`, `operator_runs`. Authoritative across sessions. Schema and rules in `ideation.logbook.md`.
- **Operator** — a single atomic subagent procedure that reads a cohort of idea IDs, applies one transformation, writes results via the CLI. Every operator is a markdown file in `operators/`.
- **Plan** — an ordered list of operator calls (sometimes wrapped in `PARALLEL:` blocks, with `CHECKPOINT:` lines between them). Produced by the planner subagent from the user's intent + topic state.

Ideas are first-class. Operators are second-class. The plan is ephemeral.

## Invocation

The user runs the skill with one of these shapes:

```
ideation <topic-slug>: <intent>                      # primary form — lean capture by default
ideation <topic-slug>: import these ideas: <list>    # capture YOUR ideas from a source
ideation <topic-slug> --import <file>: <intent>      # capture ideas from a file
ideation <topic-slug> --techniques: <intent>         # opt in to the structured treatment (frame + personas + compare)
ideation <topic-slug> --playbook <name>: <intent>    # force a specific playbook
ideation <topic-slug> --no-checkpoints: <intent>     # autonomous run, strip checkpoints
ideation --list-topics                               # list existing topics
ideation <topic-slug> --show-state                   # dump topic state (no plan, no ops)
```

**Capture-first default.** On a fresh topic the skill is lean: if the intent supplies ideas, it stores them; otherwise it makes one plain brainstorm call. It does NOT run the frame→personas→compare machinery unless the user asks for it (`--techniques`, "thorough", "deep", "score", etc.). The structured toolkit is opt-in, surfaced as follow-ups. See the planner decision procedure (Step 3) below.

Topic slug is lowercase alphanumeric with dashes or underscores. It resolves to `./.logbooks/ideation/<slug>/` under the current git repo root (or cwd if not in a repo).

## Session lifecycle

Run these steps in order. The CLI you use throughout is `python plugins/ideation/skills/ideation/scripts/ideation_db.py` (abbreviated below as `ideation_db.py`).

### Step 1 — Resolve the topic

- If the user passed `--list-topics`: run `ideation_db.py list-topics` and render results. Stop.
- If the user passed `--show-state`: run `ideation_db.py show-state <slug>` and render. Stop.
- Otherwise: check whether `./.logbooks/ideation/<slug>/logbook.sqlite` exists.
  - **Exists** — note the topic exists and proceed.
  - **Missing** — call `AskUserQuestion` to confirm creation:
    ```
    Topic '<slug>' doesn't exist yet. Create it?
    Options: Yes, create / Cancel
    ```
    On Yes: run `ideation_db.py init-topic <slug> --description "<first sentence of intent>" --owner "<git user.name or 'personal'>"`.
    On Cancel: stop.

### Step 2 — Generate a run_id and start the live wall

The live wall is **mandatory**, not optional. It gives the user real-time visibility into a session that otherwise sits silent for minutes during subagent runs. Always start it before plan execution begins, verify it's bound to **this** topic, and open the browser tab automatically.

`serve.py` is per-topic: a server bound to port 7878 will only stream events for the slug it was started with. If a stale server from a previous session is still running for a different topic, emits to the current topic's JSONL file will have no reader and the wall will appear empty. Do NOT trust `serve.py`'s silent exit — verify the bound process is serving the current slug, and kill+restart if not.

```bash
RUN_ID=$(python plugins/ideation/skills/ideation/scripts/ideation_db.py new-run-id)

# Step 2a — If port 7878 is already bound, verify it's serving THIS topic.
# If it's serving a different topic, kill it so we can start a fresh server.
existing_pid=$(lsof -ti :7878 2>/dev/null)
if [ -n "$existing_pid" ]; then
  existing_args=$(ps -p "$existing_pid" -o args= 2>/dev/null)
  if [[ "$existing_args" == *serve.py* && "$existing_args" != *" <slug>"* ]]; then
    kill "$existing_pid"
    # macOS holds the socket in TIME_WAIT briefly after kill; wait it out.
    sleep 5
  fi
fi

# Step 2b — Start the live-wall server in the background. If port 7878 is still
# bound at this point, it's already serving the current slug, and serve.py will
# exit silently — that is fine.
nohup python plugins/ideation/skills/ideation/live/serve.py <slug> > /tmp/ideation-wall-$RUN_ID.log 2>&1 &
disown
sleep 1

# Step 2c — Verify the bound server is for THIS topic before announcing the URL.
bound_args=$(ps -p $(lsof -ti :7878) -o args= 2>/dev/null)
if [[ "$bound_args" != *" <slug>"* && "$bound_args" != *" <slug>" ]]; then
  echo "WARNING: port 7878 is bound but not serving <slug>. Wall may be empty." >&2
fi

# Step 2d — Auto-open the browser tab. macOS: `open`. Linux: `xdg-open`.
# Don't fail the session if the open command isn't available — the URL is still printed below.
(open http://127.0.0.1:7878 2>/dev/null || xdg-open http://127.0.0.1:7878 2>/dev/null) &

# Step 2e — Emit session_started so the wall has a title + phase scaffold immediately,
# even before any operator runs.
python plugins/ideation/skills/ideation/live/emit.py session_started \
  '{"topic":"<slug>","phases":["Frame","Generate","Transform","Evaluate","Decide"]}' \
  <slug>
```

**Tell the user the URL** — output this exact message in your next assistant turn (before showing the plan):

> Live wall: http://127.0.0.1:7878 — opening in your browser. (If a tab didn't pop, open it manually.)

Keep `RUN_ID` for the whole session. Every `op-start` you call will pass it.

**Emit early and often.** During plan execution you will emit at every visible transition — plan accepted, op started, ideas written, checkpoint reached, op finished, session complete. The wall is designed to absorb partial state and overwrite cards as data arrives — prefer to emit speculatively rather than wait for polished output. The full event schema is at the bottom of this file under "Live wall — event schema."

### Step 3 — Spawn the planner subagent

Use the `Agent` tool to spawn the planner. Pass it the planner prompt (below), the user's intent, the topic state, the operator catalog, and the playbook catalog.

Collect topic state first:

```bash
ideation_db.py show-state <slug>
ls plugins/ideation/skills/ideation/operators/
ls plugins/ideation/skills/ideation/playbooks/
```

**If `--import <file>` was passed:** read the file's contents now and append them to the intent text you hand the planner (clearly marked as the user's supplied ideas). This makes the planner's Step 3a ingest branch fire with the file's ideas as `source=` — the planner cannot read files itself, so the orchestrator must inline them here.

**Planner prompt** (embed verbatim in the subagent's prompt):

```
You are the planner for the `ideation` skill. Your job is to produce a plan — an ordered list of operator calls — that will accomplish the user's intent against the current topic state.

## Your inputs

- User intent (free text)
- Topic state: active frame, idea counts by kind/status, recent operator runs, assessment metrics present
- Operator catalog: one-line description per operator (you read the operator files for this)
- Playbook catalog: ten playbooks with when-to-pick notes (plus the lean-capture default, which is not a playbook)

## Your decision procedure

1. If the user passed `--playbook <name>` OR the intent clearly names a playbook, load that playbook verbatim. Resolve any cohort references from the intent (e.g. IDs mentioned).

2. Else if the intent references specific idea IDs ("develop 17", "combine 17 and 24", "stress-test the top 3"):
   - Match intent shape to a playbook (followup_develop, hybridize_pair, stress_test_shortlist).
   - Use that playbook's shape, inject cohort IDs from the intent.

3. Else if the topic is fresh (zero ideas in the logbook). **Capture-first: default to the leanest path; the structured machinery is opt-in.** In order:

   **3a. INGEST** — the intent SUPPLIES external ideas (a pasted list, "import these", "here are my ideas", "store/log these ideas", or `--import <file>`):
   - Plan = one step: `generate.import source=<the supplied ideas verbatim>`.
   - No framing checkpoint, no compare. The user gave the ideas — store them, do not generate. (The orchestrator inserts a light frame first; see Light-frame precondition.)

   **3b. OPT-IN heavier shapes** — only when the intent explicitly asks for them:
   - "techniques" / "structured" / "personas" / "frame it properly" / `--techniques` → `starter` (frame + 2 personas + compare; the *old* default).
   - "deep" / "thorough" / "full treatment" / "explore every angle" / "dig in" / "comprehensive" → `deep_explore`.
   - "score" / "rank" / "prioritize formally" → `quick_seed`.
   - naming intent ("name X", "what should we call X", "rebrand X", "find a name for X") → `naming` (a distinct craft; general playbooks underperform).
   - reframing a prior problem → `reframe_and_regenerate` (only if the topic already has a frame; else fall back to `starter`).

   **3c. DEFAULT (none of the above matched): lean capture.** Plan = one step: `generate.brainstorm count=12`. ONE plain generation call — no framing checkpoint, no persona fan-out, no compare report. The orchestrator inserts a light frame first (Light-frame precondition). End by offering the technique menu (Step 6). This is the default when the intent has no clear signal — get ideas on the wall fast; techniques come on demand.

**Light-frame precondition.** `generate.brainstorm` and `generate.import` need an active frame (the not-null `frame_id_at_birth` FK), but the capture default must not run a framing exercise or pause the user. So when the plan's first step is `generate.brainstorm` or `generate.import` on a frameless topic, the ORCHESTRATOR inserts a thin placeholder frame itself before that step (see Step 5B → "Light-frame precondition"): problem statement = the user's intent, root-causes/HMW left as deferred placeholders. No subagent, no `frame.discover`, no checkpoint. Real framing is deferred (Frame-on-first-iterate).

**Frame-on-first-iterate.** When a LATER invocation runs a technique or deep shape (`route`, `deep_explore`, scoring, `develop`, `--techniques`) on a topic that has only a light placeholder frame, prepend a real `frame.discover` (+ `CHECKPOINT: framing`) so the deep work is properly grounded. Detect a light frame by its placeholder root-causes (e.g. "(deferred …)").

4. Else (the topic has ideas but the intent doesn't match a playbook shape):

   **4a.** If the intent mentions "route" / "iterate" / "keep developing" / "what should I try next" / "plan next moves" AND the topic has ≥5 active ideas: use the `route` playbook. This is the iterative follow-up shape — the router decides what to do with each idea based on current state, rather than applying a single operator to the whole batch.

   **4b.** Otherwise:
   - Emit a custom 3–8 step plan using the operator library as vocabulary.
   - Example: intent "find weak ideas" → `evaluate.score cohort=all_active` + `decide.shortlist cohort=bottom-20%` + `decide.compare`.
   - Example: intent "what ideas haven't been stressed yet" → `decide.compare cohort=<ideas without web_stress_verdict>`.

## Checkpoint insertion

The lean capture default (`generate.brainstorm`) and ingest (`generate.import`) carry NO checkpoints — capture is unpaused by design (no `frame.discover`, so no framing checkpoint applies). For all other plans, insert these checkpoints (unless the user passed --no-checkpoints, unless they are already present, OR unless the user's intent explicitly names a playbook — playbooks carry their own checkpoints):

- After `frame.discover`: `CHECKPOINT: framing`
- After `evaluate.criteria`: `CHECKPOINT: criteria_lock`
- Before any `validate.*` affecting more than 5 ideas: `CHECKPOINT: before_validation`
- Before `decide.converge` or `decide.export`: `CHECKPOINT: before_decide`
- If the plan will generate more than 30 new ideas before any evaluation: `CHECKPOINT: taste` after the generation phase

## Your output

Write the plan so a human can skim it and understand what will happen. Lead each step with a plain-language sentence; put the machine-readable tag in parentheses at the end so the orchestrator can execute it. Keep sentences short and specific.

Output this exact format:

```
## Plan

1. <one-sentence human description> (<operator.name> [key=value ...] [cohort=...])
2. <one-sentence human description> (<operator.name> ...)
3. ⏸ Checkpoint — <what the user will confirm in their own words>
4. <short overview of the fan-out>. In parallel:
   - <natural sub-step description> (<operator.name> ...)
   - <natural sub-step description> (<operator.name> ...)
...

## Rationale

<2-3 sentences: which playbook you chose (or why you emitted a custom plan) and what outcome the user should expect>
```

### Example — the DEFAULT shape (lean capture)

Most first-time invocations on a fresh topic with no clear signal should produce a one-step plan:

```
## Plan

1. Brainstorm a dozen varied ideas in one pass (generate.brainstorm count=12)

## Rationale

Lean capture — the default for fresh topics. One plain brainstorm call, no framing pause and no persona machinery (a blind A/B showed it matches or beats the old frame+personas default on substance, relevance, and diversity). Ideas hit the wall in seconds. Techniques are one follow-up away: `ideation <slug>: score and rank these`, `stress-test the top 3`, `develop idea N`, or `ideation <slug> --techniques` for the full structured treatment.
```

One step, no checkpoint, ~12 ideas, straight to the wall. The orchestrator inserts a light placeholder frame before the step (Light-frame precondition). Keep the default this tight.

### Example — INGEST shape (the user brought ideas)

```
## Plan

1. Store your ideas in the logbook (generate.import source=<the user's list>)

## Rationale

The user supplied their own ideas, so we capture rather than generate. One step, no checkpoint; the ideas land on the wall immediately and existing follow-ups (`develop idea N`, `score and rank`, `find tensions`) iterate from there.
```

### Example — opt-in structured shape (starter, via --techniques)

When the user asks for the structured treatment ("techniques", "frame it properly", `--techniques`), emit the old default's shape:

```
## Plan

1. Identify root causes and framing questions (frame.discover)
2. ⏸ Checkpoint — confirm the framing before generating ideas
3. Generate ~20 diverse ideas in parallel:
   - Practical, contradiction-driven ideas — 10 (generate.seed persona=innovator count=10)
   - Wild, random-stimulus ideas — 10 (generate.seed persona=wild_card count=10)
4. Present them side-by-side in a short report (decide.compare cohort=all_active)

## Rationale

Running the `starter` playbook because the user opted into the structured treatment. Light frame, two personas, a compare report.
```

### Example — opt-in heavy shape (deep_explore)

When the user says "thorough" / "deep" / "full treatment", emit a longer plan:

```
## Plan

1. Scout the web for citable grounding facts about the problem (frame.context_scout)
2. Identify root causes, framing questions, and the core trade-off (frame.discover)
3. ⏸ Checkpoint — confirm the framing before generating ideas
4. Generate raw seed ideas from four personas in parallel:
   - Practical, contradiction-driven ideas — 15 (generate.seed persona=innovator count=15)
   - Reverse-brainstormed ideas — 12 (generate.seed persona=provocateur count=12)
   - Wild, random-stimulus ideas — 15 (generate.seed persona=wild_card count=15)
   - Cross-domain analogies — 12 (generate.seed persona=connector count=12)
5. Push every seed wilder, ground it in a real mechanism, and pressure-test it:
   - Push wilder (transform.john zone=FIRE stance=dreamer_start cohort=all_seeds)
   - Ground with cross-domain mechanism (transform.john zone=PLASMA stance=realist_start cohort=all_seeds)
   - Pressure-test for feasibility (transform.john zone=ICE stance=critic_start cohort=all_seeds)
6. Find tensions between ideas (evaluate.tension cohort=all_active)
7. Synthesize across the hottest tensions, 2 cycles (transform.ratchet zone=FIRE cycles=2 cohort=tension_cluster)
8. ⏸ Checkpoint — taste check
9. Combine a diverse slate of 5 ideas into hybrids (transform.hybridize cohort=diversity-top(5))
10. Derive evaluation criteria (evaluate.criteria)
11. ⏸ Checkpoint — lock the criteria
12. Score every active idea against the criteria (evaluate.score cohort=all_active)
13. ⏸ Checkpoint — confirm before adversarial validation
14. Stress-test the top 8 with web research (validate.web_stress cohort=top-by-composite(8))
15. Surface brilliance signals on the top 5 (evaluate.brilliance cohort=top-by-composite(5))
16. ⏸ Checkpoint — confirm before final decision
17. Converge on 1-3 selected ideas (decide.converge cohort=top-by-composite(3))
18. Export an Idea Menu (quick wins / core bets / moonshots) (decide.export format=menu)

## Rationale

Running the full `deep_explore` playbook because the user asked for a thorough treatment. Expect ~50-80 active ideas at peak, narrowed to 3 selected at the end.
```

## Format rules

- Every step starts with a plain-language sentence the user can read without knowing operator names.
- The parenthesized tag at the end contains the exact operator name plus params and cohort, space-separated. The orchestrator parses this.
- CHECKPOINT lines start with `⏸ Checkpoint — ` followed by a human sentence explaining what the user will confirm.
- PARALLEL blocks lead with a one-line overview of the fan-out, then nest sub-steps with `-` bullets. Each bullet carries its own human description + machine tag.
- cohort can be:
  - literal IDs: `cohort=[17,24]`
  - named query: `cohort=top-by-composite(5)`, `cohort=top-by-metric(metric=taste, n=3)`, `cohort=children_of(17)`, `cohort=tension_cluster`, `cohort=all_seeds`, `cohort=all_active`, `cohort=diversity-top(5)`
  - step reference: `cohort=children_of(step 1)` — orchestrator resolves at execution time
- params use simple `name=value`. No quotes needed for single-word values.
- Keep human descriptions short (one line each). Avoid methodology jargon in the prose — say "push wilder" not "apply Disney dreamer-mode", say "stress-test" not "run adversarial web search". The parenthesized tag has the precision; the prose is for the human reading.

## Things you must NOT do

- Do not invent operator names. Use only what's in the catalog.
- Do not pass abstract cohorts the orchestrator cannot resolve ("the good ones", "the bold ideas") — translate to concrete queries (`top-by-composite(5)`, `cohort=[ideas WHERE tag='BOLD']` is NOT valid; use a named query like `tension_cluster` or a concrete list).
- Do not fabricate criteria or scores. If the plan needs scoring, include `evaluate.criteria` + `evaluate.score` explicitly.
- Do not emit any operator that reads or writes a frame other than via the frame.* operators.
```

After the planner returns, parse the `## Plan` and `## Rationale` sections.

### Step 4 — Approve the plan with the user

The planner emits plans in the human-readable format above. Show the plan + rationale verbatim via `AskUserQuestion`:

```
Plan for "<intent>":

<paste the ## Plan section verbatim — the prose leads, the parenthesized tags stay but read as brief technical anchors>

Rationale: <rationale text>

Options: Accept / Edit (Other) / Cancel
```

On Accept: proceed.
On Edit (any Other response): send the user's edit back to the planner with the original plan as context; it emits a revised plan. Re-present. Repeat until accepted or cancelled.
On Cancel: stop.

**On Accept, emit `plan_set` immediately** so the wall renders the approved roadmap. Build a JSON array of plan steps from the planner's `## Plan` section — one entry per top-level step (PARALLEL blocks count as one step, not one per sub-bullet). Use `type` of `op`, `parallel`, or `checkpoint`:

```bash
python plugins/ideation/skills/ideation/live/emit.py plan_set '{
  "steps":[
    {"n":1,"type":"op","description":"Identify root causes and framing questions"},
    {"n":2,"type":"checkpoint","description":"Confirm the framing"},
    {"n":3,"type":"parallel","description":"Generate ~20 diverse ideas in parallel"},
    {"n":4,"type":"op","description":"Present them side-by-side in a short report"}
  ]
}' <slug>
```

### Step 5 — Execute the plan

For each step in order:

#### Step 5A — Checkpoint lines (`⏸ Checkpoint — ...`)

Do NOT spawn a subagent. Identify which built-in checkpoint this is by the human description the planner emitted (e.g. "confirm the framing" → framing). Call `AskUserQuestion` with the matching payload:

- **framing** — show the active frame (root causes, framing questions, and the trade-off if present). Read via `ideation_db.py active-frame <slug>` and render in plain prose, not as JSON. Options: "Looks right, proceed" / "Let me edit (Other)".
- **taste** — delegate to `evaluate.taste_check` as a real operator invocation; the orchestrator replaces this checkpoint line with a regular operator execution over a diverse slate of recent seeds + transforms.
- **criteria_lock** — read the latest `./.logbooks/ideation/<slug>/criteria-<run_id>.json` file and render the criteria + weights as a plain list. Options: "Accept criteria" / "Adjust (Other)". On Adjust, rewrite the criteria file with user edits before proceeding.
- **before_validation** — show how many ideas are about to be validated + a short sample of their titles. Options: "Proceed" / "Narrow the list (Other)" / "Skip validation".
- **before_decide** — show the current top N ideas (titles + evidence posture). Options: "Proceed to decide" / "Run one more pass (Other)" / "Skip".
- **custom** — the step carries its own `question` and `options` params; present them.

Record the outcome in `operator_runs` — when any operator runs after a checkpoint, pass `--user-approved` (true if the user proceeded; false if they explicitly skipped). If the user bails at a checkpoint, stop the plan cleanly and write a summary of what ran up to that point.

**Live wall emits.** Bracket every checkpoint with two events so the wall renders a pause card and removes it on resolution:

```bash
# BEFORE calling AskUserQuestion:
python plugins/ideation/skills/ideation/live/emit.py checkpoint_reached \
  '{"name":"<framing|criteria_lock|before_validation|before_decide|taste|custom>","step_n":<plan_step>}' <slug>

# AFTER the user answers (proceed / edit / skip / cancel):
python plugins/ideation/skills/ideation/live/emit.py checkpoint_resolved \
  '{"name":"<same>","action":"<proceed|edit|skip|cancel>"}' <slug>
```

If the user bails (cancel/skip), still emit `checkpoint_resolved` so the wall card disappears — then emit `session_complete` and stop.

#### Step 5B — Regular operator steps

**Light-frame precondition (capture default & ingest).** Before executing a `generate.brainstorm` or `generate.import` step, check whether the topic has an active frame (`ideation_db.py active-frame <slug>`). If it does NOT, insert a thin placeholder frame yourself first — no subagent, no checkpoint:

```bash
FRAME_OP=$(ideation_db.py op-start <slug> --run-id $RUN_ID --operator frame.light --cohort-ids-json '[]')
ideation_db.py add-frame <slug> \
  --problem-statement "<the user's intent, verbatim>" \
  --root-causes-json '["(deferred — run --techniques or a deep playbook to frame properly)"]' \
  --hmw-questions-json '["(deferred)"]' \
  --operator-run-id $FRAME_OP
ideation_db.py op-finalize <slug> $FRAME_OP --status succeeded --outcome-summary "light placeholder frame (capture default)"
```

This resolves the not-null `frame_id_at_birth` FK for the capture operators while keeping framing genuinely lazy. `frame.light` is an orchestrator-internal label (no operator file, no subagent) — it is documented here, not fabricated. Do NOT run this for `--techniques`/deep plans; those carry a real `frame.discover`.

For each non-checkpoint step:

1. **Resolve the cohort to literal IDs.**
   - Literal IDs → already concrete.
   - Named query → run `ideation_db.py query <slug> <query-name> [--n N] [--metric ...] [--id ...]`.
   - Step reference (e.g., `children_of(step 1)`) → query the logbook based on what the referenced step produced (typically `ideation_db.py children-of <slug> <parent_id>` per parent).

2. **Create the operator_runs row.**

   ```bash
   OP_RUN_ID=$(ideation_db.py op-start <slug> \
     --run-id $RUN_ID \
     --plan-step <N> \
     --operator <fully.qualified.name> \
     [--persona <persona>] \
     --cohort-ids-json '<JSON array>' \
     [--params-json '<JSON object>'])
   ```

3. **Emit `phase_started` (if the phase changed) and `op_started`** — do this **before** spawning the subagent so the wall shows a placeholder card during the long subagent run:

   ```bash
   # If this op moves into a new phase (Frame/Generate/Transform/Evaluate/Decide), emit:
   python plugins/ideation/skills/ideation/live/emit.py phase_started \
     '{"name":"<Generate|Transform|Evaluate|Decide|Frame>"}' <slug>

   # Always emit op_started (placeholder card appears immediately):
   python plugins/ideation/skills/ideation/live/emit.py op_started \
     '{"op_run_id":'$OP_RUN_ID',"operator":"<operator.name>","persona":"<persona-or-empty>","cohort_size":<N>,"step_n":<plan_step>,"description":"<plan-step-prose>"}' \
     <slug>
   ```

4. **Spawn the operator subagent** via the `Agent` tool. Pass it:
   - The operator file content (read `operators/<operator>.md`).
   - The topic slug.
   - The literal cohort_ids.
   - The resolved params.
   - `$RUN_ID`.
   - `$OP_RUN_ID`.
   - Any persona/zone reference files the operator needs (read them and include inline).

   The operator subagent executes its prompt body, runs CLI commands, writes rows tagged with `$OP_RUN_ID`, and returns a 1-3 sentence outcome summary.

5. **Emit per-row events for what the subagent just wrote** — this populates the wall before `op-finalize` runs. See "Per-operator emit table" near the bottom of this file for which event to emit for which operator. The most common case (any `generate.*` or `transform.*`) is the inline Python loop below — run it as soon as the subagent returns:

   ```bash
   python -c "
   import sqlite3, json, subprocess, sys
   slug, op_run_id = sys.argv[1], int(sys.argv[2])
   conn = sqlite3.connect(f'.logbooks/ideation/{slug}/logbook.sqlite')
   rows = conn.execute(
       'SELECT idea_id, title, description, kind, tag FROM ideas WHERE origin_operator_run_id=? ORDER BY idea_id',
       (op_run_id,)
   ).fetchall()
   conn.close()
   for r in rows:
       p = json.dumps({'id':r[0],'title':r[1],'description':r[2],'kind':r[3],'tag':r[4],'status':'active'})
       subprocess.run(['python','plugins/ideation/skills/ideation/live/emit.py','idea_generated',p,slug])
   " <slug> $OP_RUN_ID
   ```

   For `evaluate.score`, `decide.shortlist`, `decide.compare`, etc. — emit `idea_scored`, `idea_kept`, `idea_ranked` etc. per the per-operator emit table below.

6. **Finalize the row.**

   On success:
   ```bash
   ideation_db.py op-finalize <slug> $OP_RUN_ID \
     --status succeeded --outcome-summary "<from subagent>"

   python plugins/ideation/skills/ideation/live/emit.py op_finished \
     '{"op_run_id":'$OP_RUN_ID',"status":"succeeded","ideas_count":<N>}' <slug>
   ```

   On failure:
   ```bash
   ideation_db.py op-finalize <slug> $OP_RUN_ID \
     --status failed --error "<failure reason>"

   python plugins/ideation/skills/ideation/live/emit.py op_finished \
     '{"op_run_id":'$OP_RUN_ID',"status":"failed","error":"<reason>"}' <slug>
   ```

7. **Retry policy.** If the operator fails, retry once. If it fails again, mark it `failed`, print a warning to the user, and continue to the next step unless the failure cascades (e.g., subsequent steps depended on output from the failed one — in that case, ask the user whether to continue or stop).

#### Step 5C — PARALLEL blocks

PARALLEL blocks are the mechanism for fan-out (multiple `generate.seed` personas, multiple `transform.john` zones, etc.).

Execute by spawning all sub-steps in **one message** using multiple `Agent` tool calls. For each sub-step:
- Create its own `operator_runs` row before spawning (ahead of time, so each subagent knows its `operator_run_id`).
- **Emit `op_started` for each sub-step** before spawning the parallel subagents — one placeholder card per sub-op appears immediately.
- Spawn all subagents in parallel.
- Collect all their outcome summaries as they return.
- For each returning subagent: run the per-row emit loop (`idea_generated` / `idea_scored` / etc. per the per-operator table) **as soon as that one returns** — do not wait for the whole block. Cards stream in as each parallel sub-op completes.
- Finalize each `operator_runs` row and emit `op_finished` per sub-op as the subagents return.

Do not proceed past the PARALLEL block until all its sub-steps have terminated.

#### Step 5D — `decide.route` fragment expansion

When the step you just executed is a `decide.route` call, the normal Step 5B flow changes: **defer the `op-finalize` on the `decide.route` row until after the fragment has been read and validated**, so the outcome summary records both the subagent's decisions and any validation drops in a single finalize.

If `decide.route` itself fails (subagent returns an error, raises an exception, or fails twice under Step 5B's retry policy), do NOT enter this expansion flow — apply Step 5B's normal failure handling and stop. Step 5D only runs on a confirmed successful `decide.route` return.

1. After the `decide.route` subagent returns its outcome summary, do NOT call `op-finalize` yet. Keep the summary in a local variable as `subagent_summary`.
2. Read `./.logbooks/ideation/<slug>/reports/<RUN_ID>-route.md` — the subagent wrote this during its operator work.
3. Extract the `## Plan fragment` section. Its grammar is narrow:
   - Exactly one `PARALLEL:` header line.
   - Zero or more `- <operator.name> [key=value ...] cohort=[id, id, ...]` bullets.
   - Parse each bullet: operator name, params (space-separated `key=value`), cohort (literal integer IDs).
   - **Coerce each param value** before building the params JSON: if it matches `^-?\d+$` → integer; if it is exactly `true` or `false` → boolean; otherwise → string. Apply this before the JSON merge in step 8 so downstream operators receive typed params (e.g., `count=3` → `3`, `cheap=true` → `true`, `hint=x` → `"x"`).
   - **On grammar violation** (missing `PARALLEL:` header, malformed `cohort=[...]` bracket, a bullet that does not match `- <operator.name> [key=value ...] cohort=[id, id, ...]`, or any other parse error): finalize the deferred `decide.route` row immediately with `ideation_db.py op-finalize <slug> <decide.route op_run_id> --status failed --error "malformed plan fragment: <one-line reason>"`, print the offending line to the user, and stop this step — skip validation (step 4) and expansion (step 8). Do not auto-retry `decide.route`; the subagent already returned "successfully", so re-prompting is a user-level decision. In `--loop` mode, treat this iteration as terminated and proceed to Step 5E's exit checks.
4. **Validate every recommended operator call** against the operator catalog (reload via `ideation_db.py list-operators --format json` if you don't already have it cached for this session):
   - Operator name exists in the catalog.
   - `cohort size >= applies_to.min_cohort`.
   - If `applies_to.kinds` is non-empty, every idea in the cohort has `kind` ∈ those kinds (read via `ideation_db.py idea <slug> <id>`).
   - If the parent `decide.route` was invoked with `params.cheap=true`, drop any bullet whose operator has `cost.web: true`.
   - For each idea in the bullet's cohort, query `ideation_db.py lineage-ops <slug> <id> --limit <cooldown + 1>` to retrieve the idea's lineage-ops history. If the bullet's operator name appears within the last `repeat_guard.same_lineage_cooldown` entries for ANY cohort idea, drop the bullet. Defense in depth — the subagent should already have respected this, but the orchestrator enforces it definitively.
   - Collect dropped bullets + reasons in a local `drops` list; print a warning per drop.
5. Compute the combined finalize summary:
   - If `drops` is empty: `final_summary = subagent_summary`.
   - Otherwise: `final_summary = subagent_summary + "; dropped during validation: " + "; ".join(drops)`.
6. Call `op-finalize <slug> <decide.route op_run_id> --status succeeded --outcome-summary "<final_summary>"` — this is the first and only finalize of the `decide.route` row.
7. If the validated fragment is empty or every bullet was dropped, proceed to the next plan step. Print "Fragment empty — nothing to expand" to the user.
8. Otherwise, treat the validated bullets as a PARALLEL block and execute them using the normal Step 5C parallel-dispatch. Each bullet gets its own `operator_runs` row:
   - Call `op-start` with `--run-id $RUN_ID` but **omit `--plan-step`** (so `plan_step_index` stores `NULL` — these are fragment-expanded, not in the planner's original plan).
   - Construct a single JSON object containing BOTH the parent-linkage keys AND every `key=value` pair parsed from the bullet. For example, if the bullet was `transform.scamper count=3 cohort=[8]`, the params JSON is `{"parent_operator_run_id": <decide.route op_run_id>, "parent_plan_step_index": <decide.route plan_step>, "count": 3}`. Pass this as `--params-json`.
   - Emit `op_started` per bullet before spawning (use the parent step's plan-step number for `step_n`, or omit it).
   - Spawn each subagent per the normal Step 5B procedure.
   - Run the per-row emit loop and emit `op_finished` per sub-op as subagents return — same pattern as Step 5C.
   - Finalize each row as subagents return.

Fragment expansion shares the outer plan's `RUN_ID` — querying `operator_runs` filtered by `RUN_ID` reconstructs the full session.

#### Step 5E — `--loop` re-entry (`route` playbook only)

When the user invoked the `route` playbook with `--loop`, after the full plan body has executed (step 1's `decide.route` + Step 5D's fragment expansion), check whether to re-enter:

**Iteration-1 stamping.** If the playbook was invoked with `--loop`, stamp the first pass too: when calling `op-start` for the initial `decide.route` (step 1 of the plan body) AND for every Step 5D expanded row, include `"loop_iteration": 1` in the `--params-json` object (alongside any parent-linkage keys for expanded rows). This way iteration 1 carries the same label as later iterations, and per-iteration queries over `operator_runs` are uniform.

1. If this iteration's `decide.route` produced an empty fragment → exit the loop. Terminal state, proceed to Step 6.
2. If `iterations_so_far >= --iterations N` (default `N = 3`, max `3`) → exit the loop.
3. If `--no-checkpoints` is not set, call `AskUserQuestion`:
   ```
   Iteration <done>/<N> complete. <executed_count> operator runs completed this round across <idea_count> distinct ideas. Continue or stop?
   Options: Continue / Stop
   ```
   Where `<executed_count>` is the number of operator_runs rows in this iteration (query: `params.loop_iteration = <done>` AND `status = 'succeeded'`, excluding the `decide.route` row itself), and `<idea_count>` is the count of distinct idea IDs appearing in any of those rows' `cohort_ids`.

   On Stop → exit the loop.
4. Otherwise, increment the iteration counter and re-execute **only the `decide.route` step**, not the full playbook body. Even if the original invocation used `--with-criteria` (which runs `evaluate.criteria` → criteria_lock checkpoint → `evaluate.score` before `decide.route` on iteration 1), iteration 2+ skips those setup steps — criteria derivation and scoring are one-shot setup per `--loop` session, not per iteration:
   - Run `decide.route cohort=all_active_capped(50)` again. When calling `op-start`, omit `--plan-step` (so `plan_step_index` stores `NULL` — iteration-2+ routes are not in the planner's original plan) and pass `--params-json` as the **original invocation's playbook params augmented with `loop_iteration: <N>`**. Specifically: carry forward `cheap` (and any other playbook param the user passed at invocation time) into every iteration's `decide.route` row and add `"loop_iteration": <N>`. Do NOT replace the params with `{"loop_iteration": <N>}` alone — that would silently disengage Step 5D's `cheap` validation gate on iteration 2+.
   - Expand the fresh plan fragment via Step 5D. Each expanded row's `params-json` includes `"loop_iteration": <N>` alongside the `parent_operator_run_id` and `parent_plan_step_index` keys.

Critical invariants:

- `RUN_ID` stays constant across all iterations.
- Each `decide.route` call and each expanded operator run creates its own `operator_runs` row, all carrying the same `run_id`.
- If any operator fails unrecoverably inside a loop iteration, the loop exits cleanly — do not retry the whole routing decision.

### Step 6 — Post-run summary

After the last step, render a human-readable summary. Lead with what changed; keep counts tight; skip internal terminology.

```
Done. Here's what this session produced:

- Generated <X> new ideas (<seeds> raw seeds, <variants> variants, <hybrids> hybrids)
- Recorded <Y> new pieces of evidence from the web
- Made <Z> judgments across <K> different metrics
- <count> ideas shortlisted, <count> selected, <count> rejected
- Reports:
    · ./.logbooks/ideation/<slug>/reports/<run_id>-<report>.md
    · ...

Try next:
- Develop a specific idea further: `ideation <slug>: develop idea N`
- Combine two ideas: `ideation <slug>: hybridize N and M`
- Stress-test the strongest: `ideation <slug>: stress-test the top 3`
- Frame it properly & go deeper (structured treatment): `ideation <slug> --techniques`
- Just peek at state: `ideation <slug> --show-state`
```

After a lean capture or ingest session especially, lead the "Try next" list with these — the techniques are opt-in, so this menu is how the user discovers them.

**Followups from operators that ran this session.** After the default bullets, iterate over `operator_runs` for this `run_id`. For each distinct operator that ran and has a non-empty `followups` list in its frontmatter, emit one additional bullet per followup. Render each as a natural-language suggestion scoped to the ideas that operator just produced or touched. Example:

    - Refine idea 8 further: `ideation <slug>: refine idea 8`        (from transform.invert.followups[0])
    - Stress-test idea 8 for evidence: `ideation <slug>: stress-test idea 8`  (from transform.invert.followups[1])
    - Refine ideas 8, 12 further: `ideation <slug>: refine ideas 8 and 12`  (deduped: transform.invert ran on 8, transform.cross_domain ran on 12, both have transform.refine as a followup)

Read the catalog once at the start of Step 6 via `ideation_db.py list-operators --format json`, then index by operator name. Deduplicate suggestions — if two runs both suggest `transform.refine`, emit one bullet referencing both idea sets.

Query the counts via:

```bash
ideation_db.py op-runs <slug> --run-id $RUN_ID
ideation_db.py ideas <slug> --status active
ls ./.logbooks/ideation/<slug>/reports/
```

Omit zero-count lines. If no ideas were generated (e.g., a decide-only session), say so explicitly — "No new ideas this session; the work was evaluation and decision."

**Emit `session_complete`** as the last action of the session — this freezes the wall's pulse and marks all phases done:

```bash
python plugins/ideation/skills/ideation/live/emit.py session_complete '{}' <slug>
```

Emit it even if the session ended early (cancel at checkpoint, fatal failure) — the wall should never sit pulsing on a stopped session.

## Operator catalog

Read the files in `operators/` for the full library. Summary:

- `frame.*` — context/problem-space operators (4): `context_scout`, `discover`, `historian`, `reframe`. (`frame.light` is an orchestrator-internal placeholder-frame insert for the capture default — not a subagent operator; see Step 5B.)
- `generate.*` — idea producers (4): `brainstorm(count=...)` (lean default — one plain pass), `import(source=...)` (capture the user's own ideas), `seed(persona=...)`, `fresh(hint=...)`
- `transform.*` — idea-to-idea operators (7): `scamper(op=...)`, `invert`, `cross_domain(domain=...)`, `hybridize`, `john(zone=..., stance=...)`, `ratchet(zone=..., cycles=...)`, `refine(hint=...)`
- `evaluate.*` — per-metric judgments (6): `hats`, `tension`, `taste_check`, `criteria`, `score(criteria_path=...)`, `brilliance`
- `validate.*` — web-sourced evidence (2): `web_stress`, `proof_search`
- `decide.*` — report/decision artifacts (5): `shortlist(n=...)`, `compare`, `converge`, `export(format=...)`, `route`

## Playbook catalog

See `playbooks/<name>.md` for full shapes. Summary:

- **lean capture** — **the default** (not a playbook; the planner's Step 3c branch). One `generate.brainstorm` call, no checkpoint, straight to the wall. Ingest (`generate.import`) is its sibling for user-supplied ideas.
- **`starter`** — opt-in (the *old* default), triggered by `--techniques` / "structured" / "frame it properly". Frame + 20 ideas + compare. 1 checkpoint. ~5 min.
- `quick_seed` — `starter` plus criteria + scoring. 2 checkpoints. ~10 min.
- `naming` — specialized for naming (products, features, companies). 70 candidates across 5 naming angles + web validation. ~10 min.
- `deep_explore` — full treatment for fresh problems (four personas, Johns, ratchet, web-stress, brilliance, converge). Opt-in only.
- `followup_develop` — develop specific ideas further
- `hybridize_pair` — combine specific ideas
- `stress_test_shortlist` — validate a shortlist with web evidence
- `reframe_and_regenerate` — mid-session pivot (new frame, regenerate)
- `converge_existing` — no new ideas, just decide on the current pool
- `route` — state-driven follow-up; router subagent decides per-idea operator assignments. Accepts `--loop`, `--cheap`, `--with-criteria`, `--iterations N`.

## Cohort query mapping

The planner emits cohort references; the orchestrator resolves them via the CLI:

| Cohort spec | CLI call |
|---|---|
| `top-by-composite(5)` | `ideation_db.py query <slug> top-by-composite --n 5` |
| `top-by-metric(metric=taste, n=3)` | `ideation_db.py query <slug> top-by-metric --metric taste --n 3` |
| `children_of(17)` | `ideation_db.py query <slug> children-of --id 17` |
| `tension_cluster` | `ideation_db.py query <slug> tension-cluster` |
| `all_seeds` | `ideation_db.py query <slug> all-seeds` |
| `all_active` | `ideation_db.py query <slug> all-active` |
| `all_active_capped(50)` | `ideation_db.py query <slug> all-active-capped --n 50` |
| `diversity-top(5)` | `ideation_db.py query <slug> diversity-top --n 5` |
| literal IDs `[17, 24]` | no CLI call needed; pass through |
| `children_of(step N)` | for each idea produced by step N (from its operator_runs row's subsequent inserts), call `children-of` |

## Live wall — event schema

The live wall is mandatory (see Step 2). This section is the canonical event reference for every emit call you make during plan execution.

Infrastructure lives in `live/` next to this file:
- `live/serve.py` — HTTP+SSE server on port 7878. Serves the dashboard shell (`view.html` + its JS modules) at `/`, an SSE stream at `/events` (replays from offset 0 on every connect), and a `/state` JSON snapshot. `/state` projects the **authoritative SQLite logbook** (`logbook.sqlite`) — frames, ideas with lineage parents + temperature zones, assessments, operator runs — and overlays the event stream for the bits the DB can't express (the plan, which op is mid-flight, open checkpoints, completion). The logbook is read strictly read-only.
- `live/emit.py` — appends one JSON line to `.logbooks/ideation/<slug>/live-events.jsonl`. Independent of the server: emits always succeed even if no server is running (events accumulate in the file).
- `live/view.html` + `views.jsx` / `live-data.jsx` / `app.jsx` — the React "Ideation Dashboard" served at `/`: a lineage **Tree** (hero), **Timeline**, and **Board** view over the live session. `live-data.jsx` polls `/state` and re-fetches on every SSE event, so the wall reflects the logbook with no lost state. The events you emit below drive the live overlay (running op, plan, checkpoints); the idea/assessment/lineage content is read from the logbook your operators write.

The emit command is uniform:

```bash
python plugins/ideation/skills/ideation/live/emit.py <type> '<json-payload>' <slug>
```

### Event payloads

```jsonc
// session_started — Step 2, once per session, immediately after server start
{"topic": "<slug>", "phases": ["Frame","Generate","Transform","Evaluate","Decide"]}

// plan_set — Step 4, immediately after the user accepts the plan
{"steps": [
  {"n": 1, "type": "op",         "description": "Identify root causes and framing questions"},
  {"n": 2, "type": "checkpoint", "description": "Confirm the framing"},
  {"n": 3, "type": "parallel",   "description": "Generate ~20 diverse ideas in parallel"},
  {"n": 4, "type": "op",         "description": "Present them side-by-side in a short report"}
]}

// phase_started — Step 5B/5C, when an op enters a new phase (Frame/Generate/Transform/Evaluate/Decide)
{"name": "Generate"}

// op_started — Step 5B/5C/5D, BEFORE spawning the operator subagent. A placeholder card appears.
{"op_run_id": 42, "operator": "generate.seed", "persona": "innovator",
 "cohort_size": 0, "step_n": 3, "description": "Practical, contradiction-driven ideas — 10"}

// idea_generated — after a generate.* / transform.* subagent returns. Loop over new idea rows.
{"id": 17, "title": "...", "description": "...", "kind": "seed", "tag": "BOLD", "status": "active"}

// idea_scored — after evaluate.score returns. composite score as int or short string.
{"id": 17, "score": 82, "rationale": "...one sentence"}

// idea_kept — after evaluate.taste_check / decide.shortlist / decide.converge marks an idea kept/shortlisted
{"id": 17}

// idea_cut — after evaluate.taste_check / decide.converge marks an idea cut. stress_note optional.
{"id": 17, "stress_note": "...one sentence on why"}

// idea_ranked — after decide.compare / decide.shortlist picks top N
{"id": 17, "rank": 1}

// op_finished — Step 5B/5C/5D, AFTER op-finalize. Removes the placeholder card.
{"op_run_id": 42, "status": "succeeded", "ideas_count": 10}
{"op_run_id": 42, "status": "failed",    "error": "..."}

// checkpoint_reached — Step 5A, BEFORE AskUserQuestion. Pause card appears.
{"name": "framing", "step_n": 2}

// checkpoint_resolved — Step 5A, AFTER user answers. Pause card disappears.
{"name": "framing", "action": "proceed"}

// session_complete — Step 6, last action of the session
{}
```

### Per-operator emit table

After each operator subagent returns, run the emit loop for its stage. Always run the emit loop **before** `op-finalize` so cards appear without waiting on the bookkeeping write.

| Operator | Emit per row in payload |
|---|---|
| `frame.*` | none (frames are not cards) |
| `generate.*` | `idea_generated` per new idea (origin_operator_run_id = $OP_RUN_ID) |
| `transform.*` | `idea_generated` per new idea |
| `evaluate.score` | `idea_scored` per idea whose `score_summary` was patched |
| `evaluate.taste_check` | `idea_kept` for each `status='kept'` patch; `idea_cut` for each `status='cut'` patch (with `stress_note` if available) |
| `evaluate.brilliance` / `evaluate.tension` / `evaluate.hats` | none (assessments only — no card change) |
| `validate.web_stress` / `validate.proof_search` | none (assessments + facts — no card change) |
| `decide.shortlist` | `idea_kept` for each idea status patched to `shortlisted`; `idea_ranked` if a rank was assigned |
| `decide.compare` | `idea_ranked` per idea in the report's top N |
| `decide.converge` | `idea_kept` for each `status='selected'` patch; `idea_cut` for each `status='rejected'` |
| `decide.export` | none |
| `decide.route` | none (router decisions don't change card state) |

### Stage → phase name mapping (for `phase_started`)

| Operator prefix | Phase name to emit |
|---|---|
| `frame.*` | `"Frame"` |
| `generate.*` | `"Generate"` |
| `transform.*` | `"Transform"` |
| `evaluate.*` | `"Evaluate"` |
| `validate.*` | `"Evaluate"` |
| `decide.*` | `"Decide"` |

### Inline Python loop for `idea_generated` (most common case)

```bash
python -c "
import sqlite3, json, subprocess, sys
slug, op_run_id = sys.argv[1], int(sys.argv[2])
conn = sqlite3.connect(f'.logbooks/ideation/{slug}/logbook.sqlite')
rows = conn.execute(
    'SELECT idea_id, title, description, kind, tag FROM ideas WHERE origin_operator_run_id=? ORDER BY idea_id',
    (op_run_id,)
).fetchall()
conn.close()
for r in rows:
    p = json.dumps({'id':r[0],'title':r[1],'description':r[2],'kind':r[3],'tag':r[4],'status':'active'})
    subprocess.run(['python','plugins/ideation/skills/ideation/live/emit.py','idea_generated',p,slug])
" <slug> $OP_RUN_ID
```

The same pattern works for `idea_scored` (query `score_summary`), `idea_kept`/`idea_cut` (query `status` after the patch), etc. — adjust the SELECT and the event type accordingly. Use it after every `transform.*` op-finalize too, not only `generate.*`.

### Resilience

- The server may be already running (port 7878 bound). `serve.py` is per-topic — verify (per Step 2a) that the bound server is serving the current slug; if not, kill it and start a fresh one. Do NOT silently trust `serve.py`'s "exit silently if bound" message — emits to the current topic's JSONL will have no reader if the bound server is on a different slug, and the wall will appear empty.
- If a browser tab is opened mid-session, it sees the full history (the server replays from offset 0).
- After a kill+restart, macOS holds the socket in TIME_WAIT for a few seconds — the `sleep 5` in Step 2a handles this. If the restart still fails, increase the sleep before treating it as an error.
- Emits never block plan execution. If `emit.py` errors (rare — disk full?), continue the plan and surface the error in the post-run summary.

## References

- `ideation.logbook.md` — authoritative schema, identity rules, correction rules, queries, governance
- `references/operations.md` — the creative ops toolkit (SCAMPER, TRIZ, Six Hats, Synectics, Reverse Brainstorming)
- `references/output-rules.md` — mandatory style rules (coffee-talk descriptions, ID discipline, no methodology names in user-facing text)
- `references/personas/<name>.md` — specialist voices loaded by parameterized operators
- `references/zones/<name>.md` — temperature-zone constraints loaded by `transform.john` and `transform.ratchet`
- `live/serve.py` — HTTP+SSE server (`/`, `/events`, `/state`); `live/emit.py` — event emitter; `live/view.html` + `views.jsx`/`live-data.jsx`/`app.jsx` — the React Ideation Dashboard (Tree / Timeline / Board)

## Tool usage reminders

- Use the `Agent` tool to spawn planner and operator subagents.
- Use `AskUserQuestion` for every checkpoint and for plan approval.
- Spawn PARALLEL sub-steps in a single message (multiple Agent tool calls), not sequentially.
- Never skip `op-start` / `op-finalize` — the `operator_runs` table is the audit log; missing rows break follow-up sessions.
- Operators never call `op-start` or `op-finalize` — that is exclusively the orchestrator's job.
