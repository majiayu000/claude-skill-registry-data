---
name: vibecode-prompt
description: Turn an app idea into a precise build prompt for an AI app builder (Lovable, v0, Bolt, Replit, and others). Trigger on "build me an app", "prompt for Lovable", "v0 prompt", "vibecode this", "I want to build a tool that", "prompt to build a web app", or any request to spin up an app with an AI builder.
---

# Vibecode Prompt

## What this does
Takes an app idea in plain words and returns a build prompt structured the way AI app builders want it: the one-sentence product, the pages, the data model, the core interactions, the styling, and what to build first. A vague prompt gives you a vague app. This one gives the builder a spec.

## What you'll need
An AI app builder to paste the result into (Lovable, v0, Bolt, Replit, or similar). No connectors. Bring the idea; the skill builds the prompt.

## Customize this for yourself
| Set this | What it is | Example |
|---|---|---|
| Target builder | The tool you will paste into | Lovable, v0, Bolt, Replit |
| Stack preference | Any framework or service you want it to use | Next.js, Supabase, Tailwind |
| Look and feel | Your default visual direction | "Clean, lots of whitespace, one accent color" |

## The method
1. Name the product in one sentence: what it is and who it is for.
2. List the pages or screens, each with its job in a phrase.
3. Define the data model: the few objects and their fields. Builders go sideways without this.
4. Spell out the core interactions: what happens when the user clicks the main button.
5. Set the styling: the visual direction and the one or two brand colors.
6. Sequence the build: "Start with the data model and the main page. Get that working before anything else." This stops the builder from trying to do everything at once and breaking.
7. Add guardrails: no auth in v1, mock the data, keep it one page until it works.

## Output (example)
Idea: "a tracker for my outreach experiments."
Built prompt:
```
Build a single-page web app: an outreach-experiment tracker for a salesperson.

Pages: one main page, a table of experiments with an "add experiment" form.

Data model:
- Experiment { name, channel, hypothesis, sent, replies, status, notes }

Interactions:
- "Add experiment" opens a form, saves a row to the table
- Each row shows a computed reply rate (replies / sent)
- A status pill: running, won, killed

Styling: clean, lots of whitespace, one orange accent, system font.

Build order: first the data model and the table with mock rows. Get that
rendering. Then the add form. Then the computed reply rate. No auth in v1.
```

## Example chat

**You:** I want to build a tracker for my outreach experiments. Can you write me a Lovable prompt?

**Claude:** Here's the build prompt.
```
Build a single-page web app: an outreach-experiment tracker for a salesperson.
Data model: Experiment { name, channel, hypothesis, sent, replies, status, notes }
Build order: first the data model and the table with mock rows. Get that
rendering. Then the add form. Then the computed reply rate. No auth in v1.
```
Key insight: the build-order line is the one thing that keeps Lovable from trying to ship auth, styling, and the data model all in one pass and breaking, sequencing it is what actually gets you a working v1. One sharpener: name your target builder (Lovable vs v0 vs Bolt), the prompt format shifts slightly for each.

## Go further
The prompt is written. Here is where an operator takes it once the manual version proves out.

- **Deploy the moment it builds.** Once the app builder ships a working version, push it straight to Vercel so you are testing on a real URL instead of a preview pane.
- **Feed it real data instead of mock rows.** Wire the tracker to pull from a live sheet or Airtable base once the data model holds up, so v1 becomes the real tool, not a demo.
- **Let a scheduled task keep it stocked.** Have a scheduled Claude task log your actual outreach sends into the tracker's data store daily, so the experiment table fills itself.

The prompt gets you a working v1; the wiring is what makes it the tool you actually use.


## Make it yours
Set your target builder, your stack, and your look. Then describe any tool you want and get a prompt the builder can actually execute. Built by an operator. Customize it, break it, make it better.
