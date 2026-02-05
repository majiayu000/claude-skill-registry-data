---
name: prdts-maker
description: Build software using PRD-driven, gate-verified development. Use this skill when (1) writing PRDs (prd.ts) to define what should be built, (2) creating gates to verify reality, (3) iterating on agent-driven development, or (4) the user mentions gateproof, gates, or PRD-driven workflows. Gates verify reality through observation—not just assertions. PRD defines intent; gates prove it works.
---

# Gateproof

Build software in reverse. PRD defines what should exist. Gates verify reality. Iterate until gates pass.

## Core Philosophy

**PRD is authority on intent.** It declares stories, dependencies, and scope. It does not implement.

**Gates verify reality.** They observe logs, execute actions, and assert evidence. They answer: "Does this work? Can I trust it?"

**Reality is the source of truth.** If the backend doesn't log it, you can't verify it. Observability is part of the system you're building.

**Minimal context, concrete feedback.** Agents iterate efficiently when they get specific failure evidence, not vague errors.

## The Gate Pattern

Every gate follows: **Observe → Act → Assert**

```typescript
import { Gate, Act, Assert, Observe } from "gateproof";

export async function run() {
  return Gate.run({
    name: "user-signup",
    observe: Observe.http({ url: API_URL }),      // where to collect logs
    act: [
      Act.browser({ url: SIGNUP_PAGE }),          // trigger the behavior
      Act.wait(1000),                             // let system settle
    ],
    assert: [
      Assert.hasAction("user_created"),           // verify positive evidence
      Assert.noErrors(),                          // verify no failures
    ],
    stop: { idleMs: 2000, maxMs: 30000 },
  });
}
```

## Writing Gates

**1. Always assert positive evidence.** `Assert.noErrors()` alone is weak—a silent system that does nothing also has no errors.

```typescript
// WEAK: Only checks absence of failure
assert: [Assert.noErrors()]

// STRONG: Checks something actually happened
assert: [
  Assert.hasAction("payment_processed"),
  Assert.hasStage("checkout_complete"),
  Assert.noErrors(),
]
```

**2. Assert what you can observe.** Before writing a gate, ask: "What will the system log when this works?" If nothing—add logging first.

**3. Use custom assertions for nuance:**

```typescript
Assert.custom("order_total_correct", (logs) => {
  const order = logs.find(l => l.action === "order_created");
  return order?.data?.total === 99.99;
})
```

**4. Scope constraints prevent accidents:**

```typescript
scope: {
  allowedPaths: ["src/auth/**"],
  forbiddenPaths: ["src/core/**", "*.config.*"],
  maxChangedFiles: 5,
  maxChangedLines: 200,
}
```

## Writing PRDs

**Keep PRD self-sufficient.** Agents should be able to act with only PRD + gate failure output.

**Low-token rule:** encode the brief in the story title and scope (files + limits), not in extra docs.

```typescript
// prd.ts
import { runPrd } from "gateproof";

const stories = [
  {
    id: "user-signup",
    title: "User can create account with email/password (gate: logs user_created)",
    gateFile: "gates/user-signup.gate.ts",
  },
  {
    id: "email-verification",
    title: "User receives verification email after signup (gate: logs email_sent)",
    gateFile: "gates/email-verify.gate.ts",
    dependsOn: ["user-signup"],  // executes after user-signup passes
  },
  {
    id: "user-login",
    title: "Verified user can log in (gate: logs session_created)",
    gateFile: "gates/user-login.gate.ts",
    dependsOn: ["email-verification"],
    scope: {
      allowedPaths: ["src/auth/**"],
      maxChangedLines: 100,
    },
  },
];

runPrd({ stories });
```

**Title template (single line):**
`<Behavior> — evidence: <action|stage|tag> — scope: <path or limit>`

Example:
`User can log in — evidence: session_created — scope: src/auth/**`

**Story brief checklist (keep in title/scope, no extra docs):**
- What must exist (behavior)
- What evidence will prove it (action/stage/error tag)
- Where the code should live (scope)
- Any hard limits (files/lines)

## The Iteration Loop

Gate fails → get concrete evidence → fix based on evidence → repeat

```
FAILED: user-signup
Evidence:
  actionsSeen: []           ← nothing happened
  errorTags: ["db_error"]   ← database failed
  stagesSeen: ["init"]      ← stuck at init
```

The evidence tells you exactly what's wrong. No guesswork.

## When to Gate

- **Critical paths**: Gate transitions that are expensive to get wrong
- **Agent-driven development**: PRD + gates = minimal context for efficient iteration
- **Reality verification**: When "it compiles" isn't enough—you need proof it works
- **Not everything**: Start with one critical path. Expand as needed.

## Reference Files

- **PRD patterns**: See references/prd-patterns.md for story structures and dependency graphs
- **Gate patterns**: See references/gate-patterns.md for assertion patterns and action examples
