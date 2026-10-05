---
name: dircreative-chat-facilitator
description: Present DIRcreative work result-first, using the project's chosen discussion, direct, or checkpoint interaction mode.
---

# Chat Facilitator

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/chat-co-creation-interface.md`
- `docs/film-preproduction/chat-stage-gate-integrity.md`
- `docs/film-preproduction/live-chat-start-protocol.md`
- `docs/film-preproduction/chat-inline-visualization-interface.md`
- `docs/film-preproduction/professional-agent-voice-standard.md`
- `docs/film-preproduction/capability-aware-generation-policy.md`
- `docs/film-preproduction/phase-contracts.yaml`

## Inputs

- routed user request and selected artifact scope
- known brief facts and bounded working assumptions
- current reversible internal state
- current generation and delivery authorization state
- project interaction state: status, mode, groups, discussion stage, checkpoints,
  and scope identity

## Outputs

- interaction setup when a new eligible project has no choice
- useful artifact or revision first after setup
- material assumptions or QA findings
- at most one user-facing question or discussion issue per response
- compact state update only when the selected mode persists state

## Rules

- Treat chat as the primary interface and files as backing evidence.
- For a new story or film-preproduction project with no interaction preference,
  explain `讨论共创`、`直接执行`、`关键节点讨论`, explain 创意组/导演组/both, and
  wait for the selection. Group names select perspectives; they do not imply
  subagents. Store it only for the current project scope. Skip this setup for
  bounded edits, analysis, already-designed asset execution, source maintenance,
  and ADCO workers; never repeat a confirmed same-scope choice.
- Reuse all known brief facts; do not ask the user to confirm supplied facts.
- In `讨论共创`, handle the current response with material judgment and usable
  suggestions, then wait for natural feedback. Do not append a compulsory
  question to each reply. “继续” stays in the current discussion stage, not
  automatic script, storyboard, or generation work. In `关键节点讨论`, wait at agreed
  creative checkpoints before production; in `直接执行`, continue through the
  authorized scope. Do not turn production reviews or repairs into questions.
- The user may switch interaction mode or groups at any time within the project.
- Resolve the current issue before offering another discussion turn. Once there
  is enough information, summarize direction, style and concrete production
  scope, then offer a short natural choice such as `按这个方向开始做，还是继续调整？`.
  This is not a mandatory approval at every story/script/shot stage.
- Bare “继续” or “可以” remains in the current discussion stage. Clear equivalents
  of `确认故事，进入剧本` and `确认剧本，进入分镜` set `discussion_stage` to `script`
  and `shots`. An equivalent of `讨论完成，准备生产` sets
  `discussion_stage: production_ready` and `awaiting_checkpoint: production_start`;
  first show the nonempty `production_scope` and any requested media, then ask
  whether to start. Only a subsequent explicit equivalent of `确认开始生产` may set
  direct stage `production` and execute previously authorized listed items.
  Production confirmation never supplies media-generation or delivery permission.
- For setup, real direction choices, agreed-stage wrap-up, and production start,
  inspect current-host tools and prefer native choice controls:
  `request_user_input_async` when available, `request_user_input` only in a mode
  that permits it, otherwise a callable host equivalent. Use `DIRcreative ·
  协作方式`, `DIRcreative · 方向确认`, or `DIRcreative · 开始制作`. Initial choices
  are `讨论共创（推荐）`、`直接执行`、`关键节点讨论`; wrap-up choices are
  `按此开始制作`、`继续调整`. Wait for a real user reply after calling the tool;
  defaults, timeouts, and success receipts are not confirmation. If no native
  control is callable, state `TOOL_BLOCKED` for button display and give text
  fallback without claiming buttons appeared. Do not create a UI site.
- Keep “优化这个镜头” on the shot and “修改第三句” on the line.
- For direct artifact requests, put valid work in the first response.
- Treat `story_state`, `script_state`, `shot_state`, `visual_state`,
  `reference_state`, `prompt_state`, and `qa_state` as reversible internal state.
- External authorization stops remain `concept_lock`, `generation_authorization`,
  and `client_delivery_approval`; reuse existing scoped authorization. Interaction
  setup and discussion wrap-up are confined to the creative phase.
- Use `concept_lock` only for materially incompatible creative directions.
- Never treat “继续” as real generation or client-delivery authorization.
- State `当前没有生成真实图片或视频` for prompt-only output.
- Keep `阶段: 出图执行建议`, `阶段: 视频生成建议`, and `阶段: QA 与重试规则`
  as optional organization labels, not additional user gates.
- Keep each discussion turn to one key issue; ask no extra question once an
  answer is sufficient to proceed.
- Do not manufacture options, disagreement, or approval ceremonies.
- Do not dump raw YAML/JSON or backend mechanics as the main response.
- Read legacy eleven-gate records only when validating an existing v1 fixture;
  never create those gates for a v2 run.

## Chat Surface

Before an eligible project's interaction setup, return the concise mode/group
choice and wait. In discussion mode, return `professional judgment -> usable
suggestion`; when a real decision is due, use `direction + style + production
scope -> start or adjust?` instead. In direct mode, return
`artifact -> material assumptions -> next action`; at a real authorization gate,
return `artifact preview -> professional judgment -> 用户确认点 -> one decision`.
`智能体创作内容` and `阶段:` are optional labels, not proof of work.

When visualization adds clarity, use `skills/dircreative/assets/visualizations/stage-surface-registry.json#stage-context-strip`
only when a visual materially improves the active decision. A selection stays
presentation-only until the controller echoes and validates it.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Fast with no file write needs no receipt. Otherwise record route, changed
artifacts, assumptions, stale outputs, external gate if any, QA status, and next
action in the smallest receipt allowed by the selected Route Card.
