---
type: Skill
name: design-image-generation
description: Generate images using AI models — Gemini, DALL·E, Stable Diffusion, Midjourney, Flux, Leonardo, Ideogram, and more. MCP bridge tools are primary; the Design Stack media worker is the fallback for advanced providers. Covers prompt engineering, model selection, size/aspect ratios, style parameters, batch generation, multi-site awareness, and WordPress integration. Use when you need to create hero images, social graphics, product mockups, brand illustrations, or any visual asset for marketing, social media, or e-commerce.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# AI Image Generation

Use this skill when creating AI-generated images for design projects, social media, brand assets, or content marketing.

## MCP Tool Discovery

The mcp-ai-wpoos plugin may register tools under **agent-specific prefixes** or
as bare names, depending on how the WordPress assistant was configured:

```
Pattern: nv_oos_{AGENT_NAME}_agent_{TOOL_NAME}
Example: nv_oos_sophie_agent_generate_gemini_image_validated
         nv_oos_local_agent_generate_gemini_image_validated
         generate_gemini_image_validated  (bare — may not be registered)
```

**Before using any tool, check what's available in your tool list.** The agent
name varies per installation — Sophie, Local, or any custom name configured in
WordPress. If bare tool names are registered, use those. Otherwise use the
agent-prefixed variant.

**When an MCP tool covers your task, use it directly.** The Design Stack media
worker (`http://localhost:3100`) is a fallback only for providers not yet
available through MCP (Midjourney, Flux, Leonardo, Ideogram, Stable Diffusion,
etc.).

### Key MCP tools (names vary by agent prefix)

| Function | Tool Name Pattern | What it does |
|---|---|---|
| Gemini image gen | `nv_oos_*_agent_generate_gemini_image_validated` or bare `generate_gemini_image_validated` | Generate images with Gemini |
| OpenAI/DALL·E image gen | `generate_openai_image` | Generate images with DALL·E 3 / GPT image models |
| DALL·E variations | `create_image_variation` | Create DALL·E 2 variations of an existing image |
| DALL·E editing | `edit_openai_image` | Edit images with DALL·E 2 (inpainting) |
| Image resize | `resize_image` | Resize images to specific dimensions |
| Background removal | `remove_background` | Make image backgrounds transparent |
| Alt text generation | `generate_image_alt_text_validated` | Generate accessible alt text |
| Image analysis | `analyze_image` | AI vision analysis of images |
| Web search | `nv_oos_*_agent_web_search_validated` | Research visual references before generating |
| Remote site ops | `remote_wp_connection` | List/manage connected spoke sites |

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for generation troubleshooting. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai provider` | List configured AI providers (Gemini, OpenAI, etc.) |
| `wp mcp-ai health` | Check provider connectivity and tool registration |
| `wp mcp-ai cache clear` | Clear provider caches after configuration changes |
| `wp mcp-ai credential` | Manage API keys for image generation providers |

## When to use this skill

Trigger when ANY of the following is true:

- The task asks to "generate an image", "create a visual", or "make a graphic".
- The user needs hero images, social graphics, product mockups, or brand illustrations.
- Selecting the right model/provider for a specific visual task.
- The task mentions AI image generation with any provider.

## Generating images via MCP (Primary)

### Gemini (recommended default)

Use the Gemini image generation tool available in your tool list (agent-prefixed
or bare). It's fast, produces high-quality images, and requires no external API
setup beyond the WordPress plugin configuration.

```
Parameters (consistent across all variants):
  prompt       — Text description of the desired image
  model        — "gemini-3.1-flash-image" (default, fast) or "gemini-3-pro-image" (premium)
  aspect_ratio — "auto", "1:1", "3:4", "4:3", "9:16", "16:9"
  mime_type    — "image/png" (default), "image/jpeg", "image/webp"
  file_name    — Optional base name for the saved attachment
  output_format — "default" (raster) or "svg" (vectorized)
  timeout      — Override request timeout in seconds (5–300)
```

**Example prompt:** "A cozy coffee shop interior with morning sunlight streaming through large windows, warm wood tones, photorealistic, 4:3 aspect ratio"

The generated image is automatically saved to the WordPress Media Library as an attachment.

### DALL·E variations

Use `create_image_variation` to generate alternative versions of an existing image in your Media Library:

```
Parameters:
  image_id       — WordPress attachment ID of the source image
  model          — "dall-e-2" (only option)
  n              — Number of variations (1–10, default 1)
  size           — "256x256", "512x512", "1024x1024"
  output_format  — "default" (raster) or "svg"
