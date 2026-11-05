---
name: factory-state-modeling
description: How to reason about state in an interface codebase before writing any component. Interfaces are functions from state to screen, so the discipline is enumerating legal states in types, not minimizing branches. Covers boolean-to-union collapse with exhaustive switches, where the compiler stops seeing (RPCs, env vars, casts), tracing every control to the predicate it changes, deriving values instead of mirroring them, the feature-flag lifecycle (one read, two trees, a removal owner), and reviewing the state model before the diff. Read before scaffolding or reviewing any frontend surface, and whenever a component is about to gain its fourth boolean prop.
---

# Factory state modeling

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint, option, tradeoff), then **Recipe** (the React + TypeScript shape we use), and **Failure mode** where one has been observed. `factory-frontend` owns CRUD recipes; this skill owns the reasoning layer those recipes depend on.

## Interfaces are state to screen, not input to output

**Principle.** An interface program never exits; its whole job is choosing what to show for the current state, so branching over state is the product, not overhead.

**Why.** A pipeline runs once from input to output. Every branch there is a path the data might take and costs twice: once at runtime across every record, once in your head when tracing what happened. Less code is better because the program has one job. An interface is a different kind of program. It is re-run on every state change, and "given this user, role, device, selection and pending request, what is visible" is the entire specification. Engineers arriving from scripts carry the minimize-code instinct into UI and express state as a handful of ad hoc booleans "to keep it simple." The result is fewer lines and more states than anyone can enumerate. The correct instinct in an interface is to enumerate state explicitly, in one place per concern, and let the compiler hold the list.

**Recipe.** Before touching markup, write the states as a type. If you cannot write the type, you do not yet know what you are building.

**Failure mode.** Pipeline instincts applied to a shell component: a boolean per concern added one at a time, each one locally reasonable, until nobody can say which combinations are legal.

## Count the states; make the compiler count them

**Principle.** More than three boolean props on one component is a signal to collapse them into a discriminated union with an exhaustive switch.

**Why.** `n` independent booleans are `2^n` states. Five is thirty-two, and most of them are nonsense: "drawer closed but editing row 7," "confirming with nothing selected." Nonsense states are still reachable, so they still need code paths, and that code is written by whoever hits the bug first. A discriminated union names only the legal states, each carrying only the fields it needs, so the illegal ones cannot be constructed. The exhaustive `never` check turns "I forgot a case" from a runtime surprise into a typecheck failure at the line that forgot it. The union is slightly more code than the booleans. That is the trade: a few more lines in exchange for a state space you can read.

**Recipe.**

```ts
type PanelMode =
  | { kind: 'closed' }
  | { kind: 'command'; query: string }
  | { kind: 'peek'; id: string }
  | { kind: 'create'; draft: Draft }
  | { kind: 'confirm'; action: PendingAction };

function assertNever(x: never): never {
  throw new Error(`Unhandled case: ${JSON.stringify(x)}`);
}

switch (mode.kind) {
  case 'closed':  return null;
  case 'command': return <CommandBody query={mode.query} />;
  case 'peek':    return <PeekBody id={mode.id} />;
  case 'create':  return <CreateBody draft={mode.draft} />;
  case 'confirm': return <ConfirmBody action={mode.action} />;
  default:        return assertNever(mode);
}
```

When proposing the union for an existing component, list the boolean combinations it removes. That list is the review artifact.

**Failure mode.** Kairos `FloatingPanelDialog` on KAI-309 reached ten boolean props, each added for one host (command, peek, create, confirm), before anyone wrote the union. Nobody could say which of the thousand combinations were intended.

## The boundary is where the bugs live

**Principle.** The compiler sees nothing past an RPC response, an environment variable or a cast, so those three places get runtime validation, and every UI control must trace to the server predicate it changes.

**Why.** Look at where the costly incidents in a typed codebase actually come from. They are almost never logic the compiler could have checked. They are a row-level security change that silently nulled an embedded relation, a role guard with a NULL-permissive `NOT IN`, a backfill keyed on the wrong timestamp, a date picker wired to a query that ignores dates. In every case the TypeScript layer trusted a shape or an effect that the other side never guaranteed. Casts are the explicit version of the same mistake: `as any` is the developer telling the compiler to stop looking, and it does. The rule is not "never cast." It is "cast only where a runtime check stands beside it, so the trust is earned."

**Recipe.**

- A cast (`as any`, `as unknown as T`) is allowed only at an import boundary with a Zod parse next to it, or with a comment naming the ticket that removes it. Inside component logic it is a defect.
- An environment variable is read once, coerced, and passed as a typed value. `process.env.X` is a string or `undefined`; compare to `'true'`, never rely on truthiness.
- Before adding or accepting any filter, toggle, sort or picker, name the RPC argument or SQL predicate it changes. If the answer is "none yet," say so in the review rather than shipping the control.
- After narrowing a security policy, grep for every embedded relation the policy touches and verify the embed still resolves for every role.

