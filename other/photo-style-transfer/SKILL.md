---
vendored_from: https://github.com/beatra-ai/photo-to-anime-skill
name: photo-style-transfer
description: "Turn a photo into anime, manga, comic, cartoon, watercolor, clay, or 3D character art while the person, pet, or product stays recognisable. This AI photo restyler works as a photo-to-anime converter and AI cartoonizer you can steer: apply a style like a filter over your own picture, or add style samples to steer the palette, line weight, and shading. A selfie, portrait, pet photo, product shot, or travel picture becomes illustration-style art for social avatars, profile pictures, sticker sets, posters, merchandise, and content series, with one chosen look repeated across a whole batch."
triggers:
  - photo-style-transfer
  - photo
  - style
  - transfer

---

# AI Photo Restyler

Turn one real photo into a chosen illustration style while the subject stays
recognisable. Anchor the look with the user's own style references when they
have them, then keep that same look across every later photo in the set.

## Scope and routing

Use this Skill when a photo already exists and the user wants it redrawn: anime
or manga, cartoon, comic, watercolor, ink or line art, pencil sketch, clay or
toy figure, 3D character, pixel, cyberpunk, or a look copied from a reference
image they supply. It fits social avatars and profile pictures, sticker and
emoji sets, couple and family portraits, pet portraits, travel and event
recaps, merchandise artwork, and a series of posts that must share one style.

Route a video restyle to `ai-video-restyler`. Route a reusable multi-view
character sheet to `ip-character-consistency-studio`. Route repairing an
already generated image toward realism to `ai-image-realism`. Route animated
comic-drama shots to `ai-comic-drama-shot-maker`, and a business headshot to
`ai-headshot-studio`.

## Inputs and defaults

The one hard input is a source photo the host Agent can actually inspect.
Everything else has a working default. Reuse the style words, reference images,
subject, destination surface, canvas, batch, and must-keeps already present in
the conversation.

Ask only when the answer changes the paid result: which style, when no style is
stated and none can be read from a supplied reference; and which subject to keep
when a photo has several people and the user named none.

Defaults that avoid extra questions:

- `count: 1` for a first look, so the user judges one result before a batch.
- The omitted edit canvas is 2K following the base photo's aspect ratio, because
  the base anchors the canvas on an edit.
- `model: "auto"` unless the user names a model.
- Must-keeps default to face and likeness, hair, visible clothing, pet markings,
  product shape and logo, and any element the user calls out.

Style references are ordered inputs. The source photo is the base and comes
first; up to three style references follow in the order their influence should
apply. Say which reference contributes what — palette, line weight, shading, or
overall look.

## Golden path

1. Inspect the source photo and write a short restyle card: subject, the one
   target style, must-keeps, destination surface, canvas, and batch size.
2. Upload local files once through the bundled client and reuse each returned
   artifact reference.
3. Call `beatra.models.list` for the capability the chosen route needs —
   `image_edit` for an in-place restyle, `image_to_image` for a new composition —
   and read the live card for accepted input count, canvas, controls, and price.
4. Compose one `beatra.images.edit` request: the source photo as the base first
   input, ordered style references after it, one positive prompt naming the
   target style and the must-keeps, no `edit_regions` because the whole frame is
   being redrawn, `count: 1`, and a `seed` when the look must be repeatable.
5. **Confirm before paid work.** Show the frozen prompt, the exact ordered
   inputs, canvas, model, controls, output count, current maximum charge, and
   one opaque stable `client_request_id`.
6. Submit exactly once, record the task ID immediately, and poll that same task.
7. Deliver the real artifact and report only the actual returned task status,
   resolved model, dimensions, format, and `billing.net_charged_credits`. Review
   only media the host Agent can actually see, say what it could not inspect,
   and treat the must-keeps as a drift review rather than exact preservation.

Once the user accepts a look, reuse its exact prompt, reference order, model,
and `seed` for the rest of the batch so the set matches. Each additional image
is new paid work and needs its own confirmation and request ID.

Choose `beatra.images.transform` instead when the user wants a new composition
rather than the same photo redrawn — a new scene, pose, or layout built from the
photo plus references. On a transform an explicit preset `aspect: "source"`
follows the last ordered input and the omitted default is 2K at 16:9, so state
the intended ratio explicitly. Read
[the photo restyle workflow](references/workflow.md) for payload shapes, style
recipes, batch consistency, recovery, and delivery review.

## How this Skill executes

Use the bundled `scripts/mcp_client.py` for every remote Beatra operation: the
MCP tool name is the CLI argument after `call`, and one JSON object goes on
standard input. Never configure or call a host Beatra Connector, and never use
REST/OpenAPI as a fallback. Register the package with
`beatra.installations.register` on first use. Every creation is an asynchronous
task: submit once, then follow that task to a terminal state.

## Decisions that require confirmation

Confirm before submitting any paid request: the frozen prompt and ordered
inputs, the canvas when it differs from the source, the output count, an
explicit model choice, and the current maximum charge. A changed source photo,
style, reference order, prompt, canvas, model, control, or count is new paid
work with a new request ID.

## Recovery

Save every task ID the moment it returns and poll with `beatra.tasks.get`;
`queued` and `running` mean wait. Replay a create only when its response is
genuinely unknown and the payload is byte-equivalent under the same request ID.
If a task ID is lost, use `beatra.tasks.list`, confirm candidates with
`beatra.tasks.get`, and recover the original before considering new work. Call
`beatra.tasks.cancel` only at the user's request; on `409`, keep polling the
original task and report cancellation only when its terminal status is
`canceled`.

## References by task

- [Photo restyle workflow](references/workflow.md): style recipes, ordered
  reference payloads, batch consistency with `seed`, revision edits, recovery,
  and delivery review.
- [Installation and authentication](references/installation-and-auth.md) and
  [installation registration](references/installation-registration.md): first
  use and shared credentials.
- [Tasks and results](references/tasks-and-results.md) and
  [billing, errors, and recovery](references/billing-errors-and-recovery.md):
  task, artifact, and billing facts.
- [Bundled MCP Client diagnostics](references/mcp-connection.md): client
  operation and connection diagnostics; do not configure a host Connector.
- Updates and security: [updates and security](references/updates-and-security.md)
- [uninstall and disconnect](references/uninstall-and-disconnect.md): package
  removal and shared credential cleanup.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
