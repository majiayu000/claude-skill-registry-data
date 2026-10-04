---
name: priced-round-dilution
description: "A founder wants to compare simple priced-equity financing scenarios. Produces A pre/post-money and ownership bridge with explicit instrument exclusions."
---

# Priced-round dilution

Read references/working-templates.md. Collect pre-money equity value, new cash, fully diluted pre-round shares and any existing holder’s shares. In a simple round with no other changes, post-money equals pre-money plus new cash, price per share equals pre-money divided by pre-round shares, and new investor ownership equals new cash divided by post-money. Reconcile new and existing shares and ensure ownership sums to 100 percent. Use scripts/dilution.py for this exact simple case. If SAFEs, notes, option-pool top-ups, warrants, secondary shares or fees are present, stop using the simple calculator and build a term-specific model from the actual documents. Distinguish cash going to the company from secondary proceeds. Present raw terms and questions for counsel; do not choose a deal for the user.
