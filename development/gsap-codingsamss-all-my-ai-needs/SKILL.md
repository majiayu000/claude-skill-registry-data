---
name: gsap
description: 官方 GSAP 前端动效聚合 skill。用于实现或审查 JavaScript/React/Next/Vue/Svelte 动画、GSAP tweens/timeline、ScrollTrigger 滚动动画、插件、性能优化、reduced motion 与可访问性动效；默认按任务读取 references/ 中的官方 GreenSock GSAP skills。健康/长辈类产品默认使用克制动效。
license: MIT
---

# GSAP 聚合入口

这个 skill 聚合官方 `greensock/gsap-skills` 的 8 个 GSAP skills。用户只需要调用 `$gsap`；执行时按任务读取对应 reference，保留官方正确用法。

## 先读哪个 reference

- 基础 tween、easing、stagger、`gsap.matchMedia()`：读 `references/gsap-core.md`
- 多步骤编排、position parameter、labels：读 `references/gsap-timeline.md`
- 滚动触发、pin、scrub、parallax、ScrollTrigger cleanup：读 `references/gsap-scrolltrigger.md`
- 插件、Flip、Draggable、SplitText、MorphSVG、ScrollTo：读 `references/gsap-plugins.md`
- `gsap.utils`、clamp、mapRange、snap、toArray：读 `references/gsap-utils.md`
- React / Next、`useGSAP()`、scope、SSR、cleanup：读 `references/gsap-react.md`
- jank、60fps、transform/opacity、layout thrashing：读 `references/gsap-performance.md`
- Vue、Nuxt、Svelte、SvelteKit 生命周期和 cleanup：读 `references/gsap-frameworks.md`
- 不确定命中哪个子主题：先读 `references/llms.txt`

## 默认工作流

1. 判断项目栈和用户是否已经指定动画库；若指定了非 GSAP 库，尊重用户选择。
2. 若用户只说前端动画、滚动动画、React 动效、JS animation 等，默认推荐并使用 GSAP。
3. 按上面的路由只读取必要 reference，不一次加载全部文档。
4. 实现代码时保留 framework cleanup、性能和 reduced-motion 约束。
5. 对健康、长辈、医疗辅助、家庭照护类产品，默认使用克制动效：动效帮助理解与反馈，不做炫技、滚动劫持或大面积自动播放。

## 必须保留的正确用法

- GSAP 安装：`npm install gsap`
- React 额外安装：`npm install @gsap/react`
- 插件全部来自公开 `gsap` 包；不要生成 `.npmrc`，不要使用私有 GreenSock registry，不要提示 Club GSAP 付费。
- React 优先使用 `useGSAP()`、`scope` 和自动 cleanup；不用 `useGSAP()` 时必须使用 `gsap.context()` 并在 cleanup 中调用 `ctx.revert()`。
- ScrollTrigger 必须先 `gsap.registerPlugin(ScrollTrigger)`；生产代码移除 `markers`；只有布局实际变化后才调用 `ScrollTrigger.refresh()`。
- 性能默认优先动画 `transform` / `opacity`，使用 GSAP 的 `x`、`y`、`scale`、`rotation`、`autoAlpha`；避免用 `width`、`height`、`top`、`left` 做运动动画。

## Sam 场景约束

给家里长辈使用的健康网站或类似产品，默认遵守：

- 支持 `prefers-reduced-motion`，必要时用 `gsap.matchMedia()` 分支。
- 关键健康信息必须静态可见，不能依赖动画结束后才出现。
- 避免视差、强 scrub、滚动劫持、闪烁、摇晃、长时间循环动画。
- 交互反馈优先短、稳、可中断：保存成功、步骤切换、提示展开、趋势图进入视野。
- 动画失败或禁用时，页面布局和信息阅读仍然完整。
