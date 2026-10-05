---
name: express
description: Express.js middleware, routing, REST API, error handling. Use when building Express apps or APIs.
---

## express

Build Express.js web servers and REST APIs.

### Middleware System
- Chain request handlers via `app.use()` and `app.VERB()`
- Order matters: middleware runs top-down
- Error middleware has 4 params: `(err, req, res, next)`

### Routing
- Express Router for modular route groups
- Route params `:id` with `req.params`
- Query strings with `req.query`
- Body parsing via `express.json()` and `express.urlencoded()`

### Security
- helmet for HTTP headers
- cors for cross-origin requests
- Rate limiting with express-rate-limit
- Input validation with express-validator or Joi

### Best Practices
- Separate routes, controllers, services layers
- Centralized error handler middleware
- Async error wrapper to catch rejected promises
- Test with supertest + jest or vitest
- Static files via express.static for assets
