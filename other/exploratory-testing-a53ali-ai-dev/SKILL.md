---
name: exploratory-testing
description: Conduct structured exploratory testing using test charters, session-based test management (SBTM), and testing heuristics. Exploratory testing finds bugs that scripted tests miss by combining simultaneous learning, design, and execution. Covers when to use it, how to plan sessions, and how to report findings.
triggers:
  - "exploratory testing"
  - "explore the feature"
  - "unscripted testing"
  - "find bugs"
  - "test charter"
  - "what could go wrong"
  - "edge cases to test"
  - "charter based testing"
audience:
  - qa
  - engineer
---

# Exploratory Testing

Find the bugs that scripted tests miss — through simultaneous learning, design, and execution.

---

## What Exploratory Testing Is (and Isn't)

**Is**: Structured, skilled, documented investigation of software using judgment, creativity, and heuristics — guided by a charter with a time-box.

**Is not**: "Just clicking around." Undocumented random clicking is *ad hoc* testing. Exploratory testing is deliberate and produces reproducible findings.

**Finds**: Integration failures, UX breakdowns, race conditions, unexpected state combinations, and anything that scripted tests didn't anticipate because the scenario wasn't imagined during planning.

**Does not replace**: Automated regression tests. Complements them — automate the known, explore the unknown.

---

## Session-Based Test Management (SBTM)

Break exploratory testing into **sessions**: time-boxed, charter-driven, individually reported.

### Session anatomy
```
Charter:    [What are we investigating?]
Duration:   [45-90 min]
Setup:      [What state/data is needed to begin?]
Notes:      [Live notes during the session]
Bugs:       [What was found]
Issues:     [What blocked you]
Coverage:   [What did you actually test?]
Debrief:    [5-min verbal or written summary]
```

---

## Test Charter Template

A charter answers: **Explore [area/feature] with [technique/focus] to discover [risk/question]**

```markdown
## Session Charter

**Explore**: [specific feature, flow, or component]
**With**: [technique — e.g., boundary values, state transitions, negative input, concurrent users]
**To discover**: [what risk or question you're investigating]

**Duration**: 60 minutes
**Environment**: [staging / local / specific build]
**Preconditions**: [account state, data, feature flags]

**Out of scope** (for this session): [what you're deliberately NOT testing]
```

### Charter examples

```
Explore: the checkout flow with promo codes
With: boundary values (expired, invalid, duplicate, empty, max length)
To discover: whether invalid promo codes are handled gracefully without corrupting the cart

---

Explore: concurrent order creation
With: two browser sessions logged in as the same user
To discover: whether duplicate orders can be created or inventory oversold

---

Explore: the password reset flow
With: state manipulation (expired tokens, already-used tokens, tokens from other accounts)
To discover: whether authentication boundaries hold under adversarial input
```

---

## Testing Heuristics (SFDPOT / FEW HICCUPPS)

Use heuristics to generate test ideas when you don't know where to start.

### SFDPOT (Structure, Function, Data, Platform, Operations, Time)
| Heuristic | Test ideas |
|---|---|
| **Structure** | What components make up the feature? Test each component and their interactions |
| **Function** | What should it do? Test that it does it, and that it doesn't do things it shouldn't |
| **Data** | What data does it process? Test: empty, null, boundary, max, special chars, injection |
| **Platform** | Where does it run? Test: browsers, OS, screen sizes, network conditions |
| **Operations** | How is it used in production? Test: concurrent users, high frequency, interruption |
| **Time** | When/how long? Test: timing boundaries, expiration, race conditions, time zones |

### FEW HICCUPPS (Consistency heuristics)
Ask: is this consistent with...
- **F**unctions it previously performed?
- **E**xpectations from specs and AC?
- **W**ords — do labels, messages, and names match behavior?
- **H**istory — does it work the same as before?
- **I**mage — does it match your mental model of what it should do?
- **C**omparable products?
- **C**laims in documentation?
- **U**ser expectations?
- **P**roduct principles and brand guidelines?
- **P**urpose — does it help users achieve their goal?
- **S**tatutes — does it comply with legal/regulatory requirements?

---

## Session Notes Template

Keep live notes during the session — they become your defect report and coverage log.

```markdown
## Session Notes: [Charter title]
**Tester**: [name]
**Date**: [date]
**Build**: [version/commit]
**Duration**: [actual time]

### Timeline
[HH:MM] Started. Environment: [state]
[HH:MM] Tested [action] — [result — pass/fail/note]
[HH:MM] Found: [brief bug description] → [filed as BUG-XXX]
[HH:MM] Noticed: [observation — not a bug but worth noting]
[HH:MM] Blocked by: [issue]
[HH:MM] Ended.

### Bugs Found
| ID | Title | Severity |
|---|---|---|
| BUG-XXX | [title] | P1/P2/P3 |

### Coverage Summary
[What was covered, what was not covered, and why]

### Follow-up Sessions Needed
- [ ] [area you identified but didn't have time to explore]
```

---

## When to Use Exploratory Testing

| Situation | Use it? |
|---|---|
| New feature, first look | ✅ Yes — learn the feature before writing scripted tests |
| Complex user flow with many states | ✅ Yes — automation misses state combinations |
| After a major refactor | ✅ Yes — regressions in unexpected places |
| Security and auth boundaries | ✅ Yes — adversarial mindset is essential |
| Before a release | ✅ Yes — final risk reduction pass |
| Simple CRUD form, well-covered by automation | 🟡 Optional — low value relative to time |
| Regression testing known stable flows | ❌ No — use automated tests |

---

## Debrief Format

After each session, a 5-minute debrief (verbal or written):

```
1. What did you test?
2. What did you find?
3. What risks remain uncovered?
4. What would you do differently next session?
```

The debrief surfaces insights that didn't make it into the notes and drives the next charter.

---

## AI-Assisted Charter Generation

```
Feature under test: [description]
Known acceptance criteria: [paste AC]
Recent changes: [what was changed in this build]

Generate 3 exploratory test charters in the format:
  Explore [area] with [technique] to discover [risk]

Focus on:
1. Integration points and state transitions
2. Boundary and negative input scenarios
3. Security/permission boundaries
Flag any areas where exploratory testing is higher value than automation.
```

---

## References
- James Bach & Michael Bolton: [Session-Based Test Management](https://www.satisfice.com/articles/sbtm.pdf)
- Elisabeth Hendrickson: *Explore It!* (the definitive book on exploratory testing)
- Jonathan Bach: [SFDPOT Heuristic](http://www.satisfice.com/tools/heuristics.pdf)
- Michael Bolton: [FEW HICCUPPS](https://developsense.com/resources/few-hiccupps/)
- LeadDev: [Modern QA practices](https://leaddev.com/testing-qa)