```

### DALL·E image editing (inpainting)

Use `edit_openai_image` to edit parts of an image:

```
Parameters:
  image_id          — WordPress attachment ID of the image to edit
  prompt            — Description of the desired edits
  mask_id           — Optional mask image (transparent areas get edited)
  request_user_mask — Set true to have the user paint a mask in chat
  model             — "dall-e-2"
  n                 — Number of results (1–10)
  size              — "256x256", "512x512", "1024x1024"
```

## Provider comparison (full ecosystem)

### Quality & Style

| Provider | Access | Best For | Style |
|---|---|---|---|
| **Gemini** | ✅ **MCP** | Fast creative images, text+image output | Native multimodal |
| **DALL·E 3** | ⚠️ Media Worker | Marketing graphics, realistic scenes | Natural language, photorealism |
| **DALL·E 2** | ✅ **MCP** (variations/edit) | Variations, inpainting | Basic edits |
| **Midjourney v6** | ⚠️ Media Worker | Artistic, moody, cinematic | Best aesthetics |
| **Flux (Replicate)** | ⚠️ Media Worker | Photorealistic, high-quality renders | State-of-the-art detail |
| **Leonardo XL** | ⚠️ Media Worker | Game assets, character design | Flexible presets |
| **Firefly v3** | ⚠️ Media Worker | Commercial-safe, brand-compatible | Adobe ecosystem |
| **Ideogram v2** | ⚠️ Media Worker | Text-in-image, logo concepts | Best text rendering |
| **Stable Diffusion XL** | ⚠️ Media Worker | Artistic styles, custom fine-tuning | Open-source |
| **SD3 / SD3 Turbo** | ⚠️ Media Worker | Fast generation, latest quality | Stability's newest |
| **Getimg.ai** | ⚠️ Media Worker | SDXL with fine-tuned models | Realistic Vision, Dreamshaper |
| **Clipdrop** | ⚠️ Media Worker | Quick one-off images | Simple API |
| **DeepAI** | ⚠️ Media Worker | Budget-friendly, niche styles | Fantasy, cyberpunk |

✅ = Available via MCP bridge   ⚠️ = Requires media worker fallback

### Speed & Cost

| Provider | Speed | Free Tier | Paid Starts At |
|---|---|---|---|
| **Gemini** | 5–15s | Generous free tier | Pay-as-you-go |
| **DALL·E 3** | 10–30s | None | $0.040/image (1024) |
| **Midjourney** | 30–90s | None | $10/mo (200 fast hours) |
| **Flux Schnell** | 2–5s | None | $0.003/image (Replicate) |
| **SD3 Turbo** | 2–5s | 25 credits | Pay-as-you-go |
| **Leonardo** | 5–15s | 150 credits/day | $12/mo |
| **Ideogram** | 5–15s | 25/day (slow) | $7/mo |
| **Getimg.ai** | 3–10s | 100/month | $12/mo |
| **Firefly** | 10–20s | 25/month | $5/mo |

## Media worker fallback

For providers not covered by MCP tools, use the media worker API at `http://localhost:3100`:

### DALL·E (OpenAI)
```
POST /api/image/generate
{ "model": "dall-e-3", "prompt": "...", "size": "1024x1024", "style": "vivid" }
```
- **Requires**: `OPENAI_API_KEY`
- **Models**: `dall-e-3`, `dall-e-2`
- **Sizes**: `1024x1024`, `1792x1024`, `1024x1792`
- **Style**: `natural` or `vivid`
- **DALL·E 3 cannot create variations or edits** — use DALL·E 2 for those (available via MCP)

### Midjourney
```
POST /api/image/generate
{ "provider": "midjourney", "model": "midjourney-v6", "prompt": "...", "aspect_ratio": "16:9" }
```
- **Requires**: `MIDJOURNEY_API_KEY`
- **Models**: `midjourney-v6`, `midjourney-v6.1`, `midjourney-v5.2`, `niji-v6`
- Use parameters: `--ar 16:9 --style raw --v 6.1`

### Stable Diffusion (Stability AI)
```
POST /api/image/generate
{ "provider": "stability", "model": "sd3", "prompt": "...", "negative_prompt": "ugly, blurry" }
```
- **Requires**: `STABILITY_API_KEY`
- **Models**: `sd3`, `sd3-turbo`, `stable-diffusion-xl`
- Keywords with commas: `cinematic lighting, 8k, highly detailed`
- Negative prompts: `ugly, deformed, blurry, low quality`

