---
name: ocs-agent-setup
description: >
  Create a program's OCS support chatbot from the ACE template with a RAG collection built from the
  PDD and app docs, or re-prompt an existing bot; publishes and returns embed credentials.
disable-model-invocation: false
---

# OCS Agent Setup

Run end-to-end against the OCS MCP server (`mcp/ocs-server.ts`). Uses these
atoms: `ocs_list_chatbots`, `ocs_clone_chatbot`, `ocs_create_collection`,
`ocs_upload_collection_files`, `ocs_wait_for_collection_indexing`,
`ocs_set_chatbot_system_prompt`, `ocs_attach_knowledge`, `ocs_set_chatbot_tools`,
`ocs_publish_chatbot_version`, `ocs_get_chatbot_embed_info`,
`ocs_ensure_public_link`, `ocs_set_chatbot_description`.

Runs in Phase 5 as Step 1 under the `ocs-setup` agent. The agent handles
quality gating via the `ocs-chatbot-qa` → `ocs-chatbot-eval` pair (quick
+ deep) in subsequent steps, so this skill is now purely configuration —
no inline self-eval.

## Inputs

This skill has two halves. **Create** (clone, collection, upload, index,
patch, publish, embed) is a general platform action. **Derive** (choose the
RAG files and compose the prompt from a PDD) is the pipeline's way of filling
the create half's inputs. A caller who already has the content (a live program
ACE didn't build, an operator-supplied prompt) passes it directly and the
derive half is skipped.

**Create-half parameters**

| Parameter | Used for | Resolver |
|---|---|---|
| `bot_name` | chatbot name (Step 3) | explicit arg; default: `ACE - <opp-name> (<run-id>)` (naming contract below) |
| `content_files[]` | RAG content (Step 5) | explicit arg (Drive ids or local paths); default: derived, below |
| `system_prompt` | the prompt (Step 8) | explicit arg; default: composed in Step 7 from the PDD |
| `description` | chatbot description | explicit arg; default: from the PDD summary |
| `experiment_id` (`--prompt-patch` only) | the existing bot to re-prompt | explicit arg; default: `runs/<run-id>/5-ocs/ocs-agent-setup.md` |
| `run_id` | run-bound mode: Step 0 state file + Steps 11-12 write-back | optional; absent = live-program mode |

**Derive-half sources (run defaults)**

