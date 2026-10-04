---
name: telegram-mtproto-api
description: Use this skill when creating or refactoring a backend-only Node.js/Express API that connects to Telegram directly using MTProto as a user client. It must implement Telegram phone login, optional 2FA password flow, local development session storage, minimal chat endpoints, and Swagger/OpenAPI documentation. Do not use Telegraf, Telegram Bot API, frontend code, BullMQ, Redis, PostgreSQL, or background workers unless the user explicitly asks for them.
---

# Telegram MTProto API Skill

This skill builds a backend-only Node.js/Express API for Telegram MTProto user-client access.

The default target is a minimal but clean backend that can:

- log in to Telegram using MTProto
- send login code to a phone number
- verify Telegram login code
- handle optional Telegram 2FA password
- save Telegram session locally for development
- return current Telegram user profile
- list chats/dialogs
- read messages from a chat
- send a text message to a chat
- expose Swagger/OpenAPI documentation for all REST endpoints

## Hard scope

Always follow these constraints unless the user explicitly asks otherwise:

- Backend only.
- Use Node.js and Express.
- Use the `telegram` npm package / GramJS MTProto client.
- Use Telegram MTProto as a user client.
- Do not use Telegraf.
- Do not use Telegram Bot API.
- Do not generate frontend code.
- Do not add BullMQ.
- Do not add Redis.
- Do not add PostgreSQL.
- Do not add background workers.
- Do not build large sync systems in the first version.
- Do not place MTProto logic inside Express controllers.
- Do not expose Telegram `api_hash` to frontend/client apps.
- Do not expose Telegram session strings to frontend/client apps.

## Recommended default dependencies

Use these dependencies unless the existing project already uses alternatives:

```json
{
  "express": "^4.18.0",
  "cors": "^2.8.5",
  "helmet": "^7.0.0",
  "dotenv": "^16.0.0",
  "joi": "^17.0.0",
  "jsonwebtoken": "^9.0.0",
  "morgan": "^1.10.0",
  "telegram": "^2.26.0",
  "swagger-jsdoc": "^6.2.8",
  "swagger-ui-express": "^5.0.1"
}
```

Development:

```json
{
  "nodemon": "^3.0.0"
}
```

## Required project structure

When creating a new project, prefer this structure:

```txt
src/
  app.js
  server.js

  config/
    env.js
    swagger.js
    telegram.js

  routes/
    auth.routes.js
    chat.routes.js
    docs.routes.js

  controllers/
    auth.controller.js
    chat.controller.js

  services/
    auth.service.js
    chat.service.js
    session.service.js
    telegramClient.service.js

  mtproto/
    clientFactory.js
    authFlow.js
    chats.js
    messages.js

  middlewares/
    auth.middleware.js
    validate.middleware.js
    error.middleware.js

  validators/
    auth.validator.js
    chat.validator.js

  utils/
    AppError.js
    asyncHandler.js
    logger.js

docs/
  get-telegram-api-keys.md
  auth-flow.md
  api-contract.md
  swagger.md
  security-notes.md

.env.example
README.md
package.json
```

## Required REST API

### Auth

- `POST /api/auth/send-code`
- `POST /api/auth/verify-code`
- `POST /api/auth/verify-password`
- `POST /api/auth/logout`
- `GET /api/auth/status`

### Telegram chat

- `GET /api/me`
- `GET /api/chats`
- `GET /api/chats/:chatId/messages`
- `POST /api/chats/:chatId/messages`

### API documentation

- `GET /api/docs`
- `GET /api/docs.json`

Swagger UI should be available at `/api/docs`.

OpenAPI JSON should be available at `/api/docs.json`.

## Required documentation

When creating a project with this skill, always generate:

- `README.md`
- `.env.example`
- `docs/get-telegram-api-keys.md`
- `docs/auth-flow.md`
- `docs/api-contract.md`
- `docs/swagger.md`
- `docs/security-notes.md`

