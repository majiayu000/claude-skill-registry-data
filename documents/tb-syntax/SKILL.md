---
name: tb-syntax
description: Use when explaining or writing TBQ3 language syntax, including Params, Vars, Events, data types, variables, sequence variables, arrays, Map variables, control flow, operators, assignment, functions, and formula execution rules.
---

# TBQ3 语法基础

本 skill 只提供写 TB 代码所需的最小语法规则。详细文档入口见 `references/syntax-map.md`。

## 代码组织

- 常见结构为 `Params`、`Vars`、`Events`。
- 参数用于可配置输入，变量用于公式内部状态。
- 事件函数放在 `Events` 下，Bar 策略通常至少包含 `OnBar(ArrayRef<Integer> indexs)`。

## 命名和注释

- 变量、参数、函数名使用简短英文业务名。
- 给用户生成的 TB 代码注释使用中文，简明说明交易意图或关键边界。
- 不确定语法时，先查 `docs/TB语言基础` 或函数文档，不要发明语法。

## 常用类型

- 数值：`Numeric`
- 整数：`Integer`
- 布尔：`Bool`
- 字符串：`String`
- 数组引用常见于事件参数：`ArrayRef<Integer>`

## 控制结构

- 条件判断使用 `If(...) { ... } Else If(...) { ... } Else { ... }`。
- 循环和复杂容器用法应查对应文档后再写，避免凭通用 C++ 习惯生成错误语法。

## 序列和历史引用

- Bar 序列常见历史引用形式如 `High[1]`、`Low[1]`。
- 当前 Bar 和历史 Bar 在回测/实时中的语义不同；交易策略中涉及触发时机时，应结合 `tb-bar-strategy`。

## 查证规则

- 变量、参数、控制结构：读 `references/syntax-map.md` 后打开对应原文。
- 函数名或返回值不确定：使用 `tb-doc-index` 的函数索引或 `rg` 搜索。
