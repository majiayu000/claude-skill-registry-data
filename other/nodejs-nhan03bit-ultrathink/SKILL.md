---
name: nodejs
description: Node.js runtime patterns, streams, worker threads, clustering, event loop optimization, and production-grade server architecture
layer: domain
category: backend
triggers:
  - "node.js"
  - "nodejs"
  - "express"
  - "worker threads"
  - "node streams"
  - "clustering"
  - "event loop"
  - "node performance"
inputs:
  - "Backend architecture requirements"
  - "Performance bottleneck descriptions"
  - "Scaling requirements"
outputs:
  - "Node.js implementation patterns"
  - "Performance optimization strategies"
  - "Production deployment configurations"
linksTo:
  - websockets
  - message-queues
  - microservices
  - graphql
  - prisma
  - drizzle
  - redis
linkedFrom:
  - error-handling
  - logging
  - testing
preferredNextSkills:
  - prisma
  - redis
  - microservices
  - websockets
fallbackSkills:
  - python
  - golang
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Node.js Domain Skill

## Purpose

Provide expert-level guidance on Node.js runtime patterns, server architecture, performance optimization, and production deployment. This skill covers the entire Node.js ecosystem from event loop internals to clustering strategies.

## Key Patterns

### 1. Event Loop Awareness

The event loop is single-threaded. Never block it.

```javascript
// BAD: Blocking the event loop
const data = fs.readFileSync('/large-file.json');
const parsed = JSON.parse(data); // Blocks for large files

// GOOD: Non-blocking with streams
const stream = fs.createReadStream('/large-file.json');
const parsed = await pipeline(stream, new JSONParseStream());
```

**Phases to understand:**
- **Timers**: `setTimeout`, `setInterval` callbacks
- **Pending callbacks**: I/O callbacks deferred from previous cycle
- **Poll**: Retrieve new I/O events; execute I/O callbacks
- **Check**: `setImmediate` callbacks
- **Close**: `socket.on('close')` callbacks

Use `setImmediate()` to yield to the event loop during CPU-intensive synchronous work:

```javascript
function processLargeArray(array, callback) {
  const CHUNK = 1000;
  let index = 0;

  function doChunk() {
    const limit = Math.min(index + CHUNK, array.length);
    for (; index < limit; index++) {
      processItem(array[index]);
    }
    if (index < array.length) {
      setImmediate(doChunk); // Yield to event loop
    } else {
      callback();
    }
  }
  doChunk();
}
```

### 2. Streams

Always prefer streams for large data. The four stream types:

```javascript
import { Readable, Writable, Transform, pipeline } from 'node:stream';
import { pipeline as pipelineAsync } from 'node:stream/promises';

// Transform stream for processing data chunks
class CSVToJSON extends Transform {
  constructor() {
    super({ objectMode: true });
    this.headers = null;
  }

  _transform(chunk, encoding, callback) {
    const line = chunk.toString().trim();
    if (!this.headers) {
      this.headers = line.split(',');
      return callback();
    }
    const values = line.split(',');
    const obj = Object.fromEntries(
      this.headers.map((h, i) => [h, values[i]])
    );
    this.push(obj);
    callback();
  }
}

// Use pipeline for proper error handling and cleanup
await pipelineAsync(
  fs.createReadStream('data.csv'),
  new CSVToJSON(),
  new Transform({
    objectMode: true,
    transform(obj, enc, cb) {
      cb(null, JSON.stringify(obj) + '\n');
    }
  }),
  fs.createWriteStream('output.jsonl')
);
```

**Backpressure handling:** Always respect `writable.write()` returning `false`:

```javascript
async function* generateData() {
  for (let i = 0; i < 1_000_000; i++) {
    yield Buffer.from(`line ${i}\n`);
  }
}

// pipeline handles backpressure automatically
await pipelineAsync(
  Readable.from(generateData()),
  fs.createWriteStream('output.txt')
);
```

### 3. Worker Threads

Use for CPU-intensive operations. NOT for I/O (the event loop handles I/O efficiently).

```javascript
// worker-pool.js
import { Worker } from 'node:worker_threads';
import { cpus } from 'node:os';

class WorkerPool {
  #workers = [];
  #queue = [];
  #activeWorkers = 0;

  constructor(workerPath, poolSize = cpus().length - 1) {
    this.workerPath = workerPath;
    this.poolSize = poolSize;
  }

  async execute(data) {
    return new Promise((resolve, reject) => {
      const task = { data, resolve, reject };

      if (this.#activeWorkers < this.poolSize) {
        this.#runTask(task);
      } else {
        this.#queue.push(task);
      }
    });
  }

  #runTask(task) {
    this.#activeWorkers++;
    const worker = new Worker(this.workerPath, {
      workerData: task.data
    });

    worker.on('message', (result) => {
      task.resolve(result);
      this.#activeWorkers--;
      if (this.#queue.length > 0) {
        this.#runTask(this.#queue.shift());
      }
    });

    worker.on('error', (err) => {
      task.reject(err);
      this.#activeWorkers--;
      if (this.#queue.length > 0) {
        this.#runTask(this.#queue.shift());
      }
    });
  }

  async shutdown() {
    // Wait for all active tasks to complete
    while (this.#activeWorkers > 0) {
      await new Promise(r => setTimeout(r, 100));
    }
  }
}

// Usage
const pool = new WorkerPool('./hash-worker.js');
const results = await Promise.all(
  files.map(file => pool.execute({ filePath: file }))
);
```

