---
name: plan
description: "Plan end to end: draft, render in plan-canvas or Plan Builder, annotate, await approval, then hand off. Generated from plugin-commands.json; invoke as $bdb-aos:plan."
---

Run the full planning pipeline: 1) draft the plan with `concise-planning`; 2) always offer the choice between plan-canvas and Plan Builder (`aos-plan-canvas open <dir> --mode bdb-plan-builder`) for rendering; 3) collect annotations and wait for the human's approval; 4) only after approval continue with `writing-plans` or `$bdb-aos:graph`. Topic: whatever the user wrote after the skill name
