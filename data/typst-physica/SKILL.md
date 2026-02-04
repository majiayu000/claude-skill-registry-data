---
name: typst-physica
description: typst公式中的微分、偏微分方程编写，latex公式转typst。
---


# 引用包

应在typst文档的开头，引用包。公式编写、文档排版，依赖`modern-cug-report`。

用于如果已经引用了`modern-cug-report`，则无需再重复添加了。

```typst
#import "@local/modern-cug-report:0.1.3": *
#show: doc => template(doc, footer: "CUG水文气象学2025", header: "")
```


# 偏微分方程

- `(∂ theta) / (∂ t)`

  `\frac{\partial \theta}{\partial t}`采用typst编写会非常简单，`pdv(theta, t)`

  ```typst
  (partial.diff theta) / (partial.diff t) // 是错误写法
  pdv(theta, t)                           // 正确写法
  ```

- `(d theta) / (d t)`则是：`dv(theta, t)`


# text

typst公式中的本文需要使用引号：

```typst
q_(infiltration)   // 错误
q_("infiltration") // 正确
```

# fraction

- latex的`\frac{y}{x}`，写成typst则是`y/x`；
  
  若分子、分母有多个变量，则用括号括起来。例如latex的`\frac{y z}{x}`，写成typst则是`(y z) / x`


# 排版

- 一级标题之前空两行，凸显章节的层次感。

- 第一个一级标题，不用空两行。
