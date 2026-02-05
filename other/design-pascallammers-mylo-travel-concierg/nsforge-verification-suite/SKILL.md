---
name: nsforge-verification-suite
description: 驗證工具組合。觸發詞：驗證, verify, check, 維度, dimension。
---

# 驗證工具 Skill

> **⚠️ 驗證後必須向用戶展示結果！**
> - 驗證成功/失敗都要清楚告知用戶
> - 維度分析結果要用人類可讀格式展示

## 工具速查

| 驗證類型 | 工具 | 參數 |
|----------|------|------|
| 符號等價 | `symbolic_equal(expr1, expr2)` | 兩表達式 |
| 導數驗證 | `verify_derivative(original, claimed, var)` | 原式、宣稱導數、變數 |
| 積分驗證 | `verify_integral(original, claimed, var)` | 被積函數、宣稱積分、變數 |
| 解驗證 | `verify_solution(equation, solution, var)` | 方程、解、變數 |
| 維度分析 | `check_dimensions(expr, units_map)` | 表達式、單位映射 |

## 調用範例

```python
# 符號等價
symbolic_equal("(x+1)**2", "x**2 + 2*x + 1")  # → True

# 導數驗證：d/dx[ln(x²)] = 2/x ?
verify_derivative("ln(x**2)", "2/x", "x")  # → correct: True

# 積分驗證：∫sin(x)dx = -cos(x) ?
verify_integral("sin(x)", "-cos(x)", "x")  # → correct: True

# 解驗證：x=2 是 x²-4=0 的解？
verify_solution("x**2 - 4", "2", "x")  # → correct: True

# 維度分析
check_dimensions("m * a", {"m": "kg", "a": "m/s**2"})
# → dimension: [mass]*[length]/[time]**2 = Force
```

## 常用單位映射

```python
# 力學
{"F": "N", "m": "kg", "a": "m/s**2", "v": "m/s", "t": "s"}

# 藥動學
{"C": "mg/L", "V": "L", "k": "1/h", "t": "h", "D": "mg"}

# 熱力學
{"T": "K", "E": "J", "R": "J/(mol*K)", "n": "mol"}
```

## 驗證順序建議

1. **維度分析** - 維度錯，結果必錯
2. **符號驗證** - 代數正確性
3. **數值抽樣** - 特殊情況
