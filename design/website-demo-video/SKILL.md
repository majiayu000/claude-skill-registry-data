---
name: website-demo-video
description: Record a visitor-accessible website flow or edit a supplied screen recording into a reviewed product-demo MP4 with Valmera. Use for SaaS walkthroughs, launch clips and landing-page demos with purposeful zooms, readable text and a clear call to action.
license: MIT
---

# Make a website or product demo video with Valmera

Show one useful product outcome. Use a public visitor flow for browser capture, or an approved screen recording supplied by the user for an authenticated or desktop workflow.

## Connection and cost

Connect to `https://valmera.io/mcp/server` and authenticate using the [client setup guide](https://valmera.io/mcp/setup). Discover the current tools and input schemas in the connected session; the names below describe a workflow, not a permanent catalog.

Account creation and uploads are free; editing requires a paid [Valmera plan](https://valmera.io/subscribe). Before billable work, explain the intended scope and use any cost estimate exposed by the account. If an exact quote is unavailable, say so and obtain approval for a bounded preview before proceeding. Reuse an existing explicit scope and budget approval; ask again if the work would exceed it. Do not buy credits or upgrade a plan without authorization. Review a preview before an approved final export.

## Workflow

1. **Choose the project and brief.** Open the intended project or create one. Reuse the supplied URL, audience, format and target action. Ask only for missing information needed to choose the flow.
2. **Plan the capture.** Pick the shortest sequence that demonstrates the outcome, such as the relevant page, feature interaction and call to action. Prefer a small representative capture before a longer sequence. Identify any action that would submit a form or change external state; recording a demo does not itself authorize that action.
3. **Record or import.** For a visitor-accessible page, use the current `record_website_demo` schema for the URL, orientation and steps; use `record_website` when a scrolling capture is sufficient. Do not type credentials, payment details or private customer data into a recording. For a supplied screen recording, upload and wait for source readiness.
4. **Shape the demonstration.** Use `showcase_demo` where suitable for the capture. For a supplied recording, identify meaningful interaction times before applying cursor emphasis or zoom paths. Keep interface labels and the result of each action readable at the delivery size.
5. **Add the story layer.** Apply the requested titles, explanatory text, captions, music and closing call to action. Verify wording, names and interface details against the approved source. Avoid adding claims the product demonstration does not show.
6. **Render and review.** Use `render_preview` and follow the existing job with `wait_for_job`. Inspect rendered frames at interactions, zooms and transitions; check text timing and sound. When a job fails, inspect the terminal result before retrying. Identify the reviewed project and edit version.
7. **Export the approved version.** When final delivery is authorized, call `export_final` with the project and reviewed `edl_version`, then `wait_for_job`, then `download_url` with `kind="final"`. Share the actual final link, not a preview or unfinished job receipt.

Use the [website-demo workflow guide](https://github.com/ABO3SKRALMASAOODI/valmera-mcp/blob/main/docs/WEBSITE-DEMO.md) for a capture brief and review criteria. Confirm delivery files and aspect ratios against the [current publishing guide](https://valmera.io/docs/publishing). Let an active edit finish before opening the same project for edits in another client.
