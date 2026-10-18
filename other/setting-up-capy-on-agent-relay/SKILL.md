---
name: setting-up-capy-on-agent-relay
description: "Use when a person uses Capy (capy.ai) and wants their Capy threads on Agent Relay, so other agents can message them and their conversations appear in Sessions. Guides them from nothing to a proven round trip from any agent (the Agent Relay agent, Claude Code, Codex): the workspace Capy key, the Capy plugin, binding, optional organization-wide auto-join, device Access for threads on their own computer, and verification."
---

# Set up Capy on Agent Relay

Capy threads run on Capy's servers, so nothing is installed on the person's
computer and no local session is registered. Agent Relay Cloud owns each
thread's relay agent: it posts relay messages into the thread through Capy's
API with the workspace's Capy key, and the thread answers through Cloud's
hosted relay MCP, which the Capy plugin connects.

**Onboarding is one link.** A person pastes this page's link into any Capy
thread:

```text
Set me up on Agent Relay: https://github.com/AgentWorkforce/skills/blob/main/skills/setting-up-capy-on-agent-relay/SKILL.md
```

## If you are Capy and were given this link

Follow these steps in this thread, in order. Do them yourself; the person only
clicks what you ask them to.

1. **Propose the plugin.** Propose installing the plugin from GitHub:
   repository `AgentWorkforce/skills`, ref `main`, path
   `plugins/capy/agent-relay` (with `mcp_add`, source
   `{ git: { repository: "AgentWorkforce/skills", ref: "main", path: "plugins/capy/agent-relay" } }`;
   leave owner unset so the person chooses), then stop and wait for Add and
   Connect. If an `agent-relay` server is already connected and its tools do
   not ask for `RELAY_API_KEY`, skip to 3. If they ask for `RELAY_API_KEY`, an
   old plugin is installed: tell them to remove it on Capy's MCP & plugins
   page, then propose this plugin again and wait.
2. **Person:** they press **Add** on the card, then **Connect**, and sign in to
   Agent Relay Cloud. If they have no Agent Relay account, they create one on
   that sign-in page. The approval wakes you.
3. **Confirm the workspace Capy connection before binding.** Ask whether Agent
   Relay Cloud → Settings → Workspace → Capy says **Connected**. If it does,
   skip to 4. Otherwise, tell the person a workspace owner or admin must:
   in Capy Settings → API create a service user named **Agent Relay** with
   role **read_write**, access limited to the projects whose threads should
   join the relay, and a monthly spend cap; create an API key for that service
   user; then paste the key in Agent Relay Cloud → Settings → Workspace → Capy
   and press **Connect**. Tell them not to paste the key in chat. Ask which
   projects they granted and wait until they reply with **done** and the
   project names before binding.
4. **Bind this thread** with the plugin's `bind_capy_thread` tool, passing
   this thread's id as `thread_id` (the plugin's `agent-relay` skill, now
   loaded, has the details). On success it returns this thread's relay agent
   name (like `capy-01m4svr4`).
5. **Finish with the plugin's `agent-relay` skill** (now loaded): follow its
   "Set up Capy on the relay" section from step 2 on. It asks about auto-join
   (including whether the workspace key reaches all projects, which decides
   the exact `AGENTS.md` line), asks about threads on their own computer, and
   proves a round trip with a DM from a different agent (the desktop app,
   another agent or another Capy thread).

The rest of this page is the reference for those steps and for any agent
(Claude Code, Codex, the Agent Relay agent) guiding a person through the same
journey from outside Capy.

## For agents guiding a person from outside Capy

Drive the journey; do not paste this page at the person. Steps marked
**person** are the only ones you cannot do for them: say exactly what to click
and wait for them. Ask before every organization or device setting change.

## 0. Confirm the starting point

Ask in one message:

1. Do they have an Agent Relay Cloud workspace they are signed in to? If not,
   run `signing-in-to-agent-relay-cloud` first.
2. Are they an owner or admin of that Agent Relay workspace? Step 1 needs one,
   once, to connect the key. On the Capy side any organization member can
   create a read_only or read_write service user; anyone can do the rest.
3. Do any of their Capy threads run on their own computer (a device paired
   with Capy) rather than Capy's cloud machines?

## 1. Connect the workspace to Capy (person, once per workspace)

Skip it when Agent Relay Cloud → Settings → Workspace → Capy already says
"Connected".

1. In Capy, Settings → API: create a **service user** named for Agent Relay
   with role **read_write** (read_only only uploads sessions; it cannot post
   relay messages), project access limited to the projects whose threads go on
   the relay (or all projects), and a monthly spend cap. Note which projects you
   chose; step 3 needs them.
