---
name: autonomous
description: Use when five specialized autonomous agents (code, deploy, planning,
  research, review) working as a coordinated pipeline. From spec to shipped code with
  automated planning, research, review, and deployment gates. Use when working with
  autonomous agents.
domain: agents
author: oyi77
license: Apache-2.0
subdomain: autonomous-agents
tags:
- agent
- ai-agent
- automation
- orchestration
- autonomous
- pipeline
- code
- deploy
- planning
- research
- review
- money
version: 1.0.0
category: agents
---
## Overview

This skill is the hub for five specialized autonomous agents — code, deploy, planning, research, and review — that decompose and execute large tasks without constant supervision. Load it when you need to staff a job across multiple expert roles and coordinate their outputs. It dispatches each agent with the right context, then integrates the results into a finished deliverable.



# Autonomous Agents

## Money-Making Overview

| Agent | Revenue Impact | Avg. Savings | Best For |
|---|---|---|---|
| **Planning Agent** | Eliminates 70% of rework | $500–2,000/feature | Complex multi-file changes, migrations |
| **Research Agent** | Cuts tech evaluation to 15 min | $200–800/decision | Library selection, competitor analysis |
| **Code Agent** | Ships 5–10x faster per story | $1,000–5,000/feature | Full feature implementation, bug fixes |
| **Review Agent** | Catches P1 bugs before production | $2,000–10,000/incident | PR review, security audit, regression check |
| **Deploy Agent** | Zero-downtime, automated rollbacks | $500–3,000/deploy | CI/CD, migrations, hotfixes |

**Combined ROI:** A single pipeline (plan → research → code → review → deploy) saves **$10,000–25,000 per release cycle** by eliminating rework, catching bugs early, and automating deployments.

---

## When to Use

**Plan first** — before any feature touching 3+ files, ambiguous requirements, or multi-agent coordination.

**Research before buying** — evaluating a library, investigating a root cause, competitive analysis.

**Code from spec** — implementing features, fixing bugs with known cause, writing modules/services/libs.

**Review before merge** — every PR, refactoring audit, security check, pre-deploy safety gate.

**Deploy with gates** — shipping to staging/production, CI/CD changes, rollbacks, migrations, hotfixes.

### When NOT to Use

- Single-command tasks — just run the command.
- Real-time human judgment calls.
- Agent lacks tool access or required data.
- Security agent needs to run security checks (see that dedicated skill).

---

## Combined Capabilities

```
                    ┌─────────────┐
                    │  Planning    │  ← Requirements → Step Decomposition
                    │  Agent       │  ← Dependencies → Risk Assessment
                    └──────┬──────┘
                           │ plan
                    ┌──────┴──────┐
                    │  Research    │  ← Evidence Gathering → Source Verification
                    │  Agent       │  ← Tech Evaluation → Root Cause Analysis
                    └──────┬──────┘
                           │ evidence
                    ┌──────┴──────┐
                    │  Code        │  ← Implementation → Tests
                    │  Agent       │  ← Following Conventions → Error Handling
                    └──────┬──────┘
                           │ code
                    ┌──────┴──────┐
                    │  Review      │  ← Adversarial Review → Security Check
                    │  Agent       │  ← Edge Cases → Performance Traps
                    └──────┬──────┘
                           │ approved
                    ┌──────┴──────┐
                    │  Deploy      │  ← CI/CD → Migration → Rollback Plan
                    │  Agent       │  ← Verification → Monitoring
                    └─────────────┘
```

### Pipeline Stages

| Stage | Input | Output | Gate |
|---|---|---|---|
| **Plan** | Feature request | Decomposed steps with deps + risk | Approval |
| **Research** | Question / tech name | Evidence-backed recommendation | Source citations |
| **Code** | Spec / plan | Working code + passing tests | Test suite |
| **Review** | Diff / PR | Findings ranked by severity | All P1/P2 resolved |
| **Deploy** | Artifact / tag | Live service + verification | Health check |

---

## Concrete Action Flow

