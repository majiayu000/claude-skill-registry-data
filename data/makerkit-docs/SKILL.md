---
name: makerkit-docs
description: >
  Consulta la documentación oficial de MakerKit (next-supabase-turbo) bajo demanda.
  Usa cuando necesites información sobre patrones, configuración o APIs de MakerKit
  que no esté en el código local. Incluye índice completo de 150 páginas.
allowed-tools: WebFetch, Read
---

# MakerKit Documentation Access

## Anuncio

"Consultando documentación oficial de MakerKit para [tema]."

## Cuándo Usar

- Cuando necesites saber "cómo hace MakerKit X"
- Cuando encuentres código que no entiendes y el CLAUDE.md local no ayuda
- Cuando planifiques una feature y quieras validar el approach oficial
- Cuando el MCP no tenga la información (patrones conceptuales vs código)
- Cuando configures billing, auth, emails, o features complejas

## Cuándo NO Usar

- Para introspección de código local (usar MCP)
- Para ver qué componentes existen en el proyecto (usar `components_search()`)
- Para entender la DB del proyecto (usar `get_database_summary()`)

---

## URL Base

```
https://makerkit.dev/docs/next-supabase-turbo
```

---

## Índice Completo

El archivo `INDEX.json` en este directorio contiene las **150 páginas** de documentación organizadas en 21 secciones.

### Cómo Usar el Índice

```typescript
// Leer el índice para encontrar la página correcta
Read(".claude/skills/makerkit-docs/INDEX.json")

// Buscar la sección y página que necesitas
// Construir URL: base_url + path
```

### Resumen de Secciones

| Sección | Slug | Páginas | Temas Clave |
|---------|------|---------|-------------|
| Installation | `installation` | 16 | Setup, comandos, migración, MCP |
| Configuration | `configuration` | 7 | Env vars, auth config, feature flags |
| Customization | `customization` | 5 | Tailwind, theme, logo, fonts |
| Development | `development` | 17 | DB architecture, migrations, RBAC, testing |
| API | `api` | 8 | Account, Team, Auth, Workspace APIs |
| Data Fetching | `data-fetching` | 7 | Supabase clients, Server Actions, React Query |
| Billing | `billing` | 12 | Stripe, Lemon Squeezy, Paddle, webhooks |
| Content | `content` | 6 | CMS, Keystatic, Wordpress |
| UI Components | `components` | 14 | Shadcn, forms, tables, marketing |
| Notifications | `notifications` | 2 | Config y envío |
| Translations | `translations` | 3 | i18n, language selector |
| Emails | `emails` | 6 | Config, templates, auth emails |
| Monitoring | `monitoring` | 5 | Sentry, Signoz, PostHog |
| Super Admin | `admin` | 1 | Adding super admin |
| Analytics | `analytics` | 5 | GA, PostHog, Umami, custom |
| Security | `security` | 4 | Next.js practices, RLS, CSP |
| Going to Production | `going-to-production` | 10 | Deploy Vercel, Cloudflare, Docker |
| Plugins | `plugins` | 6 | Waitlist, Roadmap, AI Chatbot |
| Recipes | `recipes` | 7 | Team/Personal accounts, checkout, data model |
| Developer Tools | `dev-tools` | 2 | Env vars, translations editor |
| Troubleshooting | `troubleshooting` | 7 | Install, auth, billing, deploy issues |

---

## Páginas Más Útiles (Acceso Rápido)

### Para Desarrollo de Features

| Tema | Path |
|------|------|
| Database Architecture | `/development/database-architecture` |
| Extending DB Schema | `/development/database-schema` |
| Database Functions | `/development/database-functions` |
| RBAC: Roles & Permissions | `/development/permissions-and-roles` |
| Loading Data | `/development/loading-data-from-database` |
| Writing Data | `/development/writing-data-to-database` |
| Projects Data Model (Recipe) | `/recipes/projects-data-model` |

### Para Data Fetching

| Tema | Path |
|------|------|
| Supabase Clients | `/data-fetching/supabase-clients` |
| Server Actions | `/data-fetching/server-actions` |
| Server Components | `/data-fetching/server-components` |
| Route Handlers | `/data-fetching/route-handlers` |
| React Query | `/data-fetching/react-query` |

### Para APIs

| Tema | Path |
|------|------|
| Account API | `/api/account-api` |
| Team Account API | `/api/team-account-api` |
| Authentication API | `/api/authentication-api` |
| Feature Policies API | `/api/policies-api` |

### Para Billing

