---
name: tabbar-icon-generator
description: Generate PNG icons for MiniProgram/Taro TabBar. Use when users need to create, modify, or add TabBar icons for WeChat MiniProgram or Taro projects. Supports common icon types (home, list, user, settings, search, message, cart, favorite) with customizable colors. Icons are generated as 81x81px PNG files with normal and active states.
---

# TabBar Icon Generator

Generate PNG icons for MiniProgram TabBar using code-defined SVG templates converted to PNG.

## Quick Start

```bash
# Generate all preset icons with default colors
node .codebuddy/skills/tabbar-icon-generator/scripts/generate_icons.js -o frontend/src/assets/tabbar

# Generate specific icons only
node .codebuddy/skills/tabbar-icon-generator/scripts/generate_icons.js -o frontend/src/assets/tabbar -i home,user,settings

# Custom colors
node .codebuddy/skills/tabbar-icon-generator/scripts/generate_icons.js -o frontend/src/assets/tabbar --normal-color "#666666" --active-color "#07C160"
```

## Available Icons

| Icon | Description | Usage |
|------|-------------|-------|
| home | House shape | 首页 |
| list | Three horizontal lines | 列表/记录 |
| user | Person silhouette | 我的/个人 |
| settings | Gear shape | 设置 |
| search | Magnifying glass | 搜索 |
| message | Envelope | 消息 |
| cart | Shopping cart | 购物车 |
| favorite | Heart shape | 收藏 |

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `-o, --output` | `src/assets/tabbar` | Output directory |
| `-i, --icons` | all | Comma-separated icon names |
| `--normal-color` | `#999999` | Inactive state color |
| `--active-color` | `#07C160` | Active state color |
| `--size` | `81` | Icon size in pixels |

## Output

- Files: `{icon}.png` and `{icon}-active.png`
- Format: PNG with transparency
- Size: 81x81px (WeChat MiniProgram standard)

## Usage in app.config.ts

```typescript
tabBar: {
  color: '#999999',
  selectedColor: '#07C160',
  list: [
    {
      pagePath: 'pages/index/index',
      text: '首页',
      iconPath: 'assets/tabbar/home.png',
      selectedIconPath: 'assets/tabbar/home-active.png'
    }
  ]
}
```

## Adding Custom Icons

Edit `scripts/generate_icons.js` to add new icon definitions in the `getIconSvg` function:

```javascript
'custom-icon': `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 81 81">
  <path d="..." fill="none" stroke="${color}" stroke-width="4"/>
</svg>`
```

Then regenerate: `node scripts/generate_icons.js -i custom-icon`

## Requirements

- Node.js 14+
- sharp (auto-installed on first run)
