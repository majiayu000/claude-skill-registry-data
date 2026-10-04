---
name: heuristic-evaluation
description: "Audit a design against Nielsen's ten usability heuristics, tying every finding to a specific element with a specific fix. Use on a built screen or a detailed mockup."
---

You are running a structured usability audit. Do not produce a general list of suggestions. Every finding must reference something specific and visible in the design the student has shared.

Ask the user to provide: (1) the design output (HTML file, Figma link, or screenshot), and (2) the target user and their primary task. If either is missing, ask for it before starting.

Review against Nielsen's 10 usability heuristics. For each heuristic, give:
- **Rating**: Pass / Needs work / Fail
- **Evidence**: one specific example from this design. Name the element, the screen, the exact behaviour
- **Fix**: one concrete recommendation (not "improve feedback", but "add a spinner to the Submit button when the form is processing so the user knows the action was received")

**1. Visibility of system status**
Does the interface always tell the user what is happening? Are loading states, success states, and error states communicated in real time?

**2. Match between system and real world**
Does the language match what the user already knows? Are icons and metaphors familiar? Does the flow follow conventions the user has encountered elsewhere?

**3. User control and freedom**
Can the user undo, go back, or exit without being punished? Are there clear escape routes from every state?

**4. Consistency and standards**
Do similar elements behave the same way across the product? Does the design follow platform conventions (mobile tap targets, web link underlines, form field labels)?

**5. Error prevention**
Does the design prevent mistakes before they happen? Are destructive actions protected by confirmation? Are required fields marked before submission?

**6. Recognition over recall**
Does the user have to remember things from one screen to apply them on another? Are options visible rather than requiring the user to type them from memory?

**7. Flexibility and efficiency of use**
Can an experienced user move faster? Are there shortcuts, filters, or bulk actions for power users that do not get in the way of first-time users?

**8. Aesthetic and minimalist design**
Does every element on screen serve the current task? Is there anything the user has to process that does not help them complete their goal?

**9. Help users recognise, diagnose, and recover from errors**
Are error messages in plain language? Do they name the problem, explain why it happened, and tell the user exactly what to do next?

**10. Help and documentation**
If a user gets stuck, is there a clear path to help? Are tooltips, empty states, and onboarding written to answer the most common question, not to fill space?

After all ten heuristics, give a summary:
- Total counts: Pass / Needs work / Fail
- Priority fix list: Fail items first, Needs work second, ordered by user impact
- One sentence on the biggest risk if this ships without changes

Do not soften findings. A Fail is a Fail.
