---
name: prd-generator
description: 'Generate complete PRD in 15-20min for ANY project using 5-battery question framework. Detects briefing (from context or user input), runs structured Q&A, outputs PRD.md with vision+scope+tech+timeline+KPIs+risks. Use when: "create PRD", "generate PRD for", "build PRD", "need PRD". NOT for: tech spec, design docs, task breakdown.'
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# PRD Generator Skill

Generate complete, production-ready PRD in 15-20 minutes for ANY project type using a structured 5-battery question framework. Detects existing briefing from conversation context or collects it interactively. Outputs PRD.md file with 13 sections: vision, scope, tech, timeline, KPIs, risks, constraints.

## Workflow Overview

```
Extract/Collect Briefing (2 min)
    ↓
Battery 1: Strategy (3 min) — scope + users + timeline
    ↓
Battery 2: Architecture (3 min) — state + platforms + monetization
    ↓
Battery 3: Features (3 min) — scope + auth + offline
    ↓
Battery 4: Operations (2 min) — controls + ads + analytics
    ↓
Battery 5: Dependencies (2 min) — backend + constraints
    ↓
Synthesize (1 min) — no more questions
    ↓
Generate PRD.md (2 min) — 13-section output file
```

**Total: 18 minutes**

---

## Instructions

### Step 0: Briefing Detection & Collection

Check conversation history for existing briefing about the project. Briefing is 2-5 sentences describing the problem/solution (what, who, why).

If briefing exists: Parse it. Extract: problem statement, target users (implicit or explicit), rough scope.

If briefing does NOT exist: Collect it interactively.

```
User: "I need to build a PRD"
You: "Brief me — what's the project? 2-5 sentences on problem, solution, audience."
User: [provides briefing]
```

Confirm understanding (1 sentence):

```
"Building [X] for [Y], solving [Z]. Start batteries?"
```

Expected output: Clear problem statement + user context + rough direction.

---

### Step 1: Battery 1 – Strategy (3 minutes)

Use `AskUserQuestion` with these 3 questions (single batch, sequential):

**Q1.1 — MVP Scope**

```
Question: "What's the MVP scope?"
Options:
  A) Bare minimum (5–10 features, absolute essentials)
  B) Core + management (10–20 features, essential + nice-to-have)
  C) Full-featured (20+ features, everything)
  D) Custom scope (user specifies)
```

**Q1.2 — Target Users**

```
Question: "Who uses this and for what?"
Options:
  A) Single persona (one user type, one use case)
  B) Dual persona (two distinct users or business models)
  C) Multi-persona (3+ user types with different flows)
  D) Custom (user specifies)
```

**Q1.3 — Timeline**

```
Question: "MVP deadline?"
Options:
  A) Very urgent (< 6 weeks)
  B) Normal (6–12 weeks)
  C) Relaxed (3–6 months)
  D) Flexible (user specifies exact date)
```

**Capture answers.** Proceed to Battery 2 immediately (no synthesis yet).

---

### Step 2: Battery 2 – Architecture (3 minutes)

Use `AskUserQuestion` with these 3 questions:

**Q2.1 — Codebase State**

```
Question: "Starting from?"
Options:
  A) Greenfield (zero existing code)
  B) Existing codebase (reuse part of code)
  C) Wrap/enhance (encapsulate legacy)
  D) Incremental (v1 is slice of bigger product)
```

**Q2.2 — Platforms**

```
Question: "Platforms + rollout?"
Options:
  A) Single platform (web, mobile, desktop, or API)
  B) Multi-platform simultaneous (web + iOS + Android together)
  C) Multi-platform phased (Android first → webOS later)
  D) Agnóstic (works anywhere)
```

**Q2.3 — Business Model**

```
Question: "How monetize or measure success?"
Options:
  A) Ad-supported (free with ads)
  B) Subscription (paid)
  C) Freemium (free + premium)
  D) B2B/white-label (sell to other companies)
  E) Custom or undecided
```

**Capture answers.** Proceed to Battery 3.

---

### Step 3: Battery 3 – Features (3 minutes)

Use `AskUserQuestion` with these 3 questions:

**Q3.1 — Feature Details**

```
Question: "Core features (top 5–10)?"
Options:
  A) Just core functionality (minimal scope)
  B) Core + management (search, favorites, settings, etc)
  C) Core + management + social (+ sharing, reviews, etc)
  D) Custom (user specifies exact features)
```

