---
name: prompt-architect
description: Turn a rough task into a precise, ready-to-paste prompt for any AI platform (Claude, GPT, Gemini, and others). Trigger on "write me a prompt for", "I need an AI to", "help me prompt engineer", "build a system prompt", "make this prompt better", "optimize my prompt", or any prompt-building request.
---

# Prompt Architect

## What this does
Takes a rough description of what you want an AI to do and returns a precise, structured prompt you can paste into any model. It pins down the role, the task, the inputs, the constraints, the output format, and the failure modes, so the model has nothing to guess.

## What you'll need
Any AI chat tool to paste the result into. No connectors. Bring the task; the skill builds the prompt.

## Customize this for yourself
| Set this | What it is | Example |
|---|---|---|
| Target model | The platform you will paste into | Claude, GPT, Gemini |
| Your defaults | House style for every output | "Plain language, no preamble, cite sources" |
| Reusable context | Facts the model should always have | Your company, your audience, your product |

## The method
1. Extract the job. What is the AI producing, for whom, and what does good look like.
2. Assign a role. A "you are a..." that matches the job.
3. Specify the inputs. What you will give it, in what form.
4. Set the constraints. Length, tone, what to avoid, what never to do.
5. Lock the output format. A template the model fills, not a vague ask.
6. Add the failure modes. "If you do not have X, say so and stop. Do not invent."
7. Add one example if the task is fuzzy. A model copies an example faster than it parses a paragraph.

## Output (example)
Rough ask: "summarize customer calls."
Built prompt:
```
You are a customer-research analyst. Summarize the call transcript below for a
product team that has not heard the call.

Output exactly these sections:
- One-line verdict (did this account love it, like it, or struggle)
- 3 quotes that prove the verdict, with the speaker role
- The one feature request that came up
- The next step the rep committed to

Rules: quote the customer's own words, never paraphrase a quote. If a section
has no evidence in the transcript, write "none stated." Do not infer sentiment
the words do not support.

Transcript:
[paste]
```

## Example chat

**You:** I need a prompt that summarizes customer calls for the product team. They haven't heard the call.

**Claude:** Built it from the job backward.
```
You are a customer-research analyst. Summarize the call transcript below for a
product team that has not heard the call.

Output exactly these sections:
- One-line verdict (did this account love it, like it, or struggle)
- 3 quotes that prove the verdict, with the speaker role
- The one feature request that came up
- The next step the rep committed to

Rules: quote the customer's own words, never paraphrase a quote. If a section
has no evidence in the transcript, write "none stated." Do not infer sentiment
the words do not support.
```
The rule against inferring sentiment is the piece doing the real work here. Without it, a model will happily invent a verdict from tone alone, and product will read a summary that sounds confident but isn't grounded in anything said.

**You:** Can you make it work for GPT instead of Claude?

**Claude:** Same structure, the format section and the failure-mode rules travel across models unchanged, only the framing at the top shifts slightly for how GPT tends to read instructions. Sharpener: tell me your house defaults (tone, what to always avoid, standing context like your company and audience) once, and every prompt after this one starts from that baseline instead of being rebuilt from scratch.

## Go further
One well-built prompt is a single task solved. Here's what it looks like running as infrastructure.

- **Turn it into a repeatable column.** Feed the prompt into Clay as an enrichment column so every new call transcript gets summarized the same way automatically, not one at a time.
- **Run it on a schedule.** A scheduled Claude task applies the prompt to every call logged that day and posts the summaries to Slack for the product team each morning.
- **Version it like code.** Keep the prompt in a shared doc or repo with a changelog, so when the output drifts, you can see exactly which rule changed and roll it back.

A good prompt gets the same answer twice. The system is what gets it a thousand times without you watching.

## Make it yours
Set your target model and your defaults once. Then describe any task and get a prompt that leaves nothing to chance. Built by an operator. Customize it, break it, make it better.