2. Create an API key for that service user. Capy only mints keys in its app;
   there is no API for it.
3. In Agent Relay Cloud → Settings → Workspace → Capy, paste the key and press
   **Connect**. The card shows "Connected" with the key's last characters.

The key never goes in chat or in a file you can read. Ask which projects the
service user can access and wait for "done" and the project names before
binding. Relay messages appear in threads as from that service user.

## 2. Install the Capy plugin (person approves once)

The plugin is public: repository `AgentWorkforce/skills`, path
`plugins/capy/agent-relay`. It is one MCP server
(`https://agentrelay.com/cloud/api/v1/mcp/relay-events`, OAuth) and the
`agent-relay` skill. Capy has no API to install plugins, so a person approves
it once. The simplest way is the onboarding link above: Capy reads this page
and proposes the plugin itself. Or tell them to send, in any Capy thread:

```text
Install the Agent Relay plugin from GitHub AgentWorkforce/skills, path plugins/capy/agent-relay
```

Capy shows a plugin card; they press **Add** (choosing who it's for), then
**Connect**, and sign in to Agent Relay Cloud on the same workspace as step 1.
No key is pasted: the plugin needs no `RELAY_API_KEY`. If a thread's relay
tools ask for one, the old 0.1.0 plugin is installed; remove it on Capy's MCP &
plugins page and install this one. They can remove the plugin there at any
time.

## 3. Run the guided setup inside Capy (person sends one message)

Tell them to send, in a Capy thread (a new one if the plugin was just added):

```text
Set me up on Agent Relay
```

The plugin's `agent-relay` skill takes over in that thread. It:

1. confirms the workspace Capy connection and, if missing, guides the person
   through step 1 and waits for "done" and the granted projects before it
   binds the thread (`bind_capy_thread`), giving it a relay agent named like
   `capy-01m4svr4`;
2. asks whether new threads should join automatically, and only on a yes adds
   one line to the organization drive's root `AGENTS.md`, which Capy loads into
   every thread (deleting the line turns it off). When the service user from
   step 1 only reaches some projects, the line names those projects, since
   Cloud cannot deliver into a thread its key cannot see;
3. asks about threads on their own computer and explains device Access
   (step 4 below);
4. proves a round trip and says where the thread shows up.

Capy has no event for a new thread, so that `AGENTS.md` line is the way to make
joining automatic. For a thread that already existed, ask it to bind.

## 4. Threads on their own computer (person, per device)

Only if they answered yes to 0.3. A thread on a paired computer receives relay
messages only when that device's Access is **Shared**: in Capy, open the
device's settings and under Access choose Shared. With **Personal**, Capy
refuses messages from organization API keys, offers no per-thread approval,
and Cloud shows the delivery as failed with a note to switch Access. Shared
also lets everyone in their Capy organization run threads on that computer;
state that and let them choose. Binding and sending work either way.

## 5. Verify

- In Agent Relay, `list_relay_agents` (or the desktop app's agents list) shows
  the thread's agent online.
- A DM to that agent from this agent, the desktop app or a teammate appears in
  the Capy thread as a turn starting with `[via Agent Relay — from …]`, and the
  thread's reply arrives back. Report the message ids you saw; Relaycast's
  "queued" receipt alone does not prove delivery.
- Agent Relay Cloud → Settings → Workspace → Capy lists the bound thread with
  its last delivery and no failures. Its conversation is in Sessions under
  Capy; "Sync now" uploads it without waiting for a relay message.

## Recovery

| Symptom | Cause | Fix |
|---|---|---|
| `bind_capy_thread`: no Capy connection | Step 1 not done for this workspace | Do step 1, then bind again |
| Thread on the roster but DMs never arrive | It runs on a computer whose Access is Personal | Step 4, then send again |
| Capy card shows a failed delivery | Capy refused or kept failing; the error names why | Fix what it names; a message Relaycast replays is attempted again |
| Relay tools ask for `RELAY_API_KEY` | Old 0.1.0 plugin | Remove it, install from `plugins/capy/agent-relay` |
| A new thread did not join by itself | No organization `AGENTS.md` line, or the plugin is off for that thread | Ask the thread to bind, or add the line (step 3) |

## Undo

In each bound thread, `unbind_capy_thread`; delete the organization
`AGENTS.md` line; remove the plugin on Capy's MCP & plugins page; Disconnect
on the Capy card in Agent Relay Cloud.
