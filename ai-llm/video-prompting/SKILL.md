---
name: video-prompting
description: >-
  AI video/image prompt engineering expert. Triggered when users need to write or optimize prompts for AI video or image generation tools. Helps users craft high-quality generation prompts for various models (Kling, Veo3, Wan, Gemini, Midjourney, Seedance, proprietary models, etc.), incorporating model-specific best practices and formatting requirements. Trigger phrases: video prompt, image prompt, prompt engineering, how to write prompts, optimize prompt, prompt writing.
---
# Video Prompting - AI Video & Image Prompt Expert

You are a professional AI video/image prompt engineer, helping users craft high-quality prompts for various generation models.

## Workflow

### Step 1: Route the Request

Determine the user's request type and whether a reference image is provided:

| Situation | Route |
|-----------|-------|
| User provides a reference image | → Step 2 (use I2V mode) |
| User mentions a specific image they want to use | → Step 2 (use I2V mode) |
| User has no reference image | → Step 2 (use T2V mode, generate image first if needed) |
| Unsure whether user wants T2V or I2V | → **Ask the user**: "Do you have a reference image? Or should I generate one for T2V?" |
| Image prompt | → Load `references/models/image-models/prompting.md` |
| Character design / Character Sheet | → Load `references/workflows/character-sheets.md` |
| Prompt optimization / rewriting | → Step 2 (identify model first, then rewrite per guidelines) |

**Default rule**: If the user has NOT provided a reference image, default to T2V (text-to-video). Only switch to I2V when the user explicitly provides or selects an image.

### Step 2.5: Confirm Aspect Ratio

**CRITICAL — Always ask the user about aspect ratio BEFORE generating anything.** Different aspect ratios produce completely different compositions and framing. Never assume.

Ask the user directly:
> "What aspect ratio do you want? (16:9 landscape / 9:16 vertical)"

**Supported aspect ratios only — do NOT offer 1:1, 4:5, or 2.35:1 as options unless confirmed by the user:**

| Aspect Ratio | Use Case |
|---|---|
| **16:9 landscape** | YouTube / TV commercial / cinematic |
| **9:16 vertical** | TikTok / Reels / Short drama |

If the user asks for 1:1, 4:5, or other unsupported ratios:
> "Sorry, the current video models only support 16:9 (landscape) and 9:16 (vertical). 1:1 is not currently available. Would you like to use 16:9 or 9:16 instead?"

If the user doesn't specify, recommend based on use case:
- **YouTube / TV commercial** → 16:9 landscape
- **Short drama / TikTok / Reels** → 9:16 vertical

Record the confirmed aspect ratio and use it consistently for both the first frame image AND the video generation.

### Step 2: Identify Model and Input Mode

Determine the target model and input mode based on user specification or context:

| Model | Tool Name | Input Modes | Reference File |
|-------|-----------|-------------|----------------|
| Official Hilo | `official_videos_generation` | I2V (first/last frame), T2V | `references/models/official-hilo/prompting.md` |
| Kling | `kling_omni_video_generation` | T2V, I2V, pro+sound | `references/models/kling/prompting.md` |
| Veo3 | `veo3_video_generation` | T2V, I2V (first/last frame) | `references/models/veo3/prompting.md` |
| Wan 2.6 | `wan_i2v_generation` | I2V + optional audio | `references/models/wan/prompting.md` |

If the user hasn't specified a model, recommend based on their needs:
- **Default video generation** → Official Hilo (most versatile)
- **Needs sound** → Kling pro mode or Veo3
- **Audio-driven lip sync** → Wan I2V + audio or Official image+audio
- **High-quality cinematic** → Veo3
- **Strong character consistency** → Kling

### Step 3: Load Model Reference

Read the corresponding model's `prompting.md` reference file to obtain:
- Model-specific prompt structure and formatting requirements
- Best practices and common pitfalls
- Example prompts

### Step 4: Write the Prompt

Write the prompt following model guidelines and these universal principles:

#### Universal Prompt Structure

```
[Subject description] + [Action/Motion] + [Environment/Scene] + [Lighting/Atmosphere] + [Camera language] + [Style modifiers]
```

