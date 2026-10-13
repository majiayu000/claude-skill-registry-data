---
name: chaos-engineering
description: Design and run controlled chaos experiments to proactively find system weaknesses using steady-state hypotheses, blast radius control, GameDay planning, and fault injection before failures find you in production
triggers:
  - "chaos engineering"
  - "chaos testing"
  - "fault injection"
  - "gameday"
  - "game day"
  - "resilience testing"
  - "chaos monkey"
  - "failure injection"
  - "steady state hypothesis"
  - "blast radius"
  - "resilience"
  - "simulate failure"
audience: engineer
---

# Chaos Engineering

## Context
Chaos engineering is the discipline of experimenting on a system in order to build confidence in its capability to withstand turbulent conditions in production. The insight from Netflix's Chaos Monkey program — which randomly terminated production EC2 instances — was that the act of routinely injecting failures forces teams to build resilient systems, not just test them.

The governing principle from *Principles of Chaos Engineering* (principlesofchaos.org):

> *"The best defense against major unexpected failures is to fail often. By causing failures, you force your services to be built in a way that is more resilient."*

**This is not random destruction.** Chaos engineering is a structured scientific process:
1. Define a hypothesis about normal (steady-state) behaviour
2. Introduce a controlled variable (the fault)
3. Observe whether steady-state is maintained
4. Learn from the deviation and strengthen the system

Use this skill when:
- Your team is preparing to certify a new service for production
- You want to verify that circuit breakers, retries, and fallbacks actually work
- You're building confidence before a high-traffic event (product launch, Black Friday)
- A post-incident review reveals an untested failure mode
- You are planning a GameDay exercise with cross-functional teams

**Do not run chaos in production until:** you've run the same experiments in staging and the system passed. Production chaos requires mature observability, runbooks, and an abort procedure.

---

## Instructions / Steps

### Step 1: Chaos Readiness Checklist

Before injecting any fault, verify the system is ready to observe and recover:

**Observability (required before any chaos experiment)**
- [ ] Distributed tracing is in place (Jaeger, Datadog APM, AWS X-Ray)
- [ ] Service-level metrics are dashboarded (request rate, error rate, latency p50/p95/p99)
- [ ] Alerting is configured on SLO breach (not just infrastructure health)
- [ ] Logs are centralised and queryable (Splunk, Datadog Logs, CloudWatch)
- [ ] On-call rotation is active and runbooks exist for all critical paths

**Resilience primitives (the things chaos tests)**
- [ ] Circuit breakers configured on all outbound HTTP/gRPC calls
- [ ] Retry logic with exponential backoff and jitter
- [ ] Timeouts set on every network call (no infinite wait)
- [ ] Graceful degradation paths defined (feature flags, fallback responses)
- [ ] Bulkhead isolation between service dependencies

**Process prerequisites**
- [ ] Incident commander and observers identified for the experiment window
- [ ] Abort criteria defined and communicated before starting
- [ ] Rollback mechanism tested (not just documented)
- [ ] Stakeholders notified of the experiment window

### Step 2: Define the Steady-State Hypothesis

A steady-state hypothesis describes the *normal*, *measurable* behaviour of the system. If the system maintains steady state during a fault injection, the hypothesis is confirmed. If it deviates, you've found a weakness.

**Steady-State Hypothesis Template:**

```
## Steady-State Hypothesis

**System:** [Service or cluster under test]
**Experiment ID:** CHAOS-[YYYY-MM-DD]-[NNN]
**Author:** [Name]
**Environment:** [staging / canary / production]

### Steady State Definition
The system is in steady state when ALL of the following are true:

| Metric | Measurement method | Acceptable threshold |
|---|---|---|
| HTTP success rate | Datadog: service.requests / total | > 99.5% over 5-min window |
| p99 latency | APM trace percentile | < 500ms |
| Checkout conversion | Business metric dashboard | within ±2% of 7-day baseline |
| Error budget burn rate | SLO dashboard | < 1x burn rate |

### Hypothesis
"When [fault condition], the system will [expected resilient behaviour],
and all steady-state metrics will remain within acceptable thresholds."

Example:
"When the inventory-service becomes unavailable for 60 seconds,
the checkout flow will degrade gracefully by showing 'stock unknown'
and continue processing, maintaining a checkout success rate above 97%."
```

### Step 3: Blast Radius Control

Chaos experiments must be scoped. The blast radius defines how much of the system is affected.

**Blast radius ladder — start at the bottom, earn your way up:**

| Level | Scope | Example |
|---|---|---|
| 1 — Unit | Single process, no traffic | Fault injection in unit test |
| 2 — Component | Single service in dev/staging | Kill one pod in staging |
| 3 — Integration | Service + dependencies in staging | Inject latency between two staging services |
| 4 — Canary | Small % of production traffic | 5% of requests routed to degraded service |
| 5 — Production (partial) | One AZ or region | Terminate instances in us-east-1a only |
| 6 — Production (full) | Full production environment | Simulate full dependency outage |

