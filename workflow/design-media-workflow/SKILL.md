---
type: Skill
name: design-media-workflow
description: End-to-end media pipeline automation — from AI generation through optimization to social publishing. Covers workflow design, WordPress integration, Redis job queuing, batch processing, multi-site pipelines, and orchestration. MCP bridge tools are the primary interface for individual operations; the Design Stack media worker handles batch and advanced processing. Use when you need to automate image generation→optimization→publishing chains, set up cross-site media sync, design batch processing pipelines, or orchestrate multi-step media workflows triggered by post publish or cron.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Media Workflow Automation

Use this skill when designing or implementing automated pipelines that generate, process, and publish media assets at scale — including across multiple WordPress sites.

## MCP Tool Discovery

The mcp-ai-wpoos plugin registers tools under **agent-specific prefixes** or
as bare names. Always check what's available in your tool list before building
a pipeline:

```
Pattern: nv_oos_{AGENT_NAME}_agent_{TOOL_NAME}
Examples (agent name varies per installation):
  nv_oos_sophie_agent_generate_gemini_image_validated
  nv_oos_local_agent_web_search_validated
  generate_gemini_image_validated  (bare — may not be registered)
```

| Workflow Step | Tool Name Pattern | Media Worker Fallback |
|---|---|---|
| Image generation | `nv_oos_*_agent_generate_gemini_image_validated` or bare | `/api/image/generate` (DALL·E, Midjourney, etc.) |
| Web search (research) | `nv_oos_*_agent_web_search_validated` | — |
| Content search | `nv_oos_*_agent_search_content_validated` | — |
| Image editing | `create_image_variation`, `edit_openai_image` | — |
| Image resize | `resize_image` | `/api/image/optimize` (batch, format conversion) |
| Background removal | `remove_background` | — |
| Alt text / captions | `generate_image_alt_text_validated`, `generate_image_caption_validated` | — |
| Video frame extraction | `extract_video_frames` | — |
| Video processing | — | `/api/video/process` (FFmpeg) |
| Page crawling | `run_crawl4ai_job` (remote mode) | `/api/crawl/markdown`, `/api/crawl/markdown-batch`, `/api/crawl/links` (worker v3.2.0+) |
| Crawl4AI extraction | `run_crawl4ai_job` | `/api/crawl4ai/*` (Crawl4AI-compatible facade, worker v3.2.0+) |
| Social publishing | `schedule_social_post` | `/api/social/post` |
| WordPress post CRUD | `create_post`, `save_post` | — |
| JetEngine CCT operations | `jetengine` (direct CRUD) | `remote_wp_connection` (CCT via REST) |
| Remote site management | `remote_wp_connection` | — |
| Cross-site entity sync | Graphify `graphify_sync_remote_source` (via `addons/graphify/`) | — |
| Browse template library | `browse_template_library` | — |
| Apply template to image | `apply_template` | — |
| Create media collection | `create_media_collection` | — |
| Add to collection | `add_to_collection` | — |
| Bulk tag media | `bulk_tag_media` | — |
| Sync media to remote | `sync_media_to_remote` | — |
| Import media from URL | `import_media_from_url` | — |

### Tool Rate Limits & Reliability (agent workflows)

- The server rate-limits tool executions (oOS → Security → **Tool Rate
  Limiting**: default 300 calls/min window, `tool_rate_limit_exempt_tokens`
  defaults to ON for credential-token/agent traffic) and general API requests
  (`rate_limit_requests` — use 1000 for agent sites).
- On servers **older than v1.1.55**, tool errors were returned as HTTP 500
  and some MCP SDKs silently dropped them — tool calls looked like they
  returned nothing. On v1.1.55+ JSON-RPC errors always reach the agent.
- Network-dependent tools (`remote_wp_connection`, `ezuite_erp`) can run
  through the async job queue; on v1.1.55+ the MCP wait is bounded to ~45s
  and returns a visible timeout error instead of hanging.
