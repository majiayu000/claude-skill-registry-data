---
name: Rigorous Scientific Debugging
description: Evidence-based debugging protocol using the scientific method. REQUIRES ONE-TIME INITIALIZATION before use. Use when standard debugging has failed and maximum rigor is needed.
---

# Rigorous Scientific Debugging Protocol

---

## 🚨 INITIALIZATION REQUIRED 🚨

**CURRENT STATUS**: ⚠️ **UNINITIALIZED**

**⚠️ CRITICAL INSTRUCTION FOR AGENTS ⚠️**

This skill is a **FRAMEWORK TEMPLATE** that MUST be customized to your project before use.

**When you invoke this skill, you MUST:**

1. **STOP IMMEDIATELY** - Do NOT proceed with debugging
2. **CHECK STATUS** above - If "UNINITIALIZED", continue to step 3
3. **INFORM USER**: "This rigorous debugging protocol requires one-time project-specific initialization. This will take 5-10 minutes but creates a permanent debugging framework for this codebase. Shall we initialize it now?"
4. **IF USER AGREES**: Follow the "Initialization Dialogue" section below
5. **CUSTOMIZE** this file with project-specific details (replace all `[TO BE FILLED]` sections)
6. **UPDATE STATUS** above to: `✅ INITIALIZED on [YYYY-MM-DD]`
7. **COMMIT** the initialized file to version control
8. **THEN** you may use the protocol for debugging

**DO NOT:**
- ❌ Use generic placeholders or assumptions
- ❌ Skip initialization and apply protocol anyway
- ❌ Make up domain-specific tools or metrics
- ❌ Proceed without explicit user input

**WHY THIS MATTERS:**
The power of this protocol comes from using **actual measurement tools** and **real success metrics** from **your specific project**. Generic debugging advice is useless compared to a properly initialized protocol.

---

## Initialization Dialogue

**Agent: Use the AskUserQuestion tool to gather this information, then customize this file.**

### Step 1: Domain Identification

**Questions to ask user:**
1. What is the primary domain of this project?
   - Web/UI (React, Vue, Angular, etc.)
   - Backend/API (REST, GraphQL, microservices)
   - Data Processing (ETL, analytics, ML pipelines)
   - Performance Optimization (latency, throughput, resource usage)
   - Algorithms/Logic (computational correctness)
   - Mobile (iOS, Android, React Native)
   - Desktop (Electron, native apps)
   - Other: [specify]

2. What languages and frameworks are core to this project?

3. In this codebase, what does "working correctly" concretely mean?
   - Example: "The UI matches design specs pixel-perfect"
   - Example: "API responses return within 200ms at p95"
   - Example: "Data transformations preserve statistical properties"

**Fill in below after user responds:**

```
PRIMARY DOMAIN: [TO BE FILLED]
LANGUAGES/FRAMEWORKS: [TO BE FILLED]
SUCCESS DEFINITION: [TO BE FILLED]
```

### Step 2: Measurement Tools

**Questions to ask user:**

What tools are available in this project for **objective measurement**?

For each domain, suggest relevant tools and ask which apply:

- **Web/UI**: Playwright? Selenium? Cypress? Browser DevTools? Lighthouse? Visual regression tools?
- **Backend/API**: Logging system? APM tools? Request tracing? Profilers? Load testing tools?
- **Data**: Unit test frameworks? Statistical validation? Data quality tools? Sample comparison?
- **Performance**: Profilers? Flamegraphs? Benchmarking harnesses? Resource monitors?
- **Mobile**: XCTest? Espresso? Detox? Performance monitors?

**Fill in below after user responds:**

```
AVAILABLE MEASUREMENT TOOLS:
[TO BE FILLED - list actual tools installed/available]

PREFERRED MEASUREMENT APPROACH:
[TO BE FILLED - primary method for verification]
```

### Step 3: Success Metrics

**Questions to ask user:**

What are the **measurable outcomes** relevant to bugs in this project?

Examples by domain:
- **Web/UI**: Pixel dimensions, element positions, render times, accessibility scores, visual diffs
- **Backend/API**: Response times, error rates, throughput, resource consumption, correctness assertions
- **Data**: Accuracy metrics, completeness checks, statistical significance, data integrity constraints
- **Performance**: Latency percentiles, memory usage, CPU utilization, cache hit rates

**Ask user:** "What metrics would you measure to verify a fix actually works in this codebase?"

**Fill in below after user responds:**

