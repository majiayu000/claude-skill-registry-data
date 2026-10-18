---
name: business-design-handoff
description: Generate developer handoff specs from a design. Use when a design is ready for engineering and needs a spec sheet covering layout, design tokens, component props, interaction states, responsive breakpoints, edge cases, and animation details.
argument-hint: "<Figma URL or design description>"
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

# /design-handoff

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

Generate comprehensive developer handoff documentation from a design.

## Usage

```
/design-handoff $ARGUMENTS
```

Generate handoff specs for: @$1

If a Figma URL is provided, pull the design from Figma. Otherwise, work from the provided description or screenshot.

## What to Include

### Visual Specifications
- Exact measurements (padding, margins, widths)
- Design token references (colors, typography, spacing)
- Responsive breakpoints and behavior
- Component variants and states

### Interaction Specifications
- Click/tap behavior
- Hover states
- Transitions and animations (duration, easing)
- Gesture support (swipe, pinch, long-press)

### Content Specifications
- Character limits
- Truncation behavior
- Empty states
- Loading states
- Error states

### Edge Cases
- Minimum/maximum content
- International text (longer strings)
- Slow connections
- Missing data

### Accessibility
- Focus order
- ARIA labels and roles
- Keyboard interactions
- Screen reader announcements

## Principles

1. **Don't assume** — If it's not specified, the developer will guess. Specify everything.
2. **Use tokens, not values** — Reference `spacing-md` not `16px`.
3. **Show all states** — Default, hover, active, disabled, loading, error, empty.
4. **Describe the why** — "This collapses on mobile because users primarily use one-handed" helps developers make good judgment calls.

## Output

```markdown
## Handoff Spec: [Feature/Screen Name]

### Overview
[What this screen/feature does, user context]

### Layout
[Grid system, breakpoints, responsive behavior]

### Design Tokens Used
| Token | Value | Usage |
|-------|-------|-------|
| `color-primary` | #[hex] | CTA buttons, links |
| `spacing-md` | [X]px | Between sections |
| `font-heading-lg` | [size/weight/family] | Page title |

### Components
| Component | Variant | Props | Notes |
|-----------|---------|-------|-------|
| [Component] | [Variant] | [Props] | [Special behavior] |

### States and Interactions
| Element | State | Behavior |
|---------|-------|----------|
| [CTA Button] | Hover | [Background darken 10%] |
| [CTA Button] | Loading | [Spinner, disabled] |
| [Form] | Error | [Red border, error message below] |

### Responsive Behavior
| Breakpoint | Changes |
|------------|---------|
| Desktop (>1024px) | [Default layout] |
| Tablet (768-1024px) | [What changes] |
| Mobile (<768px) | [What changes] |

### Edge Cases
- **Empty state**: [What to show when no data]
- **Long text**: [Truncation rules]
- **Loading**: [Skeleton or spinner]
- **Error**: [Error state appearance]

### Animation / Motion
| Element | Trigger | Animation | Duration | Easing |
|---------|---------|-----------|----------|--------|
| [Element] | [Trigger] | [Description] | [ms] | [easing] |

### Accessibility Notes
- [Focus order]
- [ARIA labels needed]
- [Keyboard interactions]
```

## If Connectors Available

If **~~design tool** is connected:
- Pull exact measurements, tokens, and component specs from Figma
- Export assets and generate a complete spec sheet

If **~~project tracker** is connected:
- Link the handoff to the implementation ticket
- Create sub-tasks for each section of the spec

## Tips

1. **Share the Figma link** — I can pull exact measurements, tokens, and component info.
2. **Mention edge cases** — "What happens with 100 items?" helps me spec boundary conditions.
3. **Specify the tech stack** — "We use React + Tailwind" helps me give relevant implementation notes.