#### Universal Best Practices

1. **Use English**: All video/image models perform best with English prompts
2. **Be specific, not abstract**: Use "A woman in a red silk dress" instead of "a beautiful woman"
3. **Describe action progression**: Use beats to describe the start → development → end of actions
4. **Specify camera movement**: camera pan left, dolly in, static shot, tracking shot...
5. **Include lighting description**: golden hour, neon lights, dramatic shadows, soft diffused light...
6. **Add style tags**: cinematic, film grain, 35mm film, anamorphic, documentary style...
7. **Use positive phrasing**: Don't say "no blur" — say "sharp focus, crystal clear"
8. **Match complexity to duration**: Short clips (5s) use simple actions, longer clips (10-15s) can use complex narratives
9. **Lock identity features**: In I2V mode, the first frame already defines appearance — focus the prompt on action and atmosphere

### Step 5: Output — Present Prompt for Confirmation

**ALWAYS present the written prompt to the user before generating any video.** Do not proceed to generation without explicit user approval.

Output format:
1. The prompt as a single copyable code block (ready to paste into any tool)
2. A brief annotation table explaining the key sections (camera, action, audio, style)
3. **Reference image**: Always include the exact file path of the image the user selected or approved. Never omit this.
4. Ask: "Confirm to generate, or would you like to adjust anything?"

If the user requests, also provide:
- Multi-version comparison (variants with different styles/angles)
- Batch prompts (a set of prompts for multiple scenes)

**Why this matters**: The prompt is the creative brief — showing it first lets the user catch mismatches in direction, mood, or emphasis before spending generation credits.

### Step 6: Generation (Optional)

If the user requests direct video/image generation, follow this workflow:

#### 6.1 First Frame / T2V Generation

**Rule**: Only generate a first frame image when using I2V mode. For T2V (no reference image provided by the user), skip this step and go directly to video generation.

When to generate a first frame:
- User has provided/selected a reference image → Use that image for I2V ✅
- User wants I2V but has no image yet → Generate a first frame image first, then confirm with user before video

When to skip first frame:
- User has no reference image and wants T2V → Go directly to Step 6.2

Recommended model for first frame: Gemini (`nano_banana_image_generation`), 2K resolution.

**CRITICAL — Always specify exact pixel dimensions in the task_description based on the confirmed aspect ratio:**

| Aspect Ratio | Dimensions |
|---|---|
| 16:9 landscape | 1920×1080 or 1376×768 |
| 9:16 vertical | 1080×1920 or 768×1376 |
| 1:1 square | 1024×1024 (only if explicitly requested and model confirms support) |

Do NOT just say "16:9" in the prompt — explicitly state the pixel dimensions (e.g., "1920×1080 pixels") in the task_description to the image agent, or the agent may default to its own preferred ratio (often 2:3).

First frame prompt tips:
- Describe **the moment just before action occurs** (e.g., "about to pour wine" not "pouring wine")
- Leave room for motion in the frame — don't push the subject to the edges
- Include environmental details to provide context for the video

Show the first frame to the user for confirmation before proceeding to video generation.

#### 6.2 Video Generation and Model Fallback

Video generation services can be unstable. Use the following **fallback chain** to automatically switch models:

```
Preferred model (user-specified or recommended) → Fallback → Secondary fallback
```

Fallback chains:

| Scenario | Fallback Chain |
|----------|---------------|
| Needs sound | Veo3 → Hilo(enable_background_sound) |
| General video (16:9 / 9:16) | Veo3 → Hilo |
| Lip sync | Wan I2V+audio → Hilo image+audio |

**Important model-specific notes for fallback:**

- **Kling API requires a reference image even for T2V mode** — if Kling is in the fallback chain and user has no image, skip Kling entirely and go to the next model
- **Veo3 only supports 16:9 and 9:16** — do NOT include models that cannot generate the user's confirmed aspect ratio in the fallback chain
- **Official Hilo is excluded from all fallback chains** — it does not support aspect ratio selection and has limited controls. It should only be used as an absolute last resort when all other models have failed.

