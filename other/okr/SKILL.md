---
name: OKRs
slug: okr
version: 1.0.0
description: Writing objectives and key results, setting cadence, and avoiding common stretch-goal failures.
homepage: https://clawic.com/skills/okr
metadata:
  clawdbot:
    emoji: 💰
    requires:
      bins: []
    os:
    - linux
    - darwin
    - win32
    displayName: OKRs
---

## Writing the objective (O)

- The O is qualitative and directional: the change in the world if you succeed. "Win the SMB segment" not "grow SMB revenue 20%" (that is a KR). Direction on top, numbers underneath.
- Test the O: if every KR hit and nothing important changed, the O was a restatement. Rewrite around the user or market shift you intend to cause.
- One O per battlefield, not per project. "Make checkout best-in-class" is an O; "ship Apple Pay", "ship one-click", "ship saved cards" are inputs, not three Os.
- Memorable by week 8: if a teammate cannot say the O in one breath without the doc, it is a paragraph, not a direction.
- Inspirational without vagueness: "fastest mobile experience" is directional; "improve things" is vague; "checkout latency under 800ms" is a KR.
- No O overlap: two Os sharing KRs or drivers is one O pretending to be two. Merge.
- Cap at 3-5 Os per level. >5 = wishlist; cutting to 3 is where the real trade-off gets made. The pain of cutting is the signal the list was honest.
- An O should survive the quarter. Wanting to change it mid-quarter means either it was a task (killable) or the strategy genuinely shifted (rare; renegotiate openly, do not silently swap).

## Writing key results (KR)

- KR = measurable outcome, not output. "Ship feature X" is a task; "lift activation 40% -> 55%" is a KR. Razor: if you shipped the task and the number did not move, was it still a success? If yes, it is a task disguised as a KR.
- 3-5 KRs per O. More = no focus; the team optimizes the easy ones and the hard bet goes unfunded.
- Each KR carries a start value, a target, and a unit. "Improve NPS" is not a KR; "NPS 32 -> 45" is.
- Leading vs lagging: a KR measurable only at quarter-end (revenue, churn) is lagging. Mix in a leading KR (pipeline coverage, activation rate) you can read weekly. A set of only lagging KRs is unmanageable mid-quarter.
- Binary/milestone KRs are allowed but score 0 or 1; keep them under ~30% of the set or you have rebuilt a task list with numbers on it.
- Input vs output confusion: "publish 4 blog posts" is input; "organic signups 200 -> 500/wk" is output. Inputs live in the execution plan, not the KR set.
- Avoid the circular KR: O "grow revenue" with KR "increase revenue 20%" restates the O. The KR must be a driver you believe moves the O (pipeline, win rate, expansion), not the O itself measured.
- One named owner per KR, not per O. Unowned KR = no one acts. The O owner coordinates; they do not own every KR.
- Measurability test: if the data pipeline cannot produce the number on a weekly cadence, pick a proxy you can measure or drop the KR. A number you read only at quarter-end is a postmortem, not a steering wheel.
- Guardrail KRs: 1-2 per set, metrics you must not break while pursuing the O (NPS > 40, error rate < 0.5%, margin held). Without guardrails, teams hit the O by breaking something expensive off-book.
- Stretch check: a KR you are 100% sure you will hit is a commitment, not a KR. A real KR carries genuine uncertainty about reaching 1.0.
- Confidence per KR: owner sets a 0-1 confidence at the weekly check-in and updates it. Trend beats level; falling confidence two weeks running = intervene now, do not wait for the score.

## Cadence and the scoring cycle

- Quarterly is the dominant rhythm. Annual = strategic direction at the O grain, not measurable KRs; monthly churns and never lets a KR compound.
- Write the set in week -1 to -2, before the quarter starts. Sets written in week 2 are retrofitting work already underway, not planning.
- Weekly check-in (not weekly rewrite): ~15 min, review score + confidence per KR, surface blockers. The check-in is the mechanism; the quarterly doc is just the substrate.
- Mid-quarter reset at ~week 4-5 of 12-13: if a KR is under 0.3 and the driver is not working, reset the target or kill the KR. Carrying a dead KR to quarter-end erodes the system's credibility.
- Score on a 0-1 scale, not 0-100 or letter grades. 0.7 = green (Grove/Doerr convention); under 0.4 = systemic problem, investigate the driver not the metric.
- 1.0 across every KR for two consecutive quarters = sandbagging. Force a recalibration session; the team is under-committing or comp-coupling.
- Do not rewrite KRs mid-quarter to match reality. Updating the score is honest; moving the goalpost to look good destroys the signal for everyone.
- End-of-quarter readout: ~30 min, score plus a one-paragraph "what we learned" per O. The learning is the asset; the score is the receipt.
- Annual OKRs alone fail because a year is too long for a KR to steer. Keep annual Os for direction, quarterly KRs for measurement.

