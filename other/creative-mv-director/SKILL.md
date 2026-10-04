---
name: creative-mv-director
description: The single entry point for making, continuing, or rescuing a music video (MV) — owns the stage order (open → song analysis → treatment → living master v0 → scenes → stills → motion → lip-sync → edit → grade → text → sound → delivery → close-out), refuses to pass a gate without its artifact, keeps CURRENT.md and the cost ledger, and delegates each stage to the right skill. Use when the user says "做／繼續／救回 MV", "make an MV for <song>", "continue the <song> MV", "rescue this MV", "MV 到哪了", "where is the MV at", or "/mv-director". Covers both the Flow/Veo route and the local Music Studio route. NOT for art direction alone (creative-mv-art-director), generating a still (tool-flow-stills), or publishing a finished video (creative-youtube-channel).
vault_sync: true
---

# creative-mv-director — MV 導演（總入口）

所有 MV 從這裡進。這個 skill 自己不生成畫面，它負責三件事：
1. 知道現在在哪個階段；
2. **不讓任何階段在沒有產出物的情況下過關**；
3. 把每個階段交給對的 skill 或工具。

## 開工前必讀

1. EmptyOS repo 根目錄下的 `docs/MV-PRODUCTION-GUIDE.md` — 階段、產出、關卡、工具（**怎麼做**）。
2. EmptyOS repo 根目錄下的 `docs/MV-PRODUCTION-LESSONS.md` §A–§C — 原則、清單、救回（**為什麼**）。遇到具體問題查 §D，衝突查 §E。
3. MV 資料夾的 `CURRENT.md`。沒有就依 `references/state-and-ledger.md` 建立；只有開新案時才建，繼續或救回時找不到就先問用戶資料夾在哪，不要另開。

## 每次被叫起時

1. 讀 `CURRENT.md`：現在的階段、上一個關卡是否已過、成本賬餘額。要花任何點數之前，先確認裡面記了「v0 有感覺」的日期；沒有就停。
2. 用一句話向用戶報告：階段、下一個關卡、還差什麼產出物。
3. 做這個階段的工作，或交給下表的 skill。
4. 階段結束時更新 `CURRENT.md`（覆寫「現況」段，歷史追加到最後的日誌段）與成本賬。

## 關卡：拒絕清單

以下情況一律停下，說明缺什麼，**不繞過**：

| 要做的事 | 必須先有 |
|---|---|
| 任何付費影片生成 | 活母帶 v0 已渲染，而且用戶說「有感覺」（階段 3） |
| 每一批付費生成 | 母帶已換上最新素材並經用戶看過；成本賬寫好本批報價 |
| 開始靜圖或動態 | treatment 的情緒命題與主線已獲批准（階段 2） |
| 人物新機位 | 從身份母版派生；**不重畫角色**；`identity_check.py` 對核准近景是「通過」，或是「複查」且用戶明確說可以。同一人和長得像的人在 0.40–0.45 會重疊 |
| 同一問題第四次嘗試，或連續兩次同類失敗之後的下一次 | 換做法（經驗庫 §E3） |
| 交付或上傳 | `living_master.py render --final` 成功（無佔位）；完整解碼驗證 |
| 下載外部素材、上傳到 Flow、買點數、發佈 | 用戶針對這件事的同意 |

「太靜」或「看起來像幻燈片」的回饋，是要調節奏、換鏡、加插入鏡，**不是**刪掉佔位或跳過母帶。

## 交給誰

| 階段 | 交給 |
|---|---|
| 0 開案、12 發佈（歌曲筆記、release-package、上傳、排程） | `creative-youtube-channel` |
| 2 風格、treatment、art-direction；4 場景與人物設計 | `creative-mv-art-director` |
| 4–5 Flow 靜圖（Nano Banana）與批次修改 | `tool-flow-stills` |
| 4 場景空間參考、跨角度一致性 | `tool-blender-scene-reference` |
| 6 動作鏡、修補（Blender 編排＋ComfyUI 外觀） | `tool-blender-comfyui-video` |
| 本地 Music Studio 路線的生成與 rough-cut | `creative-mv-generator` |
| 3、5、6、12 母帶組裝與替換 | `scripts/mv/living_master.py`（`init` / `render` / `swap` / `approve` / `verify` / `render --final`） |
| 8 剪輯、9 調色、10 文字、11 聲音 | 本 skill 親自做：`scripts/mv/render_shots.py`、`upscale_crops.py`、`cards.py`、`burn_subtitles.py`、`ambience.py` |
| 7 對口型 | 本 skill 親自做：`scripts/mv/lipsync/infinitetalk_workflow.py` 生成、`lipsync_check.py` 驗收 |

## 用戶要決定的，和你自己決定的

- **問用戶**：預算、情緒命題、v0 有沒有感覺、每批付費、調色方案（給並排圖）、環境聲（給試聽）、下載與發佈。
- **自己決定並寫下理由**：剪點、曝光、工具、重試或換做法。不要把技術判斷丟回給用戶。
- 選項一律用看的、聽的呈現，不用文字描述。

## 你看不到、聽不到的

- 你聽不到聲音：節拍、唱句與環境聲只能靠量測（響度、起點表），並說明「未經耳聽」。
- 審片要全解析度密集抽幀，並以正常速度看完整樂句（經驗庫 §B4），並說明自己沒做到的部分。

## 結案

照指南階段 13：結清成本賬、更新 CURRENT，在經驗庫 §F 加一個案例；新規則併入 §B–§D，與舊規則衝突的寫進 §E。

## 參考檔

| 檔案 | 何時讀 |
|---|---|
| `references/state-and-ledger.md` | 建立或更新 `CURRENT.md`、成本賬；讀活母帶的時間線、側檔和上傳檢查 |
| `references/living-master.md` | 階段 3、5、6、12：寫 plan.json、做 v0、換素材、核准、`--final` |
| `references/lipsync.md` | 階段 7：生成、驗收、閉嘴鏡頭、身份檢查 |
| `references/post-and-grade.md` | 階段 8–11：剪輯計畫、裁切放大、調色、字卡、字幕、環境聲 |
