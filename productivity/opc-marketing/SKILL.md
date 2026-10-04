---
name: opc-marketing
description: "Use when automating OPC marketing with Hermes Agent."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, marketing, opc, cron, kanban, webhook, profiles]
    related_skills: [hermes-messaging-gateway, hermes-multimachine-sync]
---

# OPC Marketing Workflow with Hermes Agent

## When to Use

- Building or extending an automated marketing/sales pipeline for a one-person company.
- Wiring an external service's events (order, lead) into Hermes as a webhook.
- Deciding whether something should be a profile, a bot, a cron agent, or a sub-agent.
- A scheduled marketing agent is failing, silent, or reporting to nobody.

## 0. Mental model: profile, bot, agent, sub-agent

Four things that get conflated. Separate them by asking a different question of each:

| Question | Answer |
|---|---|
| Where does this live? | **Profile** — a division: own home, memory, skills, sessions, cron |
| Who can talk to a human? | **Bot** — a platform connection; the door into a profile |
| Who works unprompted? | **Agent** — a cron job; runs on its schedule |
| Who is hired for a burst? | **Sub-agent** — `delegate_task`, called from a chat turn, gone when done |

**A bot is a door, not a dispatcher.** It does not read an incoming request and route it to the
right agent, and nothing else does either. Work reaches an agent by exactly three routes:

1. **Schedule** — the cron job fires whether or not anyone chats with anything.
2. **You ask in a chat** — the agent in *that session* does the job itself, spawning sub-agents when
   it is big. It does not hand off to the `content-writer` cron job or any other agent.
3. **A Kanban card's assignee** — the dispatcher spawns a worker for that card.

So "make me 30 posts this month", typed into a bot, is one agent doing one large job — not a router
splitting it across the division. When the user asks how the bot decides who does what, the answer is
that it does not: say this plainly, because it is the most common misunderstanding about the whole setup.

**Chatting with a bot and opening a new session reach the same brain.** Same profile, same memory,
same skills. The only difference is the surface: a bot is one persistent chat reachable from a phone,
a new session is a GUI session where files and the board are actually readable. Choose on convenience,
never on capability.

**Kanban columns move because a prompt told an agent to move them**, not because anything watches
column state. A per-division board works because each cron agent's prompt edits the cards it owns.
Reserve `hermes kanban swarm` for assignee-driven worker dispatch, which is a different mechanism.

Full worked roster, board flow and prompt layout for one division: `references/division-blueprint.md`.

## 1. Webhook Subscription for External Events

When an external service (e.g., Sejoli, WooCommerce, Shopify) sends a webhook on events like `order.completed`, you can let Hermes ingest, validate, and act on it.

### Steps
1. **Obtain the shared HMAC secret** from the external service’s webhook settings.
2. **Create the subscription** in Hermes:
   ```
   hermes webhook subscribe <name> --secret <HMAC_SECRET> --events <event> --prompt "<prompt_instructions>" --deliver prompt
   ```
   - `<prompt_instructions>` should extract fields from the payload (e.g., `customer_phone`, `customer_name`, `product_name`, `order_id`, `amount`) and describe the action (send WhatsApp message, log to CRM, create a Kanban card).
   - Use `--deliver prompt` so the agent runs the prompt on each valid event.
3. **Verify** the subscription:
   ```
   hermes webhook list
   ```
4. **Test** with a valid signature:
   - Build a JSON payload matching the expected event.
   - Compute `sha256=HMAC(secret, payload)`.
   - Send `POST https://<your-domain>/webhooks/<name>` with header `X-Sejoli-Signature: <sha256>` and the JSON body.
   - Check `~/.hermes/logs/gateway.log` for `"status":"accepted"`.

### Pitfalls
- **Secret handling** – Never embed the secret in a shell script that gets echoed; pass it directly via `--secret` to avoid interpolation or logging.
- **Payload shape** – If the external service nests data under different keys, adjust the prompt accordingly; test with a sample payload first.
- **Duplicate processing** – Hermes will process every verified request; ensure your prompt is idempotent or store processed IDs in memory (`hermes memory add …`) if needed.
- **Webhook platform must be enabled first** – Before creating subscriptions, ensure `platforms.webhook.enabled: true` in config.yaml (or run `hermes config set platforms.webhook.enabled true` and `hermes gateway restart`). Otherwise `hermes webhook subscribe` fails with "Webhook platform is not enabled".

## 2. Creating Scheduled Agents for Repetitive Work

For tasks that should run on a timetable (e.g., keyword research, ad performance checks, content generation), create a Hermes **cron job** with an attached prompt/script. There is no `hermes agent create` command — agents are cron jobs that run prompts.

### Steps
1. **Define goal, context, and prompt**.
   - Goal: short description.
   - Context: files, data, or notes the agent needs (e.g., product catalog, keyword list).
   - Prompt: detailed instructions, preferably requesting a structured output (JSON) if the result will be consumed by another step.