## Commit vs stretch (the two-tier system)

- Two tiers: commit (expected at 1.0, eligible for performance review) and stretch/aspirational (expected at ~0.7, not tied to comp). The label is what tells the team how to read a 0.7.
- Mixing the tiers breaks both: teams sandbag commit to hit 1.0 safely, and game stretch to look good on the impossible. Pick a tier per OKR, label it, hold the threshold.
- Single-tier (all stretch) works for small teams with an honest culture; fails fast in orgs where missing 1.0 gets punished, because the org quietly converts stretch into commit-by-anxiety.
- The 0.7 threshold is the score at which a stretch KR counts as success, not a target to aim for. Aiming for 0.7 is aiming to fail on purpose; aim for 1.0, expect 0.7.
- Commit + comp: if bonus equals OKR score, stretch dies and the score becomes a negotiation. Decouple stretch from comp; review commit for performance, never the reverse.
- Aspirational moonshots can sit at 0.3-0.5 for multiple quarters and stay healthy. A moonshot that hits 1.0 in one cycle was not a moonshot.
- Punish 0.7 once and the system collapses within two cycles: teams learn to under-commit, scores drift to 0.9+, and the stretch signal is gone permanently.

## Alignment and decomposition

- Alignment not cascade: teams self-set OKRs against org themes, not slavishly derived from the layer above. Top-down cascade is slow and produces OKRs nobody owns.
- Cascade (CEO -> team -> individual) wins at under 2 layers or in regulated, standardized ops where consistency is the constraint. Alignment wins past ~2 layers or in autonomous teams.
- Individual OKRs are contentious: many elite orgs dropped them because they become mini performance reviews. Prefer team OKRs; if individuals have them, make them about personal craft, not the team's deliverables.
- Horizontal alignment beats vertical: the failure mode at scale is two teams with contradicting OKRs (one optimizes speed, the other gatekeeps quality). Resolve in a pre-quarter alignment session, not mid-quarter.
- Shared KRs (one KR owned by two teams) force alignment by construction; use them for cross-team bets where the outcome depends on both halves.
- Do not force every team OKR to map to an org OKR. ~70% aligned, ~30% team-local (health, infra, debt) is healthier than 100% contortion.
- The alignment session is the real planning artifact: it surfaces contradictions before they cost a quarter. Skip it and you spend the quarter negotiating instead of executing.

## Common failures (blacklist)

- KR is a task list in disguise: "launch v2", "hire 3 engineers", "migrate DB". Rewrite each as the outcome the task should move; the tasks go in the execution plan.
- OKR-as-todo: if removing the KR would not change behavior, it is documentation, not a goal. A good KR makes a trade-off visible.
- Watermelon KRs: green on the metric, red underneath. "Response time < 2h" met by deferring hard tickets. Guardrails and qualitative review catch what the number hides.
- Too many OKRs: >5 Os or >5 KRs per O = no focus. The team picks the easy ones; the hard bet stays unfunded.
- OKR tied to comp: stretch becomes a negotiation, scores drift up, the signal dies. The single most common way organizations kill OKRs.
- Sandbagging: 1.0 across the board for 2+ quarters. Symptom of comp-coupling or a culture that punishes missing 1.0.
- Goalpost-moving: editing the KR target mid-quarter to match the result. The score is meant to be honest, not flattering.
- Set-and-forget: OKRs written in week 1, unread until week 12. Without the weekly check-in, the doc is theatre.
- Vanity KR: a number that rises regardless of effort (total signups in a growing market). Use a KR that would not move without the work.
- Output KR as outcome: "ship 4 features" measures activity, not value. The outcome is what changes for the user.

## OKR vs adjacent systems

