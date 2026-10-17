---
name: prototype
description: 构建一个 throwaway prototype 来回答设计问题。当用户想确认某个 state model 或 logic 是否合理，或想探索 UI 应该长什么样时使用。
---

# Prototype

prototype 是**用来回答某个问题的 throwaway 代码**。问题决定了它的形态。

## 选择分支

先确认要回答的是哪个问题，从用户的 prompt、周围的代码来判断，如果用户在场也可以直接询问：

- **「这套 logic / state model 合理吗？」** → [LOGIC.md](LOGIC.md)。构建一个单一的、可分享的 HTML 文件（包含自由操作的按钮和带标签页的引导式分步演示），让 state machine 跑过那些在纸面上很难推演的用例，而且让非开发者也能操作。
- **「它应该长什么样？」** → [UI.md](UI.md)。在单一路由上生成几个差异极大的 UI variant，通过 URL search param 和一个浮动底栏来切换。

两个分支产出的 artifact 截然不同，选错了会浪费整个 prototype。如果问题确实模棱两可，又联系不上用户，就默认选择更贴合周围代码的分支（后端 module → logic；页面或组件 → UI），并在 prototype 顶部注明这个假设。

## 适用于两个分支的规则

1. **从第一天起就是 throwaway，并且要明确标注。** 把 prototype 代码放在它实际会被使用的位置附近（紧挨着它为之做原型的 module 或页面），这样上下文一目了然，但命名要让随便翻到的人一眼看出这是 prototype，不是生产代码。对于 throwaway 的 UI 路由，遵循项目现有的路由约定，不要发明新的顶层结构。
2. **启动要毫无门槛。** UI prototype 从项目任务运行器里的一条命令就能启动：`pnpm <name>`、`python <path>`、`bun <path>` 等。logic demo 则是用户双击即可打开的单个 HTML 文件。无论哪种，启动它都不需要动脑。
3. **默认不持久化。** state 放在内存里。persistence 是 prototype 要_检验_的对象，不是它应该依赖的东西。如果问题明确涉及数据库，就接一个临时数据库，或一个命名清晰、写着「PROTOTYPE, wipe me」的本地文件。
4. **跳过打磨。** 不写测试，除了让 prototype 能_跑起来_所必需的错误处理之外不做错误处理，不做抽象。重点是快速学到东西。
5. **把 state 亮出来。** 每次操作之后（logic）或每次切换 variant 时（UI），打印或渲染完整的相关 state，让用户看到发生了什么变化。
6. **完成后收尾。** 把任何验证过的 decision 合并进真实代码，然后把 prototype 本身作为 **primary source** 留存：提交到一个 throwaway branch，不进入 main，并在实现 issue 上留下指向该 branch 的 context pointer。也要把答案记下来（结论以及它解决的问题），记在 issue 或某个 commit 里。main branch 只保留已验证的 decision。
