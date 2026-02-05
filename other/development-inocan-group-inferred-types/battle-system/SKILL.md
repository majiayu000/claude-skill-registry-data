---
name: battle-system
description: バトルシステムの設計と実装ガイド。バトル関連の変更時に参照。
---

# Battle System

## 構成

```
BattleService（エントリーポイント）
    ↓
BattleTurnEngine（ターン処理）
    ↓
BattleContext（戦闘状態コンテナ）
```

## ファイル構成

BattleTurnEngineは責務ごとに拡張ファイルに分割:

| ファイル | 責務 |
|---------|------|
| `BattleTurnEngine.swift` | エントリーポイント |
| `+TurnLoop.swift` | ターンループ制御 |
| `+PhysicalAttack.swift` | 物理攻撃 |
| `+Magic.swift` | 魔法攻撃・回復 |
| `+Damage.swift` | ダメージ計算 |
| `+StatusEffects.swift` | 状態異常 |
| `+Reactions.swift` | 反撃・パリィ |
| `+Targeting.swift` | ターゲット選択 |
| `+TurnEnd.swift` | ターン終了処理 |
| `+Logging.swift` | ログ出力 |

## 設計方針

### BattleContext

戦闘ごとに独立したインスタンスを生成。並行実行でも安全。

- 参照データ（不変）: マスターデータへの参照
- 戦闘状態（可変）: プレイヤー、敵、ターン数など

### 新機能追加時のルール

1. **状態はBattleContextに持たせる** - 静的変数禁止
2. **乱数はcontext.randomを使う** - 再現性確保
3. **ログはcontext.appendAction()で記録**
4. **関連処理は適切な拡張ファイルに追加**
