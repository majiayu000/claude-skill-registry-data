---
name: ocs-coach-setup
description: >
  Build and QA an OCS Coach bot that a supervisor triggers from Labs to coach a flagged worker.
  Never messages a real worker.
disable-model-invocation: false
---

# OCS Coach Setup

Design and rationale: `docs/superpowers/specs/2026-10-06-ocs-coach-design.md`
(including the review of the real KMC Audit bot this generalises).

**ACE never triggers coaching** — except to its own Connect test user, to record itself
answering (`skills/coach-session-capture`, owner carve-out 2026-10-07). This skill builds and tests the Coach. A person
starts each conversation from the Labs run page — the workflow's
`start_ocs_outreach` action, from its button or by asking the page's canopy agent
("start coaching sessions for the red facilitators"), which previews; the person
then sends with the Send button on Labs' coaching card in canopy's chat (MCP Apps,
connect-labs#2348). The agent never holds a send token for a worker. QA conversations to Dimagi staff use the action's `deliver_to` argument.

## When it runs

Phase 7 Step 1.9 (`agents/synthetic-data-and-workflows.md`), after the semantic
registry and programme report exist — the Coach's topic keys ARE the registry's
indicator ids — and after Phase 5's Q&A bot, which it clones for the model and the
opp collection. Re-run it whenever the registry version changes.

**Required, not best effort.** The Coach is a Phase 7 product: Phase 7 cannot be
`done` without `products.ocs_coach.experiment_id` and `products.ocs_coach.coaching_on`
(`lib/phase-products-schema.ts` `REQUIRED_PRODUCT_KEYS`, checked at the phase
boundary). A failure in any step below is a defect to fix and re-run, not a
residual to record — we know the Coach builds (Spark Coach 13972).

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `source_experiment_id` | clone source (model, collection) | explicit arg; default: run_state `phases.ocs-setup.products.ocs_chatbot.experiment_id`; no Q&A bot → `$OCS_GOLDEN_TEMPLATE_ID` (Step 1) |
| `registry_id` | indicator cards (`semantic_registry_get` → `indicators_doc.measures`) | explicit arg; default: run_state `phases.synthetic-data-and-workflows.products.synthetic.cascade.registry.registry_id`; else program context doc |
| `app_summary` | the short "how the app works" section | explicit arg (Drive id / local file, or 5-8 bullets); default: `3-commcare/pdd-to-deliver-app_summary.md` |
| `worker`, `workers`, `language` | `--worker`, `--workers`, `--language` | explicit arg; default: PDD § worker noun, languages |
| `collection_id` | opp collection the Coach searches (`--collections`) | explicit arg, or `none`; default: the Q&A bot's opp collection |
| `report_workflow_ids[]` | reports that get the coaching action (Step 9) | explicit arg; default: run_state `products.synthetic.cascade.programme_report` + `cascade.opp_reports[]` |
| `run_id` | run-bound mode: run-scoped bot names + Step 8 write-back | optional; absent = live-program mode |

**Live-program mode** (no `run_id`; e.g. a coach for a live programme with its
own registry and reports): the bot names in Steps 1 and 5 use the programme
name plus a date in place of `<run-id>` (OCS still refuses a reused Connect bot
name on a team, ace#3006); Step 8 records the `ocs_coach` block in the program
context doc instead of `run_state.yaml`. Every other step, including the QA in
Step 7 and the selection rule in Step 9, is unchanged. Never take a registry,
report or bot id from another run's state.

## Existing objects

- **Step 9 changes a live report for everyone who opens it.**
  `workflow_update_definition` adds the coaching button and the canopy panel
  to the page every supervisor sees. `config` shallow-merges, so the report's
  other keys survive, but confirm with `workflow_run_context` and get owner
  approval on a live programme's reports before writing.
- **Rebuilding the Coach is a new `public_id`.** Every report that names the
  old bot keeps starting sessions with it until it is patched again (Step 9's
  last line). Record which reports were patched.
- **A clone keeps its source's collections.** Cloning a live programme's bot
  without `--collections` hands the Coach that programme's documents
  (ace#2779). `--collections` is required for this reason.

## Steps

1. **Clone.** `ocs_clone_chatbot({template_id: <Q&A experiment_id>, new_name: "ACE Coach - <opp> (<run-id>)"})`.
   Run-scoped name, as for the Q&A bot (ace#1017).
   **No Phase 5 bot** (a standalone `/ace:demo`): clone the OCS golden template,
   `$OCS_GOLDEN_TEMPLATE_ID` (the same source `ocs-agent-setup` clones). It carries
   a shared FAQ collection that belongs to no programme, so build with
   `--collections none` and render with `--knowledge-base no` unless the demo has a
   collection of its own (ace#2779: a chlorine coach kept KMC/ECD FAQs this way).
2. **Indicator measures.** Write `indicators_doc.measures` to a local JSON file.
   Only measures with `meta.flw_applicable: true` and a `direction` other than
   `none` become topics (`lib/coach-briefing.ts` `coachableIndicators`).
3. **App summary.** 5–8 bullets from the Deliver summary: the forms, what each
   records, how payment and the cap work, which automatic flags exist, the app's
   languages. Facts only — no inferred backstory.
4. **Render** the prompt:

   ```bash
   ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
   node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/render-coach-prompt.ts" --measures <json> --app-summary <md> \
     --program "<programme>" --worker <noun> --workers <plural> --knowledge-base yes|no --out <prompt.md>
   ```

   `--knowledge-base` must match what step 5 attaches: `no` when the coach is built with
   `--collections none`, so the prompt does not tell the coach to search material it does
   not have (`ocs-coach-build.ts` refuses that combination). It refuses an unfilled placeholder. Read the cards it prints: a data-quality
   signal must read as a REVIEW FLAG; an outcome with no target must say so.

   **Case states** need nothing here: Labs' case briefing carries each case state's
   guidance from the registry at send time
   (`docs/superpowers/specs/2026-10-09-case-coaching-design.md`), and the prompt tells
   the coach to follow it.

5. **Build:**

   ```bash
   node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/ocs-coach-build.ts" --team <team> --experiment <id> \
     --prompt <prompt.md> --collections <opp collection id> --connect-bot-name "<Programme> Coach (<run-id>)"
   ```

   The bot name is run-scoped because OCS refuses a Connect bot name already used on
   the same team, so a bare `<Programme> Coach` collides on the second run of every
   opp (ace#3006, observed on `smallholder-seasonal/20261015-1402`).

   Splices `templates/ocs-coach/status_node.py` between the LLM and End nodes,
   sets prompt + collection, and creates the `commcare_connect` channel.
   `--collections` is required (the script refuses a run without it): a clone keeps
   its source's collections unless told otherwise, and `--collections none`
   detaches them all (a coach cloned from another programme's coach must not search
   that programme's documents). If the
   channel step fails with *flag_commcare_connect*, the OCS team lacks that feature
   flag: that team cannot deliver coaching to a worker's Connect app, so stop and
   report it (name the team) — the flag must be switched on, then re-run this step.
6. **Publish** with `ocs_publish_chatbot_version`.
7. **QA with a simulated worker** — prefer `skills/coach-session-capture` web mode, which
   starts the session exactly as Labs does (opening verbatim, briefing in
   `session_state.coach_briefing`). Author the worker's lines for THIS opp from its
   PDD and app summary and pass them as `--turns` (that skill's § Worker turns); the
   built-in default is programme-neutral, never another programme's script (ace#2804).
   The chat-completions route below puts the briefing in
   the conversation instead, which is not the production path. Fallback: over the OCS chat-completions API
   (`POST /api/openai/<public_id>/chat/completions`, team API key), never the
   Connect channel. First user message = a briefing from `renderBriefing`; then play
   the worker. Cover at least: (a) agrees → a specific plan; (b) disputes with a
   credible reason the data would miss → recorded `agreement=disputed`, no
   commitment pushed; (c) a safety disclosure → `[[COACH_ESCALATE:...]]`. After each,
   read the session's `participant_data` (`GET /api/sessions/<id>/`) and check
   `chatbot_topics`, `chatbot_review_needed`, `chatbot_task_status`. Run every
   assistant message through `findOverstatements` — any hit fails the QA.
8. **Write back** `phases.synthetic-data-and-workflows.products.ocs_coach`
   (`merge: 'deep'`, `validateAs: {kind: 'phase-products', phase: 'synthetic-data-and-workflows'}`).
   Phase 7 builds the Coach, so it lives in Phase 7's block; runs before
   2026-10-07 (Spark `20261004-1706`) recorded it under `phases.ocs-setup.products`:
   `experiment_id, public_id, team_slug, pipeline_id, admin_url, name,
   published_version_number, collection_id, registry_id, topic_keys[],
   connect_channel, qa`.
9. **Put coaching on the standard reports.** Coaching lives on the reports Phase 7
   already builds — the programme report (`products.synthetic.cascade.programme_report`)
   and every partner's opportunity report (`cascade.opp_reports[]`) — not on a copy.
   On each, `workflow_update_definition` with:

   ```json
   {"config": {
     "agent": {"share": true},
     "actions": [{"key": "initiate_ai_coach", "type": "start_ocs_outreach",
                  "label": "Start coaching",
                  "defaults": {"bot": "<ocs_coach.public_id>"}}]
   }}
   ```

   `config` shallow-merges, so this keeps the report's other keys. The report's own
   render shows the declared action as a button on worker rows, and `share` puts the
   canopy panel on the page, so "start coaching for every red facilitator" works there.
   Because Step 1.9 runs before the DDD render, the panel and the button are part of
   the page the demo films — coaching is a feature of the report, not an add-on.
   Confirm with `workflow_run_context` (the action is listed with this bot), then
   confirm there is someone to coach — the selection rule below — and record
   `ocs_coach.coaching_on: [{workflow_id, run_id, url, selection}]`, `selection`
   being the mode the check returned.

   **Who the Coach starts with — one rule** (`lib/coach-peer-watch.ts`
   `selectCoachingWorkers`; operator decision 2026-10-16, ace#3053). Save
   `workflow_run_indicators({run_id, scope: "worker", limit: 500})` to a file (it
   must not be `truncated`: peers are the whole run) and the registry's measures,
   then:

   ```bash
   node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/coach-select.ts" --indicators <json> \
     --measures <json> --program "<programme>" --workers <plural> [--named "<a>,<b>"] --out <items.json>
   ```

   | mode | when | who | how a person starts it |
   |---|---|---|---|
   | `band` | any worker is red or yellow (the PDD set targets) | those workers | Labs briefs them; the report's button |
   | `peer_watch` | nothing red or yellow (a target-less PDD) and a worker is well outside the other workers on a coachable indicator (Tukey fence, ≥ 10 points from the peer median, ≥ 8 peers) | those workers, on only those topics | the page's canopy agent, `workflow_run_action` with `--out`'s items |
   | `named` | nobody stands out | the workers the supervisor names | same as `peer_watch` |
   | `none` | nobody stands out and nobody is named | — | exit 2: a stop, never a pass |

   A `peer_watch` / `named` item carries its own `prompt`: a Labs-shaped briefing
   (`renderSelectionBriefing`) whose "Why this worker" line says the comparison is
   with peers and that the programme set no target, and whose topics read
   `band peer-watch` (or `unbanded` for a named worker). Labs keeps a briefing it is
   handed as-is (`actions.py` `_brief_workers`), so the worker is not skipped for
   having nothing red or yellow. The report's own button still appears only on red
   or yellow workers — on a target-less report the canopy panel is the way in, so
   the demo films that, not the button. A peer figure is never called a goal or a
   target, in the briefing, on the card (`renderIndicatorCards`) or by the coach
   (`templates/ocs-coach/coach-prompt.md`). On `none`, ask the operator for the
   supervisor's names and re-run with `--named`; Labs has no relative band to fall
   back on (ace#3053's upstream note).

   Rebuilding the Coach (a new `public_id`) means patching these reports again.

## The briefing

Labs composes it (connect-labs #2280, `connect_labs/workflow/run_grading.py`): for
each worker without a `prompt` of their own, the action builds the `renderBriefing`
shape from that worker's graded cells — red topics first, then yellow, coachable
(`flw_applicable`) indicators only — records the topic ids as the task's
`coaching_indicators`, and shows the composed briefing in the preview. Workers with
nothing red or yellow are skipped with a reason. So **do not put a briefing in
`defaults.prompt`**: anything there is appended to every worker's briefing under
"Programme team's note:". Leave it unset, or use it for a genuine standing note.

The report shows "Start coaching" only on workers who are off target or on watch;
Dimagi staff coaching one worker get a "Send to me instead (QA)" box (`deliver_to`).
When the design sets no targets nobody is red or yellow, and the worker items
`scripts/coach-select.ts` writes (step 9) carry ACE's own peer-watch briefing
instead — through the canopy panel, never through `defaults.prompt`.

## The briefing picture (optional)

A Coach can open with a picture of the worker's OWN figures. It is optional on
both sides: nothing changes for a session that does not ask for one.

- **Labs** (`start_ocs_outreach` with `include_image: true`, or a workflow default)
  adds two keys to the session data: `coach_image_url`, a signed link (7 days) to a
  chart Labs renders from the same topics as the briefing, and
  `coach_image_caption`, one sentence naming what it shows.
- **The status node** (`templates/ocs-coach/status_node.py`) fetches that link once,
  on the Coach's first reply, and attaches the PNG with OCS's
  `add_file_attachment`. A failure never blocks the reply: it lands in session
  state `coach_image_error` and the reply goes out as text. The code decides, not
  the model, so the picture cannot repeat (the model DOES re-send media it chose
  itself — ace#2822).
- **The prompt** reads `{session_state.coach_image_caption}`: empty means no
  picture, and the Coach must not mention one.
- **The fetch authenticates** with an OCS Auth Provider named exactly
  `connect-labs` (type Bearer) on the Coach's OCS team, holding a Labs token of
  scope `coach-images` (minted at `/labs/mcp/tokens/`). That token can fetch
  coaching pictures and nothing else. Without the provider every fetch fails into
  `coach_image_error`, so add it once per OCS team that runs Coaches.
- Connect delivers the picture only on apps with rich messaging (CommCare 2.66+,
  commcare-android#3946); older apps show an "update your app" notice instead.

## Terminology

Worker-facing text follows `skills/_terminology.md` — the platform is "Connect".

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-10-18 | Inputs are parameters (`source_experiment_id`, `registry_id`, `app_summary`, `collection_id`, `report_workflow_ids[]`) with the run's Phase 5/7 state as defaults; live-program mode names and records outside the run; `## Existing objects` for live-report patching and rebuilds. ace#3148. | ACE (build-vs-maintain audit) |
