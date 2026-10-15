---
name: Wolfram Alpha
description: Computational queries — math, science, conversions, and verified facts.
requires:
  bins: []
  env: [WOLFRAM_APP_ID]
---

# Wolfram Alpha

Use this when you need a **precise computational answer**: unit
conversions, math calculations, chemical properties, astronomical data,
or history/geography with verifiable facts. LLMs tend to hallucinate in
those cases; Wolfram does not.

## Tools
- `wolfram_short(input, units?)` — single-line answer. "distance earth to moon", "sqrt(2)", "capital of Colombia"
- `wolfram_query(input, format?, units?)` — full `queryresult` with pods (input, result, alternative forms, plots)

## Setup
Register at [developer.wolframalpha.com](https://developer.wolframalpha.com/) — AppID free tier: 2000 queries/month.
