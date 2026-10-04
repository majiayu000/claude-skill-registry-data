---
name: debugging-playbook
description: "Debugging playbook for this project. Use when anything is broken, a test fails, a webhook isn't firing, an AI reply is wrong, or behavior doesn't match expectations, in ANY service. Contains the general investigation workflow plus a list of known gotchas specific to this project's polyglot architecture."
---

# Debugging Playbook

## Step 0 — Check the AI Gateway logs first

If the bug involves anything AI-related (wrong reply, missing translation, TTS failure, agent didn't call the right tool) — the `ai_requests` / `ai_usage_logs` table (Supabase, written by `studio/ai-gateway`) is the single source of truth for what was actually sent to and received from each provider, and what it cost. Check this BEFORE digging into application code; it usually narrows the problem to "the gateway never got called," "the gateway called the wrong provider/prompt," or "the provider's response was fine but the caller mishandled it."

## General Workflow

1. **Reproduce** — get the exact input that triggers the issue
2. **Locate the service** — which of store-backend / storefront / dubbing / ai-gateway / bot-bridge / comment-bot / tts-service / chatwoot owns this code path? (see `project-architecture` skill's service table)
3. **Check the boundary first** — since services only talk over HTTP via env-var URLs, confirm: is the env var set correctly? Is the target service actually running and reachable? (`curl $SERVICE_URL/health` if a health endpoint exists, or just check Railway's service status)
4. **Then go inward** — once the boundary is confirmed working, debug within that one service like a normal app
5. **Fix the root cause, not the symptom** — if you're tempted to add a special-case check, ask whether the upstream service should have sent better data instead
6. **Verify** — re-run the original reproduction

## Known Gotchas (project-specific)

### Bot Bridge service replies to itself in a loop
**Symptom:** bot sends rapid duplicate messages, or costs spike suddenly.
**Cause:** the `message_type === "incoming"` check (see `social-bots` skill) is missing or inverted — the webhook is processing the bot's own outgoing messages as if they were customer messages.
**Fix:** verify the check exists and is the FIRST thing the webhook handler does, before any AI Gateway call.

### Meta webhook returns 200 but nothing happens
**Symptom:** Meta's webhook dashboard shows successful deliveries, but no reply is sent.
**Cause:** usually `X-Hub-Signature-256` verification is failing silently and the handler returns early — check it's not swallowing the verification failure without logging it. Also check: is this the `feed` subscription firing to `studio/comment-bot` when you expected `messages` to `chatwoot`, or vice versa?

### FFmpeg step fails or produces silent/garbled audio
**Symptom:** dubbing job completes but output video has no sound, wrong sound, or the job errors at the reassembly step.
**Common causes:**
- Codec mismatch between the TTS output format and what FFmpeg expects — check the TTS provider's output format matches the ffmpeg command's input flags
- Per-chunk audio durations don't match the original timestamps (translation came out much longer/shorter than the original chunk) — check Step 2's "keep speakable within original duration" instruction was followed
- `background.wav` from the Demucs step wasn't actually mixed back in — check the final ffmpeg command includes both tracks

### Medusa Admin API calls fail with 401
**Symptom:** AI store agent tools (`create_product`, etc.) fail.
**Cause:** Medusa admin auth tokens expire. Check the AI Gateway's Medusa client is refreshing the token, not using a long-lived one that's since expired.

### "It works in Node but not in Python" (or vice versa) for env vars
**Cause:** `process.env.FOO` (Node) vs `os.environ["FOO"]` / `os.getenv("FOO")` (Python) — a var set correctly in Railway for one service won't magically exist with the same name in another unless explicitly configured per-service. Each service's `.env.example` (see `project-architecture`) should be the source of truth for what that specific service needs.

### Dubbing job stuck on one status
**Cause:** check `dubbing_chunks` table — a single failed chunk can block the whole job if the pipeline doesn't handle partial failure. The job should be resumable from the last successful chunk, not restarted from scratch (see `video-dubbing` skill, Job Tracking section).

## Memory Usage

After resolving any non-trivial bug, write a short note to memory: symptom → root cause → fix. Over time this becomes a project-specific "have we seen this before" reference that makes future debugging faster.

