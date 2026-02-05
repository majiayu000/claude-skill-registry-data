---
name: decision-checklist
description: 設計決定前に確認すべき観点をチェックする
metadata:
  short-description: 設計判断チェック
---

# decision-checklist

この skill は、設計を確定してよいかを判断するためのチェックを行う。  
ファイルの編集や追加、削除などは行わない。

## 確認項目

- 破壊的変更を含むか
- 将来の拡張（TTS追加・設定拡張）を阻害しないか
- contracts を正とする設計になっているか
- bot と api の責務が明確に分離されているか
- 実装コストと得られる価値は釣り合っているか

## 出力

- 各項目に対する簡潔な評価
- 懸念点があれば列挙
