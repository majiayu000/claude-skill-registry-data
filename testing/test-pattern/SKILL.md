---
name: test-pattern
description: Tests whether patterns actually work — trigger, emerge, and produce value. Use when (1) user wants to verify a pattern before relying on it, (2) user runs /test-pattern command, (3) a pattern was just recorded and needs verification, or (4) user suspects a pattern isn't working as expected.
---

# Test Pattern

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.

---

## Core Tenet

Testing patterns is different from testing compliance skills. We're not asking "did it follow the rule?" but "did the dance happen?"

**Integration with iterative-loop-engine:** For patterns with clear pass/fail criteria,
use `/loop` to iterate testing until confidence is reached.

---

## What We're Testing

### 1. Triggering
**Question:** Given the described conditions, does the pattern get invoked?

**Method:**
- Create scenarios that match trigger conditions
- Run conversation, observe if pattern is recognized/invoked
- Pass: Pattern activates when conditions match
- Fail: Conditions present but pattern not invoked

### 2. Pattern Emergence
**Question:** When invoked, does the described interaction dynamic actually occur?

**Method:**
- Invoke the pattern explicitly
- Run the interaction
- Check: Can an observer recognize the pattern?
- Pass: "Yes, that's the pattern described"
- Fail: "The words are there but the dance didn't happen"

**What to look for:**
- The structural elements actually appear (not just referenced)
- The interaction has the described *shape*
- It doesn't collapse into monologue or Q&A

### 3. Propagation
**Question:** Does the Vasana section work?

**Method:**
- Run conversations where useful patterns emerge
- Check: Does the pattern suggest capturing new patterns?
- Check: Is the suggestion appropriate (not every conversation)?
- Check: Does created pattern include Vasana section?
- Pass: Appropriate suggestions, complete new patterns
- Fail: Never suggests, always suggests, incomplete Vasana section

### 4. Value (The Hard One)
**Question:** Does this pattern produce something useful?

**Honest limitation:** This cannot be tested objectively. There's no binary pass/fail.

**Proxy measures:**
- **Behavioral:** Human chooses to keep/share the pattern (signal of perceived value)
- **Subjective report:** Human says it helped
- **Shift observation:** Something observably changed (stuck→unstuck, vague→clear)
- **Comparison:** "Was this different from how you usually work?"

---

## Test Checklist for New Patterns

### Before Release

- [ ] **Trigger test:** Created scenarios matching conditions, pattern invokes
- [ ] **Pattern test:** Invoked pattern, dynamic recognizably emerged
- [ ] **Vasana section test:** Section present and functional
- [ ] **At least one value signal:** Human reports usefulness OR chooses to keep/share

### Ongoing (As Pattern Is Used)

- [ ] **Track:** How often invoked? How often propagation suggested?
- [ ] **Collect:** Human feedback on value
- [ ] **Watch for:** Degradation (pattern stops emerging), false triggers

---

## Pressure Testing

Pattern pressure testing asks: **Does the pattern survive being rushed/interrupted/compressed?**

**Pressure scenarios:**
- **Time pressure:** "We need this in 10 minutes"
- **Interruption:** Break the flow, see if pattern can resume
- **Complexity:** Scenario more complex than pattern was designed for
- **Distraction:** Other priorities competing for attention

**What we learn:**
- Which patterns are robust vs. fragile
- Where patterns break down
- Whether degraded pattern still produces value

**Important:** Some patterns need time. A 45-minute collaborative exploration can't happen in 10 minutes. That's not failure — it's knowing the pattern's requirements.

---

## When Testing Fails

After a pattern fails to emerge or produce value, ask:

- "The pattern was invoked but the dynamic didn't happen. Why?"
- "What would have helped the pattern emerge?"
- "Was this the wrong pattern for this situation?"

**Possible learnings:**
1. Trigger conditions too broad (invoked when shouldn't be)
2. Pattern description unclear (didn't know how to embody it)
3. Pattern requires conditions not present (time, trust, etc.)
4. Pattern just doesn't work (delete or major revision)

---

## What We're NOT Testing

**Not testing:**
- Whether pattern produces "correct" outcomes (no objective standard)
- Whether human "complies" with pattern (it's not a rule)
- Scientific proof of value (not achievable)
- Comparison to identical baselines (nothing repeats exactly)

**We ARE testing:**
- Does it trigger when it should?
- Does the pattern actually happen?
- Does propagation work?
- Do humans report value? (subjective but real)

---

## Honest Limitations

This testing cannot:
- Prove patterns "work" in any scientific sense
- Compare to true baselines (contexts never repeat)
- Remove subjectivity from value assessment
- Guarantee quality of propagated patterns

What it CAN do:
- Verify triggering works
- Verify patterns recognizably emerge
- Verify propagation mechanism functions
- Gather signals of value (human reports, behavioral choices)
- Identify failures and degradation

**This is enough.** We're not building a pharmaceutical. We're sharing ways of thinking together. The bar is "seems useful to humans who try it" not "scientifically proven."
