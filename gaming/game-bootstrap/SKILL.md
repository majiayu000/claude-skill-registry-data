---
name: game-bootstrap
description:
  "Set up a new game project or resolve missing GameGen preferences using question tools, then prove its selected
  asset-to-engine pipeline. Use also to update shared game choices, including saved art style fields; game-concept-art
  produces the resulting concepts and art direction document."
---

# Bootstrap a GameGen project

Read [shared context](../../references/shared-context.md). Start from the actual repository and conversation. The
required project file is `.agents/gamegen-prefs.json`. Never bootstrap the plugin package itself as a game.

## Resolve choices before production

1. Inspect existing preferences, project layout, accepted concepts and user decisions. Carry forward the title,
   description, player goal and development scope already provided. Inspect available Godot, local Blender,
   image-generation and optional service capabilities. For Blender, discover the executable and run the background
   Python probe in the [CLI workflow](../../references/blender-cli.md); no Blender MCP setup is needed. When audio is in
   scope, check `uv` and `ffmpeg` for the
   [local procedural audio route](../../references/providers.md#local-procedural-audio). Reuse working connections for
   providers that use them.
2. If the file is absent, run `python3 <plugin-root>/scripts/prefs.py init --project <game-repository>`. This writes an
   unconfirmed draft, not approved defaults. Use `read` for an existing file and preserve its chosen paths.
3. Run `questions --project <game-repository>` and use [the intake catalog](../../references/intake.json) to identify
   unresolved sections. Prepare one setup phase with related questions grouped into tool-sized batches. Ask all relevant
   production choices during this phase, before asset or gameplay production.
4. Use the available ask-question tools. In Default mode use the asynchronous question tool when available; use a
   blocking question tool only in a mode that supports it. Give concise alternatives, place a justified recommended
   option first and label it `Recommended`, explain its tradeoff, and allow a custom answer. Titles, descriptions and
   creative goals often need free text. Do not make every option a recommendation.
5. Wait for submitted answers on required choices. A preselected option, empty response or timeout is not acceptance. If
   question tools are unavailable, ask a concise direct question instead. Reuse explicit earlier answers and accept a
   user's instruction to choose reasonable defaults. Never require the user to re-enter all preferences after a partial
   answer.
6. Resolve applicable technical details through inspection and the pipeline proof within the user's selected policy.
   Distinguish 2D/3D simulation from rendering in 2.5D. Ask about tile dimensions and directions only when relevant. Set
   model/provider routes per purpose, with explicit permitted fallbacks and separate cash/credit budgets. Discover
   supported model choices before recommending them.
7. Write submitted answers or existing explicit decisions to a temporary JSON patch. Apply with
   `apply --project <game-repository> --answers <file> --expected-revision <revision> --confirm <section>`; repeat
   `--confirm` only for resolved sections. Arrays replace their previous values. Read back each update. The helper
   serializes writes and rejects stale revisions.

MacOS and iOS are proposed platform defaults. Godot, Blender, GPT Image 2.5 through built-in image generation and
computer use only when needed are proposed tool choices. Propose image model flavors from the
[shared flavor policy](../../references/providers.md#gpt-image-25). Resolve whether the selected route supports flavor
selection or uses an accepted opaque `provider-default`; do not present a built-in route without a selector as an exact
model choice. Higgsfield is disabled until an enabled purpose and credit allowance are resolved. SpriteCook is optional,
uses its native MCP and installed skills, and needs its own credit allowance. These recommendations do not become
accepted choices merely because the draft contains them.

For uninterrupted unattended work, resolve agent selection of concepts/assets upfront. If the user wants review
checkpoints, select assisted workflow and prepare the actual review artifacts when reached. Scope includes included
features, content size, playtime and exclusions. Signing can stay deferred for editor/local-preview work. The helper
allows explicit deferral of playtime or memory budget if they cannot usefully be set yet; a production skill cannot
silently defer core choices.

## Prove and finalize

Read [repository conventions](../../references/repository.md) and [provider routing](../../references/providers.md). Use
the selected renderer and paths. For an existing project, preserve its main scene and ordinary saves. For a new project,
create only the folders and initial scenes needed by the brief. Merge the optional AGENTS template into existing
conventions without overwriting them.

Prove one representative pipeline: create or import a tiny sprite/tileset/model, import it in Godot, run a scene,
exercise movement or interaction, and capture the actual output. For 3D check scale, facing, materials and one
articulated motion; for 2D check alpha, scale, pivot and frame or tile layout. A tool connection alone is insufficient.
Record executable/version, chosen renderer, errors, output paths and remaining limits in project evidence. Do not claim
deployment or physical-device readiness from editor success.

Once intake and the technical choices are resolved, run
`finalize --project <game-repository> --expected-revision <revision>`, then
`validate --project <game-repository> --ready`. Summarize the saved configuration and pipeline result. Continue the
authorized game task without repeating setup questions.
