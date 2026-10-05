---
name: miniprogram-implement
description: Implement miniprogram application with best practices, start's with "miniprogram" template, built with a fixed technology stack Taro, express, scss, typescript, TCB PostgreSQL, and DOES NOT support framework switching. This skill will init codebase and provide useful template information.
_meta_type: template
_meta_template_name: miniprogram
---

## Prerequisites

Initialize Project (if needed):
```bash
REPO_ROOT/.genie/scripts/bash/setup-project.sh miniprogram
```

**Generate `docs/product/features.md` before writing any code** — product overview, core features, user stories, page structure, data models, API endpoints.

**Validation**: If `docs/product/features.md` does not exist, STOP and create it first.

**Keep `docs/product/features.md` updated** as requirements evolve during development.

## Core Principles

Carefully consider what the user wants, fully utilize your skills, find the right skills, and plan it.
- Leverage the best design by SKILL: `ui-ux-pro-max`
- Use SKILL `text-to-image` for generating images, icons, or illustrations when needed.
- Use the SKILL `*-integrator` to fully realize the user's needs.

## Best Practices

### General Principles

- **Perfect Architecture**: Refactor when needed, eliminate duplication, maintain clean separation
- **Less is More**: Quality over quantity unless enterprise landing page requested
- **Leverage Existing Dependencies**: Prefer existing libraries over new ones

### MiniProgram-Specific (Automatic for All Pages)

