---
name: define-venture
description: Establish or revise the venture-definition, the one plain-language account of what the venture is and does as a business (purpose and customers, what it provides, how it works, the commercial relationship, current scope). Use at the start of strategy work, when a choice changes what is sold, how it operates or whom the whole venture serves, and to reconcile the definition after commercial choices.
---

# define-venture

Writes [`venture-definition`](../../../../.group/contracts/venture-definition.md) under the shared [document rules](../../../../.group/contracts/document-rules.md).

## When and what it decides

Run when no operative definition exists, when owner material changes what the venture is, or after other Strategy choices to reconcile. The question: **what is this business, as a whole, such that every other choice can be checked against it?** The definition can be written before products, prices or targets are settled; it states what is known and marks what is not.

Evaluating a definition, developing a revised one and adopting it are different: this skill develops and proposes; the owner adopts.

## Inputs and authority

- **Owner material** (request, attachments, notes): the authority on identity, purpose and owner-set scope. Quote it; never paraphrase it into a stronger claim.
- **Mandate** (Governance), when it exists: purpose constraints and horizon override worker proposals.
- **Capability state**: Product `documentation` for what exists, `roadmap` for what is planned; actual releases and access.
- **Current Strategy documents**: read only where their choices change the venture's purpose, offering structure, operating mechanism, commercial relationship or scope.
- An existing document that already performs this role is adopted at its path and owner; supplied owner material stays an input snapshot.

## Method

Record sources, exact owner quotes and calculation premises in the relevant table’s basis or source cells. Carry decision status in its status column and the document’s role; prose states choices and ambition directly.

1. **Recover perspective and ambition first.** Read the owner's observations, worldview, convictions and intended reach before inventorying products. Write Perspective and ambition with the owner's view at full strength and exact quotes in its basis line. Apply [venture coherence](../../../knowledge/venture-coherence-and-value-mechanisms.md), Developing perspective into purpose and ambition.
2. **Develop what the perspective makes possible.** Originate useful applications and offering families within the owner's direction. Connect purpose to customer progress, operating mechanism and commercial exchange using [venture coherence](../../../knowledge/venture-coherence-and-value-mechanisms.md) §1. Develop a coherent scope beyond the current offer; record each part's status and basis in Scope and current form.
3. **Relate the parts.** Name the offering families and how they connect: successive jobs of one customer, one capability across markets, or an integrated system (§2 of the same knowledge). Name only connections that exist or are explicitly planned.
4. **Explain the operation and the exchange** at the level a newcomer needs: product sale, service engagement, access, use. Name the roles of AI, people and the customer where they matter. Never invent terms, prices or live delivery capability; reference `revenue-model` and `offer-catalogue` when they exist.
5. **Synthesize the whole.** State what the venture is and the possibility it pursues in the Conclusion. Develop the mechanism in the body so a reader can explain what the venture enables, how it works and why its activities form a business.
6. **Place focus inside ambition.** Keep the wider purpose and accepted scope in view. Scope and current form records the first commercial route, developed options and future capability in its Status and Scope note cells, with the supporting basis.

## Evaluate and correct

| Defect | Detect by | Correct by |
| --- | --- | --- |
| Perspective missing | Owner worldview or conviction absent | Recover it from owner material and develop its implications |
| Ambition reduced to the current offer | The current product defines the limit of purpose or reach | Restore the wider possibility and show how the first route serves it |
| Category label instead of a mechanism | Conclusion fits a hundred ventures | Rewrite around the actual operation and result |
| Planned capability in present tense | A part without an available source | Set status `future` or `proposed`; reword |
| Focus replaces scope | The definition names only the first target | Restore the accepted scope; add the focus as a row |
| Copied decisions | Prices, target numbers or entitlements in the text | Replace with a reference to the owning document |
| Invented attribution | A statement labelled owner with no quote, or a quote not in the material | Quote the actual passage or relabel as `[proposed]` |
| Parts without a whole | Sections list offerings that never connect | Name the connection or report that the parts form separate businesses, as a finding for the owner |

Then run `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy --owner-material {material}`; it checks structure, labels and quotes, not meaning. Do the restatement test yourself and record it in the work-result as self-review.

## Recovery

- **NeedData:** no material states what the venture does. Write the sections the material supports, leave the rest as open owner inputs naming the exact question ("What does the customer receive after purchase?"), and continue with any part that does not depend on it.
- **Conflict:** owner material and an accepted decision disagree (the brief names a line the mandate excludes). Keep the accepted decision, state the conflict and the owner decision needed.
- **Failure:** the check reports errors. Correct at the cited row and rerun.

## Example

Illustrative fixture: fictional founder material and venture.

Founder material: “An inspector's judgment should shape the report. Software should carry that judgment from the property to the client.” “We want own-format reporting to become the standard across independent practices and inspection firms.”

```markdown
## Conclusion
Brindlewick builds reporting tools and services that carry an inspector's judgment into a client-ready report in their own format. It pursues a profession in which inspectors can develop and share their practice without surrendering its expression to a software template.

## Perspective and ambition
An inspector's professional judgment is the organising principle of a report. Capturing findings once and assembling them in the inspector's structure makes that principle practical. Brindlewick's ambition is to establish own-format reporting across independent practices and inspection firms; the desktop app and template conversion service are its first commercial route.

Basis: [owner: "An inspector's judgment should shape the report. Software should carry that judgment from the property to the client."] [owner: "We want own-format reporting to become the standard across independent practices and inspection firms."]

## Scope and current form
| Part | Status | Scope note |
| --- | --- | --- |
| Desktop app | available | Capture and assembly; [owner: "The desktop app works"] |
| Template conversion | accepted direction | Preserves the inspector's structure; [owner: "convert an inspector's existing report template into ours"] |
| Professional practice library | proposed | Develop reusable examples of inspection judgment across report formats; [proposed] extends the founder's direction into a teaching and adoption route |
| Phone photo sync | future | [owner: "Photo sync from phones is planned for next year; it does not exist yet."] |
```

The practice library extends the ambition beyond the initial offer. Its scope status lets Product and Meaning develop it while the app's available capability remains precise.

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
