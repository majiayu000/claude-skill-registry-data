---
name: dayz-route
description: "Picks the skill, agent or team for a DayZ request with free keyword rules, then Jev when configured, and prints one JSON decision, including when the dayz-router agent is needed. Use when a new DayZ request arrives in the main session, before choosing a handler yourself."
argument-hint: "\"<request>\" [--json]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-route

Route a DayZ request without spending a big-model turn on it. Run it first for every new DayZ request in the main session. Skip it for follow-ups inside work that is already routed, and for non-DayZ work.

It needs no DayZ install and does not gate on `/dayz-preflight`: it only reads `rules.json` and, when keyed, calls one web API.

## How to run

```cmd
python "<skill-dir>\route.py" "<the user's request>" --json
```

Without `--json` it prints one readable line instead. It exits 0 for a non-empty request, 2 for an empty one, and 1 with a one-line `dayz-route: rules.json: ...` message on stderr when `rules.json` is missing, is not valid JSON, or holds a bad regex, an unknown route or a bad `absorbs` value. On exit 1, fix `rules.json` (or dispatch the `dayz-router` agent meanwhile).

## Output

One shape for every stage:

```json
{"route": "dayz-build-pbo", "kind": "skill", "confidence": 0.9, "source": "rules", "args": {"mod": "MyVest"}}
```

- `kind` `skill`: run `/<route>`, passing `args` (for `dayz-build-pbo`, `args.mod` is the mod name). A decision with `source` `jev` carries no `args`. Before you run `/dayz-build-pbo`, `/dayz-lint` or `/dayz-release-pack` from one, take the mod name from the request, or ask the user for it when the request does not name one. Pasted content has its own routes, which win over anything else the message says:
  - `dayz-gate` with `args.mode` `triage`: pasted crash log or RPT lines. Pipe the pasted text to `triage.py --stdin --json` (in `dayz-gate`). Hand each `known` result's fix to its `owner_agent`, and dispatch `dayz-mod-debugger` with only the `new` lines.
  - `dayz-edit-types` with `args.mode` `merge`: a pasted chunk of `<type>` entries. Run `types_edit.py <types.xml> --merge -` with the chunk on stdin.
  - `dayz-import-mod` with `args.source`: a GitHub link to clone into `workspace\`, or a Steam Workshop link, which the skill refuses with the reason.
  - `dayz-cot-bootstrap` has model invocation turned off, so you cannot run it. Tell the user to type `/dayz-cot-bootstrap` themselves.
- `kind` `agent`: dispatch that agent with the user's request. When the route is `figma-node-normalizer`, run the whole Figma pipeline in order: `figma-node-normalizer`, then `figma-to-dayz-layout`, then `dayz-layout-validator` in gate mode.
- `kind` `team` (`route` is `orchestrator`): a whole-mod build. Tell the user to start `claude --agent agentic-z:dayz-orchestrator` (or `claude --agent dayz-orchestrator` in a clone).
- `{"route": null, "next": "dayz-router", "note": "..."}`: no stage was confident. Dispatch the `dayz-router` agent with the request; it returns the same shape with `source` `router`. Follow it when `confidence` is 0.8 or more, otherwise handle the routing yourself or ask the user.

## Stages

1. **Rules** (`rules.json`, free): regex patterns per route. A rule can carry fixed `args` (the paste rules set `mode`) that join what its pattern captures. Matches for two different routes (for example "build MyVest and launch it", or "rebuild and launch" with no mod name) cut confidence by `conflict_factor`, because that is a multi-step request. A rule's `absorbs` value says which other matches it may ignore and keep full confidence:
   - `true`: matches for routes that are not separate steps, so a named item (a car, a rifle, a changelog) does not pull a file, log, tool or question request away. Targets marked `"step": true` (build, deploy, lint, conflict check, launch, stop, types.xml edit) are separate actions, and a `true` rule absorbs one only when both matches cover the same words (such as "rebuild" in "rebuild the search index"). So "build MyVest then show me the health page" falls through instead of dropping the build.
   - a list of step targets: those steps too, because they are part of the rule's own work (the build engineer builds and launches; server admin edits types.xml; a behaviour or visual test launches the game).
   - `"all"`: everything. Paste rules and the whole-mod team use it.

   Results at or above `threshold` (0.8) are final.
2. **Jev** (`jev.py`, only with `TYPESAFE_API_KEY` set): one TypeSafe Choice question over all targets plus `other`, 5 second timeout. Missing key, network error, bad status, `other` or low confidence all fall through, with the reason in `note`. The request text is sent to `api.typesafe.ai`.
3. **dayz-router** agent: Haiku, reads nothing but the request (and `rules.json` if needed).

## Changing routes

Add a target to `targets` (with `"step": true` when it is a separate action a request can chain with others) and a rule to `rules` in `rules.json`, and add the same target to the list in `agents/dayz-router.md`. `test_route.py` fails if a target has no skill folder or agent file, or if the two lists differ.