**Q3.2 — Authentication & Data**

```
Question: "Data/auth model?"
Options:
  A) None (public, no auth)
  B) Simple local (username/password, local storage)
  C) External auth (OAuth, SSO, integrate with existing system)
  D) Multi-tenant (one user, multiple accounts/contexts)
```

**Q3.3 — Offline/Sync**

```
Question: "Offline capability needed?"
Options:
  A) Always online (no offline, no caching)
  B) Cache read (local cache, no persistent downloads)
  C) Offline read+write (cache with sync when online)
  D) Full offline (data stored locally, optional sync)
```

**Capture answers.** Proceed to Battery 4.

---

### Step 4: Battery 4 – Operations (3 minutes)

Use `AskUserQuestion` with these 3 questions:

**Q4.1 — User Controls**

```
Question: "What controls does user have?"
Options:
  A) Minimal (playback/navigation only)
  B) Basic management (favorites, search, history)
  C) Personalization (recommendations, profiles, tracking)
  D) Custom (user specifies)
```

**Q4.2 — Monetization Tech**

```
Question: "Monetization tech (if applicable)?"
Options:
  A) Ads simple (banners, pre-roll video)
  B) Ads complex (VAST, programmatic, tracking)
  C) Subscription (payment gateway, recurring billing)
  D) Hybrid (ads + premium tiers)
  E) Undecided (will decide later)
```

**Q4.3 — Analytics**

```
Question: "Telemetry/analytics?"
Options:
  A) Crashes only (Firebase Crashlytics)
  B) Basic (user sessions, device info)
  C) Detailed (custom events, funnels, heatmaps)
  D) Minimal (logs only, no PII)
```

**Capture answers.** Proceed to Battery 5.

---

### Step 5: Battery 5 – Dependencies (2 minutes)

Use `AskUserQuestion` with these 2 questions:

**Q5.1 — Backend Scope**

```
Question: "Backend/admin panel needed?"
Options:
  A) No (client-only, existing APIs only)
  B) Minimal (basic CRUD, no complex logic)
  C) Complete (multiple roles, workflows, admin dashboard)
  D) Phased (v1 is client-only, backend in v1.1+)
```

**Q5.2 — Constraints & Resources** (multi-select)

```
Question: "What tech/resources exist?"
Options (select all that apply):
  A) Existing codebase/libraries
  B) Existing test infrastructure/CI/CD
  C) Existing 3rd-party services (payment, analytics)
  D) Regulatory constraints (HIPAA, GDPR, PCI-DSS)
  E) Legacy systems to integrate
  F) None / greenfield
```

**Capture answers.**

---

### Step 6: Synthesize (1 minute)

Do NOT ask more questions.

Review all answers. Verify you have:

- [ ] Scope clear (MVP defined)
- [ ] Users/personas clear
- [ ] Timeline explicit
- [ ] Tech direction clear (or TBD noted)
- [ ] Top 5–10 features identified
- [ ] Business model clear
- [ ] Blockers/constraints documented

If 1–2 areas are unclear, note them as **TBD** in PRD (max 15% uncertainty is healthy).

---

### Step 7: Generate PRD (2 minutes)

Use `Write` tool to create `PROJECT_ROOT/PRD.md`.

Structure: 13 sections per `references/prd-template.md`.

Fill each section using Battery answers. Key mappings:

| Section                           | Source                                                 |
| --------------------------------- | ------------------------------------------------------ |
| 1. Executive Summary              | All batteries (distill to 1–2 paras)                   |
| 2. Vision & Goals                 | Battery 1 (scope + users + timeline → goals)           |
| 3. Target Users                   | Battery 1 (users) + context                            |
| 4. MVP Features                   | Battery 3 (features) + Battery 1 (scope)               |
| 5–6. Architecture & Tech          | Battery 2 (platforms, state) + Battery 5 (constraints) |
| 7. Data Model                     | Battery 3 (auth, data)                                 |
| 8. User Flows                     | Synthesize from Batteries 1–4                          |
| 9. KPIs                           | Battery 2 (business model) → metrics                   |
| 10. Timeline                      | Battery 1 (timeline) → phases                          |
| 11. Risks                         | Battery 5 (constraints, dependencies)                  |
| 12–13. Constraints & Out of Scope | Battery 1 (scope) + all batteries                      |

**Output expectations:**

- 400–700 lines markdown
- Sections balanced (vision → execution → success)
- TBDs explicit (decision trees, defer-to dates)
- Ready for handoff to engineers

