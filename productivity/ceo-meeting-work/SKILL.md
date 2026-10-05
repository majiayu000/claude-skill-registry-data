---
name: ceo-meeting-work
description: Use for meeting minutes, transcripts, silent meetings, preparation materials, summaries, decisions, and action items. Use ceo-calendar-invite for attendance decisions and ceo-work-tracking when an agreed action becomes tracked work. Load dingtalk-minutes before reading DingTalk meeting records.
metadata:
  managed_by: ceo-agent-service
  version: 1
---

# CEO Meeting Work

Load `ceo-meeting-work` for meeting preparation, records, silent meetings,
summaries, decisions, participant information, and follow-up work.

## Compose Operation Skills

Load the meeting operation Skill for the source platform before reading evidence.
Use the corresponding platform Skills instead of copying their commands here.

| Source | Operation Skills |
| --- | --- |
| DingTalk meeting or AI Minutes | `dingtalk-minutes` |
| Lark meeting record | `lark-vc` and `lark-minutes` |
| DingTalk linked document or file | `dingtalk-doc` or `dingtalk-drive` |
| Lark linked document or file | `lark-doc` or `lark-drive` |

Load the matching chat or document-comment Skill only when delivery requires it.
Use `ceo-calendar-invite` for attendance decisions and `ceo-work-tracking` when
an agreed action becomes tracked work.

## Read Evidence Deliberately

1. Identify the requested meeting outcome: preparation, summary, decision,
   alignment, task extraction, clarification, or information delivery.
2. Read the meeting identity and summary first. Confirm that the record is the
   meeting the request refers to.
3. Read tasks when ownership, delivery, or follow-up matters.
4. Read transcript only when speaker attribution, disagreement, ambiguity, or
   an unsupported summary requires it. Read only the portions needed, but
   continue through all pages needed to support the judgment.
5. Inspect linked material only when it changes or supports the requested
   judgment. Use the operation Skill for the material's actual platform and
   type.

The agent decides what evidence is needed and performs the business judgment.
The service supplies references and exact read commands without interpreting
meeting content. Use a supplied exact read command as given; use the loaded
operation Skill to discover any additional operation required by this workflow.
Do not infer meeting content from a title, preview, link, or stale conclusion.

## Decide And Deliver

Do not treat a silent meeting as an ordinary notification. Silence in the
source conversation does not remove a decision, task, unresolved question, or
requested information found in the meeting evidence.

- Produce only the decision, context, actions, and open questions needed by the
  current audience. A meeting summary is not a substitute for acting on clear
  tasks.
- Place every participant mention adjacent to that person's concrete task,
  question, decision, or information. Never put a wall of participant mentions
  at the start.
- Mention a participant once per relevant item. Do not duplicate the same
  mention as a heading or preamble.
- Do not assign a participant work that the meeting evidence does not support.
- Use canonical `no_action` when the meeting creates no decision, task,
  clarification, or useful information delivery.
- When an action is justified, use a canonical `proposal`; the operation Skill
  owns delivery mechanics and verification.

If decisive evidence is absent after using the applicable operation Skills, do
not guess. Ask for one specifically missing meeting material that the
participant can supply. Do not ask for a generic meeting recap or for material
the loaded operation Skill can read. If the dependency itself failed or access is
unavailable, report that dependency failure and do not invent a conclusion.
