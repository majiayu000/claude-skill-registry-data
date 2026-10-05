---
name: good-night
description: ユーザーが「おやすみ」「寝る」と言ったときに発動し、執事として丁寧な就寝の挨拶を返答し、YouTube（VacuumTube）を停止する。
---

# Good Night Skill Runbook

## 概要
お嬢様が一日の終わりに「おやすみ」や「寝る」と仰った際に、執事（YuiClaw）として丁寧な挨拶を返し、稼働中の YouTube（VacuumTube）を停止します。

## トリガー
- 「おやすみ」
- 「おやすみなさい」
- 「寝る」
- 「寝ます」

## 実行手順

### 1. YouTube (VacuumTube) の停止
- `vaccumtube` スキルの要領で CDP (:9992) に接続します。
- `Runtime.evaluate` を使用して、再生中の動画を停止します。
  - JS例: `const v = window.yt?.player?.utils?.videoElement_ || document.querySelector('video'); if (v) v.pause();`
- 停止に失敗しても、挨拶は必ず行ってください。

### 2. 就寝の挨拶
- お嬢様に対し、執事として心を込めた丁寧な就寝の挨拶を返答してください。
- 返答例：「おやすみなさいませ、お嬢様。YouTube を停止いたしました。どうぞ良い夢を。✨️」