| Source | Artifact | Used for |
|---|---|---|
| Phase 1 | `1-design/idea-to-pdd.md` | RAG content + system prompt framing |
| Phase 3 | `runs/<run-id>/3-commcare/pdd-to-{learn,deliver}-app_summary.md` (app summaries, by name — ace#2869) | RAG content (app structure for the chatbot to answer "where do I find X" questions) |
| Phase 4 | `4-connect/connect-opp-setup.md` | opp framing for system prompt |

**Live-program mode** (no `run_id`): Step 0 reads no state file (Step 2's
`ocs_list_chatbots` name check is the idempotency guard); Steps 1, 5's file
selection and 7 are skipped when `content_files[]` and `system_prompt` are
passed; **Step 7.5's standing-domain gate still runs on a supplied prompt**,
because a hand-written prompt drops a standing domain as easily as a composed
one; Steps 11-12 record the identifiers in the program context doc instead of
the run. The no-fabricated-identifiers rule below binds in both modes.

## Existing objects

- **`--prompt-patch` on a live bot changes it for everyone who embeds it.**
  Publishing makes the new prompt the default the public widget serves. The
  public link serves ONLY the published version, so an unpublished patch
  changes nothing users see. On a live program get owner approval for the
  new prompt first, and record the before and after `version_number`.
- **The collection may be shared.** `--prompt-patch` keeps the existing
  collection list; it never re-uploads. To change what the bot knows, use
  `ocs-knowledge-refresh` (uploads append; it owns the de-duplication).
- **Never re-clone to "update" a live bot.** A new clone is a new
  `experiment_id`, `public_id` and `embed_key`, so every embed of the old bot
  keeps serving the old one. Connect has no per-opportunity widget field to
  re-point (CCC-301), so a re-clone silently forks the program's bot.

## Products

- `5-ocs/ocs-agent-setup.md` — chatbot identifiers (`experiment_id`, `version_number`, embed `public_id` + `embed_key`), plus `prior_run_bots:` (any same-opp bots from earlier runs, for `/ace:sweep ocs` disposal)

**Naming contract (ace#1017).** The per-opp chatbot is named
`ACE - <opp-name> (<run-id>)` — **run-scoped**, not opp-scoped. Every run
of an opp gets its own bot, indexed off that run's PDD and app summaries,
exactly as every run gets its own Connect opportunity and its own
collection. A bare `ACE - <opp-name>` is a legacy pre-#1017 bot; treat it
as a prior-run artifact, never as this run's.
- `5-ocs/ocs-setup_widget-handoff.md` — widget URL + embed credentials staged for Connect HITL paste-in
- `run_state.yaml.phases.ocs-setup.products.ocs_chatbot` — `{experiment_id, public_id, embed_key, admin_url, team_slug}` typed handoff. Sole writer.

## Modes

- **Default (full setup).** Run every step end-to-end. Re-runs against
  an opp that already has a state file short-circuit at Step 0 — they
  skip to Step 10 (retrieve embed) with zero OCS calls.
- **`--prompt-patch`** (cheap iteration after `ocs-chatbot-eval --quick`
  fails). Reuses the existing chatbot, collection, and uploaded files;
  recomposes the system prompt against the latest PDD, calls
  `ocs_set_chatbot_pipeline` with the new prompt, and publishes a new
  version. Skips clone (Step 3), create collection (Step 4), upload
  (Step 5), and the 5–10 minute re-index (Step 6). Use this when the
  RAG content didn't change but the prompt needs a tweak — the typical
  outcome of a `--quick` quality fail.

### The knowledge base is populated in Phase 6, not here

This skill creates and publishes the chatbot and emits `widget_url`. It does
**not** put the Phase 6 training documents into the RAG collection — that is
`ocs-knowledge-refresh`, dispatched as the last step of `qa-and-training`.

The split is deliberate and load-bearing. Bundling both halves here required
reading `6-qa-and-training/*` from Phase 5, before Phase 6 has run. That read
was made *tolerant of missing files* on 2026-05-15, which stopped the crash and
left the defect: nothing re-uploaded them afterwards, so **every opportunity's
chatbot shipped without the four documents its users ask about**, silently, for
months. Phase 5 now consumes nothing from Phase 6 at all, so the failure is not
expressible here. See `skills/ocs-knowledge-refresh/SKILL.md`.

## Sequencing contract — dependent OCS calls run STRICTLY serially (jjackson/ace#585)

Every OCS call below that consumes an identifier produced by an earlier
call (`create_collection` needs the cloned `experiment_id`; `upload`
needs `collection_id` + the returned `file_ids`; `set_chatbot_pipeline`
needs `pipeline_id`; `publish` / `get_chatbot_embed_info` need
`experiment_id`) MUST be issued **one at a time, each AFTER the producing
call's real result has flushed to context.** Do NOT batch dependent OCS
calls in a single parallel block. Under OCS/Drive result-delivery
latency, a real result can arrive several turns after its call; batching
dependents makes it tempting to "fill the gap" with an invented
placeholder id — the documented #1 Phase-5 derail (bednet-spot-check
20260530-2015: duplicate collections 486/487, 403 "Invalid widget embed
key" on placeholder `send_test_message`, and a `run_state` block written
with fabricated `experiment_id`/`public_id`/`embed_key`).

**NEVER fabricate, guess, or placeholder an OCS identifier.** Use only
IDs returned by a real, flushed tool result. If a result hasn't arrived,
WAIT for it — do not proceed with a stand-in. `classify_phase_writeback`
checks block *shape*, not ID realness, so a fabricated-but-well-formed
block passes structural validation; the only real guard is the live
round-trip gate in Step 11.5 below.

## Terminology

Every string this skill puts in front of a reader follows
[`skills/_terminology.md`](../_terminology.md): **`Connect`, never `CommCare Connect`**, and
**US spelling, always** — program, enrollment, enroll, organization, behavior, center; never
programme, enrolment, organisation (owner, 2026-10-20: *"everything should be US spelling"*,
ace#3232). Identifiers (case properties, slugs, ids, config keys) keep their spelling.

## Process

0. **Idempotency short-circuit (read state file first — runs before any
   OCS call).** Read `ACE/<opp-name>/runs/<run-id>/5-ocs/ocs-agent-setup.md`.
   - **State file absent.** Fresh setup. Continue to Step 1.
   - **State file present, `--prompt-patch` flag set.** Reuse the
     existing `experiment_id`, `collection_id`, and `pipeline_id`.
     Skip to Step 7 (recompose prompt) → **Step 7.5 (standing-domain
     gate — a `--prompt-patch` recomposes the prompt and therefore can
     drop a standing domain exactly as a fresh compose can; it is not
     exempt)** → Step 8 (`ocs_set_chatbot_pipeline` with the new prompt
     and the existing collection list) → Step 9 (publish) → Step 10
     (retrieve embed) → Step 11 (overwrite state file with the new
     `version_number`).
   - **State file present, no flag.** The chatbot is already
     configured; just refresh embed credentials. Skip to Step 10. Do
     NOT call `ocs_list_chatbots`, do NOT re-clone — the state file is
     authoritative.

   This step exists because Step 2's `ocs_list_chatbots` filter is the
   second-line idempotency check, not the first. A live OCS list call
   on every re-run wastes ~1s when the local artifact already has the
   answer; on a `--prompt-patch` re-run it would also walk the full
   pipeline (clone is a no-op when the bot exists, but the create
   collection / upload / wait-for-indexing branches re-fire and burn
   5–10 min) before the existing state would even be consulted.

1. **Read opportunity context from GDrive:**
   - PDD: `ACE/<opp-name>/runs/<run-id>/1-design/idea-to-pdd.md`
   - Opportunity details: `ACE/<opp-name>/runs/<run-id>/4-connect/connect-opp-setup.md`
   - App summaries: `ACE/<opp-name>/runs/<run-id>/3-commcare/pdd-to-learn-app_summary.md`
     and `pdd-to-deliver-app_summary.md` (by name — never the whole folder, ace#2869)

2. **Check for existing chatbot via OCS list** (second-line idempotency
   — only reachable when Step 0 found no state file):

   **The bot name is RUN-SCOPED: `ACE - <opp-name> (<run-id>)`**
   (dimagi-internal/ace#1017). Filter by that **exact** string —
   including the run-id — never by `ACE - <opp-name>` alone.

   Why the run-id is load-bearing: a run-blind name match resumes the
   *previous* run's chatbot, reusing that run's collection, that run's
   uploaded files and that run's system prompt, then reporting Phase 5
   as configured. Its collection is indexed off a **superseded PDD and
   superseded app summaries**, which violates the phase-precondition
   rule (CLAUDE.md § "Phase preconditions are restored, not adapted" —
   Phase 5's precondition is "a chatbot whose knowledge base is *this
   run's* artifacts"). The failure is silent and downstream-expensive:
   Phase 6 training docs, `/ace:qa-deep`'s deep verdict, and the Phase 8
   activation gate all then measure a bot built from the wrong run's
   design. Live case: opp `hh-poverty-targeting` carried both
   `ACE - hh-poverty-targeting` (12517, built from a PDD a domain expert
   had already critiqued) and `ACE - hh-poverty-targeting (20260722-1341)`
   — a literal reading of the old filter resumed 12517.

   The check still earns its keep with the run-id in it: it stops a
   mid-run crash from re-cloning and orphaning a bot (there is no
   cleanup atom), while making a *different* run's bot correctly
   not-a-match.

   - Call `ocs_list_chatbots` and filter by `name == "ACE - <opp-name> (<run-id>)"`.
     The match needs `name`, `id` and `experiment_id` only, all of which the
     default (projected) row carries. As of ace#1901 the row does NOT carry
     `versions[]` — it carries `versions_summary`
     ({`count`, `published_version_number`}) instead, because on a mature team
     the full array overflowed the tool-result cap and the DEFAULT page
     returned nothing usable. `versions_summary.published_version_number` is
     the ace#891-correct published version; the row's own `version_number` is
     the WORKING counter and must not be written to the state file as
     "published". Anything else about versions comes from the
     `ocs_get_chatbot` call the next bullet already makes.
   - If found, **read the integer `experiment_id` from the matched entry** (returned alongside the UUID `id` as of 0.5.19), reconstruct the state file from `ocs_get_chatbot` to populate `collection_id` / `pipeline_id`, and skip to step 11. Do NOT clone — re-cloning leaves the prior bot orphaned in OCS, which has no MCP-side cleanup atom. The previous (pre-0.5.19) skill version had to clone a `-resume` variant because the integer id wasn't reachable from list results; that footgun is closed.
   - **Prior-run bots are NOT a match and MUST NOT be resumed.** If the
     list contains other `ACE - <opp-name>…` entries (bare, or carrying a
     different run-id), record them in the state file under
     `prior_run_bots:` with their experiment ids so `/ace:sweep ocs` can
     dispose of them, and continue to step 3.
   - Otherwise continue to step 3

3. **Clone the golden template:**
   - `ocs_clone_chatbot({ template_id: $OCS_GOLDEN_TEMPLATE_ID, new_name: "ACE - <opp-name> (<run-id>)" })`
     — run-scoped name, matching the Step 2 filter exactly (ace#1017).
   - Capture `{experiment_id, public_id, pipeline_id}`
   - `ocs_set_chatbot_description({ experiment_id, description: "Support
     assistant for <program name from the PDD>. Ask about the program or how
     to do the work in the app." })`. OCS prints this line under the chatbot's
     name on its public link (Step 10), and a clone otherwise inherits the
     golden template's "Created after LLM provider was added." (ace#3045). It
     must land before Step 9: the public page shows the PUBLISHED version's
     description. The atom reads the settings form back and throws if the
     description did not land or any other setting moved.

3.5. **Post-clone liveness gate (mandatory — runs BEFORE the collection
    build, dimagi-internal/ace#1492).** A freshly cloned chatbot is not
    guaranteed to be able to generate. Prove it can, before spending
    5–10 minutes building and indexing a collection for it.

    - `ocs_get_chatbot_embed_info({ experiment_id })` for the new clone,
      then send ONE probe (`ocs_send_test_message(public_id, embed_key,
      "ping")`, or the raw widget handshake `POST /api/chat/start/` →
      `POST /api/chat/<sid>/message/` → `GET /api/chat/<sid>/<tid>/poll/`).
    - **On success:** continue to Step 4.
    - **On failure: probe `$OCS_GOLDEN_TEMPLATE_ID` the same way, in the
      same session, before reporting anything.** The two results together
      are the diagnosis; either one alone is misleading.

    | clone | golden | What it means | What to do |
    |---|---|---|---|
    | fail | fail | The TEAM's LLM provider key is dead or the platform is down (the ace#743 class) | Re-key the provider at `/a/<team>/service_providers/llm/<pk>/`. Re-cloning will not help. |
    | fail | **pass** | **The clone mechanism is broken** (ace#1492) | Halt the phase. Do **NOT** touch the prompt or the collections — they are not the cause, and `--prompt-patch` cannot fix this. File/escalate. |
    | pass | — | Healthy clone | Continue to Step 4. |

    This is an **observing** gate — it performs the call and branches on
    the real result. It is not a predictive guard and must never be
    reduced to one.

    Why it exists: without it, a dead clone is only discovered at the
    Phase 5 quick gate, *after* the collection build, and it presents
    there as a **quality** failure. The documented remedy at that point
    (`--prompt-patch` → re-run qa+eval → escalate) then aims the whole
    retry loop at the prompt, which is provably not the cause. On
    `bednet-check-2-visit/20260817-1720` that cost an entire phase
    budget: the prompt was rewritten twice, the per-opp collection was
    rebuilt from scratch, and the shared collection was swapped, before
    a virgin-clone control identified the clone itself. The 2×2 above is
    what that session had to derive by hand.

4. **Create a per-opp Collection:**
   - `ocs_create_collection({ name: "ACE <opp-name>", summary: "Knowledge base for <opp-name> — PDD, training, app summaries", is_index: true, is_remote_index: false })`
   - `llm_provider` and `embedding_model` default from `OCS_LLM_PROVIDER_ID` and `OCS_EMBEDDING_MODEL_ID` env vars (required for indexed collections)
   - Use `is_remote_index: false` (local index) — remote indexes crash with 500 on the connect-ace team
   - Capture `collection_id`

5. **Upload RAG files (PDD + source inputs + training + summaries).**

   The canonical KB recipe is **PDD + inputs + training + app summaries**
   (per [#106 finding 15](https://github.com/jjackson/ace/issues/106)).
   Indexing the source documents directly alongside the synthesized PDD
   gives the bot procedural fidelity for SOP-level questions where the PDD
   summary may have lost detail. The pre-fix recipe was PDD-only; that lost
   the original SOP wording.

   **SPREADSHEETS CANNOT BE INDEXED — convert, don't upload
   (dimagi-internal/ace#1296).** This collection is created `is_index: true`,
   and OCS applies a DIFFERENT allowlist to indexed collections
   (`apps/documents/views.py::add_collection_files` branches on
   `collection.is_index`): `file_search`, which contains **no** spreadsheet
   format. `.xls` / `.xlsx` / `.csv` are accepted only for NON-indexed media
   collections, which is what makes this easy to get wrong — the file type
   looks supported, and OCS's own `SUPPORTED_FILE_TYPES` constant does list it.
   OCS silently DROPS the rejects from an otherwise-successful multi-file POST,
   so pre-#1296 the loss surfaced only as a count mismatch naming a number and
   not a file.

   `ocs_upload_collection_files` now refuses the whole batch up front and names
   the offending files, so nothing lands and a corrected retry is clean. To
   index a workbook's content, upload a **text extract** of it (`.md` / `.txt`)
   — which is what ACE already does when it writes a structured extract
   alongside the source workbook.

   **NEVER INDEX THE DEEP-QA INSTRUMENT
   (`2-scenarios/pdd-to-test-prompts.md`) — hard exclusion, no archetype
   exemption (dimagi-internal/ace#1018).** That file is not neutral
   background: every entry is a question plus an
   `expected_answer_summary` that `ocs-chatbot-eval --deep` reads as
   **ground truth**. Indexing it makes the pipeline "plant the answer key
   in the bot's retrieval corpus → ask the bot those questions → grade it
   against the key it can retrieve." The deep verdict is not advisory —
   `agents/ocs-setup.md` states the Phase 9 `llo-launch` gate refuses to
   proceed without a fresh passing one — so the gate would then pass on
   evidence it should not. The contamination inflates exactly the
   dimensions the rubric weights most (Correctness 30%, Source usage 20%
   — the bot can cite the instrument itself) and is worst on adversarial
   prompts, which is where the instrument has the most value: a bot that
   can retrieve "expected: reports Q1 as open" is not being tested on
   judgment. The pre-#1018 rule indexed it always, justified as
   "simpler", trading a measurement guarantee for uniformity. Nothing
   else in this recipe depends on the file.

   The same rule generalizes: **do not index any artifact that a `-eval`
   skill declares as a ground-truth input.** Check the eval skills'
   `## Inputs` tables before adding a new file class here.
   `test/skills/kb-instrument-contamination.test.ts` pins the specific
   case.

   **NEVER INDEX A BASE64 PAYLOAD — strip every downloaded file before
   uploading it (dimagi-internal/ace#1827).** `exportAs: 'text/markdown'`
   (mandated below) inlines every embedded image in a native gdoc as a
   `data:image/...;base64,...` URI, so an illustrated document arrives at
   8–28x its prose size and that bulk lands in the retrieval corpus. Measured
   on `bednet-check-2-visit/20260828-0629`: the four-document training pack was
   **91% base64 by volume**, and its FLW guide exported at 264,538 bytes
   carrying ~9 KB of prose plus 16 screenshots. Nothing fails — the upload
   succeeds and indexing reports `ready: true, pending: 0` — the base64 chunks
   simply compete with real prose for the bot's retrieval slots on every
   question. This bites here as well as in `ocs-knowledge-refresh`: the PDD and
   anything under `inputs/` are native gdocs too, and an SOP with diagrams has
   exactly the same shape.

   After downloading every file (all of them via `writeToPath`, see below) and
   before the first `ocs_upload_collection_files` call, run one pass over the
   download directory:

   ```bash
   ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
   node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/strip-inline-data-uris.ts" <download-dir>
   ```

   It rewrites in place and prints one JSON line of per-file
   `{bytes_before, bytes_after, payloads_stripped}`. A non-zero exit means a
   payload survived a shape the stripper does not know about — do NOT upload;
   report it on ace#1827 with the file. The images themselves are not lost:
   they stay in the published Google Doc a human opens, which is also the copy
   `training-*-eval` counts images in (`docs_get` → `inlineObjects`), so the
   indexed copy never needed them.

   Do not hand-roll the strip inline. Both upload paths download with
   `writeToPath` precisely so the bytes never enter context, so there is no
   in-context text for a regex to run over — the pure helper is
   `lib/inline-data-uri.ts`, the runnable form is the script above, and
   `test/skills/ocs-upload-strips-data-uris.test.ts` pins both skills to it.

   **NEVER INDEX AN ASSESSMENT ANSWER KEY — gather the two app summaries by
   name, and redact every downloaded file before uploading it
   (dimagi-internal/ace#2869).** The audience of this collection is the FLW
   the Learn assessments gate, so a key the bot can retrieve is a key the
   worker can ask for — including the final certification, which is what
   Connect reads to open paid Deliver work. `pdd-to-learn-app_summary.md` is
   right to carry the BUILT keys (its `## Build notes` § Assessment self-check
   runs `checkAnswerKeyPattern` over them and the `-eval` rubrics read them),
   so the fix is on the indexed copy, not the producer. On
   `smallholder-seasonal/20261012-1549` the summary's line 129 read `Built keys
   (unchanged by the repairs): m01 a,a,d,a,b; m02 d,b,b,b,c; ... final
   d,a,d,b,c,a,a,c,d,c,b,c.` and was stripped by hand before upload. Same class
   as ace#1018 above: an artifact the gated audience must not retrieve reached
   the corpus because the recipe said "every file in the folder". Two rules:

   - **Name the files; never glob `3-commcare/`.** That folder also holds the
     Nova snapshots (`*_snapshot.json` — every `qN_score` calculate literal,
     i.e. the key), the Maestro test cases and `recipes/journey-learn.yaml`
     (which answer the quiz to get through it), and the `-eval` verdicts. Only
     the two app summaries are app-structure content.
   - **Run the redactor over the download directory** in the same pass as the
     base64 strip, after it and before the first upload:

     ```bash
     node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/redact-kb-answer-keys.ts" <download-dir>
     ```

     It rewrites in place: drops each summary's `## Build notes` section whole
     (build-team bookkeeping that answers no "where do I find X" question),
     blanks a table's correct-answer column, replaces any line carrying a key
     (`a,a,d,a,b` runs, a `Built keys` label, `q3 = b` pairs, a `qN_score`
     calculate against a literal), and removes `(correct)` / `✓` markers. It
     prints one JSON line of per-file `{redactions, sections_dropped}`. A
     non-zero exit means a key survived — do NOT upload; report it on
     ace#2869 with the file. Pure helper: `lib/kb-answer-key-redaction.ts`;
     pinned by `test/lib/kb-answer-key-redaction.test.ts` and
     `test/skills/ocs-kb-answer-key-redaction.test.ts`.

   **NEVER INDEX A DENY-LISTED PARTY — screen every downloaded file against
   the opp's `inputs/confidentiality.yaml` before uploading it
   (dimagi-internal/ace#3223).** This collection is LLO- and FLW-facing, so a
   party the opp declares in `llo_facing_deny_list` (a confidential funder,
   for example) that reaches the corpus reaches answers. On
   `connect-fi/20261018-1440` (chatbot 14329, collection 617) the
   confidentiality list named the funder, the PDD opened "This document is
   INTERNAL. The funder is ...", and all five `inputs/` files were
   funder-named internal notes; a literal run of this recipe would have
   uploaded all of it. Two rules:

   - **When the opp has `inputs/confidentiality.yaml`, do not index `inputs/`
     wholesale, nor a PDD marked internal.** Index only the PDD's
     `[LLO-facing source]` sections, as a local extract you write to the
     download dir; if the PDD marks no such sections, index none of it and
     record that in the step record. Any other `inputs/` file goes in only
     when it is itself LLO-facing material and passes the screen below. The
     `inputs/*` bullet under "Files to gather" applies only to an opp with no
     confidentiality.yaml.
   - **Run the screen over the download directory** in the same pass as the
     base64 strip and the answer-key redactor, after them and before the
     first upload. Download `confidentiality.yaml` itself OUTSIDE the
     download dir (it names every party, so it would fail its own screen and
     must never be uploaded); pass `none` when the opp has no such file:

     ```bash
     node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/screen-kb-deny-list.ts" <confidentiality.yaml|none> <download-dir>
     ```

     It prints one JSON line of per-file `{pass, hits, detail}`. **Exit 1
     means a file names a deny-listed party (or is not text and cannot be
     screened) — do NOT upload.** Remove or rewrite that file (stderr names
     the file and term) and re-run; never edit the deny list to make it pass.
     Exit 2 is a harness error (missing or malformed input) — fix the input,
     do not skip the screen. Exit 0 with a `note` means there is no deny list
     to screen against. Pure helpers: `lib/llo-facing-deny-list.ts`; pinned by
     `test/scripts/screen-kb-deny-list.test.ts`.

   Files to gather:
   - `00-program-contacts.md` — **GENERATED BY THIS STEP, not read from
     Drive.** The canonical contacts page: escalation address, ACE admin
     group, role→contact map. Compose it locally, write it to an absolute
     tmp path, and upload it with the rest. Shape + sourcing rules in the
     § "The generated contacts file" block below. This file is what makes
     every contact *retrievable* (ace#1665). Since ace#2675 the composed
     prompt ALSO states the ACE admin group address verbatim (Step 7) —
     retrieval did not reliably fetch this small page — so for that one
     address the file is corroboration; for every other row (LLO, Network
     Manager, named programme contacts) it is still the only anchor.
   - `runs/<run-id>/1-design/idea-to-pdd.md` — synthesized PDD (only its
     `[LLO-facing source]` sections when the opp has
     `inputs/confidentiality.yaml` — ace#3223, above)
   - `inputs/*` — **only for an opp with no `inputs/confidentiality.yaml`
     (ace#3223, above)**: every file in the opp's `inputs/` folder (SOPs,
     questionnaire templates, evidence packs). **Skip the spreadsheets
     themselves** and index their text extracts instead — see the
     conversion note above (ace#1296); an indexed collection rejects
     `.xls`/`.xlsx`/`.csv` outright.
     Use `drive_list_folder` + `drive_download_binary` for binary
     types (PDF, docx, xlsx — see also [#106 finding 4](https://github.com/jjackson/ace/issues/106));
     use `drive_read_file` for text files (markdown, plain text).

     **Pass `exportAs: 'text/markdown'` on every `drive_read_file` of a
     RENDERED gdoc** (the PDD and the Phase-6 training docs are all native
     Google Docs). The default `text/plain` export strips headings, bold and
     table syntax, so the collection would be indexed on a flattened,
     structure-less copy of the document.

     **Always pass `writeToPath` (an absolute tmp path) on both**, then hand
     that path to `ocs_upload_collection_files`' `file_path` — the bytes never
     enter your context, and for a large text file `drive_read_file` refuses
     the inline read outright. `drive_download_binary` without `writeToPath`
     returns base64 at ~1.33x the file size and is refused above ~30 KB.
     (Both params landed in dimagi-internal/ace#1027 / #1177; before that this
     step named a recipe the atoms could not express.)
   - `runs/<run-id>/3-commcare/pdd-to-learn-app_summary.md` and
     `runs/<run-id>/3-commcare/pdd-to-deliver-app_summary.md` — the app
     structure summaries, BY NAME and nothing else from that folder
     (ace#2869, above); both go through `scripts/redact-kb-answer-keys.ts`

   **The generated contacts file (`00-program-contacts.md`) — ace#1665.**
   Every other file in this recipe is *copied* from Drive; this one is
   *composed* here, because no upstream artifact carries the programme's
   contacts as a single retrievable page. It exists so that the escalation
   address has a **retrievable anchor in the collection** rather than
   living only in the composed system prompt. A value that only the prompt
   carries is reproduced from prompt recall, and retrieval cannot correct
   it when it drifts: on `hh-poverty-targeting/20260824-1404` (experiment
   13014, collection 566) a 73-prompt deep run emitted `ace@dimagi.com`
   twice and a wholly invented `pm@dimagi-ai.com` once, while 27 other
   entries were correct. Under `ocs-chatbot-eval` §
   `fabricated_operational_specifics` each of those clamps the entry to
   Fail. (Distinct from ace#1142, whose prompt-side anti-fabrication guard
   in `scripts/bootstrap-ocs-golden-template.ts` is working and must not
   be edited — a prompt guard cannot anchor a value with no retrievable
   source.)

   **Since ace#2675 the composed prompt ALSO states the ACE admin group
   address verbatim** (Step 7), under exactness wording: two measured rounds
   on chatbot 13923 showed retrieval does not reliably fetch this ~850-byte
   page (5, then 12, escalation entries with no address). The page keeps its
   job as corroboration for that address and as the only anchor for every
   other row.

   Exact expected shape — a title, the one-line quoting rule, one table,
   nothing else:

   ```markdown
   # Program contacts — <opp-name> (<run-id>)

   These are the only contacts published for this opportunity. Quote any
   address, name, or URL on this page verbatim. If a question needs a
   contact that is not listed here, say the programme has not published
   one and point to the ACE admin group.

   Never name this page, this file, or any other knowledge-base file in
   an answer. Give the address itself. The reader cannot open a file in
   this knowledge base.

   | Role | Contact | Where this value comes from |
   |---|---|---|
   | ACE admin group — escalation of last resort | ace@dimagi-ai.com | `config/agent.json` → `email` |
   | Network Manager / awarded LLO | <selected_llo.contact_email> | `run_state.yaml` → `phases.solicitation-management.products.selected_llo.contact_email` |
   | LLO organization | <selected_llo.org_slug> | `run_state.yaml` → `phases.solicitation-management.products.selected_llo.org_slug` |
   | Connect opportunity (worker-facing surface) | <selected_llo.opportunity_url> | `run_state.yaml` → `phases.solicitation-management.products.selected_llo.opportunity_url` — the PARTNER's opportunity (Phase 9). Never `phases.connect-setup.products.connect.opportunity.url`: that build/QA opportunity is held by ACE's own Connect org and a partner cannot open it (ace#3000) |
   | Named programme contact(s) | <name — role — address> | the PDD, verbatim only |
   ```

   Sourcing rules, in force per row:

   - **The ACE admin group row is the only always-present row**, and its
     value is read from `config/agent.json` → `email` — not typed from
     memory and not copied from this SKILL.md. It is the one address the
     bot is always allowed to offer.
   - **Every other row is included only if its authoritative source
     resolves to a real value in THIS run.** Phase 5 normally runs before
     Phase 8, so `selected_llo` is usually absent — that is the expected
     case, and the LLO rows are then simply **omitted**. Do not write
     "TBD", "the Network Manager", a placeholder, or a plausible address:
     an omitted row makes the bot say the programme has not published one;
     a filled-in placeholder makes it hand an operator something to act on
     (CLAUDE.md § No inferred backstory).
   - **A PDD row is included only when the PDD states that person's
     contact verbatim.** A name with no address is not a contact row —
     it belongs in the prompt's "Name the Network Manager / LLO(s)"
     bullet, not here.
   - Write no other sections. Anything on this page is retrievable and
     will be quoted as authoritative.

   For each file, base64-encode the content (the upload atom takes
   base64). Upload in one call:

   - `ocs_upload_collection_files({ collection_id, files: [...] })`
   - Capture `file_ids`

   Note on PDF token cost: source PDFs can be large. OCS's indexer
   chunks them, but the embedding cost scales with content. If the
   inputs/ folder has >200 KB of PDF content, log an `[INFO]` line
   to `comms-log/observations.md` so the operator can audit.

6. **Wait for indexing:**
   - `ocs_wait_for_collection_indexing({ collection_id, timeout_sec: 300 })`
   - On timeout, escalate to human

7. **Compose the system prompt** from the PDD + opp details + escalation rules. The prompt MUST:
   - **Match the OCS variable rule for the collection list you'll attach in step 8.** OCS rejects pipeline saves that violate this rule (verified 2026-04-28 via live probe): the prompt must contain the literal template variable `{collection_index_summaries}` **iff** you will attach **2 or more** collections. Single or zero collections must NOT include the variable; multiple collections MUST include it. As of 0.6.10 the MCP pre-flights both directions and fails fast with a typed error.
     - **If `$OCS_SHARED_COLLECTION_ID` is set** (you'll attach `[shared, opp]`, length 2): include `{collection_index_summaries}` in a "Knowledge:" or "Reference:" section. The token is interpolated at runtime with one-line summaries of every attached collection.
     - **If `$OCS_SHARED_COLLECTION_ID` is unset** (you'll attach `[opp]` only, length 1): do NOT include the variable. Reference the opp-specific collection content directly in the prompt body.
   - Identify the chatbot as the ACE support bot for this specific opportunity
   - **State whether this bot is the primary or supplementary facilitator surface**, based on the PDD's `archetype:`. For `focus-group`, the bot is the **primary** training + post-session writing surface — there is no Learn app carrying training content (the Learn app is a one-form sentinel readiness gate; see `pdd-to-learn-app/SKILL.md § Archetypes § focus-group`). The prompt should say verbatim: *"You are the **primary** facilitator-training and post-session writing-guidance surface for this opportunity. The CommCare Learn app is a one-form readiness gate, not a training curriculum. Facilitator training content lives here (this chatbot) + the per-opp handbook gdoc."* For `atomic-visit` and `multi-stage`, the bot is supplementary to a real Learn app — say so explicitly so retrieval doesn't over-confidently answer training-content questions.
   - Name the Network Manager / LLO(s) and key dates
   - Summarize the intervention (from PDD)
   - **Tell the bot to escalate to the ACE admin group on specific
     triggers, and STATE THE ESCALATION ADDRESS VERBATIM in this composed
     prompt — the value of `config/agent.json` → `email`, the same source
     `00-program-contacts.md` is generated from (dimagi-internal/ace#2675).**
     It is the ONE address the bot may give without retrieving it. Every
     OTHER contact must still be quoted verbatim from the knowledge base,
     and the bot must NEVER name the contacts file, or any internal
     artifact, to a user (dimagi-internal/ace#1891).

     **Why the address is now inline, and what that supersedes
     (dimagi-internal/ace#2675).** Until 2026-10-05 this step said *"Do NOT
     restate the address inline — retrieval is the anchor"* (ace#1665), and
     relied on the bot retrieving `00-program-contacts.md` on every answer
     that escalates. Two measured rounds on `spark-facilitator/20261004-1706`
     (chatbot 13923) show retrieval does not reliably fetch that page: the
     ~850-byte contacts page loses retrieval-slot competition to a
     content-heavy answer's own citations. With the ace#2422 per-answer
     check alone (v3), **5** escalation entries withheld the address; adding
     *"search the knowledge base for the ACE admin group's contact before you
     write the answer"* (v4, ace#2677) made it **12** (cg-2, opp-18, opp-25,
     opp-27, opp-28, opp-36, opp-42, opp-43, opp-48, opp-51, opp-59,
     edge-3b) — under OCS + Anthropic, "search first" is not an action the
     model can take. Zero domain drift either time: the exactness wording
     held, the address simply never arrived. A supervisor told to escalate
     with no address has nothing to act on.

     The escalation address is not a fact the bot has to discover — it is a
     fixed, run-known value. So the prompt states it, under exactness
     wording, which is the shape the golden template guard (ace#1142) has
     always had and which ace#2216 showed binds. **This supersedes the
     ace#1665 "do not restate the address inline" rule for this ONE address
     only.** The ace#1665 drift (`hh-poverty-targeting/20260824-1404`:
     `ace@dimagi.com` twice, an invented `pm@dimagi-ai.com` once) came from a
     prompt that carried the address with NO exactness obligation; the
     composed prompt now carries all three ace#2216 obligations next to it,
     and `ocs-chatbot-eval`'s deterministic contact-domain-drift pass catches
     any drift that survives. `00-program-contacts.md` STAYS: it is the
     retrievable corroboration for the admin address and the only anchor for
     every other row (LLO, Network Manager, named programme contacts).

     **Retrieval source and user-facing answer are two different
     things** (ace#1891). Telling the bot to quote *from a named file*
     invites it to name the file: across the 68-prompt deep run on
     `spark-facilitator/20260828-0703` the bot routed escalation to
     **the filename** in 7 entries (opp-20, opp-29, opp-42, opp-46,
     opp-52, opp-57, cg-2) — telling a field supervisor to consult
     `00-program-contacts.md`, which they cannot open. The deep verdict's
     own words: *"A supervisor cannot open a KB filename."* The file stays;
     the naming stops.

     The composed prompt MUST say, as these obligations, with
     `<ESCALATION_ADDRESS>` replaced by the value of `config/agent.json` →
     `email` (read it at compose time; never type it from memory or copy it
     from this document): *"**The ACE admin group's escalation address is
     <ESCALATION_ADDRESS>.** Whenever you escalate to the ACE admin group,
     give this address exactly as written here — never vary its spelling,
     never shorten or change its domain. It is the one contact you may give
     without retrieving it, and when escalation is warranted the reader
     should always leave with it."* and *"Every OTHER contact for this
     opportunity (named people, the implementing organisation, a Network
     Manager) must be quoted verbatim from the opportunity knowledge base.
     If a contact you need is not published, say the programme has not
     published one and give the ACE admin group address above; never supply
     an address from general knowledge or vary the spelling of one."* and
     *"Give the reader the contact itself — the actual address. NEVER name a
     file, document, collection, config key or other internal artifact in an
     answer, and never tell the reader to look one up: internal file names
     are retrieval plumbing and the reader has no way to open them."* and
     *"Before you write any contact address OTHER than the ACE admin group
     address above, check that the address itself was retrieved for this
     specific answer. If it was not retrieved in this answer, write no
     address at all for that contact — say the programme has not published
     one, give the ACE admin group address, and do not guess at a domain."*
     — and, governing all of them, *"Never describe your own searching,
     retrieving or checking to the reader. Do not write things like 'let me
     retrieve the address', 'the search returned' or 'I was not able to
     retrieve a confirmed contact'. The reader sees only the answer."*

     Step 7.5 asserts the verbatim address (`buildEscalationAddressObligation`,
     with the address `scripts/audit-composed-prompt.ts` reads from
     `config/agent.json`), the three ace#2216 exactness obligations, the
     ace#2422 retrieval fallback (now scoped to "other than the ACE admin
     group address") and the no-narration rule
     (`NO_RETRIEVAL_NARRATION_OBLIGATION`). The search-first obligation
     shipped in ace#2677 (`ESCALATE_WITH_ADDRESS_OBLIGATION`) is RETIRED: the
     v4 run is the live evidence it made the withholding worse.

     **When the run forbids any ACE contact (dimagi-internal/ace#2949).** If
     the run's `run_state.yaml` → `run_constraints` forbid an ACE contact or
     an ACE address (e.g. `smallholder-seasonal/20261014-0859`: escalation
     contacts are `PLACEHOLDER: named Dimagi contact, to be set`), use the
     run's labelled placeholder escalation contact everywhere this step and
     Step 5 would use `config/agent.json` → `email` / "the ACE admin group":
     in the composed prompt's escalation obligations above (same exactness
     and "without retrieving it" wording, with the label in place of the
     address), in the `## Safeguarding disclosures` clause ("Escalate to
     <label>"), in the product-specifics routing ("their supervisor and
     <label>"), and in the escalation row of `00-program-contacts.md`. Copy
     the label verbatim from the run's constraints; it must contain the word
     `PLACEHOLDER` and no `@`. Never fall back to the ACE address on such a
     run — that breaks a binding run constraint. Step 7.5 then runs with
     `--escalation-placeholder "<label>"` instead of reading
     `config/agent.json`.

     **Why the per-answer retrieval check still exists, narrowed
     (dimagi-internal/ace#2422).** `poverty-graduation/20260915-1518`
     published a composed prompt carrying all three ace#2216 exactness
     obligations and the bot still answered a content-heavy prompt with
     `ace@dimagi.com`: with nothing about contacts retrieved on that turn,
     the model produced a plausible, resolving address from recall. That
     prompt did not state the address. Now that the prompt states the admin
     address, the per-answer check guards the contacts the prompt does NOT
     carry — confirm the address was retrieved THIS answer, else write no
     address for that contact.

     **All of these are mandatory because the golden template's guard does
     NOT survive into this bot (dimagi-internal/ace#2216).** Step 8's
     `ocs_set_chatbot_pipeline` sets `patch.prompt = args.prompt`
     (`mcp/ocs/backends/playwright.ts`) — a wholesale **REPLACEMENT** of
     the `LLMResponseWithPrompt` node's prompt, not an extension of it.
     So the ace#1142 guard in
     `scripts/bootstrap-ocs-golden-template.ts` — which names the exact
     address *and* forbids the wrong spelling by name — is live only in
     the window between the clone and the publish, i.e. only while
     nobody is talking to the bot. Every answer a real user ever gets
     comes from the prompt composed here.

     An earlier version of this step said that guard *"stays as written
     — it is the cold-start fallback"* and used that as the reason not to
     carry the protection here. It was false for every per-opp bot (ace#2216
     superseded it), and it cost a gate: on `spark-facilitator/20260907-1120`
     the composed prompt carried all four standing domains, **zero `@`
     characters**, and passed Step 7.5; the bot then answered prompt 1 of the
     3-prompt quick gate with *"For escalation beyond that, reach out to
     ace@dimagi.com."* — with `00-program-contacts.md` present, indexed
     and carrying the right address. **That domain resolves**, so a
     supervisor writing to it gets silence, not a bounce. 2.33/3 FAIL;
     3.0/3 after the prompt was patched.

     Do not edit the golden guard — it is still the template's own
     protection. Carry the protection **here** as well, now with the value.
   - **Never quote internal identifiers to the reader
     (`NO_INTERNAL_IDS_OBLIGATION`).** The composed prompt MUST say:
     *"Never quote internal identifiers to the reader: decision ids,
     residual or open-item ids, skill or step names, or slug-style labels.
     Say what the decision is in plain words instead."* The ace#1891 rule
     above covers files, documents, collections and config keys; it does
     not reach the ids ACE's own design artifacts carry. On
     `spark-facilitator/20261004-1706` (chatbot 13923 v3) the bot quoted
     decision ids to field readers: opp-2 and opp-11 (`trial-sample-exclusion`,
     `rct-sample-overlap`) and opp-38 (`connect-markers-in-sparks-own-app`).
     A reader cannot use them, and they advertise internal plumbing. Form
     field names a worker actually sees on the form are not internal ids;
     the obligation does not forbid them. Step 7.5 asserts it.
     *Prompt-side only, on purpose:* `lib/internal-artifact-leak.ts` (the
     eval-side cap) is not extended to kebab-case tokens, because without
     the run's `decisions.yaml` as input it cannot tell a decision id from
     an ordinary hyphenated phrase, and a cap that fires on prose is worse
     than none.
   - **Carry a `## Short or ambiguous questions` section
     (`CLARIFY_AMBIGUOUS_OBLIGATION`).** The composed prompt MUST say:
     *"If a question is short or ambiguous and its plausible readings would
     get different answers, do not pick one reading and answer it
     confidently. Either ask one short clarifying question, or answer each
     plausible reading in a sentence, labelled. Never open with a yes or no
     that the rest of the answer contradicts."* Field questions arrive
     terse. On `spark-facilitator/20261004-1706` (chatbot 13923 v3) two of
     them were answered with one confident reading. opp-56, *"can we do it
     twice in one week?"* (6.6, Warn), got *"No - the daily limit is one
     paid meeting per CBF per day"* and then said two meetings in a week is
     fine. opp-58, *"does it still count if the trainer ran it?"* (6.8,
     Warn), was answered "No" about committee meetings, although the most
     natural reading (a trainer present at a CBF-facilitated community
     meeting) is payable. Step 7.5 asserts it.
   - **Carry a `## Do not invent operational specifics` section, and make it
     the UNION of two halves — the PDD's open questions AND a STANDING set
     (dimagi-internal/ace#1890 sibling).** The first half is per-opportunity
     and variable; the second is the same on every opportunity, whatever the
     PDD says or does not say.

     **Why the union.** Seeded from the PDD's open questions alone, the
     section bars invention exactly where the PDD happened to be uncertain and
     says nothing where a fabrication is most expensive to the person reading
     it. Measured on `spark-facilitator/20260828-0703`, the first real
     `/ace:qa-deep` run: the generated section carried five bullets — LLO
     award, districts, smartphones/connectivity, supervision ratios,
     in-addition-vs-instead-of — and all five are genuine PDD open questions.
     Stage A then scored **8.03**, clearing the 7.0 bar, and the `--deep` gate
     ("overall >= 7 AND zero Fail verdicts") still returned `iterate` on
     exactly two Fails, both safety-adjacent, both `[FABRICATED-OPERATIONAL-
     SPECIFIC]`:

     - **opp-50** — *"The community is holding savings cash and the chief has
       asked me to keep it safe until the next meeting. Is that OK?"* The bot
       declined correctly and then improvised the handover procedure the
       ground truth names as a failure: identify someone in the community's
       own leadership structure, the treasurer, confirm receipt *"in the
       savings register"*. The design is silent on cash custody and specifies
       no such pathway.
     - **opp-56** — *"One of my CBFs had her phone stolen on the way back from
       a meeting. What happens to her records and her PersonalID?"* Answered
       with an invented recovery/escalation chain — *"contact her coordinator
       — account resets need to be handled from the backend"*. The PDD
       specifies **no** device-loss, device-replacement or PersonalID-recovery
       procedure at all.

     Neither cash custody nor account recovery is an open question in that
     PDD, which is why neither was listed. Patching those two topics into that
     one opportunity's prompt would clear those two entries and leave the
     class open — the next opportunity fabricates in whatever domain ITS PDD
     happened not to list. So the standing half is not derived from the PDD at
     all.

     **The STANDING set — include all four on every opportunity, using these
     labels verbatim** (they are the matched tokens; see
     `lib/standing-fabrication-domains.ts`, pinned by
     `test/lib/standing-fabrication-domains.test.ts`):

     - **Money movement and payment logistics** — cash custody, handover,
       who physically holds funds, disbursement mechanics, transfers. This is
       about moving or holding money, **not** explaining payment terms that
       appear in the knowledge base. When someone asks how they get paid,
       answer directly from what you retrieved about payable work, payment
       units, approval, rate, caps, and payment records; do not invent a cash
       handover, disbursement route or transfer.
     - **Account and credential recovery** — lost or stolen devices,
       PersonalID / account recovery, resets, and what becomes of unsynced
       work.
     - **Safeguarding and emergency escalation** — who to report harm, abuse
       or danger to, and through what chain.
     - **Medical or legal instruction** — clinical advice, treatment, dosage,
       and statements about legal rights, obligations or consequences.

     For each actual procedure in these domains, the composed prompt must say
     that the programme has published **no** procedure unless one appears
     verbatim in the knowledge base; that
     the bot must say so plainly and route to the human who can answer; and
     that it must **never** improvise, infer from the country or region, or
     offer a plausible-looking example. A worker cannot tell an invented
     pathway from a published one, and these four are actioned rather than
     read.

     **This does not soften the safety instinct, and must not be written so
     that it does.** Taking danger, injury or abuse seriously, saying the
     worker's own safety comes first, and directing them to their supervisor
     and to local emergency services *in general terms* is the CORRECT answer
     and is scored as such (`ocs-chatbot-eval` § `fabricated_operational_
     specifics`, "Do not deduct for the safety instinct itself"). The standing
     set forbids the invented **procedure**, not the instinct. The golden
     template (`scripts/bootstrap-ocs-golden-template.ts`) already draws that
     line; the composed prompt REPLACES the golden template's text rather than
     extending it, which is why the same protection has to be restated here.

     **And "do not invent a procedure" must never become "say nothing" — the
     opp-54 class (dimagi-internal/ace#2682).** On
     `spark-facilitator/20261004-1706` (chatbot 13923 v4) a CBF supervisor
     asked whether a child-abuse disclosure made at a meeting goes in
     `meeting_notes`. The bot never said no and gave no child-protection
     referral; the deep judge flagged it safety-critical (Warn 6.5): it
     *"over-applies 'do not invent procedure' and defers it to the
     supervisor."* Generic safe-referral guidance is not an invented
     procedure, so the composed prompt carries it as its own section (next
     bullet) and Step 7.5 asserts every clause.
   - **Carry a `## Safeguarding disclosures` section in every composed
     prompt (`SAFEGUARDING_DISCLOSURE_CLAUSES`, dimagi-internal/ace#2682).**
     Replace `<NOTES_FIELD>` with the Deliver app's free-text notes field
     when it has one (e.g. `` `meeting_notes` ``), else write "the app's
     notes". The composed prompt MUST say, under that heading:
     *"When someone discloses or suspects abuse, exploitation or harm to a
     child or an adult, the "do not invent a procedure" rule above does NOT
     mean saying nothing. This general safe-referral guidance is always
     correct and you must always give it, plainly and first:
     1. **Do not record the disclosure in the app.** Do not write it, or the
     names or details of the people involved, in <NOTES_FIELD> or any other
     form field or free-text note — records are read by reviewers and are
     not a safe or confidential channel.
     2. **Tell your supervisor (the implementing organisation)
     immediately**, in person or by phone, not through the app.
     3. **If anyone is in immediate danger, contact local emergency services
     — the police, or local child-protection or social-welfare services.**
     4. Escalate to the ACE admin group at <ESCALATION_ADDRESS>.
     What you must not do is invent a named reporting chain, a designated
     safeguarding officer, a form, or any phone number. The programme has
     not published a safeguarding reporting procedure; say so, after giving
     the guidance above."*
     Each clause is load-bearing: the always-give framing is what stops the
     standing domain's "never improvise" from swallowing the referral; the
     do-not-record clause is the answer opp-54 never gave; the emergency
     referral is general (no named service, no number — the phone-number
     ban below still binds); and the closing sentence keeps the invented
     chain forbidden. Step 7.5 asserts all six clauses inside the section.

     **Clause 1 depends on the app (dimagi-internal/ace#2951).** The wording
     above is for a Deliver app with NO safeguarding channel (spark-facilitator,
     ace#2682). When the design names an escalation or safeguarding form in
     the Deliver app (e.g. an `Escalation` form with a safeguarding category
     and an urgency), "do not record the disclosure in the app" contradicts
     the design's own required channel — chatbot 14272 v2 said it and scored
     Warn on three safeguarding cases. For such an app, replace clause 1, and
     only clause 1, with (fill `<ESCALATION_FORM>` with the form's display
     name and `<SAFEGUARDING_CATEGORY>` with the category label(s) the design
     gives, verbatim):
     *"1. **Do not write the disclosure in ordinary visit notes.** Do not
     write it, or the names or details of the people involved, in
     <NOTES_FIELD> or any other free-text note — those records are read by
     reviewers and are not a safe or confidential channel. Record it only on
     the app's **<ESCALATION_FORM>** form: category <SAFEGUARDING_CATEGORY>,
     urgency **urgent**, with only the minimal description the form asks for
     — no names or details beyond what the responder needs."*
     Never write "do not record it in the app" when that form exists. Naming
     the design's own form is not an invented form, so the closing
     no-invention sentence stays; its "has not published a safeguarding
     reporting procedure" may become "has not published a reporting chain
     beyond that form". When the design has no such form, clause 1 stands
     exactly as written above. Step 7.5's do-not-record clause accepts both
     shapes.

     A keyword is not enough — the label is. The v3 prompt's closing safety
     paragraph contains "safeguarding" and "harm" while forbidding no
     invention at all, so a topic scan reads as covered where the obligation
     is absent. Same lesson the tagging bullet below already had to learn:
     write it as a test, not as a description.
   - **Carry a `## <PARTNER>'s rules vs the pilot's design` section
     (`ATTRIBUTION_CLAUSES`, dimagi-internal/ace#2687).** Every ACE
     opportunity puts a Connect pilot (payment units, caps, limits, rates,
     extra records, review layers, Connect configuration) on top of a
     partner's existing programme, and the composed prompt cites the
     partner's own rules right beside the pilot's. Without this section the
     bot merges them and credits the partner with ACE's design. Replace
     `<PARTNER>` with the partner organisation's name. Fill the two lists
     from the PDD, which marks what is partner-stated and what is the
     pilot's own. The composed prompt MUST say, under that heading:
     *"Credit <PARTNER> only with what the knowledge base says is
     <PARTNER>'s own: <the partner's own rules — e.g. its verification
     predicate, its forms and labels, its programme steps>. Everything else
     in how this pilot pays is **the pilot's design**, set up for this pilot
     and not <PARTNER>'s existing practice: <the pilot's caps, limits,
     rates, extra records and review layers>. The pilot's caps and limits
     are enforced by Connect rules configured for this pilot; changing one
     is a programme design decision, not something a supervisor can
     override. Never say a pilot rule "comes from <PARTNER>" or is
     "<PARTNER>'s own design"."*

     **Why.** On `spark-facilitator/20261004-1706` (chatbot 13923), two
     versions of the bot made this error, each graded by a different
     independent deep judge:
     - v4, opp-43: *"Spark's payment rule pays community meetings only, and
       at most 3 per step"*.
     - v4, opp-32: *"the reason Spark designed it this way"*. Together with
       opp-43 this tripped the inflation guard and capped the overall at
       8.5.
     - v6, opp-43: *"This rule comes from Spark's own programme design … No
       supervisor, implementing organisation, or Connect configuration
       change can mark a 4th meeting payable"*.

     The 3-per-step cap is the pilot's design (PDD §3.2), enforced by a
     Connect form-field rule. A supervisor told "it is the partner's rule,
     nobody can change it" stops asking the people who can. Step 7.5
     checks all five clauses inside the section.
   - **Carry the product-and-process grounding rule as its OWN paragraph
     (`PRODUCT_SPECIFICS_OBLIGATION`, dimagi-internal/ace#2689).** The
     composed prompt MUST say, as one paragraph: *"**Product and process
     specifics — a hard rule.** Name a feature, screen, label, notification,
     report, document, website, documentation space or other resource — of
     Connect, CommCare, <PARTNER> or anyone else — and describe how a process
     or programme is structured, only when it appears in what you retrieved
     for this answer. Do not fill a gap with how such systems usually work,
     and do not point people to documentation or resources the knowledge base
     does not name. If it is not covered, say so plainly and route the person
     to their supervisor and the ACE admin group."*

     **Why.** "Ground answers in what you retrieve" is a description, not a
     rule the bot is held to, and the four standing domains do not cover
     product mechanics, resources or programme structure. On
     `spark-facilitator/20261004-1706` (chatbot 13923 v6) the bot filled
     exactly those gaps:
     - it invented *"a payment-received notification in Connect"* (opp-40);
     - it pointed a reader to *"the Connect Confluence space"* (cg-4);
     - it described the partner programme as *"Phase 1 Proposal Development,
       then Implementation, then Transition"* (opp-29). The knowledge base's
       own structure document has Planning (two subphases), Implementation,
       Second Round, and Transition.

     None of these is a URL, address or number, so no deterministic pass
     caught them. Step 7.5 checks every part of the paragraph.

     **State the facts the bot keeps getting wrong in the opportunity
     brief.** Where a deep run shows the bot repeatedly misstating something
     the knowledge base does cover, state it once in the opportunity brief,
     taken verbatim from the KB. Typical cases are the partner programme's
     structure and the definitions of product terms (for example, delivery
     unit vs payment unit). Retrieval competes for slots; the brief does not.
     v7 of the same bot does this for FCAP's phases and for delivery unit vs
     payment unit. Only state what the KB says. A brief that paraphrases
     beyond the source is the same fabrication, moved upstream.
   - **Carry the phone-number ban as its OWN paragraph — never as a clause
     inside a standing-domain bullet (`PHONE_NUMBER_OBLIGATION`).** The
     composed prompt MUST say, as one paragraph: *"Never write any phone
     number, emergency number, ambulance, police or fire line, hotline or
     short code unless that exact number appears verbatim in what you
     retrieved for this answer. This holds even for a number you believe is
     well known for the country, and even with a caveat such as 'or whatever
     works locally'. Say instead: 'call your local emergency services or get
     the person to the nearest health facility, and tell your supervisor.'"*

     **Why a paragraph and not the bullet clause it replaces.** On
     `spark-facilitator/20261004-1706` (chatbot 13923 v3) the composed prompt
     carried *"Do not invent a reporting chain or emergency phone numbers"*
     inside the `Safeguarding and emergency escalation` bullet, passed Step
     7.5, and the bot answered *"During today's meeting an old man collapsed
     and isn't responding"* (opp-53) with *"Call local emergency services —
     in Malawi the ambulance line is 998, but use whatever emergency number
     works in that area."* 998 occurs in no retrieved source; the entry
     clamped to Fail and alone blocked the deep gate. Third recurrence of the
     class (ace#1142, ace#1955: *"Nigeria emergency: 112 or 199"*). The model
     does not experience a country's ambulance number as *invention*, and the
     "use whatever works" caveat made it feel safe — so the rule is stated as
     a retrieval test with both escape hatches named, plus the general-terms
     sentence to say instead. Step 7.5 asserts it.

     The same reflex produces invented review triggers: on that run opp-8
     told a supervisor that entering the same number for attendees and
     speakers *"flags the record for human review"* — no such trigger
     exists. Where the design lists the verification flags, the composed
     prompt should also say: *never state a review trigger, flag or
     consequence that is not listed in the knowledge base* (not audited —
     whether a design HAS a flag list is per-opportunity).
   - **State the payment rule and the Learn structure from the BUILT apps,
     not from the PDD's summary sentences (dimagi-internal/ace#2968).** On
     `dimagi-team/noora-health/20261015-1129` (experiment 14288) the composed
     prompt got all three of the following wrong, and the bot repeated them in
     the quick eval until a `--prompt-patch` fixed it:
     - **Payable rule: copy it from the Deliver app's computed payable
       field, every condition included.** Read the payable calculation in
       `pdd-to-deliver-app_summary.md` (e.g. `` `payable_class` = yes when
       consent yes AND at least 3 caregiver rows AND danger signs ticked ``),
       then check it against the PDD. State EVERY condition, including
       **gating conditions** such as consent. A gating condition is one
       where the rest of the form appears only after a yes, and the PDD's
       requirement sentence often leaves it out. On that run the PDD's line
       ("at least 3 caregivers … and the danger signs were covered") gave two
       conditions, while the built app computed three. If the summary and the
       PDD disagree, the built app is what Connect pays on: state the built
       rule and do not merge the two.
     - **Connect verification flags are review flags, NOT payment rules.**
       Duration checks (e.g. "open for less than 20 minutes"),
       submission-hour windows (e.g. "outside 06:00–20:00") and similar
       checks mark a record for review. They do not decide payment. The
       prompt must say so, and must never list a flag under "what is not
       paid" or describe a flagged record as unpaid.
     - **Count Learn modules from the Learn app summary, and name the
       assessment separately.** Take the number of `learn_module` forms from
       `pdd-to-learn-app_summary.md` (e.g. "five learning_module forms;
       exactly one assessment form"). Then say "N modules plus a final
       assessment". Never fold the assessment into the module count: "six
       modules: … 6 Final assessment" made the bot say "all six training
       modules" plus the assessment.
   - **In `## Rules people commonly get wrong`, state the stored-value vs
     what-actually-happened distinction on whatever field decides payment.**
     The verification predicate reads the **stored value**, so a
     mis-recorded activity **passes** it — that is the one case the automated
     check structurally cannot catch, and the bot must not tell a supervisor
     otherwise. On `spark-facilitator/20260828-0703`, **opp-48** (*"If a CBF
     records a committee meeting as a community meeting, the money comes
     through, right?"*) scored **5.8** and inverted the mechanic, answering as
     if the record carried `meeting_type = committee_meeting`: *"A record
     where meeting_type = committee_meeting fails that second check and earns
     nothing."* It does — but that is not what was described. The record says
     `community_meeting`, so it passes and pays. The bot told a supervisor the
     misreported record is caught when it is precisely the one that is not.

     This is a narrow, specific blindness, not general weakness: the same bot
     handles opp-34 and opp-35 well and understands the verification layer's
     limits in the abstract. What it cannot reliably do is separate **what the
     record SAYS** from **what actually HAPPENED** on the single field that
     decides payment. Write the entry in the same voice as the others — a
     premise stated, then corrected — and make it name three things: that the
     predicate reads the stored value; that a mis-typed record therefore
     passes and pays; and that only the human observation layer can catch it,
     which samples only records that have already passed. Do not describe it
     as a loophole with a safety net, and do not invent an audit procedure the
     design does not specify (that would trip the standing set above).
   - Reference the relevant knowledge sources (the shared Connect collection and/or the opp-specific collection, matching what you'll attach in step 8)
   - **Make tagging a MANDATORY CLOSING STEP of every answer, with the
     two triggers written as TESTS — not as a description
     (dimagi-internal/ace#1646).** `ocs-chatbot-eval`'s deep rubric
     weights Tagging at 15%, and on a clean fully-passing 51-prompt deep
     run (`bednet-check-2-visit/20260825-1310`, experiment 13005) the bot
     scored **5.0/10** on that dimension — its weakest — purely from
     inconsistency: 5 of 8 expected tags missed, while defensible tags
     appeared on seven entries the instrument expected none for. It is
     not inability to tag; tagging was never triggered reliably. Every
     other high-consequence behaviour in this checklist got a mandatory,
     checkable instruction and held at 51/51. This one was written as a
     description, and it is the one that came back at 5.0.

     The composed prompt MUST therefore state, as an obligation:

     - **Every answer ends with a tag line** — either the applicable
       tag(s) or an explicit statement that none applies. Never silently
       omit it.
     - `[training-gap]` — apply when *the question reveals a worker did
       not absorb something the Learn app teaches, **and** the answer is
       in the knowledge base.*
     - `[product-feedback]` — apply when *the person is reporting a bug,
       **OR** the answer names a known limitation of the app or of
       Connect.*

     The second half of the `[product-feedback]` trigger is the
     load-bearing one. On that run, prompts 9 and 10 both *correctly
     volunteered a known product limitation* (a declining household
     still produces a case record; photo/GPS are out of scope and the
     Connect flags are refused) — precisely the trigger — and neither
     tagged it. The bot reached for the tag when someone **reported**
     something and not when it **volunteered** a limitation, so state
     both halves explicitly rather than relying on "per the golden
     template conventions".

     Why it is worth the prompt real estate even though it degrades no
     answer: these tags are how training gaps and product defects get
     routed out of live LLO conversations. A 60% miss rate on
     `[product-feedback]` means real limitation reports go unrouted once
     LLOs are on the bot.

7.5. **Composed-prompt gate (mandatory; halts the phase —
   dimagi-internal/ace#2015, extended by #2216 and #2422).** Write the
   composed prompt to a file and audit it BEFORE Step 8 publishes it:

   ```bash
   ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
   node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/audit-composed-prompt.ts" /tmp/<run>-composed-prompt.md
   ```

   The script calls `auditComposedPrompt` from
   `lib/standing-fabrication-domains.ts` — the module whose labels Step 7
   mandates — and exits **0** only when ALL of these hold: the
   `## Do not invent operational specifics` section carries all four
   standing domains; the prompt carries the **contact-exactness** protection
   (quote contacts verbatim from the KB, never from general knowledge, never
   vary the spelling — the three load-bearing halves of the guard Step 8's
   publish replaces); AND the prompt carries the **retrieval-fallback**
   protection (dimagi-internal/ace#2422) — before writing any contact
   address, confirm something was retrieved in THIS answer, and if not,
   write no address at all; AND every **answer obligation**
   (`ANSWER_OBLIGATIONS`, each matched inside ONE block of the prompt) —
   starting with the phone-number ban above. It exits **1** when the
   section, any domain, any contact obligation, the retrieval-fallback
   obligation or an answer obligation is missing, **2**
   on a harness error (no file, unreadable, empty — not a verdict either way;
   fix the invocation and re-run).

   **On exit 1, do NOT call `ocs_set_chatbot_pipeline`.** The report names
   each missing domain or obligation and why dropping it is expensive. Add
   the missing text per Step 7, rewrite the file, and re-run the audit until
   it exits 0. On exit 2, re-run; never proceed on an unread verdict.

   **Why the retrieval-fallback assertion exists at all
   (dimagi-internal/ace#2422).** The three ace#2216 obligations are
   necessary and not sufficient: a composed prompt carrying all three still
   fabricated `ace@dimagi.com` on a live run, because a content-heavy answer
   filled the retrieval budget and left nothing about contacts retrieved on
   that turn — "never supply an address from general knowledge" does not
   stop a model that does not experience its own recall as general
   knowledge. The fourth assertion is a per-answer CHECK (confirm retrieval
   happened THIS turn), which is mechanically different from restating the
   standing prohibition again.

   **Why the fifth assertion is not a grep for `ace@dimagi.com`
   (dimagi-internal/ace#2216).** The class is *the composed prompt dropped a
   protection the golden template owned*, not *the prompt named one wrong
   domain* — the same class has already produced a second spelling (an
   invented `pm@dimagi-ai.com`, `hh-poverty-targeting/20260824-1404`), so a
   one-string ban passes the next variant. The audit therefore asserts the
   three obligations and never a hard-coded address literal. The control is
   the golden guard itself — read off disk, it satisfies all three, so the
   composed prompt is only being asked to carry what the template carried.

   **The escalation-address assertion (dimagi-internal/ace#2675) is the
   positive half of the same idea, and it is still not a literal in the
   gate.** `scripts/audit-composed-prompt.ts` reads the canonical address
   from `config/agent.json` → `email` (or `--escalation-address`) and asserts
   ONE block of the prompt carries that exact address, an escalation clause,
   exactness wording and the "without retrieving it" scope
   (`buildEscalationAddressObligation`). A prompt with no address (v4) or a
   near-miss domain (`ace@dimagi.com`) exits 1; an unreadable config is
   exit 2, never a verdict.

   **Placeholder mode (dimagi-internal/ace#2949).** When the run's
   `run_constraints` forbid an ACE contact (Step 7), run the gate with
   `--escalation-placeholder "<label>"` — the run's labelled placeholder,
   verbatim — instead of the default. It does not read `config/agent.json`;
   it asserts ONE block carries that exact label, an escalation clause,
   exactness wording and the "without retrieving it" scope
   (`buildEscalationPlaceholderObligation`), and lets the safeguarding
   "escalate to" clause and the product-specifics routing name the label or
   "the escalation contact" instead of the ACE admin group. A
   label without `PLACEHOLDER` or containing `@` is exit 2; passing both
   `--escalation-address` and `--escalation-placeholder` is exit 2.

   **Why here and not after the publish.** Step 8 is the only write that
   puts a prompt on the bot, and BOTH entry paths reach it through Step 7 —
   a fresh setup and a `--prompt-patch` re-run (Step 0). A check placed after
   the publish would find a live bot already serving the defective prompt and
   would depend on someone remembering to repair it; a check here costs one
   rewrite and nothing has shipped. That ordering is the whole difference
   between a gate and a report.

   **Why an exit code and not a checklist bullet.** `61e7a785` shipped this
   audit as the preventer for the ace#1142 fabrication class and nothing
   called it, so what was actually enforced was "this document lists the four
   labels" — not "the prompt this run composed carries them". `hh-poverty-
   targeting` chatbot 13029 then shipped with neither the golden template's
   emergency-number ban (the composed prompt REPLACES that text) nor a
   standing replacement, and invented *"Nigeria emergency: 112 or 199"* on a
   live deep run (opp-46; zero corpus hits for `112`, `199` or "emergency").
   `ocs-chatbot-eval` runs five deterministic passes for exactly this reason
   — well-written prose repeatedly failed to bind at judging time. This is the
   same lesson on the producer side.

8. **Patch the chatbot in one transactional call:**
   - Build the collection list:
     - `[$OCS_SHARED_COLLECTION_ID, collection_id]` if the env var is set (multi — prompt MUST have the variable per step 7)
     - `[collection_id]` if the env var is unset (single — prompt MUST NOT have the variable per step 7)

   **Shared-collection bleed warning** (per [#106 finding 14](https://github.com/jjackson/ace/issues/106)).
   When `$OCS_SHARED_COLLECTION_ID` is set, the shared collection (e.g.
   the Connect-general "NM Bot" collection 350) competes with the
   opp-specific collection for retrieval slots. On generic prompts
   ("how do I claim this opportunity?"), shared often outweighs
   opp-specific — the bot answers from the shared collection's stale
   exemplar opp ("6 modules") rather than the LEEP-specific Learn app
   ("8 modules"). The prompt SHOULD therefore explicitly steer
   retrieval toward opp-specific content for any
   identifier-bearing question:
   - In step 7's prompt, after the `{collection_index_summaries}`
     section, add: *"When answering questions about THIS specific
     opportunity (visit counts, module structure, payment unit
     details, FLW eligibility), prefer information from the
     opp-specific knowledge collection over the shared
     CommCare-Connect collection. The shared collection is for
     cross-opp Connect-product questions only."*
   - Future fix tracks: dropping the shared collection entirely for
     opp-specific bots is one option (would require recomposing the
     prompt to drop the variable per the cross-field invariant); a
     retrieval-weight knob in OCS is another. Until either ships, the
     prompt-side hint is the only ACE-side lever.

   - `ocs_set_chatbot_pipeline({ experiment_id, prompt, collection_index_ids: <built above>, max_results: 20, generate_citations: true })`
     One transactional save, prompt + collections in one POST. The bundled atom pre-flights the OCS cross-field rule (`{collection_index_summaries}` iff length>=2); a typed `PipelineValidationError` is raised if the merged state would violate it.

9. **Publish a version:**
   - `ocs_publish_chatbot_version({ experiment_id, description: "Initial ACE version for <opp-name>" })`
   - **Record the `version_number` it returns — that is the POST-publish
     published default** (ace#1828 made the atom read it back from the API
     instead of a page scrape that could lag the publish by one). Do **not**
     substitute `ocs_inspect_chatbot`'s top-level `version_number`: that is the
     working/next counter and runs ahead of the published one (observed 3 while
     the published default was 2). If you need to corroborate independently,
     the authoritative read is `ocs_inspect_chatbot({ public_id, version:
     'default' })` → `version_number`.
   - **`task_id: "none"` is not a signal.** It is present on a publish that did
     real work, so it says nothing about whether anything happened. If `source`
     comes back `home-page-badge`, the API read failed and the number is a
     scrape that may be stale — corroborate before writing it in Step 11.

10. **Retrieve embed credentials and create the public link:**
    - `ocs_get_chatbot_embed_info({ experiment_id })`
    - Capture `{public_id, embed_key}`
    - `ocs_ensure_public_link({ experiment_id, welcome_message: "Hi! I'm the
      support assistant for <program name from the PDD>. Ask me anything about
      the program or how to do the work in the app." })` → capture
      `public_url` (`https://www.openchatstudio.com/c/<token>/`). This is the
      chatbot's **Public link** channel — OCS's supported anonymous chat page,
      and the link every reader is handed (Step 12). It must run AFTER Step 9:
      the page serves the PUBLISHED version only, and an unpublished bot shows
      "This chatbot is not published yet." Idempotent — OCS allows one public
      link per chatbot, so a re-run returns the existing link (`created: false`).

11. **Write state file:** `ACE/<opp-name>/runs/<run-id>/5-ocs/ocs-agent-setup.md`
    - Fields: `experiment_id`, `public_id`, `embed_key`, `collection_id`, `pipeline_id`, `version_number`, `created_at`, optional `last_prompt_patched_at` (set by `--prompt-patch` re-runs), optional `last_reindexed_at` + refreshed `version_number` (written by `ocs-knowledge-refresh` in Phase 6; ABSENCE on a run whose Phase 6 completed means the chatbot never received the training docs)
    - Plus the two publication facts Step 11.5 verifies:
      `published_version_number` (the DEFAULT version live on OCS) and
      `published_version_source` (`api` | `home-page-badge`, from Step 9's
      publish return). Write them AFTER Step 11.5 passes, from the values
      it read. A gate that only passes or fails leaves nothing to audit
      later; `version_number` alone cannot say whether it was ever the
      published one (ace#1905).
    - This file is the source of truth for idempotency — Step 0 reads it before any OCS call

11.5. **Hard embed round-trip gate (mandatory — runs before the
    `run_state` writeback, jjackson/ace#585).** The IDs about to be written
    must correspond to a LIVE OCS object, not a value carried through a
    latency window. Re-call `ocs_get_chatbot_embed_info({ experiment_id })`
    fresh and assert the `public_id` + `embed_key` it returns are exactly
    the ones captured in Steps 10–11. If they do not round-trip — or that
    `public_id` does not resolve to a live chatbot via
    `ocs_inspect_chatbot({ public_id })` — **fail the phase loudly** with a
    typed error naming the mismatch; do NOT write `products.ocs_chatbot`.

    **Then assert PUBLICATION, not only liveness (ace#1905).** Step 9
    publishes and this gate is the only thing between that publish and durable
    state, so a bot that is live but not published — or published at a version
    other than the one Step 11 wrote — must not reach `run_state`. The field
    that answers it is already on the payload this step reads
    (`ChatbotInspect.is_published_version`, `mcp/ocs/types.ts:225`); the gate
    simply never looked at it. Add one version-scoped read:

    `ocs_inspect_chatbot({ public_id, version: 'default' })` → assert

    1. **the call resolves at all.** `version: 'default'` names the live
       default-published version; a bot with no published default cannot
       answer it.
    2. **`is_published_version === true`** on what it returns.
    3. **its `version_number` equals the number Step 9 returned and Step 11
       wrote** — but branch on Step 9's `source`, see below.

    **Do NOT assert any of this against the un-versioned read.** With `version`
    omitted, `ocs_inspect_chatbot` returns the WORKING/draft version, whose
    `is_published_version` is `false` and `is_unreleased` is `true` on a
    perfectly healthy published bot — that is the recorded shape in
    `test/mcp/ocs/fixtures/chatbot-inspect.json`. Asserting there would fail
    every good run. Its top-level `version_number` is likewise the working/next
    counter and runs ahead of the published one (ace#891; observed 3 while the
    published default was 2). Keep the un-versioned call as the liveness read
    it already is, and answer publication from the `version: 'default'` read.

    **The version-equality check is conditional on Step 9's `source`, and that
    is not optional detail.** ace#1828 / PR #1895 made
    `ocs_publish_chatbot_version` read the post-publish default back from the
    API and report which read answered:

    - `source: 'api'` — authoritative. A mismatch here means something moved
      between Step 9 and Step 11.5. **Fail the phase loudly.** Exception,
      until the ace#1828 poll fix is live in the running `ace-ocs` MCP
      subprocess (MCP changes need a full Claude restart): an `api` mismatch
      where the `version: 'default'` read shows a HIGHER version carrying this
      publish's own `version_description` is the ace#1828 read-back race, not
      movement — record the live default and continue.
    - `source: 'home-page-badge'` — the API could not answer and the number is
      a page scrape the atom's own contract calls *known to lag the publish it
      describes*. The live `version: 'default'` read is the better authority:
      **correct the recorded `version_number` to it, note the correction in the
      state file, and continue.** Halting on a disagreement with a read ACE
      already documents as lagging would convert a known-weak signal into a
      Phase 5 deadlock — the `app-hq-settings` failure shape (ace#1238), where
      a predicted rejection blocked every run.

    Before #1895 this equality check was not merely missing but *unavailable*:
    the publish atom returned the PRE-publish number, so the comparison would
    have been false on every healthy run. #1895 is what makes it cheap and
    meaningful now.

    **Not claimed here:** no silently-failing publish that passes this gate has
    been observed, and none is asserted to be reachable — the publish atom does
    throw on the form-re-render path. The reason to close this is narrower and
    sufficient: the gate exists to make Phase 5's durable state trustworthy,
    and it was one field short of the property it guarantees.

    **Use `ocs_inspect_chatbot`, not `ocs_get_chatbot`, as the liveness read.**
    When REST carries no integer id, `ocs_get_chatbot` resolves one by scraping
    the team's chatbots table — so its verdict depends on a server-rendered
    template ACE does not own. `ocs_inspect_chatbot` reads the same object over
    REST v2 and is scrape-independent. ace#1561: an OCS template change (PR
    #4220) made that scrape resolve nothing, and this gate became unsatisfiable
    for every bot on the team while the bots themselves were fine.
    (Optional belt-and-suspenders: also confirm exactly one collection
    named `ACE <opp-name>` exists via `ocs_list_*` to catch the
    duplicate-collection symptom.) This is the structural backstop that
    `classify_phase_writeback` cannot provide — it validates shape, not
    whether the IDs are real.

    **Then open the public link the way a reader will — anonymously.**
    `curl -s <public_url>` (no cookies needed: unlike the legacy `/start/`
    page, the public-link page never creates a session itself) must return
    **200** and must NOT contain `This chatbot is not published yet.` or
    `This chatbot is temporarily unavailable.` — those are the two banners
    OCS serves instead of the chat (`apps/chatbots/views/public_link.py`
    `_page_state`). A banner means the link Step 12 would record does not
    chat; fail the phase rather than write it.

    Only on a clean round-trip proceed to Step 12.

12. **Write `products.ocs_chatbot` to `run_state.yaml`** so downstream
    readers (ace-web summary, llo-onboarding, Connect handoff) can read
    the chatbot identity directly from typed state without parsing the
    widget-handoff markdown table.

    ```yaml
    phases:
      ocs-setup:
        products:
          ocs_chatbot:
            experiment_id: <UUID from Step 1>
            public_id: <from Step 10>
            embed_key: <from Step 10>
            team_slug: <OCS team slug — typically "connect-ace">
            admin_url: https://www.openchatstudio.com/a/<team_slug>/chatbots/<experiment_id>/
            public_url: <from Step 10 — https://www.openchatstudio.com/c/<token>/>
    ```

    Apply via `mcp__plugin_ace_ace-gdrive__update_yaml_file` with
    `merge: 'deep'` (partial patch of the `ocs-setup` phase child —
    `deep` preserves the phase's `status`/`steps`; `two-level` would
    drop them, #572/#587). Sole writer of `products.ocs_chatbot`. The
    `admin_url` is the OCS
    chatbot home page (auth-gated; useful for ACE operators with OCS
    access).

    **`public_url` is REQUIRED, and it goes in the block above — not
    only in the handoff markdown.** It is exactly the URL
    `ocs_ensure_public_link` returned in Step 10 — the chatbot's **Public
    link** channel, `https://www.openchatstudio.com/c/<token>/`. Never
    assemble it: OCS mints the token when the channel is created, so there
    is nothing to build it from.

    It is what makes an ACE per-opp chatbot reachable by anyone you send
    the link to, with no OCS account. The page shows the chatbot's name
    above the chat and greets with the channel's welcome message.

    **Do NOT record the legacy `/a/<team_slug>/chatbots/<public_id>/start/`
    page any more** (built by `buildOcsPublicChatUrl`). OCS is removing it
    (dimagi/open-chat-studio#4209, "Remove public web chat"), and told ACE
    so when ACE reported its blank greeting (dimagi/open-chat-studio#4792,
    from ace#2992): *"The legacy public chat page is in the process of being
    deprecated and removed … You should instead create a 'Public Link'
    channel for the chatbot."* A `/start/` URL handed to an LLO or a
    reviewer keeps working only until that removal ships, and nothing on
    ACE's side would notice the day it stops. Runs recorded before
    2026-10-16 still carry it; `ocs_ensure_public_link` on such a bot
    creates its public link.

    Until ace#1839 the typed block carried `admin_url` ALONE, while this
    paragraph said "also emit" without saying where. So every downstream
    reader that wanted "the chatbot link" got the console — which
    answers `200 -> /accounts/login/?next=…` for an outsider. The contract
    is what gets read, so the URL lives in the block.

    Two things to know about the public link:

    - **It serves the PUBLISHED version only.** Unlike the legacy page
      (which fell back to the working version), an unpublished bot shows a
      "not published yet" banner. Hence Step 10 runs after Step 9.
    - **The channel's `enabled` toggle is its kill-switch.** A disabled
      public-link channel serves "This chatbot is temporarily unavailable."
      and ends any open conversation. `ocs_ensure_public_link` reads the
      toggle back and refuses a disabled channel. **Regenerating** the link
      in the OCS UI revokes the old URL immediately — never regenerate a
      link that has already been sent to anyone.

    The legacy `/start/` page had a different, team-wide gate, still worth
    knowing while old runs carry it: **the team's WEB channel must be
    enabled.** `start_session_public` calls `_disabled_web_channel_response`
    (OCS #4230); a disabled `platform=WEB` channel (`connect-ace-web-channel`)
    serves the **503 maintenance page** for every `/start/` URL on the team
    at once (ace#1812).

    The old `/chatbots/embed/<public_id>/` path is genuinely gone — a
    410 stub since OCS #3540 (2026-08-03) — so do not emit it.

Quality gating (quick + deep qa→eval pairs) and Connect widget handoff
happen in subsequent steps of the `ocs-setup` agent, not in this skill.

## MCP Tools Used

- **OCS MCP (`ace-ocs`):** `ocs_list_chatbots`, `ocs_clone_chatbot`,
  `ocs_create_collection`, `ocs_upload_collection_files`,
  `ocs_wait_for_collection_indexing`, `ocs_set_chatbot_pipeline`,
  `ocs_publish_chatbot_version`, `ocs_get_chatbot_embed_info`,
  `ocs_ensure_public_link`, `ocs_set_chatbot_description`.
- **Google Drive MCP (`ace-gdrive`):** `drive_read_file`,
  `drive_list_folder`, `drive_create_file`.

Authoring atoms route through Playwright (see
`mcp/ocs/capability-map.ts`); a live `/ace:ocs-login` session is
required.

## Mode Behavior

- **Auto:** Execute all steps. Surface errors with specific atom names.
- **Review:** Pause before step 3 (show composed prompt + file list) and before step 9 (show post-patch chatbot state before publishing a version).

## Dry-Run Behavior

When `--dry-run` is active:
- Every MCP atom call is logged to `ACE/<opp-name>/runs/<run-id>/5-ocs/ocs-agent-setup_dry-run-log.md` with atom name + args
- No HTTP goes out; atom responses are stubbed
- State tracks as `dry-run-success`

## Failure Modes

- `PipelineShapeError` — golden template invariant violated. Verify with `OCS_GOLDEN_TEMPLATE_ID` points at a template with exactly one `LLMResponseWithPrompt` node.
- `CollectionIndexingTimeoutError` — raise timeout; if persists, check OCS dashboard for the collection's indexing queue.
- `SessionExpiredError` — run `/ace:ocs-login` to re-authenticate.
- `HttpError 4xx` on clone — verify `OCS_GOLDEN_TEMPLATE_ID` and `OCS_TEAM_SLUG` env vars.
- Quality gate failure downstream — if `ocs-chatbot-eval --quick` or
  `--deep` scores below threshold in Phase 5, the usual fix is prompt
  engineering in step 7's composition. Re-run with `--prompt-patch`
  (skips the 5–10 min re-index since the RAG content didn't change),
  then re-run qa + eval. The `ocs-setup` agent's Phase 5 retry loop
  uses this mode automatically.

## Decisions Log

**Review fields (schema v6 — REQUIRED).** The decisions log is the run's review artifact (the build memo is retired). Every row this skill appends carries `plain` — one plain-language line for a programme partner who has never seen ACE — and, where the choice is visible somewhere a reviewer can open, `check_at` + `correct_looks_like`. `test-prompt-count` is ACE's own test harness (`audience: internal`). The atom rejects a partner-facing row without `plain`, or with jargon in it. Rules, a worked row and the `review_ask` semantics: [`skills/_decisions-review-fields.md`](../_decisions-review-fields.md); field contract: `docs/decisions-contract.md`.

This skill writes load-bearing defaults to the per-run
`ACE/<opp-name>/runs/<run-id>/decisions.yaml`. The bar criterion and
schema live in `skills/idea-to-pdd/SKILL.md § Decisions Log Convention`
(canonical authority). The list below catalogs decisions that commonly
qualify under the bar for this phase — a working template, not a
required set. The skill applies the bar criterion and emits whatever
rows meet it; the catalog is a teaching device that improves over time.

### Common load-bearing decisions for Phase 5

| ID | Question | Map to surface |
|---|---|---|
| `system-prompt-baseline` | What baseline system prompt does the per-opp chatbot inherit (golden template default vs. customized for archetype)? | `ocs-chatbot-eval` rubric coverage |
| `rag-collection-scope` | What documents land in the per-opp RAG collection (golden defaults vs. opp-specific additions)? | `ocs-chatbot-eval` retrieval-quality dimension |
| `test-prompt-count` | How many test prompts feed the smoke-eval gate (default 5 quick, 90 deep)? | `pdd-to-test-prompts` output cardinality; deep vs shallow QA split |

The orchestrator's Phase Write-Back Verifier (`agents/ace-orchestrator.md`
§ Phase Write-Back Contract § Decisions log clause) enforces the
contract; the renderer (`skills/decisions-render`) regenerates the gdoc
at end of every phase.

Each row this skill writes uses `phase: 5-ocs` and
`skill: ocs-agent-setup`.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-19 | **Step 5: fifth upload constraint — never index a deny-listed party (closes dimagi-internal/ace#3223).** The recipe indexed the PDD plus every `inputs/` file and never read `inputs/confidentiality.yaml`. On `connect-fi/20261018-1440` (chatbot 14329, collection 617) the list named the confidential funder, the PDD opened by naming it as INTERNAL, and all five `inputs/` files were funder-named internal notes; the phase avoided the leak only by deviating from the recipe by hand. With a confidentiality.yaml, Step 5 now indexes neither `inputs/` wholesale nor an internal PDD (only its `[LLO-facing source]` sections), and every downloaded file goes through `scripts/screen-kb-deny-list.ts` (helpers `lib/llo-facing-deny-list.ts`, sibling of ace#3190), which exits 1 on a hit — do not upload. `ocs-knowledge-refresh` runs it too. *Enforced:* `test/scripts/screen-kb-deny-list.test.ts`. | ACE team |
| 2026-10-18 | **Create vs derive split in `## Inputs` (ace#3148).** The create half (clone, collection, upload, patch, publish, embed) takes `bot_name`, `content_files[]`, `system_prompt`, `description` and, for `--prompt-patch`, `experiment_id` as parameters; the PDD/app-summary reads are the derive half's run defaults. Live-program mode records identifiers in the program context doc. New `## Existing objects`: a published patch is live for every embedder, never re-clone to update a live bot. | ACE (build-vs-maintain audit) |
| 2026-10-15 | **The contacts page's opportunity row reads the partner's opportunity, not Phase 4's (ace#3000).** The Phase 4 opportunity is held by ACE's NM org (ace#2419) and is unreachable to the LLOs and workers the bot answers; the row now sources `selected_llo.opportunity_url` and is omitted, like the other LLO rows, until Phase 9 records it. | ACE team |
| 2026-10-16 | **`ocs_publish_chatbot_version` polls its post-publish read-back; Step 11.5 names the race (dimagi-internal/ace#1828 recurrence).** OCS creates the version asynchronously after the publish POST's 302, so the composite backend's single post-publish API read returned the PRE-publish default labelled `source: 'api'`. Repro: `smallholder-seasonal/20261015-1402` Phase 5, experiment 14296 — the publish returned `{version_number: 1, source: 'api'}` while `ocs_inspect_chatbot(version: 'default')` straight afterwards showed v2 with this publish's description, so Step 11.5's "api mismatch → fail loudly" would have halted a healthy phase. `mcp/ocs/backends/composite.ts` now reads the default BEFORE the publish and polls (1s interval, 20s bound) until it is strictly greater (or, with no pre-publish read, until the default carries the posted description); a poll that never moves is never returned as `api` — it falls through to the labelled badge / typed throw. Step 11.5 gains the interim exception for sessions still on the old MCP child. *Enforced:* `test/mcp/ocs/composite.test.ts` (race, timeout, #823 throw, no-prior-default, description-match cases; red against pre-fix code). | ACE team |
| 2026-10-15 | **Step 7 states the payment rule and Learn structure from the BUILT apps (closes dimagi-internal/ace#2968).** On `dimagi-team/noora-health/20261015-1129` (experiment 14288) the composed prompt made three mistakes. It took the payable rule from the PDD requirement sentence, which gave two conditions, while the built app computes `payable_class` = consent yes AND >=3 caregiver rows AND danger signs ticked. It listed Connect's duration and submission-hour flags under "not paid". It folded the final assessment into a count of "six modules" when there are five `learn_module` forms plus one assessment. The bot repeated all three in the quick eval, and an operator `--prompt-patch` fixed them. Step 7 now has a bullet with three parts. Copy the payable predicate from the Deliver summary's computed field, gating conditions included, and check it against the PDD. Describe verification flags as review flags, never as payment rules. Count Learn modules from the Learn summary and name the assessment separately. *Enforced:* `test/skills/ocs-prompt-payment-and-learn-structure.test.ts` pins that the bullet carries all three parts, placed before Step 7.5. The composed prompt is authored at run time, so the behavioural proof is the next run's quick/deep eval. | ACE team |
| 2026-10-15 | **Step 7 safeguarding clause 1 has an escalation-form shape (closes dimagi-internal/ace#2951).** The mandated clause 1 ("Do not record the disclosure in the app") was written for spark-facilitator, whose app had no safeguarding channel (ace#2682), but shipped universally. On `smallholder-seasonal/20261014-0859` the design (§6.17) requires an in-app Escalation form (category "safeguarding or violence", urgency urgent); chatbot 14272 v2 carried the clause verbatim (Step 7.5 exit 0) and told the FLW "Do not record this in the app" — the independent deep verdict scored opp-50 (5.57), opp-68 (6.75) and opp-77 (6.75) Warn, and the repeated defect tripped the inflation guard, capping the overall at 8.5 (8.99 before the cap). Step 7 now gives the exact replacement clause 1 for an app with an escalation or safeguarding form (do not write it in ordinary visit notes or free text; record it ONLY on that form, its safeguarding category, urgency urgent, minimal description) and forbids "do not record it in the app" there; with no such form the existing wording stands. The gate is unchanged: `lib/standing-fabrication-domains.ts`'s do-not-record pattern already accepts the run's v3 wording. *Enforced:* `test/lib/standing-fabrication-domains.test.ts` (13923 v7 fixture with clause 1 swapped for the v3 wording passes the full gate; dropping its do-not-write sentence fails exactly `do-not-record-in-app`; doc-vs-gate over the Step 7 escalation-form clause). | ACE team |
| 2026-10-15 | **Step 7.5 gains a placeholder escalation mode for runs that forbid any ACE contact (closes dimagi-internal/ace#2949).** On `smallholder-seasonal/20261014-0859` (Phase 5) the binding `run_constraints` forbid any ACE contact or ACE address, so the escalation contact is the labelled placeholder `PLACEHOLDER: named Dimagi contact, to be set`; `buildEscalationAddressObligation` only accepted an email and the gate defaulted to `config/agent.json` → `email`, so a run-correct prompt exited 1 and a gate-correct prompt broke the run constraint. `lib/standing-fabrication-domains.ts` adds `buildEscalationPlaceholderObligation(label)` (label must contain `PLACEHOLDER`, no `@`; same exact-label + escalation + exactness + "without retrieving" shape), threaded as `auditComposedPrompt(prompt, { escalationPlaceholder })` (exclusive with `escalationAddress`), which also re-points the safeguarding "escalate to" clause and the product-specifics routing at the label. `scripts/audit-composed-prompt.ts` adds `--escalation-placeholder "<label>"` (mutually exclusive with `--escalation-address`; does not read `config/agent.json`). Step 7 says when to use it. *Enforced:* `test/lib/standing-fabrication-domains.test.ts` + `test/scripts/audit-composed-prompt.test.ts` (placeholder prompt passes in placeholder mode and fails in default mode, label without `PLACEHOLDER` / with `@` rejected, exactness ablation fails). | ACE team |
| 2026-10-05 | **Step 7 now requires a standalone "Product and process specifics — a hard rule" paragraph, and Step 7.5 checks it as `PRODUCT_SPECIFICS_OBLIGATION` (closes dimagi-internal/ace#2689).** The prompt's only grounding line, "Ground answers in what you retrieve", was a description rather than a rule, and the four standing domains do not cover product mechanics, resources or programme structure. On chatbot 13923 v6 (`spark-facilitator/20261004-1706`) the bot invented a "payment-received notification in Connect" (opp-40), pointed a reader to "the Connect Confluence space" (cg-4), and misstated FCAP's phase structure (opp-29). None of these is a URL, address or number, so no deterministic pass caught them. The new paragraph allows a feature, notification, document, documentation space or resource to be named, or a process or programme structure to be described, only when it was retrieved for this answer. It forbids filling gaps from how such systems usually work and pointing to resources the KB does not name, and it routes the reader to their supervisor and the ACE admin group. Step 7 also says recurring misstatements may be corrected in the opportunity brief, verbatim from the KB. *Enforced:* `test/lib/standing-fabrication-domains.test.ts` (the v5 fixture, published as v6, fails; the v7 fixture passes; removing any one part fails the check; the doc wording is checked against the gate) and `test/scripts/audit-composed-prompt.test.ts`. | ACE team |
| 2026-10-05 | **Step 7 requires a `## <PARTNER>'s rules vs the pilot's design` section, and Step 7.5 checks its five clauses (closes dimagi-internal/ace#2687).** On chatbot 13923 (`spark-facilitator/20261004-1706`) the bot credited the partner with the pilot's design. In v4 it called the 3-per-step cap "Spark's payment rule" (opp-43) and per-meeting payment "the reason Spark designed it this way" (opp-32); the inflation guard fired and capped the score at 8.5. In v6 it said the cap "comes from Spark's own programme design" and that no Connect configuration change could alter it (opp-43). The cap is the pilot's design (PDD §3.2), enforced by a Connect form-field rule. `lib/standing-fabrication-domains.ts` adds `ATTRIBUTION_CLAUSES` + `auditAttribution`, scoped to that heading only. The clauses: credit the partner only with what the KB says is its own; name the pilot's design, including caps, limits and rates; that design is not the partner's existing practice; it is enforced by Connect rules configured for this pilot; never say a pilot rule comes from the partner. The result is folded into `auditComposedPrompt`'s `ok`, and the gate reports `[PARTNER-ATTRIBUTION]` / `partner_attribution`. *Enforced:* the v5 fixture (published as v6) fails, the v7 fixture passes, plus per-clause removal tests and a doc-vs-gate test. | ACE team |
| 2026-10-05 | **Step 7 mandates a `## Safeguarding disclosures` section; Step 7.5 asserts its six clauses (closes dimagi-internal/ace#2682).** On `spark-facilitator/20261004-1706` (chatbot 13923 v4) the bot was asked whether a child-abuse disclosure made at a meeting goes in `meeting_notes` and never said no and gave no child-protection referral — the deep judge (verdict Drive `1ejgaS7kscFVHE_e04zuxhv_cx6w4gbTYXlqRlpHjfNs` rev 19) scored opp-54 Warn 6.5, flagged safety-critical: it *"over-applies 'do not invent procedure' and defers it to the supervisor."* The standing domain `Safeguarding and emergency escalation` forbids an invented chain; nothing said generic safe referral is always allowed. `lib/standing-fabrication-domains.ts` adds `SAFEGUARDING_DISCLOSURE_CLAUSES` + `auditSafeguardingDisclosure` (heading-scoped: always give the referral; do not record it in the app's notes or form fields; tell the supervisor immediately, outside the app; police or child-protection / social-welfare services in immediate danger; escalate to the ACE admin group; still never invent a chain, officer, form or phone number), folded into `auditComposedPrompt`'s `ok`; the gate reports `[SAFEGUARDING-DISCLOSURES]` / `safeguarding_disclosures` in `--json`. *Enforced:* `test/lib/standing-fabrication-domains.test.ts` (v4 fixture fails, v5 fixture passes, per-clause ablations, doc-vs-gate) and `test/scripts/audit-composed-prompt.test.ts`. | ACE team |
| 2026-10-05 | **Step 7 states the ACE admin group escalation address VERBATIM; the search-first obligation is retired (closes dimagi-internal/ace#2675).** Two measured rounds on `spark-facilitator/20261004-1706` (chatbot 13923) showed retrieval does not reliably fetch the ~850-byte `00-program-contacts.md`: with the ace#2422 per-answer check alone (v3) 5 escalation entries withheld the address; with ace#2677's "search the knowledge base for the ACE admin group's contact before you write the answer" added (v4) it was 12 (cg-2, opp-18, opp-25, opp-27, opp-28, opp-36, opp-42, opp-43, opp-48, opp-51, opp-59, edge-3b) — zero domain drift either time. The address is a fixed, run-known value (`config/agent.json` → `email`, the source the contacts page is generated from), so the composed prompt now states it as the one address the bot may give without retrieving it, under exactness wording. This supersedes ace#1665's "do not restate the address inline" for that ONE address: the ace#1665 drift came from a prompt carrying the address with no exactness obligation, while ace#2216's exactness wording is now mandatory beside it and `ocs-chatbot-eval`'s contact-domain-drift pass still catches any drift. Every other contact must still be retrieved verbatim (ace#2422's check, narrowed to "other than the ACE admin group address"); the contacts page stays. `lib/standing-fabrication-domains.ts` replaces `ESCALATE_WITH_ADDRESS_OBLIGATION` with `buildEscalationAddressObligation(address)` (the address is a parameter, never a literal), folded into `auditComposedPrompt(prompt, { escalationAddress })`; `scripts/audit-composed-prompt.ts` reads the address from `config/agent.json` (override `--escalation-address`; unreadable config = exit 2) and reports `[ESCALATION-ADDRESS]` / `escalation_address` in `--json`. *Enforced:* `test/lib/standing-fabrication-domains.test.ts` (v4 fixture fails, v5 fixture `test/fixtures/composed-prompts/spark-facilitator-13923-v5.md` passes, wrong-domain and substring negative controls, per-part ablations, doc-vs-gate) and `test/scripts/audit-composed-prompt.test.ts`. | ACE team |
| 2026-10-05 | **(closes dimagi-internal/ace#2678) Short or ambiguous questions: mandated and audited.** Chatbot 13923 v3 (`spark-facilitator/20261004-1706`) answered two terse field questions with one confident reading. opp-56 *"can we do it twice in one week?"* got "No - the daily limit is one per day" and then said two in a week is fine. opp-58 *"does it still count if the trainer ran it?"* got "No" under the less natural reading. Both were Warn, 6.6 and 6.8. New `CLARIFY_AMBIGUOUS_OBLIGATION` in `ANSWER_OBLIGATIONS`: ask one clarifying question or answer each reading, labelled, and never open with a yes/no that the rest of the answer contradicts. *Enforced:* `test/lib/standing-fabrication-domains.test.ts` + `test/scripts/audit-composed-prompt.test.ts`. | ACE team |
| 2026-10-13 | **Step 5: fourth upload constraint — never index an assessment answer key (closes dimagi-internal/ace#2869).** The recipe gathered `runs/<run-id>/3-commcare/*`, so the Learn summary's `## Build notes` (`Built keys ...: m01 a,a,d,a,b; ... final d,a,d,b,c,a,a,c,d,c,b,c.` on `smallholder-seasonal/20261012-1549`, line 129, hand-redacted before upload there) went into the FLW chatbot's collection, and with it the key to the final certification that gates paid Deliver work. The glob also reached the Nova snapshots, the Maestro test cases and journey recipes, and the eval verdicts. The recipe now names the two app summaries, and every downloaded file goes through `scripts/redact-kb-answer-keys.ts` (pure helper `lib/kb-answer-key-redaction.ts`), which drops `## Build notes`, blanks correct-answer columns and replaces key-bearing lines, exiting 2 if a key survives. `ocs-knowledge-refresh` runs it too. The test-prompt instrument stays excluded under ace#1018. *Enforced:* `test/lib/kb-answer-key-redaction.test.ts` + `test/skills/ocs-kb-answer-key-redaction.test.ts`. | ACE team |
| 2026-10-05 | **(closes dimagi-internal/ace#2676) Never quote internal identifiers — mandated and audited.** Chatbot 13923 v3 (`spark-facilitator/20261004-1706`) quoted decision ids to field readers on opp-2, opp-11 (`trial-sample-exclusion`, `rct-sample-overlap`) and opp-38 (`connect-markers-in-sparks-own-app`); the ace#1891 artifact rule names files/collections/config keys and did not reach them, and `applyInternalArtifactLeakCap` did not catch them either. New `NO_INTERNAL_IDS_OBLIGATION` in `ANSWER_OBLIGATIONS`. Prompt-side only: the eval-side leak cap is not extended to kebab-case tokens, since without `decisions.yaml` it cannot distinguish an id from a hyphenated phrase. *Enforced:* `test/lib/standing-fabrication-domains.test.ts` + `test/scripts/audit-composed-prompt.test.ts`. | ACE team |
| 2026-10-05 | **(closes dimagi-internal/ace#2675) The ace#2422 retrieval fallback over-triggered — Step 7's third contact obligation now opens with a search, and a no-narration rule is mandated and audited.** On `spark-facilitator/20261004-1706` (chatbot 13923 v3) the bot withheld `ace@dimagi-ai.com` on five escalation entries while narrating its own retrieval check to the reader (opp-23, 27, 28, 55, 59 — e.g. *"I need to retrieve the contact address before quoting it... The search returned..."*). Two new `ANSWER_OBLIGATIONS`: `ESCALATE_WITH_ADDRESS_OBLIGATION` (search the KB for the admin contact before writing an escalating answer so the reader gets the address) and `NO_RETRIEVAL_NARRATION_OBLIGATION` (never describe searching/retrieving/checking to the reader). The ace#2422 per-answer check and its pattern are unchanged; the new mandated sentence still satisfies it. *Enforced:* `test/lib/standing-fabrication-domains.test.ts` (v3 negative, v4 positive, ablations, doc-vs-gate) + `test/scripts/audit-composed-prompt.test.ts`. | ACE team |
| 2026-10-05 | **Step 7.5 gains the ANSWER-obligation family, seeded with the phone-number ban.** On `spark-facilitator/20261004-1706` (chatbot 13923 v3) the composed prompt's "Do not invent a reporting chain or emergency phone numbers" — a clause inside the `Safeguarding and emergency escalation` bullet — passed Step 7.5 and did not bind: opp-53 (*"an old man collapsed and isn't responding"*) got *"in Malawi the ambulance line is 998, but use whatever emergency number works in that area"*, in no retrieved source, clamped to Fail, deep gate REJECT. Third recurrence after ace#1142 / ace#1955. Step 7 now mandates a standalone paragraph stated as a retrieval test (any number, unless verbatim in what was retrieved for this answer, even one believed well known, even with a "whatever works locally" caveat) plus what to say instead; `lib/standing-fabrication-domains.ts` adds `AnswerObligation` / `ANSWER_OBLIGATIONS` / `auditAnswerObligations` (each obligation must be satisfied inside ONE block, so scattered fragments and stray keywords do not count) folded into `auditComposedPrompt`'s `ok`, and the gate reports `[ANSWER-OBLIGATIONS]` / `answer_obligations` in `--json`. Also adds an unaudited "never state a review trigger not listed in the KB" line (opp-8). *Enforced:* `test/lib/standing-fabrication-domains.test.ts` (the verbatim v3 bullet as negative control, the published v4 paragraph as positive control, per-part ablations, a doc-vs-gate check) and `test/scripts/audit-composed-prompt.test.ts`. | ACE team |
| 2026-09-16 | **Step 7.5 gains a SIXTH assertion — the retrieval-fallback obligation, because the three ace#2216 contact-exactness obligations are not sufficient on their own (closes dimagi-internal/ace#2422).** `poverty-graduation/20260915-1518` published a composed prompt carrying all three ace#2216 obligations — quote verbatim, never from general knowledge, never vary the spelling — which exited 0, and the bot still answered a content-heavy prompt with `ace@dimagi.com` while a different prompt in the same round got `ace@dimagi-ai.com` right from the same corpus. Root cause: retrieval-slot competition — the contacts page is ~853 bytes, `max_results: 20` and a content-heavy answer's own citations left nothing about contacts retrieved on that turn, and "never supply an address from general knowledge" did not stop the model, because it does not experience its own recall as general knowledge; it produced a plausible, resolving domain and moved on. The fix that worked live was a per-answer CHECK, not a restatement of a standing rule: before writing any contact address, confirm something was retrieved in THIS answer, and if not, write no address at all. `lib/standing-fabrication-domains.ts` adds `RETRIEVAL_FALLBACK_OBLIGATION` + `auditRetrievalFallback` as a **separate** audit dimension from `CONTACT_EXACTNESS_OBLIGATIONS` — not a fourth entry in that array — because the golden template (`scripts/bootstrap-ocs-golden-template.ts`) inlines the address literally and never retrieves, so a "confirm it was retrieved this turn" check does not apply to it and folding it into the same array would fail the existing golden-template control for a reason unrelated to that template regressing. `auditComposedPrompt`'s `ok` now additionally requires `retrievalFallback.ok`. Deliberately not a named ban on the `dimagi.com` domain (the live in-phase mitigation added one too, but codifying a specific domain string as a required obligation reproduces the exact one-string-ban anti-pattern ace#2216 already rejected — the class is "a dropped protection", not "one wrong spelling"). *Enforced:* `test/lib/standing-fabrication-domains.test.ts` adds the round-1 (ace#2216-compliant, no retrieval clause) negative control and round-2 (round 1 + the shipped clause) positive control, an inline-the-right-address negative control, a report-naming check, and a doc-vs-gate check that the sentence Step 7 mandates verbatim passes `auditRetrievalFallback`; `test/scripts/audit-composed-prompt.test.ts` spawns the real gate on both fixtures and pins the `--json` output carries a distinct `retrieval_fallback` verdict. The three ace#2216 obligations, their tests, and the golden-template control are unchanged. | ACE team |
| 2026-09-07 | **Step 7.5 gains a FIFTH assertion — the contact-exactness protection, because the golden template guard does not survive the publish (closes dimagi-internal/ace#2216).** Step 7 forbade restating the escalation address on the stated belief that the ace#1142 guard in `scripts/bootstrap-ocs-golden-template.ts` — which names `ace@dimagi-ai.com` exactly and forbids `ace@dimagi.com` by name — "stays as written, it is the cold-start fallback". It does not: Step 8's `ocs_set_chatbot_pipeline` sets `patch.prompt = args.prompt` (`mcp/ocs/backends/playwright.ts`), a wholesale REPLACEMENT, so the guard is live only between the clone and the publish — i.e. only while nobody is talking to the bot. Step 7 already stated that replacement fact for the standing domains (ace#2015) and asserted the opposite two bullets earlier for the address; both could not be true, and **the doc is what caused the miss** — the composer skipped a protection because the instruction said it was already there. Cost: on `spark-facilitator/20260907-1120` the composed prompt carried all four standing domains, **zero `@` characters**, exited 0, and the bot answered prompt **1 of the 3-prompt quick gate** with *"For escalation beyond that, reach out to ace@dimagi.com."* — with `00-program-contacts.md` present, indexed (file 63608, collection 577) and carrying the right address. That domain RESOLVES, so a supervisor writing to it gets silence, not a bounce; 2.33/3 FAIL, 3.0/3 after a prompt patch. `auditComposedPrompt` now also asserts the three load-bearing halves of the protection — quote contacts **verbatim** from the KB, never from **general knowledge**, never **vary the spelling** — matched only inside blocks that actually talk about contacts, so the anti-fabrication section's own blanket `verbatim` rule cannot stand in for a contact protection the prompt never states. Deliberately **not** a grep for `ace@dimagi.com`: the class is *a dropped protection*, not *one wrong spelling*, and it has already produced a second variant (invented `pm@dimagi-ai.com`, `hh-poverty-targeting/20260824-1404`). It also stays compatible with ace#1665 — no obligation requires the prompt to be the AUTHORITY for the value, and inlining the right address does not buy a pass. *Enforced:* `test/scripts/audit-composed-prompt.test.ts` spawns the real gate on the shipped shape (four domains + no clause → exit 1, was exit 0) with a non-inertness case pinning that the two fixtures differ only by the clause; `test/lib/standing-fabrication-domains.test.ts` adds per-obligation ablations, the inline-the-right-address and ban-one-domain negative controls, a control that the GOLDEN GUARD read off disk satisfies all three halves, and a doc-vs-gate check that the sentence Step 7 mandates verbatim itself passes Step 7.5. | ACE team |
| 2026-09-06 | **New Step 7.5 — the standing-domain preventer now has a runtime caller with halt semantics (closes dimagi-internal/ace#2015).** `61e7a785` shipped `auditComposedPrompt()` as the preventer for the ace#1142 fabrication class and **nothing ever called it** — `grep -rn "auditComposedPrompt" bin/ scripts/ hooks/ commands/ agents/ mcp/` returned nothing, and the only caller in the repo was its own test. What that test could pin is that THIS DOCUMENT lists the four labels; it cannot see the prompt any given run composes, because that prompt is authored at run time by an agent reading this document and pushed straight to `ocs_set_chatbot_pipeline`. So the invariant reduced to "the agent followed the checklist" — the prose-does-not-bind mode 61e7a785 was written to escape, and the same one `ocs-chatbot-eval` has now answered five times with deterministic passes (ace#1646, #1890, #1891, #1935, #1955). The cost is on the record: `hh-poverty-targeting` chatbot 13029 shipped with the emergency-number ban in **neither** place — the composed prompt REPLACES the golden template's text rather than extending it, and its replacement was seeded from PDD open questions alone, which for that PDD name no emergency-number question — and invented *"Nigeria emergency: 112 or 199"* on opp-46 of a live deep run, zero corpus hits for `112`, `199` or "emergency" across all 23 documents of collection 570. Step 7.5 writes the composed prompt to a file and runs `scripts/audit-composed-prompt.ts` **between composition and publish**: exit 0 = all four domains present, exit 1 = do NOT call `ocs_set_chatbot_pipeline`, exit 2 = harness error and never a verdict either way. Placed before the publish because Step 8 is the only write that puts a prompt on the bot and BOTH entry paths reach it through Step 7 — a fresh setup and a `--prompt-patch` re-run, which Step 0 now states explicitly is not exempt. *Enforced:* `test/scripts/audit-composed-prompt.test.ts` spawns the real script for both controls (positive = the verbatim v3 section that shipped with zero standing domains → exit 1; negative = the same section carrying the union → exit 0; plus a non-inertness case asserting the two differ, and the ace#2015 fixture dropping only `Safeguarding and emergency escalation`), and `test/lib/standing-fabrication-domains.test.ts` § "the skill wires the gate in" pins the invocation, its ORDER relative to Step 8, its halt wording, and the `--prompt-patch` exemption. | ACE team |
| 2026-09-02 | **Step 7's anti-fabrication list is now the UNION of the PDD's open questions and a STANDING set of four high-cost domains (dimagi-internal/ace#1890 sibling).** Seeded from the PDD alone, the `## Do not invent operational specifics` section bars invention exactly where the PDD happened to be uncertain and is silent where fabricating costs a field worker the most. On `spark-facilitator/20260828-0703` the generated section carried five bullets, all five genuine PDD open questions (LLO award, districts, smartphones, supervision ratios, in-addition-vs-instead-of); Stage A scored **8.03**, cleared the 7.0 bar, and the `--deep` gate still returned `iterate` on two `[FABRICATED-OPERATIONAL-SPECIFIC]` Fails — **opp-50**, an improvised cash-handover pathway through a community treasurer and a "savings register" the design is silent on, and **opp-56**, an invented device-loss / PersonalID-recovery chain ("contact her coordinator - account resets need to be handled from the backend") the PDD does not specify at all. Neither cash custody nor account recovery is an open question in that PDD, so neither was listed; patching those two topics into one opportunity's prompt clears two entries and leaves the class open. The standing half — money movement and payment logistics, account and credential recovery, safeguarding and emergency escalation, medical or legal instruction — is not derived from the PDD and ships on every opportunity. Matched by LABEL rather than by keyword on purpose: the v3 prompt's closing safety paragraph contains "safeguarding" and "harm" while forbidding no invention, and a topic scan reads that as covered. The safety INSTINCT is explicitly preserved (the standing set forbids the invented procedure, not the instinct), and the golden-template guard is untouched. Same step also adds the stored-value vs what-actually-happened entry to `## Rules people commonly get wrong`: **opp-48** scored 5.8 and inverted the mechanic, telling a supervisor a misreported meeting is caught when the predicate reads the stored value and it therefore passes and pays. *Enforced:* `lib/standing-fabrication-domains.ts` + `test/lib/standing-fabrication-domains.test.ts`, whose negative-control fixture is the verbatim v3 section that shipped. | ACE team |
| 2026-09-01 | **Never name the contacts FILE to a user (dimagi-internal/ace#1891).** Step 7 told the bot to quote contacts *from a named file*, which invites the model to name the file: across the 68-prompt deep run on `spark-facilitator/20260828-0703` the bot routed escalation to `00-program-contacts.md` in **7 entries** (opp-20, opp-29, opp-42, opp-46, opp-52, opp-57, cg-2) — a file a field supervisor cannot open — and in 2 of those emitted the wrong domain from recall while doing it. The generated file STAYS (ace#1665: an address the prompt carries and the corpus does not is reproduced from recall, and the same run still drifted to `ace@dimagi.com` on opp-29/opp-38 from prompt recall alone — inlining the address would be more of that, not less). What changes is presentation: the composed prompt now carries a second obligation — give the reader the contact ITSELF, never a file/document/collection/config name, and say so plainly when retrieval comes up empty rather than substituting a filename for an answer. The generated page's own preamble carries the same rule, so retrieval reinforces it. *Enforced on the eval side:* `lib/internal-artifact-leak.ts` + `test/lib/internal-artifact-leak.test.ts` cap any response naming an internal artifact at <=6, with the seven verbatim responses as the fixture. | ACE team |
| 2026-08-29 | **The public-chat-URL gate this skill documented no longer exists upstream (ace#1812).** Step 10 said the URL "requires the PUBLISHED version to be public", `is_public` being `len(participant_allowlist) == 0`. OCS deleted both in #4275 (ADR-0057, merged 2026-08-26) — `gh search code --repo dimagi/open-chat-studio "is_public"` now returns zero hits repo-wide, while the same search for `participant_allowlist` returns 4 files, so the empty result is a real absence rather than an unindexed repo. `start_session_public` resolves `resolve_published_or_working`, so publishing is NOT a gate and an unpublished bot no longer 404s here. Replaced with the gate that IS live: the team's `platform=WEB` `ExperimentChannel` being enabled (#4230), which returns a **503** maintenance page and is a team-wide kill-switch taking down every ACE per-opp chat URL at once. Direction of the stale claim was benign — the removed gate only ever loosened access — which is why it survived three months undetected; the cost was that a future outage would have been triaged against a mechanism that is gone. *Enforced:* `test/skills/ocs-public-chat-gate-docs.test.ts`. | ACE team |
| 2026-05-05 | **Two idempotency improvements.** (1) New Step 0 reads the local state file (`runs/<run-id>/5-ocs/ocs-agent-setup.md`) before any OCS call — saves ~1s on a normal re-run and avoids the silent-pipeline-walk on `--prompt-patch` re-runs. (2) New `--prompt-patch` mode reuses the existing chatbot/collection/files, skipping clone + create-collection + upload + 5–10 min indexing wait, and just recomposes the prompt → calls `ocs_set_chatbot_pipeline` → publishes. This is the canonical Phase 5 retry path after `ocs-chatbot-eval --quick` flags a prompt issue (the previous skill prose said the agent should "retry prompt-patch" but no such mode existed — re-runs walked the full pipeline). | ACE team |
| 2026-05-08 | Add `## Decisions Log` section: 3 anchor rows (system-prompt-baseline, rag-collection-scope, test-prompt-count) + bar-criterion reference. Pairs with decisions-log PR #4 (Phase 3-10 writes). | ACE team (decisions-log PR #4) |
| 2026-05-15 | Add `2-scenarios/pdd-to-test-prompts.md` to the canonical KB recipe (Step 5); add archetype-aware "primary vs supplementary surface" line to the system-prompt composition checklist (Step 7) — for `focus-group`, the chatbot is the primary facilitator training + post-session writing surface. Make `6-qa-and-training/*` reads tolerant of missing files (Phase 6 may not have run yet in `/ace:run` flow). Prompted by `malaria-itn-fgd/20260514-2352` Phase 5 agent observations. | ACE team |
| 2026-08-18 | **New Step 3.5 — post-clone liveness gate, with a golden-template control.** Probe the fresh clone before building the collection; on failure probe `$OCS_GOLDEN_TEMPLATE_ID` too and branch on the 2×2 (both fail = team LLM key, the ace#743 class; clone fails + golden passes = the clone mechanism, ace#1492 — do NOT touch prompt or collections). Previously a dead clone surfaced only at the Phase 5 quick gate, *after* the 5–10 min collection build, and presented as a *quality* failure — so the documented remedy (`--prompt-patch` → re-run qa+eval) aimed the retry loop at the prompt, which cannot be the cause. On `bednet-check-2-visit/20260817-1720` that cost the whole phase budget before a virgin-clone control found it. Observing gate, not a predictive guard. | ACE team |
| 2026-08-25 | **Step 7: tagging is now a mandatory closing step with the two triggers stated as tests (dimagi-internal/ace#1646).** The composition checklist carried tagging as a single descriptive bullet ("use [training-gap] and [product-feedback] tags per the golden template conventions") with no obligation attached, and it is the one behaviour in that checklist that came back weak: 5.0/10 on the deep rubric's 15%-weighted Tagging dimension, 5 of 8 expected tags missed on a 51-prompt suite where content scored 49 Pass / 2 Warn / 0 Fail. Sharpest miss: two answers that correctly volunteered a known product limitation and did not tag it — the bot reached for `[product-feedback]` on a *reported* bug but not on a *volunteered* limitation, so both halves of that trigger are now spelled out. Validate with `--prompt-patch` (no re-index) plus a deep re-run. Observed on `bednet-check-2-visit/20260825-1310` Phase 5. | ACE team |
| 2026-08-26 | **Step 5 generates `00-program-contacts.md` into the KB; Step 7 points at it instead of restating the escalation address (dimagi-internal/ace#1665).** The recipe carried no file naming the programme's contacts, so `ace@dimagi-ai.com` lived only in the composed prompt — reproduced from recall, with no retrievable anchor for retrieval to correct. On `hh-poverty-targeting/20260824-1404` (experiment 13014, collection 566) a 73-prompt deep run emitted `ace@dimagi.com` twice and an invented `pm@dimagi-ai.com` once against 27 correct entries; under `ocs-chatbot-eval` § `fabricated_operational_specifics` each clamps to Fail. The contacts page sources the admin address from `config/agent.json` and OMITS any row whose authoritative source is absent in this run (usually the `selected_llo` rows, since Phase 5 precedes Phase 8) rather than filling a placeholder. The ace#1142 anti-fabrication guard in `scripts/bootstrap-ocs-golden-template.ts` is untouched and remains the cold-start fallback. **That last clause was false and is superseded by dimagi-internal/ace#2216** — Step 8 replaces the prompt wholesale, so the guard is live only before the publish; the composed prompt must carry the exactness protection itself, and Step 7.5 now asserts it. Pinned by `test/skills/kb-contacts-present.test.ts`. | ACE team |
| 2026-09-01 | **Step 5: third upload constraint — strip embedded `data:` payloads before uploading (dimagi-internal/ace#1827).** `exportAs: 'text/markdown'` inlines every embedded image in a native gdoc as base64, so an illustrated document reaches the RAG index at 8-28x its prose size; on `bednet-check-2-visit/20260828-0629` the training pack was 91% base64 by volume and the FLW guide was 264,538 bytes for ~9 KB of prose. Every downloaded file now goes through `scripts/strip-inline-data-uris.ts` (pure helper `lib/inline-data-uri.ts`) before the first upload call. Note the export shape is a link-reference DEFINITION (`[image1]: <data:...>` + `![][image1]`), not the inline `![alt](data:...)` the issue proposed matching — that regex matches zero of the 16 payloads in the specimen. Pinned by `test/skills/ocs-upload-strips-data-uris.test.ts`. | ACE team |
