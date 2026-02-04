---
name: Telegram Bot Development
description: Автоматизация создания Telegram bot команд и handlers
version: 2.0.0
author: Family Budget Team
tags: [telegram, bot, python-telegram-bot, conversationhandler, webapp]
dependencies: [api-development]
---

# Telegram Bot Development Skill

Автоматизация создания новых команд, conversation handlers и Telegram Web Apps для проекта Family Budget.

## Когда использовать этот скил

Используй этот скил когда нужно:
- Создать новую команду для Telegram бота
- Добавить ConversationHandler с multi-step flow (FR-001, FR-004)
- Создать Telegram Web App (Phase 3: FR-070-FR-078)
- Интегрировать команду с backend API
- Создать inline keyboards и валидацию ввода

Скил автоматически вызывается при запросах типа:
- "Создай новую команду /command для бота"
- "Добавь multi-step conversation для X"
- "Создай Telegram Web App для Y"

## Контекст проекта

**Проект использует:**
- **python-telegram-bot 20.7+** для Telegram бота
- **ConversationHandler** для multi-step команд (add, edit)
- **Telegram Web Apps** (Phase 3) - 8 HTML forms via Menu Button
- **API Client** (`bot/utils/api_client.py`) для взаимодействия с backend
- **SessionManager** для управления JWT токенами
- **APScheduler** для weekly reports (FR-005) и budget alerts (FR-006)

**Архитектура:**
```
bot/
├── main.py                  # Entry point, graceful shutdown
├── bot.py                   # BotApplication class, handler registration
├── handlers/                # Command handlers
│   ├── start.py             # /start - OAuth authentication (FR-030)
│   ├── add.py               # /add - Add transaction (FR-001, ConversationHandler)
│   ├── add_plan.py          # /addplan - Add budget plan (FR-002)
│   ├── edit.py              # /edit - Edit/delete transactions (FR-004)
│   ├── summary.py           # /summary - Plan vs Fact (FR-003)
│   ├── today.py             # /today - Today's statistics
│   └── settings.py          # /settings - User settings
├── utils/
│   ├── api_client.py        # HTTP client for backend API
│   ├── session.py           # SessionManager (JWT tokens)
│   ├── telegram_auth.py     # Telegram OAuth validation
│   ├── validators.py        # Input validation
│   └── scheduler.py         # APScheduler for jobs
└── jobs/
    └── weekly_report.py     # Weekly budget reports (FR-005)
```

## Telegram Web Apps (Phase 3 - NEW!)

**8 HTML Forms via Menu Button:**
- **Main Menu** - Quick stats + navigation
- **Add Transaction** - Expense/income form
- **Transaction History** - List with filters
- **Statistics** - Plan vs Fact charts
- **Search** - Advanced search with CSV export
- **Add Plan** - Budget planning form
- **Edit Transaction** - Edit/delete form
- **Settings** - User preferences

**Technology:**
- Vanilla JS ES6+ (~190KB bundle)
- Telegram Web Apps SDK
- BudgetShared.js module (DateFormatter, CalendarWidget, ChoicesCategoryTree)

## Шаблон простой команды

```python
"""/{command_name} command handler."""

from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.api_client import get_api_client
from bot.utils.logger import get_logger
from bot.utils.session import SessionManager

logger = get_logger(__name__)


async def {command_name}_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /{command_name} command."""
    user = update.effective_user

    # Check authentication
    if not SessionManager.is_authenticated(context):
        await update.message.reply_text("❌ Требуется авторизация. Используйте /start")
        return

    try:
        # Fetch data from backend
        token = SessionManager.get_access_token(context)
        api_client = await get_api_client()
        data = await api_client.get("/endpoint", token=token)

        # Format response
        message = format_response(data)

        await update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error in /{command_name}: {e}", exc_info=True)
        await update.message.reply_text("❌ Произошла ошибка. Попробуйте позже.")
```

## Шаблон ConversationHandler (FR-001, FR-004)

