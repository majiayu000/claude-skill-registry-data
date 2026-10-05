---
name: split-intent-to-issues
description: Break an intent spec into 3-10 paste-ready tickets for Linear, Jira, or GitHub Issues. Use when a spec is ready to be worked on but it's too big for a single change, or when handing the spec to engineers who track work in tickets rather than reading intent specs. Each ticket links back to the outcome it delivers.
---

<what-to-do>

Load the active intent from `intent.md` in the project root first. That file is bound to this repository and remains the content authority even when `PATHMODE_API_KEY` is set. Only call `get_current_intent` when no local file exists.

Analyze the spec. The outcomes are the natural decomposition unit — each outcome typically maps to 1-3 tickets, depending on complexity.

For each outcome, propose tickets. A ticket has:

- **Title** — imperative verb phrase under 70 characters (e.g., "Add payment timeout monitoring", not "We should add a thing for timeouts")
- **Body** — 2-4 sentences: what changes, why, how to verify it works
- **Acceptance criteria** — concrete checklist linked to the outcome it delivers (copy from the spec, don't reword)
- **Outcome reference** — the outcome ID or text this ticket delivers

Output all tickets in a single block formatted for the user's tracker. Detect the tracker from these signals (in order):

1. If they ran `setup-pathmode-workflow`, use the answer captured there
2. If `.linear/`, `.jira/`, or `.github/ISSUE_TEMPLATE/` is present, use that
3. If `gh` CLI is available, default to GitHub Issues
4. Otherwise ask: Linear, Jira, GitHub Issues, or plain markdown?

For each tracker, output in its native format (markdown for Linear/Jira/GitHub all work; some teams have field conventions — surface them if found).

After the output, offer to create the issues automatically if `gh` (GitHub), `linear-cli`, or `jira-cli` is available. Do NOT create them without explicit confirmation.

</what-to-do>

<supporting-info>

## Why split by outcome, not by file

A common anti-pattern is splitting work by file or by component ("update PaymentForm.tsx", "update PaymentService.ts"). This produces tickets that are individually meaningless — they don't deliver an outcome by themselves.

Splitting by outcome means each ticket delivers something user-visible. The closing of the ticket proves an outcome moved from "draft" to "delivered." This is what makes the intent → ticket → code chain coherent.

## Sizing heuristic

- 1 outcome → 1 ticket if the work fits in ~1 day for one engineer
- 1 outcome → 2-3 tickets if it splits naturally (e.g., backend work + frontend work + observability)
- Multiple outcomes → 1 ticket only when they're trivially coupled (rare)

If a single outcome would need >3 tickets, that's a sign the outcome itself is too broad. Surface this back to the user: "This outcome is decomposing into 5 tickets — would it be cleaner to split the outcome into two before ticketing?"

## Output format

Default to a markdown block that works in all three trackers:

```markdown
### Ticket: [Title]

**Outcome:** [outcome text from spec]

[Body — what changes, why, how to verify]

**Acceptance:**
- [ ] [Criterion copied from outcome]
- [ ] [Test/check that proves the outcome]

---
```

Repeat per ticket. The `---` separator makes it easy to paste a batch.

## Tracker-specific notes

- **Linear** — Title goes in the title field; body + acceptance go in the description. If the user has a parent-child convention, group all tickets under a parent labeled with the intent title.
- **Jira** — Same shape. If "Epic" is the parent convention, propose a parent Epic with the intent title.
- **GitHub Issues** — Use a tracking issue with checkbox links to child issues for visibility.

## CLI shortcut (if available)

If `gh` is installed and the repo is on GitHub, offer:

```bash
# After user confirms:
gh issue create --title "[Title]" --body "[body]" --label "intent:[intent-id]"
```

If `linear-cli` or `jira-cli` is available, propose the equivalent command. Always show the command and wait for explicit confirmation before running.

## What this skill does NOT do

- Does not auto-create issues without confirmation
- Does not estimate story points or set due dates (team-specific; out of scope)
- Does not assign tickets to people
- Does not invent acceptance criteria — they MUST come from the intent's outcomes; the chain only works if the link is preserved

</supporting-info>
