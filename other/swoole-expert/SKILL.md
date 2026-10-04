---
name: swoole-expert
description: Deep reference for writing production Swoole PHP code. Covers the long-running process mental model (object lifetimes, what breaks vs php-fpm, per-request state via Coroutine::getContext), runtime hook flags (what's hookable year-to-year, what isn't), parent/child priority gotcha, Channel/WaitGroup/Barrier/defer patterns, server canonical skeleton (SWOOLE_BASE default since 5.0, dispatch modes, graceful reload rules), connection pooling (try/finally + defer, Channel-as-pool), the full pitfalls catalog (blocking in coroutines, shared connections, pcntl, Channel deadlocks, cooperative != concurrent-safe, exception isolation), production tuning tables, testing entry point with Co\run, Swoole 6.x version notes (removed coroutine clients, multi-threading, io_uring, Lock API changes), and build flags. Use when writing or reviewing Swoole code (swoole/swoole-src, NOT openswoole) on Swoole 5.x/6.x with PHP 8.2+.
---

# Swoole Expert

Reference for **swoole/swoole-src** (NOT openswoole). Target: **Swoole 5.x/6.x**, **PHP 8.2+**. Assumes baseline coroutine/async knowledge. This file covers only what's house-specific, load-bearing, or shifts year-to-year.

Non-negotiable defaults:
- Prefer idiomatic `Co\run` / `go()` / `Co::defer` patterns
- Always enable `SWOOLE_HOOK_ALL` so native PHP I/O becomes coroutine-aware
- Never share a connection across coroutines -- use a pool
- Workers are **resident** processes, not short-lived like php-fpm

---

## 1. The long-running process mental model

Swoole workers are **resident PHP processes**. Unlike php-fpm, memory is NOT torn down between requests. Everything allocated at class, file, or worker scope survives across every request.

### Four object lifetimes

| Lifetime | Where created | Destroyed by |
|---|---|---|
| **Program-global** | Before `$server->start()` | Full process shutdown (`reload` will NOT refresh) |
| **Process-global** | In `onWorkerStart` | `max_request` reached, worker crash, or reload |
| **Session** | `onConnect` / first `onReceive` | `onClose` |
| **Request** | Inside the request handler | End of request |

If you allocated it in a hot path, assume it's a leak unless you can point to where it's freed.

### What does NOT work (vs php-fpm)

- **Superglobals**: `$_GET`, `$_POST`, `$_COOKIE`, `$_FILES`, `$_SERVER`, `$_REQUEST`, `$_SESSION` are NOT populated. Use `$request->get`, `$request->post`, `$request->cookie`, `$request->files`, `$request->server`, `$request->header`, `$request->rawContent()`.
- **`session_start()`** -- implement sessions with Redis/DB keyed by a cookie from `$request->cookie`.
- **`echo` / `print_r` / `var_dump`** -- go to stdout/log_file, NOT the client. Use `$response->write()` / `$response->end()`.
- **`exit()` / `die()`** -- kills the worker. Swoole 4.1+ converts to `Swoole\ExitException`. Never use for control flow.
- **`header()` / `setcookie()`** -- silent no-ops. Use `$response->header()`, `$response->cookie()`, `$response->status()`. Must be called BEFORE `$response->end()`.
- **Static properties / singletons / `global`** -- leak request state across coroutines. Use `Coroutine::getContext()`.
- **`pcntl_*`** -- forbidden in coroutines. Use `Swoole\Process` and `Process::signal()`.
- **Xdebug, phptrace, aop, molten, xhprof, phalcon** -- incompatible with coroutines. Disable them.

### Per-request state with `Coroutine::getContext()`

```php
use Swoole\Coroutine;

// Context is a Swoole\Coroutine\Context (extends ArrayObject),
// auto-destroyed when coroutine exits -- no cleanup needed.
$ctx = Coroutine::getContext();
$ctx['user_id']   = 42;
$ctx['requestId'] = bin2hex(random_bytes(8));

function innerFunction(): void
{
    $ctx = Coroutine::getContext();
    $userId = $ctx['user_id'];  // works from anywhere in the same coroutine
}
```

Do NOT stash `$this` in the context -- it holds a strong reference and usually leaks the controller.

---

## 2. Coroutines

### Creating and running

```php
Swoole\Coroutine::create(callable $fn, mixed ...$args): int|false
go(callable $fn, mixed ...$args): int|false  // short alias

Swoole\Coroutine\run(callable $fn): bool    // top-level entry point
Co\run(callable $fn): bool                   // alias
```

All coroutine-creating APIs must run inside a **coroutine container** — either `Co\run()`, a server event callback, or a `Process`/`Process\Pool` worker with `enable_coroutine = true`. Nesting `run()` inside another `run()` is forbidden.

### Introspection

```php
Swoole\Coroutine::getCid(): int                   // -1 if outside coroutine
Swoole\Coroutine::getPcid(int $cid = 0): int|false
Swoole\Coroutine::exists(int $cid): bool
Swoole\Coroutine::list(): Swoole\Coroutine\Iterator
Swoole\Coroutine::stats(): array                  // coroutine_num, coroutine_peak_num, ...
Swoole\Coroutine::getBackTrace(int $cid = 0, int $options = DEBUG_BACKTRACE_PROVIDE_OBJECT, int $limit = 0): array
Swoole\Coroutine::printBackTrace(int $cid = 0): void
Swoole\Coroutine::getElapsed(int $cid = 0): int   // milliseconds alive
```

### Key non-obvious behaviors

### Parent/child priority gotcha