```python
"""/{command_name} command with ConversationHandler."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.utils.api_client import get_api_client
from bot.utils.logger import get_logger
from bot.utils.session import SessionManager
from bot.utils.validators import validate_amount, ValidationError

logger = get_logger(__name__)

# Conversation states
SELECT_ARTICLE, ENTER_AMOUNT, ENTER_DATE, CONFIRM = range(4)

# Context keys
KEY_ARTICLE_ID = "article_id"
KEY_AMOUNT = "amount"
KEY_DATE = "date"


async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start /{command_name} conversation (FR-001)."""
    user = update.effective_user

    if not SessionManager.is_authenticated(context):
        await update.message.reply_text("❌ Требуется авторизация. Используйте /start")
        return ConversationHandler.END

    try:
        # Fetch articles from backend
        token = SessionManager.get_access_token(context)
        api_client = await get_api_client()
        articles = await api_client.get("/api/v1/articles?type=expense", token=token)

        if not articles:
            await update.message.reply_text("❌ Нет доступных статей расходов.")
            return ConversationHandler.END

        # Build hierarchical inline keyboard (FR-001 AC3)
        keyboard = build_article_keyboard(articles)

        # Clear previous conversation data
        context.user_data.pop(KEY_ARTICLE_ID, None)
        context.user_data.pop(KEY_AMOUNT, None)
        context.user_data.pop(KEY_DATE, None)

        await update.message.reply_text(
            "📋 **Добавление расхода**\\n\\n"
            "Шаг 1/3: Выберите статью расхода:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

        return SELECT_ARTICLE

    except Exception as e:
        logger.error(f"Error starting /{command_name}: {e}", exc_info=True)
        await update.message.reply_text("❌ Произошла ошибка.")
        return ConversationHandler.END


async def handle_article_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle article selection (inline button callback)."""
    query = update.callback_query
    await query.answer()

    try:
        article_id = int(query.data.split("_")[1])
        context.user_data[KEY_ARTICLE_ID] = article_id

        await query.edit_message_text(
            "📋 **Добавление расхода**\\n\\n"
            "Шаг 2/3: Введите сумму расхода:",
            parse_mode="Markdown"
        )

        return ENTER_AMOUNT

    except (ValueError, IndexError) as e:
        logger.error(f"Invalid article callback: {query.data}, error: {e}")
        await query.edit_message_text("❌ Ошибка. Попробуйте /cancel")
        return ConversationHandler.END


async def handle_amount_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle amount input validation (FR-001 AC4)."""
    user_input = update.message.text

    try:
        # Validate amount (positive number, max 2 decimal places)
        amount = validate_amount(user_input)
        context.user_data[KEY_AMOUNT] = amount

        await update.message.reply_text(
            "📋 **Добавление расхода**\\n\\n"
            "Шаг 3/3: Введите дату транзакции (DD.MM.YYYY) или отправьте /skip для текущей даты:"
        )

        return ENTER_DATE

    except ValidationError as e:
        await update.message.reply_text(f"❌ {e}\\n\\nПопробуйте ещё раз.")
        return ENTER_AMOUNT  # Retry same state


async def handle_date_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle date input or skip."""
    user_input = update.message.text

    if user_input == "/skip":
        context.user_data[KEY_DATE] = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            # Parse and validate date
            date = datetime.strptime(user_input, "%d.%m.%Y")
            context.user_data[KEY_DATE] = date.strftime("%Y-%m-%d")
        except ValueError:
            await update.message.reply_text("❌ Неверный формат даты. Используйте DD.MM.YYYY")
            return ENTER_DATE  # Retry

    # Show confirmation (FR-001 AC5)
    article_id = context.user_data[KEY_ARTICLE_ID]
    amount = context.user_data[KEY_AMOUNT]
    date = context.user_data[KEY_DATE]

    await update.message.reply_text(
        f"📋 **Подтверждение**\\n\\n"
        f"Статья: {article_id}\\n"
        f"Сумма: {amount} руб.\\n"
        f"Дата: {date}\\n\\n"
        f"Всё верно?",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Подтвердить", callback_data="confirm"),
                InlineKeyboardButton("❌ Отменить", callback_data="cancel")
            ]
        ]),
        parse_mode="Markdown"
    )

    return CONFIRM


async def handle_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle confirmation - create transaction via API."""
    query = update.callback_query
    await query.answer()

    if query.data == "cancel":
        await query.edit_message_text("❌ Отменено. Используйте /{command_name} для повтора.")
        return ConversationHandler.END

    try:
        # Get data from context
        article_id = context.user_data[KEY_ARTICLE_ID]
        amount = context.user_data[KEY_AMOUNT]
        date = context.user_data[KEY_DATE]

        # Create via API (FR-001 AC1, AC7)
        token = SessionManager.get_access_token(context)
        api_client = await get_api_client()

        payload = {
            "article_id": article_id,
            "amount": amount,
            "fact_date": date,
            "record_type": "fact",
        }

        response = await api_client.post("/api/v1/facts", data=payload, token=token)

        # Success (FR-001 AC5)
        await query.edit_message_text(
            f"✅ Расход успешно добавлен!\\n\\n"
            f"ID: {response['id']}",
            parse_mode="Markdown"
        )

        logger.info(f"Transaction created for user {update.effective_user.id}")
        return ConversationHandler.END

    except Exception as e:
        logger.error(f"Error creating transaction: {e}", exc_info=True)
        await query.edit_message_text("❌ Ошибка при создании. Попробуйте позже.")
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel conversation (FR-001 AC6)."""
    await update.message.reply_text("❌ Отменено. Используйте /{command_name} для повтора.")
    return ConversationHandler.END


def build_article_keyboard(articles: list[dict]) -> InlineKeyboardMarkup:
    """Build hierarchical inline keyboard (FR-001 AC3)."""
    buttons = [
        [InlineKeyboardButton(article["name"], callback_data=f"article_{article['id']}")]
        for article in articles
    ]
    return InlineKeyboardMarkup(buttons)


# Registration in bot.py:
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("{command_name}", command_start)],
    states={
        SELECT_ARTICLE: [CallbackQueryHandler(handle_article_selection)],
        ENTER_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount_input)],
        ENTER_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_date_input)],
        CONFIRM: [CallbackQueryHandler(handle_confirm)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
```