- Batch-heavy pipelines (bulk_tag, collections, multi-site sync) should
  prefer the media worker / Redis queue for volume, and treat each MCP tool
  call as one rate-limit unit.
- Connection details and full troubleshooting:
  `.agents/skills/mcp-ai-wpoos-plugin/SKILL.md` (transports, mcp-remote
  bridge, rate limits).

## WP-CLI Commands

The mcp-ai-wpoos plugin registers these WP-CLI commands useful for design workflows. Run via the `terminal` tool inside the WordPress container (`docker compose exec wordpress wp ...`).

### Core

| Command | Use for |
|---|---|
| `wp mcp-ai` | Plugin status, CCT cleanup, remote connection management |
| `wp mcp-ai cron` | Inspect and manage scheduled cron events |
| `wp mcp-ai queue` | View/process/retry background job queues |
| `wp mcp-ai bulk` | Bulk operations (posts, media, taxonomy) |
| `wp mcp-ai content` | Content search, generation, and management |
| `wp mcp-ai health` | System health check — providers, tools, connectivity |
| `wp mcp-ai cache clear` | Clear plugin caches |
| `wp mcp-ai provider` | List/test configured AI providers |
| `wp mcp-ai log` | View execution logs and error traces |
| `wp mcp-ai memory` | Manage agent memory and context storage |
| `wp mcp-ai credential` | Manage API keys and credentials |
| `wp mcp-ai token` | Migrate provider authentication tokens |
| `wp mcp-ai rabbitmq` | Manage RabbitMQ message queues |
| `wp mcp-ai harness` | Semantic search and tracing |
| `wp mcp-ai assistant` | Create/list/manage AI assistants |
| `wp mcp-ai chat` | Send chat messages to assistants |
| `wp mcp-ai approval` | Manage approval workflows |
| `wp mcp-ai version` | Plugin and dependency versions |

### Pro (vendor integrations)

| Command | Use for |
|---|---|
| `wp ezuite status` | EZuite ERP connection status |
| `wp ezuite trigger` | Trigger ERP data sync |
| `wp ezuite low-stock-report` | Low stock inventory report |
| `wp shopify-sync status` | Shopify sync status |
| `wp shopify-sync trigger` | Trigger Shopify sync |
| `wp shopify-sync cost-report` | Shopify API cost report |

All commands support `--help` for subcommand details.

## When to use this skill

Trigger when ANY of the following is true:

- Building an automated content pipeline.
- Batch processing images or videos.
- Setting up webhook-triggered media workflows.
- Connecting AI generation → optimization → publishing.
- The task mentions "pipeline", "automation", "batch processing", or "workflow".
- Integrating multiple Design Stack services together.
- Syncing media between the Hub and spoke sites.

## Architecture overview

```
                    ┌──────────────────┐
                    │    MCP Bridge     │
                    │ (agent-prefixed)  │
                    └────────┬─────────┘
                             │ tool calls
                             ▼
┌──────────────────────────────────────────────────────────┐
│                    WordPress Plugin (Hub)                 │
│                                                          │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Generate  │→ │   Optimize   │→ │    Publish       │  │
│  │ (Gemini)   │  │ (resize/bg)  │  │ (schedule_social)│  │
│  └────────────┘  └──────────────┘  └──────────────────┘  │
│                                                          │
│  ┌────────────────── Multi-Site Layer ──────────────┐    │
│  │  remote_wp_connection → Spoke A (Docker/local)    │    │
│  │  remote_wp_connection → Spoke B (external host)   │    │
│  │  Graphify oos_federation → cross-site entity sync │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │            Media Worker (Fallback)                │    │
│  │  ┌──────────┐ ┌──────────┐ ┌─────────────────┐  │    │
│  │  │DALL·E/   │ │Sharp     │ │Social API       │  │    │
│  │  │Midjourney│ │(WebP/AVIF│ │(direct post)    │  │    │
│  │  └──────────┘ └──────────┘ └─────────────────┘  │    │
│  │  ┌──────────────────────────────────────────┐   │    │
│  │  │         Redis Job Queue                   │   │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

## Workflow patterns

### Pattern 1: Blog post → Social media package

```
Trigger: WordPress post published on Hub
    │
    ├─ 1. Research trending visuals → web search tool in your tool list
    ├─ 2. Generate featured image → Gemini tool in your tool list
    ├─ 3. Resize for each platform → resize_image (MCP)
    │     ├─ 1200×630 (Twitter/LinkedIn link preview)
    │     ├─ 1080×1080 (Instagram feed)
    │     └─ 1080×1920 (Instagram story)
    ├─ 4. Generate alt text → generate_image_alt_text_validated (MCP)
    ├─ 5. Set as featured image → WordPress set_post_thumbnail()
    ├─ 6. Schedule social posts → schedule_social_post (MCP)
    │     ├─ platforms: ["twitter", "linkedin", "facebook"]
    │     └─ scheduled_time: "optimal"
    └─ 7. Log results to WordPress post meta