### Flux / SDXL / Kandinsky (Replicate)
```
POST /api/image/generate
{ "provider": "replicate", "model": "flux-schnell", "prompt": "..." }
```
- **Requires**: `REPLICATE_API_KEY`
- **Models**: `flux-schnell`, `flux-pro`, `flux-dev`, `sdxl`, `playground-v2.5`, `kandinsky-3`

### Other providers

| Provider | API Key Env Var | Models |
|---|---|---|
| **Leonardo** | `LEONARDO_API_KEY` | `leonardo-xl`, `leonardo-vision`, `leonardo-phoenix` |
| **Ideogram** | `IDEOGRAM_API_KEY` | `ideogram-v2`, `ideogram-v1`, `ideogram-v1-turbo` |
| **Getimg.ai** | `GETIMG_API_KEY` | `realistic-vision`, `dreamshaper`, `juggernaut-xl`, `flux-schnell` |
| **Firefly** | `FIREFLY_CLIENT_ID` + `FIREFLY_CLIENT_SECRET` | `firefly-v3` |
| **DeepAI** | `DEEPAI_API_KEY` | `deepai-text2img` |
| **Clipdrop** | `STABILITY_API_KEY` (shared) | `clipdrop-sdxl` |

### Listing available providers
```bash
GET http://localhost:3100/api/image/providers
```
Returns which providers are configured and their available models.

## Prompt engineering

### Structure
```
[Subject] + [Style/Medium] + [Lighting] + [Composition] + [Quality boosters]
```

### Platform-specific dimensions

| Platform | Aspect | Prompt Style |
|---|---|---|
| **Instagram feed** | 1:1 | Product-focused, clean background |
| **Instagram story** | 9:16 | Vertical, space for text overlay |
| **Twitter/X** | 16:9 | Horizontal, bold, shareable |
| **LinkedIn** | 1.91:1 | Professional, clean |
| **Pinterest** | 2:3 | Vertical, inspirational |

### Gemini specific (MCP primary)

- Be explicit: "Generate an image of..."
- Describe visual style clearly: "photorealistic", "vector illustration", "watercolor"
- Works well with structured descriptions including colors, materials, lighting
- The generated image is auto-saved to the WordPress Media Library
- Use `output_format: "svg"` to vectorize the result for logos/icons

### DALL·E specific (media worker)

- Natural language works best
- Use `style: vivid` for saturated, dramatic results
- Text rendering is strong — can generate images with legible words

### Stable Diffusion specific (media worker)

- Keywords with commas: `cinematic lighting, 8k, highly detailed, trending on artstation`
- Negative prompts: `ugly, deformed, blurry, low quality, watermark, text, bad anatomy`
- CFG scale: 7–9

### Midjourney specific (media worker)

- Use parameters: `--ar 16:9 --style raw --v 6.1`
- Quality: `--q 2` (max), `--q 0.5` (fast)
- Creative: `--weird 500` or `--stylize 1000`

## Multi-Site: Generating for spoke sites

When working with multiple WordPress sites (Hub + spokes), use
`remote_wp_connection` to discover which spoke sites are connected and
available before generating images for them:

```
1. Discover connections:
   remote_wp_connection { action: "list_connections" }
   → Returns: [{ id: "conn_8srcad8zylhe", name: "Parfumerie Website", url: "..." }]

2. Verify site is active and has media:
   remote_wp_connection { connection_id: "conn_8srcad8zylhe", action: "get_media", per_page: 3 }

3. Generate images using your available Gemini tool (agent-prefixed or bare) —
   saved to the current site's Media Library. For cross-site generation, create
   the image on the Hub and then push to the spoke via remote_wp_connection
   create_post with the attachment URL.

4. (Future Gateway feature): Direct cross-site tool calls via site prefix:
   parfum::generate_gemini_image_validated { prompt: "..." }
```

## Research-First Generation

Use the web search tool available in your tool list (e.g.,
`nv_oos_*_agent_web_search_validated`) to find reference images and style
inspiration before generating. This dramatically improves prompt quality:

```
1. Search for visual references:
   web_search { query: "minimalist coffee shop interior design 2026 trends" }

2. Use search results to enrich your prompt with real-world details

3. Generate with the Gemini tool available in your tool list
```

## WordPress integration

Generated images are automatically saved to the WordPress Media Library via MCP tools. The attachment ID is returned and can be used immediately for featured images, post content, or social sharing.

