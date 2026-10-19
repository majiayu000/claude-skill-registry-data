---
name: pr-context-cache
description: This skill should be used during /maigo:review to persist current PR context (title / body / diff / CI status / linked issues / discussion) in the rubric. Refresh PR sources on every review; reuse unchanged local branch or range context.
---

<!-- mkdocs-include-start -->

# PR Context Cache

**Owner Agent**: Raana
**Consumers**: [`/maigo:review`](https://github.com/Lee-W/maigo/blob/main/commands/review.md) step 1

## Why this skill exists

`/maigo:review` 的第一步是 🐱 Raana 抓 context，保存到本次 review rubric 檔開頭的機讀
區段，讓後續角色讀同一份資料。PR 的 CI、留言、thread 狀態與 body 可在 diff 沒變時更新，
因此 **PR 每次重新抓取**；只有本地 branch／range 在同 source 且 diff sha 未變時還原快取。
**rubric 檔路徑不再固定**：省略 `--rubric` 時 script 會依 source
呼叫 [`scripts/artifact_path.py`](https://github.com/Lee-W/maigo/blob/main/scripts/artifact_path.py)
算出 `.maigo/review/<id>/rubric.md`（分目錄前的扁平 `.maigo/review-rubric-<id>.md`
只在新路徑沒有 cache 時當唯讀退路，永遠不寫；歸屬規則見
[`artifact-ownership`](https://github.com/Lee-W/maigo/blob/main/skills/harness-discipline/references/artifact-ownership.md)）。

## 怎麼跑

機械流程由 script 代勞（cache 偵測 / 驗證 / fetch / truncate / 寫檔一條龍）：

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/pr_context_cache.py" <source> \
    [--rubric PATH] [--base main]
```

- `<source>`：GitHub PR URL / PR 編號（需要 gh CLI）、本地 branch 名、或 commit range
- 在 maigo repo 自身工作時，直接 `python3 scripts/pr_context_cache.py` 即可
- 省略 `--rubric` 是預設用法——script 自動算路徑；只有需要覆寫既有檔案時才傳 `--rubric`

stdout 第一行是 `cache_hit: true|false`，第二行 `rubric: <path>`，其後是 cache 區段全文——
含 Source / PR number / Title / Reviewed head（本次 PR commit SHA）/ Body（截 500 行）/ Linked issues / CI status /
Diff stat / **Review threads（inline review thread，含 resolve 狀態）/ Review
summaries（`gh pr view --json reviews`）/ Conversation comments（`gh pr view
--json comments`）** / Diff sha / Full diff（截 2000 行）。

Review threads / summaries / comments 只在 `<source>` 是 PR 時抓（branch / range
diff 沒有對應的 GitHub review thread 可抓）。**未解決（`[OPEN]`）的 thread 在輸出
裡會被特別標出**——下結論前先檢查這些 thread 對照目前 diff 是否已經處理，
避免漏看 reviewer 留下但尚未收斂的架構意見（真實事故：只抓 diff + PR body +
reviewDecision，漏看某 PR 上一位 reviewer 對 `isinstance`-based type-switch 設計
留下的 OPEN thread，直到使用者問「有沒有看 TP 說了什麼」才補回）。

## 行為摘要

- **PR** → 每次抓取並保存目前的全部 context，`cache_hit: false`。以 `gh pr view` 回傳的 canonical URL／number 統一後續 diff、CI 與 threads 的目標；threads 不取目前 cwd 的 repo，diff stat 使用 additions／deletions／changedFiles metadata。每輪只抓一次 PR diff。
- **本地 cache hit**（branch／range、Source 相同且 diff sha256 未變）→ 印出快取區段。
- **本地 cache miss** 或 PR 刷新 → 寫回 rubric 開頭
  `<!-- pr-context-cache:start v1 -->` … `<!-- pr-context-cache:end -->` 區段
  （無檔案 → 建立；無區段 → prepend；有舊區段 → 整段取代）

PR 的舊扁平快取不當成即時資料；刷新後寫到新路徑，舊檔保持不變。`Fetched at` 是本次 snapshot 的時間，不能拿前一輪的時間宣稱已刷新。
它也不是最後 review 時間；review 完成後由 `review_report.py publish` 另記 `reviewed_at`，
並把這裡的 `Reviewed head` 寫入 report，供 board 判斷 PR 是否已更新。

## Fallback

script 跑不起來（找不到路徑、無 gh CLI、git 失敗 → exit 1 + stderr；或路徑歸屬衝突
`status: conflict` → exit 3，見 artifact-ownership）→ Raana 回退手動抓：依
`/maigo:review` step 1 列的 `gh pr view / gh pr diff / gh pr checks`
（或 `git diff` / `git log`）指令直接 fetch，不寫 cache。

## What this skill does NOT cover

- 讀 review rubric 檔其餘內容（rubric 本身由 Tomori 撰寫）
- 評估 diff 是否有問題（那是 Soyo 的工作）
- 決定要 review 哪個 target（caller 傳進來）
- 非 review 流程的 PR context 抓取（如 `/maigo:describe-pr` 不走這個 skill）
