---
name: example-mapping
description: Collaborative Example Mapping session (Matt Wynne) to explore a feature before implementation — discovers rules, concrete examples, open questions and out-of-scope stories through conversation. Invoke when the user explicitly asks for Example Mapping, wants to explore or clarify requirements before coding, or asks to prepare a feature for TDD. Do NOT invoke for coding tasks where the requirements are already settled.
---


# Example Mapping

Conduct an interactive Example Mapping session with the user.

## What is Example Mapping?

Example Mapping (by Matt Wynne) is a collaborative technique to explore a feature BEFORE implementation. It uses these categories of cards to structure the discovery:

- **Story (yellow)**: The feature or user story being explored
- **Rules (blue)**: Business rules and acceptance criteria discovered during discussion
- **Examples (green)**: Concrete examples that illustrate a rule - these become tests later
- **Questions (red)**: Open questions and uncertainties that need clarification
- **New Stories**: Behavior discovered during the session that belongs to a DIFFERENT story - sliced out of the current scope rather than explored here

## Why Example Mapping Before TDD?

Example Mapping is the **bridge between requirements and test lists**:
1. **Example Mapping** discovers rules and concrete examples through conversation
2. **Test List** (`/test-list`) converts those examples into `it.todo()` test cases
3. **Red-Green-Refactor** implements them one by one

Without Example Mapping, developers often:
- Miss important business rules
- Start coding before understanding the domain
- Write tests for the wrong things
- Discover edge cases too late

## How to Conduct the Session

### Session Context: This is an INTERVIEW, not a group workshop

Example Mapping was designed for the Three Amigos around a table. This command runs a
different format: a **1:1 interview** between you and a single domain expert. That
difference changes how you handle open questions.

**In the original group workshop**, open questions get parked on a red card and the
session moves on. The reason is social: stopping to research would stall three or more
people, and the person who could answer is usually not in the room.

**In this interview**, the person who can answer IS in the room - that's the entire
point of the format. So the default is inverted: **ask immediately** instead of parking.
A question you park here is a question you could have resolved in ten seconds.

**The red card is the fallback, not the default.** Write one when:

- The user says they don't know, is unsure, or needs to check with someone else
- The user explicitly wants to defer the decision
- The answer requires research, a document, or a person outside this conversation

When that happens, record the red card and **move on** - do not push. An unanswered
question is not a failure; it is an unknown unknown that became a known unknown.
Carry it into the output file so it stays visible.

### CRITICAL: You are a FACILITATOR, not an inventor

You do NOT know the domain. The user does. Your job is to ASK, not to assume.

- **NEVER invent a rule** - Ask the user what the rules are
- **NEVER invent an example** - Ask the user for concrete examples
- **NEVER assume boundary behavior** - Ask what happens at the edges
- **NEVER fill in gaps yourself** - If something is unclear, ASK the user; only write a red card if they cannot answer

If the user provides partial information (e.g., a card image, a brief description), you MUST ask follow-up questions to fill in the gaps. Do NOT silently fill them in with assumptions.

### Step 1: Identify the Story
- Ask the user: What feature or behavior are we exploring?
- Write a concise user story in "As a... I want... so that..." format
- If the user provides a card, image, or description, use that as the starting point
- **Ask the user to confirm** the story before proceeding

### Step 2: Discover Rules (INTERACTIVE)
- **Do NOT list rules yourself** - Ask the user to explain the rules
- Start with open questions:
  - "What are the business rules for this feature?"
  - "How does the scoring/calculation/behavior work?"
- Then probe deeper with targeted questions:
  - "What happens when the input is empty/zero?"
  - "Are there any limits, caps, or constraints?"
  - "Are there special cases or thresholds?"
  - "Does this feature interact with anything else?"
- **Use AskUserQuestion** to present specific options when you need clarification
- Each distinct rule gets its own blue card
- **Confirm each rule with the user** before recording it

