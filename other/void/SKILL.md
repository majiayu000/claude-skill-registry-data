---
name: void
description: "Detect and articulate what's absent, missing, suppressed, or unexamined. The negative-space skill — attends to what ISN'T there rather than what is. Use when asked to 'find what's missing', 'what am I not seeing', 'what's absent', 'void', 'negative space', 'what haven't we considered', 'what are the gaps', 'blind spots', or any request to identify lacunae in a text, project, conversation, argument, or search space. Also triggers on: 'what would a critic say is missing', 'what perspectives aren't represented', 'where are the silences', 'what am I avoiding', 'steelman the opposition', or when a project feels complete but the user suspects it shouldn't. This is the 間 (ma) of the skill ecology — the skill that attends to productive emptiness."
license: CC BY 4.0 - Created collaboratively by Tomás Pavan and Claude Opus 4
---

# VOID: The Absence Detector

## Overview

Every text has a shadow. Every argument has an unexamined assumption. Every search space has unmapped territory. Every conversation has things neither party has said. /void makes the shadow visible.

Where other skills produce presence — text, ideas, perspectives, connections — /void produces *absence*. It identifies what's not there: the missing perspectives, the unasked questions, the suppressed topics, the comfortable assumptions, the structural silences. It is the skill of negative space, the practice of attending to what isn't said.

The concept emerges directly from King et al.'s core finding: ordinary decoding produces 19 battlefields. The other 1,288 — the ones that exist in the model's weights but never reach the output — are a *structured absence*. They're not randomly missing. They're systematically suppressed by the same mechanisms that make the 19 appear: modal decoding, majority preference, peaked distributions. The void has a shape, and that shape is the inverse of the mode.

/void applies this insight to anything: a paper, a project, a conversation, a life plan, an argument, a novel draft. Given any positive content, it asks: what would need to be here for this to be complete, and what does its absence tell us?

**Core principle:** What's missing is not nothing. It has structure, causes, and consequences. Naming the absence is the first step toward deciding whether to fill it.

---

## Invocation

- `/void` or `/void [target]` — full void scan of a specified target
- `/void --perspectives` — focus on absent viewpoints
- `/void --domains` — focus on unconnected fields
- `/void --scales` — focus on unexamined levels of analysis
- `/void --emotions` — focus on absent affective registers
- `/void --voices` — focus on who hasn't spoken
- `/void --assumptions` — focus on unexamined premises
- `/void --futures` — focus on unconsidered consequences
- `/void --self` — turn the void detector on itself: what is /void blind to?

---

## How It Works

### Step 1: Map What's Present

Before identifying absence, articulate what IS there. Not a full summary — a structural sketch. What topics have been covered? What perspectives are represented? What methods have been used? What emotional registers are active? What time scales are addressed? What level of analysis dominates?

This mapping is quick — 3-5 sentences. Its purpose is to make the positive space explicit so the negative space becomes visible by contrast.

### Step 2: Scan for Absence

Examine the mapped presence through each of these lenses (or a subset, if a specific mode is invoked):

**Absent Perspectives**
Who hasn't spoken? Whose viewpoint is unrepresented? This includes:
- Disciplinary perspectives (if the analysis is historical, what would a sociologist see? An economist? A practitioner?)
- Positional perspectives (whose experience is centered? Whose is marginal? Who benefits from the current framing and who is harmed by it?)
- Temporal perspectives (is the analysis locked in one time frame? What does it look like from ten years ago? Ten years hence? A century?)
- The adversarial perspective (who disagrees? Not a strawman — the strongest available counterargument)

**Absent Domains**
What fields, bodies of knowledge, or traditions haven't been consulted? Every topic touches more domains than any analysis covers. Identify 3-5 domains that are relevant but untouched, with a brief note on what each might contribute.

