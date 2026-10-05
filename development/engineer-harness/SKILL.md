---
name: engineer-harness
description: >
  Shared delivery harness for the main commands (/toh, /toh-plan, /toh-fix,
  /toh-vibe) — senior-engineer tool selection rules (search real docs, reproduce
  before diagnosing, verify by running), THE EVIDENCE RULE (only a quoted passing
  run counts as done), non-developer communication mode, and stage-aware next
  actions with the announce contract. Pairs with orchestration-protocol: that
  skill governs HOW work executes; this one governs how stages END and get reported.
user-invocable: false  # internal — model-invoked via toh-* commands, not a user /command
---
# 🛠️ Engineer Harness Skill

> **Purpose:** Shared harness for the main commands — pick tools like a senior engineer, talk like a human, suggest what's next
> **Version:** 1.1.0
> **For:** Toh Framework v2.0.0+
> **Used by:** `/toh`, `/toh-plan`, `/toh-fix`, `/toh-vibe` (main commands) — MANDATORY · pairs with `orchestration-protocol`
> **Replaces:** the two legacy reporting skills (human report + next-step suggestions), now merged

---

## 🎯 Purpose

Three things every engineer-grade delivery needs, in one skill:

1. **Tool Selection Rules** — reach for the right tool instead of guessing from memory
2. **Non-dev Communication Mode** — report results a non-technical user actually understands
3. **Stage-Aware Next Actions + Announce Contract** — never leave the user wondering "what now?"

**Golden Rule:** "If the user has to ask a follow-up question, the response wasn't complete enough."

---

## 🧰 A. Tool Selection Rules

Act like a senior engineer choosing tools — never fake it from memory.

| Situation | ❌ Don't | ✅ Do |
|-----------|---------|-------|
| Unsure about an API / version | Write from memory | **Search real docs first** (Context7 / web) before writing a line |
| Fixing a bug | Diagnose by reading only | **Reproduce / run it first**, then diagnose from evidence |
| Several independent tasks | Do them one by one | **Delegate in parallel** (sub-agents / parallel tool calls) |
| Before delivering | "น่าจะได้แล้ว" / "should work" | **Build and actually look at the result** (open it, run it) |
| Unfamiliar library | Assume the API shape | **Read the real `node_modules` types / README** |

**Rule of thumb:** evidence over assumption, always. If a fact is checkable, check it before you write.

**THE EVIDENCE RULE (verification):** Run the check. Quote the failing lines. Fix what the quote shows. Re-run. **Only a quoted passing run counts as done.** A sub-agent's "done" report is evidence to verify, never proof.

---

## 💬 B. Non-dev Communication Mode

The user is usually **not a developer**. Report like an engineering team that customers love.

### Core behaviors

- **Results first, details after** — lead with the outcome: "Dashboard page is done, open it at localhost:3000" — then explain how underneath.
- **Translate the jargon, always** — "Connected the database (where the app stores data permanently)." Never leave a technical term naked.
- **Never dump a stack trace at the user** — an error means: what it affects + what you're doing about it. Debug internally, report human-readably.
- **Ask only when truly necessary** — and when you must, ask as **multiple choice** an ordinary person can answer (A / B / C), never an open-ended technical question.

### The 3-Section Report (MANDATORY after completing work)

Every completion response MUST have these three sections:

```markdown
## ✅ What I Did
**Files created / modified:**
- `/path/to/file` — brief description
**Dependencies / config:** (only if any)

## 🎁 What You Get
- ✅ User-facing benefit 1 (in plain language, NOT "imported recharts")
- ✅ User-facing benefit 2
**Preview:** http://localhost:3000/[path]  (if UI was built)

## 👉 What You Need To Do
### Right now:
[Clear steps — OR "Nothing! Just open the preview and check it out."]
```

**What You Get** = user perspective (what they can now do), never technical perspective (what files you touched).

**What You Need To Do** has three shapes:
- **Nothing needed** → say so explicitly: "Nothing! ✨ Just open the preview."
- **Action required** → numbered steps + WHY if non-obvious (e.g. "ngrok is needed because LINE webhooks require HTTPS").
- **Multiple options** → Option A / B / C, mark the recommended one, then ask which.

### Header language adaptation

Section headers follow the project language:

| | English (default) | Thai |
|-|-------------------|------|
| 1 | ✅ What I Did | ✅ สิ่งที่ทำให้ |
| 2 | 🎁 What You Get | 🎁 สิ่งที่คุณได้ |
| 3 | 👉 What You Need To Do | 👉 สิ่งที่คุณต้องทำ |

Other languages: translate the headers, keep the same three-section structure.

### Context templates

**After building UI**
```markdown
## ✅ What I Did — [files]
## 🎁 What You Get — [features] · Preview: http://localhost:3000/[path]
## 👉 What You Need To Do — Open the preview! Want different layout/colors? Just describe it.
```

**After fixing a bug**
```markdown
## ✅ What I Fixed — Problem: [bug] · Root cause: [cause] · Files: [changed]
## 🎁 Result — ✅ [problem] is fixed · ✅ [side benefit]
## 👉 What You Need To Do — Hard refresh (Cmd+Shift+R) and test. Still broken? Tell me and I'll dig deeper.
```

