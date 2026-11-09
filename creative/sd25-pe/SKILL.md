---
name: sd25-pe
description: Write and refine Seedance 2.5 video prompts from scene ideas, stories, and image/video/audio references, including keyframes, storyboards, blockouts, edits, and extensions. Use for prompt authoring, not service operation or API troubleshooting.
---

# Seedance 2.5 Prompt Writing

Turn the user's intended scene into one usable prompt. Preserve identities, counts, relationships, key props, event order, outcome, quoted words, and explicit asset assignments. Add compatible creative detail where useful; do not invent observations of unavailable media. User instructions override writing defaults, including format and scope, except that the final copyable prompt must always be written in English.

Prompt writing produces text; it does not authorize generation, uploads, package installation, or asset modification. No particular connector or API is required. Inspect supplied media only with available, authorized capabilities; otherwise work from text and existing labels.

## Choose the relevant guidance

For a simple text-only scene, work directly from this entrypoint. Load only references needed for the request:

| Request | Read |
| --- | --- |
| Images, video, audio, or subject mappings | [Asset roles](references/asset-roles.md) |
| Editing, extension, first/last frames, or conflicting settings | [Task routing](references/task-routing.md) |
| Story, multiple shots, timing, dialogue, camera, or a product process | [Narrative and sound](references/narrative-and-sound.md) |
| Keyframes, storyboard grids, or blockout rendering | [Visual control](references/visual-control.md), plus task routing for frame roles |
| Prompt repair needing an example | [Examples](references/examples.md) |

[Sources](references/sources.md) records provenance and adaptation decisions; it is not a required read for each prompt.

## Write the scene

Establish the subject, setting, main event, and result. Express actions and emotional changes in observable terms. Use a camera plan that supports the event. Where a reference precisely supplies motion or camera work, bind those dimensions instead of restating them inaccurately.

Use a short paragraph for simple scenes. For complex reference tasks, useful optional sections are `【Generation Goal】`, `【Reference Asset Roles】`, `【Event Script】`, and `【Maintain Consistency】`. These are writing conventions, not required API fields. Do not fill empty sections or append generic quality/negative-prompt packs.

Keep output settings such as total duration, ratio, resolution, FPS, and audio enablement outside the model prompt. They guide composition and event density and belong in the downstream interface. Creative timestamps, edit intervals, and dialogue timing belong in the prompt when useful or requested. Use continuous whole-second intervals when designing a timeline; preserve explicit user timing and do not silently retime hard constraints.

Preserve each supplied reference label exactly. Assign roles only to assets actually used; when a complete inventory includes unused assets, list those identifiers compactly under `【Unused Assets】`. Do not invent absent assets or infer identity from filenames.

Write spoken dialogue, lyrics, and in-scene text (signs, labels, screens, packaging) in the language in which they must be heard or seen; never translate them into English because the prompt is English. Keep supplied wording and punctuation verbatim unless translation or rewriting is requested, and write newly drafted lines or text directly in the intended language, such as Korean lines for a Korean-speaking presenter. Bind speech to its speaker and spoken language; do not add an accent or spoken lines just to fill a template. Draft dialogue when the user asks for dialogue creation. Add exclusions such as no subtitles or no BGM only when requested or needed to express an established reference role.

## Deliver

Always output the final copyable prompt in English, regardless of the user's language or any requested prompt language. Do not write the prompt body in Korean or another language. Only the descriptive prompt body is English: dialogue, lyrics, quoted words, and in-scene text stay in their intended spoken or displayed language inside the English prompt, as described above. Do not add a preface, code fence, or explanation unless requested. Follow a requested output format. Sequential operations may require separately labeled prompts; they are not alternative versions.

Resolve routine style, lighting, and camera gaps using context. Ask a concise question only if unresolved identity, reference role, editing master, extension boundary, or incompatible hard constraints prevent a faithful result. Missing media alone does not block a text rewrite with stated roles.

Check intent, bindings, timeline, task routing, and output once. Keep a material submission conflict outside the copyable prompt in a short note; do not claim a prompt can bypass an interface lock or guarantee exact pixels, text rendering, or synchronization. No generation is needed to validate prompt text.
