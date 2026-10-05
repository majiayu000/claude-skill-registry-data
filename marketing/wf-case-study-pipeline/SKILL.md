---
name: wf-case-study-pipeline
version: 1.0.0
description: "Turn a customer conversation into a published case study and distribute it. Use when the user wants to create a case study from meeting notes or customer data and then promote it. Also trigger when the user mentions 'case study workflow,' 'case study pipeline,' 'customer story end-to-end,' 'write and distribute a case study,' or 'case study from meeting.' For the case study draft only, see case-studies."
---

# Case Study Pipeline

End-to-end workflow: pull meeting notes, draft the case study, clean it up, then push it across social and email channels.

## Stage 1: Gather Source Material

Ask the user for the source:
- **Granola meeting notes** → Load and run the `granola` skill to pull notes
- **Raw notes or transcript** → User pastes or provides a file
- **Existing draft** → User points to a file to refine

Extract: customer name (or anonymous label), problem, solution, results, quotes.

**Gate:** Confirm the key facts with the user before drafting. Flag anything that needs `[VERIFY]`.

## Stage 2: Draft the Case Study

Load and run the `case-studies` skill for the full drafting workflow:
- Branded or anonymous (ask if not specified)
- Problem → Solution → Results structure
- Pull metrics and quotes from source material
- Include proof points from brain files

**Gate:** User approves the draft.

## Stage 3: Quality Pass

Load and run the `tagore` skill on the approved draft. Fix the AI patterns and voice issues it flags.

**Gate:** Show the Tagore score. Get approval before distributing.

## Stage 4: Social Distribution

Load and run the `social-content` skill. Using the case study as source, generate:
- 1-2 LinkedIn posts highlighting key results
- 1-2 Twitter/X posts with compelling stats or quotes
- Any other platforms the user specifies

Pass forward: customer name (if branded), key metrics, the core narrative.

**Gate:** User approves social posts.

## Stage 5: Email Integration (Optional)

Ask: "Want to add this case study to an email sequence or send it standalone?"

If yes, load and run the `email-sequence` skill to:
- Draft a case study announcement email
- Suggest placement in existing nurture sequences (e.g., bottom-of-funnel proof)

If no, skip to summary.

## Summary

```
## Case Study Pipeline Complete

### Case Study
- [title] — [branded/anonymous] → [path]
- Customer: [name or descriptor]
- Key result: [headline metric]

### Social Posts
- LinkedIn: [count] posts → [paths]
- Twitter/X: [count] posts → [paths]

### Email
- [what was created, or "Skipped"]

### Next Steps
- [ ] Get customer approval (if branded)
- [ ] Publish case study
- [ ] Schedule social posts
- [ ] Add to website case studies section
- [ ] Reference in sales enablement materials
```

## Output Structure

All files go into a single project folder:

```
marketing/case-studies/[customer-slug]/
  case-study.md
  social-linkedin-1.md
  social-linkedin-2.md
  social-twitter-1.md
  email-announcement.md         (if email stage run)
  email-nurture-insert.md       (if email stage run)
```

Use the customer name (or anonymous descriptor) as the slug. Confirm with the user before creating files.

## Rules

- Each stage uses the full component skill
- Always gate between stages
- Never publish customer names or metrics without noting they need customer approval
- All claims must be verifiable from the source material — do not embellish results
- If the user wants to skip a stage, skip it
- All output goes into the project folder, not scattered across `marketing/`
