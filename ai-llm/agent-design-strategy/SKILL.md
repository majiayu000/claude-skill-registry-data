---
name: agent-design-strategy
kind: skill
status: ready
provenance:
  principles: [P009, P027, P033, P034, P060]
---

# Agent Design Strategy

## Purpose

This skill selects and reviews the higher-level strategy behind an LLM-based agent's build — the architectural backbone, how the agent acquires new capability, how it is given a profile or persona, how it revises its plans on feedback, and, when fine-tuning is in scope, where its training data comes from. Each recommendation names the alternatives that were weighed, the trade-off accepted by choosing this option over those alternatives, and the residual limit that remains, rather than presenting any one option as free of cost.

## When this applies

- A new agent's architectural backbone — rule-based, reinforcement-learned, symbolic, or a language-model core with added mechanisms — is not yet fixed, especially when the agent must act across many varied, unscripted situations.
- The caller wants new capability without committing to fine-tuning, or wants to know which non-fine-tuning mechanism fits a specific capability gap.
- The agent needs a role, persona, or profile — for simulation, role-play, or a population of agents — and the generation strategy is not yet chosen.
- The agent plans and needs a way to revise a plan after a setback, and the feedback channel(s) to wire in are not yet decided.
- Fine-tuning is already in scope and the training-data source still needs to be chosen.
- These decisions are not gated to a narrow task type — raise every axis above that applies to the caller's agent, even if only one was asked about.

## Procedure

1. Establish the behavioral breadth the agent must cover: a narrow, well-specified task, or many novel, open-ended situations that cannot be fully scripted in advance.
2. If the breadth is open-world, compare the candidate backbones on that breadth requirement specifically, not on raw capability (P009); if the breadth is narrow and well-specified instead, this trade-off does not dictate the backbone choice — note that explicitly and move to step 3.
   - Rule out hand-authored rule systems (finite-state machines, behavior trees): they can only execute procedures a person hard-coded in advance.
   - Rule out reward-driven reinforcement learning unless the task has a cleanly definable reward; it has reached very strong performance in adversarial games with such rewards, but that has not been shown to produce believable open-world behavior.
   - Rule out classic symbolic cognitive architectures that pair short- and long-term memory with perceive-plan-act cycles: their procedural knowledge is manually crafted and gives the agent no route to genuinely new behavior.
   - Favor a language-model core, because it already encodes a wide range of human behavior from training and can be prompted with a narrow context to produce believable output — but recommend it together with explicit memory, reflection, and planning mechanisms, not as a bare prompt, and flag that long-horizon coherence remains an open weakness even in the most capable current models.
3. Decide whether fine-tuning is available, affordable, or already settled for this build; if not, or as a first step regardless, plan capability acquisition through prompt and mechanism engineering (P027):
   - Prompt engineering: describe the desired capability in natural language inside the prompt, for example with worked examples of the reasoning the agent should perform.
   - Trial-and-error / critic loop: let the agent act, have a defined critic judge the action, and feed an unsatisfactory judgment back in to refine the next action.
   - Multi-agent debate or crowd-sourcing: have several agents answer independently and iterate on each other's answers when they disagree, until they converge.
   - Experience accumulation / skill library: store the actions or skills that succeeded on past tasks and retrieve the relevant ones when a similar task recurs, so the gain comes from the memory design rather than a parameter update.
   - Self-driven evolution: let the agent set its own goals and improve through self-directed learning and feedback, such as a reward signal, rather than direct instruction.
   - All four work with either open- or closed-source models, but every one is bounded by the model's limited context window and by a very large design space that makes an optimal prompt or mechanism hard to identify by inspection alone — budget review time for that search, not only for implementation.
4. If the agent needs a role, persona, or profile — a simulated population, role-play, or any setting where consistent character matters — choose the profile-generation strategy by its trade-off, and combine strategies rather than assuming one is always best (P033):
   - Handcrafting is fully flexible (any attribute can be assigned deliberately) but labor-intensive, and the labor cost becomes prohibitive once the population is large.
   - LLM-generation sharply cuts the time and effort of profiling a large population but offers less precise control, and can drift into inconsistencies or deviations from the intended character.
   - Dataset alignment derives profiles from real-world data and so captures real population attributes accurately, making the resulting behavior more realistic and meaningful.
   - Combining strategies — for example, dataset-aligned profiles for roles that already exist in data plus handcrafted profiles for roles that do not — can add value over any single strategy, but this combination benefit rests on lighter evidence than the three base strategies, so treat it as an option worth testing rather than a proven default.
5. If the agent plans and must revise a plan after a setback, wire in feedback from more than one source and combine them rather than relying on a single channel (P034):
   - Environment feedback — completion signals, post-action observations, execution errors, self-verification — makes the plan adaptive; a detailed reason for a failure corrects the next plan far better than a bare success/fail signal, so prefer the detailed form wherever the environment can supply it.
   - Human feedback is a subjective signal that aligns the agent with human values and preferences and helps offset hallucination, at the cost of needing a person in the loop.
   - Model (internal) feedback lets the agent critique its own output in a self-refine cycle — output, then model-generated feedback, then a revision, repeated until a target condition is met; prefer feedback expressed in words over a single scalar score, since verbal feedback carries more of the information the next revision needs.
   - Combine sources — for example, collecting both environment and human feedback within the same agent — rather than treating any one source as sufficient alone.
