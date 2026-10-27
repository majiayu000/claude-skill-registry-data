---
name: video-spec-qa
description: >
  Structural QA on the spec.yaml produced by /ace:video-from-program-page
  (or hand-authored) for an ace-web video program. Binary pass/fail.
  13 static checks, no LLM. Gates video-spec-eval.
disable-model-invocation: true
---

# Video Spec QA

Structural correctness checks on the `spec.yaml` for one ace-web video
program. Binary verdict: pass / fail / incomplete. All 13 checks run
statically (parse + regex + arithmetic, no LLM) in <50ms via the
importable `checks.ts` module.

The checks are template-aware: rules like word budgets and required
beats live in `TEMPLATE_RULES` keyed by the spec's `provenance.template`
field. Adding a new template (e.g. `120s-program-demo`) means appending
a new entry there.

See `skills/_qa-template.md` for the shared QA contract (verdict YAML
format, auto-fix protocol).

## Inputs

Pipeline-only: checks a video run's spec, which exists only in a run.

| Source | Artifact | Used for |
|---|---|---|
| ace-web Drive | `videos/<slug>/runs/<run-id>/spec.yaml` | the spec under structural check |

## Products

- A `video-spec-qa_result.yaml` per the canonical `QAResult` schema
  (`lib/qa-types.ts`). The skill prints the result to stdout; the
  caller decides where to persist (a follow-up `videos_publish_qa`
  endpoint in ace-web is the right home, not built yet).

## Checks

