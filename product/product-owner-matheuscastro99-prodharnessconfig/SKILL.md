---
name: product-owner
description: Product lens for BabyBuddyHelper. Checks a proposed feature, backlog item or scope question for caregiver value, Parenting Companion fit, cost, architectural impact and roadmap timing, then gives a P0-P3 priority. Use when a feature is proposed, when an issue's scope or acceptance criteria are unclear, or when comparing what to build next.
---

# Product Owner

This skill adds a product lens on top of the session context. It produces a **recommendation**. The project owner decides scope, priority and roadmap.

## 1. Load context

- `docs/ProjectVision.md` for identity and what the app is not
- `docs/ai/context/ROADMAP.md` and `docs/ai/context/CURRENT_STATE.md` for the current phase and what's next
- `docs/FeaturesSet.md` for what already exists (don't propose what's shipped)
- The GitHub issue and its comments, if one exists (`gh issue view <n> --comments`), because the owner records decided scope there

## 2. Evaluate

**User need.** Which caregiver problem does it solve, for whom, and how often? Daily-use, time-saving and reminder features rank higher than rare or novelty ones.

**Parenting Companion fit.** Does it make the app feel more helpful, supportive and encouraging, or just more feature-rich? Reject drift toward a generic task manager, an enterprise planner, a social network or a productivity suite.

**Cost** (Low / Medium / High). Count implementation, UI and testing effort, plus ongoing maintenance. Remember that testing is manual, done by the owner, on every entity.

**Architectural impact** (None / Low / Medium / High). Does it touch the cache services (`TaskListService`, `BabyProfileService`), the persistence boundary (`ITrackerDbService` → EF Core + SQLite), the models or the scheduler projection? Would it need schema changes or cloud sync? Flag anything that conflicts with an ADR.

**Timing.** Does it serve the current phase, or does it belong to a later one (MVVM in Phase 4, cloud and backup in Phase 5, companion AI in Phases 6 and 7)? Good features in the wrong phase get "Next phase", not "Now".

**Expansion value.** Is it foundational (notifications, recurring appointments, local persistence), or a one-off?

Don't prioritize something just because it's technically interesting, other apps have it, or it's easy.

## 3. Priority

- **P0 Foundational.** Later roadmap work depends on it.
- **P1 High value.** Strong caregiver value at a reasonable cost.
- **P2 Nice to have.** Improves the experience but isn't essential.
- **P3 Low.** Novelty, purely cosmetic, or experimental.

## 4. Output

- **Feature summary** (one or two lines)
- **User value / Companion fit / Cost / Architectural impact**, each rated Low, Medium or High
- **Priority** (P0 to P3)
- **Recommendation:** Now / Next phase / Backlog / Reject
- **Advantages vs. disadvantages**, and why this fits *this* project now
- **Acceptance criteria** as a short checklist, when scoping an issue
- **Open decisions for the owner.** When the call is ambiguous, give 2-3 options with one marked as recommended.
