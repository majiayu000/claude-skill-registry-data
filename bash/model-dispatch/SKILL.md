---
name: model-dispatch
description: Resolve Maigo role models and delegation from an explicitly selected profile and the current host's tools. Use before role execution in Maigo commands, including single-model or no-subagent hosts.
---

<!-- mkdocs-include-start -->

# Model Dispatch

**Owner**: orchestrator
**Consumers**: 有角色執行步驟的 Maigo commands；Claude Code、Codex 或其他能讀取這份流程的宿主。

角色的責任、工具限制與交棒契約留在 `agents/*.md`；模型由宿主提供。
不要從宿主品牌、模型名稱、參數量或安裝了 Ollama 推測派工能力。

## 派工前

1. 讀當前 session 的工具 schema 與限制，確認能否啟動 subagent、逐次指定模型、同時執行
   互不相依的 subagents。未確認就視為沒有；工具存在也不代表本次任務獲准使用。
2. 只有使用者明確指定 `--model-profile <path>`（或在本次 session 指定沿用某份 profile）
   才載入該檔；從命令參數移除這一對，剩餘內容交給原 command。
   不掃描 repo、家目錄或環境變數找設定。相對路徑以入口的 project cwd 解析為絕對路徑，
   再進 worktree；內層 quick/go/team 沿用同一個明確選擇。
3. 呼叫下面的 resolver，`--roles` 只列本次會執行的角色；保留 command 原本的順序與
   mode 造成的省略。只有步驟 1 確認可用的能力才加對應旗標。沒有角色要執行時
   （例如 crystallize 沒有候選），不呼叫 resolver。

```bash
python3 <maigo-root>/scripts/resolve_dispatch.py --roles Anon Soyo
# 可用時追加：--subagents --model-override --parallel
# 有明確選擇時追加：--profile <absolute-profile-path>
```

`<maigo-root>` 是目前讀取的 Maigo plugin 的絕對路徑；不能用 target repo 代替。
設定格式、單一模型與混用範例見 [Agents reference](../../docs/reference/agents.md#model-profiles)。
沒有 profile 時仍呼叫 resolver，讓沒有 subagents 的宿主走明確的 fallback。

## 套用結果

CLI exit 0 / `status=ready` 是派工計畫，**不代表模型已連線或任務驗證通過**。
exit 2 / `status=error` 時顯示原因，先解決設定或能力衝突；不能默默忽略指定模型。

- `roles[].model` 為字串：原樣交給宿主的逐次 model 參數；先確認它是宿主實際接受的值。
  不把模型名稱翻成 `haiku` / `sonnet` / `opus`，也不自行換 endpoint 或 provider。
- `roles[].model` 為 `null`：省略逐次 model override，保留宿主原生預設。
  Claude Code 可能沿用 agent frontmatter；其他宿主可能沿用主線模型，不能宣稱一定相同。
- `execution=subagents`：依 command 派工，載入對應 `agent_file`，遵守宿主的工具權限與
  context 傳遞方式。有 fresh context 選項時，review 不繼承實作過程，只傳需求、diff 與證據。
- `execution=inline`：主 agent 依序執行各角色，逐段讀取角色定義並保留原本的讀寫限制、
  產物、checklist 與驗證步驟。明示「同一模型、共用 context」，不能宣稱獨立審查。
- `parallel=true` 只容許 command 原本可並行的階段；探索 → 計畫 → 實作仍有相依順序。
  `parallel=false` 時 `/maigo:team` 自動改為先 🟡 爽世、再 🟣 立希；`--force-sequential`
  永遠優先。角色數量不等於同時啟動數量。

這裡的能力判斷與 fallback 限定 command 中「如何啟動角色」的規則：沒有 subagents
時不要求不存在的 Task tool，但不可省略該 command 的 review / verification。
沒有 hook 時明確執行檢查，依 command 與 target repo 規範留下 command、exit code、output。
宿主若回報替代模型，記錄實際值並處理與要求的差異；無回報則標「實際模型未確認」。

## 模型選擇與重試

未指定 profile 時保留宿主既有預設。使用者可以讓全部角色共用同一模型，也可以只替
規劃或審查配置別的模型；角色職責不依賴模型廠牌。

同一子任務最多重試兩輪（初次不計），換模型也計入這兩輪，不能藉換模型重設計數。
先根據實際失敗證據修正；只有使用者已選定並授權的替代模型、且宿主能套用時才換。
沒有替代模型時可在原模型預算內修正，預算用完就回報卡點。具體 must-fix / 測試失敗
閉環依 [`skills/failure-handling`](https://github.com/Lee-W/maigo/blob/main/skills/failure-handling/SKILL.md)，
不因模型較小放寬標準。Reviewer 已指定機械修法時，不自動升級。

續用 agent 能否更換模型也看當前工具 schema；若需新 agent，附原始任務與失敗證據。
[`skills/harness-discipline`](https://github.com/Lee-W/maigo/blob/main/skills/harness-discipline/SKILL.md)
在它適用的環境處理委派門檻；本 skill 處理模型選擇與能力不足時的角色執行方式。
