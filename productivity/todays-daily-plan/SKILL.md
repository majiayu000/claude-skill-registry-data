---
name: todays-daily-plan
description: Write spoken daily planning notes into an Obsidian Mandala Grid day-plan Markdown file. Use when the user says 今日的日計畫, 今日的日計劃, 日計畫, 日計劃, 青蛙, frog, 🐸, 九宮, 曼陀羅, Mandala Grid, 時段, time block, 日記, or asks to place spoken tasks/events/reflections into today's Obsidian daily plan sections.
---

# 今日的日計畫

## Overview

Use this skill to turn the user's spoken Chinese or mixed-language notes into precise updates inside an Obsidian Mandala Grid day-plan Markdown file. Preserve Mandala Grid section markers, route content into today's 8 time slots, and append diary reflections without rewriting unrelated days.

Default target file, when the user does not provide another path:
`/Users/twhsi/+ 02 Area_Mandlal Diary 曼陀羅手帳/00 Daily/1.a 2026 日計劃.md`

## Required Contract

Before manually editing a Mandala Grid day-plan file, read `references/mandala-grid-day-plan.md`. Prefer `scripts/update_today_plan.py` for section-safe updates.

Only operate on files with `mandala: true` and `mandala_plan.enabled: true`. Do not alter `<!--section: ...-->` IDs except to add missing child sections `N.1` through `N.8` under an existing day root section.

## Workflow

1. Identify the target date. Use the user's explicit date if provided; otherwise use today's local date.
2. Read the target Markdown and confirm Mandala Grid day-plan frontmatter.
3. Resolve the day root section from the plan year and date. Example: 2026-06-18 is section `169`.
4. Ensure the day has 8 child sections and slot headings from `mandala_plan.slots`.
5. Classify each spoken item into a slot.
6. Before writing, inspect the target day or run the script without `--apply` to preview. If the task resumes after an interruption, append only entries that are still missing.
7. Append content to the chosen section. Never overwrite existing content unless the user explicitly asks to replace it.
8. Read back the target day section after writing and summarize the changed section(s). When the user asks for syntax, show the exact spoken prompt pattern they can reuse.

## Slot Routing

Use explicit time first, then semantic cues.

- `1` / `陽光起床運動`: 起床, 太陽, 陽光, 跑步, 運動, 靜坐, 早餐, 心情, 習慣.
- `2` / `09-12`: 上午, 早上, 09, 9點, 10點, 11點, 日文課, 深度工作.
- `3` / `12-13`: 中午, 午餐, 午睡, 12點, 領午餐.
- `4` / `13-15`: 13點, 14點, 下午一點, 下午兩點, 午後開始.
- `5` / `15-18`: 15點, 16點, 17點, 下午三點到六點.
- `6` / `18-19`: 18點, 六點, 六點半, 晚餐, 傍晚.
- `7` / `19-21`: 晚上, 19點, 20點, 合唱, 管委會, 晚間課, 會議.
- `8` / `日記`: 日記, 反省, 感謝, 心得, 今天發生, 回顧, 感覺.

If the user says `青蛙`, `frog`, or `🐸`, preserve that marker in the entry. Route it by the surrounding time words; if no time is present, ask one short clarification or append to `日記` when it is clearly a reflection.

If the user gives both a vague spoken time and an explicit slot, prefer the explicit slot. Example: `八點那一格...十八點這格` should go to `18-19` when the user names `18點` or `18-19`. Preserve the user's chosen names, but normalize obvious speech/context slips when the surrounding context is clear, such as `小木` to `小睦` in this diary and `Scale loops` to `Skill Loops` in a Skill/GitHub topic.

## Entry Formatting

- Keep short events as plain text: `羽球`, `林君`, `Esor`.
- Use unchecked tasks only when the user frames the item as a to-do: `- [ ] 老實寫書`.
- Use checked tasks only when the user says it is done: `- [x] 買午餐`.
- Use numbered list items for diary entries and continue the existing number sequence.
- Preserve Obsidian links, Brain links, Markdown tables, image embeds, and code blocks.

## Script

Use the script for deterministic writes:

```bash
python3 scripts/update_today_plan.py \
  --file "/Users/twhsi/+ 02 Area_Mandlal Diary 曼陀羅手帳/00 Daily/1.a 2026 日計劃.md" \
  --date 2026-06-18 \
  --slot "09-12" \
  --text "羽球" \
  --apply
```

Preview without writing by omitting `--apply`. Use `--kind diary`, `--kind task`, `--kind done`, or `--kind plain` when the output format should be explicit.

The script reports `duplicate_skipped: true` when the exact entry already exists in the target section. Treat that as a successful no-op, especially when continuing after a partial write.

## Examples

User: `今日的日計畫，上午羽球，下午三點林君，日記 Miru 來訪，狀況不是很好，加油。`

Action:
- Append `羽球` to `09-12`.
- Append `林君` to `15-18`.
- Append the Miru sentence as the next numbered diary item.

User: `🐸 晚上耿彬 Hermes＋Codex 活動。`

Action: Append `🐸 耿彬 Hermes＋Codex 活動` to `19-21`.

User:

```text
請做 2026-06-19 五 的日計畫：
09-12 準備晚上直播投影片。
13-15 14:00 小睦到達。
18-19 晚上和小睦一起吃披薩。
19-21 20:00 騰訊直播，主題：Hermes、Skill Loops、GitHub。
```

Action:
- Preview or inspect `2026-06-19` first.
- Append each line into the matching slot only if missing.
- Read back the `2026-06-19` section and report the reusable syntax if requested.
