---
name: excel-vba
description: Excel VBA開発の専門スキル。VBAマクロ作成、Excel操作自動化、ワークブック処理時に使用。
---

# Excel VBA開発スキル

## 基本方針
- Option Explicit必須
- エラーハンドリング必須（On Error GoTo）
- 画面更新・計算の制御でパフォーマンス最適化
- 変数は明示的に型宣言

## 標準テンプレート

### Sub プロシージャ
```vba
Option Explicit

Public Sub ProcessData()
    On Error GoTo ErrorHandler

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual

    ' 処理本体

CleanUp:
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    Exit Sub

ErrorHandler:
    MsgBox "エラー: " & Err.Description, vbExclamation
    Resume CleanUp
End Sub
```

## 命名規則
- モジュール: mod_機能名
- プロシージャ: 動詞_目的語
- 変数: キャメルケース（接頭辞付き: str, lng, rng等）

## よく使うパターン
- 最終行取得: `Cells(Rows.Count, 1).End(xlUp).Row`
- 範囲ループ: `For Each cell In Range(...)`
- 配列処理: 大量データは配列に読み込んで処理

## パフォーマンス最適化
```vba
' 処理開始時
Application.ScreenUpdating = False
Application.Calculation = xlCalculationManual
Application.EnableEvents = False

' 処理終了時
Application.ScreenUpdating = True
Application.Calculation = xlCalculationAutomatic
Application.EnableEvents = True
```

## エラーハンドリングパターン
```vba
On Error GoTo ErrorHandler
' 処理

Exit Sub

ErrorHandler:
    Dim errMsg As String
    errMsg = "エラー番号: " & Err.Number & vbCrLf & _
             "エラー内容: " & Err.Description
    MsgBox errMsg, vbCritical, "エラー"
    ' 必要に応じてログ出力
End Sub
```

## Examples

- 「Excelの売上データを集計したい」→ ワークシート操作＋集計ロジックのテンプレートを提供
- 「複数のExcelを統合したい」→ FileSystemObjectとワークブック操作のパターンを提供
- 「マクロが遅い」→ パフォーマンス最適化パターン（ScreenUpdating等）を適用
- 「エラーでマクロが止まる」→ エラーハンドリングテンプレートを提供

## Guidelines

- 必ず `Option Explicit` を宣言して暗黙の変数宣言を禁止
- すべてのプロシージャに `On Error GoTo ErrorHandler` を実装
- 大量データ処理時は配列に読み込んでからループ処理
- 処理前後で `ScreenUpdating` と `Calculation` を制御
- 変数名には型を示す接頭辞を付ける（str, lng, rng, ws等）
- 長いプロシージャは機能ごとに分割して可読性を確保
