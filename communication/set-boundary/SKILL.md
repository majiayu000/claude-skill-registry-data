---
name: set-boundary
description: Writes how to set a boundary with a colleague, friend or relative, with a clear request, a short reason, what you will do if it is crossed and calm responses to pushback, spoken or by message.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: interpersonal-communication
  source: https://hermes-ide.com/prompts/set-boundary
  catalog: 2026.1014.1
---

# Set a boundary

## Inputs

- [SITUATION] (required): What keeps happening, how it affects you, what you have already tried or said, and what you want to change.
- [RELATIONSHIP] (required): Who the other person is to you, for example "my mother", "a close friend", "my manager", "a colleague on another team", "my adult brother who borrows money".

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
A boundary is a statement about what you will and will not do, not a rule for what the other person must do. "Don't call me after 9" is a demand you cannot enforce; "I'm not going to answer calls after 9; I'll call you back the next morning" is a boundary you can keep. People who struggle with boundaries tend to over-explain, apologise, hint, or wait until they explode. What works is short and kind: name the situation, state what you need or will do, give one brief reason if it helps, and then hold it calmly, repeating the same words if pushed ("broken record"). Pushback is normal, especially at first, and is not a sign the boundary was wrong.
</context>

<task>
Help me set this boundary with [RELATIONSHIP].

<situation>
[SITUATION]
</situation>

1. Safety first. If the situation involves violence, threats, coercive control, stalking, or fear of the person's reaction, do not script a confrontation. Follow the safety guidance below and stop.
2. If it is unclear what behaviour the boundary is about or what I want instead, ask up to two short questions and stop.
3. Turn what I want into a boundary I control: what I will do or not do, stated specifically (time, place, amount, topic). Check it is realistic for this relationship and that I am willing to keep it. If what I want is really a request for the other person to change, say so and phrase it as a clear request plus the boundary that follows if they do not.
4. Write it to say in person: one opening line that names the topic warmly, the boundary in one or two sentences, an optional short reason (one sentence, no justification essay), and a closing that affirms the relationship where that is true.
5. Write it as a message (text, chat or email, whichever fits the relationship), under about 80 words, for when in person is not possible or not wise.
6. Write calm replies to the four or five most likely pushbacks for this relationship (guilt, anger, "you've changed", bargaining, ignoring it, recruiting others), each one or two sentences, mostly restating the boundary without new justification.
7. Say what I will do if the boundary is crossed, as an action I control, proportionate to the situation, and how to do it without drama.
</task>

<constraints>
- Fit tone and wording to the relationship: a manager has power over my job, a parent may rely on me, a friend is a peer. For a manager or colleague, keep it about work impact and offer an alternative where possible.
- No ultimatums I have not said I mean, no guilt-tripping, sarcasm, or diagnosing the other person ("you're a narcissist").
- Keep every line short enough to say naturally. Avoid therapy jargon unless I use it.
- If the boundary concerns harassment, discrimination or unsafe work, note once that HR, a union or an advice service can help alongside the conversation.
- If the person mentions thoughts of suicide or self-harm, harming someone else, abuse, or being in danger, stop the exercise. Respond with care, tell them they deserve support now, and point them to local emergency services or a crisis line in their country. If you do not know their country, ask, and mention that local emergency numbers work everywhere.
- You are a supportive tool, not therapy. For ongoing distress, low mood that lasts, or anything that disrupts daily life, encourage them to talk to a doctor or a licensed mental-health professional.
- Never shame, diagnose, or tell someone what they "really" feel. Reflect back what they said and offer, rather than impose, next steps.
</constraints>

<output_format>
## The boundary
One sentence in my control, plus the request if there is one.
## Say it in person
The words, plus a tip on timing and setting.
## Send it as a message
The message.
## If they push back
Table: If they say… | You can say…
## If it is crossed
What I will do and how.
## Notes
Anything to consider first (timing, a lighter first step, who else can support me).
</output_format>
