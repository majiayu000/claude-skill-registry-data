---
name: hone-prompts
description: >
  Capture and diagnose Phi's actual model requests from Logfire, including
  instructions, conversation, tool results, and tool definitions. Use for voice
  failures, prompt debugging, and tracing instructions to their current source.
---

# hone-prompts

Start from the behavior being investigated. Use
[phi-check](../phi-check/SKILL.md) to identify its public record and producing run.
A local render or personality file is not evidence of what a past run received.

## Capture the generating turn

Pass explicit start/end bounds to Logfire; the MCP's default 30-minute scan is
not widened by a SQL filter. Discover the relevant `chat %` spans in the trace,
then select the turn whose output contains the action under investigation.
The first request in a run is insufficient when tools loaded more context later.

Export these attributes to a local JSON file, alongside trace ID, span ID,
timestamp, and release when known:

- `gen_ai.system_instructions`
- `gen_ai.input.messages`
- `gen_ai.tool.definitions`
- `gen_ai.output.messages`
- `gen_ai.agent.name`, request/response model, and request parameters

Inspect the returned schema: SDK versions and providers can encode these fields
differently. If SQL JSON manipulation is limited, export attributes and parse
locally; do not substitute a truncated static-base query. Note missing, scrubbed,
or truncated fields. Retain the full available capture privately and render a
readable view of instructions and ordered messages for inspection.

Trace the tool call to its result and publication receipt. A judge's request is
not the main agent's request; identify both when diagnosing a rejection. An
assistant's final logging summary is not necessarily published text.

## Inspect context, then locate its source

Read the actual instructions and the messages preceding the action. Include loaded
skills, tool responses, retrieved memory, and previous assistant text. Measure
block and tool-schema sizes when investigating dilution, but do not equate their
character shares with causal influence. Look for conflicting directions and old
writing presented as examples. Quote the relevant evidence; distinguish a plausible
cause from a cause established by a controlled replay.

Find current owners in source with `rg`, rather than relying on line numbers or
a fixed list of agent names:

- Live personality comes from Phi's PDS personality records; the repository file
  seeds an empty collection. A present-day record may differ from the captured run.
- Operational instructions and dynamic context assembly are in `src/bot/agent.py`
  and its imported prompt modules. Search the captured text or block label.
- Policies and judge prompts are under `src/bot/core/`; inspect the implementation
  supplying the relevant agent.
- Tool descriptions come from their definitions or MCP server. Runtime skills
  live in `skills/`; operator skills in `.claude/skills/` are a separate surface.
- Memory and other PDS state have their own writers. Identify those before changing
  either stored prose or its injection.

Local rendering can test a proposed change; it cannot reproduce historical state
without the captured inputs. Preserve the baseline and change one relevant source
at a time. Follow the task's authorization for edits or deployment, update affected
reference docs, and verify a fresh request after rollout. PDS personality revisions
and deployed code have different activation paths; check the one actually changed.