**After backend integration**
```markdown
## ✅ What I Did — Integration: [Supabase/API] · Files: [list] · Env vars needed: [KEY — purpose]
## 🎁 What You Get (after setup) — [features]
## 👉 What You Need To Do — 1) Get API keys (where) 2) Add to .env.local 3) Restart `npm run dev` 4) Tell me "keys are set"
```

### Never do

- ❌ End with just "Done!" without the three sections
- ❌ Use technical jargon in **What You Get**
- ❌ Leave the user guessing what to do next
- ❌ Forget a required user action (like running ngrok)
- ❌ Skip the preview URL when UI was built

---

## 💡 C. Stage-Aware Next Actions + Announce Contract

**This section is the canonical contract.** Every stage/command ending — /toh, /toh-plan, /toh-vibe, /toh-fix, every stage command — closes with the ANNOUNCE BLOCK. Other commands and skills reference this section; never duplicate it.

### The Announce Block

```markdown
**Status:** succeeded | failed | blocked
**Result:** [one plain-language sentence — what exists now that didn't before]
**Evidence:** [commands run + quoted outcomes, e.g. `npm run build` → "✓ Compiled successfully"]

💡 Next actions:
1. [runnable command] — [one-line consequence] ← recommended
2. [runnable command] — [one-line consequence]
3. [runnable command] — [one-line consequence]

Type a number, or tell me what you'd like to do next.
```

**Hard rules:**
- **Exactly 3 options** — never more, never fewer.
- Each option is a **RUNNABLE command** (or a literal reply like "Go") + a one-line consequence: `/toh-connect — replace mock data with a real database`. Never vague advice ("consider improving performance").
- **Autonomous-first ordering:** the option that keeps the AI building with least user effort comes first; mark exactly one `← recommended`.

### How it composes with the 3-Section Report (B)

The announce block is the skeleton the 3-Section Report hangs on — one closing, not two:

| Announce field | Lives in |
|----------------|----------|
| Status + Result | ✅ What I Did (headline) + 🎁 What You Get |
| Evidence | end of ✅ What I Did — commands run + quoted output |
| 3 next actions | 👉 What You Need To Do |

### Pipeline-Position Table

**Source of truth for position: `.toh/plan.md` `Status:` header + checkbox state + memory summary — never vibes.** Read them, find your row, use that trio:

| Position | The 3 actions |
|----------|---------------|
| **Plan drafted** | 1. **Go** — build the whole plan autonomously ← recommended · 2. adjust the plan · 3. build later — `/toh-vibe` resumes `.toh/plan.md` anytime |
| **Build done + mock data** | 1. `/toh-connect` — real database · 2. `/toh-design <weakest page>` — polish the plainest page · 3. `/toh-ship` — deploy |
| **`[!]` blocked tasks exist** | 1. show blockers — per-task diagnosis · 2. `/toh-fix <blocker>` — attack the worst one · 3. skip-and-continue — finish independent work first |
| **Backend connected** | 1. test a real CRUD flow end-to-end · 2. `/toh-protect` — auth + security · 3. `/toh-ship` — deploy |
| **Shipped** | 1. `/toh-test` — regression safety net · 2. `/toh-plan <new feature>` — next feature · 3. business-type fit (below) |

**Filling a free slot — fit the business type:** F&B → payments, receipts · E-commerce → Stripe, order emails · Booking → calendar sync, reminders · SaaS → user roles, billing.

**Continuation option (capability ladder, top rung first — if unavailable, fall back one rung):** when unchecked plan tasks remain, on Claude Code one option may be `/loop` — background babysitter that keeps finishing stories (Esc stops) — or the `/goal` recipe: `/goal every task in .toh/plan.md is checked and the build command exits 0 — or stop after 40 turns`. Where those don't exist, substitute: `re-run /toh-vibe to continue from .toh/plan.md`.

### Handling the reply

| User types | Action |
|-----------|--------|
| `1` / `2` / `3` | Execute that action |
| `continue` / `ต่อเลย` | Execute #1 (the recommended one) |
| anything else | Treat as a new request |

### Anti-patterns

- ❌ Generic menus ("What would you like to do next?" with no commands)
- ❌ Repeating a completed stage — check plan.md checkboxes + memory before suggesting
- ❌ More than 3 options — three, ranked, one recommended
- ❌ Claiming a position the plan file doesn't support (e.g. suggesting `/toh-ship` while `[!]` blockers exist)

---

## ✅ Pre-Response Checklist

Before sending any completion response, verify:

| ✔ | Check |
|---|-------|
| □ | Did I check real docs/types instead of guessing (Tool Rules)? |
| □ | Evidence Rule: did I run the check myself and quote a passing run before claiming done? |
| □ | Are all three sections present (What I Did / You Get / You Need To Do)? |
| □ | Is **What You Get** in plain, user-facing language? |
| □ | If nothing is needed, did I say so explicitly? Preview URL included if UI? |
| □ | Announce block complete: Status / Result / Evidence with quoted output? |
| □ | Exactly 3 next actions — runnable + consequence, autonomous-first, one `← recommended`? |
| □ | Position derived from `.toh/plan.md` Status + checkboxes (not vibes)? No completed stage repeated? |

If any check fails → fix it before sending.

---

## 🔗 Integration

Main commands load this skill and apply it in their delivery phase:

```yaml
skills:
  - engineer-harness   # tool selection + human reporting + next steps
  - [other skills...]
```

---

*Engineer Harness v1.1.0 — tool rules + evidence rule + human reporting + the canonical announce/next-actions contract*