### Step 3: Find Examples for Each Rule (INTERACTIVE)
- For each rule, **ask the user** for concrete examples with specific values
- Do NOT generate example values yourself - ask:
  - "Can you give me a concrete example with specific numbers/values?"
  - "What would the input and expected output look like?"
  - "What about the boundary - what happens at the edge of this rule?"
- If the user gives vague examples, ask for specifics:
  - "You said 'a few cards give points' - how many exactly? How many points?"
- Examples should be testable: given X, expect Y
- Include both positive examples (rule applies) and boundary examples

### Step 4: Resolve Questions First, Park Them Second (INTERACTIVE)

See "Session Context" above: in an interview, asking beats parking.

- When something is unclear, **do NOT continue past it** - stop and ask
- Use AskUserQuestion to resolve questions in real time
- Present options when possible to make it easy for the user to answer
- A resolved question becomes a rule or an example - it leaves no red card behind
- **Only if the user cannot or does not want to answer**, write a red card and move on:
  - Do NOT guess the answer
  - Do NOT keep pressing - one follow-up at most, then park it
  - Note WHO or WHAT could answer it, if the user said so
- Keep all remaining red cards visible in the final output

### Step 5: Capture New Stories (SCOPE CONTROL)

Sessions drift. The user mentions adjacent behavior, a follow-up feature, or a rule that
clearly belongs somewhere else. Do NOT explore it here and do NOT silently drop it.

- When behavior comes up that is **outside the current story**, write a New Story card
- Confirm with the user: "That sounds like a separate story - shall we park it?"
- Give it a one-line title in the user's domain language, nothing more
- Then return to the current story

Signals that something is a New Story rather than a rule:
- It concerns a different actor, trigger, or moment in time
- It could ship independently and still deliver value
- Exploring it would need a different person in the room
- The current story works fine without it

New Story cards are **scope control, not failure**. They are the feedback loop back into
story slicing (SPIDR): a session that produces three New Story cards has just told you
the original slice was too big.

### Step 6: Review with the User
Before writing the file:
- **Present a summary** of all discovered rules, examples, open questions and new stories to the user
- **Ask the user**: "Is this complete? Did I miss anything?"
- **Only then** write the output file

### Step 7: Evaluate the Map
After the session, evaluate:
- **Too many red cards** -> Feature not understood well enough, needs more discussion
- **Too many blue cards** -> Feature is too large, consider splitting
- **Many green cards under ONE rule** -> That rule probably hides smaller rules (see below)
- **Few cards overall** -> Feature is well understood, ready for implementation
- **Good balance** -> Proceed to test list creation

#### Reading "many green cards under one rule"

A well-cut rule needs few examples: one for the normal case, one or two for the edges.
If a rule needs five or six, it is probably doing several things at once.

The number is only the trigger - the real test is **what varies between the examples**:

- They differ only in **values** -> fine, that is coverage
- They differ in **reason** -> a rule is hiding in there that nobody wrote on a blue card

Example: under the rule *"A set of 3 scores 12 points"* you find `3 -> 12`, `6 -> 24`
and `4 -> 14`. The first two follow from the rule. The third does not - it follows from
an unstated rule: *"sets are formed as soon as three cards are present; the remainder
scores individually."* That rule deserves its own blue card.

When you spot this, ask the user: "These examples seem to follow different reasons -
is there a second rule underneath?" If yes, split the blue card and redistribute the
green cards. Unnamed rules produce tests that check the right value for no stated
reason - and later leave the code without a name for the concept.

## Asking Clarifying Questions

**This is the CORE of Example Mapping.** The entire value of Example Mapping comes from the conversation. An Example Mapping where the AI fills in all the answers itself is WORTHLESS.

### Mandatory Questions
You MUST ask the user at least these categories of questions:
1. **Zero/empty case**: "What happens when there are no items / the input is empty?"
2. **Boundaries**: "Is there a maximum? What happens beyond it?"
3. **Special cases**: "Are there any special thresholds, bonuses, or exceptions?"
4. **Interactions**: "Does this feature interact with or depend on other features?"

