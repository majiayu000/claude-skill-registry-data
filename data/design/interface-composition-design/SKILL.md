---
name: interface-composition-design
description: クラス設計やアーキテクチャリファクタリング時に使用。継承より合成を推奨。
---

# Interface-based Design

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] クラスを設計する?
- [ ] 継承 vs 合成の判断をする?
- [ ] 依存性注入を設計する?
- [ ] リファクタリングで構造改善する?

### 前提条件
- [ ] 変化する部分を特定したか?
- [ ] 依存関係を把握しているか?
- [ ] 単一責任の原則を確認したか?

### 禁止事項の確認
- [ ] 深い継承階層を作ろうとしていないか?
- [ ] 具象クラスに直接依存しようとしていないか?
- [ ] パラメータを追加し続けて爆発していないか?

---

## トリガー

- クラス設計時
- 継承 vs 合成の判断時
- 依存性注入設計時
- リファクタリングで構造改善時

---

## 🚨 鉄則

**実装を隠し、インターフェースのみ公開。合成で拡張。**

---

## 判断基準

### 1. パラメータ爆発していないか?

```typescript
// ❌ パラメータ追加し続ける
process(data, useA: boolean, useB: boolean, useC: boolean, ...)

// ✅ 実装クラスを追加
interface Processor { process(data): Result }
class ProcessorA implements Processor {}
class ProcessorB implements Processor {} // 新規追加
```

### 2. 継承 vs 合成

```typescript
// ❌ 深い継承
class A extends B extends C extends D

// ✅ 合成
class Service {
  constructor(
    private readonly processor: Processor,
    private readonly validator: Validator
  ) {}
}
```

---

## 依存性注入

```typescript
// インターフェースに依存
interface Repository {
  find(id: string): Promise<Entity>;
}

class Service {
  constructor(private readonly repo: Repository) {}
}

// テスト時はモック注入
const mockRepo: Repository = { find: async () => mockEntity };
new Service(mockRepo);
```

---

## 🚫 禁止事項まとめ

- 深い継承階層
- 具象クラスへの直接依存
- パラメータの無限追加
- インターフェースなしの設計
