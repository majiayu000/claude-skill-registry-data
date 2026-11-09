---
name: telegram-bot
description: "Создание Telegram-ботов: aiogram/python-telegram-bot/grammY, команды, кнопки, FSM, вебхуки, деплой"
whenToUse: "Применяй, когда нужно создать или доработать Telegram-бота (команды, инлайн-кнопки, диалоги, интеграции)"
---

# Telegram Bot

Гайд по разработке Telegram-ботов.

## Выбор стека

| Язык | Библиотека |
|------|-----------|
| Python (рекомендуется) | `aiogram` 3.x (async) или `python-telegram-bot` |
| Node.js/TypeScript | `grammY` или `telegraf` |

## Важные концепции

- **Long polling** — простой режим через `getUpdates`, подходит для дева и малых ботов.
- **Webhook** — для продакшена (быстрее, но нужен HTTPS-домен).
- **FSM (Finite State Machine)** — цепочки диалогов (`State`, `MemoryStorage`/`RedisStorage`).

## Чек-лист разработки

### Настройка
- [ ] Создай бота через @BotFather, сохрани токен в `.env` (не коммить)
- [ ] Установи библиотеку: `pip install aiogram` / `npm i grammy`
- [ ] Базовый скелет: dispatcher + роутеры + запуск polling

### Команды и обработчики
- [ ] `/start`, `/help` — приветствие и список возможностей
- [ ] Обработчики сообщений (`message`, `callback_query`, `inline_query`)
- [ ] Инлайн-кнопки (`InlineKeyboardMarkup`) и меню (`ReplyKeyboard`)
- [ ] FSM-диалоги для пошаговых сценариев (анкеты, заказы)

### Интеграции
- [ ] Хранение состояния: SQLite/Redis для FSM
- [ ] Интеграция с БД для данных пользователей
- [ ] Платежи (Telegram Payments API) или внешние сервисы при необходимости
- [ ] Webhooks: маршрут + регистрация через `setWebhook`

### Надёжность
- [ ] Обработка ошибок в хендлерах (middleware для логов/ошибок)
- [ ] Rate-limit и retry при сбоях API
- [ ] Graceful shutdown (закрыть polling/webhook)

### Деплой
- [ ] Docker-образ или `systemd`/pm2 для long-polling
- [ ] Для webhook — HTTPS (nginx/caddy + certbot)
- [ ] Логирование ошибок

## Правила
1. Токен бота — секрет, храни в env, не в репозитории.
2. Разделяй хендлеры по роутерам (фичи → модули).
3. Обрабатывай ошибки — бот не должен падать от одного кривого запроса.
4. Тестируй в @BotFather и реальном клиенте перед релизом.
