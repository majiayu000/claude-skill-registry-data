---
name: telegram-bot
description: |
  Build Telegram bots with modern frameworks.
  Use when: creating Telegram bot, chatbot, notification bot.
  Triggers: "telegram", "tg bot", "телеграм бот", "teloxide", "aiogram".
---

# Telegram Bot Development

## Project Protection Setup

**MANDATORY before writing any code:**

```bash
# 1. Create .gitignore
cat >> .gitignore << 'EOF'
# Build
target/
node_modules/
__pycache__/
*.pyc
dist/

# Secrets - CRITICAL for bots!
.env
.env.*
!.env.example
*.key
bot_token.txt

# IDE
.idea/
.vscode/
.DS_Store
EOF

# 2. Setup pre-commit hooks
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
EOF

pre-commit install
```

**Why critical for bots:** Bot tokens give FULL access to your bot. Leaked token = compromised bot.

---

## Stack Options

| Language | Framework | Best For |
|----------|-----------|----------|
| **Rust** | teloxide | Performance, type safety |
| **Python** | aiogram 3.x | Rapid development, async |
| **Node** | grammY / telegraf | JS ecosystem |

---

## Quick Start

### Rust (teloxide)

```toml
# Cargo.toml
[dependencies]
teloxide = { version = "0.13", features = ["macros"] }
tokio = { version = "1", features = ["full"] }
log = "0.4"
pretty_env_logger = "0.5"
```

```rust
use teloxide::prelude::*;

#[tokio::main]
async fn main() {
    pretty_env_logger::init();
    log::info!("Starting bot...");

    let bot = Bot::from_env();

    teloxide::repl(bot, |bot: Bot, msg: Message| async move {
        bot.send_message(msg.chat.id, "Hello!").await?;
        Ok(())
    })
    .await;
}
```

### Python (aiogram 3.x)

```python
# requirements.txt
aiogram>=3.0
```

```python
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

bot = Bot(token="BOT_TOKEN")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Hello!")

@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

### Node (grammY)

```typescript
// package.json: "grammy": "^1.21"
import { Bot } from "grammy";

const bot = new Bot(process.env.BOT_TOKEN!);

bot.command("start", (ctx) => ctx.reply("Hello!"));
bot.on("message", (ctx) => ctx.reply(ctx.message.text ?? ""));

bot.start();
```

---

## Command Handlers

### Rust

```rust
use teloxide::{prelude::*, utils::command::BotCommands};

#[derive(BotCommands, Clone)]
#[command(rename_rule = "lowercase")]
enum Command {
    #[command(description = "Start the bot")]
    Start,
    #[command(description = "Get help")]
    Help,
    #[command(description = "Echo text")]
    Echo(String),
}

async fn answer(bot: Bot, msg: Message, cmd: Command) -> ResponseResult<()> {
    match cmd {
        Command::Start => bot.send_message(msg.chat.id, "Welcome!").await?,
        Command::Help => bot.send_message(msg.chat.id, Command::descriptions().to_string()).await?,
        Command::Echo(text) => bot.send_message(msg.chat.id, text).await?,
    };
    Ok(())
}
```

### Python

```python
from aiogram.filters import Command

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Welcome!")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Available commands:\n/start - Start\n/help - Help")
```

---

## Inline Keyboards

### Rust

```rust
use teloxide::types::{InlineKeyboardButton, InlineKeyboardMarkup};

let keyboard = InlineKeyboardMarkup::new(vec![
    vec![
        InlineKeyboardButton::callback("Option 1", "opt_1"),
        InlineKeyboardButton::callback("Option 2", "opt_2"),
    ],
    vec![
        InlineKeyboardButton::url("Website", "https://example.com".parse().unwrap()),
    ],
]);

bot.send_message(chat_id, "Choose:")
    .reply_markup(keyboard)
    .await?;
```

### Python

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Option 1", callback_data="opt_1"),
        InlineKeyboardButton(text="Option 2", callback_data="opt_2"),
    ],
    [
        InlineKeyboardButton(text="Website", url="https://example.com"),
    ]
])

await message.answer("Choose:", reply_markup=keyboard)
```

---

## Callback Handling

### Rust

```rust
#[derive(Clone)]
enum CallbackAction {
    Option1,
    Option2,
}

async fn callback_handler(
    bot: Bot,
    q: CallbackQuery,
) -> ResponseResult<()> {
    if let Some(data) = &q.data {
        let text = match data.as_str() {
            "opt_1" => "You chose Option 1",
            "opt_2" => "You chose Option 2",
            _ => "Unknown",
        };

        bot.answer_callback_query(&q.id).await?;

        if let Some(msg) = q.message {
            bot.edit_message_text(msg.chat.id, msg.id, text).await?;
        }
    }
    Ok(())
}
```

### Python

```python
@dp.callback_query(lambda c: c.data.startswith("opt_"))
async def process_callback(callback: types.CallbackQuery):
    if callback.data == "opt_1":
        text = "You chose Option 1"
    else:
        text = "You chose Option 2"

    await callback.answer()  # Remove loading state
    await callback.message.edit_text(text)
```

---

## FSM (Finite State Machine) for Dialogs

### Python (aiogram)

```python
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    email = State()
    confirm = State()

@dp.message(Command("register"))
async def start_registration(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Enter your name:")

@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.email)
    await message.answer("Enter your email:")

@dp.message(Form.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(f"Registered: {data['name']} ({data['email']})")
```

