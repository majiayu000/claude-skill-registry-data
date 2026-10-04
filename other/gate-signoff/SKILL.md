---
name: gate-signoff
description: Use this skill to capture a human phase-gate sign-off through chat rather than requiring the user to manually edit the gate markdown file. Prompts the user with the artifact path, collects a work-item URL (REQ / ticket / CR) as the non-trivial acknowledgment, validates the URL shape against the ticket system configured in `config/tools.json`, and writes the signed gate file at `.claude/sdlc/gates/<phase>-<task-slug>.md`. Invoked at the end of `/plan`, `/analyze`, `/design`, `/build`, `/test`, and `/support`. Deliberately NOT invoked by `/deploy` or `/fix-fast` — those still require the human to open and edit the gate file by hand. `/docs` has no dedicated gate file and does not invoke this skill.
config_requirements:
  - key: tracker.type
    required: false
    on_skip: accept_any_url
  - key: tracker.host
    required: false
    on_skip: skip_host_validation
---

# Gate Sign-off

Capture a fresh, auditable human approval at the end of a phase — without forcing a context-switch into the editor, but without letting approval degrade into a rubber-stamped "yes" either.

## When this skill runs

- **Invoked by phase commands** — `/plan`, `/analyze`, `/design`, `/build`, `/test`, `/support` — *after* the phase artifact has been written and shown to the human.
- **Does NOT run for** `/deploy` or `/fix-fast`. Deploy has blast radius; fix-fast bundles three phases into one mini-gate. Both require the human to physically open and sign the gate file.
- **Does NOT run for** `/docs`. Docs is cross-cutting and has no dedicated gate file.

## The sign-off dialogue

After the phase artifact is written, surface it and ask:

> Phase artifact: `.claude/sdlc/<folder>/<task-slug>.md` — please review.
>
> To sign off, paste the URL of the REQ / ticket / CR you're approving against.
> If no ticket system is configured (degraded mode), type `no ticket` followed by the REQ ID(s) from the requirements artifact — e.g. `no ticket REQ-12, REQ-13`.

Wait for the user's raw input. Do not proceed on a bare "yes", "ok", "lgtm", or emoji — those are not acknowledgments, they're rubber stamps. If the response is one of those, re-ask with the prompt above.

## Validation

Before writing the gate file, validate the input:

1. **URL form.** If the input looks like a URL, confirm it parses (scheme + host + path).
2. **Host match.** Read `config/tools.json` → `ticket_system.host`. If present, warn (not block) when the URL's host differs — the human may be pointing at a secondary system on purpose.
3. **Degraded form.** If the input starts with `no ticket`, require at least one `REQ-<n>` token and confirm each REQ ID appears in the requirements artifact for this task.
4. **Task-slug echo.** The skill independently computes the expected gate path; the written file lands there. Do not let the user's pasted text redirect the output path.

If any check fails, explain the failure and re-ask once. After a second failure, pause and ask the human what to do — do not guess.

## Approval packet compilation

Before writing the gate file, check whether the gate template will include a `## Required sign-offs` block (i.e., `approvals.roles` is non-empty or the human has added sign-off roles during this phase). If so, compile an approval packet at `.claude/sdlc/approval-packets/<phase>-<task-slug>.md` using `templates/approval-packet.md`.

**Inputs to compile from (read in order; skip gracefully with a "Source unavailable" note if absent):**

1. `plans/<task-slug>.md` — scope, out-of-scope, risk level, plan version
2. `plans/<task-slug>.v<N-1>.md` — prior signed version for the delta section (omit if plan is v1)
3. `scope.md` — overall project scope context
4. `requirements/<task-slug>.md` — REQ IDs and summaries for the traceability table
5. `gates/build-<task-slug>.md` — test status per REQ (if the build gate is signed)
6. `architecture/platform.md` — mitigation and rollback context (if exists)

**Length check:** if the compiled packet exceeds 100 lines, warn:
> Approval packet is `<N>` lines — reviewers will read more than two screens. Consider tightening the scope or delta sections before sending to reviewers.

This is a warn, not a block. The human decides whether to revise.

**Show the packet path** in the sign-off prompt so reviewers know where to find it:
> Approval packet compiled at `.claude/sdlc/approval-packets/<phase>-<task-slug>.md`.
> Share this path with reviewers — they can use it as the `evidence:` value in their sign-off file.

If `approvals.roles` is empty and the gate template has no `## Required sign-offs` block, skip packet compilation entirely — single-signer gates do not need a packet.

## Writing the gate file

Write to `.claude/sdlc/gates/<phase>-<task-slug>.md` using the `gate.md` template. Fill:

- `Signed by` — the active user's identity (email if available from the session, otherwise ask)
- `Signed at` — ISO-8601 UTC timestamp, captured at write time (not from user input)
- `Work-item reference` — the URL or `no ticket / REQ-<n>, …` string, verbatim
- `Acknowledgment` — the user's raw message, verbatim, quoted

Verbatim capture matters: an auditor reading the gate later should be able to see exactly what the human said, not a paraphrase.

## What this skill does NOT do

- Does **not** infer approval from prior conversation. A human has to type a fresh acknowledgment in response to the sign-off prompt.
- Does **not** auto-advance to the next phase. Phase commands are run by the human; this skill just produces the gate file the next command checks for.
- Does **not** write waivers or scope changes. Those go through `/plan` (for scope) or a new change-request artifact.
- Does **not** apply to `/deploy` or `/fix-fast`. For those, show the gate file path and stop — the human opens the file and edits it directly.

## Graceful degradation

- No `config/tools.json` or no `ticket_system` key → skip host validation; accept any well-formed URL or `no ticket REQ-…` form.
- User identity unknown → ask for a name or email at sign-off time; record whatever they provide verbatim.
- Writing the gate file fails (permissions, disk) → surface the error; do not retry silently. The human decides whether to fix the environment or record the sign-off elsewhere.

## Related

- [`templates/gate.md`](../../templates/gate.md) — the artifact shape this skill produces
- [`templates/approval-packet.md`](../../templates/approval-packet.md) — the compiled reviewer summary this skill produces for multi-team sign-offs
- [`hooks/phase-gate.sh`](../../hooks/phase-gate.sh) — the downstream hook that checks the signed gate exists before the next phase command runs
- [`hooks/work-item-validation.sh`](../../hooks/work-item-validation.sh) — complementary hook that validates the work-item reference independently at build time