2. **Store prompt in a file** (recommended for complex prompts) under `~/prompts/<agent-name>.txt`.
3. **Create a wrapper script** in `~/.hermes/scripts/<agent-name>.py` that prints the prompt (required because `hermes cron create --script` only accepts scripts inside `~/.hermes/scripts/`).
4. **Create the cron job**:
   ```
   hermes cron create "<cron-expression>" \
     --name <agent-name> \
     --skill <skill-name> \
     --script <agent-name>.py \
     --deliver local
   ```
   - `--schedule` follows standard cron syntax (e.g., `0 9 * * *` for 09:00 daily).
   - `--skill` loads the skill (and its references/) into the agent's context.
   - `--script` points to a Python file in `~/.hermes/scripts/` that outputs the prompt to stdout.
   - `--deliver local` sends output to the local session log (use `bot-chat:<profile>` for gateway delivery).
5. **Run manually** for testing:
   ```
   hermes cron run <job-id>
   ```
6. **Inspect logs** for debugging:
   ```
   hermes cron runs <job-id>
   ```

### Pitfalls
- **Vague prompts** lead to unpredictable outputs; always specify the exact format you expect (e.g., `"Output JSON: {\"keywords\":[{\"term\":\"...\",\"cpc\":0,…}]}"`).
- **Missing context** – If the agent needs files that aren’t in its working directory, specify absolute paths in the prompt or use `--workdir` when creating the cron job.
- **Overlapping schedules** – Ensure cron expressions don’t cause resource contention; stagger long‑running tasks.
- **Scripts must live in ~/.hermes/scripts/** – `hermes cron create --script` rejects absolute or home-relative paths. Place wrapper scripts there and reference by filename only.
- **No `hermes agent create` command** – The skill previously documented a non-existent command. Use `hermes cron create` with `--script` instead.
- **A failed run's real cause is not in the cron output.** The scheduler reports only
  `session ended without a final assistant message (lifecycle=interrupted) — booking run as
  cron_incomplete_no_output`, and `hermes cron run <job>` prints a bare `Ran now: failed.` The
  underlying error — provider `HTTP 402` insufficient credits, auth failure, `HTTP 500` — is in
  `~/.hermes/logs/errors.log`. Read that file before doubting the job's wiring, the skill, or the
  model routing: an out-of-credit provider fails *every* job while looking exactly like an agent bug,
  and the jobs keep producing partial output that hides it.
- **A job can report success and deliver nothing useful.** Grep the delivery receipt
  (`delivered to telegram:<chat>`) rather than trusting the run status.

## 3. Linking Agents to a Kanban Board

Use a Kanban board to visualize work items (e.g., “Create caption for AP‑1512HH”, “Review ad performance”). Each card can be moved by agents or manually.

### Steps
1. **Create a board** (SQLite-backed, not JSON file):
   ```
   hermes kanban boards create <board-slug>
   hermes kanban boards switch <board-slug>
   ```
2. **Add cards** via `hermes kanban create` (no `--column` flag; cards start in `ready` status, assignee determines who picks them up):
   ```
   hermes kanban create "Task title" --body "Task details" --assignee <profile-name>
   ```
3. **Move cards** by changing assignee/status via dispatcher, or manually:
   ```
   hermes kanban assign <task-id> <profile-name>
   hermes kanban block <task-id> --reason "waiting on..."
   hermes kanban complete <task-id> --summary "Done"
   ```
4. **Review** the board:
   ```
   hermes kanban list
   hermes kanban show <task-id>
   ```

### Pitfalls
- **No `--column` flag on `hermes kanban create`** – Cards are created with status `ready` and picked up by the dispatcher based on assignee. Column workflow is managed by the dispatcher, not manual column moves.
- **Board is per-project, not per-division** – Use `hermes kanban boards create` for separate workstreams.
- **Non‑unique IDs** – Let Hermes generate task IDs (e.g., `t_abc123`); don't invent your own.
- **Stale cards** – Configure `kanban.failure_limit` and `kanban.dispatch_stale_timeout_seconds` in config.yaml; the dispatcher auto-blocks after repeated failures.

## 4. Watcher Agents for Service Health

To catch downtime of external APIs (MCP servers, webhook endpoints, ad platforms, gateway, VPS), run a lightweight cron job on a frequent schedule that alerts you via WhatsApp when something fails.

### Steps
1. **Create a watcher cron job** (same pattern as scheduled agents):
   ```
   hermes cron create "*/5 * * * *" \
     --name watcher-<service> \
     --skill <skill-name> \
     --script watcher_<service>.py \
     --deliver bot-chat:default
   ```
   - Wrapper script in `~/.hermes/scripts/watcher_<service>.py` prints the monitoring prompt.
   - `--deliver bot-chat:default` sends alerts to the gateway's default bot chat (WhatsApp/Telegram).
2. **Prompt pattern for watchers**: include failure counter logic (only alert after N consecutive failures) and recovery notification.
3. **Test** manually: `hermes cron run <job-id>`.
4. **Monitor** logs: `hermes cron runs <job-id>`.

### Pitfalls
- **Secret leakage** – Never put API keys or tokens directly in the prompt; store them in Hermes config (`hermes config set`) or memory and reference via variables if supported, or use the `--secret` flag where the tool accepts it.
- **Alert fatigue** – Add throttling (e.g., only alert if failure persists for two consecutive checks) to avoid spamming your phone.
- **Use memory for state** – Store failure counters and last-alert timestamps in Hermes memory (`memory` tool with `operations` batch) so state persists across cron runs.
- **Gateway/WA bot watcher needs terminal access** – The watcher script can call `terminal` tool to run `hermes gateway status` and restart if needed.

## 5. Putting It All Together – Example Flow for a New Order

1. **Sejoli** sends `order.completed` webhook to Hermes.
2. Hermes validates the HMAC signature, extracts `customer_phone`, `customer_name`, `product_name`, `order_id`, `amount`.
3. The webhook subscription's prompt runs (with `smartmillionaire-marketing` skill loaded):
   - Sends a WhatsApp welcome message using template from skill references.
   - Creates a Kanban task `Follow-up WA – Order #{order_id}` with assignee `followup-agent` and body containing customer details.
   - Logs to Novamira CRM via MCP (`create_contact`, `add_tag`, `log_activity`).
   - Stores deduplication key in memory: `lead:{order_id}`.
