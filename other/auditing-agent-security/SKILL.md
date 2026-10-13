---
name: auditing-agent-security
metadata:
  version: "2.0.0"
description: >
  Applies the Agent Security framework to autonomous AI systems and ghost-team architectures —
  permission and blast-radius mapping, prompt-injection and context-poisoning review, MCP
  bridge security, and quarterly cleanses. Activates on agent security audit, permission stack
  review, agent hygiene, context window poisoning, prompt injection defense, MCP security,
  ghost team security, agent-to-agent trust, blast radius test, permission escalation risk.
  Not for application or codebase vulnerability review and not for building the agent itself
  (use orchestrating-ai-agents or building-langgraph-agents).
---

## When to Use / When NOT

**Use when** — "audit the permissions on my ghost team before I let it run unattended." "could prompt injection through a tool result compromise this agent."

**Do NOT use when** — "build a LangGraph agent that does X" — route to building-langgraph-agents.

# Auditing Agent Security

**TL;DR:** Agent autonomy is the attack surface. This skill maps threats, audits permission stacks, and produces actionable security outputs — whether you're hardening your own ghost team or teaching someone else to do the same.

---

## Decision Tree

```
What mode are you in?
  ├─ AUDIT ──── You have an existing agent stack to review → Golden Path A
  ├─ DESIGN ─── You're building a new agent workflow → Golden Path B
  ├─ TEACH ──── You need to explain agent security to someone else → Golden Path C
  └─ ALL THREE ─ Run A → B → C in sequence
```

---

## Usage Examples

**Example 1 — Audit existing stack**
User: "Audit my ghost team — I have agents on email, calendar, and a Stripe account."
→ Map the Permission Stack (Access/Memory/Action/Sharing). Score each tier. Output: threat report + remediation list ranked by severity.

**Example 2 — Design review before shipping**
User: "I'm about to give an agent access to my n8n workflows and GitHub. What should I check?"
→ Run Golden Path B. Pre-flight security checklist. Flag high-risk permission grants before they're live.

**Example 3 — Teaching mode**
User: "Teach me agent security like I'm a non-technical founder."
→ Golden Path C. Phishing → Agent Injection analogy. Three threat scenarios. One-pager output they can keep.

**Example 4 — Specific threat**
User: "What is a poisoned context window and how do I prevent it?"
→ Pull references/threat-taxonomy.md > Section 2. Explain mechanism, concrete example, mitigation steps.

**Example 5 — Quarterly cleanse**
User: "Run me through the quarterly agent cleanse."
→ references/quarterly-cleanse-protocol.md, interactive checklist, completed audit log output.

---

## Golden Path A: AUDIT

**Step 1 — Inventory**
List every active agent. For each: name/purpose, what it reads, what it writes, what it can spend or delete, what external services it connects to.

**Step 2 — Permission Stack Mapping**
Score each agent across four tiers:
- **Access:** What data can it read?
- **Memory:** What does it retain across sessions?
- **Action:** What can it write, modify, delete, send, or spend?
- **Sharing:** What external services or agents can it communicate with?

→ See `references/permission-stack-audit.md` for tier-by-tier audit questions and scoring.

**Step 3 — Threat Taxonomy Overlay**
Run the 6 threat types against each agent's permission profile:
1. Prompt Injection
2. Poisoned Context Windows
3. Malicious MCP Services
4. Agent-to-Agent Manipulation
5. Permission Escalation
6. Compromised Training Data

→ See `references/threat-taxonomy.md` for detection signals and mitigations per threat.

**Step 4 — Output**
Produce a ranked threat report using `references/output-templates.md > Audit Report`.

---

## Golden Path B: DESIGN

**Pre-flight security checklist before granting any agent access:**