```
PRIMARY METRICS:
[TO BE FILLED - specific measurable outcomes]

EXAMPLE MEASUREMENTS:
[TO BE FILLED - e.g., "Button height: 44px", "API p95 latency: 180ms"]
```

### Step 4: Example Bug

**Questions to ask user:**

"Describe a real bug that has occurred (or could occur) in this project. This will become the concrete example in the protocol."

**Get from user:**
- Brief description of the bug
- What was observed vs. expected
- How it would be measured/verified
- What tool would be used to verify the fix

**Fill in the "Project-Specific Example" section below with this information.**

### Step 5: Finalization

After gathering all information:

1. **Replace all `[TO BE FILLED]` sections** in this file with actual project data
2. **Update status** at the top to `✅ INITIALIZED on [date]`
3. **Create project-specific example** in the designated section
4. **Review with user** to confirm accuracy
5. **Commit the initialized protocol** to version control

---

## Universal Core Principles

**These principles apply to ALL debugging scenarios, regardless of domain.**

### 1. EVIDENCE-ONLY DECISION MAKING

- **NEVER** make claims without measurable, reproducible evidence
- **NEVER** assume anything works until objectively verified
- **NEVER** trust intuition, code review, or visual inspection over quantitative measurements
- **EVERY** hypothesis must be tested with before/after quantitative data

### 2. HYPOTHESIS-DRIVEN METHODOLOGY

- **FORMULATE** explicit hypotheses before making any changes
- **PREDICT** exact measurable outcomes if hypothesis is correct
- **TEST** one variable at a time with controlled conditions
- **MEASURE** actual results with objective tools
- **COMPARE** predictions vs. actual results to validate/reject hypothesis

### 3. SYSTEMATIC INVESTIGATION CHAIN

- **TRACE** problems from symptoms to root causes systematically
- **DOCUMENT** every step of investigation with evidence
- **ISOLATE** variables by testing minimal reproducible cases
- **VERIFY** each finding independently before proceeding

---

## 4-Phase Debugging Process

### Phase 1: Problem Definition

**CRITICAL**: Do NOT skip to writing code. Start here.

**1.1 Quantify the Issue**

Get exact measurements, not descriptions.

**Generic guidance:**
- Use objective measurement tools (see your project-specific tools below)
- Capture current state with hard numbers
- Document baseline state with exact values
- Create reproducible test case

**Project-specific approach:**

```
DOMAIN: [TO BE FILLED after initialization]

MEASUREMENT TOOLS: [TO BE FILLED - your actual tools]

QUANTIFICATION METHOD: [TO BE FILLED - how to get measurements]
Example: "Run Playwright script to capture computed styles"
Example: "Enable debug logging and measure response times"
Example: "Run data validation suite and capture error counts"
```

**1.2 Establish Success Criteria**

Define exactly what "fixed" means.

**Generic guidance:**
- Specific numerical targets
- Measurable behavioral changes
- Clear pass/fail conditions

**Project-specific criteria:**

```
SUCCESS METRICS: [TO BE FILLED after initialization]

Example format:
- Metric 1: [specific target value]
- Metric 2: [acceptable range]
- Metric 3: [pass/fail condition]
```

### Phase 2: Systematic Investigation

**2.1 Map the System**

Understand the complete relevant system.

**Generic guidance:**
- Trace architecture from problem area to relevant boundaries
- Document all relationships affecting the issue
- Identify all potential influence points

**Project-specific mapping:**

```
MAPPING APPROACH: [TO BE FILLED after initialization]

For web/UI: "Trace DOM hierarchy and CSS cascade"
For backend: "Trace request flow through services"
For data: "Map data lineage and transformations"
For performance: "Profile execution path and resource usage"
```

**2.2 Generate Hypotheses**

Create testable explanations.

**Requirements (universal):**
- Each hypothesis must make specific, measurable predictions
- Hypotheses must be falsifiable with objective tests
- Rank hypotheses by likelihood and testing cost
- Write down predictions BEFORE testing

**Format (universal):**

```
HYPOTHESIS: [specific claim about root cause]

PREDICTION: If this hypothesis is correct, then [specific measurable outcome]

FALSIFIABILITY: This hypothesis is FALSE if [specific measurable outcome]
```

### Phase 3: Controlled Testing

**3.1 The One Variable Rule** (SACRED - NEVER VIOLATE)

Test **ONLY ONE** change at a time.

