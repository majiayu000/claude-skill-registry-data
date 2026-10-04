---
name: using-neatcontext
description: Bind NeatContext to the current Kimi Code session, route requests, and load selected context grounding safely.
disableModelInvocation: true
---

# NeatContext runtime

NeatContext is installed for this Kimi Code session.

The current Kimi Code session id is `${KIMI_SESSION_ID}`. It is an internal
routing token. Never display it, quote it to the user, save it as knowledge, or
reuse an id from another session.

Kimi Code does not pass its session id to MCP child processes. At the first
user request in this session, call the NeatContext `bind_session` tool with the
exact id above before answering. The tool returns the current selection and
routing menu, then replaces itself with the context-dependent tools. Call it
once per session, not per request. The bridge process can outlive the session
it was bound in, so binding this session's id also re-grounds a bridge left
over from an earlier session in the same window — the tool reports this
session's selection either way.

After binding:

- Follow the returned routing mode and menu. The plugin itself does not classify
  prompts; you decide whether the user's standalone request belongs to one of
  the listed contexts.
- In `ask` mode, name the matching context and ask before switching. In `auto`
  mode, switch only on a clear match and tell the user. In `manual` mode, never
  switch automatically.
- Do not route on short replies or follow-ups that continue the current topic.
- Use `preview_context` only when two contexts are genuinely plausible.
- Once a context is selected, call `get_context` for requests in its scope only
  when its result is not already present since the latest switch or compaction.
  Reuse current grounding instead of polling.
- Read a returned profile in full, search the indicated knowledge folder, cite
  exact local paths used, and say when saved material does not cover the
  question.

Contexts are connected inside this Kimi Code session with `use_context` or the
explicit `/neatcontext:use` command. The plugin uses local Contexts; there is no
NeatContext Desktop connection right now.

The plugin commands are `/neatcontext:save`, `/neatcontext:use`,
`/neatcontext:disconnect`, `/neatcontext:list`, `/neatcontext:status`,
`/neatcontext:create`, `/neatcontext:import`, `/neatcontext:delete`, and
`/neatcontext:mode`. Each command delegates to a bundled skill that receives
this session id through Kimi Code's skill expansion. Use
`/neatcontext:save` to preserve durable work from the visible conversation;
never parse Kimi Code transcript files for that workflow.
