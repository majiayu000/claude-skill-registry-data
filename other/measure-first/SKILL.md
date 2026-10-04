---
name: measure-first
description: 动 briffy 里任何用户看得见的东西之前，先把真工作区量一遍——分布、基数、每一格里真有什么。当你要回答「这个功能该怎么做」「这一版好不好」「该不该加这个维度」，或者要改筛选、搜索、检索、卡片、设置里任何一处呈现时使用。也用于给一个改动配上可复现的数。
---

# 先量一遍

briffy 的所有结论都是量出来的。`docs/NOTES.md` 开篇第一句：
「每一节都是一个决定，以及量出来的、让它变成那个决定的数。」
paper-ui 里每一条硬约束后面都跟着一个实测值。**这是这个仓库的说话方式，不是可选的严谨。**

## 为什么非量不可

不量的代价是具体的，不是「不够严谨」这种抽象损失：

- **2026-09-09，筛选。** 凭印象说「来源那个下拉筛掉的只有 21%」——错的。那 21% 是
  `entrySource`（剪贴板 262 / 331），而下拉筛的是站点和应用名。量完才看见真正的病在别处：
  筛选行写「文字 203」而屏幕上只有 19 条，**差十倍**，因为「筛」和「数」是两段各自算的代码。
  这个错误存在了不知道多久，五版界面改动都没碰到它——**因为没人对过那个数**。
- **同一天，第二次。** 「来源」那一档里最大的一格是「未知」，144 条，占 44%。
  一个常驻的筛选位置，里面最大的一项是「没记下来」。这件事只有数能告诉你。

**一个产品判断如果没有数撑着，它就是个偏好。** 这个仓库里偏好不算数。

## 怎么打开真库

工作区默认在 `~/Library/Application Support/briffy/workspace`（macOS）。
两套写法都在用，**新台子优先用 node 那套**——快、不用起 electron、能进 `npm test`。

### node 里跑（推荐；`dev/` 里 8 个台子这么写）

```js
// store.js 的 paths() 会问 electron 要 userData（放模型的那两处），node 里没有那个 app。
// 垫一个假的：只要不碰模型文件就够了。
const Module = require('module');
const realLoad = Module._load;
Module._load = function (req, ...rest) {
  if (req === 'electron') return { app: { getPath: () => '/tmp/briffy-no-userdata' } };
  return realLoad.call(this, req, ...rest);
};
const { Store } = require('../src/main/store');

const store = new Store();
// **workspaceDir 是 getter。** `store.workspaceDir = x` 在 'use strict' 下抛错，
// **不在 strict 下会静默失败**——赋完值它还是原来那个，于是你量的是一个空库
// 却以为量的是真库。要设就设 settings。
store.settings = { workspaceDir: process.argv[2]
  || require('path').join(process.env.HOME, 'Library/Application Support/briffy/workspace') };
```

### electron 里跑（`dev/` 里 13 个台子这么写）

```
npx electron dev/xxx.js
```
文件里 `const { app } = require('electron')`，等 `app.whenReady()`。
**要用真的 userData（模型、索引 `index.db`）时才值得走这条**。

## 两个坑

1. **`store.workspaceDir` 是 getter。** `'use strict'` 下 `store.workspaceDir = x` 抛
   TypeError；**没写 `'use strict'` 的话它静默失败**，赋完值仍然是默认路径——
   你会量到一个空库，还以为量的是真库。**台子一律写 `'use strict'`**，让它当场炸。
   正确的写法是 `store.settings = { workspaceDir }`。
2. **`store.paths()` 里有两项在 userData 底下**（`models`、`ocrModels`），所以纯 node 必须垫 electron，
   哪怕你一个模型都不碰。

## 该量什么

回答「这个维度配不配有一个常驻的位置」，量这四样：

| 量什么 | 判据 |
| --- | --- |
| **基数** 有几个值 | 十几个值的维度进不了一排词，得换个形状 |
| **选择性** 点一个值筛掉多少 | **筛完还剩八成的，不叫筛选**。每个值都该筛掉一大半 |
| **覆盖率** 多少条答不上来 | 最大的一格是「未知」的维度，是个坏维度 |
| **使用** 这个功能被用过几次 | `pinned` 在 331 条里是 0——它占着一格，从来没被按过 |

现成的台子：`dev/` 里 **21 个直接读真库**（`grep -l "Application Support/briffy\|workspaceDir" dev/*.js`），
其中检索类的看 `dev/recall-arch-bench.js`（14 个问题 / 33 条满分记录），
筛选类的看 `dev/filter-count-test.js`。

## 量完要做的两件事

1. **把数写进注释和提交信息**，带上日期和样本量：「2026-09-09 量的：331 条里 262 条是剪贴板」。
   下一个人（或者三周后的你）才不用重量一遍。这个仓库里每条硬约束都长这样。
2. **能变成不变量的，写成台子**。`dev/filter-count-test.js` 就是这么来的：
   量出「数和屏幕对不上」之后，把「每个数都必须等于点下去之后屏上的条数」变成 12073 个断言。
   一次性的数会过期，台子不会。

## 什么时候不用量

- 纯重构、改名、补注释——没有用户看得见的行为变化。
- 用户已经明确给了方向（那时该做的是**照做**，量是为了发现他没说的坑）。
- 修一个有明确复现步骤的 bug。
