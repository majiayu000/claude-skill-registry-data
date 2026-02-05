---
name: express-nodejs-expert
description: Expert knowledge of Express.js and Node.js for building production-ready web applications and APIs. Covers middleware patterns, routing, async/await error handling, security, performance optimization, proxy patterns, static file serving, and production deployment. Use when working with server.js, adding routes, implementing middleware, debugging Express issues, or optimizing API endpoints.
---

# Express.js & Node.js Expert

This skill provides comprehensive expert knowledge of Express.js web framework and Node.js runtime for building robust, secure, and performant web applications and API servers.

## Express Application Structure

### Basic Application Setup

**Minimal Express app**:
```javascript
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
```

**Production-ready structure**:
```javascript
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(helmet()); // Security headers
app.use(cors()); // CORS support
app.use(morgan('combined')); // Logging
app.use(express.json()); // Parse JSON bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies
app.use(express.static('public')); // Serve static files

// Routes
app.use('/api', require('./routes/api'));

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    error: {
      message: err.message,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
});

// Start server
const server = app.listen(port, () => {
  console.log(`Server running in ${process.env.NODE_ENV || 'development'} mode on port ${port}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  server.close(() => {
    console.log('HTTP server closed');
  });
});

module.exports = app;
```

## Middleware Patterns

### Middleware Execution Order

**Order matters**:
```javascript
// 1. Security middleware (first)
app.use(helmet());

// 2. Logging
app.use(morgan('combined'));

// 3. Body parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 4. CORS
app.use(cors());

// 5. Static files
app.use(express.static('public'));

// 6. Custom middleware
app.use(customMiddleware);

// 7. Routes
app.use('/api', apiRoutes);

// 8. 404 handler (after all routes)
app.use((req, res) => {
  res.status(404).json({ error: 'Not Found' });
});

// 9. Error handler (last)
app.use((err, req, res, next) => {
  // Error handling
});
```

### Built-in Middleware

**express.json()** - Parse JSON request bodies:
```javascript
app.use(express.json({ limit: '10mb' })); // Set size limit

// Now req.body contains parsed JSON
app.post('/api/data', (req, res) => {
  console.log(req.body); // { key: 'value' }
  res.json({ received: req.body });
});
```

**express.urlencoded()** - Parse URL-encoded bodies:
```javascript
app.use(express.urlencoded({ extended: true }));

// Handles form submissions
app.post('/form', (req, res) => {
  console.log(req.body); // { name: 'John', email: 'john@example.com' }
});
```

**express.static()** - Serve static files:
```javascript
// Serve files from 'public' directory
app.use(express.static('public'));

// With options
app.use(express.static('public', {
  maxAge: '1d', // Cache for 1 day
  etag: true,
  lastModified: true,
  index: 'index.html'
}));

// Multiple static directories
app.use(express.static('public'));
app.use('/uploads', express.static('uploads'));
```

### Custom Middleware

**Simple middleware**:
```javascript
// Logging middleware
const logger = (req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next(); // MUST call next() to continue
};

app.use(logger);
```

**Async middleware**:
```javascript
const asyncMiddleware = async (req, res, next) => {
  try {
    // Async operations
    const data = await fetchData();
    req.data = data;
    next();
  } catch (error) {
    next(error); // Pass errors to error handler
  }
};

app.use(asyncMiddleware);
```

**Conditional middleware**:
```javascript
const devOnly = (req, res, next) => {
  if (process.env.NODE_ENV === 'development') {
    return next();
  }
  res.status(403).json({ error: 'Development only' });
};

