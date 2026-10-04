---
name: nodejs
description: Серверная разработка на Node.js — событийный цикл (что блокирует, микро/макротаски), async-паттерны (Promise.all vs allSettled, AbortController-таймауты), поиск утечек памяти (--inspect, heap snapshot), worker_threads vs cluster, стримы и backpressure. Use при написании или отладке серверного кода на Node.js, зависании event loop, росте памяти, выборе воркеров/кластеризации.
---

# Навык: Node.js

## Событийный цикл
- Один поток исполняет JS; I/O (сеть, fs, DNS) уходит в libuv и не блокирует. Блокирует **синхронный CPU-код**: `JSON.parse`/`stringify` мегабайтных тел, `fs.readFileSync`, sync-крипто/sync-сжатие, regex с катастрофическим бэктрекингом, огромные циклы.
- Порядок исполнения: синхронный код → **микротаски** (`process.nextTick` — раньше всех, затем промисы/`queueMicrotask`) → **макротаски** по фазам (`setTimeout`/`setInterval` → I/O-коллбэки → `setImmediate`). Рекурсивные `nextTick`/микротаски морят I/O голодом; «уступить цикл» — это `setImmediate`, не `nextTick`.
- Диагностика зависаний: `monitorEventLoopDelay()` из `perf_hooks` в метрики; задержка цикла стабильно >100ms — где-то синхронный счёт. `--trace-sync-io` ловит sync-I/O после старта.
- CPU-тяжёлое (парсинг, хэши, изображения) — в `worker_threads` или async-версии API (`crypto.pbkdf2`, `zlib.gzip`), не sync.

## Async-паттерны
- **`Promise.all` vs `allSettled`**: `all` — «всё или ничего», первый reject роняет результат (незавершённые промисы продолжают работать!); `allSettled` — когда нужны все исходы, включая ошибки:
  ```ts
  const [user, orders] = await Promise.all([getUser(id), getOrders(id)]) // зависимые данные: любая ошибка = ошибка всего
  const results = await Promise.allSettled(urls.map(fetchOne))           // независимые задачи: разбираем каждый исход
  const ok = results.filter((r) => r.status === 'fulfilled').map((r) => r.value)
  ```
- **Таймауты и отмена — AbortController**, а не «гонка» с setTimeout:
  ```ts
  const res = await fetch(url, { signal: AbortSignal.timeout(5000) })   // встроенный таймаут
  const ac = new AbortController()                                      // отмена по внешнему событию
  req.on('close', () => ac.abort())
  await doWork({ signal: ac.signal })                                   // signal передавай вглубь всех вызовов
  ```
- Ограничивай параллелизм (пул на N задач, `p-limit`) — не пускай `Promise.all` на тысячи запросов разом.
- `unhandledRejection`/`uncaughtException` — обрабатывай (лог + graceful shutdown), не глотай.

## Утечки памяти
Симптом: RSS/heap растёт от запроса к запросу и не отпускается после GC.
1. Запусти с инспектором: `node --inspect app.js` → Chrome `chrome://inspect` (или `npx clinic heap`).
2. Сними **heap snapshot** до нагрузки → прогони нагрузку → второй снапшот → режим Comparison: что выросло по Retained Size и кто держит ссылку (Retainers).
3. Типовые виновники: глобальные Map/массивы-кэши без лимита (нужен LRU/TTL), слушатели без `removeListener` (симптом — MaxListeners warning), замыкания с большими объектами, незакрытые таймеры/сокеты.
4. Динамику без снапшотов — `process.memoryUsage()` в метрики; `--max-old-space-size` — страховка, не лечение.

## worker_threads vs cluster
| | worker_threads | cluster / несколько процессов |
|---|---|---|
| Задача | CPU-тяжёлые вычисления внутри сервиса | масштабирование HTTP-сервера на ядра |
| Память | общая возможна (SharedArrayBuffer), дешёвый обмен | изолирована; обмен только IPC/сеть |
| Падение | роняет только воркер | изолировано, supervisor перезапустит процесс |
| Когда | парсинг, сжатие, крипто, генерация PDF | production HTTP: PM2 / `node:cluster` / реплики k8s |

Воркеров держи пулом, не создавай на каждый запрос. В контейнерах для HTTP предпочитай реплики оркестратора, а не `cluster` внутри контейнера.

## Стримы и backpressure
- Большие файлы/ответы — стримами, не буферизуй целиком в память.
- `pipeline(src, transform, dst)` из `stream/promises` — сам пробрасывает ошибки и закрывает стримы (в отличие от голого `.pipe()`) и уважает backpressure: медленный потребитель притормаживает производителя.