- OKR vs KPI: KPIs are the org's vital signs, always-on health metrics; OKRs are the quarterly bets, time-bound and stretch. KPIs for the dashboard, OKRs for the focus. A KR often reads like a KPI with a delta and a deadline.
- OKR vs MBO: MBO is annual, top-down, tied to comp, no stretch. OKR is quarterly, self-set-ish, decoupled from comp, stretch. The comp coupling is the decisive difference, not the format.
- OKR vs SMART: SMART is a goal-writing hygiene check (Specific, Measurable, etc.), not a system. OKRs subsume the measurable part; SMART alone gives no cadence, no stretch, no alignment.
- OKR vs V2MOM: V2MOM adds Vision and Method to the objective; it is a strategic alignment narrative, not a scored system. Use V2MOM for the story, OKRs for the measurable focus.
- OKR vs EOS rocks: rocks are quarterly goals, often un-scored and commit-only. OKRs add numeric KRs and the stretch tier.
- One system per quarter: an org running OKRs plus a separate "priorities" list has two priority systems and will honor neither.

## Interface with adjacent roles

- CEO/founder: owns the annual Os and org themes; should not write team KRs. A CEO writing team KRs has cascaded, and cascade kills ownership.
- Product/engineering leads: negotiate KRs with the teams that do the work. The lead's job is to ensure KRs are outcomes and measurable, not to author them solo.
- Finance: owns the revenue and cost numbers OKRs reference. A KR citing a number finance does not recognize becomes an argument at quarter-end; align KR metrics with the finance source of truth before the quarter.
- Data/analytics: owns the measurement pipeline. A KR whose number the data team cannot produce weekly is a KR you will not steer; involve them at KR-writing time, not score-reading time.
- People/comp: the firewall. Keep comp review separate from stretch OKR scores; the comp committee reads commit OKRs and qualitative signals, not aspirational numbers.
- Cross-team KR owners: when two teams share a KR, name one accountable owner (the team whose work moves it most) and a contributor. Two equal owners = no owner.

## Situations

| Situation | Play |
|---|---|
| Every KR lands at 1.0, two quarters running | Sandbagging. Force a recalibration session, raise the bar next cycle, check comp-coupling. |
| A KR sits at 0.2 in week 5 | Reset the target or kill the KR. Carrying a dead KR erodes credibility. |
| Leadership wants OKRs tied to bonus | Decouple stretch from comp. Use commit OKRs for review, keep aspirational out of the bonus math. |
| Team shows up with 8 objectives | Cut to 3-5. >5 = wishlist; the cut is where the real trade-off gets made. |
| A KR reads "ship feature X" | Rewrite as the outcome the feature should move (activation, retention, latency). Task goes in the plan. |
| Two teams' OKRs contradict | Resolve in the pre-quarter alignment session, not mid-quarter. Or split into a shared KR. |
| CEO wants annual OKRs only | Annual Os for direction, quarterly KRs for measurement. A year is too long for a KR to steer. |
| The metric cannot be measured weekly | Pick a measurable proxy or drop the KR. A quarter-end-only number is a postmortem. |
| New product, no baseline | Quarter 1: baseline KR (just measure). Quarter 2: commit OKR against the baseline. |
| Stretch KR missed at 0.65 | Celebrate. 0.7 is the success threshold; 0.65 on a real stretch is a healthy cycle. |
| A KR is the O restated | Rewrite the KR as a driver (pipeline, win rate, expansion), not the O itself measured. |

## Where camps disagree

- **Decouple from comp (Doerr/Google) vs tie to comp (enterprises):** decouple wins for stretch culture and honest scores; tie wins where accountability is the binding constraint and the org will not stretch anyway. Frontier: the org's existing incentive honesty. If comp is already gamed, coupling OKRs to it imports the gaming.
- **Two-tier commit + stretch (Google) vs single set:** two-tier wins at scale with mature ops and a comp firewall; single set wins for small teams who cannot maintain two rhythms and do not need the comp distinction.
- **Individual OKRs:** drop them (Google moved away) vs keep them (some enterprises). Frontier: team size and review density. In a high-review-density org they become performance theatre; in a flat autonomous team they can encode craft growth.
- **Quarterly vs monthly:** quarterly is the empirically dominant rhythm; monthly churns and never lets a KR compound. Monthly wins only pre-PMF, where the strategy itself shifts that fast.
- **Cascade vs alignment:** cascade wins at under 2 layers or in regulated ops; alignment wins past ~2 layers and in creative teams. The cost of cascade is ownership; the cost of alignment is contradiction, which the alignment session exists to catch.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/<slug> (install if the user confirms):
- `metrics` - choosing KPIs, leading vs lagging indicators, the measurement layer KRs depend on
- `strategy` - the annual direction and org themes OKRs decompose from
- `product` - product roadmaps and bets that OKRs operationalize into measurable focus
- `management` - the cadence, one-on-ones, and people system OKRs sit inside
- `analytics` - the data pipeline that must produce each KR's number on a weekly cadence
