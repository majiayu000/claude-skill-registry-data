---
name: event-modeling-implement
em-version: 1.22.0
description: >-
  Use when building a single ratified event-modeling slice (status: ready-to-implement) into
  merged, tested code — the one phase where the agent builds rather than facilitates. Gates on
  readiness, treats the slice doc as the read-only spec, surfaces gaps instead of deciding them
  silently, and requires tests traceable to the doc's invariants and scenarios.
---

# Event Modeling — implement

Goal: turn a single `ready-to-implement` slice into merged, verified code — the one phase where
the agent builds rather than facilitates.

**Read `reference/implement.md` before doing any implement work and follow it as the
contract.** In short: gate on `em validate <model>.em --slice-ready <key>` (stop and hand
back if it fails — never edit the doc to make the gate pass); read the project's implementation
constitution before writing code and stay inside its rules; before a project's first slice PR,
land a one-time foundation PR holding every model event (plus the shared interface shell) so
slices only ever import contracts, never invent or reach into a sibling's; build in dependency
order from `em query upstream`, not timeline order; treat the slice doc as
the spec (read-only, except the merge-time `status`/`implementedIn` flip); implement exactly one
slice doc per PR — a `covers:` doc's two keys ship together in that one PR, and an `again` view
instance is a continuation of its originating slice (no doc, status, or PR of its own — it
ships in the originating doc's PR); ship the endpoint a
`ui`-triggered command or `ui`-consumed view obligates, and surface — never invent — one the
model doesn't show; surface every gap to the user instead of deciding it silently; cover every
`INV-<MNEMONIC>-n` and every scenario with tests, proving the citations before merge with
`em coverage <model>.em --slice <key> --tests <dir> --strict` (the default form skips a
`ready-to-implement` slice); write or update the slice's `conformance/bindings/<key>.yaml`
(GH #450, `docs/bindings.md`'s schema) and verify it with `em conform bindings check <model>.em
--repo <path> --slice <key> --exit-code` before calling the slice done; in spec-kit projects,
allocate via em-sdd-bridge (redirect mode) and never run `/speckit.specify`.

**Gate: no constitution, no first slice.** The constitution is the project's ratified house rules
— stack and architectural shape (including which implementation skill each slice pattern routes
to), code style, testing norms, NFR baselines, review/merge norms. It lives at
`.specify/memory/constitution.md` in a spec-kit project (when that file exists), otherwise
`constitution.md` beside the model; `em status` reports which, and whether it's there. If it's missing — or its `ratifiedBy:`
is empty, meaning nobody has signed it off — run `reference/implement.md` §7 ("Before the first
slice: the constitution") first: ask its questions conversationally, write the answers in, and
have a human ratify them. Don't decide the project's stack or style yourself to get moving.

That contract applies to any implementing agent, whether or not the session started from
`/event-modeling` — `em contract` prints it to stdout with no `.claude/` awareness required, for
an agent that can run a shell but isn't Claude Code.

If the project ships pattern-specific implementation skills (for example an Axon/DCB skill set
keyed on a slice doc's `pattern:` frontmatter), route by the slice's pattern and follow those —
`reference/implement.md` §2 explains where that hand-off happens, and the constitution's
routing table (§7) is what names the skill set for each pattern.

Preconditions (tool check, model location) are the same as every other phase — see
`../event-modeling-shared/reference/operating-principles.md` — but this phase additionally
requires the target slice to already be ratified; if it isn't, stop and say so rather than
starting on unratified work. The one documented exception is **inline ratification** (GH #399,
`reference/implement.md` §1a): for an internal (non-public-touching, non-engagement) slice whose
doc is already `reviewed`, drafting code on the same branch ahead of the human's `em slice
ratify` is sanctioned — provided you never flip the gate yourself and re-confirm
`--slice-ready` reads `true` before treating the slice as done. `event-modeling-engagement` is
unchanged by this: it still requires every dispatched slice ratified before its branch is cut.

End of phase: PR merged, slice doc flipped to `status: implemented` with `implementedIn`
filled, `em slice index <model-name>.em` run to refresh `README.md`'s Slices table. Implement
doesn't chain to another phase — run it once per ratified slice; `event-modeling-conform`'s
`conform` phase later checks the result against the model.