### 4. Clustering

Use the cluster module or PM2 for multi-process scaling:

```javascript
import cluster from 'node:cluster';
import { cpus } from 'node:os';
import process from 'node:process';

const WORKERS = parseInt(process.env.WEB_CONCURRENCY) || cpus().length;

if (cluster.isPrimary) {
  console.log(`Primary ${process.pid} starting ${WORKERS} workers`);

  for (let i = 0; i < WORKERS; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.error(`Worker ${worker.process.pid} died (${signal || code})`);
    if (code !== 0) {
      console.log('Starting replacement worker...');
      cluster.fork();
    }
  });
} else {
  // Workers share the TCP connection
  const app = createServer();
  app.listen(process.env.PORT || 3000);
  console.log(`Worker ${process.pid} started`);
}
```

### 5. Graceful Shutdown

Always implement graceful shutdown in production:

```javascript
class GracefulServer {
  #server;
  #connections = new Set();
  #isShuttingDown = false;

  constructor(app) {
    this.#server = app.listen(process.env.PORT || 3000);
    this.#server.on('connection', (conn) => {
      this.#connections.add(conn);
      conn.on('close', () => this.#connections.delete(conn));
    });

    process.on('SIGTERM', () => this.shutdown());
    process.on('SIGINT', () => this.shutdown());
  }

  async shutdown() {
    if (this.#isShuttingDown) return;
    this.#isShuttingDown = true;

    console.log('Graceful shutdown initiated...');

    // Stop accepting new connections
    this.#server.close(() => {
      console.log('Server closed');
      process.exit(0);
    });

    // Close idle connections
    for (const conn of this.#connections) {
      conn.end();
    }

    // Force close after timeout
    setTimeout(() => {
      console.error('Forcing shutdown after timeout');
      for (const conn of this.#connections) {
        conn.destroy();
      }
      process.exit(1);
    }, 30_000);
  }
}
```

## Best Practices

1. **Use `node:` protocol** for built-in modules: `import fs from 'node:fs/promises'`
2. **Prefer `node:fs/promises`** over callback-based `fs`
3. **Use `AbortController`** for cancellable operations
4. **Set `--max-old-space-size`** appropriately for memory-intensive apps
5. **Enable source maps** in production: `--enable-source-maps`
6. **Use `node --watch`** for development (Node 18+)
7. **Validate environment variables** at startup with libraries like `envalid`
8. **Use structured logging** (pino, winston) -- never `console.log` in production
9. **Set proper `keep-alive` timeouts** on HTTP servers (must exceed load balancer timeout)
10. **Always handle `unhandledRejection`** and `uncaughtException`**

```javascript
process.on('unhandledRejection', (reason, promise) => {
  logger.error({ reason, promise }, 'Unhandled rejection');
  // In production, trigger graceful shutdown
});

process.on('uncaughtException', (error) => {
  logger.fatal({ error }, 'Uncaught exception');
  // Must exit -- state is unreliable after uncaught exception
  process.exit(1);
});
```

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Blocking event loop with `JSON.parse` on large payloads | All requests stall | Use streaming JSON parser or worker threads |
| Not handling backpressure in streams | Memory exhaustion | Use `pipeline()`, check `.write()` return value |
| Memory leaks from event listeners | OOM crashes | Remove listeners on cleanup, use `AbortController` |
| Using `cluster` with stateful sessions | Inconsistent state | Use Redis for session storage |
| Not setting `server.keepAliveTimeout` | 502 errors behind load balancers | Set higher than LB timeout (e.g., 65s) |
| Sync operations in async context | Degraded throughput | Audit for sync calls: `readFileSync`, `execSync` |
| Ignoring `ERR_USE_AFTER_CLOSE` | Silent failures | Always check stream state before operations |

## Performance Checklist

- [ ] No synchronous I/O in request handlers
- [ ] Streams used for files > 10MB
- [ ] Worker threads for CPU tasks > 50ms
- [ ] Connection pooling for databases
- [ ] Graceful shutdown implemented
- [ ] Memory leak monitoring in place
- [ ] HTTP keep-alive configured correctly
- [ ] Clustering or PM2 for multi-core utilization