Documentation must explain:

- This backend uses Telegram MTProto, not Telegram Bot API.
- The user must create Telegram API credentials from `my.telegram.org`.
- Required credentials are `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`.
- Credentials must be stored only in `.env`.
- Frontend/client apps must never receive `TELEGRAM_API_HASH`.
- Frontend/client apps must never receive Telegram session strings.
- Basic login flow:
  - send code
  - verify code
  - verify 2FA password if required
  - use backend JWT for later API calls
- Swagger UI is available at `/api/docs`.
- OpenAPI JSON is available at `/api/docs.json`.

## Environment variables

Always create `.env.example` with at least:

```env
PORT=5000
NODE_ENV=development

TELEGRAM_API_ID=123456
TELEGRAM_API_HASH=your_api_hash_here

JWT_SECRET=change_this_to_a_long_random_secret
JWT_EXPIRES_IN=7d

SESSION_STORAGE=file
SESSION_DIR=.sessions

CORS_ORIGIN=http://localhost:5173
LOG_LEVEL=info
```

## Architecture rules

Controllers must:

- parse request data
- call services
- return HTTP responses
- not contain MTProto implementation details

Services must:

- contain business logic
- call MTProto modules
- normalize Telegram responses for API output

MTProto modules must:

- directly interact with the `telegram` package
- hide GramJS-specific details from controllers
- return clean objects where possible

Session service must:

- save and load Telegram session strings
- support local file storage for development
- be replaceable later with encrypted database storage
- never send raw session strings to API clients

Swagger/OpenAPI must:

- document every public REST endpoint
- document request body schemas
- document success responses
- document common error responses
- include JWT bearer authentication where required
- not include Telegram `api_hash` or session strings in public schemas
- not mix Swagger annotations with MTProto business logic if a separate OpenAPI file is used

## Security rules

- Never commit `.env`.
- Never expose Telegram `api_hash` to frontend/client apps.
- Never expose Telegram session strings to frontend/client apps.
- Store sessions locally only for development.
- For production, recommend encrypted session storage.
- Use JWT for backend API authorization after Telegram login.
- Use validation middleware for request bodies and params.
- Do not implement scraping, spam, mass messaging, bypassing restrictions, account abuse, or automation that violates Telegram rules.

## Default implementation workflow

When the user asks to create a project:

1. Create package metadata and scripts.
2. Create `.env.example`.
3. Create Express app and server.
4. Create config modules.
5. Create session storage service.
6. Create Telegram client factory.
7. Create auth flow service.
8. Create chat service.
9. Create controllers and routes.
10. Create validators and middleware.
11. Create Swagger config and docs routes.
12. Add Swagger annotations or OpenAPI specs for all endpoints.
13. Create README and docs files.
14. Ensure no Telegraf/Bot API/BullMQ/Redis/PostgreSQL/frontend files were added.
15. Explain how to run and test login flow.

## Preferred Swagger approach

For small projects, use `swagger-jsdoc` comments inside route files or a separate `src/config/swagger.js` file.

For cleaner structure, prefer:

```txt
src/config/swagger.js
src/routes/docs.routes.js
```

Swagger dependencies:

```bash
npm install swagger-jsdoc swagger-ui-express
```

## Suggested user prompt

```txt
Use $telegram-mtproto-api.

Create a backend-only Node.js/Express Telegram MTProto API.

Requirements:
- Use MTProto user login with phone code and optional 2FA password.
- Implement local development session storage.
- Implement /api/me, /api/chats, get messages, and send text message endpoints.
- Add Swagger UI at /api/docs and OpenAPI JSON at /api/docs.json.
- Add .env.example and docs for getting TELEGRAM_API_ID and TELEGRAM_API_HASH.
- No frontend.
- No Telegraf.
- No Telegram Bot API.
- No BullMQ.
- No Redis.
- No PostgreSQL.
```