app.get('/debug', devOnly, (req, res) => {
  res.json({ debug: 'info' });
});
```

**Error handling middleware** (must have 4 parameters):
```javascript
app.use((err, req, res, next) => {
  console.error(err.stack);

  // Handle specific error types
  if (err.name === 'ValidationError') {
    return res.status(400).json({ error: err.message });
  }

  if (err.name === 'UnauthorizedError') {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  // Generic error
  res.status(err.status || 500).json({
    error: process.env.NODE_ENV === 'production'
      ? 'Internal Server Error'
      : err.message
  });
});
```

## Routing Best Practices

### Route Organization

**Inline routes** (small apps):
```javascript
app.get('/', (req, res) => res.send('Home'));
app.get('/about', (req, res) => res.send('About'));
app.post('/api/users', (req, res) => {/* ... */});
```

**Router modules** (recommended):
```javascript
// routes/api.js
const express = require('express');
const router = express.Router();

router.get('/users', (req, res) => {
  res.json({ users: [] });
});

router.post('/users', (req, res) => {
  res.json({ created: true });
});

module.exports = router;

// server.js
const apiRoutes = require('./routes/api');
app.use('/api', apiRoutes);
```

**Grouped routes by resource**:
```javascript
// routes/users.js
const router = express.Router();

router.get('/', getAllUsers);
router.get('/:id', getUser);
router.post('/', createUser);
router.put('/:id', updateUser);
router.delete('/:id', deleteUser);

module.exports = router;

// server.js
app.use('/api/users', require('./routes/users'));
```

### Route Parameters

**Path parameters**:
```javascript
app.get('/users/:id', (req, res) => {
  const userId = req.params.id;
  res.json({ userId });
});

// Multiple parameters
app.get('/users/:userId/posts/:postId', (req, res) => {
  const { userId, postId } = req.params;
  res.json({ userId, postId });
});
```

**Query parameters**:
```javascript
app.get('/search', (req, res) => {
  const { q, page, limit } = req.query;
  // /search?q=test&page=2&limit=10
  res.json({ query: q, page, limit });
});
```

**Route parameter validation**:
```javascript
// Middleware to validate ID
const validateId = (req, res, next) => {
  const id = parseInt(req.params.id);
  if (isNaN(id) || id < 1) {
    return res.status(400).json({ error: 'Invalid ID' });
  }
  req.params.id = id; // Convert to number
  next();
};

app.get('/users/:id', validateId, (req, res) => {
  // req.params.id is now a number
});
```

### HTTP Methods

**RESTful API routes**:
```javascript
const router = express.Router();

// GET - Retrieve resources
router.get('/items', (req, res) => {
  res.json({ items: [] });
});

router.get('/items/:id', (req, res) => {
  res.json({ item: {} });
});

// POST - Create resource
router.post('/items', (req, res) => {
  const newItem = req.body;
  res.status(201).json({ created: newItem });
});

// PUT - Update entire resource
router.put('/items/:id', (req, res) => {
  const updated = req.body;
  res.json({ updated });
});

// PATCH - Partial update
router.patch('/items/:id', (req, res) => {
  const updates = req.body;
  res.json({ updated: updates });
});

// DELETE - Remove resource
router.delete('/items/:id', (req, res) => {
  res.status(204).send(); // No content
});
```

## Async/Await Error Handling

### The Problem

**Without proper handling**:
```javascript
// BAD - Unhandled promise rejection
app.get('/users', async (req, res) => {
  const users = await fetchUsers(); // If this throws, app crashes
  res.json(users);
});
```

### Solutions

**Option 1: Try-catch in every route**:
```javascript
app.get('/users', async (req, res) => {
  try {
    const users = await fetchUsers();
    res.json(users);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
});
```

**Option 2: Async wrapper utility** (recommended):
```javascript
// utils/asyncHandler.js
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

module.exports = asyncHandler;

// Usage
const asyncHandler = require('./utils/asyncHandler');

app.get('/users', asyncHandler(async (req, res) => {
  const users = await fetchUsers(); // Errors automatically caught
  res.json(users);
}));
```

**Option 3: express-async-errors package**:
```javascript
// Install: npm install express-async-errors
require('express-async-errors'); // At the top of your app

// Now async errors are automatically caught
app.get('/users', async (req, res) => {
  const users = await fetchUsers();
  res.json(users);
});

// Error handler catches async errors
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.message });
});
```

### Custom Error Classes

```javascript
// errors/AppError.js
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error';
    this.isOperational = true;

    Error.captureStackTrace(this, this.constructor);
  }
}

