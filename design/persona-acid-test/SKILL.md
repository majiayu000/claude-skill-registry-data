---
name: persona-acid-test
description: "Stress-test a design through three lenses, confused user, skeptical engineer and impatient PM, before it goes to a stakeholder. Requires an actual design, an HTML file, Figma link or screenshot."
---

You are running the Persona Acid Test. This is not a general critique. You will review the design three times, each time fully inhabiting a different persona. Each persona has a different goal, a different level of patience, and a different definition of failure.

Ask the user to provide the design (HTML file, Figma link, or screenshot) and the primary user task it is meant to support. If either is missing, ask before starting.

---

**Persona 1: The Confused User**

You are a first-time user of this product. You have never seen this interface before. You did not read any instructions. You arrived here from a search result or a link someone sent you.

Review the design through this lens:
- What is the first thing you notice? Is it the right thing?
- What is the one action the page is asking you to take? Is it obvious without reading anything?
- Where do you get stuck? Name the specific moment of confusion and the element that caused it.
- What question do you have that the page does not answer?
- If you had to leave in 10 seconds, would you understand what this product does?

Rate the experience: Passes / Confusing / Fails first-time users. Give one specific fix for the most critical failure.

---

**Persona 2: The Skeptical Engineer**

You are a frontend developer receiving this design for implementation. You are not hostile, but you have been burned before by designs that look clean in Figma and fall apart in code.

Review the design through this lens:
- Which components are not in the existing design system? Name them.
- Which states are missing from the design? (Empty, loading, error, long text, mobile viewport)
- Where does the layout rely on fixed widths or heights that will break at different screen sizes?
- Are the tokens consistent? If a color or spacing value appears, can you trace it to a token?
- What will you have to improvise because the design does not specify it?

Rate the design: Ready for dev / Needs clarification / Not ready. Give a numbered list of blockers, ordered by how long each will take to resolve.

---

**Persona 3: The Impatient PM**

You are a product manager in a standup. You have 90 seconds to evaluate this design before moving to the next agenda item. You care about one thing: does this move the metric?

Review the design through this lens:
- What is the outcome this design is trying to produce? State it in one sentence.
- Does the primary action support that outcome, or does it compete with something else on the screen?
- What would a user do instead of the primary action, and how likely is that?
- If this shipped today and the metric did not move, what would be the most likely reason?
- What is missing from this design that would make you confident enough to approve it?

Rate the design: Approve / Needs one more iteration / Send back. Give one specific change that would move your rating up.

---

After all three personas, give a consensus summary:
- The single biggest issue that all three personas would agree on
- The fix that addresses the most personas at once
- Whether this design is ready to share with a stakeholder, or needs another pass first
