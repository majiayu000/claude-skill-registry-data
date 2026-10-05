---
name: context-report
description: 分析當前專案的 Claude Code session 資料，產出 context 效率報告（模型用量、工具效率、委派比例、TodoWrite 使用率）。搭配 context-management.md 使用。
disable-model-invocation: true
context: fork
allowed-tools: Bash(jq:*), Bash(find:*), Bash(wc:*), Bash(du:*), Bash(sort:*), Bash(uniq:*), Bash(head:*), Bash(cat:*), Bash(basename:*), Bash(bc:*), Bash(date:*), Bash(ls:*), Bash(tr:*), Bash(grep:*), Bash(sed:*), Bash(echo:*), Bash(printf:*)
---

# Context Efficiency Report

## 觸發條件

- 評估一個 project 的 Claude Code 使用效率
- 做成本最佳化分析（過高 Opus 比例時）
- 專案完成後的 session 回顧
- 配合 `.claude/rules/context-management.md` 做 context 壓縮決策

## 執行腳本

執行以下 bash 腳本（適配 Claude Code 官方 `~/.claude/projects/` 路徑）：

```bash
#!/bin/bash
CWD="${ARGUMENTS:-$(pwd)}"
PROJECT_KEY=$(echo "$CWD" | sed 's|/|-|g; s|^-||')
PROJECTS_BASE="$HOME/.claude/projects"
PROJECT_DIR="$PROJECTS_BASE/$PROJECT_KEY"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "No session data found for: $CWD"
  echo "Looking in: $PROJECT_DIR"
  echo "Available projects:"
  ls "$PROJECTS_BASE" 2>/dev/null | head -10
  exit 1
fi

echo "╔══════════════════════════════════════════════════════════════════╗"
printf "║  Context Efficiency Report: %-35s║\n" "$(basename "$CWD" | head -c 34)"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo "Project: $CWD"
echo ""

# Session counts
session_count=$(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" ! -name "agent-*.jsonl" 2>/dev/null | wc -l | tr -d ' ')
agent_count=$(find "$PROJECT_DIR" -maxdepth 1 -name "agent-*.jsonl" 2>/dev/null | wc -l | tr -d ' ')
echo "📁 SESSIONS"
echo "────────────────────────────────────────────────────────────────────"
echo "Main Sessions:  $session_count"
echo "Agent Sessions: $agent_count"
if [ "$session_count" -gt 0 ]; then
  ratio=$(echo "scale=2; $agent_count / $session_count" | bc)
  echo "Delegation Ratio: ${ratio}:1"
fi
echo ""

# Model usage
echo "🤖 MODEL USAGE"
echo "────────────────────────────────────────────────────────────────────"
find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -size +1k -exec cat {} + 2>/dev/null | \
  jq -r 'select(.message.model != null) | .message.model' 2>/dev/null | \
  sort | uniq -c | sort -rn
echo ""

# Tool usage top 15
echo "🔧 TOOL USAGE (top 15)"
echo "────────────────────────────────────────────────────────────────────"
find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -size +1k -exec cat {} + 2>/dev/null | \
  jq -r '.message.content[]? | select(.type == "tool_use") | .name' 2>/dev/null | \
  sort | uniq -c | sort -rn | head -15
echo ""

# Data size
echo "📊 DATA SIZE"
echo "────────────────────────────────────────────────────────────────────"
total_size=$(du -sh "$PROJECT_DIR" 2>/dev/null | cut -f1)
msg_count=$(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -exec cat {} + 2>/dev/null | wc -l | tr -d ' ')
echo "Total Size:      $total_size"
echo "Message Records: $msg_count"
echo ""

# Collect data once
all_tools=$(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -size +1k -exec cat {} + 2>/dev/null | \
  jq -r '.message.content[]? | select(.type == "tool_use") | .name' 2>/dev/null)
all_models=$(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -size +1k -exec cat {} + 2>/dev/null | \
  jq -r '.message.model // empty' 2>/dev/null)

# Model counts
opus=$(echo "$all_models" | grep -c "opus" || echo 0)
sonnet=$(echo "$all_models" | grep -c "sonnet" || echo 0)
haiku=$(echo "$all_models" | grep -c "haiku" || echo 0)
model_total=$((opus + sonnet + haiku))

# Tool counts
bash_count=$(echo "$all_tools" | grep -c "^Bash$" || echo 0)
grep_count=$(echo "$all_tools" | grep -c "^Grep$" || echo 0)
glob_count=$(echo "$all_tools" | grep -c "^Glob$" || echo 0)
todo_count=$(echo "$all_tools" | grep -c "^TodoWrite$" || echo 0)

# Scoring (100 pts)
score=0
warnings=""

# 1. Model efficiency (30 pts)：Opus ≤50% = 30pts，100% Opus = 0pts
if [ "$model_total" -gt 0 ]; then
  opus_pct=$((opus * 100 / model_total))
  model_score=$((30 - (opus_pct > 50 ? (opus_pct - 50) * 30 / 50 : 0)))
  [ "$model_score" -lt 0 ] && model_score=0
  score=$((score + model_score))
  [ "$opus_pct" -gt 80 ] && warnings="${warnings}⚠️  Opus ${opus_pct}% — 探索型任務改用 Haiku\n"
else
  opus_pct=0; model_score=15; score=$((score + 15))
fi

# 2. Delegation ratio (25 pts)：3:1 = 25pts
if [ "$session_count" -gt 0 ]; then
  delegation_ratio_x100=$((agent_count * 100 / session_count))
  delegation_score=$((delegation_ratio_x100 * 25 / 300))
  [ "$delegation_score" -gt 25 ] && delegation_score=25
  score=$((score + delegation_score))
  [ "$delegation_ratio_x100" -lt 100 ] && warnings="${warnings}⚠️  委派比例低 — 多用 subagent 隔離大型任務\n"
else
  delegation_score=0
fi

# 3. Tool efficiency (25 pts)：native Grep/Glob > Bash
native_search=$((grep_count + glob_count))
if [ "$bash_count" -gt 0 ]; then
  tool_ratio_x100=$((native_search * 100 / bash_count))
  tool_score=$((tool_ratio_x100 * 25 / 50))
  [ "$tool_score" -gt 25 ] && tool_score=25
  score=$((score + tool_score))
  [ "$tool_ratio_x100" -lt 10 ] && warnings="${warnings}⚠️  優先用 Grep/Glob 工具而非 bash grep/find\n"
else
  tool_score=25; score=$((score + 25))
fi

# 4. TodoWrite tracking (20 pts)
if [ "$msg_count" -gt 0 ]; then
  todo_ratio_x1000=$((todo_count * 1000 / msg_count))
  todo_score=$((todo_ratio_x1000 * 20 / 50))
  [ "$todo_score" -gt 20 ] && todo_score=20
  score=$((score + todo_score))
  [ "$todo_count" -eq 0 ] && warnings="${warnings}⚠️  未使用 TodoWrite — 複雜任務應追蹤進度\n"
else
  todo_score=0
fi

# Output score
echo "📈 EFFICIENCY SCORE"
echo "────────────────────────────────────────────────────────────────────"
echo ""
echo "  ┌─────────────────────────────────────┐"
printf "  │         SCORE: %3d / 100            │\n" "$score"
echo "  └─────────────────────────────────────┘"
echo ""
echo "  Breakdown:"
printf "    Model efficiency:    %2d/30  (Opus %d%%)\n" "$model_score" "$opus_pct"
del_ratio=$(echo "scale=1; ($agent_count + 0.0) / ($session_count + 0.001)" | bc)
printf "    Task delegation:     %2d/25  (ratio %s:1)\n" "$delegation_score" "$del_ratio"
printf "    Tool efficiency:     %2d/25  (Grep+Glob: %d, Bash: %d)\n" "$tool_score" "$native_search" "$bash_count"
printf "    Task tracking:       %2d/20  (TodoWrite: %d)\n" "$todo_score" "$todo_count"
echo ""

if [ -n "$warnings" ]; then
  echo "  Warnings:"
  printf "  $warnings"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "Generated: $(date '+%Y-%m-%d %H:%M')"
```

## 評分標準說明

| 維度 | 滿分 | 目標 | 說明 |
|------|------|------|------|
| 模型效率 | 30 | Opus ≤50% | 搜尋/探索用 Haiku，實作用 Sonnet |
| 委派比例 | 25 | ≥3:1 | agent session / main session |
| 工具效率 | 25 | Grep+Glob:Bash ≥50% | 優先用 native tools |
| 任務追蹤 | 20 | TodoWrite 有使用 | 複雜任務應有追蹤 |

## 搭配使用

- 與 `.claude/rules/context-management.md` 對照：score <60 時觸發 Compressed 層級
- 委派比例 <1:1 時，參考 `.claude/rules/subagent-strategy.md` 調整
