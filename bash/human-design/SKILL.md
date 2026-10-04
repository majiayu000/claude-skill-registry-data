---
name: human-design
description: Generate a grounded Human Design BodyGraph and whole-chart reading from exact birth data. Use for Human Design charts, BodyGraph, decisions, profile, channels, talents, work, wealth, relationships, mission, or chart-based follow-up questions. Supports Chinese and English.
---

# Human Design

Use this skill to calculate first and interpret second. Never infer a chart from personality descriptions or invent missing gates, channels, centers, Authority, profile, or incarnation cross.

## Required Input

Collect all three before producing a formal chart:

- Gregorian birth date
- Birth time, preferably exact to the minute
- Birth place or an explicit IANA timezone

If the time or place is missing, explain the precision limit and ask for it. Do not present a birthday-only result as a formal Human Design chart.

## Privacy Boundary

Prefer local calculation. Do not send birth data, names, reports, or chat history to the public demo or another remote API without explicit user consent. Never place real user data in README examples, screenshots, fixtures, logs, issues, or commits.

Read [references/privacy.md](references/privacy.md) before using a remote endpoint.

## Local Workflow

From an installed skill bundle, run:

```bash
python scripts/human_design_agent.py chart '1988-10-09T20:30:00+08:00'
python scripts/human_design_agent.py report '1988-10-09T20:30:00+08:00' --map-type talent
python scripts/human_design_agent.py context '1988-10-09T20:30:00+08:00' --focus talent --question '我的天然优势怎样形成代表作？' --format markdown
```

With an explicit UTC offset or `--timezone`, chart calculation stays local and makes no network requests. If you use a birth place without a timezone, the CLI refuses to continue unless you pass `--allow-location-lookup`; that flag means the user has consented to external geocoding and timezone lookup. The script also rejects a local datetime that has neither an offset, timezone, nor place. Read the privacy reference before using remote lookup. The script requires the `human-design-llm` Python package. If it is unavailable, install the repository in a virtual environment:

```bash
python -m pip install 'human-design-llm @ git+https://github.com/joyozhang333-lgtm/human-design-llm.git@v0.7.1'
```

For development inside the cloned repository, prefer:

```bash
python -m pip install -e '.[web]'
```

## Interpretation Order

1. Verify input warnings and chart facts.
2. Explain type, action strategy, Authority, profile, definition, and incarnation-cross name.
3. Explain each actual defined channel in ordinary language.
4. Combine the relevant structures into the user's question instead of giving isolated glossary entries.
5. Name the mature expression, blind spot, stuck pattern, likely cause, and one observable practice.
6. End with one useful question when continued dialogue would improve accuracy.

## Whole-Chart Rule

For talent, work, wealth, relationships, or mission, connect at least two real chart structures. A profile or channel should never be treated as a complete answer by itself. Describe what the combined pattern looks like when lived well, what it costs when misused, and how the user can test it in current life.

Use the report modes in [references/contracts.md](references/contracts.md) when you need a structured output.

## Language

For Simplified Chinese, use `荐骨中心`, `阿姬娜中心`, and `喉咙中心`. Show Authority with its professional English name plus a short Chinese explanation, for example `Sacral Authority（荐骨决策方式）`.

Write for a reader, not a developer. Never expose prompt instructions, reasoning traces, field names, validation notes, fallback status, or product acceptance language.

## Safety

Human Design is a reflective framework, not scientific proof, medical or psychological diagnosis, financial advice, or deterministic fate prediction. Use observable and probabilistic language. Do not promise an accuracy percentage.

## Host Setup

See [references/host-install.md](references/host-install.md) for Codex, Claude Code, DeepSeek Harness, Hugging Face-compatible Agent Skills, OpenClaw, and Tencent WorkBuddy.