```

### Pattern 2: Batch brand asset generation (mixed)

```
Trigger: Manual or scheduled (content calendar)
    │
    ├─ 1. Generate N logo concepts via Gemini (MCP, parallel calls)
    ├─ 2. For each concept:
    │   ├─ Remove background → remove_background (MCP) if needed
    │   ├─ Resize to favicon → resize_image (MCP): 32×32
    │   ├─ Resize to social avatar → resize_image (MCP): 400×400
    │   └─ Convert to WebP → /api/image/optimize (media worker)
    ├─ 3. Package into "Brand Kit" zip
    └─ 4. Upload to WordPress media library with metadata
```

### Pattern 3: Video production pipeline (mixed)

```
Trigger: Upload raw video to WordPress
    │
    ├─ 1. Extract thumbnail → extract_video_frames (MCP)
    │     save_to_media: true, timestamps: [0.5]
    ├─ 2. Optimize poster image → resize_image (MCP)
    ├─ 3. Compress for web → /api/video/process (media worker)
    ├─ 4. Create social cuts → /api/video/process (media worker):
    │   ├─ 1:1 square (Instagram feed)
    │   ├─ 9:16 vertical (Reels/TikTok)
    │   └─ 16:9 horizontal (YouTube/LinkedIn)
    ├─ 5. Create GIF preview → /api/video/process (media worker, "gif")
    ├─ 6. Schedule social posts → schedule_social_post (MCP)
    └─ 7. Upload all variants to WordPress media library
```

### Pattern 4: Cross-Site Media Sync (Multi-Site)

```
Trigger: New product added to a spoke site (e.g., Parfumerie)
    │
    ├─ 1. Discover spoke → remote_wp_connection { action: "list_connections" }
    ├─ 2. Pull product media → remote_wp_connection {
    │     connection_id: "conn_8srcad8zylhe",
    │     action: "get_wc_products", per_page: 5 }
    ├─ 3. Download product images → wp_remote_get( product.image_url )
    ├─ 4. Optimize for Hub → resize_image (MCP) — resize to Hub's dimensions
    ├─ 5. Generate alt text → generate_image_alt_text_validated (MCP)
    ├─ 6. Upload to Hub media library → wp_insert_attachment()
    └─ 7. (Future) Graphify federation → sync cross-site knowledge graph
```

### Pattern 5: Hub → Spoke Brand Push (Multi-Site)

```
Trigger: Brand assets updated on Hub
    │
    ├─ 1. Detect updated logo/colors → WordPress post meta change
    ├─ 2. List connected sites → remote_wp_connection { action: "list_connections" }
    ├─ 3. For each spoke with WooCommerce (e.g., Parfumerie, Myyco):
    │   ├─ Push logo → remote_wp_connection { action: "create_post", ... }
    │   ├─ Push brand colors → remote_wp_connection (via post meta)
    │   └─ Log result per site
    └─ 4. Verify consistency → remote_wp_connection get_posts on each spoke