| Tema | Path |
|------|------|
| How Billing Works | `/billing/overview` |
| Billing Schema | `/billing/billing-schema` |
| Stripe | `/billing/stripe` |
| Lemon Squeezy | `/billing/lemon-squeezy` |
| Per Seat Billing | `/billing/per-seat-billing` |
| Handling Webhooks | `/billing/billing-webhooks` |

### Para Seguridad

| Tema | Path |
|------|------|
| Next.js Best Practices | `/security/nextjs-best-practices` |
| Row Level Security | `/security/row-level-security` |
| Data Validation | `/security/data-validation` |

### Para Deploy

| Tema | Path |
|------|------|
| Production Checklist | `/going-to-production/checklist` |
| Deploy Supabase | `/going-to-production/supabase` |
| Deploy to Vercel | `/going-to-production/vercel` |
| Deploy to Cloudflare | `/going-to-production/cloudflare` |

---

## Cómo Consultar

### Método 1: URL Directa (si conoces el path)

```
WebFetch(
  url: "https://makerkit.dev/docs/next-supabase-turbo/development/permissions-and-roles",
  prompt: "Extrae el patrón para implementar RBAC con roles y permisos"
)
```

### Método 2: Buscar en Índice Primero

```
1. Read(".claude/skills/makerkit-docs/INDEX.json")
2. Buscar la sección relevante
3. WebFetch con el path encontrado
```

### Método 3: Explorar una Sección

```
WebFetch(
  url: "https://makerkit.dev/docs/next-supabase-turbo/billing/overview",
  prompt: "Lista todas las subsecciones de billing disponibles en el menú lateral"
)
```

---

## Ejemplos de Uso

### Ejemplo 1: Implementar RBAC

```
WebFetch(
  url: "https://makerkit.dev/docs/next-supabase-turbo/development/permissions-and-roles",
  prompt: "Extrae: estructura de tablas para roles/permisos, funciones SQL, y cómo verificar permisos en el código"
)
```

### Ejemplo 2: Configurar Stripe

```
WebFetch(
  url: "https://makerkit.dev/docs/next-supabase-turbo/billing/stripe",
  prompt: "Lista: variables de entorno necesarias, configuración de webhooks, y eventos a escuchar"
)
```

### Ejemplo 3: Data Model para Proyectos

```
WebFetch(
  url: "https://makerkit.dev/docs/next-supabase-turbo/recipes/projects-data-model",
  prompt: "Extrae: schema SQL completo, políticas RLS, y componentes UI necesarios"
)
```

### Ejemplo 4: Server Actions Pattern

```
WebFetch(
  url: "https://makerkit.dev/docs/next-supabase-turbo/data-fetching/server-actions",
  prompt: "Extrae: cómo usar enhanceAction, validación con Zod, y manejo de errores"
)
```

### Ejemplo 5: Troubleshooting Auth

```
WebFetch(
  url: "https://makerkit.dev/docs/next-supabase-turbo/troubleshooting/troubleshooting-authentication",
  prompt: "Lista problemas comunes de autenticación y sus soluciones"
)
```

---

## Integración con Otros Tools

### Con makerkit-architecture

Cuando diseñes features:
1. **MCP primero:** `find_complete_features()`, `analyze_feature_pattern()`
2. **Docs para validar:** Usa este skill para confirmar patrones oficiales
3. **Combina:** Blueprint informado por código real + docs oficiales

### Con MCP Database Tools

| Si necesitas... | Usa... |
|-----------------|--------|
| Ver tablas del proyecto | `get_database_summary()` |
| Entender patrones de tablas | Este skill → `/development/database-architecture` |
| Generar RLS | `generate_rls_policy()` |
| Entender RLS patterns | Este skill → `/security/row-level-security` |

---

## Notas Importantes

1. **URLs específicas:** No existen páginas índice como `/billing`. Siempre usa paths completos como `/billing/overview`

2. **Índice local:** El archivo `INDEX.json` tiene las 150 URLs validadas. Consúltalo si no encuentras algo.

3. **Actualización:** El índice fue extraído el 2026-01-01. Si MakerKit reorganiza sus docs, puede necesitar actualización.

4. **Contenido dinámico:** Algunas páginas cargan contenido con JavaScript. Si WebFetch retorna solo navegación, intenta con un prompt más específico.

---

## Troubleshooting del Skill

| Problema | Solución |
|----------|----------|
| 404 Not Found | Verificar path en INDEX.json |
| Contenido incompleto | Usar prompt más específico |
| Solo navegación | La página usa JS; probar otra subsección |
| Info desactualizada | WebFetch es en tiempo real, el índice puede estar desactualizado |