## Scheduled Jobs (APScheduler)

**Weekly Reports (FR-005):**
```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

async def send_weekly_reports():
    """Send weekly plan-fact reports to all users (FR-005)."""
    # FR-005 AC1: scheduled job
    # FR-005 AC2: plan, fact, deviation, top-3 articles
    # FR-005 AC3: respect user settings (can disable)
    pass

# FR-005 AC1: Sunday evening
scheduler.add_job(send_weekly_reports, 'cron', day_of_week='sun', hour=20, minute=0)
scheduler.start()
```

**Budget Alerts (FR-006):**
```python
async def check_budget_threshold(fact_amount, article_id, period_id):
    """Check if budget exceeded threshold (FR-006)."""
    # FR-006 AC1: check after adding new fact
    # FR-006 AC2: configurable threshold (default 90%)
    # FR-006 AC3: send alert to user
    # FR-006 AC4: disable via settings
    threshold = 0.90
    plan = await api_client.get(f"/api/v1/analytics/plan?article={article_id}&period={period_id}")

    if plan and fact_amount >= plan * threshold:
        await send_alert(user_id, f"⚠️ Превышен бюджет: {article_name}")
```

## Telegram Web App интеграция

**Menu Button Setup:**
```python
from telegram import MenuButtonWebApp, WebAppInfo

async def setup_menu_button(bot):
    """Setup Menu Button with Web App (Phase 3)."""
    web_app = WebAppInfo(url="https://your-domain.com/webapp/main")
    menu_button = MenuButtonWebApp(text="Меню", web_app=web_app)

    # Set for all users
    await bot.set_chat_menu_button(menu_button=menu_button)
```

## Проверочный чеклист

- [ ] Handler файл создан в `bot/handlers/{command_name}.py`
- [ ] Добавлена проверка аутентификации (SessionManager)
- [ ] Используется API client для взаимодействия с backend
- [ ] Добавлено логирование (logger)
- [ ] Валидация пользовательского ввода (validators)
- [ ] Обработка ошибок (try/except)
- [ ] Handler зарегистрирован в `bot/bot.py`
- [ ] Для ConversationHandler добавлен fallback (/cancel)
- [ ] Протестирована команда в Telegram
- [ ] Соответствует FR требованиям из PRD

## Связанные скилы

- **api-development**: для создания backend endpoints
- **testing**: для создания тестов bot handlers

## Примеры использования

### Пример 1: Простая команда (FR-003)

```
Создай команду /balance для показа баланса по всем ЦФО.
Получай данные из GET /api/v1/financial-centers/balance.
Форматируй ответ с эмодзи 💰.
```

### Пример 2: Multi-step команда (FR-001)

```
Реализуй команду /add для добавления расхода (FR-001 из PRD).
Шаги:
1. Выбрать статью (inline keyboard, иерархия)
2. Ввести сумму (валидация: положительное число, 2 знака)
3. Ввести дату (или skip для текущей)
4. Подтвердить
API: POST /api/v1/facts
Реализуй все 7 Acceptance Criteria из FR-001.
```

### Пример 3: Scheduled Job (FR-005)

```
Реализуй еженедельные отчеты (FR-005 из PRD).
- APScheduler: каждое воскресенье 20:00
- Формат: план, факт, отклонение, топ-3 статьи
- Уважай настройки пользователя (можно отключить)
- Все 4 Acceptance Criteria из FR-005.
```

## Часто задаваемые вопросы

**Q: Как передавать данные между состояниями ConversationHandler?**
A: Используй `context.user_data` dictionary

**Q: Как обработать timeout в conversation?**
A: Добавь `conversation_timeout=300` в ConversationHandler

**Q: Как интегрировать Telegram Web Apps?**
A: Setup Menu Button с WebAppInfo URL + используй Telegram.WebApp.initDataUnsafe для auth