6. If fine-tuning is in scope — because prompt and mechanism engineering alone (step 3) proved insufficient, or the domain calls for it from the outset — choose the training-data source by its trade-off, and combine or sequence sources where the budget allows (P060):
   - Human-annotated data is versatile across scenarios but requires designing the annotation task and recruiting and managing annotators, which is costly, especially at scale.
   - LLM-generated data is much cheaper to produce and can be generated in far greater volume, at the cost of a real risk of lower quality than human-annotated data.
   - Real-world application data (diverse tasks, real scenarios, genuine user interaction patterns) is an effective choice specifically for domain-specific tasks, such as navigating real applications or turning natural language into structured queries.
7. Assemble the recommendation as one strategy statement covering every axis from steps 2-6 that applies to this agent: the backbone, the capability-acquisition mechanism(s), the profile-generation approach (if any), the plan-feedback wiring (if any), and the fine-tuning data source (if any) — each paired with the alternative(s) set aside, the reason, and the trade-off or residual limit being accepted.
8. Hand the implementation, the exact prompts, and the actual parameter tuning back to the engineering team; this skill selects and justifies the strategy, it does not build it.

## Anti-patterns

- Defaulting to a hand-authored finite-state machine or behavior tree for an agent that must cover open-world breadth, because it will only ever execute what was hard-coded in advance (P009).
- Assuming reinforcement learning alone will yield believable general behavior because it succeeded in a game with a clean, definable reward — open-world believability has not been shown to follow from that success (P009).
- Treating a bare language-model prompt, with no explicit memory, reflection, or planning, as sufficient for an agent that must stay consistent over a long run, then treating the resulting incoherence as a mystery (P009).
- Jumping straight to fine-tuning before trying prompt and mechanism engineering, or conversely assuming prompt engineering always suffices regardless of how much task information the context window can hold (P027).
- Picking one non-fine-tuning mechanism, such as only a critic loop, without checking whether the actual capability gap is better matched by debate, an experience/skill library, or self-driven evolution (P027).
- Assuming one profile-generation strategy is universally best — handcrafting an entire large population regardless of cost, or trusting generated profiles for a role where precise, controlled characterization matters — instead of weighing the trade-off for this case (P033).
- Driving plan revision from a single feedback source, such as only an environment success/fail bit or only the model's own self-critique, when other reachable sources would catch different error classes (P034).
- Choosing a fine-tuning dataset source on cost or convenience alone without naming the quality, control, or realism it trades away (P060).
- Presenting the recommended strategy as risk-free or already solved instead of naming its trade-off and the residual limit the caller must still manage.

## Principles covered

- P009 — For open-world behavioral breadth, prefer a language-model core with explicit memory, reflection, and planning over hand-authored rule systems, reward-driven reinforcement learning, or classic symbolic cognitive architectures; none scale to that breadth alone.
- P027 — Acquire capability without fine-tuning through prompt and mechanism engineering — critic loops, multi-agent debate, experience/skill libraries, self-driven evolution — usable with open- or closed-source models but bounded by the context window and the design-space size.
- P033 — Choose a profile-generation strategy — handcrafting, LLM-generation, dataset alignment — by its flexibility/control/realism trade-off, and combine strategies when it adds value.
- P034 — Drive plan revision with feedback from the environment, from humans, and from the model itself, favoring detailed reasons over bare signals and combining sources rather than relying on one.
- P060 — Choose a fine-tuning dataset source — human-annotated, LLM-generated, real-world — by its cost/control/realism trade-off.

## Inputs

- The agent's target environment and how open-ended its behavior must be.
- Whether fine-tuning is available, affordable, or already decided for this build.
- Whether the agent needs a role, persona, or profile, and for what purpose.
- Whether the agent plans, and which feedback channels (environment, human, model) are actually reachable.
- What the caller has already fixed versus what is still open for recommendation.

## Output

- A strategy recommendation across the axes that apply to this agent — backbone, capability acquisition, profile generation, plan-feedback wiring, fine-tuning data source — each tied to a named principle and its trade-off.
- The alternatives considered and the specific reason each was set aside for this case.
- The residual risk or limit the caller must still manage after adopting the recommendation.

## References

- The generative-agents interactive-simulation study, for the comparison of agent-building backbones under open-world breadth (P009).
- The survey of large-language-model-based autonomous agents, for capability acquisition without fine-tuning, profile-generation strategy, plan-revision feedback, and fine-tuning dataset source (P027, P033, P034, P060).

## Provenance

Grounded in principles P009, P027, P033, P034, P060; see this package's provenance ledger and principles/evidence records for full claim- and source-level traceability.
