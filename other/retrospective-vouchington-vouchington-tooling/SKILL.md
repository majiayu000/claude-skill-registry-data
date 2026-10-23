---
name: retrospective
description: Summarize completed work from verified facts and the session journal.
---

# Retrospective

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/retrospective/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use at task completion or session close-out when the repository has a retrospective workflow. Read
local `AGENTS.md`, and journal guidance first.

Budget: at most 10 tool calls, 5 minutes, and 25k tokens. Aggregate already-captured facts; do not
re-mine transcripts, dispatch a subagent, read raw session files, or search transcripts with
`grep`, `rg`, `jq`, or `awk`. The evidence sources are the `facts` and `transcript` inputs of
`retrospective_save`'s `compose` argument and the `journal_entries` tool. Evidence that neither can
answer is `unknown — no journal`, never a guess.

1. Read the agent's own journal oldest-first and check for an existing retrospective. Capture a
   material new observation before filing a follow-up issue. Preserve entry-level repository tags.
2. Generate routine repository and transcript facts with the approved composer: pass `compose` to
   the `retrospective_save` MCP tool and preview the composition with `dryRun`, never a CLI. Save the preview by passing its
   `previewToken` to `retrospective_save` (no markdown). `compose` takes a concise `narrative`,
   `date`, `issues`, `prs`, `description`, `facts`, `transcript`, `tools`, and `architecture`; the
   server adds the session, repositories, outcome, and coverage from the call's own `workOutcome`,
   `feedbackCoverage`, and `repositories`. Pass `compose.transcript.harnessSessionId` whenever the
   harness session id differs from the call's `sessionId`. The composer builds the CI failures and
   sandbox audit sections from the session's hosted journal entries alone, so do not rerun
   collectors to fill them. A session unknown to the journal reports both as unavailable, not as
   none observed. Put sensitive values only in
   `compose.knownSensitiveValues`, or `knownSensitiveValues` for a markdown save. Keep exact factual
   section markers generated, preserve unavailable counts, and never replace missing evidence with
   invented zero statistics. Do not paste raw collectors' output or manually reconstruct facts.
3. Record work outcome, feedback coverage, and delivery independently. Success, failure,
   cancellation, timeout, no-change, and policy refusal each need truthful terminal reporting.
   Missing or truncated sources are unavailable/partial; durable interactive pending remains pending.
   Autonomous completion requires the controller's acknowledged terminal readback or visible block.
4. Report observed first-party tool and architectural behavior with concrete evidence and a
   disposition, including useful resolved outcomes and rejected proposals. None observed requires
   the inspected scope. Not assessed or unavailable requires a reason. Do not turn a plausible
   cause into an observed diagnosis or infer permission decisions from requests.
   For applicable configured tools, report used versus skipped/unavailable with reasons, the owning
   workflow or command-catalog entrypoint, and terminal result/action, especially pr-shepherd and no-mistakes.
5. Keep the top five findings or improvements in the human prose. The bounded durable evidence can
   retain additional relevant findings; a prose limit is not permission to silently discard them.
   Separate recurring root causes from one-off noise and preserve existing issue references.
6. Check for an existing retrospective with the `retrospective_check` MCP tool and save with
   `retrospective_save`, never a CLI. A revision of changed content needs a new `sourceEventId`.
   Interactive outages use the approved bounded private
   outbox with visible pending count; failed persistence blocks capture. Autonomous reporting stays
   online and never uses that outbox to authorize an attempt or completion. Report the acknowledged
   record/receipt, or the actual pending/blocked state and next replay action.

Read [ci-failures](references/ci-failures.md) when the session observed CI failures, and
[sandbox-audit](references/sandbox-audit.md) when it hit denied or escalated commands.

Use raw evidence only for local verification. Save only bounded structured facts or redacted summaries
in durable retrospectives; never embed unredacted logs, command output, environment dumps, provider
payloads, or transcript content there. Exclude secrets. Consumer wrappers own providers, commands,
report schema, retention, trusted runner mode, and issue routing; they cannot weaken this minimization
boundary.
