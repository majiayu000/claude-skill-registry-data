---
name: online-assessment-solver
description: Solve a coding question from an online written test / 笔试 under time pressure - reverse-derive the true problem definition from the examples, write zero-dependency code that can be pasted straight in, verify against every given sample, and flag method-name risk when the platform ships an empty template. Triggers on "这道题怎么做", "笔试算法题", 截图带 class Solution / 输入 输出 / 时间限制. Not for take-home projects, system design, or explaining algorithms at length.
version: 1.0.0
---

# Online Assessment Solver (笔试算法题)

Context: the user is mid-test with a countdown. Every second of back-and-forth costs him the question.
**Answer first, explain in three lines.** Never ask for clarification when the examples are enough to pin the definition down.

## Step 1: Derive the definition from the examples, not from the prose

The Chinese problem statement is often ambiguous. **The samples are the real spec.** Reverse-engineer until
every sample output matches exactly, then commit to that definition.

Worked example — 题目写「下载量递增月」，听起来像"连续递增的月数"：

- 输入 `[100,150,99,500,150,200,200,100,800]` → 输出 `[1,2,1,5,1,3,2,1,0]`
- 若按"连续递增"算，下标 1（150）后面是 99，应当是 0 —— 但答案是 2
- 下标 1 右侧第一个**严格大于** 150 的是 500，隔着 2 个月 → **答案 = 右侧第一个更大元素的下标差**

One mismatch is enough to kill a hypothesis. Test the hypothesis against **every** index, including
the duplicates (they decide `<=` vs `<` in the stack pop) and the last element (0 case).

**Always check the equal-element case.** In the example above, `200, 200` sit at index 5 and 6:
index 5 must skip index 6 and find 800. That single pair decides whether the pop condition is `<=` or `<`.

## Step 2: Answer shape

Give, in this order:

1. **One code block, complete and pasteable** — no `...`, no "fill this in"
2. **One-line idea**
3. **Sample verification** — the exact expected output, and specifically the indices where a naive
   reading gets it wrong
4. **Risk notes** — method name, imports, overflow

The code block is the deliverable. Explanations exist so he can defend the answer if asked, not so he
can re-derive it.

## Step 3: Code conventions that survive the grader

```java
// 手写栈，零 import —— 模板没有 import 语句时 Deque/ArrayDeque 会编译失败
int[] st = new int[n];
int top = 0;
```

- 🔴 **零依赖优先**：平台给的模板常是空的 `class Solution {}`（连 `import` 都没有）。
  用手写数组栈代替 `ArrayDeque`，手写快排代替 `Arrays.sort`（若要求不用库）。
- 🔴 **空模板 = 方法名不确定**：题目正文里的签名和模板对不上是常态。按题目给的方法名写，
  **并明确告诉他**：如果右侧「答题指引」给了别的名字，只改方法名、其余不动。
- 🔴 **溢出**：`cur`、`gap`、累加值用 `long`，即便入参是 `int[]`。`1e9` 级别的入参相加必爆。
- 复杂度写一句，让他知道不会超时（判题机卡的是 O(n²)）。

## Step 4: The four failure modes

| 坑 | 表现 | 防法 |
|---|---|---|
| **题意猜错** | 样例全过但提交 0 分 | 定义必须对上**每一个**下标，不是"大多数" |
| **相等元素** | 样例里有两个相同值时最容易错 | 单独验一遍这两个下标 |
| **最后一个元素** | 边界返回值（通常是 0） | 单独验 |
| **空数组 / 单元素** | 数组越界 | 循环前先看 n |

## Verification before you send

```
□ 样例逐位对上了吗（不是"看起来对"，是一位一位数）
□ 严格大于还是大于等于 —— 由样例里的相等对决定了吗
□ 最后一位的返回值对吗
□ 有没有 import（模板里没有就不许有）
□ 方法名是不是题目正文里那个
□ 会不会溢出
```

## Red lines

- 🔴 **不先问澄清**：倒计时在走。样例能定死定义就定死，把"我理解为 X"写进答案里，不要反问。
- 🔴 **不给半成品**：不要写 `// TODO: 处理边界`，他没时间补。
- 🔴 **不展开讲算法课**：给思路一句话 + 验证，不要长篇教程。
- 🔴 **看不清题目就直说**（Houston 准则）：截图里的数字读不出来时，第一句必须声明"这几个数我看不清，按 X 理解"，
  然后**按最可能的理解给出完整代码**，让他能改一处就交。不许因为没有 100% 把握就不给答案。

## Example

> 平台：`class Solution { }` 空模板，题面「求每个月的下载量递增月数」
> 输入 `[100,150,99,500,150,200,200,100,800]` 输出 `[1,2,1,5,1,3,2,1,0]`
>
> → 反推出「右侧第一个严格更大元素的下标差」，单调栈从右往左，手写数组栈零 import
> → 验证：下标 1 得 2（不是 0）、下标 5 得 3（`<=` 弹栈）、下标 8 得 0
> → 提醒：方法名按题面写，若「答题指引」给了别的名字只换名字
