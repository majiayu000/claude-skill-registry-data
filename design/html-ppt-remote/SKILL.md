---
name: html-ppt-remote
description: >
  给任意 HTML 幻灯片注入翻页笔遥控 + 智能全屏能力。当用户提到"翻页笔"、"全屏"、"幻灯片翻页"、
  "HTML PPT"、"presentation remote"时自动触发。兼容所有幻灯片结构（deck-stage、.slide、#deck、Swiper.js 等）。
license: MIT
compatibility: 纯浏览器端 JS，无需 Node.js 环境，任何能运行 HTML 的环境即可
---

# html-ppt-remote

> 给任意 HTML 幻灯片注入"翻页笔遥控 + 智能全屏"能力。

## 功能

1. **翻页笔上下翻页** — 拦截键盘事件（ArrowLeft/Right、PageUp/Down、Space、Enter 等），兼容主流翻页笔硬件
2. **首页按上一页 → 全屏** — 在第一页按"上一页"键自动进入全屏，无需 F5
3. **尾页按下一页 → 退出全屏** — 在最后一页按"下一页"键自动退出全屏
4. **无需刷新** — 首页尾页持续生效，不依赖页面刷新
5. **零冲突** — 使用 capture 模式监听，仅在需要全屏/退出全屏时拦截事件，其他情况交给页面已有的翻页逻辑

## 四层检测架构（兼容未知结构）

| 层级 | 机制 | 作用 |
|------|------|------|
| 第一层 | DOM 快速检测 | 直接读取已知结构的属性/class/transform |
| 第二层 | 事件监听捕获 | 拦截 `slidechange` / `postMessage` / `hashchange` |
| 第三层 | MutationObserver | 追踪 DOM 属性变化（class/data-* 增删） |
| 第四层 | 键盘计数器兜底 | 计数翻页按键次数，模拟页码位置 |

**关键：即使完全未知的框架，也能通过第四层键盘计数器正常工作。**

## 已知兼容的幻灯片结构

| 结构 | 检测方式 | 示例 |
|------|----------|------|
| `<deck-stage>` web component | 读取 `.index` / `.length` 属性 | beautiful-html-templates（34个模板） |
| `.slide` + `.active` / `.current` / `.is-active` class | 遍历查找活跃页 | pratyaya-ppt, reveal.js |
| `#deck` + `translateX` 滑动 | 读取 CSS transform | open-design deck.html, guizang-ppt |
| `.swiper-slide` + `.swiper-slide-active` | Swiper.js 标准结构 | Swiper.js |
| `display:none/flex` 切换 | 可见性检测 | 自定义结构 |
| `[data-active]` / `[data-state]` / `[data-current]` | data 属性标记 | 自定义框架 |
| URL hash 驱动翻页 | 监听 `hashchange` | 单页应用 |
| 未知结构 | 键盘计数器兜底 | 任意框架 |

## 使用方法

### 方法1：引入 JS 文件（推荐）

在 HTML 的 `</body>` 前加一行：

```html
<script src="slide-remote.js"></script>
```

### 方法2：内联代码

直接在 HTML 的 `</body>` 前粘贴以下代码：

```html
<script>
(function(){
  'use strict';
  function getSlides(){return document.querySelectorAll('.slide')}
  function getIdx(){
    var s=getSlides();if(!s.length)return 0;
    for(var i=0;i<s.length;i++)if(s[i].classList.contains('active'))return i;
    var d=document.getElementById('deck');
    if(d){var m=getComputedStyle(d).transform;if(m&&m!=='none'){try{var mat=new DOMMatrix(m),w=s[0].offsetWidth||innerWidth;return Math.round(Math.abs(mat.m41)/w)}catch(e){}}}
    return 0
  }
  function getTotal(){return getSlides().length||1}
  function isFS(){return!!(document.fullscreenElement||document.webkitFullscreenElement||document.msFullscreenElement)}
  function goFS(){var el=document.documentElement,fn=el.requestFullscreen||el.webkitRequestFullscreen||el.msRequestFullscreen;if(fn)fn.call(el)}
  function exitFS(){var fn=document.exitFullscreen||document.webkitExitFullscreen||document.msExitFullscreen;if(fn)fn.call(document)}
  document.addEventListener('keydown',function(e){
    var nk=['ArrowRight','ArrowDown','PageDown',' ','Enter'],pk=['ArrowLeft','ArrowUp','PageUp','Backspace'];
    var isN=nk.indexOf(e.key)>=0,isP=pk.indexOf(e.key)>=0;
    if(!isN&&!isP)return;
    var idx=getIdx(),total=getTotal();
    if(isP&&idx<=0&&!isFS()){goFS();e.preventDefault();e.stopPropagation();return}
    if(isN&&idx>=total-1&&isFS()){exitFS();e.preventDefault();e.stopPropagation();return}
  },true);
})();
</script>
```

### 方法3：让 AI 自动注入

当你（或 Agent）生成 HTML PPT 时，只需在文件末尾 `</body>` 前加入：

```html
<!-- 翻页笔遥控 + 智能全屏 -->
<script src="slide-remote.js"></script>
```

`slide-remote.js` 就在**本 skill 同级目录**下，复制出来放到 HTML 同级目录即可，或用 CDN 托管。

## 支持的翻页笔按键

| 按键 | 行为 |
|------|------|
| `→` / `↓` / `PageDown` / `Space` / `Enter` | 下一页（尾页且全屏时退出全屏） |
| `←` / `↑` / `PageUp` / `Backspace` | 上一页（首页且非全屏时进入全屏） |

## 兼容的幻灯片生成器

| 生成器 | 结构 | 兼容 |
|--------|------|------|
| beautiful-html-templates | `<deck-stage>` web component | ✅ |
| open-design html-ppt | `#deck` + translateX | ✅ |
| pratyaya-ppt | `.slide` + `.active` class | ✅ |
| 任意 `.slide` 结构 | `.slide` 元素 + 翻页逻辑 | ✅ |

## 常见翻页笔硬件兼容

| 品牌型号 | 发送按键 | 兼容 |
|----------|----------|------|
| 罗技 R400/R800 | PageUp / PageDown | ✅ |
| 诺为 N33/N55 | ArrowLeft / ArrowRight | ✅ |
| 得力 18630 | PageUp / PageDown | ✅ |
| 通用 USB 翻页笔 | PageUp / PageDown | ✅ |

## 原理

### 核心架构：capture 模式优先拦截
- 使用 `addEventListener('keydown', handler, true)` 的 **capture 模式**，优先于页面自身的 keydown handler
- 仅在"首页+上一页"和"尾页+下一页"两个场景拦截事件（`stopPropagation`）
- 其他情况放行，让页面已有的翻页函数正常执行
- 全屏 API 兼容 Chrome/Firefox/Safari/Edge（含 webkit/ms 前缀）

### 兼容未知结构的关键
- **四层递进检测**：DOM 快速检测 → 事件捕获 → MutationObserver → 键盘计数器
- 每层失败自动降级到下一层，最终兜底方案不依赖任何 DOM 结构
- 即使遇到全新的幻灯片框架，只要它有键盘翻页功能，就能通过按键计数追踪页码位置

## 注意事项

1. **页面必须已有翻页逻辑** — 本脚本**只处理全屏切换**，不接管翻页
2. 全屏需要用户手势触发（键盘事件满足此条件），首次按键即可生效
3. 如果页面已有 F5 全屏逻辑，不冲突——本脚本用的是翻页笔按键触发
4. 首次加载时会尝试 DOM 检测，如果失败会自动切换到事件监听或键盘计数器
