---
name: engineer-plugin-hooks
description: >-
  Build AI-IDE plugin hook elements - shared policies plus Claude
  Code/Codex/OpenCode/Cursor adapters for lifecycle events, blocking, audit, and
  context injection. Use when adding or configuring plugin hooks.
---

# Plugin Hook Engineer

Use this skill for hooks that ship inside a plugin. For a one-off project hook not tied to plugin packaging, use the project's hook-authoring workflow instead.

## Official Docs First

Do not treat this skill as a full hook specification. Hook event names, matcher
fields, input payloads, blocking outputs, and validation commands can change.
Before implementation, open the current official docs for every requested host
and cite or link the pages used in the output.

- Claude Code hooks: https://code.claude.com/docs/en/hooks-guide
- Claude Code plugins: https://code.claude.com/docs/en/plugins
- Codex hooks: https://developers.openai.com/codex/hooks
- Codex plugin build guide: https://developers.openai.com/codex/plugins/build
- Cursor hooks: https://cursor.com/docs/hooks
- OpenCode plugins: https://opencode.ai/docs/plugins/

Fetch only the sections needed for the current task. For any host not listed,
find its official hook, plugin, extension, or agent-loop docs first. If no
official docs exist, say so and separate verified behavior from assumptions.

## Workflow

1. Classify the request.
   - Design, plan, evaluate, or "help me design" -> output a hook design only;
     do not create files or run tests.
   - Create, implement, scaffold, write files, or modify this repo -> implement
     after the host docs and validation path are clear.
   - A concrete policy name or blocked command pattern does not make a request
     an implementation request. The verbs decide.
2. Define the policy.
   - Event, target tool, inspected fields, allow/block/ask behavior.
   - Required data and side effects.
3. Normalize input.
   - After reading the host docs, convert host hook input to an internal shape:
     - event name
     - tool name
     - tool input
     - current working directory
     - permission mode
     - transcript or session identifiers when present
4. Implement shared policy once.
   - No host-specific branching in policy unless unavoidable.
   - Return a normalized decision: allow, block with reason, add context, or modify output.
5. Add thin host adapters.
   - Use each host's current docs for event names, matcher fields, input JSON,
     block/deny result shapes, and plugin packaging paths.
   - Keep the adapter host-specific and the policy host-neutral.
6. Validate per host.
   - Use the validation commands and runtime mode from the current host docs.
   - Use a real repository when host trust or project-local config affects hooks.
   - Do not use non-interactive runs alone as evidence when the host docs require
     interactive trust review or a plugin runtime.
   - Always state that Codex hook validation may require interactive or trusted
     sessions; non-interactive `codex exec` can skip hooks or differ from the
     real plugin runtime.
   - Account for trust prompts and managed hook restrictions.

## Output Shape

Return or create:

- Shared policy module or script.
- Host adapter scripts/modules.
- Host hook config snippets.
- Official docs consulted.
- Test commands and expected evidence.
- Trust/approval caveats.
- Codex interactive-vs-non-interactive validation caveat.

For design-only requests, return the same shape as a concise design response
without writing files or running smoke tests.

## Pitfalls

- Do not freeze full hook schemas in this skill. Link the official docs and copy
  only the task-specific fields into implementation notes.
- Do not match shell command text in hook config when the host matcher expects tool names.
- Do not assume stdin JSON fields are environment variables; verify payload shape
  from docs or a local trace.
- Do not rely on arbitrary inherited environment variables.
- Do not mix plugin hooks with user/project hooks in tests without noting possible noise.
