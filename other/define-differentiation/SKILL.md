---
name: define-differentiation
description: Develop the venture's customer-relevant advantage against what target buyers actually use or do instead, as advantage chains with capability availability, support and trade-offs. Use when targets or candidate segments are set or change, when capability or alternatives change, or before choosing a frame. Writes differentiation.
---

# define-differentiation

**Transformation:** target situations × actual alternatives × available and planned capabilities → [`differentiation`](../../../../.group/contracts/differentiation.md).

Document form, basis and requiredness: [document rules](../../../../.group/contracts/document-rules.md).

## When to use

- Initial direction: run on candidate `segments` (SEG ids) so choose-targets can compare winnability; iterate with choose-targets inside the same change.
- A target, capability (new release, roadmap change) or alternative (a new competitor, a buyer behaviour Evidence reports) changes.
- choose-frame or a consumer finds an advantage that does not hold.

The question this skill answers: **against what the target would actually do instead, which capability produces an outcome the buyer cares about, and for whom does it matter most?**

## Inputs and authority

| Input | Use | Authority |
| --- | --- | --- |
| `target-segments`, or candidate `segments` | The situations compared | market-strategist; reference by id |
| `customer-knowledge`, `market-landscape` | What buyers do now and which alternatives exist | Evidence; `[observed: …]` |
| `documentation` | Available capability | Product |
| `roadmap` | Planned capability, for explicitly future advantages | Product |
| Owner material | Capability and scope the owner states | Quote with `[owner: "…"]` |
| `venture-definition` | Scope the advantage serves | venture-strategist |

You decide which alternatives are real, which chains hold, which advantage leads and which trade-offs matter. You do not decide what the product can do: availability comes from Product or owner material. When a capability source is missing, the capability's availability is `unknown` and the gap is named as an open input.

## Method

Apply the relationships in [alternatives and value mechanisms](../../../knowledge/alternatives-and-value-mechanisms.md): alternatives first, because they define what counts as unique; then capabilities, value and best-fit buyer.

1. **Establish the alternatives per target situation.** For each target, ask what a buyer in that situation does today when the problem occurs and what they would do if the offer vanished. Include the status quo (tolerate, improvise, hire) whenever buyers would keep it; it is often the leading alternative for early buyers. Leave out competitors the target never considers. Each alternative row says why it is real for that target, with its basis in Basis.
   - Evidence names the alternatives → cite the observation in Basis.
   - No landscape yet → develop plausible alternatives from the situation, record the hypothesis in Basis and produce the comparison or research the decision needs.
2. **Trace each candidate chain.** capability → operational consequence → customer outcome → who values it most, under conditions the customer cares about. Stop a chain when a link fails: no consequence, outcome irrelevant in the situation, buyer without the situation.
3. **Sort the attributes.**
   - Shared with every credible alternative → table stakes: record as purchase requirements in Support and trade-offs, not as advantages.
   - Unique without consequential outcome → drop.
   - Common capabilities whose combination yields an outcome no alternative gives → one combination advantage.
4. **Set availability from source.** `available` only when documentation or owner material establishes it; `planned` for roadmap items, with the development or proof needed; otherwise `unknown`. A planned chain is recorded to inform bets; it never leads.
5. **Choose the leading value.** Prefer the available chain with the most consequential outcome for the best-fit buyer, compared with the next chain: say why it leads. The best-fit buyer is the situation where the outcome weighs most, not the whole market.
6. **Match each claim to support.** A quantified superiority needs the alternative, the condition and an observation or estimate on comparable work; otherwise describe the useful outcome qualitatively, put its hypothesis and basis in Support, and name the comparison to produce in Needed proof or development.
7. **Name the sacrifices.** For each advantage, what the venture gives up and whom that leaves badly served. These rows tell choose-targets and choose-frame where the advantage stops.

## How the conclusions change the document

- The Conclusion and Leading value state the leading chain and its best-fit buyer in one or two sentences, not a feature.
- Each alternative becomes an `ALT` row; each surviving chain an `ADV` row with `Against` naming its ALT ids; each ADV gets a Support and trade-offs row.
- A changed alternative re-runs steps 2–5 for the targets it touches; a changed capability updates availability and may change the leading value.
- Put sources, owner quotes and calculation expressions in the table's basis or source cells; carry decision status in the status column and document role. State the venture's choices and ambition directly in prose, qualifying only distinctions that change a decision.

## Example

Illustrative fixture: fictional venture.

Independent inspectors can carry findings into a client-ready report in their own format. The comparison is with assembling a report by hand (ALT-1) or adopting a fixed vendor format (ALT-2).

| ID | Capability | Availability | Against | Customer consequence | Target |
| --- | --- | --- | --- | --- | --- |
| ADV-1 | Capture findings and assemble the report | available | ALT-1 | A single capture supplies the report the client receives | SEG-1 |
| ADV-2 | Convert an inspector's existing template | available | ALT-2 | Preserve the professional's reporting approach while adopting the app | SEG-1 |
| ADV-3 | Phone photo sync | planned | ALT-1 | Bring phone photos into the assembled report | SEG-1 |

| Advantage | Support | Sacrifice | Needed proof or development |
| --- | --- | --- | --- |
| ADV-1 | [owner: "records findings on a tablet, and the app assembles a client-ready report"]; [hypothesis] time effect needs comparison | Desktop assembly step remains | Compare complete reports under the old and proposed workflows |
| ADV-2 | [owner: "convert an inspector's existing report template into ours"] | Conversion needs the customer's template | Inspect format fidelity on a converted sample |
| ADV-3 | [owner: "Photo sync from phones is planned for next year; it does not exist yet."] | Phone workflow requires development | Build and demonstrate photo sync |

ADV-1 and ADV-2 lead the commercial frame. ADV-3 supplies a development option for bets.

## Evaluate and correct

Before delivering, read the document as a buyer in the target situation and as choose-frame:

| Defect | Detect | Correct |
| --- | --- | --- |
| Feature list | An advantage row has no customer consequence, or the consequence restates the capability | Complete the chain or drop the row |
| Wrong alternative | A target buyer would not name the alternative | Re-derive from the situation; replace ALT rows |
| Status quo missing | Only competitor products appear for early buyers | Add the status quo alternative |
| Planned leads | Leading value rests on a `planned` or `unknown` ADV | Lead with an available chain |
| Invented superiority | A number without a comparison basis | Relabel `[hypothesis]`; name the measurement |
| Everyone fits | Best-fit buyer equals all targets | Name the situation where the outcome weighs most |

Run `python3 workers/strategy/positioning-strategist/tools/positioning.py check {path}/differentiation.md` from this skill's directory (or `python3 workers/strategy/positioning-strategist/tools/positioning.py check …` from the worker root) and `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy --owner-material {paths}` from the worker root. Fix every error at its row. A passing check establishes references, support rows and labels only; the evaluation above establishes fitness.

## Output

A candidate `venture/{v}/strategy/candidate/differentiation.md` following its contract, and in the answer: the leading value, which advantages are planned, the open inputs (alternatives or capability evidence) and the next observation that would strengthen the leading claim.

## Recovery

- No target or candidate segment: ask the router for segment-market; meanwhile state the situations the owner material describes as the scope and mark the result provisional.
- Capability sources disagree (owner material says available, documentation silent): availability `unknown`; name Product as the owner of the evidence.
- No alternative evidence: derive from the situation as `[hypothesis]`; name the market-landscape question for Evidence.
- Check fails on a reference: correct the ID or the referenced target; rerun.

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
