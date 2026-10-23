---
name: connect
description: >-
  Set up the services this kit's skills use — API keys, Google login, MCP servers — step by step, without keys ever passing through the chat. Creates one private keys file, walks the user through getting each key, registers MCP servers in Claude Code, and runs a health check that tests every key with a free request. Use when someone installs the kit, asks "what do I need to connect", "set up Ahrefs / GA4 / Parallel", "why doesn't X work", or a skill fails on a missing key. Triggers: "connect", "setup", "doctor", "check my keys".
---

# Connect

One keys file, one health check, one command per MCP server. Detailed guides per service live in `connections/` at the root of this kit.

```bash
KIT="python3 ${CLAUDE_SKILL_DIR}/scripts/kit.py"
$KIT init             # create ~/.config/marketing-agent-kit/.env (chmod 600)
$KIT open             # open it in a text editor
$KIT doctor --live    # tools, keys (tested with free requests), Google login, MCP servers
$KIT mcp list         # MCP servers it can register
$KIT mcp add ahrefs   # register one (add --dry-run to preview)
```

## The one rule: keys never go through the chat

Everything typed in a chat is saved in session transcripts on disk. So:

- Ask the user to paste keys **into the keys file**, not into the chat. Run `kit.py open` for them.
- Never print a key, never `cat` the keys file, never put a key in a URL or a command you show. `kit.py` reads the file and masks secrets in everything it prints.
- If a user pastes a key into the chat anyway: don't repeat it. Offer to write it into the file for them, and recommend rotating the key later, since it is now in the transcript.
- Prefer OAuth where the service offers it (Stripe, Ahrefs, ElevenLabs, SearchApi, Higgsfield): no key is stored at all.

## Order of work

1. **Find out what the user wants to do**, not which services exist. Map it with the table below and set up only those services.
2. `kit.py init`, then `kit.py open`. Tell the user which lines to fill in.
3. **One service at a time:** open its guide in `connections/`, walk the user through getting access in plain steps (what to click, what plan is needed, what it costs), wait for them to save the key.
4. `kit.py doctor --live` — confirm the key is accepted before moving on.
5. MCP servers: `kit.py mcp add <name>`. For OAuth servers, tell the user to run `/mcp` in Claude Code → pick the server → Authenticate. A new server appears after restarting the session (desktop app: start a new session).
6. Google services (GA4, Google Ads, BigQuery) use a gcloud login, not a key — follow `connections/ga4-mcp.md`. The login opens a browser: run it in the background and tell the user to sign in. Search Console uses a service account and a site config instead — `connections/search-console.md`.
7. Video: `python3 ${CLAUDE_SKILL_DIR}/../video-sound/scripts/library.py install` downloads the sound library (~150 MB), then `library.py venv` builds its analysis environment. HyperFrames: `connections/hyperframes-cli.md`.
8. Finish with `kit.py doctor --live` and a short table: what works, what's left, what it costs.

## Which skill needs what

| Skill | Needs | Cost to start |
|---|---|---|
| parallel-research | `PARALLEL_API_KEY` (or the free Parallel Search MCP for search only) | free credits on signup |
| ads-parser | `SEARCHAPI_KEY` | 100 free requests |
| ahrefs | Ahrefs MCP (OAuth or `AHREFS_MCP_KEY`); for scripted keyword research either `AHREFS_API_KEY` (API v3, any paid plan from Lite) or MCP results imported into `kw.py` | paid Ahrefs plan, Lite or higher |
| seo | nothing itself; routes to gsc-insights, seo-tech-audit and ahrefs | — |
| gsc-insights | `uv`, a Search Console service account with Restricted access, a site config; optional Google Sheet, BigQuery, Slack | free |
| seo-tech-audit | `uv`, the same site config; optional `CRUX_API_KEY`, `BING_WMT_API_KEY`, Chrome for the render check | free |
| competitor-research | all three above | — |
| ga4-reports | gcloud login + GA4 MCP | free |
| image-gen | `OPENAI_API_KEY` | pay per image (~$0.006–0.21) |
| ads-video-library | FFmpeg; optional Google service account for Drive | free |
| funnel-screenshots | Python 3.10+; its `setup.sh` installs Playwright + Chromium | free |
| video-studio, video-sound, video-build, video-moves, video-check | Node 22+, FFmpeg, HyperFrames CLI and skills, `ELEVENLABS_API_KEY` (paid plan for sound effects), the sound library (`video-sound/scripts/library.py install`), `uv` for its analysis venv, a Whisper CLI | ElevenLabs Starter $6/mo |
| video-3d | the same, plus a GPU-capable Chrome for HyperFrames | free |
| video-generated | `ATLAS_API_KEY` | pay per generation |
| plain-copy, copy-critic | nothing | — |

Optional extras with their own guides: Google Ads MCP, Stripe MCP, BigQuery, Playwright MCP, ElevenLabs, HyperFrames, Higgsfield, Slack.

## Safety defaults to recommend

- **Read-only wherever possible.** GA4 and Google Ads MCP are read-only by design. Stripe: grant Read only; BigQuery: allow only `execute_sql_readonly`. Add deny rules for write tools (examples in each guide).
- **Spending caps.** Ahrefs (monthly unit cap per key, plus `monthly_unit_cap` in the SEO site config), ElevenLabs (credit quota per key), Parallel (a separate key for agents), OpenAI (project budget), Atlas Cloud (top up small amounts).
- **Separate keys for agents.** A key that only an agent uses can be revoked without breaking anything else.

## When something fails

- `doctor` says a key is rejected → the key is wrong, expired or rotated. Issue a new one in the service's dashboard.
- An MCP server shows "Failed to connect" → see the troubleshooting section of its guide. For GA4 the usual causes are an expired gcloud login or a stale cached install (`pipx run --no-cache analytics-mcp`).
- `claude` CLI not found (desktop-app users) → open the app's built-in terminal (Ctrl+`) and run the command `kit.py mcp add --dry-run` prints, or add the server via **+ → Connectors** in the desktop app where the service is listed.
