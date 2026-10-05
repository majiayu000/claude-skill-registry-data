---
name: fastify
description: Fastify schema validation, hooks, plugins, serialization. Use when building Fastify apps.
---

## fastify

Build high-performance Node.js APIs with Fastify.

### Schema Validation
- JSON Schema for request validation via `schema` option
- Fastify serializes responses automatically from schema
- Supports Ajv custom validators and formats

### Hooks & Plugins
- Request lifecycle hooks: onRequest, preHandler, onSend, onResponse
- Encapsulated plugin system via fastify-plugin
- Decorators to extend Fastify instance

### Serialization
- Automatic JSON schema-based serialization
- Custom serializers for non-JSON formats
- Higher throughput than JSON.stringify

### TypeScript
- Full TypeScript support with auto-generated types
- Type providers for validation (Zod, TypeBox)
- Strict typing for request/reply

### Best Practices
- Encapsulate routes in plugins
- Use pino logger (built-in)
- Content Type Parser for non-JSON bodies
- Testing with fastify.inject() (no supertest needed)
- Compression via @fastify/compress