```

## WordPress integration

### Webhook trigger on post publish

```php
add_action( 'transition_post_status', function ( $new, $old, $post ) {
    if ( 'publish' !== $new || 'publish' === $old ) return;
    if ( 'post' !== $post->post_type ) return;

    // The AI agent (via MCP) handles:
    // 1. Gemini image generation → featured image
    // 2. resize_image → platform variants
    // 3. schedule_social_post → publish to social

    // Store workflow state
    update_post_meta( $post->ID, '_workflow_status', 'pending_media' );
}, 10, 3 );
```

### Media worker workflow endpoint (fallback)

```php
// For pipelines that need media worker steps (e.g., DALL·E generation):
add_action( 'transition_post_status', function ( $new, $old, $post ) {
    if ( 'publish' !== $new || 'publish' === $old ) return;

    wp_remote_post( 'http://media-worker:3100/api/workflow/social-package', [
        'body'    => wp_json_encode( [
            'post_id'    => $post->ID,
            'title'      => $post->post_title,
            'content'    => wp_strip_all_tags( $post->post_content ),
            'platforms'  => get_post_meta( $post->ID, '_social_platforms', true ) ?: [ 'twitter', 'linkedin' ],
        ] ),
        'headers' => [ 'Content-Type' => 'application/json' ],
        'timeout' => 60,
    ] );
}, 10, 3 );
```

## Job queue patterns (Redis / media worker)

```javascript
// Enqueue a job via media worker
await redis.lpush('queue:image-generation', JSON.stringify({
  prompt: 'Social media hero for tech blog',
  model: 'dall-e-3',
  callback: 'http://wordpress:80/wp-json/design/v1/image-ready',
}));

// Worker processes jobs
while (true) {
  const job = await redis.brpop('queue:image-generation', 0);
  const { prompt, model, callback } = JSON.parse(job);
  const result = await generateImage(prompt, model);
  await fetch(callback, { method: 'POST', body: JSON.stringify(result) });
}
```

## Error handling & retry logic

```
Attempt 1: Gemini generate → success (attachment ID: 874)
Attempt 1: resize_image → fails (timeout)
    → Retry with wait
Attempt 2: resize_image → success
Attempt 1: schedule_social_post → Twitter OK, LinkedIn fails (expired token)
    → Alert admin, mark LinkedIn as failed
    → Do NOT retry (auth error, not transient)
    → Retry only LinkedIn later
```

## Performance considerations

| Operation | Typical Duration | Parallelizable? |
|---|---|---|
| Gemini image generation (MCP) | 5–15s | ✅ Yes |
| Image resize (MCP) | <1s | ✅ Yes |
| Background removal (MCP) | 1–5s | ✅ Yes |
| DALL·E 3 generation (media worker) | 10–30s | ✅ Yes |
| Image optimization (WebP, media worker) | 100–500ms | ✅ Yes |
| Video compression (FFmpeg, media worker) | 10–120s | ⚠️ CPU-bound |
| Social scheduling (MCP) | 200ms–2s | ✅ Yes |
| Cross-site remote calls | 100–500ms + target site latency | ✅ Yes |
| WordPress media sideload | 1–5s | ⚠️ Serialize |

## Common Mistakes

```
WRONG:
  ● Hard-coding site URLs in workflow scripts — breaks when domains change or sites migrate
  ● Triggering image generation on every post save without deduplication — creates hundreds of duplicate images
  ● Using synchronous HTTP calls for AI generation in WordPress hooks — blocks the request for 30+ seconds
  ● Mixing MCP tools and media worker calls for the same operation type without a clear routing rule
  ● Forgetting to verify spoke site connectivity before running cross-site media sync workflows
  ● Tracking workflow state in scattered post meta keys — use a single `_workflow_log` array or toolkit_cpt records (mcp_ai_project / mcp_ai_task)

