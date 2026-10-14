---
name: marketkit-to-checklist
description: Turn a campaign into a publishing checklist. Use when the assets are generated and the user needs a checklist of everything to verify and publish before the campaign goes live.
license: MIT
---

# To Checklist

Turn a campaign into a publishing checklist: every asset, every channel, every step.

1. Read the campaign plan and all assets: posts, ads, email, and the schedule. The checklist must cover every asset in the schedule and every asset the plan scoped from the [asset inventory](../references/asset-inventory.md).
2. For each asset, write a checklist item with the channel, the asset, and the action needed to publish it. An asset without a publish action is an asset that will not go live.
3. Add pre-publish checks that apply to every asset: the link works, the image loads, the voice is consistent, and the call to action is clear.
4. Add channel-specific checks from the [platform specs](../references/platform-specs.md): every character limit, image size, and safe zone the asset must fit. Emails have a subject under 60 characters.
5. Order the checklist by the schedule. The first item is the first thing to publish; the last item is the last. A checklist that is not in schedule order is a checklist that will be done out of order.
6. Mark each item as a checkbox. The user checks them off as they publish.

A checklist is a record of what must be done, not a summary of what was made. If an asset is missing from the checklist, it will not be published.

Record this output in `docs/plans/` using the [doc system](../../plan-mode/references/doc-system.md).
