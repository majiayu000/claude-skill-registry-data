---
name: prototype
description: Build throwaway code to validate an uncertain approach before committing to a plan. Two branches — Logic (terminal state machine) or UI (multiple designs on one route with URL-param switcher). No persistence, no tests, single-command start. Use between analyze and plan when the approach itself is uncertain.
---

# /supergraph:prototype

Throwaway code to validate approach. Explore fast, decide, then delete or integrate.

Announce: "🧪 /supergraph:prototype — building throwaway prototype..."

## When to Use

- Between `/supergraph:analyze` and `/supergraph:plan` when approach is uncertain
- Multiple valid UI designs need visual comparison
- Core logic (state machine, algorithm, data model) needs validation before full TDD
- User says "I'm not sure which approach" or "can we try both?"

## Choose Branch

Ask user (or infer from task):

**Logic branch** — validate state, algorithm, or data model  
**UI branch** — validate layout, interaction, or multiple designs

---

## Logic Branch

Goal: validate core logic in a minimal terminal program.

Rules:
- Single file (`prototype-<slug>.ts` / `.py` / etc.)
- No database, no HTTP, no external services — in-memory only
- No tests — feedback is the running output
- Single command to run: `npx ts-node prototype-<slug>.ts` or equivalent
- Hard-code sample data

Structure (TypeScript example):
```typescript
// prototype-<slug>.ts — THROWAWAY, do not review
type State = "idle" | "processing" | "done" | "error"
type Event = { type: "start" } | { type: "finish" } | { type: "fail" }

function transition(state: State, event: Event): State {
  // ...
}

// Run through sample cases
const cases = [ ... ]
cases.forEach(({ from, event, expected }) => {
  const result = transition(from, event)
  console.log(result === expected ? "✅" : "❌", { from, event, result, expected })
})
```

Run and observe:
```bash
npx ts-node prototype-<slug>.ts
```

---

## UI Branch

Goal: compare multiple visual/interaction designs without committing.

Rules:
- All designs live on ONE route: `/prototype/<slug>`
- URL param `?design=A|B|C` switches between designs
- Floating control bar (fixed position) lets user switch designs visually
- No persistence layer — mock data only
- No auth, no real API calls
- Single command to start: `npm run dev` (or project equivalent)

Structure:
```
app/prototype/<slug>/page.tsx   (router + floating switcher)
app/prototype/<slug>/DesignA.tsx
app/prototype/<slug>/DesignB.tsx
app/prototype/<slug>/DesignC.tsx
```

Floating switcher (inline):
```tsx
<div style={{position:'fixed',bottom:16,right:16,zIndex:9999,background:'#fff',padding:8,borderRadius:8,boxShadow:'0 2px 8px rgba(0,0,0,.2)'}}>
  {["A","B","C"].map(d => (
    <button key={d} onClick={() => router.push(`?design=${d}`)}
      style={{margin:4, fontWeight: design===d ? 'bold' : 'normal'}}>
      {d}
    </button>
  ))}
</div>
```

---

## After Prototyping

Present findings to user:

```
Prototype: [slug]
Branch: Logic | UI

Findings:
- [What was validated]
- [What was ruled out]
- [Surprises / unexpected behavior]

Recommendation:
- Approach: [chosen approach]
- Confidence: high | medium | low
- Reason: [evidence from prototype]
```

Ask: "Ready to proceed to `/supergraph:plan` with this approach?"

## Cleanup

After approach is decided:
```bash
# Delete prototype file(s)
rm prototype-<slug>.ts
# or git stash if user wants to keep for reference
```

**Never commit prototype code to main branch.**

## Rules

- No persistence — in-memory or mock data only
- No test suite — prototype is the test
- Single command to run/start — no setup steps
- Delete or integrate after decision — never leave prototype code in codebase
- Max scope: 1 file (Logic branch) or 4 files (UI branch) — if approach is still unclear after that, escalate to user
