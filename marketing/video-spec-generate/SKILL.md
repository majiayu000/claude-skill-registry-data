---
name: video-spec-generate
description: >
  Template-agnostic generator for ace-web video programs. Ingests a template's
  structured data (meta + intent + skeleton + example), fills every
  {{placeholder}} from a source (program-page URL, pasted brief, or prospect
  research), substitutes into the skeleton, validates, and POSTs the complete
  spec to ace-web. Works for every video template; no per-template prompt
  required. Owns one artifact: the new program's spec.yaml in Drive.
disable-model-invocation: true
---

# video-spec-generate

Turn any **source** (a Connect program-page URL, a pasted brief, or prior
prospect research) into a fully-populated `spec.yaml` for ace-web's videos
surface using the template you specify. POST it as a new program in the target
workspace. The output is a Drive file at
`<workspace.drive_root>/videos/<slug>/runs/run-001/spec.yaml` plus a program
detail page in the ace-web UI ready to render.

This is the general generator. `video-from-program-page` is a thin wrapper
around this skill (source = Connect program URL, template = `60s-campaign-overview`).
`partnership-video-build` is a specialized wrapper that pre-assembles
partnership-research artifacts before delegating here.

Adding a new video template requires only `meta` + `intent` + `skeleton` +
`example` in ace-web — no new skill, no new prompt.

## Inputs

| Name | Required | Default | Notes |
|---|---|---|---|
| `template_id` | yes | — | The ace-web template to use (e.g. `60s-campaign-overview`, `connectify-program`, `partnership-pitch`). |
| `source` | yes | — | A program-page URL, pasted text brief, or structured research content (prospect.yaml + angles.yaml for partnership-pitch). |
| `program_slug` | yes | — | Slug for the new video program. Must match `[a-z0-9][a-z0-9-]{0,63}`. |
| `workspace_slug` | no | `dimagi-team` | ace-web workspace to write into. |
| `gdrive_folder_id` | no | — | Drive folder holding the program's media. When set, enumerates it and populates `manifest:` + clip refs. |
| `base_url` | no | `$ACE_WEB_BASE_URL` or `https://labs.connect.dimagi.com/ace` | ace-web base URL. |
| `no_post` | no | false | When set, print the filled spec to stdout instead of POSTing (useful for eval or manual inspection). |
| `ACE_WEB_PAT_TOKEN` | yes (env) | — | Bearer token. ACE's own by default (`/ace:setup`); yours via `/ace:ace-web-pat-mint`. |

## Outputs

1. **One Drive file** at `videos/<slug>/runs/run-001/spec.yaml` in the target
   workspace's Drive root. (Skipped when `--no-post` is set.)
2. **Stdout summary** — program detail URL + a list of any `[TBD]` placeholders
   the agent couldn't confidently fill.

## Preconditions

- `ACE_WEB_PAT_TOKEN` is set. If not, instruct the operator to run
  `/ace:ace-web-pat-mint` and stop.
- The target ace-web is reachable at `<base_url>/api/health`.
- The operator has Editor (or higher) membership in the target workspace.

## Steps

### 1. Resolve inputs and validate slug

- Parse args. Strip trailing slash from `base_url`.
- Validate `program_slug` against `[a-z0-9][a-z0-9-]{0,63}`. Reject `..`, `/`,
  leading hyphen. Stop with a clear error if invalid.

### 2. Fetch the template bundle from ace-web

```bash
curl -sS -H "Authorization: Bearer $ACE_WEB_PAT_TOKEN" \
  "$BASE_URL/api/w/$WORKSPACE_SLUG/videos/templates/$TEMPLATE_ID"
```

