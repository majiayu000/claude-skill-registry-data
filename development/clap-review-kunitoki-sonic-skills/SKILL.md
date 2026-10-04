---
name: clap-review
description: >
  Reviews CLAP plugin implementations for spec compliance, thread safety, and correctness.
  Use when the user asks to review a CLAP plugin, audit a CLAP extension, or check whether
  their process() callback follows the CLAP threading model. Trigger on phrases like
  "review my CLAP plugin", "check CLAP extension", "is my CLAP process() safe",
  "audit my clap_plugin_t", or when you see clap_plugin_t, clap_process_t, or CLAP
  extension structs in the code.
---

# CLAP Plugin Review

CLAP's threading model is explicit by design — every host method and extension entry point is tagged with a thread requirement. Violations are silent at compile time and often only surface under specific host implementations.

## Step 0 — Run universal checks first

Invoke `audio-dsp-review` and `audio-numerics-review` before this skill. This skill adds CLAP-specific spec compliance checks on top; it does not replace realtime-safety or numerics reviews.

## Step 1 — Identify plugin structure

Locate and characterize the plugin's registered interfaces:

| Item | What to check |
|------|--------------|
| `clap_plugin_t` | `process`, `activate`, `deactivate`, `start_processing`, `stop_processing` implemented |
| Extensions returned by `get_extension` | Which of: `audio-ports`, `params`, `state`, `gui`, `note-ports`, `log`, `timer-support`, `posix-fd-support` |
| Host extensions queried in `init` | Which host callbacks are cached; which thread they may be called from |
| `clap_plugin_descriptor_t` | `id` is stable and reverse-DNS formatted; `features` declared correctly |

## Step 2 — Scan for CLAP-specific violations

| Violation | Where | Risk |
|-----------|-------|------|
| Holding `clap_event_*` pointer after callback returns | `process()` | Use-after-free — events are host-owned, lifetime ends when process() returns |
| Calling a host method from the wrong thread context | audio↔main boundary | Spec violation — obey each method's `[main-thread]`, `[audio-thread]`, or `[thread-safe]` tag |
| State save/restore doing I/O on wrong thread | `save`/`load` in state extension | Thread safety violation — state methods run on main thread, not audio thread |
| Extension methods not guarded by `thread_check` | any extension handler | Data race — extensions have per-method thread requirements; check each one |
| `process()` returning wrong `clap_process_status` | `process()` | Host misinterprets plugin state — `CLAP_PROCESS_SLEEP` vs `CLAP_PROCESS_CONTINUE` affects scheduling |
| Param IDs not stable across save/load cycles | params extension | Broken parameter recall — param IDs must be stable for the lifetime of the plugin ID |
| Audio port channel counts mismatched at runtime vs declared | audio-ports extension | Buffer overread/underwrite — host allocates buffers based on declared port config |
| Calling host `params->request_flush()` from `process()` | params extension | Spec violation — `request_flush` is `[thread-safe, !audio-thread]`; emit output events during `process()` instead |
| Querying plugin extensions before `plugin->init()` | host/plugin setup | Spec violation — `get_extension()` is forbidden before `init`, but allowed during and after `init` |
| Not handling `CLAP_EVENT_TRANSPORT` when transport-aware | `process()` | Incorrect playback position — transport events must be consumed each process call |

## Step 3 — Write the review

```
## CLAP Plugin Review: `[file / plugin id]`

### Verdict
[Spec-compliant | Has critical violations | Warnings only] — [one sentence summary]

### Critical Violations
**[Category]: [description]**
`file:line` — `offending code`
Why: [one sentence on the spec / thread safety risk]
Fix: [concrete CLAP-idiomatic suggestion]

### Warnings
[same format]

### What's Done Well
[correct patterns — proper event copying, thread_check guards, correct status codes, etc.]

### Recommended Fixes (priority order)
1. ...
```

## Quick fix table

| Violation | Fix |
|-----------|-----|
| Storing `clap_event_*` pointer | Copy the event struct by value before `process()` returns |
| Host call from wrong thread | Use only methods allowed for the current thread, or queue `host->request_callback()` and handle main-thread work in `on_main_thread()` |
| Wrong `clap_process_status` | Return `CLAP_PROCESS_SLEEP` only when all voices are done; `CLAP_PROCESS_CONTINUE` otherwise |
| Unstable param IDs | Use a fixed enum or stable hash derived from param name, never an index |
| Port count mismatch | Validate `audio_inputs_count` / `audio_outputs_count` in `process()` against declared ports |
| Missing `thread_check` guard | Wrap host calls with `host_thread_check->is_main_thread(host)` before calling |

For the full CLAP audit checklist organized by extension, threading rules, and BAD/GOOD code patterns see `references/clap-spec-checklist.md`.