module.exports = AppError;

// Usage
const AppError = require('./errors/AppError');

app.get('/users/:id', async (req, res, next) => {
  const user = await User.findById(req.params.id);

  if (!user) {
    return next(new AppError('User not found', 404));
  }

  res.json(user);
});

// Error handler
app.use((err, req, res, next) => {
  err.statusCode = err.statusCode || 500;
  err.status = err.status || 'error';

  res.status(err.statusCode).json({
    status: err.status,
    message: err.message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
});
```

## Request/Response Patterns

### Request Object

**Common properties**:
```javascript
app.post('/api/data', (req, res) => {
  // URL parameters
  const { id } = req.params; // /api/data/:id

  // Query string
  const { page, limit } = req.query; // /api/data?page=1&limit=10

  // Request body (requires express.json())
  const data = req.body;

  // Headers
  const contentType = req.get('Content-Type');
  const auth = req.headers.authorization;

  // Request info
  const method = req.method; // POST
  const path = req.path; // /api/data
  const url = req.url; // /api/data?page=1
  const protocol = req.protocol; // http or https
  const ip = req.ip; // Client IP

  // Cookies (requires cookie-parser)
  const sessionId = req.cookies.sessionId;
});
```

### Response Methods

**Send responses**:
```javascript
// Send JSON
res.json({ message: 'Success' });
res.status(201).json({ created: true });

// Send text
res.send('Plain text');

// Send HTML
res.send('<h1>HTML</h1>');

// Send file
res.sendFile('/path/to/file.pdf');

// Download file
res.download('/path/to/file.pdf', 'filename.pdf');

// Redirect
res.redirect('/new-url');
res.redirect(301, '/permanent-redirect');

// Set status
res.status(404).json({ error: 'Not Found' });
res.sendStatus(204); // No Content
```

**Set headers**:
```javascript
res.set('Content-Type', 'application/json');
res.set({
  'Content-Type': 'application/json',
  'X-Custom-Header': 'value'
});

// Set cookies
res.cookie('sessionId', '12345', {
  maxAge: 900000,
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
});

// Clear cookies
res.clearCookie('sessionId');
```

### Response Patterns

**Success responses**:
```javascript
// 200 OK - General success
res.json({ data: items });

// 201 Created - Resource created
res.status(201).json({ id: newId, created: true });

// 204 No Content - Success with no response body
res.status(204).send();
```

**Error responses**:
```javascript
// 400 Bad Request - Invalid input
res.status(400).json({ error: 'Invalid email format' });

// 401 Unauthorized - Authentication required
res.status(401).json({ error: 'Authentication required' });

// 403 Forbidden - Insufficient permissions
res.status(403).json({ error: 'Access denied' });

// 404 Not Found - Resource doesn't exist
res.status(404).json({ error: 'User not found' });

// 409 Conflict - Resource conflict
res.status(409).json({ error: 'Email already exists' });

// 422 Unprocessable Entity - Validation error
res.status(422).json({
  error: 'Validation failed',
  details: validationErrors
});

// 500 Internal Server Error - Server error
res.status(500).json({ error: 'Internal server error' });
```

## Proxy Patterns with Axios

### Basic Proxy

```javascript
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

app.post('/api/proxy', async (req, res) => {
  try {
    const response = await axios.post(
      'https://external-api.com/endpoint',
      req.body,
      { headers: { 'Content-Type': 'application/json' } }
    );

    res.json(response.data);
  } catch (error) {
    console.error('Proxy error:', error.message);
    res.status(error.response?.status || 500).json({
      error: 'Proxy request failed',
      details: error.response?.data || error.message
    });
  }
});
```

### Advanced Proxy with Headers

```javascript
app.post('/api/proxy', async (req, res) => {
  try {
    // Forward headers from client
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': req.headers.authorization,
      'User-Agent': req.headers['user-agent']
    };

    const response = await axios.post(
      'https://external-api.com/endpoint',
      req.body,
      {
        headers,
        timeout: 5000, // 5 second timeout
        validateStatus: (status) => status < 500 // Don't throw on 4xx
      }
    );

    // Forward response headers
    res.set('X-Response-Time', response.headers['x-response-time']);

    res.status(response.status).json(response.data);
  } catch (error) {
    if (error.code === 'ECONNABORTED') {
      return res.status(504).json({ error: 'Gateway timeout' });
    }

    res.status(error.response?.status || 500).json({
      error: 'Proxy request failed',
      originalError: error.response?.data || null
    });
  }
});
```

### Proxy with Retry Logic

```javascript
const axios = require('axios');
const axiosRetry = require('axios-retry');

// Configure axios with retry
axiosRetry(axios, {
  retries: 3,
  retryDelay: axiosRetry.exponentialDelay,
  retryCondition: (error) => {
    return axiosRetry.isNetworkOrIdempotentRequestError(error)
      || error.response?.status === 429; // Retry on rate limit
  }
});

app.post('/api/proxy', async (req, res) => {
  try {
    const response = await axios.post(
      'https://external-api.com/endpoint',
      req.body,
      {
        headers: { 'Content-Type': 'application/json' },
        'axios-retry': {
          retries: 3
        }
      }
    );

    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      error: 'Request failed after retries',
      details: error.response?.data
    });
  }
});
```

### Request Validation Before Proxying

```javascript
const Joi = require('joi');