When you call `go()`, the **child starts immediately** and runs until its first yield. Only then does `go()` return to the parent:

```php
echo "a\n";
go(function () {
    echo "b\n";
    Co::sleep(0.1);   // yields here
    echo "d\n";
});
echo "c\n";
// Output: a, b, c, d
```

Coroutines have no parent/child lifecycle -- a parent exiting does not cancel or wait for children. Use `Barrier` or `WaitGroup` to wait.

### Scheduling yield points

A coroutine runs until: hooked I/O, `Co::sleep()`, `Channel::push()`/`pop()`, `Coroutine::yield()`/`suspend()`, `WaitGroup::wait()`/`Barrier::wait()`.

**A CPU-bound loop with no I/O monopolizes the worker.** Sprinkle `Coroutine::sleep(0)` to voluntarily yield, or dispatch CPU work to a task worker.

### Coroutine config

```php
Swoole\Coroutine::set(array $options): void  // call BEFORE run() / Server->start()
```

| Option | Default | Note |
|---|---|---|
| `max_coroutine` | 100000 | Global limit |
| `stack_size` / `c_stack_size` | 2 MB | C stack per coroutine |
| `hook_flags` | 0 | One-click hooks, e.g. `SWOOLE_HOOK_ALL` |
| `enable_preemptive_scheduler` | false | Force preemption at 10 ms |
| `socket_connect_timeout` | | Default connect timeout |
| `socket_timeout` | | Read/write timeout |
| `dns_cache_expire` / `dns_server` | | DNS defaults |
| `enable_deadlock_check` | true | |

### Cancellation

```php
Swoole\Coroutine::cancel(int $cid, bool $throwException = false): bool  // $throwException added 6.1
Swoole\Coroutine::isCanceled(): bool
Swoole\Coroutine::setTimeLimit(float $seconds): void  // 6.2+
```

**Caveat**: `cancel()` cannot cancel file I/O coroutines; may segfault. Since 6.2 it can cancel in-flight io_uring ops.

---

## 3. Runtime hooks and flag reference

Hooks patch PHP's blocking stdlib to yield on I/O. Set **once** at bootstrap:

```php
Co::set(['hook_flags' => SWOOLE_HOOK_ALL]);
// Or: $server->set(['hook_flags' => SWOOLE_HOOK_ALL]);
```

### Flag reference (ext-swoole 6.x)

| Flag | Covers |
|---|---|
| `SWOOLE_HOOK_TCP` | TCP streams, fsockopen, mysqlnd-based PDO_MYSQL/mysqli, predis, php-amqplib |
| `SWOOLE_HOOK_UNIX` | Unix-domain stream sockets |
| `SWOOLE_HOOK_UDP` / `SWOOLE_HOOK_UDG` | UDP / Unix datagram |
| `SWOOLE_HOOK_SSL` / `SWOOLE_HOOK_TLS` | TLS streams |
| `SWOOLE_HOOK_SLEEP` | `sleep`, `usleep` (>= 1ms), `time_nanosleep`, `time_sleep_until` |
| `SWOOLE_HOOK_FILE` | `fopen`, `fread`, `fwrite`, `file_get_contents`, `file_put_contents`, `unlink`, `mkdir`, `rmdir`. Uses AIO or **io_uring** in 6.0+ |
| `SWOOLE_HOOK_STREAM_FUNCTION` | `stream_select()` |
| `SWOOLE_HOOK_BLOCKING_FUNCTION` | `gethostbyname`, `shell_*` |
| `SWOOLE_HOOK_PROC` | `proc_open`, `proc_close`, `proc_get_status`, `proc_terminate` |
| `SWOOLE_HOOK_NATIVE_CURL` | Real libcurl coroutinized -- **use this**, not legacy `SWOOLE_HOOK_CURL`. Requires `--enable-swoole-curl`. Guzzle/Symfony HttpClient work transparently |
| `SWOOLE_HOOK_CURL` | **Legacy** partial reimplementation. Avoid |
| `SWOOLE_HOOK_SOCKETS` | ext-sockets. Auto-dropped in 6.1.6+ if ext-sockets not loaded |
| `SWOOLE_HOOK_STDIO` | STDIN/STDOUT/STDERR |
| `SWOOLE_HOOK_PDO_PGSQL` | `pdo_pgsql` (5.1+; 6.1.7 added timeout) |
| `SWOOLE_HOOK_PDO_ODBC` | `pdo_odbc` (5.1+) |
| `SWOOLE_HOOK_PDO_ORACLE` | `pdo_oci` (5.1+). **Constant is `_ORACLE`, not `_OCI`** |
| `SWOOLE_HOOK_PDO_SQLITE` | `pdo_sqlite` (5.1+) -- requires sqlite serialized/multi-thread |
| `SWOOLE_HOOK_PDO_FIREBIRD` | `pdo_firebird` (**new 6.2**) |
| `SWOOLE_HOOK_MONGODB` | MongoDB (**new 6.2** via `Swoole\RemoteObject\Server`) |
| `SWOOLE_HOOK_NET_FUNCTION` | coroutine `gethostbyname` (6.2+) |
| `SWOOLE_HOOK_ALL` | All of the above |

### Not hookable (block -- don't use in a coroutine)

- `mysql` extension (libmysqlclient)
- `mongo` / `mongodb` (mongo-c-client) -- use the 6.2+ MongoDB hook instead
- `php-amqp` (C AMQP ext -- but `php-amqplib` over streams works)
- Any extension bypassing PHP's streams layer