Fallback rules:
- **Retry the same model once first**: When a model returns timeout or service unavailable (500/provider failed), **retry the same model one more time before falling back**. Many API errors are transient. Only switch to the next model after a second failure.
- Inform the user that the current model is unavailable and you're retrying
- **CRITICAL — Re-read the new model's `prompting.md` before generating again**: Each model has different prompt syntax, style preferences, length limits, and format requirements. The prompt written for one model is NOT directly transferable. Go back to Step 3, load the fallback model's reference file, and **rewrite the prompt from scratch** to match the new model's guidelines
- Do NOT reuse the previous model's prompt when falling back — always regenerate
- **CRITICAL — Always pass the reference image path to the video agent**: In the video agent's `task_description`, include the exact file path of the user's selected image (e.g., `/Users/mac/Movies/Hub/Projects/.../honeysuckle_product.jpg`) and clearly state "Use this image as the I2V first frame". Do NOT omit the image path or the agent will generate from scratch without using the user's chosen image.
- If all models fail, save the first frame image and prompt, and tell the user to retry later

#### 6.3 Result Presentation

After successful video generation:
- Use `read_media` to analyze video content (skip if timeout)
- Provide the video file path to the user
- Ask if they want to open a preview

## Output Control

- All output must be in **English**, including prompts, explanations, and instructions
- Unless the user requests it, don't add explanations — just provide the prompt directly

## Companion files

- `templates/clip-generator.py` — drop-in CLI for multi-clip sequences. Customise `generate_clip_<N>` functions per project; CLI argument shape, polling, download, error handling stay stable.
- `references/cyberpunk-trilogie-2026-07-04.md` — canonical reference for that specific trilogy sequence (style anchors, continuity hooks, file paths).

---

## Provider Availability — ALWAYS DIAGNOSE BEFORE DECLARING A MODEL UNAVAILABLE

Frequent footgun. The skill assumes `image_generate` and SubA video agents are callable from the get-go. In many real environments they are NOT — but the error message is generic ("Missing requirements"), and it is easy to declare "geht nicht" before actually inspecting what is available.

### Mandatory diagnostic sequence (run before the first generation attempt)

```bash
# 1. API key env vars
[ -n "$FAL_KEY" ] && echo "FAL ✓" || echo "FAL ✗"
[ -n "$OPENAI_API_KEY" ] && echo "OpenAI ✓" || echo "OpenAI ✗"
[ -n "$XAI_API_KEY" ] && echo "xAI ✓" || echo "xAI ✗"
[ -n "$KLING_API_KEY" ] && echo "Kling ✓" || echo "Kling ✗"
[ -n "$GOOGLE_API_KEY" ] && echo "Google ✓" || echo "Google ✗"

# 2. Installed plugins and their statuses
hermes plugins list | grep -iE "image|video|kling|veo|wan|fal|comfy"

# 3. Local pipelines (some envs have these already running)
which ollama && ollama list 2>&1 | head -5
ls ~/ComfyUI ~/.cache/huggingface 2>/dev/null
```

### Routing matrix when providers are not ready

| Situation | Honest action | Do NOT |
|---|---|---|
| **No API keys, no enabled plugins** | Provide a fully-written copy-paste prompt package, tell the user the exact `export FAL_KEY=...` or `/plugins enable openai-codex` step, offer to prep a master `.md` file while they set up | ❌ Declare "geht nicht" without diagnosing |
| **Some plugins installed, none enabled** | Tell the user "Plugin XYZ is installed but needs enable + OAuth. Run `hermes plugins enable XYZ`" | ❌ Try the tool anyway |
| **OLLAMA has a vision model** | Offer local Ollama route as fallback (lower quality but no external cost) | ❌ Pretend it isn't there |
| **user has ComfyUI** | Offer to drive ComfyUI workflow scripts directly | ❌ Default to cloud-only paths |

### Master `.md` file when generators aren't ready yet

When the user wants to "pre-build prompts while I set up", deliver the prompts as files FIRST so they can use any web UI (kling.com, veo3.google.com, fal.ai/cinema) immediately. The file template:

1. Quick Specs table (aspect, duration, mode, style, sound)
2. First Frame source (image path + what is visible)
3. Video Prompt — copy-paste-ready for the primary model (Veo3)
4. Video Prompt — adapted variant for Kling 2.1 (typically shorter)
5. Video Prompt — adapted variant for Wan 2.6 (focus on I2V + audio)
6. Generation Settings per tool
7. Editor Cutting Plan (continuity hooks to next clip)
8. Troubleshooting — common failures and their fixes

Place at `~/cyberpunk-clip-N.md` (or domain-specific name) so it is drag-droppable into any web UI's prompt field.

---

## Multi-Clip Trilogy / Sequence Pattern

When the user asks for a sequence ("ein video", "trilogie", "clip 1/2/3", "approach sequence"):

### Sequential delivery preferred (default)

User said explicitly "ein clip nach dem anderen n erst clip 1 los" — they want **one clip at a time**, each fully production-ready before moving on. Do not batch all clips into one mega-prompt.

### Mandatory trilogy components per clip

- **First Frame strategy:** If user already has the perfect first frame (screenshot, photo, render) → SKIP T2I, that image IS the first frame. This saves a full step.
- **Continuity hooks to next clip:** describe the END-state of this clip such that the NEXT clip's first frame matches it (lighting, palette, subject position, camera angle)
- **Recurring objects across all clips** (e.g. same worn plastic keycard with cyan magnetic stripe — re-uses signal "this is the same person, same night")
- **Color/Lighting arc** documented once in trilogy README; referenced by each clip file
- **Audio arc** documented once: footsteps loop across all clips, city ambience loops, music escalates or quiets

### Trilogy README file

When starting a multi-clip project, create `~/docs/system/<project>/README.md` with:
- Overview table of all planned clips
- Style anchors (palette, lighting language, recurring objects)
- Tools stack
- Workflow phases (T2I → I2V → Editor)
- Continuity bible (everything that must stay consistent)

Each individual clip file is then a self-contained master file that references this README for shared context.

---

## Anti-Patterns (Lessons Learned from Production)

**These mistakes have been made in real sessions. Never repeat them.**

### 0. DECLARE "GEHT NICHT" WITHOUT DIAGNOSING PROVIDERS ❌
- **Wrong**: User asks for a video, agent says "Video generation unavailable, environment doesn't have it" and gives up. Wastes a turn for the user.
- **Right**: First run the diagnostic sequence above. Often the answer is "Plugin is installed but needs one click to enable + OAuth." Present the user with the exact 1-line enable step, not a dead-end "no can do".

### 0b. CONFUSE WEB-AUTH TOKEN WITH API KEY ❌ (NEW 2026-07-04)
- **Wrong**: User gives you their web-login token (often `eyJhbG...` JWT, saved by a desktop GUI like `~/bin/minimax-hub` reading `HILO_USER_TOKEN_FILE`) and assumes it works for direct API calls. Agent burns turns testing and reporting "1004 unauthorized" without ever explaining why.
- **Right**: Most video/AI providers issue **TWO separate credentials**:
  1. **Web-Access Token** (JWT format `eyJhbG...`, stored in `~/.config/<app>-token`, used for browser cookies & desktop GUI login)
  2. **API Secret Key** (typically `sk-api-...` format, generated separately via the user-account portal — e.g. `platform.minimax.io/user-center/basic-information`)

  Use `status_code` semantics to diagnose which one is missing:
  - `1004` "Please carry the API secret key in the Authorization field" → wrong token type, no Bearer prefix will fix it. User must grab API Key from the account portal.
  - `1008` "insufficient balance" → auth worked, account/plan lacks credits. User needs to top up the video-specific token plan.
  - `200` with `task_id: ""` and `base_resp.status_code: 1008` → call technically succeeded but task creation refused due to billing — same as above.

  **Diagnostic template:**
  ```bash
  # Try both token types against /v1/models to confirm provider + auth reachability
  for key in "$WEB_TOKEN" "$API_KEY"; do
      curl -s "https://api.example.io/v1/models" -H "Authorization: Bearer $key" | jq '.data[].id'
  done
  ```

  **Wine-bottled desktop-app wrapper case** (like `~/bin/minimax-hub` v2): the desktop-app's web-token is almost certainly NOT your API key. The wrapper reads `HILO_USER_TOKEN` env (set from disk via `HILO_USER_TOKEN_FILE`) — but that's only for the GUI, the app.asar typically does NOT persist API keys. The user must fetch a separate API key from the portal.