const requestSchema = Joi.object({
  keyword: Joi.string().max(100),
  startDate: Joi.date().iso(),
  endDate: Joi.date().iso().min(Joi.ref('startDate'))
});

app.post('/api/search', async (req, res) => {
  // Validate request body
  const { error, value } = requestSchema.validate(req.body);

  if (error) {
    return res.status(400).json({
      error: 'Validation failed',
      details: error.details
    });
  }

  try {
    const response = await axios.post(
      'https://external-api.com/search',
      value, // Use validated data
      { headers: { 'Content-Type': 'application/json' } }
    );

    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      error: 'Search request failed',
      details: error.response?.data
    });
  }
});
```

## Security Best Practices

### Helmet - Security Headers

```javascript
const helmet = require('helmet');

// Basic usage
app.use(helmet());

// Custom configuration
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        scriptSrc: ["'self'"],
        imgSrc: ["'self'", "data:", "https:"]
      }
    },
    hsts: {
      maxAge: 31536000,
      includeSubDomains: true,
      preload: true
    }
  })
);
```

### CORS Configuration

```javascript
const cors = require('cors');

// Allow all origins (development only)
app.use(cors());

// Production configuration
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || 'https://myapp.com',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400 // 24 hours
}));

// Dynamic origin validation
app.use(cors({
  origin: (origin, callback) => {
    const allowedOrigins = ['https://myapp.com', 'https://app.example.com'];

    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  }
}));
```

### Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

// Global rate limit
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later.',
  standardHeaders: true,
  legacyHeaders: false
});

app.use(limiter);

// Route-specific rate limit
const strictLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: 'Too many login attempts, please try again later.'
});

app.post('/api/login', strictLimiter, (req, res) => {
  // Login logic
});
```

### Input Validation and Sanitization

```javascript
const { body, validationResult } = require('express-validator');

app.post('/api/users',
  // Validation middleware
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }).trim(),
  body('name').trim().escape(),

  (req, res) => {
    const errors = validationResult(req);

    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    // Proceed with validated data
    const { email, password, name } = req.body;
    res.json({ created: true });
  }
);
```

### Prevent Parameter Pollution

```javascript
const hpp = require('hpp');

// Prevent query parameter pollution
app.use(hpp());

// Whitelist certain parameters that can be arrays
app.use(hpp({
  whitelist: ['tags', 'categories']
}));
```

## Performance Optimization

### Compression

```javascript
const compression = require('compression');

app.use(compression({
  filter: (req, res) => {
    if (req.headers['x-no-compression']) {
      return false;
    }
    return compression.filter(req, res);
  },
  level: 6 // Compression level (0-9)
}));
```

