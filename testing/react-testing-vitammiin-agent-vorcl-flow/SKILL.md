---
name: react-testing
description: Тестирование React-компонентов — Testing Library + Vitest/Jest, поведенческие проверки от лица пользователя, MSW для мокинга сети. Use при написании или ревью тестов фронтенда.
version: 1.0.0
---

# Навык: React testing

Поведенческие тесты компонентов на **Testing Library** + **Vitest** (или Jest).

## Принцип
- Тестируй поведение, а не реализацию: то, что видит и делает пользователь.
- Ищи элементы по доступным ролям/тексту: `getByRole`, `getByLabelText`, `findByText`; избегай тестовых `data-testid`, где есть роль.
- Взаимодействие — через `@testing-library/user-event`, а не сырые `fireEvent`.

## Структура (AAA)
- Arrange (рендер + окружение) → Act (действие пользователя) → Assert (видимый результат).
- Оборачивай в нужные провайдеры (QueryClientProvider, стор, тема) через кастомный `renderWithProviders`.

## Сеть и данные
- Мокай **границу сети** через **MSW** (`msw`), а не внутренние модули.
- Для Query-компонентов давай свежий `QueryClient` на тест (без общего кэша), `retry: false`.

## Асинхронность
- `await findBy*` / `await waitFor(...)` для асинхронного UI; не тестируй по таймингу.
- Проверяй состояния loading/empty/error, а не только happy path.

## Пример
```tsx
test('показывает заказы', async () => {
  renderWithProviders(<OrdersList />);
  expect(await screen.findByText('Заказ #1')).toBeInTheDocument();
});
```
