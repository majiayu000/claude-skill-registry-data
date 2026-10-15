---
name: tokenlab-run
description: "The execution contract for every TokenLab media and decision call: read the model contract, pick the operation, estimate cost, upload or link inputs, call the endpoint, wait for async tasks, and read the result URLs. Use when an agent must actually run a TokenLab image, video, music, 3D, world, speech, transcription, or System One request, when a call fails with unsupported_parameter or a contract error, or when a task never seems to finish. Other tokenlab-* outcome skills call this one for the mechanics. To choose which model to use, use tokenlab-model-picker. To write production integration code in an app, use tokenlab-api-integration."
license: MIT
metadata:
  category: foundation
---

# TokenLab Run

Run one TokenLab request correctly: right model, right operation, right fields, a known price, and a finished result. Every outcome skill in this repository uses this procedure.

## Roots and auth

- API root: `https://api.tokenlab.sh`. Docs: `https://tokenlab.sh/docs`.
- Auth: `Authorization: Bearer $TOKENLAB_API_KEY`. Read the key from the environment. Never print it, log it, or put it in a URL.
- Model discovery and pricing need no key. Every create, upload, poll, and cancel call needs a key.

## Execution surfaces

| Surface | When | Notes |
| --- | --- | --- |
| HTTP | Default for scripts and apps | Use the helper below or plain `curl` / `fetch` / `requests` |
| MCP | The client has the TokenLab MCP server | `core` profile has `list_models`, `get_model`, `get_model_pricing`, `create_image`, `edit_image`, `create_video`, `create_music`, `create_3d_model`, `create_speech`, `transcribe_audio`, `upload_file`, `get_task_status`, `cancel_task`, `evaluate_decisions`. World tools (`create_world`, `get_world_status`) need the `full` profile. |
| SDK | The app already uses the OpenAI SDK | Base URL `https://api.tokenlab.sh/v1`. SDKs cover images and audio. Use HTTP for video, music, 3D, worlds, and System One. |

Helper script, standard library only:

```bash
python scripts/tokenlab_run.py contract MODEL --operation OP   # step 1-2
python scripts/tokenlab_run.py price MODEL                     # step 3
python scripts/tokenlab_run.py run /v1/videos/generations --json @body.json --wait   # step 5-7
python scripts/tokenlab_run.py poll TASK_ID_OR_POLL_URL        # resume a stored task
```

The path is relative to this skill's folder. Other TokenLab skills call it as `../tokenlab-run/scripts/tokenlab_run.py`. Without the helper, send the same requests with `curl` (see `references/recipes.md`).

`run` prints the task identity (`request_id`, `task_id`, `poll_url`) to stderr as soon as the create call returns. `--wait` waits up to 100 s by default. Exit code 0 means a terminal success, 1 means failed or unknown, and 2 means the task is still running: continue with the `resume` command in the output.

## The procedure

1. **Read the model contract.** `GET /v1/models/{model}`. Confirm `tokenlab.lifecycle.stage` is `active`. Read `tokenlab.public_contract_summary` (or `public_contract`):
   - `public_operations`: the operations this model sells.
   - `request_endpoint_by_operation`: the endpoint for each operation. It wins over any table in a skill. For example, many image-edit models use `/v1/images/generations` with `operation: "image-edit"`, not `/v1/images/edits`.
   - `operation_constraints[]`: per operation `supported_parameters`, `allowed_durations`, `allowed_resolutions`, `allowed_aspect_ratios`, `parameter_options`, and `notes`.
   - `recommended_request` / `recommended_request_summary`: a known-good starting body.
   - `tokenlab.deliveryAvailability.operations[op]`: which delivery options (`verified`, `official`) have supply for that operation.