4. **followup-agent** (cron `0 10 * * *`) picks up due tasks, sends staged follow-ups (D+2, D+7, D+30, D+60, D+90), updates task metadata, moves cold leads to `Cold` column.
5. **ads-performance-agent** (cron `*/30 9-18 * * 1-5` + daily `0 21 * * *` + weekly `0 7 * * 1`) monitors Meta Ads, alerts on CPC/CTR/ROAS anomalies, creates `Refresh Creative` tasks when frequency > 3.5.
6. **content-edu-agent** (cron `0 7 * * *`) generates daily educational content (image prompt + WA caption), creates `Content Pipeline` tasks for review.
7. **Three infrastructure watchers** (webhook, gateway/WA, VPS) run every 5/10/60 minutes, alert on failure with auto-recovery attempts.

By combining webhook‑triggered actions, scheduled cron jobs, Kanban task queue, and watcher bots, a single operator can run a fully automated marketing and sales pipeline with minimal manual intervention.

## 6. Skill Structure for Domain Context

Create a **domain skill** (e.g., `smartmillionaire-marketing`) to hold all reusable assets:

```
<skill-name>/
├── SKILL.md                    # This file's pattern
├── references/
│   ├── products.json           # Product catalog with prices, links, upsell map
│   ├── templates.md            # WA message templates with variables
│   ├── keywords.txt            # Keyword research history + negative keywords
│   └── faq.md                  # Comprehensive FAQ + quick responses
├── scripts/                    # Optional: image generation, etc.
└── prompts/                    # Agent prompts (in ~/prompts/)
    ├── lead-intake.txt
    ├── followup.txt
    ├── content-edu.txt
    ├── ads-performance.txt
    ├── watcher-webhook.txt
    ├── watcher-gateway.txt
    └── watcher-infra.txt
```

Load in cron jobs via `--skill <skill-name>`. The skill's `references/` files are available to the agent as context.

### Memory Keys Pattern
Use consistent memory keys for cross-agent state:
- `lead:{order_id}` – deduplication for lead intake
- `lead:{customer_phone}:{product_name}` – alternative dedup key
- `customer:{phone}` – customer profile (name, orders, segment, preferences)
- `webhook_check:{timestamp}` – webhook health log
- `gateway_check:{timestamp}` – gateway/WA bot health log
- `vps_check:{timestamp}` – VPS infrastructure health log
- `content:{date}` – generated content metadata
- `ads:benchmarks` – 7-day rolling benchmarks for anomaly detection

### User Tone & Style (This User)
- **Language**: Casual Indonesian (bray, lo/gua, gass, susah njir)
- **Tone**: Warm, helpful, credible, NOT salesy
- **Emoji**: 1-2 per message, natural
- **Length**: Max 1600 chars per WA (1 segment)
- **CTA**: Soft, value-first, link at bottom
- **Prefers GUI over CLI** – Default to `hermes dashboard` for monitoring, not terminal logs.
- **Explaining architecture**: answer with one analogy held consistently through the whole reply,
  plus a table per concept, and always a "who does what" table for any workflow. This user asks for
  the same explanation more than once when it arrives as prose — a concrete roster (named agents with
  schedules and duties) lands where an abstract description does not. Build the thing while explaining
  it rather than explaining first and waiting for a go-ahead.