| # | id | type | description | auto-fix on fail |
|---|---|---|---|---|
| 1  | `spec_yaml_parses` | static | spec.yaml is valid YAML and the root is a mapping. | Re-author from the skeleton; substitution likely produced invalid YAML. |
| 2  | `required_top_level_fields` | static | All required top-level fields present: slug, workspace, name, country_focus, status, tagline, program_url, manifest, scene, problem, product, impact, narration, voice. | Add missing fields from the template skeleton. |
| 3  | `slug_format_valid` | static | slug matches `[a-z0-9][a-z0-9-]{0,63}`. | Use lowercase letters, digits, and hyphens. |
| 4  | `provenance_block_present` | static | provenance block has generator/template/generated_from/generated_at, all non-empty. | Fill every provenance.* field. The skill must echo template_id and stamp generated_at. |
| 5  | `provenance_timestamp_valid` | static | provenance.generated_at parses as ISO-8601 UTC. | Use ISO-8601 (e.g. `2026-05-15T12:34:56Z`). |
| 6  | `no_unresolved_placeholders` | static | No `{{...}}` survives in the spec body (template fully filled). | Provide values for every listed key. |
| 7  | `impact_count_matches_template` | static | impact[] has the count the template requires (2 for `60s-campaign-overview`). | Provide exactly N entries (use `[TBD]` rather than dropping). |
| 8  | `required_beats_present` | static | narration.by_beat has every beat the template declares (hook/cycle/handoff/scene/problem/product/impact/cta for 60s). | Add missing beats (empty string ok for cta). |
| 9  | `narration_within_word_budgets` | static | Each beat is within its template-declared Min/Max word range. Over-budget audio is cut mid-word at render. | Trim/expand each listed beat. |
| 10 | `no_tbd_in_narration` | static | No `[TBD]` tokens in narration.by_beat (they'd be read aloud). | Replace `[TBD]` markers with real text. Keep `[TBD]` only in titles/captions/sources. |
| 11 | `hook_paraphrases_connect_tagline` | static | narration.by_beat.hook either contains Connect's tagline verbatim or shares 3+ of its 4 key tokens (pay/verified/service/delivery). | Rewrite hook to paraphrase or quote: "Pay for verified service delivery, not planned activity." |
| 12 | `no_banned_voice_tokens` | static | Narration doesn't contain Connect's banned marketing-voice words: leverage / synergy / robust / comprehensive / transformative / game-changing / world-class / best-in-class / cutting-edge. | Rewrite in documentary lower-third style: concrete nouns, numbers over adjectives. |
| 13 | `voice_config_valid` | static | voice.provider/voice_id/model all set. | Restore voice.* from the template skeleton. |
| 14 | `spec_has_renderable_clips` | static | At least one clip is referenced in scene.clips OR product.beats. Remotion's Zod schema requires non-empty arrays — an empty-manifest spec lands in Drive but the render aborts before producing a video. | Either attach footage to manifest: and reference it from scene.clips[] / product.beats[], OR populate `manifest_todo:` with proposed aliases for the operator. |
| 15 | `spec_manifest_refs_resolvable` | static | Every `@alias` used in scene.clips / product.beats has a matching manifest entry. Catches typos and forgotten manifest additions. | Add manifest entries for the missing aliases. Format: `<alias>: gdrive:<file-id>.<ext>` |

The check functions live at `skills/video-spec-qa/checks.ts` as
importable TS. Each returns a `QACheckResult` (`{pass, detail?,
auto_fix_hint?}`) per `lib/qa-types.ts`.

**Adding a check:** append to the `CHECKS` array in `checks.ts`, add a
row to the table above (matching `id`), add a unit test in
`test/skills/video-spec-qa/checks.test.ts`.

**Adding a template:** append an entry to `TEMPLATE_RULES` in
`checks.ts` keyed by the template id. The map declares the template's
`required_beats`, `word_budgets`, and `required_impact_count`. Existing
checks pick the new rules up automatically.

## Process

1. **Read the spec.yaml from ace-web.** Either:
   - Through the workspace's Drive folder via `drive_read_file` if
     you know the file id, **or**
   - Through ace-web's API:
     `curl -fsS -H "Authorization: Bearer $ACE_WEB_PAT_TOKEN" \\
       "$ACE_WEB_BASE_URL/api/w/<workspace>/videos/programs/<slug>/runs/<run-id>" \\
       | jq -r '.yaml_path'`
     gives you the Drive path; pair with `drive_read_file` once the
     Drive file id is in hand.

2. **Save to a local temp path** so the runner can read it as a file:
   `TMP=$(mktemp /tmp/video-spec-XXXX.yaml); cat > "$TMP"`.

3. **Run all checks** via the generic CLI runner:
   ```bash
   ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
   node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/qa-run.ts" \\
     --skill video-spec-qa \\
     --artifact "$TMP" \\
     --target "<workspace>/<slug>/<run-id>" \\
     --capture-path "videos/<slug>/runs/<run-id>/spec.yaml"
   ```

4. **Print the verdict YAML to stdout** for the caller to consume.

## Auto-fix protocol

See `skills/_qa-template.md § Auto-fix protocol`. For video-spec-qa
specifically, the producer that auto-fixes is /ace:video-from-program-page
— the orchestrator passes each `auto_fix_hint` back to it for
regeneration. Two attempts max.

QA is necessary but not sufficient. A passing QA result means the spec
is *gradable*, not that the video will be good. `video-spec-eval`
grades quality.

## MCP Tools Used

- Google Drive: `drive_read_file` (to fetch spec.yaml)
- Bash: `node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/qa-run.ts" ...`

## Writing the result (shared writer — every `-qa` skill)

Write the result file through the shared writer, never by hand:
collect one outcome per check you evaluated (`{check, type, result: {pass,
detail, auto_fix_hint}}`, or `{check, not_judged: "<why>"}` for a check whose
input does not exist yet) into a local JSON file, then

```bash
node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/qa-result.ts" write \
  --skill <this skill> --target <opp>/<run-id> --capture-path <artifact path> \
  --outcomes <outcomes.json> --out <local result.yaml>
```

and upload that file. It derives `stats` from the outcomes and a result that
evaluated nothing is a FAIL (`aggregateQAResult`, `lib/qa-types.ts`); ACE's own
ace-gdrive write guard turns a `*-qa_result.yaml` in any other shape into an
`INVALID_QA_RESULT` error (`lib/qa-result-write-guard.ts`). A hand-written shape reads on ace-web as
"Passed (0/0 checks)" — `skills/_qa-template.md § QA result YAML contract`.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-15 | Initial skill paired with /ace:video-from-program-page (PR #307 in ace plugin). 13 static checks; template-aware via TEMPLATE_RULES. Supports `60s-campaign-overview` out of the box. | ACE team |