`pdo_mysql` and `mysqli` hookable **only in mysqlnd mode**. Check `php -m | grep mysqlnd`.

---

## 4. Concurrency primitives

### `Swoole\Coroutine\Channel`

```php
final class Swoole\Coroutine\Channel {
    public int $capacity;
    public int $errCode;  // SWOOLE_CHANNEL_OK | _TIMEOUT | _CLOSED | _CANCELED

    public function __construct(int $capacity = 1);
    public function push(mixed $data, float $timeout = -1): bool;
    public function pop(float $timeout = -1): mixed;
    public function close(): bool;
    public function length(): int;
    public function isEmpty(): bool;
    public function isFull(): bool;
    public function stats(): array;
}
```

**Gotchas**:
- Pushing `false`/`null`/`0` is ambiguous -- `pop()` also returns `false` on close/timeout. Always check `$chan->errCode`.
- `close()` wakes ALL waiting producers/consumers; they return `false`.
- Create channels in `onWorkerStart`, not before `start()`.

**Channel as semaphore** (capacity N, pre-filled):

```php
$sem = new Channel(5);
for ($i = 0; $i < 5; $i++) $sem->push(true);

go(function () use ($sem) {
    $sem->pop();
    try { doLimitedWork(); } finally { $sem->push(true); }
});
```

### `Swoole\Coroutine\WaitGroup`

```php
final class Swoole\Coroutine\WaitGroup {
    public function __construct(int $delta = 0);
    public function add(int $delta = 1): void;
    public function done(): void;
    public function wait(float $timeout = -1): bool;  // false on timeout
    public function count(): int;
}
```

Always call `done()` in `finally` -- if a worker throws and skips `done()`, `wait()` hangs.

### `Swoole\Coroutine\Barrier` (preferred over WaitGroup)

```php
use Swoole\Coroutine\Barrier;

$barrier = Barrier::make();
for ($i = 0; $i < 4; $i++) {
    go(function () use ($barrier) {  // capturing $barrier bumps refcount
        Co::sleep(0.5);
    });
}
Barrier::wait($barrier);  // by reference; nulled after wait
```

`wait()` takes the barrier **by reference**. If you forget `use ($barrier)` the child doesn't hold a ref and `wait()` returns immediately.

### `defer` -- Go-style cleanup

```php
go(function () {
    $db = new PDO(/* ... */);
    defer(fn() => $db = null);  // runs on coroutine exit, LIFO order, even on exception
});
```

### Timers

```php
Swoole\Timer::tick(int $msec, callable $cb, mixed ...$params): int
Swoole\Timer::after(int $msec, callable $cb, mixed ...$params): int
Swoole\Timer::clear(int $timer_id): bool
Swoole\Timer::clearAll(): bool
Swoole\Timer::info(int $timer_id): ?array
Swoole\Timer::list(): Swoole\Timer\Iterator
Swoole\Timer::stats(): array
```

Callback: `function(int $timerId, mixed ...$params): void`. In a coroutine container, timer callbacks run inside a new coroutine automatically.

### Batch primitives

```php
Swoole\Coroutine\batch(array $tasks, float $timeout = -1): array    // concurrent callables
Swoole\Coroutine\parallel(int $n, callable $fn): void               // N copies of $fn
Swoole\Coroutine\map(array $list, callable $fn, float $timeout = -1): array
Swoole\Coroutine::join(array $cids, float $timeout = -1): bool      // wait by cid
```

---

## 5. HTTP / WebSocket / TCP servers

### Canonical HTTP server skeleton

```php
<?php
declare(strict_types=1);

use Swoole\Http\{Server, Request, Response};

$server = new Server('0.0.0.0', 9501, SWOOLE_BASE);

$server->set([
    'worker_num'            => swoole_cpu_num() * 2,
    'task_worker_num'       => 4,
    'task_enable_coroutine' => true,
    'max_request'           => 10_000,
    'max_wait_time'         => 60,
    'reload_async'          => true,
    'hook_flags'            => SWOOLE_HOOK_ALL,
    'http_compression'      => true,
    'log_file'              => '/var/log/swoole.log',
    'log_level'             => SWOOLE_LOG_INFO,
    'package_max_length'    => 8 * 1024 * 1024,
]);

$server->on('request', function (Request $request, Response $response): void {
    $method = $request->server['request_method'] ?? 'GET';
    $uri    = $request->server['request_uri']    ?? '/';
    $body   = $request->rawContent();
    $response->status(200);
    $response->header('Content-Type', 'application/json');
    $response->end(json_encode(['method' => $method, 'uri' => $uri]));
});

$server->on('workerStart', function (Server $server, int $workerId): void {
    // Reset per-worker state, open DB/Redis pools here
});

$server->start();
```

### Server constructor

```php
new Swoole\Server(
    string $host = '0.0.0.0',
    int $port = 0,
    int $mode = SWOOLE_BASE,           // SWOOLE_BASE (default), SWOOLE_PROCESS, SWOOLE_THREAD (6.0+ ZTS)
    int $sock_type = SWOOLE_SOCK_TCP
)
```

`Http\Server` and `WebSocket\Server` extend `Swoole\Server` with the same constructor. SSL: OR sock type with `SWOOLE_SSL`.

### All server events