2. **Pick the operation and build the body.** Send `model` always. Send `operation` explicitly when the endpoint takes it (images, video). Do not send `operation` to `/v1/3d/generations`; it infers text-to-3d or image-to-3d from the inputs. Send only fields in `supported_parameters`, with values from the allowed lists. A field that is not listed returns `400 unsupported_parameter`; remove it or pick another model. Do not guess fields from the model name.
3. **Estimate the cost first.** TokenLab has no dry-run. Read `GET /v1/models/{model}/pricing`. Multiply the price by your quantity (images, seconds, characters, tokens, or requests; `pricing_unit` tells you which). Prices sit in `pricing_details` as `entries`, `formulas`, `unitPriceVariants`, or a credit table, plus `minimumUnitCount` where a minimum applies. `official` is the Official price; `platform` is the Verified price. The default delivery option `Auto` holds the higher amount and charges the route that ran. To force one option, send `X-TokenLab-Delivery-Policy: verified` or `official` (helper: `--delivery`); with no supply in that option the request fails and is not charged. Use the Official price as the upper bound. Tell the user the estimate before a paid video, 3D, or world job, and before any batch.
4. **Provide input media.**
   - Remote inputs must be public `https` URLs that stay valid until the task starts. No private hosts, credentials, fragments, or short-lived signed URLs.
   - A TokenLab result URL from an earlier task (`https://api.tokenlab.sh/v1/media-results/...`) is a valid input. Chain steps this way: generate an image, then animate or edit that URL.
   - Many image and video fields also take a `data:` URL, but media URL fields accept at most 8192 characters. That fits a small thumbnail, not a photo or an audio clip. Host larger private files at a public `https` URL instead.
   - `POST /v1/files` (`purpose=user_data`, optional `model`) returns a `file_id` for `/v1/images/edits` `images[].file_id`. It is not a general media host for video, music, or 3D.
   - Speech-to-text takes a multipart `file` upload (max 25 MB).
5. **Call the endpoint.** Save the `x-request-id` response header, the returned `id` / `task_id`, `poll_url`, model, and your own job ID before you do anything else.
6. **Wait for async results.** Video, music, 3D, and worlds are always async. Images and transcriptions can be sync or async; decide from the response, not from the model. A response with `status: "pending"` or `"processing"` and a `poll_url` is a task:
   - Poll `poll_url` (fall back to `GET /v1/tasks/{id}`) every 5–10 s. Stop at `completed` or `failed`.
   - A status read returns HTTP 200 even when the task failed. Decide from `status`. On failure read `error_details` (`code`, `param`, `message`, `retryable`). `param` names the field to fix.
   - A timeout on your side is not a failure. Keep the task ID and resume polling. Never create a second task because a poll failed or a page refreshed.
   - Cancel only on user request: `DELETE /v1/tasks/{id}`. Only some queued tasks can be cancelled (`400 unsupported_task_cancel`, `409 task_not_cancellable` otherwise).
7. **Read the result.** Images: `data[].url` (or `b64_json` on a sync request). Video: `video_url`, `video.url`, or `videos[]`. Music: `audio_url` (plus `video_url`, `image_url`, `lyrics` for some models). 3D: `model_url` and format URLs such as `glb_url`. Worlds: `world_marble_url`, `glb_url`, `pano_url`. TTS returns audio bytes. Result URLs stay valid for 30 days; download anything the user needs for longer. Downloads redirect, so follow redirects. A URL can return `502 media_unavailable` for about a minute right after the task completes; wait and try the download again. Do not hand `stream_audio_url` to the user; it is a temporary listening link, not the result.

## Errors

| Error | Meaning | Action |
| --- | --- | --- |
| `400 unsupported_parameter` / `invalid_request` with `param` | Field not in this model's contract | Fix that field from `operation_constraints`; do not drop the user's core input |
| `400 model_not_found` + `did_you_mean` | Wrong or retired ID | Re-discover; switch only with user consent |
| `402 insufficient_balance` | Not enough balance; `estimated_cost_usd` shows the need | Tell the user. Do not switch to a cheaper model without consent |
| `429` | Rate limit | Wait `Retry-After` / `retry_after`, then retry the same request |
| Create request timed out or the connection broke | The task may exist and may be charged | Do not resend. Ask the user first, and check Runs or Usage in the console. The helper reports `accepted: unknown` |
| `5xx` on a create request | The request may or may not have started | Retry only when the body says `retryable: true` and no task ID came back; otherwise ask the user |
| `503 all_channels_failed` / `delivery_tier_unavailable` with `retryable: false` | No supply for this operation and delivery option | Do not repeat. Pick another model that publishes the operation |
| Task `failed` with `error_details.retryable: true` | Transient upstream failure | One new task is acceptable; it is a new charge |

Retrying a failed generation creates a new task and a new charge. Ask before you retry paid video, 3D, or world jobs.

## Quality bar

- The body uses only contract fields, and the model publishes the operation.
- The user saw a cost estimate before any paid job above a few cents.
- The task ID was stored before polling, and the final answer names the result URL, the model, and the task ID.
- Failures report `error_details.code` and `param`, not only "it failed".

## References

- `references/recipes.md`: copy-ready HTTP bodies for each endpoint family.
- `scripts/tokenlab_run.py`: contract, price, run, poll, cancel, and upload commands.

## Related skills

- `tokenlab-model-picker`: choose the model before you run it.
- `tokenlab-prompting`: write the prompt for the chosen model family.
- `tokenlab-api-integration`: put the same flow into application code.
