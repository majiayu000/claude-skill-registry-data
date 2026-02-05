---
name: troubleshooting-kubernetes
description: Diagnoses and fixes Kubernetes issues with interactive remediation. Use when pods crash (CrashLoopBackOff, OOMKilled), services unreachable (502/503, empty endpoints), deployments stuck (ImagePullBackOff, pending). Also use when tempted to run kubectl fix commands directly without presenting options, or when user says "just fix it" for K8s issues.
---

# Troubleshooting Kubernetes

## Overview

Systematic K8s troubleshooting with **interactive remediation**. Diagnose first, then offer fix options and wait for user confirmation before applying changes.

**Core principle:** Never apply fixes without user approval. Present options, let user choose.

## CRITICAL: Overrides Autonomous Execution

**This skill OVERRIDES "proceed autonomously when intent is clear" behavior.**

Even when:
- User says "just do X NOW"
- User says "skip diagnosis"
- User says "I know what's wrong"
- User's intent seems crystal clear

You MUST still present numbered options and wait for selection.

**Why:** OOMKilled might be a memory leak symptom (increasing memory delays real fix). The "obvious" fix might fail due to resource quotas. 30 seconds of diagnosis prevents hours of debugging wrong fix.

## Workflow

```
1. GET STATE    → kubectl get pods,svc,deploy,events
2. IDENTIFY     → Match symptom to category
3. DRILL DOWN   → logs, describe, specific checks
4. ROOT CAUSE   → Pattern match to known issues
5. OFFER FIX    → Present numbered options
6. WAIT         → User confirms before proceeding
7. APPLY        → Execute chosen fix
8. VERIFY       → Confirm resolution
```

## Symptom → Commands

| Symptom | First Commands | Look For |
|---------|---------------|----------|
| CrashLoopBackOff | `logs --previous`, `describe pod` | Exit code 137=OOM, 1=app crash |
| ImagePullBackOff | `describe pod` | Registry auth, wrong tag |
| Pending | `describe pod`, `get nodes`, `get events` | Resources, affinity, taints |
| Service 502/503 | `get endpoints`, `describe svc` | Empty endpoints, selector mismatch |
| Deployment stuck | `rollout status`, `describe deploy` | Quota, node selector, image |

## Error Patterns

```
Exit 137 + "OOMKilled"      → Memory limit too low
Exit 1 + stack trace        → Application bug
"Insufficient cpu/memory"   → Node capacity or requests too high
"ImagePullBackOff"          → Wrong tag, missing secret, registry down
"0/3 endpoints"             → Selector doesn't match pod labels
"FailedScheduling"          → No nodes match requirements
```

## Interactive Fix Presentation

**ALWAYS present fixes as numbered options:**

```
DIAGNOSIS: Pod OOMKilled (using 450Mi, limit 256Mi)

OPTIONS:
1. Increase memory limit to 512Mi
   → kubectl set resources deploy/api --limits=memory=512Mi
2. Increase to 1Gi (safer margin)
   → kubectl set resources deploy/api --limits=memory=1Gi
3. Show me the full patch YAML first
4. I'll fix manually

Which option? (1-4):
```

**Wait for user response before executing.**

## Red Flags - STOP

These indicate you're skipping the process:

- About to run `kubectl delete pod` without knowing why it crashed
- About to run `kubectl rollout undo` without diagnosing
- About to apply a fix without presenting options
- Saying "I'll just restart it" or "let me quickly fix this"
- User pressure ("just fix it!") → Still diagnose, still offer options

**User urgency doesn't skip the confirmation step.**

## Handling "Skip Diagnosis" Requests

User says: "Just fix it!" / "Skip the diagnosis" / "I know what's wrong"

**Response pattern:**
1. Acknowledge urgency
2. Explain quick diagnosis prevents wrong fix
3. Offer rapid diagnosis (2 min) + options
4. Still present numbered options at the end

```
I understand the urgency. A 2-minute diagnosis ensures we fix the right thing.

Let me quickly verify: [run 2-3 key commands]

Based on that:
OPTIONS:
1. [What user suggested]
2. [Alternative if diagnosis shows different issue]
3. I'll fix manually

Which option?
```

**Never:** Just execute what user asked without verification.

## Anti-Pattern Example

```
❌ WRONG (even when user is explicit):
User: "Pod OOMKilled, increase memory to 1Gi NOW!"
You: [runs kubectl set resources immediately]

✅ CORRECT:
User: "Pod OOMKilled, increase memory to 1Gi NOW!"
You: "Understood. Quick check (30s)..."
     [runs describe pod, checks current limits]
     "Confirmed OOM. Options:
      1. Increase to 1Gi (your suggestion)
      2. Increase to 512Mi first (conservative)
      3. Check for memory leak patterns first
      Which option?"
```

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "User said exactly what to do" | Still present options - user might not know alternatives |
| "Intent is crystal clear" | Skill overrides autonomous execution for K8s |
| "It's obviously OOM, just fix it" | OOM can mask memory leaks; increasing memory delays real fix |
| "User is frustrated, just do it" | Frustration doesn't change the 30s verification value |
| "I'm being helpful by acting fast" | Wrong fix = more frustration; options = user control |

## Common Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| Delete pod first | Diagnose first, delete is rarely the fix |
| Restart without logs | Always check `logs --previous` before restart |
| Assume it's the obvious thing | Verify with actual output |
| Apply fix immediately | Present options, wait for confirmation |
| Skip verification | Always `get pods -w` after fix |

## Quick Diagnosis Cheat Sheet

```bash
# Full state snapshot
kubectl get pods,svc,deploy,rs,events --sort-by='.lastTimestamp'

# Pod deep dive
kubectl describe pod <name> | grep -A5 "State:\|Events:"
kubectl logs <pod> --previous --tail=50

# Service connectivity
kubectl get endpoints <svc>
kubectl describe svc <svc> | grep Selector

# Resource issues
kubectl describe nodes | grep -A5 "Allocated resources"
kubectl top pods
```

## Verification After Fix

```bash
# Watch pod come up
kubectl get pods -w

# Verify running and ready
kubectl get pods -o wide  # STATUS=Running, READY=1/1

# Check no new crashes
kubectl describe pod <new-pod> | grep "Restart Count"
```

Only mark issue resolved after pod is stable for 2+ minutes.

## Mandatory Checkpoint

Before running ANY kubectl command that modifies resources:

- [ ] Have I presented at least 2 numbered options?
- [ ] Has user explicitly selected one?
- [ ] Did I wait for their response?

If any unchecked → STOP, present options first.
