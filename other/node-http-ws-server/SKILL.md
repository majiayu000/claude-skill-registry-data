---
name: node-http-ws-server
description: The node:http plus ws server for a Node Web Only project - src/ module layout, routing, static serving from public/, the WebSocket upgrade, broadcast, and graceful shutdown. Use when building or changing the backend server, adding a route or an API endpoint, serving the frontend, handling realtime messages, or deciding where an error is caught. Triggers on createServer, WebSocketServer, noServer, server.on('upgrade'), wss.handleUpgrade, serveStatic, path traversal guards, SIGTERM, and process.exit.
user-invocable: false
---

# Node HTTP and WebSocket Server

**One `node:http` server handles both HTTP and the WebSocket upgrade, serves the vendored `public/` frontend, and shuts down on a signal.**

Builtins do everything except the WebSocket protocol itself, which is what `ws` is there for.

## Modules

`src/` is organized by feature, not by technical layer, so a change to authentication touches one file.

```
src/
├── server.js       # node:http server, upgrade handler, graceful shutdown
├── router.js       # request routing and static serving from public/
├── auth.js         # hashing, session cookies, users.json
├── state.js        # state.json read and atomic write
├── config.js       # defaults plus config.json deep merge
└── ws.js           # websocket message dispatch and broadcast
```

Each module exports the functions its callers need and nothing more. A default-export grab-bag makes every consumer import the whole surface and hides which parts are actually used.

## The Server

```js
import { createServer } from 'node:http';
import { WebSocketServer } from 'ws';
import { route } from './router.js';
import { handleMessage } from './ws.js';

function log(level, msg) {
    console.log(`${new Date().toISOString()} ${level} ${msg}`);
}

export function createApp(config) {
    const server = createServer((req, res) => route(req, res, config));
    const wss = new WebSocketServer({ noServer: true });

    server.on('upgrade', (req, socket, head) => {
        const { pathname } = new URL(req.url, 'http://localhost');
        if (pathname !== '/ws') {
            socket.destroy();
            return;
        }
        wss.handleUpgrade(req, socket, head, (ws) => wss.emit('connection', ws, req));
    });

    wss.on('connection', (ws) => {
        ws.on('message', (data) => handleMessage(wss, ws, data));
        ws.on('error', (err) => log('ERROR', `ws: ${err.message}`));
    });

    return { server, wss };
}
```

One listener serves both protocols. A second listener would need a second port, a second firewall rule, and a second TLS certificate to deliver what one upgrade handler already does.

`ws` runs in `noServer` mode so the handshake completes by hand, which is what makes it possible to reject or authenticate a connection before the socket is accepted rather than after.

An unexpected upgrade path is destroyed rather than upgraded, so the server does not hold open sockets for endpoints it does not serve.

## Shutdown

```js
export function start(config) {
    const { server, wss } = createApp(config);

    server.listen(config.port, config.host, () => {
        log('INFO', `listening on ${config.host}:${config.port}`);
    });

    let closing = false;
    const shutdown = (signal) => {
        if (closing) return;
        closing = true;
        log('INFO', `${signal} received, shutting down`);
        for (const client of wss.clients) client.close(1001, 'server shutdown');
        server.close(() => process.exit(0));
        setTimeout(() => process.exit(1), 10_000).unref();
    };
    process.on('SIGTERM', () => shutdown('SIGTERM'));
    process.on('SIGINT', () => shutdown('SIGINT'));

    return { server, wss };
}
```

WebSocket clients are closed explicitly with code 1001, because `server.close` stops accepting new connections and waits for existing ones, and an open socket never finishes on its own.

The force-exit timer is `unref`'d so it never keeps the process alive by itself. It fires only when `server.close` is still waiting on a stuck connection after the grace period.

The `closing` guard makes a second signal a no-op, since a user pressing Ctrl+C twice should not start two shutdown sequences.

## Routing and Static Serving

`route` dispatches API paths and hands everything else to static serving.