```
onStart(Server $server)                    // master start; NOT in SWOOLE_BASE mode
onShutdown(Server $server)
onManagerStart(Server $server)             // NOT in SWOOLE_BASE mode
onManagerStop(Server $server)
onBeforeReload(Server $server)             // 4.5+
onAfterReload(Server $server)              // 4.5+
onWorkerStart(Server $server, int $workerId)
onWorkerStop(Server $server, int $workerId)
onWorkerExit(Server $server, int $workerId)   // fires when reload_async and worker is draining
onWorkerError(Server $server, int $workerId, int $workerPid, int $exitCode, int $signal)
onBeforeShutdown(Server $server)           // 4.8+
onPipeMessage(Server $server, int $srcWorkerId, mixed $message)

// TCP
onConnect(Server $server, int $fd, int $reactorId)
onReceive(Server $server, int $fd, int $reactorId, string $data)
onPacket(Server $server, string $data, array $clientInfo)   // UDP
onClose(Server $server, int $fd, int $reactorId)

// Task workers
onTask(Server $server, Swoole\Server\Task $task)
onFinish(Server $server, int $taskId, mixed $data)

// HTTP
onRequest(Swoole\Http\Request $request, Swoole\Http\Response $response)

// WebSocket
onHandShake(Http\Request $request, Http\Response $response): bool
onOpen(WebSocket\Server $server, Http\Request $request)
onMessage(WebSocket\Server $server, WebSocket\Frame $frame)
```

### Core server methods

```php
public function set(array $settings): bool;
public function on(string $event, callable $callback): bool;
public function start(): bool;
public function stop(int $workerId = -1): bool;
public function shutdown(): bool;
public function reload(bool $onlyReloadTaskworker = false): bool;

public function send(int|string $fd, string $data, int $serverSocket = -1): bool;
public function close(int $fd, bool $reset = false): bool;
public function exists(int $fd): bool;
public function pause(int $fd): bool;
public function resume(int $fd): bool;

public function task(mixed $data, int $workerIdx = -1, ?callable $finishCb = null): int|false;
public function taskwait(mixed $data, float $timeout = 0.5, int $workerIdx = -1): mixed;
public function taskCo(array $tasks, float $timeout = 0.5): array|false;
public function finish(mixed $data): bool;

public function sendMessage(mixed $message, int $dstWorkerId): bool;
public function addProcess(Swoole\Process $process): int|false;

public function getClientInfo(int $fd, int $reactorId = -1): false|array;
public function getWorkerId(): int|false;
public function stats(): array;
```

### `Swoole\Http\Request` properties

```php
public int    $fd;
public int    $streamId;
public array  $header;     // lowercase keys
public array  $server;     // request_method, request_uri, query_string, request_time, remote_addr, ...
public ?array $cookie;
public array  $get;
public array  $post;
public array  $files;

public function rawContent(): string|false;   // alias getContent()
public function getMethod(): string|false;
```

### `Swoole\Http\Response` methods

```php
public function status(int $httpCode, string $reason = ''): bool;
public function header(string $key, string|array $value, bool $format = true): bool;
public function cookie(string $name, string $value = '', int $expires = 0,
    string $path = '/', string $domain = '', bool $secure = false, bool $httponly = false,
    string $samesite = '', string $priority = ''): bool;
public function trailer(string $key, string $value): bool;
public function write(string $content): bool;     // chunked; disables compression
public function end(?string $content = null): bool;
public function sendfile(string $filename, int $offset = 0, int $length = 0): bool;
public function redirect(string $location, int $httpCode = 302): bool;
public function detach(): bool;

// Upgrade to WebSocket from an HTTP server
public function upgrade(): bool;
public function push(Frame|string $data, int $opcode = WEBSOCKET_OPCODE_TEXT, int $flags = WEBSOCKET_FLAG_FIN): bool;
public function recv(float $timeout = 0): Frame|string|false;
public function close(): bool;
```

### Server modes

**Default mode changed from `SWOOLE_PROCESS` to `SWOOLE_BASE` in 5.0.** `SWOOLE_BASE` has no manager process -- workers accept directly. `SWOOLE_THREAD` (6.0+) requires ZTS PHP.

### Dispatch modes

| Mode | Constant | Use for |
|---|---|---|
| 1 | `SWOOLE_DISPATCH_ROUND` | Stateless, async only; `onConnect`/`onClose` suppressed |
| 2 | `SWOOLE_DISPATCH_FDMOD` | Stateful TCP (fd % worker_num) |
| 3 | `SWOOLE_DISPATCH_IDLE_WORKER` | Preemptive to idle worker -- recommended for HTTP |
| 4 | `SWOOLE_DISPATCH_IPMOD` | Sticky by client IP |
| 5 | `SWOOLE_DISPATCH_UIDMOD` | Sticky by `$server->bind($fd, $uid)` |
| 7 | `SWOOLE_DISPATCH_STREAM` | Workers `accept` themselves |
| 9 | `SWOOLE_DISPATCH_CO_REQ_LB` | Coroutine request LB (best for stateless HTTP) |

### Response gotchas

- `end()` can only be called **once**.
- `status()`/`header()`/`cookie()` must be called **before** the first `write()` or `end()`.
- `write()` switches to chunked transfer and disables compression.

### Task workers

```php
// Fire-and-forget
$server->task(['job' => 'resize', 'file' => $file]);

// Concurrent batch (requires task_enable_coroutine=true)
$results = $server->taskCo([['job' => 'a'], ['job' => 'b']], 5.0);
```

**Caveat**: `task()`/`taskwait()` only callable from event workers. Prefer `taskCo()` when `task_enable_coroutine=true`.

### WebSocket server

WS-specific methods:

```php
public function push(int $fd, Frame|string $data, int $opcode = WEBSOCKET_OPCODE_TEXT, int $flags = WEBSOCKET_FLAG_FIN): bool;
public function isEstablished(int $fd): bool;    // NOT exists() -- use this for WS
public function disconnect(int $fd, int $code = WEBSOCKET_CLOSE_NORMAL, string $reason = ''): bool;
public function ping(int $fd, string $data = ''): bool;
```

Use `$server->isEstablished($fd)` (NOT `exists()`) to check WS connection. `onHandShake` gives full control of the handshake; `onOpen` fires after the built-in one.

**Broadcast pattern**:

```php
foreach ($server->connections as $fd) {
    if ($server->isEstablished($fd)) $server->push($fd, $payload);
}
```

### TCP packet framing

`open_length_check` + `package_length_type` delivers complete packets to `onReceive`. EOF variant: `'open_eof_split' => true, 'package_eof' => "\r\n"`.

### Graceful reload

- `$server->reload()` -> workers finish in-flight, exit, get replaced.
- `reload_async=true`: old workers keep running current coroutines. `onWorkerExit` fires when done.
- **Smooth reload only picks up files `require`'d inside `onWorkerStart`**. Files required before `start()` stay cached forever.
- If `opcache.validate_timestamps=0`, add `opcache_reset()` at the top of `onWorkerStart`.

---

## 6. Process and Process\Pool

### `Swoole\Process`

```php
final class Swoole\Process {
    public int $pipe;
    public int $pid;
    public int $id;

    public function __construct(
        callable $callback,
        bool $redirectStdinStdout = false,
        int $pipeType = SOCK_DGRAM,    // 0=none, 1=SOCK_STREAM, 2=SOCK_DGRAM
        bool $enableCoroutine = false
    );

    public function start(): bool|int;
    public function write(string $data): int|false;
    public function read(int $size = 8192): string|false;

    // Sysv message queue IPC
    public function useQueue(int $key = 0, int $mode = 2, int $capacity = -1): bool;
    public function push(string $data): bool;
    public function pop(int $size = 65536): string|false;

    public function exportSocket(): Swoole\Coroutine\Socket|false;
    public function name(string $name): bool;
    public function exit(int $exitCode = 0): void;

    public static function wait(bool $blocking = true): array|false;
    public static function signal(int $signalNo, ?callable $callback = null): bool;
    public static function kill(int $pid, int $signalNo = SIGTERM): bool;
    public static function daemon(bool $nochdir = true, bool $noclose = true, array $pipes = []): bool;
}
```

`$enableCoroutine = true` makes the callback run inside a coroutine scheduler. Signal handling: use `Swoole\Process::signal()`, not `pcntl_signal()`.

```php
Swoole\Process::signal(SIGTERM, fn() => $server->shutdown());
Swoole\Process::signal(SIGINT,  fn() => $server->shutdown());
```

### `Swoole\Process\Pool`

```php
final class Swoole\Process\Pool {
    public function __construct(
        int $workerNum,
        int $ipcType = SWOOLE_IPC_NONE,   // 0=none, 1=UNIXSOCK, 2=MSGQUEUE, 3=SOCKET
        int $msgqueueKey = 0,
        bool $enableCoroutine = false
    );
    public function set(array $settings): void;
    public function on(string $event, callable $cb): bool;
    public function getProcess(int $workerId = -1): Process|false;
    public function listen(string $host, int $port = 0, int $backlog = 2048): bool;
    public function write(string $data): bool;
    public function sendMessage(string $data, int $dstWorkerId): bool;
    public function start();
    public function stop(): void;
    public function shutdown(): bool;
}
```

Minimal supervised worker pool -- bring your own protocol, no reactor. Good for "run my callable across N processes with shared TCP socket". Events: `WorkerStart`, `WorkerStop`, `Message`, `Start`, `Shutdown`.

**Pool vs Server**: `Pool` has no `onConnect`/`onReceive`/HTTP/WS. `Server` is the full reactor + protocol helpers.

---

## 7. Shared memory -- Table, Atomic, Lock

### `Swoole\Table`

Mmap'd shared hash table -- the only way to share state across workers. Per-row spinlocks + CAS.

```php
final class Swoole\Table implements Iterator, Countable {
    public const TYPE_INT    = 1;
    public const TYPE_FLOAT  = 2;
    public const TYPE_STRING = 3;

    public function __construct(int $tableSize, float $conflictProportion = 0.2);
    public function column(string $name, int $type, int $size = 0): bool;
    public function create(): bool;
    public function destroy(): bool;

    public function set(string $key, array $value): bool;
    public function get(string $key, ?string $field = null): mixed;
    public function exists(string $key): bool;
    public function del(string $key): bool;
    public function count(): int;
    public function incr(string $key, string $column, int|float $incrby = 1): int|float;
    public function decr(string $key, string $column, int|float $incrby = 1): int|float;
    public function getSize(): int;
    public function getMemorySize(): int;
    public function stats(): array|false;
}
```

```php
$table = new Swoole\Table(8192);
$table->column('name',  Swoole\Table::TYPE_STRING, 64);
$table->column('age',   Swoole\Table::TYPE_INT);
$table->column('score', Swoole\Table::TYPE_FLOAT);
$table->create();  // MUST create before $server->start()

$server->table = $table;  // attach so workers can reach it
```

**Gotchas**:
- `TYPE_STRING` columns have fixed byte length; overflow silently truncated.
- Size ~30% over peak for collision chains.
- In 5.0+, `Table` **no longer implements `ArrayAccess`** -- use `set()`/`get()`.

### Atomic / Lock

`Swoole\Atomic` -- shared-memory counters (32-bit unsigned; `Atomic\Long` for 64-bit signed). `wait()`/`wakeup()` are futex-style and **block the entire process** -- use `Channel` in event workers instead.

