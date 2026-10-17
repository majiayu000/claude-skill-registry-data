---
name: founder-os-earlyvangelist-qualifier
description: FounderOS earlyvangelist qualifier. Checks one interviewee against Steve Blank's five earlyvangelist criteria (has the problem, knows it, is looking for a fix, has built a workaround, has or can get budget) with Laya, and escalates anyone meeting four or more to Claude and then Sean. Triggers when a founder at stage 3 asks "is this person an earlyvangelist", "who are my early adopters", or after a Mom Test audit turns up a strong interview.
plugin: behalfbot-founder-os
enabled_when: "chassis.config.yaml modules.founder-os.enabled == true"
type: auditor-skill
stage: 3
gate: stage-3-discovery
question_set: earlyvangelist
---

# Earlyvangelist qualifier

Earlyvangelist is Steve Blank's term, from *The Four Steps to the Epiphany* and
*The Startup Owner's Manual*. Credit him and point the founder there. The five
criteria roughly build on each other: the person has the problem, knows they
have it, is actively looking for a fix, has already cobbled one together, and
has or can get the money to pay for a real one.

Laya screens. It never decides. The stage 3 gate wants every earlyvangelist
backed by interview evidence, checked by Claude and then Sean.

## When to run

- On one saved interview (an `interviews` row), after its Mom Test audit.
  Criteria met in a conversation full of hypotheticals mean little.
- Run it for every interview in the founder's target segment, not only the
  ones the founder liked.

## Laya pass

```bash
python3 "$FOUNDER_OS_DIR/scripts/audit.py" earlyvangelist \
  --founder-id <founder_id> --interview-id <interview_id> --transcript \
  --founder "<founder's speaker label>" --lang <en|pt|...> --record
```

`--transcript` sends only the interviewee's words; the founder's pitch
describes the problem too and would score as if the interviewee had said it.
Drop it for prose notes, and warn the founder that notes in their own words
make this weaker.

The output has `criteria` (per criterion `value`, `p`, `trust`, and on long
text an `excerpt` of the passage that carried the answer), `met`, and
`escalate`, which is true at `escalate_at` (4) or more.

## Claude pass

For each criterion, find the evidence in the interview: a quote and the turn it
came from. A criterion counts only with a past-tense, specific quote behind it,
whatever Laya said. "I'd pay for that" is not budget; "I pay a bookkeeper 300 a
month to chase these" is.

Then:

- **4 or 5 confirmed:** escalate. Tell the founder this looks like an
  earlyvangelist, list the quote per criterion, and say that Sean signs off
  before it counts at the gate. Suggest the next ask that would prove it:
  a paid pilot, a pre-order or a deposit.
- **3 or fewer:** not an earlyvangelist yet. Name the missing criteria and the
  question for a follow-up that would settle each one.
- Where you and Laya disagree, say so. That disagreement is the most useful
  label in the set.

## Without Laya

If `mode` is `claude-only`, `criteria_to_check` lists the five questions. Answer
each from the interview yourself, with a quote and turn, and apply the same
four-or-more rule. Say in one line that Laya was unavailable. Write no labels.

## Label capture

Show the founder the five answers and ask which are wrong. Record every one
they accept or reject:

```bash
python3 "$FOUNDER_OS_DIR/scripts/labels.py" accept --founder-id <id> --by <founder_id> <label_id> ...
python3 "$FOUNDER_OS_DIR/scripts/labels.py" reject --founder-id <id> --by <founder_id> <label_id>
```

When Sean reviews an escalation, record his calls with `--by sean`. Do not
accept tags nobody looked at. The cross-founder export is operator-only.

## Ledger writes

- Labels, one per criterion, from `audit.py --record`; corrections from
  `labels.py`.
- One `audits` row on the interview:
  `record_audit.py --table interviews --id <interview_id> --auditor claude --check earlyvangelist --verdict flag|fail --findings "<criteria met, with quotes and turns>"`.
  `flag` means escalated to Sean; `fail` means fewer than four.
- After Sean confirms, his own `audits` row with `--auditor sean --verdict pass`.
  Sean writes it himself: `--auditor sean` is operator-only
  (`FOUNDER_OS_OPERATOR=1`), and no skill sets that.
- Never set `interviews.earlyvangelist` from this skill. The ledger has no call
  to change an interview after it is written, and the gate reads the audits.