### Rust (teloxide dialogue)

```rust
use teloxide::dispatching::dialogue::{InMemStorage, Dialogue};

type MyDialogue = Dialogue<State, InMemStorage<State>>;

#[derive(Clone, Default)]
pub enum State {
    #[default]
    Start,
    ReceiveName,
    ReceiveEmail { name: String },
}

async fn start(bot: Bot, dialogue: MyDialogue, msg: Message) -> HandlerResult {
    bot.send_message(msg.chat.id, "Enter your name:").await?;
    dialogue.update(State::ReceiveName).await?;
    Ok(())
}

async fn receive_name(bot: Bot, dialogue: MyDialogue, msg: Message) -> HandlerResult {
    let name = msg.text().unwrap_or_default().to_string();
    bot.send_message(msg.chat.id, "Enter your email:").await?;
    dialogue.update(State::ReceiveEmail { name }).await?;
    Ok(())
}
```

---

## Webhooks vs Polling

| Method | Pros | Cons | Use When |
|--------|------|------|----------|
| **Polling** | Simple setup, works locally | Less efficient, delay | Development, small bots |
| **Webhooks** | Real-time, efficient | Needs HTTPS, public URL | Production |

### Webhook Setup (Rust)

```rust
use teloxide::dispatching::update_listeners::webhooks;

let addr = ([0, 0, 0, 0], 8443).into();
let url = "https://your-domain.com/webhook".parse().unwrap();

let listener = webhooks::axum(bot.clone(), webhooks::Options::new(addr, url))
    .await
    .unwrap();

teloxide::repl_with_listener(bot, handler, listener).await;
```

---

## Database Integration

### SQLite with SQLx (Rust)

```rust
use sqlx::SqlitePool;

struct AppState {
    db: SqlitePool,
}

async fn save_user(pool: &SqlitePool, user_id: i64, username: &str) -> Result<()> {
    sqlx::query!(
        "INSERT OR REPLACE INTO users (id, username) VALUES (?, ?)",
        user_id, username
    )
    .execute(pool)
    .await?;
    Ok(())
}
```

---

## Environment & Security

```bash
# .env (NEVER commit!)
TELOXIDE_TOKEN=123456:ABC-DEF...
DATABASE_URL=sqlite:bot.db

# .gitignore
.env
*.db
```

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Token in code | Use environment variables |
| No error handling | Wrap handlers in try/catch |
| Blocking in async | Use tokio::spawn for heavy work |
| No rate limiting | Respect Telegram limits (30 msg/sec) |
| Large media sync | Use file_id, not re-uploading |

---

## Testing

### Rust (teloxide)

```rust
#[cfg(test)]
mod tests {
    use super::*;

    // Unit test for message processing logic
    #[test]
    fn test_parse_command() {
        let result = parse_expense("/add 100 food");
        assert_eq!(result.amount, 100.0);
        assert_eq!(result.category, "food");
    }

    // Integration test with mock bot
    #[tokio::test]
    async fn test_start_command_returns_welcome() {
        // Use teloxide_tests or mock the bot
        let response = handle_start_command().await;
        assert!(response.contains("Welcome"));
    }
}
```

### Python (aiogram)

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_message():
    message = MagicMock()
    message.answer = AsyncMock()
    message.text = "/start"
    message.from_user.id = 123
    return message

@pytest.mark.asyncio
async def test_start_handler(mock_message):
    await cmd_start(mock_message)
    mock_message.answer.assert_called_once()
    assert "Welcome" in mock_message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_fsm_state_transition(mock_message, state):
    await start_registration(mock_message, state)
    current_state = await state.get_state()
    assert current_state == Form.name
```

### Node (grammY)

```typescript
import { describe, it, expect, vi } from 'vitest';

describe('Bot handlers', () => {
  it('responds to /start', async () => {
    const ctx = {
      reply: vi.fn(),
      message: { text: '/start' },
    };

    await startHandler(ctx);
    expect(ctx.reply).toHaveBeenCalledWith(expect.stringContaining('Welcome'));
  });
});
```

---

## TDD Workflow

```
1. Task[tdd-test-writer]: "Create /start command handler"
   → Writes test that expects welcome message
   → cargo test / pytest / npm test → FAILS (RED)

2. Task[rust-developer]: "Implement /start handler"
   → Implements minimal code
   → cargo test → PASSES (GREEN)

3. Repeat for each command/feature

4. Task[code-reviewer]: "Review bot implementation"
   → Checks security, error handling, patterns
```

---

## Security Checklist

- [ ] Token in environment variable (never hardcoded)
- [ ] `.env` in `.gitignore`
- [ ] pre-commit hooks with gitleaks
- [ ] Input validation (no command injection)
- [ ] Rate limiting for user requests
- [ ] Webhook URL uses HTTPS
- [ ] No sensitive data in logs
- [ ] User data encrypted if stored

---

## Project Structure

```
telegram-bot/
├── src/
│   ├── main.rs
│   ├── handlers/
│   │   ├── mod.rs
│   │   ├── commands.rs
│   │   └── callbacks.rs
│   ├── state.rs        # FSM states
│   └── db.rs           # Database
├── tests/
│   └── integration.rs  # Integration tests
├── Cargo.toml
├── .env.example        # Template (committed)
├── .env                # Real secrets (NOT committed)
└── .gitignore
```