`Swoole\Lock` -- **process-level, NOT coroutine-safe**. If a coroutine holds the lock and yields, deadlock. Use `Channel(1)` for coroutine-safe mutex. In 6.1+: API unified to `lock($op = LOCK_EX, $timeout = -1)`, `unlock()`. `lockwait()`/`trylock()` removed.

---

## 8. Coroutine clients

### `Swoole\Coroutine\Http\Client`

```php
new Swoole\Coroutine\Http\Client(string $host, int $port, bool $ssl = false)
// $host = IP, domain (async DNS), or unix://tmp/foo.sock. Do NOT pass http:// prefix.
```

**Properties**: `$errCode`, `$errMsg`, `$statusCode` (negative = network issue), `$body`, `$headers`, `$cookies`, `$set_cookie_headers`.

Negative statusCode constants: `-1` CONNECT_FAILED, `-2` REQUEST_TIMEOUT, `-3` SERVER_RESET, `-4` SEND_FAILED.

```php
set(array $options): void
setMethod(string $method): void
setHeaders(array $headers): void
setCookies(array $cookies): void
setData(string|array $data): void
addFile(string $path, string $name, ?string $mime = null, ?string $filename = null, int $offset = 0, int $length = 0): void
addData(string $data, string $name, ?string $mime = null, ?string $filename = null): void
get(string $path): bool
post(string $path, mixed $data): bool
download(string $path, string $filename, int $offset = 0): bool
upgrade(string $path): bool        // websocket handshake
push(mixed $data, int $opcode = WEBSOCKET_OPCODE_TEXT, int $flags = WEBSOCKET_FLAG_FIN): bool
recv(float $timeout = 0): Frame|false
close(): bool
```

**Functional shortcuts** (`Swoole\Coroutine\Http` namespace, >= 4.6.4):

```php
use function Swoole\Coroutine\Http\{get, post, request};
$resp = get('https://httpbin.org/get?hello=world');
```

### `Swoole\Coroutine\Socket`

Low-level coroutine-native socket for custom protocols.

```php
new Swoole\Coroutine\Socket(int $domain, int $type, int $protocol);

bind(string $address, int $port = 0): bool
listen(int $backlog = 0): bool
accept(float $timeout = 0): Co\Socket|false
connect(string $host, int $port = 0, float $timeout = 0): bool
send(string $data, float $timeout = 0): int|false
sendAll(string $data, float $timeout = 0): int|false
recv(int $length = 65536, float $timeout = 0): string|false
recvAll(int $length, float $timeout = 0): string|false
recvPacket(float $timeout = 0): string|false   // uses framing from setProtocol()
recvLine(int $length = 65536, float $timeout = 0): string|false
setProtocol(array $settings): bool              // same framing options as Server->set()
checkLiveness(): bool
close(): bool
```

### Removed coroutine clients (6.0+)

**Removed entirely**: `Swoole\Coroutine\MySQL`, `Coroutine\Redis`, `Coroutine\PostgreSQL`. Use hooked PDO/ext-redis with `SWOOLE_HOOK_ALL`. Never generate code using these for 6.x.

---

## 9. Hooked PDO and curl

### Hooked PDO

With `SWOOLE_HOOK_ALL`, native `PDO` becomes coroutine-aware transparently.

**One-connection-per-coroutine rule** -- a single PDO handle is **not safe** across concurrent coroutines. The socket is bound to one coroutine; interleaved use corrupts the wire protocol. Use `PDOPool`.

**Persistent connections are NOT compatible** -- always `PDO::ATTR_PERSISTENT => false`.

**SQLite caveat**: `pdo_sqlite` hook requires SQLite in serialized/multi-threaded mode. Since 6.1.5, `PDO::sqliteCreateAggregate/Collation/Function` removed in coroutine mode.

### Hooked curl

**Use `SWOOLE_HOOK_NATIVE_CURL`** (included in `SWOOLE_HOOK_ALL`), not legacy `SWOOLE_HOOK_CURL`. **Guzzle and Symfony HttpClient work transparently**:

```php
Co\run(function () {
    $guzzle = new \GuzzleHttp\Client();
    $resp   = $guzzle->get('https://httpbin.org/get');  // coroutine-aware, no changes needed
});
```

---

## 10. Connection pooling

`swoole/library` ships with ext-swoole (auto-loaded via `swoole.enable_library=On`).

### Canonical pattern -- "put it back or leak"

**A pool connection that isn't returned is lost forever.** Always `try/finally`:

```php
use Swoole\Database\{PDOConfig, PDOPool};

$pool = new PDOPool(
    (new PDOConfig())
        ->withDriver('mysql')
        ->withHost('127.0.0.1')
        ->withPort(3306)
        ->withDbname('app')
        ->withCharset('utf8mb4')
        ->withUsername('app')
        ->withPassword('secret')
        ->withOptions([PDO::ATTR_EMULATE_PREPARES => false]),
    size: 32,
);

go(function () use ($pool) {
    $pdo = $pool->get();
    try {
        $stmt = $pdo->prepare('SELECT id, email FROM users WHERE id = :id');
        $stmt->execute(['id' => 1]);
    } finally {
        $pool->put($pdo);  // MUST return, even on exception
    }
});

// Or cleaner with defer:
go(function () use ($pool) {
    $conn = $pool->get();
    Co::defer(fn() => $pool->put($conn));
    // ... use $conn ...
});
```

