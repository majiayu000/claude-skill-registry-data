---
name: knowledge
description: >
  過去の失敗・設計判断・バグ解決の教訓をナレッジベースに参照・追記する。
  Use when user asks to [ナレッジ参照, 失敗から学ぶ, 教訓を記録, 過去の判断を調べる, /knowledge, ナレッジを追加].
domain: ops
---

過去の失敗と学びを参照・追記する。

## 使い方

- **参照**: 以下のナレッジから、現在の作業に関連するパターンがないか確認する
- **追記**: バグ解決や設計判断の教訓があれば、このファイル末尾に以下の形式で追記する

```markdown
---

## タイトル（簡潔に）

**問題**: 何が起きたか
**原因**: なぜ起きたか
**対策**: どうすれば防げるか
```

---

## tsconfig パスエイリアス

**問題**: `paths` を設定しても `@/*` が解決されない。

**原因**: `baseUrl` が未設定。`paths` は `baseUrl` からの相対パスで解決される。

**対策**: `baseUrl: "."` と `paths: {"@/*": ["./src/*"]}` をセットで設定する。`apps/web/tsconfig.json` のパターンを参照。

---

## drizzle-kit generate のスナップショット衝突

**問題**: `drizzle-kit generate` で `prevId collision` エラー。

**原因**: 手動作成したスナップショットの `prevId` が自分自身を指していた（`0005_snapshot.json` の `prevId` が `0005` の `id` と同一）。

**対策**: `drizzle/meta/*_snapshot.json` の `prevId` が前のスナップショットの `id` を正しく指しているか確認する。

---

## drizzle-kit push / generate の対話プロンプト

**問題**: `drizzle-kit push` や `drizzle-kit generate` がカラム削除・リネーム時に対話プロンプトを出し、非対話環境（CI、Claude Code）で止まる。

**対策**: 手動でマイグレーション SQL を作成し、`better-sqlite3` で直接適用する。`packages/database/drizzle/0007_articles_refactor.sql` が実例。

---

## seed のローカルディレクトリ統一（解決済み）

**経緯**: ローカル `.local/r2/seed/` と R2 の `seeds/` で名称が不一致だった。`npm run r2:upload` でアップロードすると R2 に `seed/` キーで保存されてしまい混在した。

**解決**: ローカルディレクトリを `.local/r2/seeds/` に統一。`sync-download.ts` の DEFAULT_PREFIXES も `"seeds"` に変更。現在は `r2:upload` でも `seed:push` でもどちらも R2 の `seeds/` に正しくアップロードされる。

---

## 企業プロキシと R2 S3 API

**問題**: `@aws-sdk/client-s3` 経由の R2 アクセスが HTTP 407/503 で失敗する。

**対策**: `npx wrangler r2 object put/get` で個別操作する。`/push-r2` スキルがフォールバック手順を提供。タイミングによって S3 API が通ることもある。

---

## MDX frontmatter の YAML クォート不正

**問題**: ブログ記事の frontmatter で `title: "...「鉤括弧」..."` のように YAML 二重引用符内に別の二重引用符を含めると、YAML パーサーが途中で文字列終端と解釈して `Unexpected scalar at node end` エラーになる。

**原因**: YAML の二重引用符文字列内では `"` をエスケープ (`\"`) しないと構文エラーになる。`compileMDX({ parseFrontmatter: true })` が記事コンテンツの frontmatter を再パースする際に発生。

**対策**: frontmatter の値に `"` を含める場合は `\"` にエスケープするか、シングルクォート `'...'` で囲む。または値にコロン・引用符を含まない場合はクォートなしで記述する。`/write-blog-article` の品質チェックリストに追加済み。

---

## Bash で cd するとローカルデータのパスが解決できなくなる

**問題**: `cd packages/svg-builder` 等でサブディレクトリに移動した後、`.local/r2/blog/<slug>/data/` や `.local/d1/` への相対パスが解決できず「No such file or directory」になる。

**原因**: `.local/` はプロジェクトルート直下にあるため、サブディレクトリから相対パスで参照できない。Bash の作業ディレクトリは `cd` 後も維持される。

**対策**: Bash コマンドで `cd` を使わない。型チェック等は `npx tsc --noEmit -p apps/web/tsconfig.json` のようにプロジェクトルートから実行する。やむを得ず `cd` する場合は同一コマンド内で `cd /c/Users/m004195/stats47 &&` で戻す。

---

## マイグレーションファイルのジャーナル外管理による不整合

**問題**: `drizzle/` に手動で SQL ファイルを追加し、`meta/_journal.json` に登録せずに運用した結果、ジャーナルは 7 件（0000〜0006）だが実ファイルは 20 本（0000〜0020）に乖離。削除済みテーブルの CREATE/DROP も混在し、新環境構築時に適用順序が不明になった。