### Caching Headers

```javascript
// Static files with caching
app.use(express.static('public', {
  maxAge: '1d',
  etag: true,
  lastModified: true
}));

// API responses with cache control
app.get('/api/data', (req, res) => {
  res.set('Cache-Control', 'public, max-age=300'); // 5 minutes
  res.json({ data: [] });
});

// No cache for dynamic data
app.get('/api/user/profile', (req, res) => {
  res.set('Cache-Control', 'no-store, no-cache, must-revalidate, private');
  res.json({ user: {} });
});
```

### Response Time Tracking

```javascript
const responseTime = require('response-time');

app.use(responseTime((req, res, time) => {
  console.log(`${req.method} ${req.url} - ${time.toFixed(2)}ms`);
}));

// Or send as header
app.use(responseTime());
```

### Connection Pooling (for databases)

```javascript
// Example with PostgreSQL
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});

app.get('/api/users', async (req, res) => {
  const client = await pool.connect();
  try {
    const result = await client.query('SELECT * FROM users');
    res.json(result.rows);
  } finally {
    client.release();
  }
});
```

## Production Configuration

### Environment-based Configuration

```javascript
const express = require('express');
const app = express();

const isDevelopment = process.env.NODE_ENV === 'development';
const isProduction = process.env.NODE_ENV === 'production';

// Development-only middleware
if (isDevelopment) {
  const morgan = require('morgan');
  app.use(morgan('dev'));
}

// Production-only middleware
if (isProduction) {
  app.use(require('compression')());
  app.use(require('helmet')());
}

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);

  res.status(err.status || 500).json({
    error: isProduction ? 'Internal Server Error' : err.message,
    ...(isDevelopment && { stack: err.stack })
  });
});
```

### Graceful Shutdown

```javascript
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

const server = app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

// Handle shutdown signals
const gracefulShutdown = (signal) => {
  console.log(`\n${signal} signal received: closing HTTP server`);

  server.close(() => {
    console.log('HTTP server closed');

    // Close database connections, cleanup resources
    // db.close();

    process.exit(0);
  });

  // Force close after 10 seconds
  setTimeout(() => {
    console.error('Forcing shutdown');
    process.exit(1);
  }, 10000);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  gracefulShutdown('uncaughtException');
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  gracefulShutdown('unhandledRejection');
});
```

### Logging

```javascript
const winston = require('winston');
const morgan = require('morgan');

// Winston logger
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}

// Morgan for HTTP logging
app.use(morgan('combined', {
  stream: {
    write: (message) => logger.info(message.trim())
  }
}));

// Use logger in routes
app.get('/api/data', async (req, res) => {
  try {
    const data = await fetchData();
    logger.info('Data fetched successfully');
    res.json(data);
  } catch (error) {
    logger.error('Error fetching data:', { error: error.message, stack: error.stack });
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

## Testing Express Applications

### Setup with Jest and Supertest

```javascript
// Install: npm install --save-dev jest supertest

// server.test.js
const request = require('supertest');
const app = require('./server');

describe('GET /', () => {
  it('responds with 200 status', async () => {
    const response = await request(app).get('/');
    expect(response.status).toBe(200);
  });

  it('responds with JSON', async () => {
    const response = await request(app).get('/api/users');
    expect(response.headers['content-type']).toMatch(/json/);
  });
});

describe('POST /api/users', () => {
  it('creates a user with valid data', async () => {
    const userData = { name: 'John', email: 'john@example.com' };

    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .set('Content-Type', 'application/json');

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
  });

  it('rejects invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'invalid' });

    expect(response.status).toBe(400);
  });
});
```

### Mocking External APIs

```javascript
const axios = require('axios');
jest.mock('axios');

