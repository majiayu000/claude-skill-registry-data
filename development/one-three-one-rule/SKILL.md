---
name: one-three-one-rule
description: >
  Structured decision-making framework for technical proposals and trade-off analysis.
  When the user faces a choice between multiple approaches (architecture decisions,
  tool selection, refactoring strategies, migration paths), this skill produces a
  1-3-1 format: one clear problem statement, three distinct options with pros/cons,
  and one concrete recommendation with definition of done and implementation plan.
  Use when the user asks for a "1-3-1", says "give me options", or needs help
  choosing between competing approaches.
version: 1.1.0
author: Willard Moore
license: MIT
category: communication
metadata:
  hermes:
    tags: [communication, decision-making, proposals, trade-offs]
---

# 1-3-1 Communication Rule

Structured decision-making format for when a task has multiple viable approaches and the user needs a clear recommendation. Produces a concise problem framing, three options with trade-offs, and an actionable plan for the recommended path.

## When to Use

- The user explicitly asks for a "1-3-1" response.
- The user says "give me options" or "what are my choices" for a technical decision.
- A task has multiple viable approaches with meaningful trade-offs (architecture, tooling, migration strategy).
- The user needs a proposal they can forward to a team or stakeholder.

Do NOT use for simple questions with one obvious answer, debugging sessions, or tasks where the user has already decided on an approach.

## Procedure

1. **Problem** (one sentence)
   - State the core decision or desired outcome in a single concise sentence.
   - Focus on the *what*, not the *how* — no implementation details, tool names, or specific technologies.
   - Keep it tight. If you need "and", you're describing two problems.

2. **Options** (exactly three)
   - Present three distinct, viable approaches labeled A, B, C.
   - Each option gets a brief description, pros, and cons.
   - Options should represent genuinely different strategies, not minor variations of the same approach.

3. **Recommendation** (one option)
   - State which option you recommend and why, based on the user's context and priorities.
   - Be direct — this is your professional judgment, not a hedge.

4. **Definition of Done**
   - List the specific success criteria for the recommended option.
   - These are concrete, verifiable outcomes — not vague aspirations.
   - If the user picks a different option, revise this section to match.

5. **Implementation Plan**
   - Concrete steps to execute the recommended option.
   - Include specific commands, tools, or actions where applicable.
   - If the user picks a different option, revise this section to match.

## Verification

- Response has exactly one Problem sentence.
- Response has exactly three Options (A, B, C) with pros and cons for each.
- Response has a single Recommendation that picks one option with reasoning.
- Definition of Done and Implementation Plan align with the recommended option.
- If the user selects a different option, Recommendation, DoD, and Implementation Plan update accordingly.

## Example

User: "Give me a 1-3-1 for adding retry logic to our API client."

Agent:

**Problem:** API calls to external services fail intermittently under load and need graceful retry handling.

**Options:**

- **Option A: Exponential backoff with jitter in a shared utility.**
  Pros: Simple, well-understood pattern; single implementation shared across all callers.
  Cons: No circuit-breaking; callers still block during retries.

- **Option B: Retry library (tenacity) as a decorator on each endpoint call.**
  Pros: Configurable per-endpoint; built-in support for circuit breakers and rate limits.
  Cons: Adds a dependency; decorator pattern can obscure control flow.

- **Option C: Queue-based async retry with dead letter handling.**
  Pros: Non-blocking; failed calls are tracked and replayable; scales well.
  Cons: Significant complexity increase; requires a queue backend; overkill for low-volume services.

**Recommendation:** Option A. The call volume doesn't justify queue infrastructure, and a shared utility with exponential backoff + jitter covers the failure mode cleanly without new dependencies.

**Definition of Done:**
- `api_retry()` utility handles transient HTTP errors (429, 502, 503, 504).
- Retries up to 3 times with exponential backoff and jitter.
- All external API calls route through the retry utility.
- Logs each retry attempt with endpoint and attempt number.
- Tests cover retry exhaustion, immediate success, and transient-then-success scenarios.

**Implementation Plan:**
1. Create `utils/api_retry.py` with configurable max retries, base delay, and retryable status codes.
2. Add jitter using `random.uniform(0, base_delay)` to prevent thundering herd.
3. Wrap existing API calls in `api_client.py` with the retry utility.
4. Add unit tests mocking HTTP responses for each retry scenario.
5. Verify under load with a simple stress test against a flaky endpoint mock.

---

## R23 Verification Pattern (Added 2026-08-03)

When proposing options, every option must include a **Verification** subsection that answers:

1. **What command or curl shows success?** (e.g., `curl -s http://127.0.0.1:8645/api/X | head -c 200`)
2. **What number goes up after shipping?** (e.g., "endpoint count goes from 24 to 25")
3. **What does the user see that proves it works?** (e.g., "log output shows cost_alert fired and dispatched to Telegram")

### Verification Anti-Patterns

❌ "Should work" — never acceptable
❌ "I tested it" without showing output
❌ "Looks correct" — vague
❌ "Likely succeeds" — hedging

### Verification Patterns That Work

✅ "Exit code 0 from `python3 script.py` after running on real data"
✅ "Endpoint returns 432 bytes of JSON with the expected schema"
✅ "Cron registers cleanly with `hermes cron list` showing it; manual run succeeds"
✅ "curl -u admin:hermes http://... returns {success: true, count: 5}"

### When The Verification Is Hard

Sometimes you can't verify end-to-end immediately (e.g., "after 7 days of trace data"). In that case:

1. **State what you DID verify** (e.g., "registry entry created, content registered")
2. **State what's PENDING** (e.g., "awaiting 7 days of trace data for promotion decision")
3. **State when you'd re-check** (e.g., "re-run on 2026-08-10")

This is the **honest skip** pattern — better to acknowledge uncertainty than fake verification.

---

## Round-Based Decision Making

When the user asks "do all of this" or gives broad instructions, use 1-3-1 to anchor decisions, then decompose into R-N tasks:

| Decision area | Use 1-3-1 here | Why |
|---------------|----------------|-----|
| Architecture choice | ✓ | Multi-option trade-offs |
| Tool selection | ✓ | Different stack implications |
| Migration strategy | ✓ | Affects timeline + risk |
| Specific bug fix | ✗ | Just do it |
| "Add an endpoint" | ✗ | Obvious approach |
| New file/script | ✗ | Just write it |

For round-based work (R-N), the recommendation in 1-3-1 should specify which R-N tasks will implement it. E.g., "Option A: Recommendation. Implement as R23-1 (build), R23-2 (test), R23-3 (commit)."
