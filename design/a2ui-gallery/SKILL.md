---
name: a2ui-gallery
description: A curated tour of the A2UI component catalog — what every Jutsu app can look like.
commands:
  - id: demo-data
    run: ./scripts/demo.sh
    description: Generate sample data bound to the gallery surface
    output: json
ui: .
---
# a2ui-gallery

Showcase app for the Jutsu A2UI catalog. Ships a pre-baked A2UI surface
(`ui/a2ui.json`) and a `demo-data` command whose stdout JSON hydrates the
data model. Try: "refresh the demo data".