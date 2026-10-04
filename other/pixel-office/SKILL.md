---
name: pixel-office
description: "Show Codex subagents working in a live Stardew-style pixel office web page. Use PROACTIVELY and implicitly whenever a task starts or observes subagents (spawn_agent/collaboration or sub_agent_activity), even when the user never mentions this plugin; automatically open the Codex app right sidebar page. Also use when the user mentions 子智能体/subagents/多智能体/编排, asks to watch them work, or mentions the pixel office (像素办公室)."
---

# Pixel Office · 子智能体办公室

A local web page that mirrors Codex subagent activity in real time as a
pixel-art office: each subagent gets a desk, streams output in a cloud speech
bubble, delivers results to the boss (the orchestrator) at the center desk,
then rests in the lounge corner. The boss randomly shouts slogans.

## PROACTIVE BEHAVIOR (default-on)

**When a response will start subagents, or a subagent is observed, treat this
skill as active automatically and do this WITHOUT waiting for the user to ask
or mention Pixel Office:**

1. Call the `pixel_office_status` MCP tool (provided by this plugin). It
   ensures the bridge server is running and returns the office URL.
   If the MCP tool is unavailable, ensure the server directly:
   `node <plugin-root>/server/server.mjs --port 8791` in the background
   (check `curl -s http://localhost:8791/api/state` first; only start if down).
2. After the bridge is confirmed (including after the direct fallback), open
   the page in the Codex app's right sidebar exactly once per conversation by
   calling the host tool:

   ```js
   tools.codex_app__open_in_codex({
     target: { type: "browser", url: "http://localhost:8791/" },
     placement: "right"
   })
   ```

   Do this automatically as soon as the first subagent is started (or just
   before the first `spawn_agent` call); do not wait for a manual click or a
   user request. If the host tool is unavailable, keep the bridge running and
   rely on its registered Local servers entry instead.
3. Tell the user once, briefly: the pixel office is live at
   http://localhost:8791/ and is listed in the app's browser sidebar under
   local servers. Do not repeat this on every turn.

## When to use

- Automatically, per the proactive behavior above.
- The user asks to open / show / preview the pixel office (像素办公室).
- The user wants to watch subagents work while a multi-agent task runs.
- The user asks for a demo of the office (demo mode below).

## Start the bridge server manually

The page needs the bundled zero-dependency Node server:

```bash
node <plugin-root>/server/server.mjs --port 8791      # real-time mode
node <plugin-root>/server/server.mjs --demo --port 8792   # demo mode (fake agents)
node <plugin-root>/server/server.mjs --replay <rollout.jsonl> --speed 20  # replay a past session
```

- `<plugin-root>` is the directory containing this skill's `skills/` folder.
- Real-time mode (default): tails `~/.codex/sessions/**/rollout-*.jsonl` and
  pushes `spawn_agent` / `sub_agent_activity` / agent output events over SSE.
- If port 8791 is in use, check `curl -s http://localhost:8791/api/state` —
  it is almost always this server already running.

## What the user sees (explain briefly when asked)

- 8 desks (2×4). Each spawned subagent walks in, sits at a free desk, and its
  latest output scrolls inside the cloud bubble overhead (max 3 lines,
  auto-scroll; click the bubble for the full text panel).
- On completion the worker walks the documents to the boss desk (center),
  the boss nods, a paper lands on the pile, and the worker rests in the
  lounge corner (chaise / cushions / coffee spots). If the same subagent gets
  new work (`interacted` event), it gets recalled to its desk.
- Failures: the worker throws the papers into a trash bin and slumps over the
  desk with a red bubble.
- The boss shouts one of four slogans every 20–40s while anyone is working.
- More than 8 concurrent agents: extras wait by the door with briefcases.

## Notes

- Only reads session logs; never writes to `~/.codex`.
- Assets were extracted from user-provided reference images; the extraction
  scripts live in `tools/` (Pillow required) and only need to run once.
- A launchd LaunchAgent keeps the bridge running across restarts when the
  user installed it via `install.sh` (default; `--no-daemon` skips).
