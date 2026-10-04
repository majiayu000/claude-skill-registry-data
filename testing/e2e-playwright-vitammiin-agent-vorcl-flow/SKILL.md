---
name: e2e-playwright
description: "E2E-тестирование на Playwright — приоритет селекторов (getByRole > testid > css), fixtures и переиспользование auth-state (storageState), web-first assertions без sleep, trace/screenshot при падении, параллельность и шардинг в CI, паттерн Page Object. Use при написании, ревью или стабилизации браузерных e2e-тестов."
version: 1.0.0
---

# Навык: Playwright E2E

E2E проверяет **критический путь пользователя** в реальном браузере. Не дублируй unit/integration: e2e-набор маленький, медленный и самый дорогой в поддержке.

## 1. Селекторы (в порядке предпочтения)
1. `page.getByRole('button', { name: 'Сохранить' })` — как видит пользователь и скринридер; заодно проверяет a11y.
2. `getByLabel` / `getByPlaceholder` / `getByText` — поля форм и статичный текст.
3. `getByTestId('checkout-submit')` — когда роли/текста нет или текст нестабилен (i18n).
4. CSS/XPath — последний резерв: классы вёрстки меняются чаще всего.

## 2. Ожидания: только web-first assertions
```ts
await expect(page.getByRole('alert')).toHaveText(/сохранено/i); // сам ждёт и ретраит
```
- НИКАКИХ `page.waitForTimeout(3000)` / sleep — главный источник flaky.
- Web-first assertions (`toBeVisible`, `toHaveText`, `toHaveURL`, `toHaveCount`) авто-ретраятся до таймаута.
- Действия (`click`, `fill`) сами ждут actionability (visible, enabled, stable) — не оборачивай их ручными wait.

## 3. Auth: логин один раз через storageState
```ts
// auth.setup.ts (setup-проект)
await page.goto('/login'); // заполнить форму, отправить
await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
await page.context().storageState({ path: 'playwright/.auth/user.json' });
```
```ts
// playwright.config.ts
projects: [
  { name: 'setup', testMatch: /auth\.setup\.ts/ },
  { name: 'chromium', use: { storageState: 'playwright/.auth/user.json' }, dependencies: ['setup'] },
]
```
Логин через UI в каждом тесте — медленно и flaky. Разные роли пользователей — отдельные state-файлы + fixtures.

## 4. Диагностика падений
```ts
use: { trace: 'on-first-retry', screenshot: 'only-on-failure', video: 'retain-on-failure' }
```
Смотреть: `npx playwright show-trace trace.zip` (или `npx playwright show-report`) — таймлайн действий, DOM-снапшоты, сеть, консоль. Чини первопричину по trace, а не «подкручивай селектор» наугад.

## 5. Параллельность и шардинг
- Файлы гоняются параллельно (`workers`), тесты внутри файла — последовательно; каждый тест обязан быть независимым (свои данные).
- `fullyParallel: true` — только когда все тесты действительно изолированы.
- CI-шардинг: `npx playwright test --shard=1/4` … `--shard=4/4` на разных машинах; отчёты сливай `npx playwright merge-reports`.

## 6. CI-конфиг (минимум)
```ts
export default defineConfig({
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0, // retry — телеметрия flaky, не лекарство
  reporter: process.env.CI ? [['html'], ['github']] : 'list',
  use: { baseURL: process.env.BASE_URL ?? 'http://localhost:3000', trace: 'on-first-retry' },
  webServer: { command: 'npm run dev', url: 'http://localhost:3000', reuseExistingServer: !process.env.CI },
});
```
`webServer` сам поднимает приложение — тесты не требуют ручного запуска. Тест, прошедший только с retry, — flaky: чини, не считай зелёным.

## 7. Page Object — кратко
Выноси в класс страницы повторяющееся: локаторы + действия (`await checkout.submitOrder()`); assertions оставляй в тестах. Не строй POM ради POM на 3 теста — часто достаточно fixtures.

## 8. Гигиена
- Каждый тест сам готовит свои данные (API-сиды быстрее UI-кликов) и не зависит от соседей.
- Селектор упал после редизайна — обнови роль/имя, а не добавляй `nth(3)`.
- Visual-снапшоты — только для стабильных экранов, с отключёнными анимациями (`animations: 'disabled'`) и фиксированными шрифтами.
