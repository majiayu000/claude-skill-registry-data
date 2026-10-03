---
name: crun-effect-template
description: Discover, preview, select, and apply Crun video effect templates from Kling, Vidu, or ByteDance using live template-list endpoints and the matching template task model. Use whenever the user asks for an AI special effect, effect template, template video, Kling effect, Vidu effect, ByteDance effect, 特效模板, 模板视频, 可灵特效, Vidu 特效, or 字节特效, including requests that name an effect but do not know its template ID.
---

# Crun Effect Templates

Use `../../../runtime/crun_cli.py`. Treat the authenticated template-list endpoints as the source of truth for current
IDs, preview media, input requirements, supported settings, and credits. A model schema does not enumerate the valid
template IDs.

Read `../../crun-account-credits/SKILL.md` before estimating and `../../crun-task-runner/SKILL.md` before creating or
monitoring a task.

## Discover templates

List one page for a known platform:

```text
python <runtime>/crun_cli.py templates list --platform kling --page 1 --page-size 20
python <runtime>/crun_cli.py templates list --platform vidu --page 1 --page-size 20
python <runtime>/crun_cli.py templates list --platform bytedance --page 1 --page-size 20
```

Look up one exact ID with the unified flag; the CLI maps it to each platform's API parameter:

```text
python <runtime>/crun_cli.py templates list --platform <platform> --template-id <id>
```

Use `total` to fetch additional pages when the requested effect is not on the first page. Never invent an ID, use a
stale remembered ID, or substitute a similarly named effect silently.

When the user has not named a platform and has not already requested a platform-specific search, search Kling first
because it is the preferred default for effect quality. Evaluate its candidates against the user's actual intent,
source-media requirements, preview, settings, and credits. If Kling has a suitable match, use or present that match and
do not query another platform. If no relevant Kling template exists, or the available Kling templates do not satisfy
the user's intent, stop and ask the user to choose whether to continue searching ByteDance or Vidu. Query only the
platform the user selects; do not search both automatically.

When presenting a candidate list, show every candidate selected as relevant and display exactly these five fields for
each candidate:

- Platform
- Template name
- Template input requirements
- Credit cost
- Preview link

Localize the candidate list to the user's language. Localize all five field labels, template names, input-requirement
text, missing-preview text, and surrounding choice instructions. Prefer an official localized template-name field when
the response provides one; otherwise translate the display name when safe while preserving brands and proper nouns.
Keep platform names, numeric credit values, and preview URLs unchanged.

Do not display template IDs, categories, tags, resolutions, settings, cover links, or other metadata in the candidate
list. Preserve each template ID internally so the selected candidate can be queried and submitted later. Never omit
one of the five fields or replace content with an ellipsis. Condense the input requirements into clear localized prose,
removing examples and repetitive wording while retaining every constraint that can affect task success: required image
count and order, subject type or count, accepted aspect ratio or range, prompt requirements, and unsupported inputs.
Report the credit value exactly as returned. For ByteDance, include every `Resolution` and `Credit` pair from
`ConsumeItems` inside the single credit-cost field so no pricing option is lost. Prefer the video preview field
(`video_url`, `video`, or `PreviewVideo`); when no preview link exists, display a localized explicit value. If the
relevant candidates require
multiple messages, continue until every candidate and every required field has been shown. Template browsing or
choosing a preview is not authorization to spend credits.

Interpret each platform's response explicitly:

| Platform  | ID and preview fields                 | Constraint and price fields                                                                          |
|-----------|---------------------------------------|------------------------------------------------------------------------------------------------------|
| Kling     | `key`, `cover_url`, `video_url`       | Read image-count and subject rules from `info`; use `credit`.                                        |
| Vidu      | `template`, `cover`, `video`          | Parse the JSON string in `input_instruction`; use `credits`, `resolution`, and `aspect_ratio`.       |
| ByteDance | `TemplateId`, `Cover`, `PreviewVideo` | Enforce `InputNum` and `InputRequirement`; use the selected resolution's `Credit` in `ConsumeItems`. |

## Validate source media and map the task

Require the selected template's source media before task creation. Accept attached local files or directly usable URLs
from the current conversation. Upload each local file and use its returned `file_url`:

```text
python <runtime>/crun_cli.py upload <local-file>
```

Never send local paths, Base64, or data URIs. Preserve the user's image order for multi-image effects. Read the selected
template's returned instructions and enforce its exact image count and media constraints; do not infer them from another
template.

Use this mapping, then inspect the live model schema before constructing input:

| Platform  | Model                | Template field | Media field | Platform-specific rules                                                                                                                  |
|-----------|----------------------|----------------|-------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Kling     | `kling/template`     | `template_id`  | `img_urls`  | Follow the selected template's `info` instructions for image count.                                                                      |
| Vidu      | `vidu/template`      | `template`     | `images`    | Send optional `prompt`, `aspect_ratio`, `area`, `beast`, `bgm`, or `story` only when the live schema and selected template support them. |
| ByteDance | `bytedance/template` | `template_id`  | `img_urls`  | Choose only a `resolution` published in `ConsumeItems`; report its matching `Credit`, but do not send `ConsumeItems` in task input.      |

```text
python <runtime>/crun_cli.py models describe --model <model>
```

Construct only fields allowed by `input_schema`. Re-fetch the exact template by ID immediately before estimation when
earlier discovery results may be stale.

If a live schema endpoint is temporarily unavailable, do not invent optional fields. Use only the minimal platform
mapping above, then let `task estimate` perform server-side validation before any creation. For Kling the minimal input
is exactly `template_id` plus `img_urls`.

## Estimate, confirm, and run

Estimate the exact final input before every new task:

```text
python <runtime>/crun_cli.py task estimate --model <model> --input-file <input.json>
```

Require `affordable: true`. If the effect or settings were discovered or selected during the conversation, show a
localized summary containing platform, effect name and ID, model, ordered source-media count, relevant settings,
estimated credits, and balance, then obtain explicit confirmation for that exact task. If the user's initial request
already supplied the exact platform, exact template ID, source media, settings, and an instruction to run it, follow the
shared task runner's user-specified-model confirmation rule.

After authorization, create exactly once, retain the task ID, and wait only on that task:

```text
python <runtime>/crun_cli.py task create --model <model> --input-file <input.json>
python <runtime>/crun_cli.py task wait --task-id <task_id> --timeout-seconds 120
```

Follow `crun-task-runner` for timeouts, failures, recovery, downloads, and delivery. Never retry `CreateTask`
automatically. Return the localized effect name, platform, exact template ID, task ID, credits, and local media path;
include the preview or remote result URL only as a fallback.

## Localize interaction

Write all choices, summaries, progress, errors, and delivery text in the user's language. Keep platform names, model
IDs, template IDs, API field names, URLs, task IDs, and enum values unchanged.
