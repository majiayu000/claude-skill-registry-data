---
name: founder-os-mom-test-auditor
description: FounderOS Mom Test interview auditor. Splits a customer interview transcript into founder and interviewee turns, has Laya tag each turn (compliment, hypothetical, pitching, past behaviour, commitment signals for time, intro and money), then writes a feedback report that cites turn numbers. Triggers when a founder at stage 3 shares an interview transcript or notes, or asks "audit my interview", "was this a good interview", "did I pitch too early".
plugin: behalfbot-founder-os
enabled_when: "chassis.config.yaml modules.founder-os.enabled == true"
type: auditor-skill
stage: 3
gate: stage-3-discovery
question_set: mom-test
---

# Mom Test interview auditor

This is step 7 of `interviews-without-fooling-yourself`: the line-by-line audit.
Laya pre-tags every turn. You confirm the tags, and you write the feedback. The
Mom Test is Rob Fitzpatrick's; use his terms and point the founder at his book
for the full argument.

## When to run

- The founder has a transcript or detailed notes from one interview, ideally
  within a day of the call.
- Save it first, so labels and audits have a row to hang on:
  `add_interview(founder_id, interviewee=<pseudonym>, notes=<transcript>, conducted_on=<date>)`.
  `interviewee` is a label like `studio-owner-3`, never a name or contact.
  Set `commitment` only if the transcript plainly shows it; otherwise leave it
  `none` and record the audit's view in the audit findings.
- The transcript should be `Speaker: text` lines. If it is prose notes, ask
  the founder to mark who said what, or run it anyway and tag it yourself.

## Laya pass

```bash
python3 "$FOUNDER_OS_DIR/scripts/audit.py" mom-test \
  --founder-id <founder_id> --interview-id <interview_id> \
  --founder "<founder's speaker label>" --lang <en|pt|...> --record
```

Always pass `--lang`; it picks the checkpoint. The output is JSON:

- `turns[]`: `n`, `speaker`, `role` (founder or interviewee), `text`, `tags`
  (per tag `value`, `p`, `trust`), `patterns` and `label_ids`.
  - `patterns.bare_yes_no`: the answer opened with a bare yes or no. Mark it
    doubtful; the question before it was probably leading.
  - `patterns.closed_question`: the founder asked a yes/no question.
  - `patterns.hypothetical_wording`: the interviewee said would, maybe,
    probably, everyone, people and the like.
- `summary`: turn numbers per tag, `founder_talk_share`,
  `pitched_before_first_fact`, `facts_vs_struck`, and the commitments:
  - `commitment_candidates`: commitment tags on turns that are not
    hypothetical, by `time`, `reputation` (an intro) and `money`.
  - `commitment_talk_only`: commitment tags on hypothetical turns. "I'd pay
    twenty euros for that" is talk about paying, not a payment. Never count
    these.
  - `suggested_commitment`: the strongest candidate, or `none`.

Every tag in this set has `trust: unmeasured`. No accuracy has been measured on
it yet. Read each flagged turn yourself before you repeat Laya's call, and look
for turns it missed. In a first live run on the english checkpoint,
`commitment_money` fired on almost any turn that mentioned money, and
`past_behaviour` missed most dated incidents. Check both every time.

## Claude pass

Write the report in this order, citing turn numbers for every claim
("turn 4", "turns 6-8"):

1. **Verdict in one line.** Could anything in this interview have changed what
   they build? If not, say so.
2. **Facts that survived.** Dated incidents, money or hours already spent,
   tools in use. Quote the short phrase and give the turn.
3. **Struck and flagged.** Compliments (struck, carry no information),
   hypotheticals and generic claims (flagged fluff), bare yes/no answers
   (doubtful). Count facts against struck lines.
4. **The founder's side.** Pitching, especially before the first fact;
   leading or future-tense questions, each with a rewrite about the recent
   past; talk share above about a third.
5. **Commitment.** What the interviewee agreed to do next and what it costs
   them: time, reputation (an intro) or money. "Keep me posted" is none.
6. **Next interview.** Two or three concrete changes.

Do not soften it. A warm conversation with no facts is a failed interview, and
the founder is better off hearing it now.

## Without Laya

If `mode` is `claude-only`, `degraded_reason` says why. The turns are split and
numbered and the patterns are filled; `tags` is null. Tag each turn yourself
with the same tags, using the question text in `laya/mom-test.json`, and write
the same report. Say in one line that Laya was unavailable. Write no labels:
labels are Laya's judgments, and there are none.

## Label capture

After the report, show the founder the tags you disagreed with and ask them to
confirm. Then record every tag they accepted or rejected:

```bash
python3 "$FOUNDER_OS_DIR/scripts/labels.py" accept --founder-id <id> --by <founder_id> <label_id> ...
python3 "$FOUNDER_OS_DIR/scripts/labels.py" reject --founder-id <id> --by <founder_id> <label_id>
```

A rejected yes/no tag flips. When the founder says "that's right" about the
report as a whole, accept the tags the report relied on. Tags nobody reviewed
stay unreviewed; never accept them in bulk to fill the set. Each reviewed tag
is a fine-tuning example. The cross-founder export is operator-only and is
never run from a founder session.

## Ledger writes

- The `interviews` row, before the audit (see When to run).
- Labels, one per turn and tag, from `audit.py --record`; corrections from
  `labels.py`.
- One `audits` row with your verdict:
  `record_audit.py --table interviews --id <interview_id> --auditor claude --check mom_test --verdict pass|flag|fail --findings "<one paragraph with turn numbers>"`.
- Never change `commitment` or `earlyvangelist` on the interview from here. The
  interview is written once; `suggested_commitment` goes in the audit
  findings, and the earlyvangelist call belongs to
  `founder-os-earlyvangelist-qualifier`.