**Pool notes**:
- `get(-1)` blocks forever; `get($timeout)` returns `false` on timeout.
- `put(null)` signals broken connection -- pool decrements count, rebuilds next `get()`.
- `PDOProxy` auto-reconnects on lost-connection exceptions outside transactions.
- **Transactions must begin and commit on the same connection.** Don't return mid-transaction.
- `RedisPool` / `MysqliPool` follow the same shape.
- **SQLite restriction**: `PDOPool` rejects `:memory:` and empty DB names.

### Channel-as-pool pattern

```php
final class GrpcPool
{
    private Channel $channel;

    public function __construct(
        private readonly \Closure $factory,
        private readonly int $size = 32,
    ) {
        $this->channel = new Channel($size);
        for ($i = 0; $i < $size; $i++) {
            $this->channel->push(($this->factory)());
        }
    }

    public function get(float $timeout = -1): object
    {
        $conn = $this->channel->pop($timeout);
        if ($conn === false) throw new \RuntimeException('pool exhausted or closed');
        return $conn;
    }

    public function put(object $conn): void { $this->channel->push($conn); }
}
```

---

## 11. Pitfalls catalog

### Never block inside a coroutine

These stall the whole worker (not just one coroutine):
- `mysql`/`mysqli`/`pdo_mysql` **without** `mysqlnd + hooks`
- `sleep()` without `SWOOLE_HOOK_SLEEP`
- `curl_*` without `SWOOLE_HOOK_NATIVE_CURL`
- `file_*`/`fread`/`fwrite` without `SWOOLE_HOOK_FILE`
- Any extension bypassing PHP streams

**Fix**: `SWOOLE_HOOK_ALL` at bootstrap. Exclude flags only when a library fights the scheduler (e.g. `SWOOLE_HOOK_ALL ^ SWOOLE_HOOK_TCP` for PHPMailer raw SMTP).

### Sharing a connection across coroutines

Swoole error: `"redis client has already been bound to another coroutine"`. PDO/Redis/socket handles are bound to the first coroutine. **Always pool, one checkout per coroutine.**

**Multiple processes must not share connections either.** Create per-worker pools in `onWorkerStart`, not program-global.

### `pcntl_*` is forbidden

`pcntl_fork`/`pcntl_signal`/`pcntl_waitpid` conflict with Swoole's `signalfd`. Use `Swoole\Process`, `Process::signal()`, `Coroutine\System::waitSignal()`.

### `go()` in `onStart` / `onManagerStart`

`onStart` runs in the master. Coroutine APIs there can conflict with `dispatch_func` and `package_length_func`. Put bootstrap in **`onWorkerStart`**.

### Channel deadlocks

`Channel::pop()` with default `timeout = -1` hangs forever if all producers exited and channel is empty. **Always pass a timeout**, or pair with `$channel->close()`.

### Cooperative != concurrent-safe

Read-modify-write across an I/O boundary is a data race:

```php
// WRONG
$count = $table->get('k', 'count');
$count++;  // yield possible if I/O runs
$table->set('k', ['count' => $count]);

// RIGHT
$table->incr('k', 'count');
```

### Exception handling across coroutines

Exceptions **cannot** cross coroutine boundaries. `go(fn() => throw new X)` inside an outer `try/catch` does nothing. Every top-level `go()` closure needs its own `try/catch`.

### Stashing `$this` in context

`Coroutine::getContext()['controller'] = $this` keeps the controller alive -- usually a leak. Stash only data.

### Framework compatibility

| Framework | Status |
|---|---|
| Hyperf | **Swoole-native**, production-ready |
| Webman | Fast, Swoole driver available |
| Imi | Swoole-native |
| Laravel Octane | Works, but use `app->scoped()` not `singleton()` for request-adjacent services |
| Slim / Mezzio | Work via PSR-15 bridges, not Swoole-aware |
| Phalcon | **Incompatible** -- C extension, globals-heavy |

---

## 12. Production tuning

### Worker sizing

| Setting | Guidance |
|---|---|
| `worker_num` | Default `swoole_cpu_num()`. Async/coroutine: 1-4x cores |
| `task_worker_num` | `(tasks/sec / tasks/worker/sec)`. Default 0 |
| `max_request` | Respawn after N requests. Mitigates leaks. **No effect in SWOOLE_BASE.** 10k-50k reasonable |
| `max_wait_time` | Drain timeout on reload/shutdown. 30-60s for HTTP |
| `reload_async` | **Set `true`** for graceful coroutine reload |
| `max_coroutine` | Per-worker cap, default 100000 |

### Buffers

| Setting | Default | Note |
|---|---|---|
| `package_max_length` | 2 MB | Max packet / HTTP POST body |
| `buffer_output_size` | 2 MB | Max `send()` payload. Memory = `worker_num x size` |
| `socket_buffer_size` | 2 MB | Per-connection send buffer |

### SSL / HTTP/2 / compression

- `ssl_cert_file` / `ssl_key_file`: PEM. Set `SWOOLE_SSL` socket flag.
- `open_http2_protocol`: requires `--enable-http2`.
- `http_compression`: gzip/brotli/zstd (6.0+ added zstd).

### Daemon / logs

- **`daemonize`**: `false` under systemd/Docker/k8s. Only `true` from interactive shell.
- **`log_file`**: use absolute paths (CWD changes after daemonize).
- `SIGRTMIN` reopens the log after logrotate.
- `log_rotation`: `SWOOLE_LOG_ROTATION_DAILY|HOURLY|MONTHLY`.

### Kernel tuning (Linux)

