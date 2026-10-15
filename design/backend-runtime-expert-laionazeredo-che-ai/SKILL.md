---
name: "backend-runtime-expert"
description: "Master guide for modern backend runtimes and frameworks. Covers NestJS, Deno, Payload CMS, and server-side TypeScript patterns."
---

# Backend Runtime Expert Guide

This skill provides the standards for building scalable, enterprise-grade backend services across multiple runtimes.

## 🦅 NestJS (Node.js)
- **Modular Design**: Use `Modules` to group related functionality. Follow the Dependency Injection pattern.
- **Controllers & Services**: Keep controllers thin. Put business logic in services.
- **Pipes & Guards**: Use Pipes for validation/transformation and Guards for authentication/authorization.

## 🦕 Deno
- **Security**: Leverage Deno's permission system (e.g., `--allow-net`, `--allow-read`).
- **Standard Library**: Prefer the Deno standard library for basic utilities.
- **Deploy**: Use Deno Deploy for edge computing and low-latency execution.

## 📄 Payload CMS
- **Collections & Globals**: Define clear schemas for content. Use hooks for side effects.
- **Access Control**: Implement granular permissions per collection and field.
- **Customization**: Extend the admin UI using custom React components.

## 🔗 References
- [NestJS Documentation](https://docs.nestjs.com/)
- [Deno Documentation](https://deno.land/)
- [Payload CMS Documentation](https://payloadcms.com/docs)
