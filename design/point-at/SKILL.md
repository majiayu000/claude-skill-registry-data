---
name: point-at
description: "Use when about to ask the person a question, answer one of theirs, or explain something to them, about a screen, a region or a component of the interface: in an interview, a plan, a board, a review or plain chat. Also when the person says they do not see what is meant on a screen. Finds the screen's prototype and points the person's viewer at the components concerned, so the question or the answer is given in the prototype's own names with the thing lit in front of them. Not for designing or changing a prototype (design-prototype), and not for a question with no screen in it."
---

# Point at it

**A screen is talked about with the screen in front of the person, in the prototype's own names**, whether the agent is asking or answering.

1. **Find the prototype before writing the question**, through the `aiview` skill: `list --kind prototype --tag <project>`, or the one the person named. Read the prototype that draws the screen, the screen's own file and never the library it pulls from, and run `components` on it. Its `page` and `variants` lines are the vocabulary: every name the person can be shown on that page.
2. **What the prototype already answers is stated and confirmed, not asked.** Point at it all the same.
3. **Write the question in those names only.** A region with no name of its own is placed by the named component it sits in. Where the code differs from the prototype, say both: the prototype's name, then the code's `file:line`. A comparison with another screen points at the screen the decision changes, and names the other by its prototype and component.
4. **Point, then ask**: one `show <prototype>` with `--component <Name>` once per component, and `--variant` when they exist only in one. Three components at most, the ones the question is about. A name the command refuses is not on that page: go back to 1, never rephrase around it. `show` writes each name on the component it outlines, so the question uses the same names, and carries the link the command prints.
5. **One pointer per question**: each `show` replaces the last. Questions about different regions are asked one at a time, the one the others depend on first.
6. **When the answer is in, `show --done`**: the person's tab goes back to what they were reading before the first pointer. Between two questions in a row there is no `--done`: it closes the run.
7. **No prototype draws it**: say so in the question and cite the screen's `file:line`. A layout that exists nowhere goes to the `design-prototype` skill first, never described in prose for the person to choose in.

**An answer follows the same steps**: the person asks where something is, what a name means or how two regions relate, and the reply points at it before it explains, with the link in the reply, and `show --done` once they have it. "Which one is that?" is answered by a `show`, never by a longer description.

`tabs: 0` in the command's answer means no viewer is open: the link in the question is how the person gets there.
