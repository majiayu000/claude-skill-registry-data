---
name: generate-code
description: >
  Generate TypeScript/Python code scaffolds from VDM-SL specifications.
  Triggered by "generate code from the spec", "convert to TypeScript", "generate Python code",
  "create a scaffold", "generate implementation template", "create type definitions from VDM",
  or "generate agent code".
  Also responds to Japanese: 「仕様からコードを生成して」「TypeScriptに変換して」等。
  Generates runtime verification code for pre-conditions, post-conditions, and invariants.
metadata:
  version: "0.4.0"
---

# Code Generation from VDM-SL Specifications

Read VDM-SL specifications (types, functions, operations, invariants) and generate
TypeScript or Python implementation scaffolds. Includes runtime verification (pre/post/inv checks).

VDM-SL仕様を読み取り、TypeScript/Pythonの実装スキャフォールドを生成する。
ランタイム検証（pre/post/inv チェック）も含める。

## Generation Flow

### Step 1: Read the Specification File

Read the `.vdmsl` file specified by the user.
If no file is specified, search for `.vdmsl` files in the workspace.

ユーザーが指定した `.vdmsl` ファイルを読み取る。指定がなければワークスペース内を探索。

### Step 2: Confirm Target Language

If the user hasn't specified, ask with AskUserQuestion:
- TypeScript
- Python
- Both

ユーザーが明示しない場合、AskUserQuestionで確認する。

### Step 2.5: Check for Model Routing (optional, token saving)

If a `model-routing.json` (produced by the `route-models` skill) exists next to the spec file:

- Process each module as a **separate subagent with the module's assigned model**
  (Claude Code: the Task tool's `model` parameter). Read the tier → model mapping
  from the routing file — never hard-code model names.
- Modules not listed in the file use `defaults.tier`.
- Verification is unchanged: generated code must pass the same gates as without
  routing. If a module's output fails its gate twice, escalate one tier,
  regenerate, append to `escalation.history`, and add the same row to the
  "Escalations" section of `MODEL-ROUTING.md`
  (see the `route-models` skill, `references/routing-rules.md`).
- If the runtime does not support per-subagent model selection, present the
  routing table as a recommendation and continue normally. Never fail the phase
  because routing is unavailable.

仕様ファイルの隣に `model-routing.json`（`route-models` スキルの成果物）があれば、
モジュールごとに割り当てモデルのサブエージェントで生成する（層→モデル対応は必ず
ファイルから読む）。検証はルーティング無しのときと同一で、同一モジュールが2回
失敗したら1層上げて再生成し、escalation.history と MODEL-ROUTING.md の両方に追記する。モデル指定が使えない環境では
推奨表の提示に留め、通常どおり進める。

### Step 3: VDM-SL → Code Conversion

Follow the conversion rules in `references/typescript-rules.md` or `references/python-rules.md`.

`references/typescript-rules.md` または `references/python-rules.md` の変換ルールに従う。

Generated file structure:

**TypeScript:**
```
generated/
├── types.ts          -- Type definitions (interface/type)
├── contracts.ts      -- Pre/post/invariant verification functions
├── <module>.ts       -- Function/operation implementation scaffolds
└── index.ts          -- Exports
```

**Python:**
```
generated/
├── types.py          -- Type definitions (dataclass)
├── contracts.py      -- Pre/post/invariant verification functions
├── <module>.py       -- Function/operation implementation scaffolds
└── __init__.py       -- Exports
```

### Step 4: Type Conversion

Convert VDM-SL types to target language types. See references for detailed rules.

VDM-SL型をターゲット言語の型に変換する。変換ルールの詳細はリファレンス参照。

Core mapping:

| VDM-SL | TypeScript | Python |
|--------|-----------|--------|
| `nat`, `nat1`, `int` | `number` | `int` |
| `real` | `number` | `float` |
| `bool` | `boolean` | `bool` |
| `seq of char` | `string` | `str` |
| `seq of T` | `T[]` | `list[T]` |
| `set of T` | `Set<T>` | `set[T]` |
| `map K to V` | `Map<K, V>` | `dict[K, V]` |
| Record type | `interface` | `@dataclass` |
| `[T]` (option) | `T \| null` | `Optional[T]` |
| Union type | union type | `Union[...]` |

### Step 5: Generate Contract Verification Code

Generate runtime check functions for invariants, pre-conditions, and post-conditions.

不変条件・事前条件・事後条件をランタイムチェック関数として生成する。

**Policy:**
- Invariants → factory functions or validation functions for types
- Pre-conditions → assert/raise at function entry
- Post-conditions → assert/raise at function exit (debug mode)
- Toggle verification on/off with environment variable `VDM_CONTRACT_CHECK`

### Step 6: Generate Function/Operation Scaffolds

**Explicit definitions** → convert implementation where possible
**Implicit definitions (pre/post only)** → generate stubs with `TODO` comments

明示的定義 → 可能な範囲で実装を変換。暗黙的定義 → `TODO`付きスタブを生成。

```typescript
// VDM-SL: findUser(uid, users) == users(uid) pre uid in set dom users
function findUser(uid: UserId, users: Map<UserId, User>): User {
  // Pre-condition check
  assert(users.has(uid), `Pre-condition failed: uid ${uid} not in users`);

  // Implementation
  const result = users.get(uid)!;

  return result;
}
```

### Step 7: Output Files

Place generated code in a `generated/` subfolder in the same directory as the spec file.
If files already exist, ask the user for overwrite confirmation.

生成したコードを仕様ファイルと同じディレクトリの `generated/` に配置する。

## Generated Code Quality Guidelines

- Generated code should be **immediately runnable** (no compilation errors)
- Mark locations requiring manual implementation with `TODO` comments
- Include the original VDM-SL definition in JSDoc / docstrings
- Contract violation error messages should be specific (which condition failed, with what value)

生成コードはそのまま動作可能な状態を目指す。`TODO`で手動実装箇所を明示。
JSDoc/docstringで元のVDM-SL定義を記載。エラーメッセージは具体的に。

## Handling Unconvertible Syntax

The following constructs cannot be generated and should be noted with `TODO` comments:

以下はコード生成を断念し `TODO` コメントで注記する:

- `exists` / `exists1` quantifiers → describe semantics in comments
- Pattern match exhaustiveness guarantees → suggest type guards only
- Map comprehension `{k |-> v | ...}` → convert to loop construction or `TODO`
- Auto-insertion of state invariants → recommend hooks on state-changing methods

## Detailed References

- `references/typescript-rules.md` — Complete TypeScript conversion rules
- `references/python-rules.md` — Complete Python conversion rules