The response has:
- `meta` — template metadata: `id`, `name`, `description`, `expected_duration_seconds`,
  `intended_audience`, `when_to_use`, and **`intent`** (1–3 sentences naming the
  template's narrative thesis — the irreducible per-template framing). The `intent`
  field is the primary per-template signal this skill consumes.
- `skeleton_yaml` — the `spec.template.yaml` skeleton with `{{placeholders}}`.
  Read it to discover: which beats/sections exist, whether `problem`/`impact`
  stat beats are present (→ whether numbers are in play), and whether
  `narration.variants[]` is present (→ multi-angle mode).
- `example_yaml` — the `example.spec.yaml` fully-filled reference; this is the
  few-shot exemplar of what a good completed spec looks like for this template.
- `prompt_md` *(optional)* — a legacy per-template prose prompt, present only
  on older templates. **Do NOT treat this as the primary generator instruction.**
  If present, append it after all universal steps as a low-weight per-template
  override. The universal body below is authoritative.

Stop on non-200 with a clear error.

### 3. Ingest the source

**If `source` is a URL:**

Use WebFetch against the URL. Capture:
- `program_name` (page H1 / `<title>`)
- `country_focus` (look for country mentions, "active in" lines)
- `program_tagline` (one-line description / hero subtitle)
- `status` (e.g. "Active in 4 countries", scale indicators)
- Headline stats: e.g. "1M+ verified visits", "350K beneficiaries"
- Partner / funder mentions

If the page returns 4xx/5xx or has less than ~200 useful words, fall back to
operator-pasted source:

> "Could not auto-extract from `<url>` ({status}). Paste the program write-up
> below as raw text (Ctrl-D to finish), or rerun with a working URL."

**If `source` is pasted text or structured research:**

Parse the pasted content directly. For partnership-pitch, the caller supplies
`prospect.yaml` (identity), `angles.yaml` (three pre-grounded narration
variants), and research content — use them as authoritative without rewriting.

### 4. Optionally enumerate Drive media

If `gdrive_folder_id` is set, call:

```
mcp__plugin_ace_ace-gdrive__drive_list_folder { folder_id: gdrive_folder_id }
```

Filter to MP4 / MOV / PNG / JPG. Suggest aliases from filenames:
`web-microplan.mp4` → `@microplan`, `field-walking-towards-house.mp4` → `@field-walk`.
Format as:

```yaml
gdrive_media:
  - { name: "file.mp4", file_id: "1...", mime_type: "video/mp4", suggested_alias: "alias" }
```

If `gdrive_folder_id` is absent, skip. The generator leaves the manifest empty
for hand-edit via the ace-web UI.

For templates that expose a workspace media library endpoint
(`GET …/api/w/<ws>/videos/library/video`), fetch it and prefer `library:video/…`
refs over raw `gdrive:` IDs for demo clips.

### 5. Derive per-beat word budgets (UNIVERSAL — do not override per template)

Word budgets are derived from beat seconds using the formula:

```
target_words = round(beat_seconds × 2.5)
min_words    = target_words - 2
max_words    = target_words + 2
```

**Worked example:**
- A `scene` beat of 8s → target 20w, min 18w, max 22w.
- A `hook` beat of 4s → target 10w, min 8w, max 12w.
- A `product` beat of 12s → target 30w, min 28w, max 32w.
- A `cta` beat of 0s → empty (leave `""`).

Beat durations are declared in the skeleton (or derivable from
`expected_duration_seconds` / beat count). Use the beat-seconds values from the
skeleton's inline comments or the template meta. When beat seconds are not
explicit, divide `expected_duration_seconds` by the beat count equally.

**Enforcement:** after drafting each narration field, count words. If over `max`,
trim before substituting. Going long means the TTS synthesizer cuts mid-word.

### 6. Determine generation mode from the skeleton

Inspect the fetched `skeleton_yaml`:

**Stat beats** — if the skeleton has a `problem:` block (with `problem.big`
placeholder) or `impact:` entries mapped to outcome stats:
- Numbers are in play. Stats MUST come from the source page or research input.
- Never invent numbers. If a stat is unavailable, write `[TBD] <what's missing>`.

**Stat-free mode** — if the skeleton has NO `problem:` block (e.g. `connectify-program`
uses `impact` only for benefit cards with no numbers):
- Omit all numeric claims. Use value-prop language ("Built for scale", not "12× faster").

**Multi-angle mode** — if the skeleton has `narration.variants[]`:
- Generate one complete `by_beat` per angle variant. The angle theses come from
  the template's `intent` field or a structured `angles` block in the source.
- For partnership-pitch: use `angles.yaml`'s pre-grounded text verbatim per beat
  — do not rewrite angle narration.
- Set `active_angle` to the best-fit angle (see template intent for angle selection
  logic; default to `the-scale-gap` when ambiguous).

**Single-angle mode** — if no `variants[]`: produce one `by_beat` block.
Leave `active_angle` unset.

### 7. Fill every `{{placeholder}}` (the content generation step)

This is the LLM-as-agent generation step. Apply the universal voice rules and
the per-template signal (intent + example) to fill every placeholder:

**Universal brand voice (apply to every template):**
- Plain, declarative, specific. Documentary lower-third register — not a TV ad.
- Short sentences. Active voice. Numbers over adjectives.
- Honest mechanism over slogan.
- `narration.by_beat.hook` MUST paraphrase or use verbatim the Connect tagline:
  **"Pay for verified service delivery, not planned activity."**
  Keep all four key concepts: pay / verified / service / delivery. Do not invent
  a different tagline.
- **Banned words** (never use): leverage, empower, transform, robust, comprehensive,
  world-class, transformative, game-changing, synergy, imagine if, what if we told
  you, you won't believe, the future of, a revolution in.

**Per-template narrative signal** — read from the template bundle:
- **`intent`**: the narrative thesis (e.g. "Show the Connectify journey + business
  case; open on the org's reality, not the product; close with the why-scale
  benefit cards"). This defines the story arc the agent fills toward.
- **`example_yaml`**: the few-shot exemplar. Study the completed example to
  understand tone, specificity level, clip choices, and card language for this
  template. Match the register and specificity.

**Specificity mining (do this BEFORE drafting beats):** the source's distinctive
details are what separate "describes THIS program" from "generic Connect copy" —
and they are easy to drop. Up front, extract and rank:
- **Named places** — districts, regions, sites. Surface at least 2-3 of them in
  narration (scene/handoff) — do NOT collapse a named list to a generic count
  ("four districts"). Rotate named places through `scene.lower_third` where it fits.
- **Scale/proof figures** — visits completed, workers trained, footprint (e.g.
  "410,000 verified visits in 18 months", "1,200 CHWs"). These are often the single
  most credibility-building "this is real, at scale" numbers. The two `impact[]`
  cards usually hold *outcome* stats, so route the strongest **scale** figure into
  the `status` field, the `handoff` narration, or the `scene` lower-third so it
  isn't silently dropped.
- **Named partners/funders** — fold into handoff/status if a slot fits.
A spec that leaves named places or a headline scale figure unused is a fidelity
miss even when every stated fact is correct.

**Grounding rule (load-bearing):**
- Never invent stats, organizational backstory, or claims not present in the
  source. If the skeleton has stat placeholders and the source lacks the number,
  write `"[TBD] <what's missing>"` so the operator can grep it before rendering.
- Plausible-sounding fabrications are worse than explicit `[TBD]` gaps — a
  prospect audience or funder will fact-check.

**Output JSON** — one key per `{{placeholder}}` in the skeleton. Every key is
a string. No nested objects, no arrays in the output JSON (nested content is
reconstructed during substitution in Step 8). For any value the agent can't
confidently ground from the source, write `"[TBD] <what's missing>"`.

### 8. Substitute placeholders into the skeleton

Replace every `{{placeholder}}` in `skeleton_yaml` with the corresponding value
from the Step 7 JSON output. If the JSON includes a `manifest` / `scene.clips` /
`product.beats` block (from Step 4), replace the skeleton's empty `manifest: {}`
and `clips: []` with the populated versions.

**Validate** that no `{{` remains in the output. If any placeholder is unresolved,
stop with an error listing the missing keys. Do not proceed to POST with
unresolved placeholders.

Set `provenance` fields in the output spec:
```yaml
provenance:
  generator: video-spec-generate
  template: "<template_id>"
  generated_from: "<source_url_or_brief>"
  generated_at: "<ISO-8601 UTC timestamp>"
```

### 9. POST to ace-web (or print when `--no-post`)

**Normal mode:**

```bash
curl -sS -X POST \
  -H "Authorization: Bearer $ACE_WEB_PAT_TOKEN" \
  -H "Content-Type: application/json" \
  "$BASE_URL/api/w/$WORKSPACE_SLUG/videos/programs" \
  -d "$(jq -nc --arg slug "$PROGRAM_SLUG" --arg spec "$SPEC_YAML" \
        '{slug: $slug, spec_yaml: $spec}')"
```

Expect 201. The response has: `program_slug`, `run_id` (= "run-001"),
`spec_path`, `message`.

On 409 (program already exists): stop — slugs are human-meaningful identifiers.
Surface the error and ask the operator to pick a different `--slug` or copy the
existing run via the ace-web UI.

On 400: surface the `detail` field — the spec failed server-side validation;
revisit the placeholder fill.

**`--no-post` mode:**

Print the filled spec YAML to stdout (without POSTing) and list all `[TBD]`
values. Used for preview, eval, or piping to `video-spec-eval`.

### 10. Report

```
✓ Created video program <slug> in workspace <ws>   [or: ⚠ Printed spec only (--no-post)]
  Template:  <template_id>
  Detail:    <base_url>/w/<ws>/videos/<slug>
  Spec:      videos/<slug>/runs/run-001/spec.yaml
  Run:       run-001
  TBDs (N):  <list of "[TBD]" placeholder values the operator should edit>

Next: open the detail URL above and click "Re-render" to produce
the first MP4.
```

## Word-budget enforcement pass (MANDATORY — run before emitting the spec)

This is a hard gate, not a style note. Beats over budget get cut mid-word by the
audio synthesizer, so an over-budget beat is a defect. After `narration.by_beat`
is drafted and BEFORE you emit/POST the spec:

1. For each beat compute `target = round(beat_seconds × 2.5)` and `max = target + 2`.
2. **Recount the words** in that beat's narration.
3. If any beat exceeds `max`, **re-tighten and re-count** — do not emit a spec with
   any beat over `max`. Never pad an under-budget beat; only expand for real missing
   content.
4. **The `problem` beat is the chronic overrunner** (a short ~8s beat that tempts you
   to carry both a number and the stakes). It must NOT carry *both* the headline
   incidence stat AND the mortality/urgency-timing clause. Keep the single headline
   stat in `problem`; push any timing/stakes clause into the `scene` or `product`
   setup, or compress to one sentence.

## Anti-redundancy: each beat owns a distinct job

The `cycle` beat owns the four-step mechanism (Learn → Deliver → Verify → Pay). The
`product` beat owns the **in-app field workflow** — walk the actual app screens/tasks
the worker performs (e.g. weigh, check temperature, counsel, log the verified visit),
NOT a re-narration of Learn/Verify already in `cycle`. Do not state "GPS + photo
verified" in both beats. If the source names specific places (districts, regions),
use at least one in `scene` or `scene.lower_third` (e.g. `"Kurigram, Bangladesh ·
<Program>"`) — country-only granularity leaves earned specificity on the table.

## Stat-card parity (when the skeleton has stat beats)

Every outcome number you *voice* in `narration.by_beat` (problem/impact) must also
appear on a `problem`/`impact` **card** (and vice versa) — the cards are what the
viewer remembers; a stat spoken but never carded is wasted. If the source gives
three strong numbers and only two card slots exist, card the two strongest and do
NOT voice the third — keep the spoken track aligned to the cards.

## Edge cases

- **Slug collision**: 409 from ace-web. Do not auto-suffix. Surface the error.
- **Sparse source**: mark more fields `[TBD]` rather than invent content.
  The spec can still render; the operator edits gaps in the UI before clicking
  Re-render.
- **Drive folder enumeration fails**: degrade silently — manifest ships empty.
- **Stat beat with no source stat**: write `[TBD] <what the stat should be>`.
  Never guess a number.
- **Multi-angle with thin research**: fill all angle variants with `[TBD]` rather
  than reusing the same thin text across all three.
- **`narration_hook` drift**: if the hook you draft does not paraphrase the
  Connect tagline, rewrite it before proceeding to Step 8.
- **`prompt_md` present**: append the prompt's additional instructions as a
  low-weight supplement AFTER the universal fill above. The universal voice rules
  and grounding rule take precedence over any per-template override.

## Shell reference

```bash
set -euo pipefail

[ -n "${ACE_WEB_PAT_TOKEN:-}" ] || {
  echo "ACE_WEB_PAT_TOKEN not set; run /ace:ace-web-pat-mint"; exit 2;
}

BASE_URL="${BASE_URL:-${ACE_WEB_BASE_URL:-https://labs.connect.dimagi.com/ace}}"
BASE_URL="${BASE_URL%/}"
WORKSPACE_SLUG="${WORKSPACE_SLUG:-dimagi-team}"

# 1. Fetch template bundle
TEMPLATE_JSON=$(curl -fsS \
  -H "Authorization: Bearer $ACE_WEB_PAT_TOKEN" \
  "$BASE_URL/api/w/$WORKSPACE_SLUG/videos/templates/$TEMPLATE_ID")

# 2-8. Agent does source ingestion, budget derivation, fill, and substitution.
#      (Not shell — this is the part the LLM owns.)

# 9. POST the spec (normal mode)
curl -fsS -X POST \
  -H "Authorization: Bearer $ACE_WEB_PAT_TOKEN" \
  -H "Content-Type: application/json" \
  "$BASE_URL/api/w/$WORKSPACE_SLUG/videos/programs" \
  -d "$(jq -nc --arg slug "$PROGRAM_SLUG" --arg spec "$SPEC_YAML" \
        '{slug: $slug, spec_yaml: $spec}')"
```

## Why the universal body is here and template intents are in ace-web

The ~70% shared logic (voice rules, grounding rule, word-budget formula,
multi-angle detection, placeholder substitution, POST) belongs in a single
skill so every template benefits from improvements in one place. The ~30%
per-template signal (intent, skeleton structure, example) belongs in ace-web
so template authors can update it without touching the skill. This skill reads
the structured data; it does not author it.

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-06-09 | Initial skill — generalizes video-from-program-page to be template-agnostic; consumes structured template bundle instead of per-template prose prompt. | ACE team |
