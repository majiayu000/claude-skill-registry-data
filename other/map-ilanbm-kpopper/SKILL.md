---
name: map
description: "Map existing materials into a first knowledge record, or investigate a subject's history in depth. Use whenever the user asks to map, survey, go through, reconstruct or investigate what already exists - folders of documents, decision records, meeting notes, emails, exports, code - or wants a starting record built from existing materials, even when the word 'record' is never said: consult this before listing or reading the files yourself, because a map has an agreed scope, a protocol and a report. Also, once, at a suitable moment, to offer the starting choices where a workspace has no record and the work is clearly ongoing - never on a greeting. Learning while working needs no map. Requests come in any language."
---

# Map

A map is work in its own right, with a scope and a result the user asked for. Learning while working - the default - needs none of this: the [record skill](../record/SKILL.md) keeps findings as they arise, and the first useful one creates the record. Run `kpop` or `kpopper` from the native runtime and prefer the canonical executable in `KPOPPER_AGENT_CONTEXT.command`. Do not guess a path or silently use PATH.

In ordinary conversation, name the product **kpopper** and describe the action in the user's language. Reserve the exact skill name `kpopper:map` for invocation instructions, technical documentation, debugging, or explaining this specific skill. Fold the product name into the explanation of the action; no extra announcement is needed.

**If it does not exist:** there is no record here yet; knowledge may already live in the
materials. Run `kpop open` if the hook did not supply `KPOPPER_START`, and follow
`kpopper _agent guide` for the optional first offer, source discovery and contextual explanations.
An unavailable registered record is a location problem, not a new project.

## The starting offer, once

In a Git project, use the mode and Board onboarding from `kpopper _agent guide`.
Inspect `kpop board`: `mode_offer` means offer **Simple (recommended)** with a chosen
external shared record location, or **Advanced (experimental)** with branch records.
Explain Advanced's possible record merge conflicts and repeated CI, and use the existing
README illustration. `offer` is the separate Board publication choice after mode selection;
keeping Board local does not select Simple. Reuse any already-approved publication scope.
Honor saved choices across worktrees and never stack the generic introduction below onto
this flow. Mapping and deeper investigation remain available whenever requested.

For non-Git Simple projects where a workspace has no record and the work is clearly going to be revisited, offer the three
starting choices once, briefly, at the first suitable moment in real work: **learn while working**
(the default), **map existing materials**, or **investigate more deeply**. Allow skipping. Do not
interrupt urgent work, and do not ask on a greeting - a session that only said hello gets no
offer. No answer means continue the task, not permission to scan. After showing the offer run
`kpopper _agent shown welcome`; the choice and what was shown are remembered per project and per
user, so a later session does not repeat them, and `kpopper _agent status` says what is still
unseen. Skip the introductory explanation for a user who has already seen it in another project.
`kpop config --guidance off` turns explanations off without turning the work off.

**Mapping is available by choice.** Offer learning while working, an initial map of existing
materials, or a deeper investigation within agreed subjects, sources and dates. An explicit
mapping request already chooses that work; no extra confirmation is needed. Use the guide
to locate where decisions happen and to keep historical accounts separate from present
findings. Do not expand into unrelated private sources or infer permission from silence.
For an explicit mapping request, call `kpop map --json` or `kpop map --deep --json`
with the host session environment, accept and execute the returned task, and report its actual
result through the supplied internal protocol. Do not stop after announcing a ready task.
Learning during ordinary work needs no configuration. Public operations are `open`, `map`,
and `config --guidance on|off`; request IDs and receipt calls are internal.

**Teach through actual events.** A compact card can explain the first saved finding, linked
source, grounded decision, conflict, reuse, or changed premise. Show real links where available
and use the host's native card or a Markdown block. `kpopper _agent status` lists unseen concepts;
`kpopper _agent shown EVENT` acknowledges an explanation only after displaying it. The introduction
is remembered per user, the starting offer per project. Respect `kpop config --guidance off` and do
not turn an onboarding step into a requirement for finishing the user's task.

A selected mapping or investigation makes discovery the task: follow `kpopper _agent guide` (the packaged [start guide](../../native/shared/start-guide.md)), stay inside the agreed subjects, sources and dates, and report its limits. The availability of more material is not a reason to survey it. The result is a report the user can read and a record whose first entries carry their sources; render the optional experimental [hub](../hub/SKILL.md) only if explicitly requested or covered by a standing preference.
