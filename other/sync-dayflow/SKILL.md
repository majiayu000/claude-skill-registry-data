---
name: sync-dayflow
description: 将 Dayflow 数据库增量同步到 Obsidian。当用户说"同步 dayflow"、"sync dayflow"或"/sync-dayflow"时使用此 skill。
---

# Dayflow 数据同步

将 Dayflow 应用的数据库内容增量同步到 Obsidian。

## 同步内容
- 时间线卡片 (timeline_cards) -> Dayflow活动日志/
- 日志总结 (journal_entries) -> Dayflow每日报告/
- 观察记录 (observations) -> Dayflow提醒建议/

## 执行步骤

使用 Bash 工具执行以下 Python 脚本：

```bash
python3 << 'EOF'
import os
import sqlite3
from datetime import datetime


def to_datetime(ts):
    if ts is None:
        return None
    value = int(ts)
    if value > 1_000_000_000_000:
        value = value / 1000
    return datetime.fromtimestamp(value)


def write_if_changed(filepath, content):
    old_content = None
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            old_content = f.read()
    if old_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


db_path = "/Users/tangchunwu/Library/Application Support/Dayflow/chunks.sqlite"
obsidian_base = "/Users/tangchunwu/Documents/Obsidian Vault"

activity_dir = os.path.join(obsidian_base, "Dayflow活动日志")
report_dir = os.path.join(obsidian_base, "Dayflow每日报告")
tips_dir = os.path.join(obsidian_base, "Dayflow提醒建议")
os.makedirs(activity_dir, exist_ok=True)
os.makedirs(report_dir, exist_ok=True)
os.makedirs(tips_dir, exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1) 同步活动日志（timeline_cards）
cursor.execute("SELECT DISTINCT day FROM timeline_cards WHERE is_deleted = 0 ORDER BY day")
days = [row[0] for row in cursor.fetchall()]
activity_updated = 0

for day in days:
    cursor.execute(
        """
        SELECT start, end, title, summary, detailed_summary, category, subcategory
        FROM timeline_cards
        WHERE day = ? AND is_deleted = 0
        ORDER BY id
        """,
        (day,),
    )
    rows = cursor.fetchall()
    if not rows:
        continue

    lines = [f"# {day} Dayflow 活动日志", ""]
    for start, end, title, summary, detailed_summary, category, subcategory in rows:
        title = (title or "(无标题)").strip()
        start = (start or "--").strip()
        end = (end or "--").strip()
        summary = (summary or "").strip()
        detailed_summary = (detailed_summary or "").strip()
        category = (category or "").strip()
        subcategory = (subcategory or "").strip()

        lines.append(f"## {start} - {end}")
        lines.append(f"### {title}")
        lines.append("")
        if category:
            tag_line = f"**分类**: {category}"
            if subcategory:
                tag_line += f" / {subcategory}"
            lines.append(tag_line)
            lines.append("")
        if summary:
            lines.append(summary)
            lines.append("")
        if detailed_summary:
            lines.append("**详细总结**")
            lines.append("")
            lines.append(detailed_summary)
            lines.append("")
        lines.append("---")
        lines.append("")

    filepath = os.path.join(activity_dir, f"{day}.md")
    content = "\n".join(lines).rstrip() + "\n"
    if write_if_changed(filepath, content):
        activity_updated += 1

print(f"活动日志: 更新 {activity_updated} 天")

# 2) 同步每日报告
# 优先使用 journal_entries；若无数据则由 timeline_cards 自动聚合生成日报
cursor.execute(
    """
    SELECT day, intentions, goals, notes, reflections, summary, status
    FROM journal_entries
    ORDER BY day
    """
)
reports = cursor.fetchall()
report_updated = 0

if reports:
    for day, intentions, goals, notes, reflections, summary, status in reports:
        filepath = os.path.join(report_dir, f"{day}.md")

        blocks = []
        if status:
            blocks.append(("状态", str(status).strip()))
        if intentions:
            blocks.append(("今日意图", intentions.strip()))
        if goals:
            blocks.append(("目标", goals.strip()))
        if summary:
            blocks.append(("总结", summary.strip()))
        if reflections:
            blocks.append(("反思", reflections.strip()))
        if notes:
            blocks.append(("补充笔记", notes.strip()))

        if not blocks:
            continue

        lines = [f"# {day} Dayflow 每日报告", ""]
        for title, content in blocks:
            if not content:
                continue
            lines.append(f"## {title}")
            lines.append("")
            lines.append(content)
            lines.append("")

        new_content = "\n".join(lines).rstrip() + "\n"
        if write_if_changed(filepath, new_content):
            report_updated += 1
else:
    cursor.execute(
        """
        SELECT day, start, end, start_ts, end_ts, title, summary, detailed_summary, category
        FROM timeline_cards
        WHERE is_deleted = 0
        ORDER BY day, id
        """
    )
    rows = cursor.fetchall()

    cards_by_day = {}
    for day, start, end, start_ts, end_ts, title, summary, detailed_summary, category in rows:
        cards_by_day.setdefault(day, []).append(
            {
                "start": (start or "--").strip(),
                "end": (end or "--").strip(),
                "start_ts": start_ts,
                "end_ts": end_ts,
                "title": (title or "(无标题)").strip(),
                "summary": (summary or "").strip(),
                "detailed": (detailed_summary or "").strip(),
                "category": (category or "Unknown").strip() or "Unknown",
            }
        )

    for day, cards in sorted(cards_by_day.items()):
        if not cards:
            continue

        total = len(cards)
        category_counts = {}
        for c in cards:
            category_counts[c["category"]] = category_counts.get(c["category"], 0) + 1

        top_category, top_count = sorted(category_counts.items(), key=lambda x: (-x[1], x[0]))[0]

        start_candidates = [to_datetime(c["start_ts"]) for c in cards if c["start_ts"] is not None]
        end_candidates = [to_datetime(c["end_ts"]) for c in cards if c["end_ts"] is not None]
        start_candidates = [x for x in start_candidates if x is not None]
        end_candidates = [x for x in end_candidates if x is not None]

        if start_candidates and end_candidates:
            first_time = min(start_candidates).strftime("%H:%M")
            last_time = max(end_candidates).strftime("%H:%M")
        else:
            first_time = cards[0]["start"]
            last_time = cards[-1]["end"]

        def card_score(c):
            duration = 0
            if c["start_ts"] is not None and c["end_ts"] is not None:
                duration = max(0, int(c["end_ts"]) - int(c["start_ts"]))
            text_score = len(c["summary"]) + len(c["detailed"])
            return (duration, text_score)

        top_cards = sorted(cards, key=card_score, reverse=True)[:5]

        summary_parts = []
        for c in top_cards:
            text = c["summary"] or c["detailed"]
            if text:
                summary_parts.append(text)
            if len(summary_parts) >= 3:
                break
        if summary_parts:
            one_liner = "；".join(summary_parts)
            if len(one_liner) > 240:
                one_liner = one_liner[:240].rstrip() + "..."
        else:
            one_liner = "今天主要围绕多个任务场景切换推进。"

        lines = [f"# {day} Dayflow 每日报告", ""]
        lines.append("## 今日概览")
        lines.append("")
        lines.append(f"- 卡片数: {total}")
        lines.append(f"- 活跃时段: {first_time} - {last_time}")
        lines.append(f"- 主分类: {top_category} ({top_count}/{total})")
        lines.append("")

        lines.append("## 今日重点")
        lines.append("")
        for idx, c in enumerate(top_cards, start=1):
            key_text = c["summary"] or c["detailed"] or "(无摘要)"
            if len(key_text) > 120:
                key_text = key_text[:120].rstrip() + "..."
            lines.append(f"{idx}. {c['start']} - {c['end']} | {c['title']}")
            lines.append(f"   - {key_text}")
        lines.append("")

        lines.append("## 分类统计")
        lines.append("")
        for k, v in sorted(category_counts.items(), key=lambda x: (-x[1], x[0])):
            pct = (v * 100.0) / total
            lines.append(f"- {k}: {v} ({pct:.1f}%)")
        lines.append("")

        lines.append("## 一句总结")
        lines.append("")
        lines.append(one_liner)
        lines.append("")

        filepath = os.path.join(report_dir, f"{day}.md")
        new_content = "\n".join(lines).rstrip() + "\n"
        if write_if_changed(filepath, new_content):
            report_updated += 1

print(f"每日报告: 更新 {report_updated} 天")

# 3) 同步提醒建议（observations）
cursor.execute(
    """
    SELECT start_ts, end_ts, observation
    FROM observations
    ORDER BY start_ts
    """
)
obs_rows = cursor.fetchall()

obs_by_day = {}
for start_ts, end_ts, observation in obs_rows:
    start_dt = to_datetime(start_ts)
    end_dt = to_datetime(end_ts)
    if start_dt is None:
        continue
    day = start_dt.strftime("%Y-%m-%d")
    obs_by_day.setdefault(day, []).append((start_dt, end_dt, (observation or "").strip()))

tips_updated = 0
for day, items in sorted(obs_by_day.items()):
    lines = [f"# {day} Dayflow 提醒建议", ""]
    for start_dt, end_dt, text in items:
        start_text = start_dt.strftime("%H:%M:%S")
        end_text = end_dt.strftime("%H:%M:%S") if end_dt else "--:--:--"
        lines.append(f"## {start_text} - {end_text}")
        lines.append("")
        lines.append(text if text else "(空)")
        lines.append("")
        lines.append("---")
        lines.append("")

    filepath = os.path.join(tips_dir, f"{day}.md")
    content = "\n".join(lines).rstrip() + "\n"
    if write_if_changed(filepath, content):
        tips_updated += 1

print(f"提醒建议: 更新 {tips_updated} 天")

conn.close()
print(f"\n同步完成! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
EOF
```

执行完成后向用户报告同步结果。
