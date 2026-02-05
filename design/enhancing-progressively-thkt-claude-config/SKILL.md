---
name: enhancing-progressively
description: >
  CSS-first approach - use CSS before JavaScript. Triggers: レイアウト, スタイル,
  位置, アニメーション, 表示/非表示, トグル, レスポンシブ, CSS Grid, Flexbox,
  transforms, transitions, CSSのみ, JavaScript不要, シンプル
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Progressive Enhancement

## Purpose

Prefer CSS solutions over JavaScript. "The best code is no code."

## Quick Decision

Before writing JS, ask:

1. **"Can CSS solve this?"** → Grid, Flexbox, :has(), transforms
2. **"Is this needed now?"** (YAGNI) → No evidence = don't implement
3. **"Simplest solution?"** (Occam's Razor) → 3 lines CSS > 50 lines JS

## Reference

For detailed guide, see:
[@~/.claude/rules/development/PROGRESSIVE_ENHANCEMENT.md](~/.claude/rules/development/PROGRESSIVE_ENHANCEMENT.md)

## Related

- `applying-code-principles` - SOLID, DRY, Occam's Razor
- `optimizing-performance` - Performance optimization

## Used by

- `/code --frontend` - Frontend implementation
- `/audit` - CSS-first approach verification