**Failure mode.** Kairos: an RLS lockdown nulled a `distributors` embed and the rep's name was stamped as the distributor on new orders. A `NOT IN` guard over a nullable role let a profile-less auth user mark invoices paid. A commissions timeframe control was provably inert because the RPC behind it was date-blind by construction.

## Derive, don't store

**Principle.** A value computable from props or other state is computed on render, never kept in a second piece of state that must be synced.

**Why.** Two copies of one fact will disagree. The second `useState` holding a derived total is correct on the render that set it and stale on the next one that changed an input, and the bug surfaces as "sometimes the total is wrong," which nobody can reproduce. `useMemo` recomputes from inputs; there is nothing to sync. This is the UI-local case of a broader rule: `factory-frontend §One direction of truth` covers server state versus client state. This section covers state versus state within one component tree.

**Recipe.** If the value can be written as `f(props, state)`, write it as `useMemo(() => f(...), [deps])` or as a plain expression. Reserve `useState` for facts the user created that cannot be recomputed: text they typed, a row they selected, a drawer they opened. A codebase with twice as many `useState` calls as `useMemo` calls usually has mirrored state hiding in the difference.

**Failure mode.** Kairos KAI-148: an uncontrolled form held line totals in state and recomputed them only on some edits, so the submitted total did not match the lines.

## Feature flags: one read, two trees, a death date

**Principle.** A feature flag is read once at the server boundary, decides which component tree to mount, and carries a ticket that deletes it.

**Why.** A flag separates deploying code from releasing a feature. Code merges to main small and early, ships to production dark, goes live when you choose and retreats in seconds without a revert. That is worth one `if`. The danger is that a flag is a boolean whose value comes from outside the type system, exactly the kind of switch the previous sections warn about. Threaded through twenty components, it multiplies against every state those components already have. Read once at the top, it produces two trees that are each internally unaware of the flag, and the state space below the boundary does not grow. Flags are also temporary by definition. Every other state in the app is permanent product state. A flag nobody owns stays forever, and a year later there are two UIs and nobody remembers which one is real.

**Recipe.**

```tsx
// app/admin/layout.tsx (server component)
const panelOn = process.env.KAIROS_MOBILE_COMMAND_PANEL === 'true';
return <AdminShell mobileCommandPanel={panelOn} ... />;
// Below the shell, nothing reads the env var.
```

- Keep the legacy path untouched. The flag's value is the ability to go back, and a "cleaned up" legacy path restores nothing.
- Run the browser suite with the flag off and on. An untested rollback path rots within weeks.
- Write a runbook: the variable's name, what on and off look like, how to roll back.
- Open the ticket that owns default-on and flag deletion before the flag ships.
- Do not nest flags. Two flags inside each other are four combinations to test, and one of them is overdue for removal.

**Failure mode.** Flag threaded below the shell: each component gains one more bit of state it did not need. Flag with no removal owner: permanent dual maintenance. The env-var flag is global; when someone needs "on for one user," move it to a small admin-writable settings table read at the same boundary rather than adding a second mechanism alongside.

## Review the state model before the diff

**Principle.** For any new or substantially changed component, the props type and the state union are approved first; the implementation follows, and the review leads with which states were added or removed.

**Why.** Agentic development means the operator reviews outcomes, and outcomes hide the state model. A screenshot that looks right says nothing about how many states the component can be in. Approving the type first moves the review from "does it look right" to "which states exist," which is the question the incidents above all failed. It also costs almost nothing: a type and one sentence per state on when it occurs. For a fixed defect, the first failing test is the operator's to write; the agent offers the shape and the assertion. A test you wrote and watched fail for the right reason is a test you understand. See `factory-mentor` for the pedagogy behind this.

**Recipe.** The agent's review message opens with:

```
## State model
- Added: { kind: 'confirm'; action } (nested confirmation suspends the panel)
- Removed: isConfirming, pendingAction (collapsed into the union)
- Unchanged: 'closed' | 'command' | 'peek' | 'create'

## Diff
...
```

**Failure mode.** Review by screenshot. The surface looks right at 390px and desktop; the component has four booleans more than it did last week.

## Where this applies

- Every frontend build, before the first component is written
- Every review of a frontend diff, as the first section of the review
- Any component about to gain its fourth boolean prop
- Any control, filter or picker added to a surface backed by an RPC
- Any feature flag, from the day it is proposed to the day it is deleted

## Related

- `factory-frontend.md` owns the CRUD recipes (DataTable + drawer mode union) this reasoning produces
- `factory-frontend-engineer.md` runs "What are the states?" as a workflow step before scaffolding
- `factory-design.md` owns visual coherence; this skill does not touch tokens or layout
- `factory-mentor` (pending on its own branch) owns the operator-learning contract that "types before code" serves
- `factory-pitfalls.md` indexes the failure modes above under Frontend
