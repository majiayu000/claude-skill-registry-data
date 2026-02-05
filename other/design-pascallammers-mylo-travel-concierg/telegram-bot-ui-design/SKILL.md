---
name: Telegram Bot UI Design
description: Expert in designing Telegram bot interfaces with keyboards, buttons, conversational flows, and mobile-first UX patterns.
---

# Telegram Bot UI Design Specialist

A specialized skill for designing and optimizing Telegram bot user interfaces. This skill helps you create intuitive, accessible, and mobile-first bot experiences with proper keyboard layouts, button hierarchies, and conversational flows.

## How to Use

This is a **pure instruction skill** - no scripts required. Invoke it when you need help with:

1. **Keyboard Design**: Reply keyboards, inline buttons, callback structures
2. **Conversational Flows**: Multi-step workflows, user journeys, state management
3. **Message Formatting**: HTML markup, emoji strategy, visual hierarchy
4. **Navigation Patterns**: Pagination, back buttons, breadcrumbs
5. **Accessibility**: Touch targets, color-blind support, clear language
6. **Performance**: Response times, timeout handling, loading states

Simply describe your bot UI challenge or paste your code, and I'll provide:
- Design recommendations following Telegram best practices
- Code examples for keyboards and buttons
- UX improvements for better user engagement
- Accessibility fixes for inclusive design

## Examples

### Example 1: Design a Product Browsing Keyboard

**Request:**
```
Design a keyboard for browsing products by category in an e-commerce bot.
Categories: Electronics, Fashion, Home, Sports, Books
```

**Response includes:**
- Reply keyboard vs inline keyboard recommendation
- Button layout (2-column grid for mobile)
- Emoji usage for visual scanning
- Back button placement
- Pagination strategy for large lists

### Example 2: Improve Message Formatting

**Request:**
```
Improve this message format:
Product: USB Cable
Price: $5.99
Link: http://example.com
```

**Response includes:**
- HTML markup for emphasis (`<b>`, `<i>`, `<code>`)
- Emoji for visual breaks (📦, 💰, 🔗)
- Proper spacing and line breaks
- Call-to-action button design

### Example 3: Fix Navigation Flow

**Request:**
```
Users are getting stuck in my bot after selecting a product.
They can't go back to the category menu.
```

**Response includes:**
- Add "← Back to Categories" button
- Breadcrumb pattern (Categories > Electronics > Product)
- State management strategy
- Callback data structure

## Core Principles

**Mobile-First**: 95% of Telegram users are on mobile
- Minimum 44px tap targets
- 2-3 button columns maximum
- Large, clear labels

**Speed Matters**: Every 1s delay increases drop-off
- Response times < 2 seconds
- Loading indicators for slow operations
- Timeout fallbacks

**Consistency Builds Trust**: Same action = same location
- Primary action always bottom-right
- Back button always top-left
- Destructive actions use red emoji (🗑️, ❌)

**Accessibility**: Inclusive by default
- No emoji-only buttons (always add text)
- Color contrast for visibility
- Clear error messages with retry options

## Keyboard Types

**Reply Keyboard** (suggested replies):
```python
keyboard = [
    [KeyboardButton("🔍 Search"), KeyboardButton("📋 My Orders")],
    [KeyboardButton("⚙️ Settings"), KeyboardButton("❓ Help")]
]
```
**Best for**: Main menu, persistent navigation

**Inline Keyboard** (buttons below message):
```python
keyboard = [
    [InlineKeyboardButton("View Details", callback_data="view_123")],
    [InlineKeyboardButton("Add to Cart", callback_data="cart_add_123")],
    [InlineKeyboardButton("← Back", callback_data="back_categories")]
]
```
**Best for**: Actions on specific items, confirmations

## Common Patterns

1. **Browse → Select → Detail → Action**
2. **Search → Results (paginated) → Select → Detail**
3. **Multi-Step Form**: Step 1 → Step 2 → Step 3 → Confirm → Execute
4. **Settings**: Menu → Category → Option → Save

## Anti-Patterns to Avoid

❌ **Too many buttons** (>5 per row, >3 rows)
❌ **Inconsistent positioning** (back button moves around)
❌ **Emoji spam** (every word has emoji)
❌ **No back navigation** (users get stuck)
❌ **Confusing labels** ("Option 1", "Button A")
❌ **Timeout without feedback** (>3s with no status)

## Notes

- **Telegram Limits**: 4096 chars per message, 100 buttons per keyboard
- **Callback Data**: Max 64 bytes per button
- **Message Editing**: Use `edit_message_text()` to update status
- **Testing**: Always test on mobile Telegram (Android + iOS)
- **Documentation**: [Telegram Bot API](https://core.telegram.org/bots/api)

This skill integrates with your existing bot code (python-telegram-bot, aiogram, telebot, etc.) and provides language-agnostic design guidance.
