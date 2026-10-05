---
name: senior-technical-product-evaluation
description: Evaluate senior technical candidates across resume screening, interview preparation, interview-transcript review, scorecard updates, and hiring decisions. Use for CTOs, technical directors, principal engineers, architects, AI leaders, and other senior technical candidates whenever product quality, personal technical ownership, AI judgment, product/customer judgment, operating responsibility, cross-functional leadership, target-role fit, or missing evidence must be assessed and handed to later interviewers. Requires public product research, responsibility-boundary inference, stage-aware evidence handling, and an actionable validation ledger.
---

# Senior Technical Product Evaluation

Evaluate the same seven objects from resume screening through interview review and the final hiring decision:

1. 产品/项目技术含金量。
2. 候选人个人技术贡献深度。
3. AI、算法、数据与评测判断。
4. 产品与客户判断。
5. 经营责任与创业型 ownership。
6. 跨职能领导与信息整合。
7. 目标产品与阶段匹配。

Keep product facts and personal facts separate. Public evidence can establish what a company or product did, but it cannot prove what the candidate personally decided, built, operated, or achieved. Use the same seven dimensions at resume and interview stages; change the evidence treatment and output by stage, not the evaluation target.

Read [references/methodology.md](references/methodology.md) completely before evaluating a candidate. It is authoritative for the seven-dimension formula and subdimensions, evidence grades and caps, missing-information state machine, gates, coverage calculation, continuous validation ledger, and exact output format. Do not invent alternative weights, an eighth scoring dimension, or a disconnected report format.

## Required inputs

Collect and preserve the best available version of:

- Current stage: resume screening, interview preparation, interview-transcript review, scorecard update, or final hiring decision.
- Target role mission, level, product stage, customers, technical priorities, operating expectations, and near-term problems.
- Current internal product definitions for each product line the role may serve. For Stardust/PreSeen, evaluate Friday and MorningStar separately unless the role is explicitly scoped to one.
- Candidate resume, employment dates, original product/project claims, and the actual function of current and recent roles.
- Interview transcript or AI minutes, exact candidate answers, interviewer questions, and inspectable artifacts when available.
- Existing scorecards or interview reviews and the prior round's conclusions, contradictions, uncertainty flags, and continuous validation ledger（持续验证清单）.
- Candidate-attributable technical decisions, implementations, alternatives, tradeoffs, failures, iterations, production duration, and measurable results.
- Operating metrics and resource decisions, including revenue, renewal, gross margin, cost, adoption, retention, or customer-value outcomes when relevant.
- Customer evidence and cross-functional decisions involving product, algorithm, engineering, sales, delivery, or operations.
- Public information about every material product during the candidate's tenure.
- Candidate public technical artifacts when available: GitHub/GitLab identity, representative repositories, upstream projects, commits, pull requests, reviews, tests, releases, and adoption signals.

If the target role, product line, candidate identity, tenure, or evaluation stage is unclear, state the working assumption and keep it as an unresolved validation item. Do not silently judge against a generic senior-engineer profile.

## Mandatory execution sequence

Follow this order:

1. **Identify the stage.** Select the resume-stage or interview/hiring-stage contract below. Interview preparation begins from the resume-stage evidence and ledger; transcript review and scorecard updates use the interview/hiring-stage contract.
2. **Inherit earlier evidence.** Read the resume, previous conclusions, scorecards, transcripts, and validation ledger. Preserve unresolved items, exact source text, prior states, and contradictions; do not restart the evaluation from zero.
3. **Define target-role tracks and gates.** Build the target capability map for every real hiring track the organization is willing to use, such as technical director and L4 architect. Declare each track's mission, level, responsibilities, and inapplicable gates before candidate scoring. Do not invent a fallback role merely to rescue a candidate.
4. **Build product fact cards.** Resolve each material product, research its tenure-aligned facts and contrary evidence, and separate product, platform, internal-project, and company-stack boundaries.
5. **Infer personal responsibility.** For each claim, show the likely owned part, inference basis, confidence, parts not attributable to the candidate, and the next verification question.
6. **Score all seven dimensions and route the candidate.** Use only the fixed formula and subdimensions in the methodology. Keep Friday and MorningStar fit separate. When the organization assigns people by fit rather than a fixed product scope, calculate both composites, select the better-supported primary product and responsibilities, name an adjacent alternative when useful, and never average them.
7. **Apply the missing-information state machine.** Use exactly the methodology states, preserve state history, and distinguish absence, demonstrated weakness, and contradiction.
8. **Update the continuous validation ledger.** Every unresolved or contradicted claim must become an actionable row with the next question, qualifying evidence, risky answer, owner, and current state.
9. **Apply gates and issue the stage-appropriate decision.** Apply gates per predeclared role track. A failed technical-director operating gate can block that track without blocking an accepted L4 architect track where operating ownership was predeclared inapplicable. Recalculate every contribution and total before finalizing.

## Internet research is mandatory

Research every product that materially affects the decision. A resume, interview statement, company name, existing scorecard, or internal table is only a lead.

For each product:

1. Resolve the exact entity from company, product name, dates, geography, product category, repository, and domain. If identity remains ambiguous, mark it unresolved rather than attaching a similarly named product.
2. Prefer primary technical and business sources, then add an independent source when available. Search for limitations, failed launches, weak adoption, incidents, discontinued products, and contradictory metrics as well as positive evidence.
3. Compare the product with alternatives available during the candidate's tenure. Current popularity does not prove historical leadership, and current documentation may describe capabilities added after the candidate left.
4. Record the direct URL, publication date, source type, supported claim, unsupported inference, and tenure alignment. A high-confidence product-leading claim requires at least two materially different sources, including one primary source.
5. Explain what buyers and users actually do, the product boundary and workflow, and where the candidate's claimed system sits before scoring technical quality.

For GitHub or other public-code evidence, use the methodology's representative-project protocol. Select relevant and representative projects first; then inspect project impact and candidate-attributable diff, commits, pull requests, reviews, tests, upstream merge, releases, and adoption. Forks, code volume, stars, and AI tools have asymmetric meanings and must not become simplistic personal scores.

Public product or company facts may support product technical value and context only. They never establish the candidate's personal ownership, technical depth, AI judgment, product/customer judgment, operating responsibility, or cross-functional leadership without candidate-attributable evidence. Do not transfer company scale, product features, financing, team quality, or leadership reputation into a personal score.

## Recent-function evidence is horizontal

Apply the candidate's actual recent function across every candidate-ability dimension: evidence from the most recent 0–3 years supplies at least 70% of the judgment, evidence from 3–7 years supplies at most 20%, and evidence older than 7 years supplies at most 10%. Do not create a separate recent-role dimension, and do not reallocate a missing recent share to older prestigious work.

When the recent function is mainly SRE, DevOps, quality, delivery, project management, or pure people management, score only the abilities actually proved. Titles and product adjacency do not establish current core-product, AI, architecture, product, customer, or operating ability. Always output the methodology's recent-function evidence table and state what older evidence proves and does not prove.

## Stage routing and output contract

### Resume screening and interview preparation

Use resume evidence and mandatory public product research to produce:

- Seven resume signal scores and the fixed-formula `简历信号综合分`.
- Overall and per-dimension `证据覆盖率` using the methodology's evidence-object boundaries.
- Uncertainty flags and material risks, including unresolved entities, missing tenure, unclear personal boundaries, non-recomputable metrics, company capability attributed to the candidate, and critical dimensions not covered.
- A screening conclusion: enter interview, targeted verification, reject, or insufficient information.
- An HR routing summary at the top: recommended product line, role/level, responsibility scope, interview decision, adjacent alternative, and upgrade path. If multiple products are allowed, choose the best-supported route instead of leaving the primary HR question unresolved.
- Targeted follow-up questions and an updated continuous validation ledger that later interviewers can execute.

Do not output evidence-capped confirmation scores at this stage. Public research can strengthen product context and comparison baselines, but it cannot confirm personal contribution. Missing resume evidence is `简历未覆盖`; it creates a question and affects visible signal or coverage according to the methodology, but it is not proof that the candidate lacks the ability.

### Interview-transcript review, scorecard update, and hiring decision

Read the resume-stage report and every available prior-round conclusion and validation item before using the interview transcript. Then produce:

- Seven raw ability scores and `原始能力综合分`.
- An E0–E4 grade and current confirmed score for each dimension, plus `当前确认综合分`.
- Per-dimension and overall `确认覆盖率`.
- Preserved contradictions, changed judgments, decision gates, remaining risks, and remaining validation items.
- An updated continuous validation ledger that cites the prior item, exact question and answer, new evidence, state transition, next owner, and next action.

Distinguish the two interview absences strictly:

- `面试未覆盖`: the topic was not meaningfully asked. Do not use the omission as negative candidate evidence; keep the critical dimension unconfirmed and return it to the ledger.
- `已追问未证明`: a targeted question was asked but the claim remained unsupported. Preserve the question and answer, treat this as bounded negative evidence, and lower the relevant raw and confirmed scores as the methodology requires.

Use `证据矛盾` when resume, interview, public, or artifact evidence conflicts. Show both sides and create a second verification or reference-check item instead of silently choosing the favorable version.

## Final output constraints

- Produce one auditable report using the exact stage-aware structure in the methodology; omit the scoring table that does not apply to the current stage.
- Keep original resume/interview excerpts, public product facts, responsibility inference, scores, and conclusions visibly separate.
- Show all seven dimension scores, every required subdimension, weight, weighted contribution, evidence basis, coverage, and missing-information state. A top-level score without traceable arithmetic is incomplete.
- Keep Friday and MorningStar in separate fit rows. Never average the two product lines merely to create one result.
- Put the HR routing summary immediately after the one-line conclusion. Repeat the recommended product, role/level, and responsibility scope in the final decision so HR does not have to infer them from dimension scores.
- Treat technical-team environment only as product-fact-card and risk context. It is not a scored dimension and does not enter any composite.
- Every factual public claim needs a direct source link; every inference must be labeled; every personal claim must trace to candidate-attributable evidence.
- Preserve the continuous validation ledger across stages. The report is not complete if later interviewers cannot see what remains unknown, why it matters, exactly what to ask, what counts as proof, and who should verify it.
- Recompute the seven-dimension formula, subdimension contributions, coverage, and displayed totals before issuing the conclusion.