**原因**: `drizzle-kit generate` の対話プロンプト回避のため、手書き SQL を `drizzle/` に直接配置した。ジャーナルはスナップショット 0006 で止まったまま、実際の DB スキーマだけが進んだ。

**対策**: (1) `drizzle/` には `drizzle-kit generate` の生成物のみ配置する（手動 SQL は `better-sqlite3` で直接適用）。(2) マイグレーションが 10 本を超えたら `/reset-migrations` でリセットする。(3) 詳細は `packages/database/README.md` の「マイグレーション運用ルール」を参照。

---

## 定数→DB 移行時のデータ消失

**問題**: アフィリエイトバナーを定数（`AFFILIATE_BANNERS`）から DB 管理に移行した際、定数を削除したが DB への INSERT を行わず、7件のバナーデータが消失した。

**原因**: 移行コミットでスキーマ変更とコード変更のみ実施し、既存データの移行（INSERT 文やシードデータ生成）を忘れた。

**対策**: 定数→DB 移行時は以下を必ず実施する: (1) 既存の定数データを INSERT 文に変換してローカル D1 に投入 (2) `--dry-run` 等で行数を確認 (3) 定数の削除は INSERT 確認後に行う。

---

## MDX で太字がリンクの外側にあるとパースされない

**問題**: `**[環境基本法第15条](url)**` と書くと、`**` がそのまま表示されボールドにならない。

**原因**: MDX v3 のパーサーは `**` で囲まれた範囲にリンク構文が含まれると、正しく強調としてパースできない場合がある。

**対策**: 太字はリンクテキストの内側に置く: `[**環境基本法第15条**](url)`。`/check-mdx --rules syntax` のチェック項目6に検出パターンを追加済み。

---

## ローマ数字がアンカーIDから除去される

**問題**: 見出し `## Ⅰ-1-40` へのアンカー `#ⅰ-1-40` が機能しない。48ファイルで一括修正が必要になった。

**原因**: `generateHeadingId()` の正規表現 `[^\w\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF\u3400-\u4DBF\s-]` がローマ数字（U+2160 Ⅰ / U+2170 ⅰ）を許可文字に含めていないため、ID生成時に除去される。`Ⅰ-1-40` → `1-40` になる。

**対策**: アンカーリンクではローマ数字を含めず `#1-40` の形式で記述する。`/check-mdx --rules syntax` のチェック項目6 および `/keyword-page` SKILL.md に記載済み。


---

## MDX 太字範囲内の鉤括弧でパースが崩れる

**問題**: `**「地球の3つの危機」**` のように太字範囲内に鉤括弧があると、 がそのまま表示されボールドにならない。

**原因**: MDX v3 のパーサが  と「」の組み合わせで強調の開始・終了を正しく認識できない場合がある。

**対策**: 鉤括弧を太字の外に出す「**text**」、または鉤括弧を除去する。 のチェック項目6に追加済み。

---

## SNS生成バイナリは「アーカイブ・作業セット・一時物」を分離する

**問題**: Instagram Reels・YouTube 動画を全件生成すると、gitignore 済みでもローカルに mp4 / wav / PNG と
VOICEVOX のダウンロードキャッシュが残り、空き容量を数 GiB 単位で消費した。gitignore は Git への混入を
防ぐだけで、ローカル実体を片付けない。

**原因**: 完成成果物、近日投稿に必要な作業セット、再生成可能な一時キャッシュを同じ「動画素材」として扱い、
退避後の自動復元とクラウド到達確認が無いままローカルへ全件常備していた。Google Drive のストリーミング
マウントを `--verify --deep` で順次読むと、cloud-only ファイルの取得待ちで全件照合が極端に遅くなることもある。

**対策**: (1) 人と手元スクリプトだけが使う完成物は Drive 台帳へ登録し、初回移行は
`drive-vault-sync --verify --deep --cloud` で台帳・実体・Drive APIを全件照合する、(2) 日常削除は
`instagram-reels:prune -- --cloud` / `youtube-renders:prune -- --cloud` で Drive API の MD5/bytes と
ローカル sha256 を照合し、予約済み・公開済み・予約窓外だけを削除する、(3) 公開時は対象だけ自動復元する、
(4) `.tmp/sns` / `.tmp/yt-gen` / VOICEVOX installer は Drive へ保存せず、プロセス停止と再生成経路を確認して
削除する。削除判定は fail-closed とし、`tests/video-cache-prune.test.mjs` で「照合不足なら削除しない」
「QA待ち通常動画は保持」を固定する。