### Full Pipeline: Feature to Production

```bash
# 1. PLAN: Decompose the feature
agent planning-agent \
    --input "Add OAuth2 login with Google provider" \
    --require "auth.ts, login.tsx, test files, docs" \
    --output plan.json

# 2. RESEARCH: Evaluate library options
agent research-agent \
    --question "Best OAuth2 client library for Next.js 2025" \
    --sources "npm trends, github stars, security audits" \
    --output research.md

# 3. CODE: Implement from plan
agent code-agent \
    --plan plan.json \
    --conventions "src/**/*.ts" \
    --require-tests

# 4. REVIEW: Adversarial code review
agent review-agent \
    --diff "$(git diff main...HEAD)" \
    --focus "security, edge-cases, perf" \
    --output review.json

# 5. DEPLOY: Ship with rollback
agent deploy-agent \
    --target production \
    --strategy blue-green \
    --migration "ALTER TABLE users ADD COLUMN provider"
```

### Standalone: Quick Bug Fix

```bash
# 1. RESEARCH root cause
agent research-agent \
    --question "Why is session token expiring after 5 min?" \
    --context "auth/docs, github issues" \
    --output cause.md

# 2. CODE the fix
agent code-agent \
    --fix "session.ts: token TTL set to 300 instead of 3600" \
    --add-regression-test

# 3. REVIEW before commit
agent review-agent \
    --diff "$(git diff)" \
    --require "test-coverage, no-regression" \
    --auto-approve-if "everything looks fine"
```

---

## First Action in 60 Minutes

1. **Pick one feature** you are about to implement.
2. **Run planning-agent** to break it down into steps with deps and risk.
3. **Run research-agent** on the 1–2 riskiest technical decisions.
4. **Run code-agent** on the first slice (3–5 files).
5. **Run review-agent** on the diff.
6. **Run deploy-agent** to ship it.

**Total time:** ~45 min for a typical feature. Without agents: 4–8 hours.

---

## Real Code Examples

### Python: Orchestrate Multiple Agents

```python
#!/usr/bin/env python3
"""Orchestrate a full autonomous pipeline."""

import json, subprocess, sys
from pathlib import Path

def run_agent(agent: str, **kwargs) -> dict:
    """Run an agent subprocess and return its output."""
    args = ["agent", agent, "--json"]
    for k, v in kwargs.items():
        args.extend([f"--{k.replace('_', '-')}", str(v)])
    result = subprocess.run(args, capture_output=True, text=True)
    return json.loads(result.stdout)

def pipeline(feature: str, target: str):
    # 1. Plan
    plan = run_agent("planning-agent",
        input=feature,
        output="plan.json")
    print(f"Plan: {len(plan.get('steps', []))} steps")

    # 2. Research unknowns
    unknowns = [s for s in plan.get("steps", [])
                if s.get("needs_research")]
    for step in unknowns:
        research = run_agent("research-agent",
            question=step["research_question"],
            output=f"research_{step['name']}.md")
        step["evidence"] = research

    # 3. Implement each step
    for step in plan.get("steps", []):
        if step.get("type") == "implementation":
            run_agent("code-agent",
                plan=json.dumps(step),
                conventions="src/**/*.ts",
                require_tests=True)

    # 4. Review everything
    review = run_agent("review-agent",
        diff=subprocess.run(
            ["git", "diff", "main...HEAD"],
            capture_output=True, text=True).stdout,
        output="review.json")
    if any(f["severity"] == "P1" for f in review.get("findings", [])):
        print("P1 findings — aborting deploy")
        sys.exit(1)

    # 5. Deploy
    run_agent("deploy-agent",
        target=target,
        strategy="rolling",
        health_check="/health")

if __name__ == "__main__":
    pipeline("Add payment webhook handler", "staging")
```

### Bash: Quick Review + Deploy Cycle