- Chinese UI text for all user-facing content
- Mobile-first design (750px design width)
- Use px unit (28px body text, 88px button height) - auto-converted to rpx/rem
- Touch targets minimum 88px (44px physical)
- WeChat Green (#07C160) for primary actions
- Card-based layout with vertical scroll

## MiniProgram Template Architecture

```
/
├── backend/                        # Express.js + TypeScript
│   ├── package.json
│   ├── tsconfig.json
│   ├── jest.config.js
│   ├── .env.example / .env
│   └── src/
│       ├── index.ts                # Server entry point
│       ├── app.ts                  # Express configuration
│       ├── config/
│       │   ├── env.ts              # Environment validation (Zod)
│       │   └── logger.ts           # Pino logger factory
│       ├── modules/                # Feature modules (routes + handlers)
│       │   └── [resource].ts
│       ├── types/
│       │   └── [resource].types.ts # Zod schemas
│       ├── middleware/
│       │   ├── errorHandler.ts
│       │   ├── validation.ts
│       │   └── logger.ts
│       └── __tests__/
│
└── frontend/                       # Taro 4.x + React 18
    ├── package.json
    ├── tsconfig.json
    ├── project.config.json         # WeChat miniprogram config
    ├── babel.config.js
    ├── config/                     # Taro build configuration
    │   ├── index.ts                # Base config (esnextModules: ['taro-ui'])
    │   ├── dev.ts
    │   └── prod.ts
    └── src/
        ├── app.tsx                 # Root component (Taro UI styles import)
        ├── app.config.ts           # App config (pages, window, tabBar)
        ├── app.scss                # Global styles
        ├── pages/
        │   └── [page]/
        │       ├── index.tsx
        │       ├── index.scss
        │       └── index.config.ts
        ├── components/             # Reusable components
        ├── services/
        │   └── api-client.ts       # Taro.request wrapper
        ├── assets/
        │   ├── images/
        │   └── tabbar/             # TabBar icons (PNG)
        └── types/
```


## Technical References

Detailed implementation patterns in `references/`:

- **[api-protocol.md](references/api-protocol.md)**: JSON-based API standard (CRITICAL - no URL parameters for data operations)
- **[frontend-patterns.md](references/frontend-patterns.md)**: Taro component mapping, navigation, storage, styling
- **[architecture.md](references/architecture.md)**: Complete monorepo structure, key files, commands
- **[publish-guide.md](references/publish-guide.md)**: 小程序发布流程指引（AppID/密钥获取、体验版、审核上架）

## Quick Reference

### Adding New Resources

**Frontend:**
1. Define types in `src/types/[resource].ts`
2. Create API functions in `src/services/[resource].ts` using JSON-based calls
3. Build Page/Components using Taro UI components

**Backend:**
1. Create types in `src/types/[resource].types.ts`
2. Create module in `src/modules/[resource].ts`
3. Register router in `src/app.ts`

### Key Commands

```bash
# Frontend
npm run dev:h5       # H5 development (browser testing)
npm run dev:weapp    # WeChat MiniProgram development

# Debugging
python3 "$PROJECT_ROOT/.genie/scripts/python/fetch_monitor_errors.py"
```

### Critical Rules

1. **⚠️ NO `*` Selector**: WeChat WXSS does NOT support the `*` universal selector. **NEVER use Tailwind CSS** in miniprogram — it injects `* { ... }` base styles that cause `unexpected token '*'` compile errors. Use SCSS with Taro UI instead
2. **JSON Protocol**: All data operations use POST with JSON body, not URL parameters
3. **Component Mapping**: Use Taro components (`View`, `Text`, `Image`), NOT HTML elements
4. **Navigation**: Use Taro APIs (`Taro.navigateTo`, `Taro.switchTab`), NOT React Router
5. **Storage**: Use `Taro.setStorageSync`/`getStorageSync`, NOT localStorage
6. **Taro UI Components**: Use existing components, DO NOT create custom versions
7. **AtInput onChange**: Receives value directly, NOT event object
8. **⚠️ NEVER USE process.env**: Causes "ReferenceError: process is not defined". Use `Taro.getEnv()` for environment detection
9. **ScrollView Padding**: Wrap content in View container, padding on ScrollView doesn't work
10. **Fixed Bottom**: Use `bottom: 100px` directly, SCSS conditional compilation doesn't work
11. **⚠️ 750px Design Width**: Use px unit based on 750px design (28px=14px physical, 88px=44px physical). Taro auto-converts to rpx/rem
12. **⚠️ API Client Import**: Use `apiClient.post()` NOT `{ post }` - see below
13. **⚠️ Zod Schema Structure**: Validation middleware expects `{ body, query, params }` wrapper - see below
14. **⚠️ LOCAL IMAGES IN CSS**: NEVER use `background-image: url(...)` with local paths in SCSS/CSS. WeChat error: "本地资源图片无法通过 WXSS 获取". Use `<Image>` component instead - see below

### ⚠️ Common Runtime Errors - MUST AVOID

**Error 1: process is not defined**
```
ReferenceError: process is not defined
```
**Cause**: Using `process.env.XXX` anywhere in frontend code
**Solution**: Use `Taro.getEnv()` instead. Use existing `src/services/api-client.ts`.

**Error 2: post is not a function**
```
TypeError: (0 , _api_client__WEBPACK_IMPORTED_MODULE_2__.post) is not a function
```
**Cause**: Wrong import - trying to destructure non-existent named exports
**Solution**: 
```typescript
// ✅ CORRECT - use instance methods
import { apiClient } from '@/services/api-client';
// or
import apiClient from '@/services/api-client';

// Use full path with /api prefix
const data = await apiClient.post<ResponseType>('/api/users/list', body);
const data = await apiClient.get<ResponseType>('/api/health');

// ❌ WRONG - no named exports exist
import { post, get } from '@/services/api-client';  // ERROR!
```

**Error 3: Zod validation fails (400 Bad Request)**
```
400 Bad Request - Validation failed
```
**Cause**: Zod schema missing `body` wrapper
**Solution**:
```typescript
// ❌ WRONG - flat structure
export const createUserSchema = z.object({
  name: z.string(),
  phone: z.string()
});

// ✅ CORRECT - must wrap with body
export const createUserSchema = z.object({
  body: z.object({
    name: z.string(),
    phone: z.string()
  })
});
```

**Error 4: 本地资源图片无法通过 WXSS 获取**
```
[渲染层网络层错误] pages/xxx/index.wxss 中的本地资源图片无法通过 WXSS 获取
```
**Cause**: Using `background-image: url(./local-path)` in SCSS/CSS.
**Solution**: Use `<Image>` component instead. `background-color` and `linear-gradient()` are fine — only `url()` with local paths is blocked.

### Launch Configuration

`.cloudstudio` file defines startup - DO NOT modify. Always use unified process script.