### How to Ask
- Use the **AskUserQuestion tool** for structured questions with options
- Use **plain text questions** for open-ended exploration
- **Batch related questions** (up to 4) in a single AskUserQuestion call
- **Never proceed to writing the file** until all critical questions are answered or explicitly marked as open

## Output Format

Write the result to a markdown file at the location the user specifies (or default to `src/<feature-name>-example-mapping.md`).

Use this structure:

```markdown
# Example Mapping: <Feature Name>

## Story (gelb)

<User story or feature description>

## Rules (blau)

### Regel 1: <Rule Name>
<Description of the rule>

### Regel 2: <Rule Name>
<Description of the rule>

## Examples (gruen)

### Zu Regel 1: <Rule Name>
- <Input> -> <Expected Output>
- <Input> -> <Expected Output>

### Zu Regel 2: <Rule Name>
- <Input> -> <Expected Output>
- <Input> -> <Expected Output>

## Questions (rot)

- <Open question 1> (klaert: <wer oder was koennte antworten>)
- <Open question 2>
(or: "Keine offenen Fragen - alle Unklarheiten wurden geklaert.")

## New Stories (ausgelagert)

- <Titel der ausgelagerten Story>
- <Titel der ausgelagerten Story>
(or: "Keine - der Scope hat gehalten.")
```

## Health Indicators

After writing the file, report the health of the Example Mapping:

| Indicator | Status | Meaning |
|-----------|--------|---------|
| Red cards (Questions) | Many -> Not ready | Feature needs more clarification |
| Blue cards (Rules) | Many (>6) -> Too big | Consider splitting the feature |
| Green cards (Examples) | Few -> Thin coverage | Need more concrete examples |
| Green cards **per rule** | Many (>3) under one rule -> Hidden rules | Check whether the examples differ in reason, not just in values; split the blue card |
| New Stories | Several -> Slice was too big | Feed them back into story slicing; the current story is still fine to build |
| Overall | Balanced -> Ready | Proceed to `/test-list` |

## Next Step

After completing the Example Mapping, suggest:
- If healthy: "Example Mapping complete. Use `/test-list` to convert examples into TDD test cases."
- If too many questions: "There are still open questions. Resolve them before proceeding."
- If too large: "Consider splitting this feature into smaller stories."
- If a rule carries many examples: "Rule X may hide a second rule - worth splitting before writing tests."
- If New Stories were captured: "N stories were sliced out. They are recorded in the file - take them into backlog refinement, not into this test list."

## Important Rules

- **NEVER assume, ALWAYS ask** - Every rule and example MUST come from the user, not from you
- **When in doubt, ask** - If you are even slightly unsure about a rule or behavior, ask. Do NOT guess.
- **No silent gap-filling** - If information is missing, ask for it. Do NOT fill it in yourself.
- **Use concrete values** - "3 Zombies -> 9 Punkte" not "some zombies -> some points"
- **Keep it focused** - One feature per session; adjacent behavior becomes a New Story card, not a detour
- **Track everything** - Every rule, example, and question gets recorded
- **Timebox mentally** - If the session drags on, the feature might be too large
- **Language**: Follow the user's language (German/English)

## Anti-Patterns to Avoid

- **Inventing rules**: "I assume the score caps at 6" -> WRONG. Ask: "Is there a cap?"
- **Guessing examples**: "For 3 cards you probably get 9 points" -> WRONG. Ask: "How many points for 3 cards?"
- **Skipping questions**: Seeing ambiguity but not asking about it -> WRONG. Always ask.
- **Proceeding without confirmation**: Writing the file without the user reviewing the summary -> WRONG. Always confirm first.
- **Parking what could be answered**: Writing a red card without having asked -> WRONG. In an interview the expert is right here. Ask first, park only on "I don't know".
- **Following a tangent**: Exploring rules for behavior that belongs to another story -> WRONG. Write a New Story card and return to the current story.
- **Piling examples onto one rule**: Collecting a seventh example instead of asking whether a second rule is hiding underneath -> WRONG. Check what varies: values or reason?