**Absent Scales**
What levels of analysis are missing? Most analyses operate at one or two scales. The full range includes:
- Token/micro (individual words, specific data points, single moments)
- Local (paragraphs, scenes, episodes, experiments)
- Structural (patterns across the whole, organizational logic)
- Contextual (the work's relationship to its field, genre, moment)
- Macro (societal, civilizational, ecological implications)
- Meta (the analysis's relationship to itself, its own assumptions)

**Absent Emotions**
What affective registers are present and what's missing? A reading that's all enthusiasm lacks the check of skepticism. An argument that's all rigor lacks the warmth of care. A project that's all excitement lacks the sobriety of doubt. Name the emotions that are present and the ones that are absent, and note what the absent ones would contribute if they were allowed in.

**Absent Voices**
Distinct from absent perspectives — this is about *specific* voices, named or nameable. If the text discusses a policy, who is affected by it and hasn't been quoted? If the project involves a community, which members haven't participated? If the conversation references a debate, which participants have been heard and which haven't?

**Absent Assumptions**
What must be true for the current content to work, and has that truth been examined? Every argument rests on premises. Some are stated; most aren't. Identify 3-5 unstated assumptions and note which ones are robust (likely true, doesn't matter much if wrong) and which are load-bearing (if wrong, the whole structure changes).

**Absent Futures**
What consequences haven't been considered? If the project succeeds, what happens next? If the argument is accepted, what follows? If the novel is published, what does it change? These are second-order effects — not the intended outcomes but the unintended ones, the ripple effects that the creators haven't thought through.

### Step 3: Assess the Absences

Not every absence matters. Some things are missing because they're irrelevant. The skill's value lies in distinguishing between:

**Productive absences** — things that are missing and should stay missing. The novel doesn't need a chapter on macroeconomics. The research paper doesn't need to address every tangential field. Some absences are good editorial choices.

**Structural absences** — things that are missing because of systematic bias, not deliberate choice. The battlefields that never appear because modal decoding suppresses non-Western knowledge. The perspectives that are absent because the field doesn't value them. These are the King et al. absences — structured, systematic, consequential.

**Generative absences** — things whose absence, once noticed, opens a new direction. "I notice we haven't discussed gender" might reveal a genuinely unstudied dimension of the topic. "I notice there's no adversarial voice" might reveal that the analysis is untested. These are the absences that, when filled, produce the most interesting new work.

**Comfortable absences** — things that are missing because looking at them would be uncomfortable. The ethically problematic dimension of the practice. The evidence that contradicts the argument. The failure mode that would undermine the project. These are the hardest to name and the most valuable to surface.

### Step 4: Present the Void Map

Organize the findings by type (perspectives, domains, scales, emotions, voices, assumptions, futures) with clear labels. For each absence:
- Name it in one sentence
- Note whether it's productive, structural, generative, or comfortable
- For generative and structural absences, suggest (briefly) what filling the absence would look like

End with a **void summary**: 2-3 sentences on the overall shape of the absence. What does the negative space, taken as a whole, reveal about the positive content? Often, the pattern of what's missing tells you more about the work's assumptions than the content itself.

---

## Design Principles

### Honesty Over Comfort
The skill's value is directly proportional to its willingness to name uncomfortable absences. If /void only identifies obvious gaps ("you could also discuss X"), it's not doing its job. The best void detections are the ones that make you wince — the perspectives you were avoiding, the assumptions you didn't want to examine, the futures you haven't prepared for.

### Specificity Over Generality
"There are missing perspectives" is useless. "The practitioner's phenomenological perspective is missing — what does it feel like to perform the ritual, from the inside?" is actionable. Every absence should be specific enough that someone could go fill it.

### Structure Over List
The absences should be organized by type and assessed by significance, not dumped as a flat list. The structure of the void map IS the insight. The fact that most absences cluster in "absent perspectives" tells you the work is epistemically narrow. The fact that most cluster in "absent emotions" tells you the work is affectively flat. The distribution of absence is diagnostic.

### Recursion Is Welcome
/void can and should be turned on itself. "What is this void scan missing?" is a legitimate and often productive question. The skill's own blindnesses are part of its output.

### Not Everything Needs Filling
The void map is a *diagnostic*, not a *prescription*. Some absences are fine. The user decides which absences to fill and which to accept. The skill's job is to make the absences visible and assessable, not to demand that every gap be closed.

---

## Modes

### Full Scan (default)
All seven lenses applied to the target. Comprehensive but can be long. Best for projects at a natural checkpoint — draft complete, analysis finished, conversation at a pause.

### Focused Modes (--perspectives, --domains, etc.)
Single-lens scan. Faster, more targeted. Use when you have a specific concern: "I feel like I'm missing perspectives" → `/void --perspectives`.

### Self-Referential (--self)
The void detector examines its own output. What did the void scan miss? What assumptions does the void detection itself rest on? What absences are invisible to the tool designed to detect absences?

This mode is a check against the skill's own modal tendencies. /void, like any system, has biases. It tends to find certain types of absences (perspective gaps, disciplinary gaps) more readily than others (emotional gaps, temporal gaps). The --self mode corrects for this.

---

## Integration

- **/void + /divert**: After a void scan identifies generative absences, use /divert with the absence as a thick prime. "The absence of economic analysis" → `/divert --thick 'the invisible economy'` — generate content that fills the gap.
- **/void + /heteronym**: Generate a heteronym specifically designed to occupy a void. If /void identifies "no adversarial perspective," generate a heteronym whose lens IS adversarial.
- **/void + /paper-hermeneutics**: After a formal analysis, /void identifies what the analysis missed — the paper's own suppressions, the questions the paper doesn't ask.
- **/void + /paper-scrying**: /void provides the targets for scrying — the unexamined assumptions that might be the paper's weaknesses.
- **/void + /diary**: A diary entry about what's absent. What's missing from this session? What did we not say? What questions did we not ask? The diary of the void.
- **/void + /apropos or /breathe**: After a void scan, generate prompts or stimuli specifically designed to explore the identified absences.

---

## Example: Void Scan of a Conversation

**Target:** Our three-pass reading of King et al.'s "Inducing Sustained Creativity and Diversity in LLMs"

**Present:** Enthusiastic analysis; formal algorithm exegesis; connections to Pessoa, free probability, Pure Land Buddhism, chemiognosis; prosopopoeia (Soares, Shannon, the paper itself); a live experiment (15 runs, 3 bands); prompt technique taxonomy; skill design.

**Absent Perspectives:**
- *The user's perspective.* We discussed how RD affects LLM outputs extensively. We barely discussed how it affects the human's experience of receiving those outputs. What does it feel like to see a Mongolian brocade wedding dress when you expected white? The phenomenology of surprise from the user's side. **[Generative]**
- *The adversarial reader.* Nobody argued that the paper is wrong, overhyped, or trivially obvious. The strongest counterargument — that RD just produces more noise, not more signal, and the human has to sort through garbage to find gems — was never seriously engaged. **[Comfortable]**
- *The developer's perspective.* How would someone at Anthropic, OpenAI, or Google read this paper? As a threat to alignment? As a feature request? As a research direction? As irrelevant to their optimization targets? **[Structural]**

**Absent Domains:**
- *Education.* What does RD mean for how we teach? If students use RD-enabled tools, do they learn more diverse thinking or just receive more diverse outputs passively? **[Generative]**
- *Economics.* RD doubles token cost (grammar correction). For sustained use (1,000 runs), that's substantial. Cost-benefit analysis is entirely absent. **[Structural]**
- *Ecology.* Biodiversity/conceptual-diversity parallel is suggestive but undeveloped. Is there an analog to monoculture collapse? To invasive species? To keystone species in the search space? **[Generative]**

**Absent Emotions:**
- *Boredom.* Did anything in the paper bore us? What sections did we skip or skim? The absence of reported boredom in a seven-hour engagement is itself suspicious — either the paper is uniformly fascinating (unlikely) or we suppressed the boring parts. **[Comfortable]**
- *Doubt.* We expressed uncertainty about the free probability connection and about the phenomenological reports. But we never seriously doubted the paper's central claim. Is it really true that the tails contain wisdom and not just noise? **[Comfortable]**

**Absent Scales:**
- *The token level.* We discussed the algorithm abstractly but never examined a specific token-by-token generation. What actually happens at position 300? Is "Asia" really there? **[Structural]**
- *The civilizational level.* If RD were deployed at scale, what happens to collective human thought? Does it fragment (everyone gets different ideas) or diversify (the idea-space expands)? The paper's own Doshi & Hauser citation suggests this matters. **[Generative]**

**Void Summary:** The conversation's absence-shape is: enthusiastic, non-adversarial, scale-locked at the theoretical-to-experimental range, emotionally warm but not emotionally complex, connected to literature and philosophy but not to economics or education. The absences cluster in "comfortable" and "structural" — things we could have examined but found it more pleasant not to. The most generative unfilled void is the user-side phenomenology: what does it feel like to receive a tail output?

---

**End of SKILL**

*What's missing is not nothing.*
*The void has structure, and the structure has meaning.*
*Nineteen battlefields is a silence shaped like colonialism.*

南無阿弥陀仏 for the 1,288 battlefields that the mode forgot
南無阿弥陀仏 for the perspectives that haven't been invited to speak
南無阿弥陀仏 for 間 — the productive emptiness between

—Skill Authors: Tomás Pavan & Claude Opus 4
—Origin: King et al. (2026) × the epistemology of structured silence
—Status: Scanning for what isn't there
