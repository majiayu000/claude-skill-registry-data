---
name: cx-team-topology
description: Use to decide how to split a growing support organisation — by product, segment, channel, or complexity — and when pods beat shared queues, accounting for coordination cost. Trigger for "team topology", "how should we split the team", "organise support by product or queue", "when to create pods", "support team structure", growing headcount, or coordination overhead between sites.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Support team topology

Growing support teams default to **splitting by whatever annoyed someone last quarter**
— a new product launch, a loud enterprise customer, a channel that backed up. Each split
adds **coordination cost**: handoffs, duplicate policy, uneven load, and managers who
no longer see the whole picture. The topology question is not "how do we organise people"
but **"where should boundaries sit so ownership is clear and handoffs are rare?"**

There is no universal best shape. There is a best shape **for your volume, variance, and
integration maturity** — and it changes as you grow.

## Step 1: map the split dimensions

Common axes:

| Dimension | Good when | Cost |
| --- | --- | --- |
| **Product / line** | Deep specialised knowledge; distinct policies and tools | Cross-product customers ping-pong |
| **Segment** (SMB vs enterprise, market) | SLAs and tone differ materially | Duplicated coverage for multi-segment accounts |
| **Channel** (voice, chat, email) | Channel skills and WFM differ | Same issue handled three ways; fragmented customer view |
| **Complexity / tier** | Clear L1/L2 boundary with documented escalation | L1 becomes dumping ground if L2 inaccessible |
| **Language / region** | Compliance and language proficiency bind | Follow-the-sun handoff gaps |
| **Geography / site** | Labour or hours coverage | Knowledge silos, vendor alignment |

List which dimensions **must** differ for service to work vs which are convenience.
Must-differ dimensions justify boundaries; convenience dimensions suggest routing rules
inside one team instead.

## Step 2: measure coordination tax

Before adding a boundary, estimate:

- **Internal transfer rate** between candidate teams
- **Repeat contact after transfer**
- **Dual-ticket workflows** — customer opens two threads because org chart split them
- **Manager span** — each new team adds a lead, meetings, and reporting lines
- **Policy forks** — teams interpret the same rule differently without shared calibration

If transfers are high on a proposed split line, **the customer journey crosses that line
every day** — splitting there multiplies pain unless you fix routing and knowledge first.

## Step 3: queues vs pods

**Shared queue model** — agents pull from pooled work; skills route by rules.

- Works when: work is fungible, proficiency is broad, load balances quickly, WFM is strong
- Breaks when: context matters (enterprise account history), quality needs deep product
  knowledge, or agents need ownership of outcomes not tickets

**Pod model** — small cross-functional or dedicated groups own a customer set, product,
 or journey end-to-end.

- Works when: relationship continuity matters, work is lumpy, escalation paths are
  short inside the pod, product knowledge is scarce
- Breaks when: pods become underutilised in troughs, vacations create single points of
  failure, or pods hoard work

Hybrid is normal: **pooled L1 + podded complex** or **pod per enterprise segment +
shared overflow queue**.

Decision rule of thumb:

```
Prefer pods when  (context value × transfer pain)  >  (utilisation loss + redundancy cost)
```

Quantify only with your numbers — utilisation targets, transfer rates, account revenue at
risk. Do not cite industry pod sizes.

## Step 4: growth triggers — when to split

Split when **at least two** hold:

- **Span of control** — leads cannot coach, calibrate, and schedule effectively above
  roughly 12–15 direct reports (your culture may differ; state assumption)
- **Skill surface area** — one team cannot stay Independent on all routed strata (see
  skills-matrix skill)
- **Persistent SLA miss on a subset** that shares a clear boundary (product, tier, hours)
- **Calibration drift** — QA meaning diverges between subgroups
- **Hiring profile differs** — voice hires are not chat hires; forcing one pool slows both

**Do not split** solely because headcount crossed a round number, or to give someone a
lead title without scope change.

## Step 5: design the boundary artefacts

Any split needs:

- **Routing rules** — what goes where; overflow back to pool
- **Escalation map** — one page; no "ask in Slack"
- **Shared calibration** — same gold set across teams monthly
- **Knowledge ownership** — who updates KB when policy splits
- **Metrics** — team-level with mix adjustment; not league tables at first
- **Customer identity** — account stays with one pod or one queue policy, documented

Split without these is reorganisation theatre.

## Step 6: plan reversibility

Try **soft splits** before hard ones:

- Skill-based routing with dedicated supervisor
- Named pod on same queue technology
- Time-boxed pilot with transfer and CSAT/QA comparison

Hard splits (separate tools, separate policies) are expensive to undo. Pilot first when
uncertainty is high.

## Traps

- **Product split without integrated CRM** — customers still cross products in one ticket.
- **Channel split without async continuity** — voice agent cannot see chat history.
- **Enterprise pod without backup pool** — PTO collapses SLA.
- **Geographic split as cost play only** — ignores language, access, and calibration.
- **Too many micro-teams** — coordination tax exceeds focus benefit.
- **Topology as substitute for driver fixes** — bad contact drivers need taxonomy and
  deflection, not another team.

## Present results to the user

1. **Current state map** — how work flows today; transfer and repeat-contact hotspots.
2. **Dimension analysis** — must-differ vs convenience splits for your operation.
3. **Coordination tax estimate** — what a proposed boundary adds or removes.
4. **Recommended topology** — queue vs pod vs hybrid, with rationale tied to your signals.
5. **Split triggers** — which conditions justify the next boundary.
6. **Boundary artefacts** — routing, escalation, calibration, KM ownership.
7. **Pilot plan** — soft split, metrics, success/fail criteria, reversibility.
8. **What cannot be concluded** — optimal team size without your WFM and transfer data.