- [ ] What is the minimum permission set this agent needs? (Principle of Least Privilege)
- [ ] Is this a one-time task or ongoing? If one-time: schedule permission revocation before deployment.
- [ ] Does this agent touch financial accounts, production databases, or send external communications?
- [ ] What is the blast radius if this agent is compromised? (If you can't answer this, you're not ready to ship.)
- [ ] Is there a human-in-the-loop checkpoint before every irreversible action? (Delete, spend, send)
- [ ] What external data does this agent read? (Injection vector if outputs aren't validated before action)
- [ ] Are MCP bridges sandboxed and sourced from vetted providers only?
- [ ] Is agent memory scoped to the task lifecycle, not persistent by default?

**The hardest rule:** Agents that read the web cannot also have action permissions on your accounts. Separate the readers from the doers.

---

## Golden Path C: TEACH

**The anchor analogy (always lead with this):**
Phishing in 2010 tricked a human into clicking a link. The human had to be awake, had to open the email, had to fall for it. Agents never sleep. Agent injection tricks an autonomous system into executing commands at machine speed, 24/7, with system-level access. The attack window is always open.

**Core framework to teach (in this order):**
1. The Permission Stack — 4 tiers, low to critical risk
2. The 6 Threat Types — mechanism, example, mitigation
3. The 3 Minimum Viable Defenses — separate, cleanse, checkpoint
4. The Blast Radius Test — one question that forces honest scoping

**Output options:**
- Teaching One-Pager (async / follow-up) → `references/output-templates.md > Teaching One-Pager`
- Story-format scenarios → `references/teaching-scenarios.md`
- Verbal script for live delivery → `references/teaching-scenarios.md > Verbal Walkthrough Script`
- Client Brief for stakeholders → `references/output-templates.md > Client Brief`

---

## Self-Verification Checklist

Before delivering any audit, design review, or teaching output:
- [ ] Permission stack mapped for every agent in scope
- [ ] All 6 threat types checked against the permission profile
- [ ] Blast radius documented for every agent with Action-tier permissions
- [ ] Remediation steps ranked High / Medium / Low
- [ ] One-time agents flagged for revocation
- [ ] MCP bridges reviewed for vetting status
- [ ] Output uses correct template from references/output-templates.md
- [ ] Teaching outputs use analogy-first ordering (phishing → agent injection)

---

## CLAIMS
- [GENERATED] Agent autonomy is the primary new attack surface — not code bugs, but decision-making without human oversight at machine speed
- [GENERATED] The Permission Stack (Access/Memory/Action/Sharing) is the correct mental model for scoping and scoring agent risk
- [GENERATED] Quarterly cleanse cadence is the minimum viable security hygiene for any agent-first business; high-velocity orgs need monthly or event-driven audits

## COUNTEREXAMPLE
- A perfectly audited permission stack doesn't prevent compromised training data — that threat exists before the agent is deployed and cannot be fixed at runtime
- Quarterly cleanses miss rapidly changing agent stacks — the cadence is a floor, not a ceiling

## CONTRADICTIONS
- "Principle of Least Privilege" conflicts with "Ghost Team efficiency" — maximally scoped agents are more capable but dramatically more dangerous
- "Human-in-the-loop checkpoints for irreversible actions" conflicts with "Ambient Business / zero daily human input" — you must decide which irreversible actions are acceptable exceptions and document that decision explicitly


## FAIL Conditions

Named failure modes for this skill. Each is a hard stop, not a warning.

- **Declaring an all-clear without enumerating every permission and credential each agent and MCP bridge can reach** → an escalation path is missed — map the full permission stack and blast radius per agent before any verdict.
- **Running a blast-radius or injection test against production agents or live data** → real damage from the test itself — test against a sandboxed copy with scoped throwaway credentials only.
- **Treating tool output or retrieved context as trusted** → prompt injection and context poisoning slip through — model every external text input as adversarial.
- **Auditing one agent in isolation** → lateral movement goes undetected — audit the agent-to-agent trust graph and assume a compromised agent will pivot.
- **Leaving over-permissioned MCP tokens in place because they work** → standing escalation risk — enforce least privilege and flag any token broader than the task needs.
- **No scheduled re-audit after the cleanse** → drift reintroduces risk — schedule the quarterly cleanse and re-audit after any new tool or connector is added.

## Evals

- ✅ **SHOULD TRIGGER** — "audit the permissions on my ghost team before I let it run unattended."
- ✅ **SHOULD TRIGGER** — "could prompt injection through a tool result compromise this agent."
- ❌ **SHOULD NOT TRIGGER** — "build a LangGraph agent that does X" — route to building-langgraph-agents.