RIGHT:
  ✅ Use remote_wp_connection to dynamically discover spoke sites at workflow runtime
  ✅ Implement idempotency checks — query existing media before generating, use post meta flags
  ✅ Route AI generation through a job queue (Action Scheduler or Redis Bull) — never block the request thread
  ✅ Define a clear routing rule: check MCP tool availability first, fall back to media worker only when no MCP tool exists
  ✅ Call remote_wp_connection { action: "list_connections" } and test_connection before cross-site pipeline execution
  ✅ Store workflow state centrally — use post meta arrays or toolkit_cpt on mcp_ai_project (project-level) and mcp_ai_task (step-level)
```

## Critical rules

- **Check your available tools first** — tool names vary by agent configuration. Search for `generate_gemini` or `web_search` in your tool list to find the correct prefixed names.
- **MCP first in every pipeline step** — check if an MCP tool exists before routing to the media worker.
- **Always use a job queue for production workflows** — never block HTTP requests waiting for AI generation.
- **Implement idempotency** — the same trigger should not generate duplicate content.
- **Track workflow state in WordPress post meta** — know what stage each post is at.
- **Log every step** — `update_post_meta( $post_id, '_workflow_log', $log_entries )`.
- **Handle partial failures** — if Twitter succeeds but LinkedIn fails, don't retry Twitter; only retry LinkedIn.
- **Verify spoke sites before cross-site ops** — use `remote_wp_connection` to list connections and test connectivity before routing workflows to remote sites.
- **Use Graphify federation for entity sync** — when moving content across sites, use `graphify_sync_remote_source` (from `addons/graphify/`) to maintain cross-site knowledge graph consistency.
- **Research before generating** — use the web search tool in your tool list to ground image prompts in real-world references.

## Cross-references

- Run **`design-image-generation`** for the generation step — check your tool list for the correct Gemini tool name.
- Run **`design-image-optimization`** for the optimization step — use `resize_image` (MCP).
- Run **`design-social-publishing`** for the publishing step — use `schedule_social_post` (MCP).
- Run **`design-content-calendar`** to schedule workflow triggers.
- Run **`design-brand-kit`** for Hub→spoke brand asset distribution.
- Run **`wp-action-scheduler`** for WordPress-native job queuing.
- Run **`wp-rest-api`** for WordPress webhook endpoints.
- Run **`mcp-ai-wpoos-plugin`** for `remote_wp_connection` docs, Graphify federation docs, and multi-site Gateway architecture.
- Use **`paper_store_*`** tools with `connection_id` to persist workflow state to specific spoke sites.
- Use **`browse_template_library`** to discover available media templates before applying them.
- Use **`apply_template`** to process individual images through saved template configurations.
- Use **`create_media_collection`** and **`add_to_collection`** to group images for batch pipeline processing.
- Use **`bulk_tag_media`** for taxonomy-based organization of media library assets.
- Use **`sync_media_to_remote`** to push media assets to remote WordPress sites via `remote_wp_connection`.
- Use **`import_media_from_url`** to bring external images into the media library for pipeline processing.

## What This Skill Does NOT Cover

- **Individual image generation** — use `design-image-generation` for one-off AI image creation; this skill covers chaining generation into pipelines.
- **Individual image optimization** — use `design-image-optimization` for single-image resize/compress/convert operations.
- **Social content strategy** — use `design-social-content` for caption writing and platform-specific content planning.
- **Campaign planning** — use `design-campaign-orchestration` for monthly themes and product selection that drive workflow triggers.
- **Video production** — use `design-video-creation` for video-specific pipelines (transcoding, frame extraction, AI generation).
- **Project and task management** — use `toolkit_cpt` on `mcp_ai_project` and `mcp_ai_task` for tracking workflow status outside media pipeline metadata.

## References

- WordPress Action Scheduler: <https://actionscheduler.org/>
- Redis Bull (Node.js job queue): <https://github.com/OptimalBits/bull>
- Design Stack media worker API: see `media-worker/README.md`
- Multi-Site Gateway plan: `docs/project/plans/multi-site-gateway-plan.md`
