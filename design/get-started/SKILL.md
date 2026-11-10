---
name: get-started
description: Help someone new to the Endless Design Studio find their way and make a first prototype on Endless Studios screens. Use when they are new, ask for a tour, or want help starting; registration and configuration have their own skills.
---

# Get started in the studio

Read the module [README](../../README.md). The person is usually an Endless designer or product person; speak in their terms (prototypes, screens, canvases), not in file paths, unless they ask.

## Find out where they are

1. Confirm the studio folder you work in is the one they have open. A browser tab alone doesn't tell you which checkout it is.
2. Run `yarn studio whoami`. If it resolves to nobody, register them first with [setup-contributor](../../../../platform/skills/setup-contributor/SKILL.md); they can look around without it, but they can't make a prototype.
3. Ask what they want to do today. If they only want a tour, use the [What newcomers hear](#what-newcomers-hear) points below, then offer to make a first prototype together.

## Make a first prototype on Endless Studios

4. Ask about the idea in a few questions, not a form: what they want to explore, who it's for (the system's [user types](../../../../systems/endless-studios/context/user-types.md) help name them), which Endless Studios screen it starts from, and what they want to learn. Start with what they know; assume the rest out loud.
5. Follow [build-prototype](../../../prototypes/skills/build-prototype/SKILL.md) and the Endless Studios system's `AGENTS.md`. Create the prototype with `yarn new "<their title>"` as them; the default system is Endless Studios. Build one view from the closest existing screen, with sample data and the signed-in user that fit the idea. Add named states only for the variations they asked about.
6. Give them the address `yarn new` printed and ask them to try it. Then ask what should change and what should stay.
7. When there is more than one view or option, offer a canvas to lay them out side by side ([use-canvas](../../../canvas/skills/use-canvas/SKILL.md), only while Canvases is on) or a short document of what they learned ([write-document](../../../document/skills/write-document/SKILL.md), only while Documents is on). Offer, don't impose.

## What newcomers hear

Keep each point to a sentence or two, and only what helps now:

- The studio is the Endless team's prototyping sandbox: they describe an idea, you build it as a working prototype, and the team tries it in the studio.
- Prototypes start from Endless Studios' own screens and components, so they look and behave like the product, with sample data instead of real accounts.
- A canvas puts views, documents and notes side by side; they can draw over a view to show you what to change.
- To ask you for something, say what to explore, for whom and from which screen. To show you which part they mean, they comment on it in the studio (**Comment** on the page, while Comments is on) and ask you to address the comments; pointing in their agent's browser or a screenshot works too.
- The Manual (while it's on) explains the rest: point to [Working with your agent](../../../documentation/pages/agent.md) and [Prototypes & systems](../../../documentation/pages/prototypes.md).

## The welcome

The welcome opens over Home on a contributor's first local visit and is recorded on their profile (`preferences.onboarding.welcomeDismissed`). If they want to see it again, set that flag to `false` in their own `contributors/<key>.json` and reload Home. Don't change anyone else's profile.

## Don't

Don't install tools, change `studio.config.json`, turn modules on or off, or change the Endless Studios system just to get someone started. Those have their own skills ([configure-studio](../../../../platform/skills/configure-studio/SKILL.md), [manage-modules](../../../../platform/skills/manage-modules/SKILL.md), [setup-design-system](../../../systems/skills/setup-design-system/SKILL.md)) and need the person to ask for them.
