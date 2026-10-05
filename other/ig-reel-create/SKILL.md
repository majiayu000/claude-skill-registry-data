---
name: ig-reel-create
description: 過去問パックのカルーセル PNG をベースに 1080×1920 縦型 IG Reels mp4 を生成。Satori で reels サイズの PNG 10 枚再生成 → VOICEVOX TTS → ffmpeg 連結まで自動化。
allowed-tools: Bash, Read, Write
domain: sns
---

# Instagram Reels 自動生成スキル

`content/sns/instagram/{exam}/exam-packs/<year>/pack-<NN>/slide-data.json` を入力に、**1080×1920 縦型 60-120 秒の IG Reels 動画を完全機械生成**する。

## 人物・見出しと既存投稿の改修

制作・改修の前に [SNS 投稿画像ポリシー §0・§0.1](../../../knowledge/reference/sns-image-policy.md) を読む。先生キャラクター＋短い極太見出しを媒体別に構成し、既存レンダラーの未対応箇所は実装して代表 1 件を画像確認してから展開する。文字を編集可能な元データとして保持する。

再生成は外部の予約・公開投稿を自動更新しない。動画冒頭を改修する未投稿パックはカバーと動画派生物を揃える。公開済みサムネだけの変更は §0.1 に従い、動画本体の更新と区別する。

## 前提

1. **ffmpeg / ffprobe が PATH にある**
   ```bash
   ffmpeg -version
   ```
2. **VOICEVOX エンジンがローカル起動している**
   ```bash
   docker run --rm -p 50021:50021 voicevox/voicevox_engine:cpu-latest
   curl http://localhost:50021/version
   ```
3. **対象パックの slide-data.json が新スキーマ**（optionExplanations + pointText 必須）

## 使い方

```bash
# 技術士総監（既定）
node .claude/skills/social/ig-reel-create/scripts/ig-reel-create.mjs \
  --exam r07-pack-01

# 技術士第一次試験
node .claude/skills/social/ig-reel-create/scripts/ig-reel-create.mjs \
  --exam-dir pe-first-stage --exam r07-pack-01

# 1級土木（令和7年度）
node .claude/skills/social/ig-reel-create/scripts/ig-reel-create.mjs \
  --exam-dir 1級土木 --exam r07-pack-01 --skip-png

# 2級土木（令和7年度 後期=k / 前期=z）
node .claude/skills/social/ig-reel-create/scripts/ig-reel-create.mjs \
  --exam-dir 2級土木 --exam r07k-pack-01 --skip-png
```

### 引数

| 引数 | 必須 | 既定 | 説明 |
|---|---|---|---|
| `--exam` | ✅ | - | パック ID（例: `r07-pack-01`）。2級土木は年度に前期/後期の接尾辞が付く（`r07z`=前期 / `r07k`=後期、例: `r07k-pack-01`） |
| `--exam-dir` | - | 技術士総監 | 試験軸（`pe-first-stage` / `1級土木` / `2級土木` 等）。資格ごとの `content/sns/instagram/<exam>/exam-packs/<year>/` を参照 |
| `--speaker` | - | 1（四国めたん） | VOICEVOX speaker ID |
| `--skip-png` | - | false | PNG 再生成をスキップ（既存 reels/img/*.png を使う）。既存 PNG が 1080×1920 ならこれを付けて Satori 再生成を回避 |
| `--audio-only` | - | false | `script.txt` と `reels/wav/*.wav` まで生成して終了。推奨の1問1リールをJIT生成する前処理 |
| `--problem-pause` | - | 3 | problem スライド読み上げ後に挿入する無音秒数（考える間）。`0` で無効 |

> [!warning]
> **カバー/テンプレ刷新時は `--skip-png` を付けない。** カバーPNGテンプレ（`exam-cover-ig`）や 09-cta テンプレを更新した後は、PNG から再生成しないと旧テンプレが動画に残る。`--skip-png` は「PNG が現行テンプレと一致している」と確信できる時だけ使う。カバーPNGだけ別途更新して動画を再生成しない運用は **desync を生むため禁止**（`yt-shorts-create` の `assertCoverInSync` ガードが派生時に SSIM<0.90 で検知・中断する）。

> **コミット方針**: `reels/script.txt` と `caption.txt` のみコミット。`video.mp4` / `wav/` / `slide-NN.mp4` / `_combined.mp4` / `_empty.ass` / `concat.txt` は再生成可能な派生物で `.gitignore` 済み。wav は Google Drive vault 退避（`npm run drive-vault-sync -- --group sns-archived-media --commit`、取り戻しは `--pull`）、手元に無ければ script.txt から VOICEVOX で再生成（真実源 `.claude/knowledge/reference/sns-archive-policy.md`）。

## 出力

```
content/sns/instagram/{exam}/exam-packs/<year>/pack-<NN>/reels/
├ video.mp4              最終動画（IG Reels として upload 可能）
├ img/{00..09}.png       1080×1920 各スライド PNG（中間ファイル）
├ wav/slide-NN.wav       各スライドの TTS 音声（中間ファイル）
└ script.txt             読み上げ台本（デバッグ用）
```

## 工程

1. VOICEVOX / ffmpeg の利用可能チェック
2. slide-data.json 読み込み（10 slides: cover/problem×4/answer×4/cta）
3. PNG 10 枚を `--size reels` で再生成（既存 ig-post-create.mjs 流用）
4. 各スライドの台本生成（cover/problem/answer/cta 型別）
5. VOICEVOX で WAV 10 個生成
6. ffmpeg で連結 → mp4

## 台本テンプレート

| スライド | 台本 |
|---|---|
| **cover** | 技術士総監:「令和{年度}年度の択一式過去問、{N}番です。全 4 問、答えは動画内で発表します」／土木:「{令和\|平成}{年度}年度{前期\|後期}の第一次検定 過去問、{N}番です。全 4 問、答えは動画内で発表します」（Reels は自動再生のため「スワイプ」表現は使わない → [ig-reels-policy.md](../../../../.claude/knowledge/reference/ig-reels-policy.md)） |
| **problem** | 「問題{N}。{bodyLines}」 |
| **answer** | 「正答は{N}番。{correctText}。{pointText}」 |
| **cta** | 「フォローすると毎週、過去問解説が届きます。全問解説はドボクノートでチェック」（Reels はリーチ獲得器のため保存より新規フォロー誘導を主にする → [ig-reels-policy.md](../../../../.claude/knowledge/reference/ig-reels-policy.md)） |

選択肢は読み上げない（時間制約のため、視聴者は画面で読む）。

## 時間目安

- cover: 約 6 秒
- problem: 約 12-15 秒（問題文の長さによる）
- answer: 約 10-12 秒（pointText の長さによる）
- cta: 約 6 秒
- **合計: 約 90-110 秒**（IG Reels の理想範囲 60-90 秒に近い）

## 関連スキル

- `ig-post-create`（カルーセル PNG 生成、本スキルが内部で利用）
- `yt-shorts-create`（YouTube Shorts、共通基盤 sns-common を共有）

## 担当外

- IG への自動投稿（手動アップロード前提。将来 `ig-reel-publish.mjs` で対応）
- BGM / 効果音（サイレント + TTS のみ）
- 字幕焼き込み（PNG にテキスト既存のため不要）