**Rules:**
- Never skip levels. Confidence is earned, not assumed.
- Always have an abort mechanism before increasing blast radius.
- Keep experiments short (5-30 minutes) until you understand the system's recovery time.
- Run experiments during business hours with your team present, not on Friday at 4pm.

### Step 4: Fault Injection Checklist by Category

#### Network Faults
- [ ] **Latency injection** — add 200ms, 500ms, 2s to outbound calls from a specific service
- [ ] **Packet loss** — drop 10%, 50% of packets on a network interface
- [ ] **Bandwidth throttle** — limit to 1Mbps to simulate congested link
- [ ] **DNS failure** — resolve dependency hostname to unroutable IP
- [ ] **Partition** — block traffic between two specific services entirely

#### Node / Pod Faults
- [ ] **Pod/container kill** — terminate one instance, verify traffic shifts to healthy nodes
- [ ] **Node drain** — cordon a Kubernetes node and verify workloads reschedule
- [ ] **CPU spike** — run CPU stress on one pod (10%, 50%, 90% utilisation)
- [ ] **Memory pressure** — fill memory to trigger OOM killer, verify restart
- [ ] **Disk full** — fill ephemeral storage, verify service handles write failures

#### Dependency Faults
- [ ] **Timeout** — make upstream service take 30s to respond (beyond client timeout)
- [ ] **Error responses** — return 500/503 for 100% of requests from one dependency
- [ ] **Slow responses** — return correct response after 5s delay
- [ ] **Partial degradation** — return errors for 50% of requests
- [ ] **Payload corruption** — return malformed JSON or unexpected schema

#### Infrastructure Faults
- [ ] **Availability zone failure** — terminate all instances in one AZ
- [ ] **Database failover** — promote replica, verify app reconnects automatically
- [ ] **Cache unavailability** — kill Redis/Memcached, verify cache-miss path handles load
- [ ] **Queue backlog** — pause consumers, let queue grow to 10k messages, then resume
- [ ] **Certificate expiry** — use a soon-to-expire cert and verify renewal process

### Step 5: Tools

| Tool | Platform | Best For |
|---|---|---|
| **Chaos Monkey** | AWS EC2 (Spinnaker) | Random instance termination in production |
| **LitmusChaos** | Kubernetes | Wide library of k8s fault types, GitOps workflow |
| **AWS Fault Injection Simulator (FIS)** | AWS | Managed, IAM-scoped; EC2, ECS, RDS, EKS faults |
| **Gremlin** | Any (SaaS) | Enterprise; team workflows, scheduling, impact scoring |
| **Toxiproxy** | Local / staging | Network proxy for injecting latency and errors in tests |
| **tc / netem** (Linux) | Any Linux host | Low-level traffic shaping for network fault injection |

**Toxiproxy quick start (network fault injection in staging):**
```bash
# Install
brew install toxiproxy
# OR: docker run --rm -p 8474:8474 -p 5432:5432 ghcr.io/shopify/toxiproxy

# Start toxiproxy server
toxiproxy-server &

# Create a proxy: your app connects to localhost:15432, toxiproxy forwards to real DB
toxiproxy-cli create --listen localhost:15432 --upstream real-db.internal:5432 postgres-proxy

# Inject 500ms latency
toxiproxy-cli toxic add postgres-proxy --type latency --attribute latency=500

# Inject 50% packet loss (downstream = responses from upstream)
toxiproxy-cli toxic add postgres-proxy --type bandwidth --downstream --attribute rate=100

# Remove all toxics (restore normal behaviour)
toxiproxy-cli toxic remove postgres-proxy --toxicName latency_downstream

# Delete proxy
toxiproxy-cli delete postgres-proxy
```

**AWS Fault Injection Simulator (FIS) — basic template:**
```json
{
  "description": "Terminate 1 instance in us-east-1a",
  "targets": {
    "instancesInAZ": {
      "resourceType": "aws:ec2:instance",
      "filters": [
        { "path": "Placement.AvailabilityZone", "values": ["us-east-1a"] },
        { "path": "State.Name", "values": ["running"] }
      ],
      "selectionMode": "COUNT(1)"
    }
  },
  "actions": {
    "terminateInstance": {
      "actionId": "aws:ec2:terminate-instances",
      "parameters": {},
      "targets": { "Instances": "instancesInAZ" }
    }
  },
  "stopConditions": [
    { "source": "aws:cloudwatch:alarm", "value": "arn:aws:cloudwatch:..." }
  ]
}
```

**LitmusChaos — Kubernetes pod-kill experiment:**
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: checkout-pod-kill
  namespace: production