describe('POST /api/proxy', () => {
  it('proxies request successfully', async () => {
    const mockData = { result: 'success' };
    axios.post.mockResolvedValue({ data: mockData });

    const response = await request(app)
      .post('/api/proxy')
      .send({ query: 'test' });

    expect(response.status).toBe(200);
    expect(response.body).toEqual(mockData);
    expect(axios.post).toHaveBeenCalledWith(
      expect.any(String),
      { query: 'test' },
      expect.any(Object)
    );
  });

  it('handles proxy errors', async () => {
    axios.post.mockRejectedValue(new Error('Network error'));

    const response = await request(app)
      .post('/api/proxy')
      .send({ query: 'test' });

    expect(response.status).toBe(500);
    expect(response.body).toHaveProperty('error');
  });
});
```

## Common Express Issues

### Headers Already Sent

**Problem**:
```javascript
// BAD - sends headers twice
app.get('/data', (req, res) => {
  res.json({ data: [] });
  res.status(200).send(); // Error: headers already sent
});
```

**Solution**:
```javascript
// GOOD - single response
app.get('/data', (req, res) => {
  return res.json({ data: [] }); // Use return to prevent further execution
});

// Or use else
app.get('/data', (req, res) => {
  if (error) {
    return res.status(500).json({ error: 'Failed' });
  } else {
    return res.json({ data: [] });
  }
});
```

### Middleware Not Running

**Problem**: Middleware defined after routes
```javascript
// BAD - middleware defined after route
app.get('/api/data', (req, res) => {
  res.json({ data: req.user }); // req.user is undefined
});

app.use(authMiddleware); // Too late!
```

**Solution**: Define middleware before routes
```javascript
// GOOD - middleware before routes
app.use(authMiddleware);

app.get('/api/data', (req, res) => {
  res.json({ data: req.user }); // req.user exists
});
```

### Forgot to call next()

**Problem**:
```javascript
// BAD - middleware doesn't call next()
app.use((req, res) => {
  console.log('Request received');
  // Request hangs here!
});
```

**Solution**:
```javascript
// GOOD - always call next()
app.use((req, res, next) => {
  console.log('Request received');
  next(); // Continue to next middleware
});
```

### CORS Errors

**Problem**: Missing CORS headers
```javascript
// Frontend gets CORS error
```

**Solution**:
```javascript
const cors = require('cors');
app.use(cors());

// Or manual headers
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }

  next();
});
```

### Body Parser Not Working

**Problem**: req.body is undefined
```javascript
app.post('/api/data', (req, res) => {
  console.log(req.body); // undefined
});
```

**Solution**: Add body parser middleware
```javascript
app.use(express.json()); // Parse JSON
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded

app.post('/api/data', (req, res) => {
  console.log(req.body); // Now it works
});
```

## Best Practices Summary

### Application Structure
1. Use environment variables for configuration
2. Implement graceful shutdown
3. Use middleware in correct order
4. Separate routes into modules
5. Implement proper error handling

### Security
1. Always use helmet for security headers
2. Configure CORS appropriately
3. Implement rate limiting
4. Validate and sanitize all inputs
5. Never expose sensitive errors in production
6. Use HTTPS in production
7. Keep dependencies updated

### Performance
1. Use compression middleware
2. Implement caching where appropriate
3. Use connection pooling for databases
4. Minimize middleware stack
5. Use async/await instead of callbacks

### Error Handling
1. Use async error wrapper or express-async-errors
2. Create custom error classes
3. Centralize error handling middleware
4. Log errors appropriately
5. Never crash on unhandled errors

### Code Quality
1. Use consistent naming conventions
2. Keep route handlers small and focused
3. Extract business logic into separate modules
4. Write tests for routes and middleware
5. Use TypeScript for larger applications

### Production Readiness
1. Set NODE_ENV=production
2. Implement logging (Winston, Morgan)
3. Use process managers (PM2, Docker)
4. Monitor application health
5. Implement graceful shutdown
6. Handle uncaught exceptions

## Resources

- Express.js Documentation: https://expressjs.com/
- Node.js Best Practices: https://github.com/goldbergyoni/nodebestpractices
- Express Security: https://expressjs.com/en/advanced/best-practice-security.html
- Helmet Documentation: https://helmetjs.github.io/
- Axios Documentation: https://axios-http.com/docs/intro