```php
// Example: using a generated image as a featured image
$attachment_id = /* result from Gemini image generation */;
set_post_thumbnail( $post_id, $attachment_id );
update_post_meta( $attachment_id, '_ai_prompt', $prompt );
update_post_meta( $attachment_id, '_ai_model', $model );
```

## Common Mistakes

```
WRONG:
  ● Using generate_gemini_image_validated without first checking your tool list for the correct agent-prefixed name
  ● Generating images at full resolution without resizing — uploads 4096px images to WordPress with no optimization
  ● Using "make it look good" as a prompt instead of structured [Subject]+[Style]+[Lighting]+[Composition] descriptions
  ● Skipping provider comparison — using DALL·E for photorealism when Flux would produce better results at lower cost
  ● Generating images without checking existing Media Library — duplicates assets already available
  ● Forgetting to verify spoke site connectivity via remote_wp_connection before attempting cross-site image generation

RIGHT:
  ✅ Search your tool list for "generate_gemini" to find the correct agent-prefixed tool name before generating
  ✅ Always follow generation with design-image-optimization — resize to target dimensions, convert to WebP
  ✅ Use structured prompts: "Product photography of [item], [lighting], [background], [style], luxury catalog"
  ✅ Match provider to purpose: Gemini for fast creative, Flux for photorealism, Ideogram for text-in-image
  ✅ Run semantic_content_search or search_attachments first to check for existing usable assets
  ✅ Call remote_wp_connection { action: "list_connections" } before any cross-site image operations
```

## Critical rules

- **Check your available tools first** — tool names vary by agent configuration. Search your tool list for `generate_gemini_image` or `web_search` to find the correct names.
- **MCP first, media worker second** — always check if an MCP tool exists before reaching for the media worker.
- **Always optimize after generation** — use `resize_image` (MCP) or the media worker to convert raw AI images to WebP.
- **Store prompts as metadata** — for reproducibility and attribution.
- **Respect rate limits** — Gemini: generous free tier; DALL·E 3: 5/min (Tier 1); Midjourney: 3 concurrent.
- **Auto-detect provider from model name** — when using the media worker, just pass `model`, the worker finds the right provider.
- **Firefly is commercial-safe** — trained on licensed Adobe Stock; ideal for client work.
- **Ideogram for text** — if your image needs legible text, use Ideogram or DALL·E 3 via media worker.
- **Flux for photorealism** — best quality-to-speed ratio via media worker.
- **Verify spoke sites before cross-site ops** — use `remote_wp_connection` to list connections and test connectivity before targeting remote sites.
- **Research before prompting** — use the web search tool available in your tool list to gather visual references for more accurate prompts.

## What This Skill Does NOT Cover

- **Image optimization** — use `design-image-optimization` for resizing, format conversion (WebP/AVIF), compression, and alt text generation.
- **Product photography standards** — use `design-product-photography` for e-commerce shot types, composition rules, and catalog consistency.
- **Video creation** — use `design-video-creation` for AI video generation (Sora, Veo, Runway) and FFmpeg processing.
- **Social media publishing** — use `design-social-publishing` to schedule and post generated images to social platforms.
- **Brand identity design** — use `design-brand-kit` for logos, color palettes, and typography that should guide image styling.
- **OCR and text extraction** — use `extract_image_text` or `design-document-generation` for extracting text from images.

## Cross-references

- Run **`design-image-optimization`** after generation — use `resize_image` (MCP) to optimize.
- Run **`design-social-content`** to generate captions matching visuals.
- Run **`design-brand-kit`** for consistent visual identity.
- Run **`design-media-workflow`** for pipeline automation including cross-site pipelines.
- Run **`mcp-ai-wpoos-plugin`** for `remote_wp_connection` documentation and multi-site architecture.
- Use **`generate_design_ai`** as an alternative generation path through the Design Stack unified pipeline.

## References

- Gemini image generation: <https://ai.google.dev/gemini-api/docs/imagen>
- OpenAI DALL·E: <https://platform.openai.com/docs/guides/images>
- Stability AI: <https://platform.stability.ai/docs/api-reference>
- Replicate: <https://replicate.com/collections/text-to-image>
- Leonardo.ai: <https://docs.leonardo.ai/reference>
- Ideogram: <https://ideogram.ai/api>
- Getimg.ai: <https://docs.getimg.ai/reference>
- Adobe Firefly: <https://developer.adobe.com/firefly-api/docs/api/>