```
ulimit -n 262140
net.core.somaxconn = 65535
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_max_syn_backlog = 81920
net.core.wmem_max = 16777216
net.core.rmem_max = 16777216
net.unix.max_dgram_qlen = 100
```

Do **not** set `net.ipv4.tcp_tw_recycle = 1` -- removed in Linux 4.12, unsafe with NAT.

---

## 13. Testing

### PHPUnit entry point

```php
public function testAsync(): void
{
    $result = null;
    \Swoole\Coroutine\run(function () use (&$result) {
        $client = new \Swoole\Coroutine\Http\Client('httpbin.org', 443, true);
        $client->get('/ip');
        $result = $client->body;
    });
    self::assertNotNull($result);
}
```

### Resetting state

Workers are resident -- static state persists. In `setUp()`: reset singletons, run each test in its own `Co\run` (fresh context), `Timer::clearAll()`. In `tearDown()` assert `Coroutine::stats()['coroutine_num'] === 0` -- non-zero means a leak.

### IDE stubs

```bash
composer require --dev swoole/ide-helper
```

PHPStan: add `vendor/swoole/ide-helper/src/swoole/constants.php` to `bootstrapFiles`.

---

## 14. Swoole 6.x version notes

### 6.0 (2024-12)

- **Removed**: `Coroutine\MySQL`, `Coroutine\Redis`, `Coroutine\PostgreSQL`. Use hooked PDO.
- Requires PHP 8.1+.
- **Multi-threading**: `SWOOLE_THREAD`, `Swoole\Thread`, `Thread\Map/ArrayList/Queue/Lock/Barrier/Atomic`. Requires ZTS + `--enable-swoole-thread`.
- **io_uring** for file AIO: `--enable-iouring`.
- `Swoole\Async\Client` (non-blocking TCP/UDP/Unix).
- zstd HTTP compression.
- Non-blocking reentrant coroutine mutex.

### 6.1 (2025-10)

- **llhttp** replaces `http_parser`.
- **Lock API unified**: `lock($op = LOCK_EX, $timeout = -1)`, `unlock()`. `lockwait()`/`trylock()` **removed**.
- Coroutine cancellation gains `$throwException` -> throws `CanceledException`.
- WebSocket: `disconnect()`, `ping()`, fragmented messages.
- Runtime hooks can **only** be set in main thread, before child threads.
- 6.1.5: `PDO::sqliteCreateAggregate/Collation/Function` removed from coroutine mode.
- 6.1.6: auto-strips `SWOOLE_HOOK_SOCKETS` if ext-sockets not loaded.
- 6.1.7: hooked `pdo_pgsql` gained timeout.

### 6.2 (2026-04)

- Requires **PHP 8.2+**. Supports up to PHP 8.5.
- Coroutine **FTP** (`--enable-swoole-ftp`) and **SSH** (`--with-swoole-ssh2`) clients.
- `SWOOLE_HOOK_PDO_FIREBIRD`, `SWOOLE_HOOK_MONGODB`, `SWOOLE_HOOK_NET_FUNCTION`.
- `Coroutine::setTimeLimit()` -- per-coroutine timeout.
- HTTP over io_uring sockets: `--enable-uring-socket`.
- `--enable-openssl` removed (always on). `liburing >= 2.8` required.
- `Coroutine::cancel()` cancels in-flight io_uring ops.

### Build flags cheatsheet

```bash
./configure --enable-swoole \
  --enable-sockets \
  --enable-swoole-thread \       # requires ZTS
  --enable-swoole-curl \          # SWOOLE_HOOK_NATIVE_CURL
  --enable-swoole-pgsql \
  --enable-swoole-sqlite \
  --with-swoole-firebird \        # 6.2+
  --with-swoole-ssh2 \            # 6.2+
  --enable-swoole-ftp \           # 6.2+
  --enable-iouring \              # Linux io_uring
  --enable-uring-socket \         # 6.2+
  --enable-brotli \
  --enable-zstd \                 # 6.0+
  --enable-cares                  # c-ares DNS
```

### swoole/library version alignment

`swoole/library` is bundled into ext-swoole and auto-loaded. Composer releases are tagged for 6.1 and 6.2 (latest v6.2.3 as of 2026-09), so `composer require swoole/library` resolves to 6.2.x. Treat the extension as source of truth for library classes in production.

---

## Quick reference -- canonical program skeleton

```php
<?php
declare(strict_types=1);

use Swoole\Coroutine;
use Swoole\Coroutine\{Barrier, Channel};
use function Swoole\Coroutine\run;

Coroutine::set([
    'hook_flags'            => SWOOLE_HOOK_ALL,
    'max_coroutine'         => 10_000,
    'socket_timeout'        => 5,
    'enable_deadlock_check' => true,
]);

run(function (): void {
    $jobs    = new Channel(32);
    $results = new Channel(32);
    $barrier = Barrier::make();

    for ($w = 0; $w < 4; $w++) {
        go(function () use ($jobs, $results, $barrier): void {
            while (($job = $jobs->pop()) !== false) {
                $results->push(['job' => $job, 'pid' => getmypid()]);
            }
        });
    }

    go(function () use ($jobs, $barrier): void {
        foreach (range(1, 20) as $i) $jobs->push($i);
        $jobs->close();
    });

    go(function () use ($results, $barrier): void {
        defer(fn() => $results->close());
        $collected = [];
        for ($i = 0; $i < 20; $i++) {
            $msg = $results->pop(5.0);
            if ($msg === false) break;
            $collected[] = $msg;
        }
        var_dump($collected);
    });

    Barrier::wait($barrier);
});
```
