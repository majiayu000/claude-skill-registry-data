---
name: external-campaign-triage
description: Track state across many candidate issues, PRs, and repos in a multi-repo external open-source contribution campaign, using a local tracker instead of GitHub labels. Use when scouting, claiming, implementing, or following up across many third-party repos in an ongoing campaign, and always before posting any status-check comment on a stalled external PR.
---

# External Campaign Triage

Use this for a campaign tracker repo (e.g. `open-source-tracker`) running many concurrent candidate issues/PRs across third-party repos we don't own. `ai-agent-pr-metadata`'s `picked by agent` / `agent:<model>-<effort>-<role>` label convention only works on repos we own or collaborate on; it cannot be applied to someone else's issue or PR. This skill defines the state machine and metadata that replace it: JSON records in the tracker repo, not upstream labels.

## State machine

Each candidate moves through these states, recorded in the tracker, never skipped backward:

`scouted` → `viability_checked` → `claimed` → `implementing` → `in_review` → `merged` | `abandoned` | `stalled_awaiting_maintainer` | `silenced`

- `scouted`: a candidate issue/repo identified, not yet vetted.
- `viability_checked`: `external-pr-viability` ran; only proceed past this state if it passed.
- `claimed`: an agent has started work. Check the tracker for an existing `claimed`/`implementing`/`in_review` record on this candidate before starting — the tracker file is the source of truth for "already picked" since no GitHub label exists to signal it.
- `implementing`: code, tests, and PR draft in progress, following `subagent-pipeline` roles.
- `in_review`: PR opened (`external-pr-style` for the description) and awaiting maintainer response.
- `stalled_awaiting_maintainer`: reached only through the Maintainer Follow-Up Guardrail below. Terminal until a maintainer responds; never re-entered from itself.
- `merged` / `abandoned`: terminal, normal outcomes.
- `silenced`: terminal, reached whenever a maintainer responds negatively to any contact (see Guardrails).

## Tracker record

One JSON record per candidate:

```json
{
  "id": "owner-repo-issue-123",
  "repo": "owner/repo",
  "url": "https://github.com/owner/repo/issues/123",
  "state": "in_review",
  "history": [
    {"state": "scouted", "at": "2026-09-01T10:00:00Z", "role": "scout", "model": "sonnet5-medium"},
    {"state": "viability_checked", "at": "2026-09-01T10:20:00Z", "role": "scout", "model": "sonnet5-medium"},
    {"state": "claimed", "at": "2026-09-01T11:00:00Z", "role": "implementer", "model": "sonnet5-medium"},
    {"state": "in_review", "at": "2026-09-02T09:00:00Z", "role": "implementer", "model": "sonnet5-medium"}
  ],
  "maintainer_contact": {"follow_ups_sent": 0, "last_follow_up_at": null, "maintainer_response": null},
  "silenced": false
}
```

Every state transition appends a `history` entry with `role` (`scout` / `implementer` / `reviewer` / `fixer`, mirroring `subagent-pipeline`'s roles) and the resolved `model` — the same traceability `ai-agent-pr-metadata` records as an `agent:<model>-<effort>-<role>` label, kept as tracker-JSON metadata here because there is no upstream label surface to write it to. Don't assume this exact schema matches the live `open-source-tracker` repo's own field names; check its current schema before writing to it.

## Maintainer follow-up guardrail (critical)

Real incident: two unrelated third-party maintainers responded with hostile pushback after receiving a second "just checking in" comment on their own open PR with no prior maintainer response — one said to stop chasing PRs as a last warning, the other said time is a gift, not something people are entitled to. Treat this as a standing constraint, not a style preference:

- Send at most one polite status-check comment per stalled PR, and only after 10 or more days of maintainer silence since the PR was opened or last touched by a maintainer.
- Never post a second "checking in" or "following up" comment on the same PR. One touch, then silence and patience are the default.
- Never state an exact elapsed day count in the comment itself (e.g. "it's been 8 days"). Precise counts are what make a message read as bot-generated even when a human typed it — say "it's been a while" or similar instead.
- After that single follow-up, set the record's state to `stalled_awaiting_maintainer` and stop nudging it. Do not re-check or re-comment on a fixed schedule.
- Never wire follow-up comments into an automated periodic reminder loop. Only escalate a specific stalled candidate when a human explicitly asks for that specific escalation (then use `hitl-blocker` if the escalation itself needs a human-held action).
- If a maintainer responds negatively to any contact (asks to stop, expresses annoyance), record the response verbatim in `maintainer_contact.maintainer_response`, set `state` to `silenced` and `silenced: true`, and treat that **maintainer as silenced org-wide, not just repo-wide**: the same person commonly maintains several repos in the same org, and a maintainer annoyed on one repo is the same maintainer on the others. Apply the silence to every repo in that maintainer's org, not only the one where the pushback happened — no further unsolicited comments to that maintainer anywhere in the org, ever. This mirrors the `silenced_repos.json` convention already used in `open-source-tracker` — check that repo's current schema before writing to it, don't assume this skill's field names match it exactly.

## Workflow

1. Scout a candidate; run `external-pr-viability` before writing any code. Record `scouted` then `viability_checked`.
2. Before claiming, check the tracker for an existing non-terminal record on the same candidate to avoid duplicate work across concurrent agents.
3. Record `claimed`, then run the implementation through `subagent-pipeline`'s cold-start roles, updating `history` at each role handoff.
4. Open the PR with `external-pr-style`; record `in_review`.
5. If the PR goes quiet, apply the Maintainer Follow-Up Guardrail before doing anything else.
6. On merge, close-without-merge, or a negative maintainer response, record the terminal state and stop touching that candidate.

## Guardrails

- Never apply a `picked by agent` or `agent:*` GitHub label to a repo we don't own or collaborate on — the tracker record is the only claim mechanism here.
- When this tracker's own PR/commit (against the campaign repo) references a third-party PR/issue, never write the unbroken `owner/repo#123` pattern (or a full `github.com` URL) in the PR title, body, or commit message — both forms trigger a public "mentioned this pull request" cross-reference on the target's timeline, exposing the campaign tool. See `ai-agent-pr-metadata`'s cross-reference-leak guidance for the confirmed-safe forms (inline code backticks in PR/issue bodies; a broken adjacency like `repo PR #123` in commit messages). This only applies to what you type into a PR/issue/commit-message field — a tracker markdown/JSON file's own content is not scanned for cross-references.
- See `subagent-pipeline`'s Guardrails section (the "Public issues, PRs, comments, and handovers..." bullet) for the parallel credential-redaction discipline that applies to every public comment this skill causes an agent to post.
- Do not skip `viability_checked` to save time — an unvetted candidate wastes the same implementation effort `external-pr-viability` exists to avoid.
- Do not delete or rewrite `history` entries; append only. The tracker is an audit trail, not a status field to overwrite.
- Concurrency ceiling: Maintain a recommended maximum of 3 open external PRs (`in_review`) **per third-party repository**, not a total across the whole campaign — a healthy multi-repo campaign will legitimately have far more than 3 open PRs in aggregate. Submitting more than 3 simultaneous unsolicited PRs into any single repository dramatically increases the likelihood of being flagged as an automated spammer by that project's maintainers or platform abuse detection. Space new PRs into the same repo (and the same org, since a maintainer's patience is often org-wide, not repo-scoped — see the Maintainer Follow-Up Guardrail) rather than opening all 3 at once.
