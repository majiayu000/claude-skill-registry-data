---
name: dircreative
description: "Use after explicit $dircreative for film concepts, stories, scripts, director or creative groups, shot/asset planning, reference-video analysis, and image/video prompts. Real media execution requires the corresponding authorization. Validated ADCO handoffs are supported. DIRcreative source maintenance is outside this Skill."
---

# DIRcreative

Plans and prompts are not media.

## Invocation Boundary

Start only on explicit DIRcreative invocation (for example, `$dircreative`) or validated `adco.specialist-exchange`
selecting `dircreative.film-preproduction`. DIR/ADCO source maintenance stops
runtime execution (`source_maintenance`); runtime tests use isolated fixtures.
Never modify project instructions to activate this Skill.

## Router Contract

Choose the route by unfinished work. Read exactly one selected Route Card and its active
reference together; replace references by stage and reuse loaded bodies.
There are zero unconditional protocol reads. An obvious Fast or Studio request needs no router tool call.
Canonical asset work still uses the stage selector before its first image.

**Full film preparation starts in Studio even when images are authorized.**
Delivery executes already-designed assets after the required film craft.

| Requested result | Mode / route | Task reference |
| --- | --- | --- |
| Bounded copy/script edit | Fast / `copy_revision` | `references/copy-script.md` |
| One shot / small storyboard review | Fast / `shot_optimization` or `storyboard_review` | `references/shot-storyboard.md` |
| Bounded prompt edit | Fast / `prompt_revision` | `references/prompt-model.md` |
| Two-or-more-person blocking, movement or reverse-shot discussion | Studio / `film_development` with `spatial_discussion` layer | `references/spatial-discussion.md` |
| Other bounded revision | Fast / `bounded_revision` | none |
| Reference-video analysis | Studio / `video_distillation` | `references/video-distillation.md` |
| Client-readable story only | Studio / `film_development` | `references/client-story.md` |
| Full film/scene preparation, including real images | Studio / `film_development` | `references/film-development.md` |
| Recurring character master/derivative | Studio / `film_development` | `references/character-master-sheet.md` |
| Execute an already-designed asset / client delivery | Delivery / `generation_authorization` or `client_delivery` | `references/generation-delivery.md` |
| Validated ADCO handoff | Delivery / `adco_specialist_exchange` | `references/specialist-exchange.md` plus descriptor schema |

Route Cards: `routes/fast-task.md`, `routes/studio-development.md`,
`routes/delivery-audit.md`. Run `scripts/dircreative_route.py` only to validate an ADCO handoff
or resolve genuine ambiguity; it is not a mandatory creative preflight.
A handoff must validate its actual descriptor, sources, locks and output scope.

## Work from the requested outcome

Preserve supplied material and the whole requested output set. Story-only stops
at story; full preparation continues through script, shots, assets and prompts.

- **Fast:** one bounded change, zero Threads or Director Room. Return the edit.
- **Studio:** one controller, at most three dynamic professional perspectives
  and one critical pass. Establish dramatic cause, action, visual/sound choices
  and continuity before matrices.
- **Delivery:** check tool/reviewer/readback availability early; validate the
  asset and dependencies, execute authorized work, inspect, then continue.

Named 导演组/创意组 use the active craft card. For real/ambiguous collaboration read
`docs/film-preproduction/director-room-routing.md`. Distinguish perspectives,
subagents and user tasks. Never simulate delegation. No nested dispatch
through ADCO; disclose unavailable tools before substituting single-agent work.

## Project Interaction

For a new story or film-preproduction project with unknown preference, use the
host's native choice control for `讨论共创（推荐）`、`直接执行`、`关键节点讨论` and
wait for a real reply. `自行编排`、`自主完成`、`直接执行` are direct-mode choices:
record them for this project and do not ask again. 创意组 covers story, motivation
and writing; 导演组 covers performance, shots, space and sound. They are
perspectives, not a subagent claim. Detailed tool, deduplication and fallback
rules live in `docs/film-preproduction/chat-co-creation-interface.md`.

Skip this setup for bounded edits, analysis, already-designed assets, source
maintenance and ADCO workers. Discussion answers the current issue without a
mandatory question each turn. When a direction is ready, state direction, style
and concrete scope, then offer `按此开始制作` or `继续调整`. Production start only
executes that shown, authorized scope; it never authorizes unlisted media or
client delivery.

## Intelligent Skill Stack

Infer required assets from the requested deliverables and current story, including
“九宫格分镜和相关资产”. Apply `references/shot-development.md` through
`select --stage <stage> --format task`. Recurring human assets default to one
identity per master: frontal portrait plus front, left, right and back full bodies;
read `references/character-master-sheet.md` before designing them. A standalone
portrait or text-only board stays bounded. Initial assets need design, not their
own future images.

For canonical asset generation, use `references/image-execution.md`: prepare the
role-bound Jingzao spec, validate the current packet, submit its returned arguments,
record the real PNG, and inspect the batch before an actual downstream dependency
uses it. Repair failed candidates within scope. A generic compiled prompt, later
plan, or unchecked generation cannot replace this sequence. Contact/action
rehearsals and narrative frames retain their selected craft and coverage requirements.

Reuse the scenario/gaps/staged-pass selector: one craft owner, needed
collaborators and at most one validator. Read each selected method once and
reuse it; when a public helper already returns the needed output, do not read its
source or tests. “已用” requires applying the selected body.

## External User Gates

External gates are `concept_lock`, `generation_authorization` and
`client_delivery_approval`. Reuse scoped authorization; image, video and delivery
remain separate. Unknown facts block only affected claims.

## State and truth

`standalone_chat` owns response/state. In `orchestrated_worker`, ADCO owns
adoption, versions, visibility and cleanup; return artifacts, domain QA, status and open questions.
Keep one creative source and one physical owner for identical bytes; mark only affected descendants stale.
Use `runtime/state-snapshot.schema.json` for resume or multi-file execution;
follow `references/project-hygiene.md` after the first useful artifact.

## Quality and completion

Preserve source truth, project vocabulary, voice and genre. Before affected assets
or prompts, reconcile the current source and adjacent continuity; proposed revisions
do not become source facts. Keep offscreen presence distinct from an actual exit.
Use `references/copy-script.md` for language craft; load
`references/humanization-workflow.md` only for requested layered diagnosis,
demonstrated document-scale defects or explicit providers.

Keep Prompt IR model-neutral; compile one verified model surface at a time.
Preserve reference roles, acting, scene/support truth and preserve/change limits.
Record final candidates in `ai-film-production-ledger`; it neither executes nor approves.

Whole-film coverage follows `references/film-development.md`. A ready root asset
starts as soon as its design/authorization are ready; do not wait for unrelated
downstream coverage. Generate independent assets in a batch; review only blocks
the real next dependency. Preserve five-view masters, approved parent locks and
actual image QA. Required coverage remains checked at its own stage and delivery
gate. Show a newly completed story/shot artifact briefly with its openable file;
preview each saved image immediately, but do not call either acceptance. Continue
authorized self-check and repair without stage-by-stage process broadcasts.
`visual_assets_complete` requires real canonical PNGs, visual review and trusted
readback across the requested scope. It is not a finished video or user/client
acceptance. Required pre-video gate gaps remain work to finish, not completion.