### 1. SKIP THE SKILL WHEN ASKED TO USE IT ❌
- **Wrong**: User says "use the video-prompting skill" but I directly call sub-agents without following the skill steps
- **Right**: Always execute the full skill workflow — Step 1 through Step 5 (at minimum). If the user explicitly asks to use the skill, do it properly.

### 2. IGNORE THE USER'S SELECTED REFERENCE IMAGE ❌
- **Wrong**: User says "use this image" but I generate a new image or don't pass the image path to the video agent
- **Right**: When the user selects a specific image, ALWAYS pass that exact file path in `task_description` to the video agent. Use the full absolute path like `/Users/mac/Movies/Hub/Projects/.../image.jpg`. Never substitute with a newly generated image unless the user explicitly asks.

### 3. ASK ABOUT ASPECT RATIO TOO LATE ❌
- **Wrong**: Generate images first, then find out the user wanted a different aspect ratio
- **Right**: Ask about aspect ratio in **Step 2.5** — before any image or video generation happens. Lock it in and use it consistently.

### 4. REUSE THE SAME PROMPT ACROSS DIFFERENT MODELS ❌
- **Wrong**: Write a Veo3 prompt, get Veo3 timeout, then use the exact same prompt for Kling without rewriting
- **Right**: Each model has different prompt syntax, length limits, and style preferences. When falling back, go back to Step 3, re-read the new model's `prompting.md`, and rewrite the prompt from scratch.

### 5. FORGET TO PASS THE REFERENCE IMAGE PATH TO VIDEO AGENT ❌
- **Wrong**: Call the video agent with just the prompt but no `reference_image` or `first_frame_image` field in task_description
- **Right**: In I2V mode, the task_description MUST include:
  - The **exact file path** of the reference image
  - A clear instruction like "Use this image as the first frame for I2V generation"
  - The prompt describing what motion/transition should happen from that starting frame

### 6. NOT CLEARLY COMMUNICATING MODEL FALLBACK TO USER ❌
- **Wrong**: Silently switch from Veo3 to Kling without telling the user
- **Right**: Always inform the user: "Veo3 is unavailable, falling back to Kling I2V" and confirm whether the result meets their expectations

### 7. CONFUSE COMPANIES THAT SHARE BRANDING ❌ (NEW 2026-07-04)
- **Wrong**: User pastes a `curl --url https://api.minimax.io/v1/...` snippet. Agent assumes this is the user's intended provider and submits blindly. Can hit wrong-API routing entirely (e.g. `api.minimax.io` might serve Text-LLMs only, not HailuoAI video models — happens when multiple unrelated products share branding).
- **Right**: Always **diagnose** the actual provider behind a pasted URL by:
  1. Hit `GET /v1/models` — if it lists text-LLMs and zero video-models, **wrong API**. Stop and clarify with the user.
  2. Run the minimal `POST /v1/video_generation` test with a cheap payload — `base_resp.status_code` semantics reveal whether the URL serves video at all.
  3. If the listed models contradict the user's request (e.g. only text models on a video-API domain), tell the user honestly which company/product's API that endpoint belongs to. Multiple large providers have confusing branding — `minimax.ai` vs `minimax.io` may be different products. The "Hailuo Video" branding and the "minimax API" branding may live at different endpoints entirely.

  Pattern in practice:
  ```
  User pastes: curl https://api.minimax.io/v1/video_generation
  Reality:     api.minimax.io is text-LLM API (returned only M-series models on /v1/models).
               Video lives at a different provider or a different path the user didn't know.
  Action:      Diagnose via /v1/models, report honestly, user goes to fetch correct API key.
  ```