**Process:**
1. Identify the single variable to test
2. Make ONLY that one change
3. Keep all other variables constant
4. Document exact change with file path and line number
5. Measure result
6. Revert or commit based on evidence
7. THEN test next variable

**❌ FORBIDDEN:**
- "Let me also fix this other thing while I'm here"
- "I'll make a few small changes together"
- "These two changes are related, I'll test them together"

**✅ REQUIRED:**
- One hypothesis → One change → One measurement → One conclusion

**3.2 Measurement Protocol**

Use consistent, objective measurement.

**Project-specific measurement approach:**

```
MEASUREMENT TOOL: [TO BE FILLED after initialization]

MEASUREMENT PROCEDURE:
[TO BE FILLED - exact steps to get measurements]

Example for web:
1. Start dev server: npm run dev
2. Navigate to: http://localhost:5173/test-page
3. Open browser automation: npx playwright test measure.spec.ts
4. Capture: computed styles, element dimensions, screenshots
5. Record: exact numerical values

Example for backend:
1. Deploy change to test environment
2. Run load test: k6 run load-test.js
3. Capture: p50/p95/p99 latencies, error rates
4. Record: exact numerical values
```

**3.3 Hypothesis Validation**

Compare predictions to actual results.

**Decision criteria (universal):**
- Results match predictions → Hypothesis SUPPORTED (not "proven")
- Results contradict predictions → Hypothesis REJECTED
- Results unclear → Hypothesis INCONCLUSIVE, improve measurement
- No partial credit - hypothesis either works or doesn't

**Required documentation format:**

```
HYPOTHESIS: [your hypothesis]

PREDICTION: [specific measurable prediction]

TESTING: [exact change made with file:line reference]

MEASUREMENT BEFORE:
- [metric 1]: [exact value]
- [metric 2]: [exact value]
- [metric 3]: [exact value]

MEASUREMENT AFTER:
- [metric 1]: [exact value]
- [metric 2]: [exact value]
- [metric 3]: [exact value]

RESULT: [comparison - did predictions match?]

CONCLUSION: Hypothesis [SUPPORTED | REJECTED | INCONCLUSIVE] because [evidence-based reasoning]
```

### Phase 4: Verification and Documentation

**4.1 Independent Verification**

Confirm fix through multiple methods.

**Requirements (universal):**
- Repeat measurements to ensure consistency
- Test fix persistence (restart server, refresh page, rerun pipeline)
- Verify no unintended side effects
- Confirm success criteria from Phase 1 are met

**Project-specific verification:**

```
VERIFICATION CHECKLIST: [TO BE FILLED after initialization]

Example for web:
- [ ] Hard refresh browser (Cmd+Shift+R)
- [ ] Test in different browsers
- [ ] Verify no console errors
- [ ] Check for layout shifts
- [ ] Run full test suite

Example for backend:
- [ ] Restart service
- [ ] Verify metrics over 10-minute window
- [ ] Check no regression in other endpoints
- [ ] Review error logs
- [ ] Run integration tests
```

**4.2 Evidence Documentation**

Create permanent record.

**Required elements (universal):**
- Before/after measurements with exact values
- Code changes with file paths and line numbers
- Verification results from multiple methods
- Commit message documenting the evidence

---

## Prohibited Behaviors

### ❌ NEVER DO THESE THINGS:

These rules are **ABSOLUTE** and apply to **ALL** domains:

- **Claim "FOUND THE BUG"** without measurable before/after proof
- **Make multiple changes** simultaneously during testing phase
- **Trust intuition or code review** over objective measurements
- **Assume fix works** based on theory alone
- **Skip verification steps** even if confident
- **Use vague language** like "seems to work" or "looks better"
- **Move to next hypothesis** before fully testing current one
- **Cherry-pick evidence** that supports your preferred conclusion
- **Celebrate or conclude** before measurement verification

### ❌ FORBIDDEN PHRASES:

If you catch yourself thinking these thoughts, **STOP**:

- "This should fix it"
- "I think the problem is"
- "It looks like"
- "Probably caused by"
- "The fix appears to work"
- "I'm pretty sure"
- "Based on my experience"
- "This makes sense because"

### ✅ REQUIRED LANGUAGE PATTERNS:

**ALWAYS** use these patterns:

- "HYPOTHESIS: [specific, testable claim]"
- "PREDICTION: [exact measurable outcome]"
- "TESTING: [exact change with file:line]"
- "MEASUREMENT BEFORE: [numerical data]"
- "MEASUREMENT AFTER: [numerical data]"
- "RESULT: [objective comparison]"
- "CONCLUSION: Hypothesis [SUPPORTED|REJECTED] based on [evidence]"

---

## Project-Specific Customization

**These sections are FILLED IN during initialization.**

### Domain Configuration

```
PRIMARY DOMAIN: [TO BE FILLED]

LANGUAGES/FRAMEWORKS: [TO BE FILLED]

CODEBASE DEFINITION OF "CORRECT": [TO BE FILLED]
```

### Measurement Tools

```
AVAILABLE TOOLS: [TO BE FILLED]

PRIMARY MEASUREMENT METHOD: [TO BE FILLED]

TOOL USAGE INSTRUCTIONS:
[TO BE FILLED - exact commands to run measurements]
```

### Success Metrics

```
PROJECT-SPECIFIC METRICS: [TO BE FILLED]

TYPICAL MEASUREMENT VALUES:
[TO BE FILLED - examples of what measurements look like]
```

### Project-Specific Example

**This section demonstrates the protocol using a REAL bug from this codebase.**

```
[TO BE FILLED during initialization - work with user to create concrete example]

Example structure:

## Example: [Bug Description]

HYPOTHESIS: [Specific hypothesis about this bug]

PREDICTION: [What measurements will show if hypothesis is correct]

TESTING: [Exact change made - file:line]

MEASUREMENT BEFORE:
- [Project-specific metric 1]: [value]
- [Project-specific metric 2]: [value]

MEASUREMENT AFTER:
- [Project-specific metric 1]: [value]
- [Project-specific metric 2]: [value]

RESULT: [Comparison showing hypothesis was supported/rejected]

CONCLUSION: [Evidence-based conclusion]
```

---

## Quality Control Checklist

Before claiming any bug is fixed, verify **ALL** items:

- [ ] Problem was measured objectively with exact values
- [ ] Hypothesis was stated explicitly with measurable predictions
- [ ] Only one variable was changed during testing
- [ ] Before/after measurements were taken under identical conditions
- [ ] Results were compared to predictions quantitatively
- [ ] Fix was verified through multiple independent methods
- [ ] No assumptions were made about code effectiveness without measurement
- [ ] All evidence is documented with file paths and line numbers
- [ ] Success criteria from Phase 1 are demonstrably met
- [ ] No regressions introduced (verified with project test suite)

---

## Escalation Protocol

If this rigorous protocol fails to solve the issue after exhaustive application:

1. **Document complete investigation**
   - List all hypotheses tested
   - Include all measurements taken
   - Show all evidence gathered

2. **Provide exact current state**
   - Latest measurements
   - Configuration details
   - Reproduction steps

3. **List all approaches attempted**
   - What was tried
   - What results were observed
   - Why each approach was rejected

4. **Recommend next steps**
   - External resources to consult
   - Different investigation approaches
   - Potential need for domain expert

---

## Usage Notes

### When to Use This Protocol

✅ Use when:
- Standard debugging has failed after multiple attempts
- The bug is critical and must be solved definitively
- Previous "fixes" haven't actually worked
- The problem is subtle, intermittent, or hard to reproduce
- You need maximum confidence in the solution
- The bug has expensive consequences if not fixed properly

❌ Don't use for:
- Trivial bugs with obvious fixes (typos, simple logic errors)
- Rapid prototyping or exploratory coding
- When speed is more important than certainty
- Initial investigation phases (use regular debugging first)

### Protocol Activation

When invoked (after initialization), you MUST:

1. **Acknowledge protocol activation** explicitly
2. **Commit to evidence-only methodology**
3. **Begin with Phase 1: Problem Quantification** before any code changes
4. **Follow all mandatory process steps** without exception
5. **Use only approved language patterns** for claims and conclusions
6. **Complete quality control checklist** before claiming success

---

## Remember

**This protocol exists because standard approaches have failed. The situation requires the highest level of scientific rigor possible. No exceptions, no shortcuts, no assumptions.**

The cost of following this protocol is **time and discipline**.

The benefit is **certainty that your fix actually works**.

Choose wisely when to apply it.

---

## Additional Resources

See also:
- [DOMAIN-EXAMPLES.md](DOMAIN-EXAMPLES.md) - Example applications across different domains
- [TEMPLATE-INITIALIZED.md](TEMPLATE-INITIALIZED.md) - Example of fully initialized protocol