spec:
  appinfo:
    appns: production
    applabel: "app=checkout-service"
    appkind: deployment
  engineState: active
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "30"           # seconds
            - name: CHAOS_INTERVAL
              value: "10"           # kill every 10s
            - name: FORCE
              value: "false"        # graceful kill first
            - name: PODS_AFFECTED_PERC
              value: "50"           # kill 50% of pods
```

### Step 6: GameDay Planning Template

A GameDay is a scheduled, facilitated session where a team intentionally breaks things and learns.

```
## GameDay Plan

**Date / Window:** [YYYY-MM-DD HH:MM – HH:MM timezone]
**System:** [Service or platform under test]
**Facilitator:** [Name]
**Incident Commander:** [Name — authorised to call abort]
**Observers:** [List of participants and their roles]
**Stakeholder notification sent:** [ ] Yes

---

### Objectives
1. Verify [resilience behaviour 1] under [fault type 1]
2. Verify [resilience behaviour 2] under [fault type 2]
3. Identify unknown failure modes

### Environment
- [ ] Staging  [ ] Canary (___% of traffic)  [ ] Production
- Environment health check: [link to dashboard]
- Baseline snapshot taken at: ___________

---

### Experiments

| # | Hypothesis | Fault | Duration | Blast Radius | Owner | Pass criteria |
|---|---|---|---|---|---|---|
| 1 | Checkout degrades gracefully when inventory-service is down | Kill all inventory pods | 5 min | All checkout traffic | @engineer-a | Checkout success > 97%; no 500s to users |
| 2 | API gateway rate-limits bots before they saturate upstream | Inject 10x normal RPS from synthetic client | 3 min | Synthetic traffic only | @engineer-b | Upstream CPU < 70%; real user latency unchanged |

---

### Abort Criteria (STOP IMMEDIATELY if any of these occur)
- [ ] Checkout success rate drops below 90%
- [ ] User-visible error rate exceeds 1%
- [ ] Database connection pool exhausted
- [ ] Incident commander calls abort
- [ ] Any unrecoverable state (data loss, security event)

### Rollback Procedure
1. [Step-by-step manual recovery procedure]
2. Toxiproxy: `toxiproxy-cli toxic remove <proxy> --toxicName <name>`
3. FIS: Stop experiment in console or `aws fis stop-experiment --id <id>`
4. LitmusChaos: `kubectl patch chaosengine checkout-pod-kill -p '{"spec":{"engineState":"stop"}}' --type merge`

---

### Post-GameDay
- [ ] Findings documented in incident tracker
- [ ] Follow-up issues created for each failure mode found
- [ ] Retrospective scheduled within 48 hours
- [ ] Runbooks updated
```

### Step 7: Chaos Maturity Model

Assess your team's chaos engineering maturity before planning experiments:

| Level | Description | Signs you're here |
|---|---|---|
| **0 — Unprepared** | No resilience testing | Outages are always surprising; no retries or circuit breakers |
| **1 — Reactive** | Testing after incidents | Circuit breakers added post-outage; manual chaos experiments |
| **2 — Proactive (staging)** | Scheduled chaos in staging | GameDays in non-prod; basic fault library; chaos in pre-deploy gate |
| **3 — Automated (staging)** | Chaos runs continuously in CI/CD | LitmusChaos / FIS in pipeline; results block deploys |
| **4 — Production chaos** | Controlled production experiments | Chaos Monkey running; blast radius tightly controlled; instant abort |
| **5 — Continuous** | Chaos as a platform capability | Chaos is invisible — resilience is just how systems are built |

Most teams should target **Level 2–3** before considering production chaos.

---

## Output Format
When applying this skill, the agent should:
- Complete the Chaos Readiness Checklist and identify any gaps before proceeding
- Write a Steady-State Hypothesis with specific, measurable thresholds
- Assign the experiment to the correct blast radius level
- Provide the specific tool command (Toxiproxy / FIS / LitmusChaos) for the desired fault
- Fill in the GameDay Plan template for multi-experiment sessions
- Define explicit abort criteria before the experiment runs
- Generate a post-experiment findings template with pass/fail for each hypothesis

---

## References
- [Principles of Chaos Engineering — principlesofchaos.org](https://principlesofchaos.org/)
- [Chaos Engineering — Netflix Technology Blog](https://netflixtechblog.com/the-netflix-simian-army-16e57fbab116)
- [LitmusChaos — Documentation](https://litmuschaos.io/docs)
- [AWS Fault Injection Simulator — Documentation](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html)
- [Toxiproxy — GitHub (Shopify)](https://github.com/Shopify/toxiproxy)
- [Resilience Engineering — LeadDev](https://leaddev.com/technical-direction-strategy/building-resilient-systems)
- [Site Reliability Engineering — Google (Chapter 22: Addressing Cascading Failures)](https://sre.google/sre-book/addressing-cascading-failures/)
