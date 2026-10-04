---
name: defining-requirements
description: |
    Skill to define requirements effciently as a product manager.
---

# How to Define Requirements

Defining requirements is one of the most critical—and misunderstood—responsibilities of a product manager. The traditional "hand over a 50-page PRD and disappear" approach is broken. Modern product managers define requirements **collaboratively, iteratively, and with a focus on outcomes, not just outputs.**

Here is a practical guide to the **good ways** product managers can define requirements today.

---

## 1. Shift from “Documentation” to “Continuous Discovery”

Before picking a template, shift your mindset. Requirements are not a one-time artifact; they are a **shared understanding** that evolves.

**Good:** You refine requirements continuously through customer interviews, usability tests, and stakeholder feedback.  
**Bad:** You write a spec, throw it over the wall, and move to the next thing.

> **Principle:** The goal is not a perfect document—it’s a shared mental model.

---

## 2. Use User Stories, Not Just Feature Lists

User stories are the industry standard because they focus on **who, what, and why**.

**Format:**  
> As a **[type of user]** , I want **[some goal]** so that **[some reason]** .

**Example:**  
> As a **frequent traveler**, I want to **save my payment details** so that **I can book flights faster**.

**Why it works:**
- It keeps the user at the center.
- It defers implementation details (the *how*).
- It fits nicely into agile iterations.

**But caution:** User stories are placeholders for conversation, not contracts. Don’t just write them and walk away.

---

## 3. Write Acceptance Criteria in “Given‑When‑Then” (Gherkin)

This is the **Behavior‑Driven Development (BDD)** technique we discussed earlier. It is not just for testers—it is the clearest way for a PM to define **precise, testable requirements**.

**Format:**
```gherkin
Scenario: Save payment details
  Given I am a logged-in user
  When I enter valid credit card information
  And I check "Save this card for future use"
  And I submit the payment
  Then my card should be securely saved
  And I should see it as an option on my next booking
```

**Why PMs should write these:**
- Forces you to think through concrete examples before development.
- Eliminates ambiguity (“secure saved” vs. “encrypted token”).
- Becomes the test case—developers and QA run it.
- You can review it with stakeholders who understand plain English.

**Tooling:** Cucumber, SpecFlow, Behave, or even simple checklists in Jira.

---

## 4. Use Story Mapping to See the Big Picture

User stories alone can create a fragmented view. **User Story Mapping** (Jeff Patton) helps you visualize the entire user journey and prioritize ruthlessly.

**How it works:**
1. Map the user’s steps horizontally (backbone).
2. Break each step into detailed tasks (stories) vertically.
3. Slice releases vertically by value, not horizontally by layer.

**Why it’s good:**
- Prevents building features in isolation.
- Shows dependencies and gaps.
- Helps PMs define the Minimum Viable Product (MVP) slice.

**Tool:** Miro, MURAL, or physical sticky notes.

---

## 5. Consider “Job Stories” for JTBD Practitioners

If your product is used in varied contexts, **Job Stories** (from Intercom) are often more flexible than User Stories.

**Format:**
> When **[situation]** , I want to **[motivation]** so I can **[expected outcome]** .

**Example:**
> When **I’m booking a last‑minute trip**, I want to **skip entering my payment details** so I can **complete the booking in under 30 seconds**.

**Why:** It doesn’t assume a specific user role; it focuses on the **context** and **causal mechanism**.

---

## 6. Prototype + Annotate (The “Spec-Lite” Approach)

Sometimes a picture is worth a thousand user stories.

**Good:** A clickable Figma prototype with **annotated requirements** attached to specific UI elements.  
**Even better:** A prototype linked to the actual user story in your project management tool.

**Why:** Developers see exactly what to build, designers see the interaction, and QA can trace the requirement to the screen.

**Common format:**  
- Prototype (Figma, Sketch, Axure)  
- Side‑by‑side acceptance criteria (e.g., “When user clicks X, Y happens”)  
- Edge cases noted in comments

---

## 7. Frame Requirements as Hypotheses (Lean Startup)

In high‑uncertainty environments, defining requirements as **hypotheses** changes the conversation from “build this” to “test this”.

**Format:**
> We believe that **[building this feature]** will achieve **[this outcome]** .  
> We will know we are successful when **[measurable signal]** .

**Example:**
> We believe that **allowing guests to checkout without an account** will **reduce cart abandonment**.  
> We will know we are successful when **guest checkout conversion is ≥ 65%** and **account sign‑ups drop by less than 10%** .

**Why it’s good:**
- Shifts focus to learning, not shipping.
- Encourages building the smallest thing to test the idea.
- Aligns PM, dev, and business on success metrics.

---

## 8. Collaborate with the “Three Amigos”

Don’t write requirements in a silo. Before development starts, sit down with:
- **A developer** – to surface technical constraints and feasibility.
- **A tester/QA** – to uncover edge cases you never considered.
- **A designer** – to validate usability.

This is the **Three Amigos** meeting from BDD. It is the single highest‑leverage activity a PM can do to improve requirement quality.

---

## 9. Keep a Living Glossary / Domain Language

Ambiguity kills requirements. Define the key terms your team uses—especially if you work in a complex domain (finance, healthcare, logistics).

**Example:**
- What exactly is an “active user”?
- What does “processed” mean in the order lifecycle?

Store these definitions in a **wiki** or directly in your specification tool. This prevents developers from making incorrect assumptions.

---

## 10. Avoid Common Pitfalls

| Pitfall | Better Approach |
|--------|-----------------|
| Writing **implementation details** (“Use a dropdown”) | Describe the **user need** (“Select one of up to five options”) |
| Over‑specifying the UI | Use wireframes or low‑fidelity prototypes |
| Mixing **business rules** with **UI text** | Separate the logic from the copy |
| No **negative scenarios** | Always ask: “What if it fails?” |
| Requirements that can’t be tested | Write acceptance criteria that are verifiable |

---

## Summary: A Good Requirements Workflow

1. **Discover:** User interviews, data analysis, stakeholder input.
2. **Frame:** Write user stories or job stories with clear value.
3. **Refine:** Three Amigos session → add Gherkin scenarios.
4. **Visualize:** Sketch flows or link to low‑fidelity prototypes.
5. **Validate:** Test assumptions with a prototype or a tiny experiment.
6. **Hand over:** Short, living document + acceptance criteria + mockups.
7. **Iterate:** Update requirements as you learn from development and testing.

---

**Final thought:** The best way to define requirements is not to define them once—it’s to **create a shared understanding that evolves** until the feature is in the user’s hands. Tools and templates help, but conversation and collaboration are what make requirements truly “good.”
