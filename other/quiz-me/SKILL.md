---
name: quiz-me
description: 就一次变更出报告和测验，满分通过才 merge。
disable-model-invocation: true
---

给我一份 HTML 报告讲清这次变更：背景、直觉、做了什么、行为依赖哪些既有 code path。
diff 只能带来浅层理解，很多行为藏在既有的 code path 里。

报告之后附上测验：就这次变更考我，一次一题，答错就讲解并重问。
我满分通过后才能 merge；没通过就一直问到通过为止。
