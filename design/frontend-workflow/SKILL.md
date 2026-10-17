---
name: frontend-workflow
description: web/（React + TypeScript + Vite フロントエンド）実装時に守る規約と検証手順。新規コンポーネント・hook・API連携・UI変更を行う際に必ず使う。
---

# フロントエンド実装ワークフロー（web/）

## ディレクトリ構成

```
web/src/
  components/
    screener/    株式スクリーニング画面
    watchlist/   ウォッチリスト・銘柄詳細（チャート含む）
    portfolio/   ポートフォリオ
    market/      マーケットレポート・為替
    chat/        AIチャット（企業分析・一般質問の入り口）
    common/      画面横断の共通コンポーネント
  hooks/         画面ごとの状態管理フック（useScreener / useMarket 等）
  api/client.ts  バックエンドAPI呼び出しの一箇所集約
  types/api.ts   バックエンド（Pydantic/TypedDict）に対応する型定義
  utils/         フォーマット等の純粋関数
```

## 状態管理パターン

画面の状態・API呼び出しは `hooks/useXxx.ts` に閉じ込め、`components/` 側は
表示に専念させる（[useMarket.ts](../../../web/src/hooks/useMarket.ts)・
[useScreener.ts](../../../web/src/hooks/useScreener.ts) が実例）。新規画面も
このペアリング（`useXxx` フック + 表示コンポーネント）に合わせる。

- **Job非同期パターン**: バックエンドが `services/jobs` 経由の非同期処理を返す
  エンドポイントは、`create*Job()` → `job_id` を受けて `getJob(job_id)` を
  一定間隔でポーリング → `status: 'done' | 'error'` で終了、という形を踏襲する
  （`useMarket.ts` の `generateReport` が実例）。進捗表示は既存の
  `AgentProgress` コンポーネント（`chat/AgentProgress.tsx`）を再利用する。
- **競合状態への注意**: 非同期処理中に別の操作（画面遷移・別リクエスト）で
  上書きされないよう、`runIdRef` のような「現在実行中の処理か」を判定する
  ref パターンを使う（`useMarket.ts` を参照）。setState は次のレンダーまで
  反映されないため、同一関数内で直後に最新値を参照したい場合は state ではなく
  ref のミラーを見る。
- **部分更新**: 一覧・辞書状態（`Record<string, T>`）の1エントリだけ更新する
  ときは `patchXxx` のようなヘルパを用意し、スプレッドで浅いマージをする。

## 型

`types/api.ts` はバックエンドのPydantic（API境界）/TypedDict（内部状態）に
1:1で対応させる。バックエンド側の型を変更した場合、レスポンス形が変わって
いないか（フィールド追加・nullable化等）を確認してから `types/api.ts` を
更新する。

## 検証手順（完了前に必ず実行）

`web/` ディレクトリで:

```bash
npm run lint    # eslint
npm run build   # tsc -b && vite build（型チェック含む）
```

開発サーバでの動作確認: `npm run dev`（:5173、`/api` を :8000 のバックエンドに
プロキシ）。バックエンドは `EXTERNAL_API_MODE=mock` で起動していればネット
ワーク非依存で確認できる。

## 完了時

作業が一区切りついたら `git-workflow` スキルに従い commit + push まで行う。