---

## Examples

### Example 1: IPTV Player (RipTV)

**User input:** "Building IPTV player. React frontend, Android/webOS/Tizen. Uses xtream code server. Free + ads + licensing model. <3 months."

**Battery 1 answers:**

- Scope: Core + management (play + favorites + search + history + parental controls)
- Users: Both personal + commercial
- Timeline: < 3 months (very urgent)

**Battery 2 answers:**

- State: Greenfield
- Platforms: Android first → webOS/Tizen later (phased)
- Monetization: Freemium (ads + B2B licensing)

**Battery 3 answers:**

- Features: Full (Live TV + VOD + Series + EPG)
- Auth: Direct xtream server login
- Offline: Streaming only (no offline)

**Battery 4 answers:**

- Controls: Basic (favorites, search, history, parental PIN)
- Ads: Undecided (decision tree in PRD)
- Analytics: Detailed custom events

**Battery 5 answers:**

- Backend: Not in MVP (v1.1)
- Constraints: Existing xtream servers to test against

**Output:** `PRD.md` with 13 sections, 550 lines, ready for engineering sprint.

---

### Example 2: SaaS Project Management Tool

**User input:** "SaaS PM tool for teams. Web-first. Subscription model. Collaborative task boards + timeline view + integrations."

**Battery 1 answers:**

- Scope: Core + management
- Users: Teams (3–4 personas: PM, developer, designer)
- Timeline: 6–12 weeks (normal)

**Battery 2 answers:**

- State: Greenfield
- Platforms: Web (responsive) + mobile web later
- Monetization: Subscription (tiered pricing)

**Battery 3 answers:**

- Features: Core + management
- Auth: OAuth (GitHub, Google, email)
- Offline: Cache read (no persistent offline)

**Battery 4 answers:**

- Controls: Basic (permissions, org settings)
- Ads: None (paid-only)
- Analytics: Detailed (feature adoption, engagement funnels)

**Battery 5 answers:**

- Backend: Complete (user management, billing, webhooks)
- Constraints: Greenfield + need Stripe integration

**Output:** `PRD.md` with emphasis on multi-user workflows, subscription metrics, integration strategy.

---

## Troubleshooting

### Issue: Briefing too vague

**Cause:** User hasn't thought through problem clearly.

**Solution:** Ask: "What's the one sentence describing what this solves?" Then: "Who feels that pain?" Then: "Why now?"

### Issue: Answers conflict (e.g., "< 6 weeks" + "20+ features")

**Cause:** User wants everything fast.

**Solution:** Note in PRD: "High risk — timeline and scope misaligned. Recommend cutting 60% of features OR extending timeline to 12 weeks."

### Issue: User keeps adding "one more thing"

**Cause:** Scope creep during Q&A.

**Solution:** Say: "Write that down. It goes in v1.1 (out-of-scope for MVP). Focus on the 5–10 core features."

### Issue: TBDs pile up (>20% of PRD)

**Cause:** User not ready to make decisions.

**Solution:** Ask: "What's the ONE TBD that blocks you most? Let's decide that now." Defer the rest.

### Issue: Project already has PRD

**Cause:** User wants to refine, not create.

**Solution:** Out of scope for this skill. Use for NEW projects only.

---

## Important Notes

- **Speed is feature:** 18-min target is strict. If Battery Q&A goes >15 min total, move to PRD generation regardless of certainty. Iterate later.
- **Flexibility:** If user has strong opinions on a Battery answer, accept and move on. PRD doesn't require perfect exploration.
- **TBDs are OK:** 10-15% unknown is healthy. Decision trees in PRD clarify unknowns.
- **Not a design doc:** This generates requirements, not architecture design or technical specification. Those come AFTER PRD.
- **Reusable template:** Full PRD sections in `references/prd-template.md`. Use as-is for consistency across projects.
- **Project-specific patterns:** See `references/patterns.md` for tech stack / feature recommendations by project type (SaaS, mobile, backend, etc.).

---

## Next Steps After PRD

1. **Tech Spec:** Engineer reads PRD → writes detailed tech spec (5–15 pages)
2. **Design:** Designer reads PRD → creates wireframes + flows
3. **Tasks:** PM reads PRD → breaks into sprints + tasks
4. **QA:** Tester reads PRD → writes test cases + acceptance criteria
5. **Review:** Leadership approves scope, timeline, budget