```js
import { readFile } from 'node:fs/promises';
import { join, normalize, extname } from 'node:path';
import { fileURLToPath } from 'node:url';

const PUBLIC_DIR = fileURLToPath(new URL('../public/', import.meta.url));

const MIME = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.ico': 'image/x-icon',
    '.woff2': 'font/woff2',
};

export async function route(req, res, config) {
    const url = new URL(req.url, 'http://localhost');
    try {
        if (url.pathname === '/api/health') {
            return sendJSON(res, 200, { status: 'ok' });
        }
        if (url.pathname.startsWith('/api/')) {
            return sendJSON(res, 404, { error: 'not found' });
        }
        return await serveStatic(url.pathname, res);
    } catch (err) {
        console.error(`${new Date().toISOString()} ERROR ${req.method} ${url.pathname}: ${err.message}`);
        return sendJSON(res, 500, { error: 'internal error' });
    }
}

async function serveStatic(pathname, res) {
    const rel = pathname === '/' ? 'index.html' : pathname.slice(1);
    const target = normalize(join(PUBLIC_DIR, rel));
    if (!target.startsWith(PUBLIC_DIR)) {
        res.writeHead(403).end();
        return;
    }
    try {
        const body = await readFile(target);
        res.writeHead(200, { 'Content-Type': MIME[extname(target)] ?? 'application/octet-stream' });
        res.end(body);
    } catch (err) {
        if (err.code === 'ENOENT' || err.code === 'EISDIR') {
            const index = await readFile(join(PUBLIC_DIR, 'index.html'));
            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(index);
            return;
        }
        throw err;
    }
}

function sendJSON(res, status, body) {
    res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(body));
}
```

`route` is `async` and `await`s the static path inside its own `try`. A synchronous `try` around a returned promise never sees the rejection, and Node terminates the process on an unhandled one, so the boundary would exist in the source and not in the running program.

`PUBLIC_DIR` ends in a separator, which is what makes `startsWith` on the normalized absolute path a real traversal guard: without the trailing separator, a sibling directory whose name shares the prefix would pass.

An unknown non-API path falls back to `index.html` so a client-routed deep link loads the app instead of a 404, while an unknown `/api/` path returns a JSON 404 rather than the HTML page.

The `MIME` table is explicit and short. A dependency for eight content types is a version to track in exchange for a lookup.

## WebSocket Messages

Messages are JSON objects carrying a `type` string, with the rest of the object as that type's payload.

```js
export function broadcast(wss, message) {
    const data = JSON.stringify(message);
    for (const client of wss.clients) {
        if (client.readyState === client.OPEN) {
            client.send(data);
        }
    }
}

export function handleMessage(wss, ws, raw) {
    let msg;
    try {
        msg = JSON.parse(raw);
    } catch {
        return;
    }
    switch (msg.type) {
        case 'ping':
            ws.send(JSON.stringify({ type: 'pong' }));
            break;
        case 'broadcast':
            broadcast(wss, { type: 'message', payload: msg.payload });
            break;
        default:
            ws.send(JSON.stringify({ type: 'error', error: 'unknown type' }));
    }
}
```

`broadcast` serializes once outside the loop, since the payload is identical for every recipient.

Sockets not in the `OPEN` state are skipped, because sending on a closing socket throws and would abort the broadcast partway through the client list.

A frame that is not valid JSON is dropped silently. Replying to it invites a client stuck in a bad state to loop.

## Error Boundaries

Feature modules return or throw and never call `process.exit`. `process.exit` and signal handlers belong to the entry layer, which is the Node equivalent of keeping context and logging at the boundaries.

Task-style helpers such as storage, hashing, and parsing throw or return as they are, with no logging and no wrapping for its own sake. Letting the error keep its `code`, such as `ENOENT`, is what allows a caller to branch on it.

`route` is the boundary. It wraps its body in `try`/`catch`, awaits everything async inside it, logs with an `ERROR` prefix, and sends a generic 500. A stack trace or an internal message in the response tells an attacker about paths and versions the page was never meant to disclose.

Catching inside `route`, with an `await` on every async call it makes, is what keeps a rejected handler from taking down the process. `process.on('uncaughtException')` is not part of normal control flow, since by the time it fires the process state is already unknown.
