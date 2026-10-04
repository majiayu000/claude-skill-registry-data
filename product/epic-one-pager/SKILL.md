---
name: epic-one-pager
description: Write a concise Notion 1-pager for a Jira epic (goal + metrics, orientation diagram of the systems, ticket dependency plan, product-terms acceptance criteria, notes) with native Notion mermaid diagrams. Use when asked to "write a 1-pager", "render a one-pager in Notion", "explain this epic", or document a body of ticketed work for a wiki.
---

# Epic 1-pager in Notion

Write one page that stakeholders read in two minutes. Cover the goal, measures, systems, work, and definition of done. The model was a 1-pager for an epic that makes a bot pick up every flaky test on its own. Match its tone and density.

## The brief

This brief produced the model page. Project names are replaced with placeholders. Use it when the user gives no brief. The user's brief wins when details differ.

> Now please render a 1-pager in notion, under: <parent page> based on the <work>. Express clearly what the goal of the work is (<e.g. 100% of flakes should be picked up by the bot>) and how to measure success. Then do a little orientation section where you conceptually introduce the key pieces of the puzzle, introing the systems and diagramming them out (inline HTML diagrams with /narrative-diagram with animations).
>
> Then, do a high-level overview of the actual work, draw out the dependency diagram and have it animated. Explain in PRODUCT terms what the AC is (waht is the PRODUCT result, regardlss of how one gets there? Ie, no impl details needed - although guidacne to look in specific areas and where to learn into would be good).

Two changes followed. The HTML diagrams became native Notion mermaid. The “100%” slogan became a scoped number.

## Workflow

1. **Load tickets.** Fetch the epic and every child: `acli jira workitem view KEY --fields summary,description,parent,issuelinks --json`. Descriptions do not create dependencies; only Blocks `issuelinks` draw arrows.
2. **Ground systems.** Name only records, services, and entry points that exist in the code today. Everything else is planned.
3. **Draft the page.** Fill `references/page-template.md` in the fixed order below. Write every sentence to `references/writing.md`. Draw both diagrams to `references/diagrams.md`.
4. **Check before publishing.** Run the self-check in `references/writing.md`.
5. **Publish and inspect.** Use `notion-create-pages`, then `notion-fetch`. Make sure that every diagram is a real ` ```mermaid ` block. To fix an existing page, use `notion-update-page` with `update_content` find-and-replace edits so the user's hand edits survive.
6. **Report.** Give the URL and open questions. Do not re-summarize the page.

## Fixed section order

- **Goal:** State the end behavior, number, scope caveat, and metrics.
- **Orientation:** Explain current systems and the remaining gap.
- **Plan:** Show ticket tracks and real dependencies.
- **Acceptance criteria, in product terms:** State observable outcomes and where to learn more.
- **Notes:** Record legends, overlaps, open questions, dependencies, and non-goals.
- **Source tickets:** Link the epic and child tickets.

## Top pitfalls

- Verify the topic when the session contains several artifacts; do not choose because the question timed out.
- Verify `issuelinks` and direction; descriptions do not create dependencies.
- Keep headings short, not full sentences, and keep prose concise.
- Keep implementation details out of acceptance criteria.
- Do not pad the page with history, rosters, or unasked timelines; state empty sections in one line.
- Apply diagram shape, color, and label rules from `references/diagrams.md`.

## References

| File | Open it when |
|---|---|
| `references/page-template.md` | Drafting the page and checking content rules. |
| `references/diagrams.md` | Naming, styling, or drawing diagrams. |
| `references/writing.md` | Drafting prose and running the prose self-check. |