```bash
#!/bin/bash
# review-and-deploy.sh — review a branch then deploy

BRANCH="${1:-main}"
DIFF=$(git diff "$BRANCH"...HEAD)

# Review
review_output=$(mktemp)
agent review-agent \
    --diff "$DIFF" \
    --focus "security,perf" \
    --output "$review_output"

if grep -q '"severity": "P1"' "$review_output"; then
    echo "P1 findings — fix before deploy"
    cat "$review_output"
    exit 1
fi

# Deploy
agent deploy-agent \
    --target production \
    --strategy blue-green \
    --health-check "/api/health" \
    --rollback-on-failure

echo "Deploy complete — monitoring..."
agent research-agent \
    --question "Any deployment errors in last 5 min?" \
    --context "logs/app.log" \
    --timeout 60
```

---

## Verification

- Dispatch one task through the full agent set (plan → code → test → review → deploy) and confirm each role produced its documented artifact.
- Introduce a deliberate defect in the code step and confirm the review agent catches it before deploy.
- Verify handoffs carry context: each downstream agent's input includes the upstream agent's output without re-asking.
- Confirm the final deliverable passes the acceptance criteria stated in the plan.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will just do it manually" | Manual does not scale; agents automate 80% of the rote work |
| "The agent will figure it out" | Without clear instructions, agents hallucinate. Give explicit context |
| "One agent is enough" | Specialized agents outperform a generalist on every stage |
| "Planning is a waste of time" | Planning eliminates 70% of rework from ambiguous requirements |
| "I don't need review, I wrote it" | Adversarial review catches what your blind spots miss |
| "Deploying is just git push" | Deploy agent runs migrations, health checks, and rollbacks |
| "I can research as I code" | Dedicated research compresses 2 hours into 15 minutes |

---

## Output Format

Each agent outputs a structured JSON result:

### Planning Agent Output
```json
{
  "steps": [
    {
      "name": "auth-setup",
      "type": "implementation",
      "files": ["src/auth.ts", "src/middleware.ts"],
      "dependencies": [],
      "risk": "low",
      "effort": "30min"
    }
  ],
  "risks": [{ "description": "Breaking change to session format", "mitigation": "Version session tokens" }],
  "estimated_time": "3h",
  "parallelizable_steps": ["ui-login", "callback-handler"]
}
```

### Research Agent Output
```json
{
  "question": "Best OAuth2 library for Next.js",
  "recommendations": [
    { "name": "next-auth", "score": 9, "stars": "28k", "security": "audited" }
  ],
  "sources": ["npmtrends.com/next-auth", "github.com/nextauthjs/next-auth"],
  "decision": "next-auth v5"
}
```

### Code Agent Output
```json
{
  "files_changed": ["src/auth.ts", "src/middleware.ts", "tests/auth.test.ts"],
  "coverage": 87,
  "tests_added": 12,
  "warnings": ["TODO: rate-limit auth endpoint"]
}
```

### Review Agent Output
```json
{
  "findings": [
    { "file": "src/auth.ts", "line": 42, "severity": "P2",
      "finding": "Missing input validation on callback URL",
      "recommendation": "Validate against allowlist" }
  ],
  "summary": "2 minor issues, no blockers",
  "verdict": "approve"
}
```

### Deploy Agent Output
```json
{
  "target": "production",
  "strategy": "blue-green",
  "duration": "142s",
  "health_check": "passed",
  "rollback_plan": "Switch DNS to previous blue environment",
  "migrations_run": ["ALTER TABLE users ADD COLUMN provider"]
}
```

---

## Verification Checklist

- [ ] All agents in the pipeline executed successfully
- [ ] Results validated against acceptance criteria for each stage
- [ ] Error handling tested with edge cases (bad input, network failure)
- [ ] Rollback plan is documented and tested
- [ ] Research sources are cited and cross-referenced
- [ ] Code compiles and all tests pass
- [ ] Review findings resolved (no P1/P2 outstanding)
- [ ] Deploy health check passes and monitoring confirms stability
- [ ] Documentation updated with any API or config changes


## Workflow
See the parent skill for authoritative workflow documentation.
