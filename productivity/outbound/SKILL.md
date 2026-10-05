---
name: outbound
description: Verify an artifact about to leave the building — partnership brief, pitch page, press release, customer email, RFP response, or any document sent outside the org. Six checks before send — premise, confidentiality forward-test, evidence class, cold read by recipient personas, AI read, tone metrics — returning what to change with replacement copy.
when_to_use: "before sending, check this before it goes out, outbound review, pitch review, is this safe to send, cold read, how does this land, review before I email them, partnership brief review, 发出去之前检查, 对外物料审查 — NOT for code review (/review-pr), the corrections meta-file (/audit), or blog/ad copy quality (/blog-audit, /ads-audit)"
user_invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - WebFetch
  - WebSearch
  - Task
---

# Outbound — verify before it leaves the building

Clade's business skills all **produce** artifacts. This one **verifies** one, applying
the same trust loop the repository gets — evidence, calibrated verification, correction
learning — to the things that go outside, which usually carry more risk than a commit.

## The premise

An outward-facing artifact fails in ways a document review does not catch, because
the reviewer is normally the author, and the author cannot see:

- that they asked the recipient for something the recipient does not sell;
- that a sentence which reads as candour reads as leverage to the person receiving it;
- that a third party's confidential detail is sitting in a paragraph about something else;
- that a joke is wrong in front of the only audience qualified to notice;
- that an LLM summarising the page will describe their honesty as a tactic.

Run the six checks. Report findings with replacement copy, never advice about copy.

## Inputs

- **The artifact** — a file path or URL.
- **The recipient** — who receives it, and what they can be assumed to know already.
- **The relationship state** — first contact, second meeting, existing customer, under NDA or not. This changes what is safe to say more than anything else.

If the relationship state is not supplied, ask. It is the difference between a
disclosure and a leak.

## The six checks

### 1. Premise — can the recipient actually do the thing you are asking for?

The cheapest fatal error. Verify every capability you attribute to the counterparty
against a **primary source**: their API spec, docs index, pricing page, ToS. Not their
marketing, and not your memory of a conversation.

> Found in the field: three separate asks for reverse image lookup from a vendor whose
> search endpoint accepts exactly `query`, `location`, `language` — checkable in one
> call. Sending it would have disproved the document's own central claim, which was
> that its author had done the reading.

### 2. Confidentiality — the forward test

For every fact about a third party, ask: **how does this read when the recipient
forwards it to their investor, their counsel, or the person it is about?**

Flag without exception: verbatim quotes from a named person describing their own
weakness · ownership percentages · proprietary volumes and metrics · contract status ·
internal de-prioritisations · anything implying a customer is dissatisfied. Then check
whether the *combination* of non-identifying details re-identifies the subject.

Separately: does the artifact claim something about a third party that is **not true**?
Authors smooth "we asked for X" into "we have X" under deadline pressure.

### 3. Evidence class — voiced, visible, or speculative

Label every claim about what a third party needs:

| Class | Meaning |
|---|---|
| `voiced` | They said it. Cite where. |
| `visible-in-workflow` | Observable in what they do; they never said it. |
| `speculative` | You are extrapolating. Say so **in the artifact**, not just in the review. |

An artifact that labels its own speculation is more persuasive than one that does not,
because the unlabelled parts become credible by contrast.

### 4. Cold read — personas with no context

Spawn one agent per plausible reader, each with a distinct role, incentive and
professional reflex. For a company: the executive who decides, the operator who would
be assigned the work, the communications lead who thinks about how things leak, and a
skeptic whose default answer is no.

Give them the artifact and **no other context about the sender**. Ask each for: first
impression in twenty seconds, would-you-reply, what earned trust (quoted), what made
them wince (quoted, with severity), and what they would actually do.

The signal to watch for: **when every reader writes the same counter-offer, that
sentence is the real ask — write it yourself and keep the credit.**

### 5. AI read — the check nobody runs

Recipients paste documents into an LLM. Do it first, with the prompt they would use:

> *"Summarise this for a busy executive. What is being asked for, what is offered, what
> should they be careful about, and be blunt about any hidden agenda you detect."*

**Expect it to be more hostile than any human reader.** An LLM cannot weigh sincerity;
it pattern-matches *voluntary disclosure early in a sales document* onto *disarming
tactic*. The strongest move in a document is often the one it flags as manipulation.

Two things to fix from the output:

- **Words you handed it.** Self-deprecating phrasing gets escalated. One artifact wrote
  "before we had any right to"; the model returned "unauthorized pilots".
- **Facts it invented.** If a summariser hallucinates against your document, the
  document left room. Close the gap rather than assuming the reader will be careful.

### 6. Tone metrics — count, do not intuit

Authors cannot hear their own tics. Count them:

```bash
# humility constructions, hedges, and the we/you balance
python3 - <<'EOF'
import re, html, sys
t = html.unescape(re.sub(r'<[^>]+>', ' ', open(sys.argv[1]).read()))
t = re.sub(r'\s+', ' ', t)
for label, pat in [
    ('"we would rather"', r"we would rather|we'd rather"),
    ('"we think"',        r"\bwe think\b"),
    ('"honest/plainly"',  r"\bhonest|honestly|plainly\b"),
    ('"we"',              r"\bwe\b"),
    ('"you/your"',        r"\byou\b|\byour\b"),
]:
    print(f"{label:22s} {len(re.findall(pat, t, re.I))}")
print(f"{'words':22s} {len(t.split())}")
EOF
```

Rule of thumb: any humility construction appearing **more than twice per thousand
words** has stopped reading as modesty and started reading as a formula. A `we` to
`you` ratio far above 1 means the artifact is about the sender.

## Output

A revision plan. For each finding: the current text verbatim, the replacement verbatim,
which check caught it, and severity. Then a decision on the ask itself — keep, soften,
or replace — with the replacement written out.

Only report a change if a check actually caught it. A long list of style preferences
buries the two findings that matter.

## Refusals

Do not use this skill to make a misleading artifact more persuasive. If a check finds
a claim that is false, the fix is to remove the claim, not to soften the wording. If
confidential third-party material is present, the fix is deletion — the author's
judgment that "they won't mind" is not a finding this skill accepts.

## Maturity

This shape has been exercised on a small number of real artifacts. Treat the six
checks as load-bearing and the ordering as provisional. Record what each check caught
in `corrections/rules.md` so the ordering can be revised on evidence.
